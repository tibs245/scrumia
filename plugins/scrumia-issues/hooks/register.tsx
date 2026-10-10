import type { EngineInterface, PromptOrigin, Register } from 'claude-code'

type Issue = {
  number: number
  title?: string
  isTakenIntoAccount: boolean
  isAssessed: boolean
  isReminded: boolean
  status: string
  remaining: string
}

type Ledger = { sessionId: string; touchedAt: number; issues: Issue[] }

type Vocabulary = { statuses: string[]; done: string; isFromTracker: boolean; note?: string }

const PANE = 'issues'
const TRACK_TOOL = 'mcp__scrumia-issues__track_issue'
const TRACKER_MODULE = 'scrumia-github-project'
const UNKNOWN = 'Unknown'
const DEFAULT_COLUMNS = ['Backlog', 'Ready for dev', 'To dev', 'In progress', 'In review', 'Done']
const LEDGER_PREFIX = 'ledger:'
const KEEP_SESSIONS = 30
const NOTE_MARK = '[scrumia-issues]'
const TYPED_BY_PERSON: PromptOrigin['kind'][] = ['composer', 'bridge']
const MENTION = /(?<![\w&/])#(\d{1,6})\b/g
const CODE = /```[\s\S]*?```|`[^`\n]*`/g
const READ_TIMEOUT_MS = 10_000

let queue: Promise<unknown> = Promise.resolve()
let vocabulary: Promise<Vocabulary> | undefined

const defaults = (note?: string): Vocabulary => ({
  statuses: [...DEFAULT_COLUMNS, UNKNOWN],
  done: 'Done',
  isFromTracker: false,
  note,
})

const isText = (value: unknown): value is string => typeof value === 'string' && value.trim() !== ''

async function readSettings($: EngineInterface, cwd: string | undefined, args: string[]) {
  const ran = await $.process.run(['scrumia-extends', ...args], { cwd, timeoutMs: READ_TIMEOUT_MS })
  if (ran.exitCode !== 0) {
    throw new Error(`scrumia-extends ${args[0]} exited with ${ran.exitCode}`)
  }

  return JSON.parse(ran.stdout) as unknown
}

async function readVocabulary($: EngineInterface, cwd: string | undefined): Promise<Vocabulary> {
  try {
    const modules = (await readSettings($, cwd, ['--modules', '--json'])) as { key: string; module: string; state?: string }[]
    const tracker = modules.find(one => one.module === TRACKER_MODULE && one.state !== 'absent')
    if (tracker === undefined) {
      return defaults(`no ${TRACKER_MODULE} module is declared`)
    }
    const settings = (await readSettings($, cwd, ['--settings', tracker.key])) as {
      columns?: unknown
      board?: { options?: Record<string, unknown>; flow?: { done?: unknown } }
    }
    const columns = Array.isArray(settings.columns) ? settings.columns : Object.keys(settings.board?.options ?? {})
    if (columns.length === 0 || !columns.every(isText)) {
      return defaults('the tracker declares no columns')
    }
    const named = columns as string[]
    const done = settings.board?.flow?.done

    return {
      statuses: named.includes(UNKNOWN) ? named : [...named, UNKNOWN],
      done: isText(done) ? done : named[named.length - 1]!,
      isFromTracker: true,
    }
  } catch (failure) {
    return defaults(failure instanceof Error ? failure.message : 'the tracker settings could not be read')
  }
}

function vocabularyOf($: EngineInterface, cwd?: string): Promise<Vocabulary> {
  vocabulary ??= readVocabulary($, cwd)

  return vocabulary
}

const statusOf = (given: string, known: Vocabulary) =>
  known.statuses.find(one => one.toLowerCase() === given.trim().toLowerCase())

function problemWith(input: Record<string, unknown>, known: Vocabulary): string | undefined {
  const { number, title, isTakenIntoAccount, status, remaining } = input
  if (typeof number !== 'number' || !Number.isInteger(number) || number < 1) {
    return 'number must be an integer from 1, without #'
  }
  if (title !== undefined && typeof title !== 'string') {
    return 'title must be text'
  }
  if (typeof isTakenIntoAccount !== 'boolean') {
    return 'isTakenIntoAccount must be true or false'
  }
  if (typeof status !== 'string' || statusOf(status, known) === undefined) {
    return `status must be one of: ${known.statuses.join(', ')}`
  }
  if (!isText(remaining)) {
    return 'remaining must be non-empty text: say what is left to do, or "nothing"'
  }

  return undefined
}

const isTypedByPerson = (origin: PromptOrigin | undefined) =>
  origin !== undefined && (TYPED_BY_PERSON.includes(origin.kind) || (origin.kind === 'plugin' && origin.asUser === true))

function mentionsIn(text: string): number[] {
  const own = (line: string) => line.includes(NOTE_MARK)
  const kept = text
    .split('\n')
    .filter(line => !own(line))
    .join('\n')
    .replace(CODE, ' ')
  const numbers = [...kept.matchAll(MENTION)].map(match => Number(match[1])).filter(number => number >= 1)

  return [...new Set(numbers)]
}

const withMentions = (issues: Issue[], numbers: number[]): Issue[] => {
  const known = new Set(issues.map(one => one.number))
  const fresh = numbers.filter(number => !known.has(number))

  return [
    ...issues,
    ...fresh.map(
      (number): Issue => ({
        number,
        isTakenIntoAccount: false,
        isAssessed: false,
        isReminded: false,
        status: UNKNOWN,
        remaining: 'Not assessed yet',
      }),
    ),
  ]
}

const reminderNote = (numbers: number[]) =>
  `${NOTE_MARK} Tickets named and not yet recorded: ${numbers.map(number => `#${number}`).join(', ')}. Read each one's status on the board, then record it with track_issue with what remains.`

