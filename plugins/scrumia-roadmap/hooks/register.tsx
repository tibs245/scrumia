import type { EngineInterface, Register } from 'claude-code'

type SourceKind = 'milestone' | 'tickets' | 'column' | 'other'

type SprintState = 'planned' | 'running' | 'done'

type Ticket = { number: number; title: string; description: string; status: string }

type Sprint = {
  name: string
  order: number
  source?: { kind: SourceKind; reference: string }
  objective: string
  testableAtEnd?: string[]
  nothingTestable?: boolean
  state?: SprintState
  tickets?: Ticket[]
  resolvedAt?: number
  recordedIn?: string
}

type Project = { sprints: Sprint[] }

type Filter = 'all' | SprintState

type Vocabulary = { statuses: string[]; done: string; isFromTracker: boolean; note?: string }

const PANE = 'roadmap'
const PLAN_TOOL = 'mcp__scrumia-roadmap__plan_sprint'
const KINDS: SourceKind[] = ['milestone', 'tickets', 'column', 'other']
const STATES: SprintState[] = ['planned', 'running', 'done']
const TRACKER_MODULE = 'scrumia-github-project'
const UNKNOWN = 'Unknown'
const DEFAULT_COLUMNS = ['Backlog', 'Ready for dev', 'To dev', 'In progress', 'In review', 'Done']
const READ_TIMEOUT_MS = 10_000

let queue: Promise<unknown> = Promise.resolve()
let vocabulary: Promise<Vocabulary> | undefined
let projectDirectory: string | undefined
const view: { filter: Filter } = { filter: 'all' }

const defaults = (note?: string): Vocabulary => ({
  statuses: [...DEFAULT_COLUMNS, UNKNOWN],
  done: 'Done',
  isFromTracker: false,
  note,
})

const isText = (value: unknown): value is string => typeof value === 'string' && value.trim() !== ''
const isRecord = (value: unknown): value is Record<string, unknown> =>
  typeof value === 'object' && value !== null && !Array.isArray(value)

const stateOf = (one: Sprint): SprintState => (one.state !== undefined && STATES.includes(one.state) ? one.state : 'planned')
const ticketsOf = (one: Sprint): Ticket[] => (Array.isArray(one.tickets) ? one.tickets : [])
const same = (first: string, second: string) => String(first).trim().toLowerCase() === String(second).trim().toLowerCase()
const isTicketDone = (one: Ticket, known: Vocabulary) => same(one.status, known.done)
const statusColor = (one: Ticket, known: Vocabulary) => {
  if (isTicketDone(one, known)) {
    return 'success'
  }
  if (same(one.status, UNKNOWN)) {
    return 'error'
  }
  const columns = known.statuses.filter(column => column !== UNKNOWN)
  const place = columns.findIndex(column => same(column, one.status))
  const closing = columns.findIndex(column => same(column, known.done))

  return place > 0 && place < closing ? 'warning' : 'subtle'
}
const statusOf = (given: string, known: Vocabulary) => known.statuses.find(one => same(one, given))

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
  if (vocabulary === undefined) {
    const reading = readVocabulary($, cwd ?? projectDirectory)
    vocabulary = reading
    // a failed read serves the defaults for this call only, so the next call reads again
    void reading.then(known => {
      if (!known.isFromTracker && vocabulary === reading) {
        vocabulary = undefined
      }
    })
  }

  return vocabulary
}

const notDoneCount = (one: Sprint, known: Vocabulary) => ticketsOf(one).filter(ticket => !isTicketDone(ticket, known)).length
function mismatchOf(one: Sprint, known: Vocabulary): string | undefined {
  const total = ticketsOf(one).length
  const open = notDoneCount(one, known)
  if (stateOf(one) === 'done' && open > 0) {
    return `state done, ${open} ticket(s) not done`
  }
  if (stateOf(one) === 'planned' && total > 0 && open === 0) {
    return `state planned, all ${total} ticket(s) done`
  }

  return undefined
}
const stateColor = (state: SprintState) => (state === 'done' ? 'success' : state === 'running' ? 'warning' : 'suggestion')
const byOrder = (first: Sprint, second: Sprint) => first.order - second.order || first.name.localeCompare(second.name)
const whenText = (at: number | undefined) =>
  at === undefined ? 'at an unknown time' : `${new Date(at).toISOString().slice(0, 16).replace('T', ' ')} UTC`