const keyOf = (sessionId: string) => `${LEDGER_PREFIX}${sessionId}`

async function load($: EngineInterface): Promise<Ledger> {
  const sessionId = await $.session.id()
  const stored = (await $.store.get(keyOf(sessionId))) as Ledger | undefined

  return stored ?? { sessionId, touchedAt: 0, issues: [] }
}

async function forget($: EngineInterface, current: string) {
  const keys = (await $.store.keys()).filter(key => key.startsWith(LEDGER_PREFIX))
  if (keys.length <= KEEP_SESSIONS) {
    return
  }
  const dated = await Promise.all(
    keys.map(async key => ({ key, touchedAt: ((await $.store.get(key)) as Ledger | undefined)?.touchedAt ?? 0 })),
  )
  const oldest = dated.filter(one => one.key !== keyOf(current)).sort((first, second) => first.touchedAt - second.touchedAt)
  for (const one of oldest.slice(0, keys.length - KEEP_SESSIONS)) {
    await $.store.delete(one.key)
  }
}

function change($: EngineInterface, edit: (issues: Issue[]) => Issue[], isRedrawn = true): Promise<Ledger> {
  const run = queue.then(async () => {
    const ledger = await load($)
    const next = { ...ledger, touchedAt: await $.clock.now(), issues: edit(ledger.issues) }
    await $.store.set(keyOf(next.sessionId), next)
    await forget($, next.sessionId)
    if (isRedrawn) {
      $.ui.invalidate('ui.render')
    }

    return next
  })
  queue = run.catch(() => undefined)

  return run
}

const statusColor = (status: string) =>
  ({
    Done: 'success',
    'In review': 'suggestion',
    'In progress': 'warning',
    Unknown: 'error',
  })[status] ?? 'subtle'