function problemWith(input: Record<string, unknown>, known: Vocabulary): string | undefined {
  const { name, order, source, objective, testableAtEnd, nothingTestable, state, tickets } = input
  if (!isText(name)) {
    return 'name must be non-empty text'
  }
  if (typeof order !== 'number' || !Number.isInteger(order)) {
    return 'order must be an integer'
  }
  if (!isRecord(source) || !KINDS.includes(source.kind as SourceKind) || !isText(source.reference)) {
    return `source must be { kind: ${KINDS.join('|')}, reference: non-empty text }`
  }
  if (!isText(objective)) {
    return 'objective must be non-empty text'
  }
  if (!Array.isArray(testableAtEnd) || !testableAtEnd.every(isText)) {
    return 'testableAtEnd must be an array of non-empty texts a person can try'
  }
  if (nothingTestable !== undefined && typeof nothingTestable !== 'boolean') {
    return 'nothingTestable must be true or false'
  }
  if (testableAtEnd.length === 0 && nothingTestable !== true) {
    return 'testableAtEnd is empty: list what a person can try at the end, or say nothingTestable: true'
  }
  if (testableAtEnd.length > 0 && nothingTestable === true) {
    return 'nothingTestable: true contradicts a non-empty testableAtEnd'
  }
  if (!STATES.includes(state as SprintState)) {
    return `state must be one of ${STATES.join(', ')}`
  }
  if (!Array.isArray(tickets) || tickets.length === 0) {
    return 'tickets must be a non-empty array of { number, title, description, status }'
  }
  const numbers = new Set<number>()
  for (const ticket of tickets) {
    if (
      !isRecord(ticket) ||
      typeof ticket.number !== 'number' ||
      !Number.isInteger(ticket.number) ||
      ticket.number <= 0 ||
      !isText(ticket.title) ||
      !isText(ticket.description) ||
      !isText(ticket.status)
    ) {
      return 'every ticket needs a positive integer number and non-empty title, description and status'
    }
    if (statusOf(ticket.status as string, known) === undefined) {
      return `status of ticket #${ticket.number} must be one of: ${known.statuses.join(', ')}`
    }
    if (numbers.has(ticket.number)) {
      return `ticket #${ticket.number} appears twice in the sprint`
    }
    numbers.add(ticket.number)
  }

  return undefined
}

const keyOf = (root: string) => `project:${root}`

async function load($: EngineInterface): Promise<Project> {
  const stored = (await $.store.get(keyOf(await $.session.root()))) as Project | undefined

  return { sprints: Array.isArray(stored?.sprints) ? stored!.sprints : [] }
}

function change($: EngineInterface, edit: (project: Project) => Project): Promise<Project> {
  const run = queue.then(async () => {
    const key = keyOf(await $.session.root())
    const stored = (await $.store.get(key)) as Project | undefined
    const next = edit({ sprints: Array.isArray(stored?.sprints) ? stored!.sprints : [] })
    await $.store.set(key, next)
    $.ui.invalidate('ui.render')

    return next
  })
  queue = run.catch(() => undefined)

  return run
}