export const register: Register = on => {
  queue = Promise.resolve()
  vocabulary = undefined

  on('session.start', async ($, e, next) => {
    const known = await vocabularyOf($, e.cwd)
    await $.command.register({
      name: 'issues',
      description: 'Show the tickets mentioned in this session and what remains on each',
    })
    await $.tool.register({
      name: 'track_issue',
      isDeferred: false,
      description:
        'Record or update a ticket this session has mentioned. Call it whenever you mention, start, advance or finish work on a ticket by its number, and whenever a ticket is listed as named but not yet recorded. Read the ticket\'s status on the board first (scrumia-board) and report that status: this tool does not check the board. Say whether this session took the ticket into account (worked on or covered it, not merely named it), and precisely what remains to do, so the person can tell its state from that sentence alone. The call is refused when a field is missing or malformed: read the reason and call again.',
      inputSchema: {
        type: 'object',
        properties: {
          number: { type: 'integer', minimum: 1, description: 'Ticket number, without #' },
          title: { type: 'string', description: 'Short title, optional' },
          isTakenIntoAccount: {
            type: 'boolean',
            description: 'true when this session worked on or covered the ticket, false when it was only mentioned',
          },
          status: { type: 'string', enum: known.statuses, description: 'Its column on the board, or Unknown' },
          remaining: {
            type: 'string',
            description: 'Exactly what remains to do for this ticket; write "nothing" when it is done',
          },
        },
        required: ['number', 'isTakenIntoAccount', 'status', 'remaining'],
      },
    })

    return next(e)
  })

  on('tool.call', { tool: TRACK_TOOL }, async ($, e) => {
    const input = e as unknown as Record<string, unknown>
    const known = await vocabularyOf($)
    const problem = problemWith(input, known)
    if (problem !== undefined) {
      return { deny: `scrumia-issues: ${problem}` }
    }
    const number = input.number as number
    const status = statusOf(input.status as string, known)!
    const given = {
      title: input.title as string | undefined,
      isTakenIntoAccount: input.isTakenIntoAccount as boolean,
      isAssessed: true,
      status,
      remaining: (input.remaining as string).trim(),
    }
    const ledger = await change($, issues => {
      const rest = issues.some(one => one.number === number)
        ? issues
        : withMentions(issues, [number])

      return rest.map(one =>
        one.number === number ? { ...one, ...given, title: given.title ?? one.title, isReminded: true } : one,
      )
    })
    const open = ledger.issues.filter(one => one.status !== known.done).length

    return { result: `#${number} recorded as ${status}. ${open} open of ${ledger.issues.length} in this session.` }
  })

  on('prompt.submit', async ($, e, next) => {
    const typed = isTypedByPerson(e.origin) ? mentionsIn(e.text) : []
    const ledger =
      typed.length === 0 ? await load($) : await change($, issues => withMentions(issues, typed))
    const waiting = ledger.issues.filter(one => !one.isAssessed && !one.isReminded).map(one => one.number)
    if (waiting.length === 0 || e.origin === undefined || !isTypedByPerson(e.origin)) {
      return next(e)
    }
    const ran = await next({ ...e, context: [...(e.context ?? []), reminderNote(waiting)] })
    if (ran.drop === undefined) {
      await change($, issues => issues.map(one => (waiting.includes(one.number) ? { ...one, isReminded: true } : one)), false)
    }

    return ran
  }).catch(($, e, next) => next(e))

  on('turn.complete', async ($, e, next) => {
    const named = e.reason === 'answer' ? mentionsIn(e.answer) : []
    if (named.length > 0) {
      await change($, issues => withMentions(issues, named))
    }

    return next(e)
  })

  on('command.run', { command: 'issues' }, async $ => {
    await $.ui.open({ id: PANE, title: 'Issues' })

    return { text: 'Issues pane opened.' }
  })

  on('ui.render', { component: 'Pane', requestId: PANE }, async ($, e) => {
    const { Box, Text } = $.ui.resolve(e)
    const known = await vocabularyOf($)
    const { issues } = await load($)
    const isOpen = (one: Issue) => one.status !== known.done
    const sorted = [...issues].sort(
      (first, second) => Number(isOpen(second)) - Number(isOpen(first)) || first.number - second.number,
    )
    const taken = issues.filter(one => one.isTakenIntoAccount).length
    const open = issues.filter(isOpen).length
    const vocabularyLine = known.isFromTracker
      ? `Statuses: the tracker's columns (${known.statuses.join(', ')})`
      : `Statuses: the default columns, the tracker's could not be read (${known.note ?? 'unknown reason'})`

    if (issues.length === 0) {
      return (
        <Box flexDirection="column">
          <Text dimColor>No ticket mentioned in this session yet.</Text>
          <Text dimColor>{vocabularyLine}</Text>
        </Box>
      )
    }

    return (
      <Box flexDirection="column" gap={1}>
        <Box gap={2}>
          <Text bold>Issues</Text>
          <Text dimColor>
            {issues.length} mentioned · {taken} taken into account · {open} open
          </Text>
        </Box>
        <Text dimColor>{vocabularyLine}</Text>
        <Box gap={2}>
          <Box width={8}>
            <Text dimColor bold>
              TICKET
            </Text>
          </Box>
          <Box width={11}>
            <Text dimColor bold>
              IN SESSION
            </Text>
          </Box>
          <Box width={14}>
            <Text dimColor bold>
              STATUS
            </Text>
          </Box>
          <Box flexGrow={1}>
            <Text dimColor bold>
              REMAINING
            </Text>
          </Box>
        </Box>
        {sorted.map(one => (
          <Box key={`issue-${one.number}`} gap={2}>
            <Box width={8}>
              <Text bold>#{one.number}</Text>
            </Box>
            <Box width={11}>
              <Text color={one.isTakenIntoAccount ? 'success' : undefined} dimColor={!one.isTakenIntoAccount}>
                {one.isAssessed ? (one.isTakenIntoAccount ? '✓ yes' : 'no') : '?'}
              </Text>
            </Box>
            <Box width={14}>
              <Text color={statusColor(one.status)} bold>
                {one.status}
              </Text>
            </Box>
            <Box flexGrow={1} flexDirection="column">
              {one.title && <Text dimColor>{one.title}</Text>}
              <Text wrap="wrap" dimColor={!one.isAssessed}>
                {one.remaining}
              </Text>
            </Box>
          </Box>
        ))}
      </Box>
    )
  })
}