export const register: Register = on => {
  queue = Promise.resolve()
  vocabulary = undefined
  projectDirectory = undefined

  on('session.start', async ($, e, next) => {
    projectDirectory = e.cwd
    const known = await vocabularyOf($, e.cwd)
    await $.command.register({
      name: 'roadmap',
      description: 'Open the roadmap of sprints the agent planned',
    })
    await $.tool.register({
      name: 'plan_sprint',
      isDeferred: false,
      description:
        'Record or update, by name, one sprint of the roadmap. A lot is whatever the person asked you to take into account (a milestone, a list of ticket numbers, a column, something else): resolve it yourself and give its source. Give the sprint order, objective, what a person can really try at its end (testableAtEnd; if nothing, an empty list with nothingTestable: true), its state (planned, running, done) and its tickets with number, title, description and board status. The call is refused when a field is missing or malformed: read the reason and call again. The mod reads no ticket state, only the tracker\'s list of columns: it shows only what you record.',
      inputSchema: {
        type: 'object',
        properties: {
          name: { type: 'string', description: 'Unique name of the sprint; recording the same name replaces it' },
          order: { type: 'integer', description: 'Position in the roadmap, ascending' },
          source: {
            type: 'object',
            properties: {
              kind: { type: 'string', enum: KINDS },
              reference: { type: 'string', description: 'The milestone, ticket numbers, column or other reference' },
            },
            required: ['kind', 'reference'],
          },
          objective: { type: 'string' },
          testableAtEnd: {
            type: 'array',
            items: { type: 'string' },
            description: 'What a person can really try at the end of the sprint, not what is merely implemented',
          },
          nothingTestable: {
            type: 'boolean',
            description: 'true, with an empty testableAtEnd, when nothing can be tried at the end',
          },
          state: { type: 'string', enum: STATES },
          tickets: {
            type: 'array',
            items: {
              type: 'object',
              properties: {
                number: { type: 'integer' },
                title: { type: 'string' },
                description: { type: 'string' },
                status: { type: 'string', enum: known.statuses, description: 'Its column on the board, or Unknown' },
              },
              required: ['number', 'title', 'description', 'status'],
            },
          },
        },
        required: ['name', 'order', 'source', 'objective', 'testableAtEnd', 'state', 'tickets'],
      },
    })

    return next(e)
  })

  on('tool.call', { tool: PLAN_TOOL }, async ($, e) => {
    const input = e as unknown as Record<string, unknown>
    const known = await vocabularyOf($)
    const problem = problemWith(input, known)
    if (problem !== undefined) {
      return { deny: `scrumia-roadmap: ${problem}` }
    }
    const planned = input as unknown as Sprint
    const resolvedAt = await $.clock.now()
    const recordedIn = await $.session.id()
    let isReplaced = false
    let clash: string | undefined
    await change($, project => {
      clash = project.sprints.find(one => one.order === planned.order && one.name !== planned.name)?.name
      if (clash !== undefined) {
        return project
      }
      isReplaced = project.sprints.some(one => one.name === planned.name)
      const sprint: Sprint = {
        name: planned.name,
        order: planned.order,
        source: planned.source,
        objective: planned.objective,
        testableAtEnd: planned.testableAtEnd,
        nothingTestable: planned.nothingTestable === true,
        state: planned.state,
        tickets: planned.tickets.map(ticket => ({ ...ticket, status: statusOf(ticket.status, known)! })),
        resolvedAt,
        recordedIn,
      }

      return {
        sprints: isReplaced
          ? project.sprints.map(one => (one.name === planned.name ? sprint : one))
          : [...project.sprints, sprint],
      }
    })
    if (clash !== undefined) {
      return { deny: `scrumia-roadmap: order ${planned.order} is already taken by the sprint "${clash}"; the order is unique per project, choose another or record under that name` }
    }
    $.ui.toast(`Sprint ${planned.name} ${isReplaced ? 'updated' : 'recorded'}`)

    return {
      result: `Sprint "${planned.name}" ${isReplaced ? 'updated' : 'recorded'} at order ${planned.order} (${planned.tickets.length} tickets, ${planned.state}).`,
    }
  })

  on('command.run', { command: 'roadmap' }, async $ => {
    await $.ui.open({ id: PANE, title: 'Roadmap' })

    return { text: 'Roadmap pane opened.' }
  })

  on('ui.render', { component: 'Pane', requestId: PANE }, async ($, e) => {
    const { Box, Button, Markdown, Text } = $.ui.resolve(e)
    const known = await vocabularyOf($)
    const sessionId = await $.session.id()
    const everything = (await load($)).sprints.slice().sort(byOrder)
    const filter = view.filter
    const shown = everything.filter(one => filter === 'all' || stateOf(one) === filter)
    const show = () => $.ui.invalidate('ui.render')
    const filters: { value: Filter; label: string; count: number }[] = [
      { value: 'all', label: 'All', count: everything.length },
      ...STATES.map(state => ({
        value: state,
        label: state[0]!.toUpperCase() + state.slice(1),
        count: everything.filter(one => stateOf(one) === state).length,
      })),
    ]

    return (
      <Box flexDirection="column" gap={1}>
        <Box gap={2}>
          <Text bold>Roadmap</Text>
          {filters.map(one => (
            <Button
              key={`filter-${one.value}`}
              onPress={() => {
                view.filter = one.value
                show()
              }}
            >
              <Text bold={filter === one.value} inverse={filter === one.value} dimColor={filter !== one.value}>
                {' '}
                {one.label} {one.count}{' '}
              </Text>
            </Button>
          ))}
        </Box>
        {!known.isFromTracker && <Text dimColor>Default columns in use: {known.note ?? 'the tracker could not be read'}.</Text>}
        {shown.length === 0 && <Text dimColor>No sprint here. The agent records them with plan_sprint.</Text>}
        {shown.map(sprint => {
          const state = stateOf(sprint)
          const tickets = ticketsOf(sprint)
          const doneCount = tickets.filter(one => isTicketDone(one, known)).length
          const testable = Array.isArray(sprint.testableAtEnd) ? sprint.testableAtEnd : []
          const isStale = sprint.recordedIn !== sessionId
          const mismatch = mismatchOf(sprint, known)

          return (
            <Box
              key={`sprint-${sprint.name}`}
              flexDirection="column"
              gap={1}
              padding={1}
              borderStyle="round"
              borderColor={stateColor(state)}
            >
              <Box gap={2}>
                <Text color={stateColor(state)} bold>
                  {state === 'done' ? '✓ DONE' : state === 'running' ? '● RUNNING' : '○ PLANNED'}
                </Text>
                <Text bold>
                  {sprint.order}. {sprint.name}
                </Text>
                <Text dimColor>
                  {doneCount}/{tickets.length} done
                </Text>
                <Button key={`remove-${sprint.name}`} label="Remove" onPress={() => change($, project => ({
                  sprints: project.sprints.filter(one => one.name !== sprint.name),
                }))} />
              </Box>
              <Box gap={2}>
                <Text dimColor>
                  {sprint.source ? `${sprint.source.kind}: ${sprint.source.reference}` : 'source not recorded'}
                </Text>
                <Text dimColor>resolved {whenText(sprint.resolvedAt)}</Text>
                {isStale && <Text color="warning">possibly stale</Text>}
                {mismatch !== undefined && <Text color="warning">{mismatch}</Text>}
              </Box>
              <Box flexDirection="column">
                <Text color="subtle" bold>
                  OBJECTIVE
                </Text>
                <Markdown text={sprint.objective} />
              </Box>
              <Box flexDirection="column">
                <Text color="subtle" bold>
                  TESTABLE AT THE END
                </Text>
                {testable.length > 0 ? (
                  testable.map((item, index) => <Text key={`testable-${sprint.name}-${index}`}>- {item}</Text>)
                ) : (
                  <Text dimColor>{sprint.nothingTestable === true ? 'Nothing testable at the end of this sprint.' : 'Not recorded.'}</Text>
                )}
              </Box>
              <Box flexDirection="column" gap={1}>
                <Text color="subtle" bold>
                  TICKETS
                </Text>
                {tickets.map(ticket => (
                  <Box key={`ticket-${sprint.name}-${ticket.number}`} flexDirection="column">
                    <Box gap={2}>
                      <Text bold>#{ticket.number}</Text>
                      <Text>{ticket.title}</Text>
                      <Text color={statusColor(ticket, known)} bold>
                        {ticket.status}
                      </Text>
                    </Box>
                    <Markdown text={ticket.description} />
                  </Box>
                ))}
              </Box>
            </Box>
          )
        })}
      </Box>
    )
  })
}
