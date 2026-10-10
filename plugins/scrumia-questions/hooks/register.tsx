import type { EngineInterface, Register } from 'claude-code'

type Answer = { text: string; notes?: string; isOther: boolean }

type Draft = { choice?: string; notes?: string }

type Question = {
  id: number
  context: string
  ticket?: string
  question: string
  impact: string
  isBlocking?: boolean
  options: string[]
  recommended?: string
  askedAt: number
  answer?: Answer
  isDelivered: boolean
}

type Project = { nextId: number; questions: Question[]; drafts: Record<string, Draft> }

type Filter = 'all' | 'blocking' | 'non-blocking'

const PANE = 'questions'
const ASK_TOOL = 'mcp__scrumia-questions__ask_later'
const OTHER = 'Other'
const MAX_OPTIONS = 6
const KEEP_DELIVERED_MS = 30 * 24 * 60 * 60 * 1000

let queue: Promise<unknown> = Promise.resolve()
const view: { filter: Filter; selectedId?: number } = { filter: 'all' }

const isPending = (one: Question) => one.answer === undefined
const isUndelivered = (one: Question) => one.answer !== undefined && !one.isDelivered
const isBlockingQuestion = (one: Question) => one.isBlocking === true
const matchesFilter = (filter: Filter) => (one: Question) =>
  filter === 'all' || (filter === 'blocking') === isBlockingQuestion(one)
const blockingFirst = (first: Question, second: Question) =>
  Number(isBlockingQuestion(second)) - Number(isBlockingQuestion(first)) || first.id - second.id

const isText = (value: unknown): value is string => typeof value === 'string' && value.trim() !== ''

function problemWith(input: Record<string, unknown>): string | undefined {
  const { context, ticket, question, impact, isBlocking, options, recommended } = input
  if (!isText(context) || !isText(question) || !isText(impact)) {
    return 'context, question and impact must be non-empty text'
  }
  if (ticket !== undefined && typeof ticket !== 'string') {
    return 'ticket must be text'
  }
  if (typeof isBlocking !== 'boolean') {
    return 'isBlocking must be true or false'
  }
  if (!Array.isArray(options) || options.length === 0 || options.length > MAX_OPTIONS || !options.every(isText)) {
    return `options must be 1 to ${MAX_OPTIONS} non-empty texts`
  }
  if (recommended !== undefined && !options.includes(recommended)) {
    return 'recommended must be copied from options'
  }

  return undefined
}

const readyAnswer = (one: Question, draft: Draft | undefined): Answer | undefined => {
  const choice = draft?.choice ?? one.recommended
  const notes = draft?.notes?.trim() ?? ''
  if (choice === undefined || (choice === OTHER && notes === '')) {
    return undefined
  }

  return { text: choice, notes: notes === '' ? undefined : notes, isOther: choice === OTHER }
}

const missing = (one: Question, draft: Draft | undefined) =>
  (draft?.choice ?? one.recommended) === undefined ? 'pick one' : 'needs a note'

const emptyProject = (): Project => ({ nextId: 1, questions: [], drafts: {} })

const keyOf = (root: string) => `project:${root}`

async function load($: EngineInterface): Promise<Project> {
  const stored = (await $.store.get(keyOf(await $.session.root()))) as Project | undefined

  return stored ?? emptyProject()
}

function change($: EngineInterface, edit: (project: Project) => Project, isRedrawn = true): Promise<Project> {
  const run = queue.then(async () => {
    const key = keyOf(await $.session.root())
    const next = edit(((await $.store.get(key)) as Project | undefined) ?? emptyProject())
    await $.store.set(key, next)
    if (isRedrawn) {
      $.ui.invalidate('ui.render')
    }

    return next
  })
  queue = run.catch(() => undefined)

  return run
}

function amend($: EngineInterface, id: number, draft: Partial<Draft>, isRedrawn: boolean) {
  return change(
    $,
    project => ({ ...project, drafts: { ...project.drafts, [id]: { ...project.drafts[id], ...draft } } }),
    isRedrawn,
  )
}

function sendAll($: EngineInterface, filter: Filter) {
  return change($, project => {
    const answers = new Map<number, Answer>()
    for (const one of project.questions.filter(isPending).filter(matchesFilter(filter))) {
      const given = readyAnswer(one, project.drafts[one.id])
      if (given !== undefined) {
        answers.set(one.id, given)
      }
    }
    const drafts = { ...project.drafts }
    for (const id of answers.keys()) {
      delete drafts[id]
    }

    return {
      ...project,
      drafts,
      questions: project.questions.map(one => (answers.has(one.id) ? { ...one, answer: answers.get(one.id) } : one)),
    }
  })
}

function remove($: EngineInterface, id: number) {
  return change($, project => {
    const drafts = { ...project.drafts }
    delete drafts[id]

    return { ...project, drafts, questions: project.questions.filter(one => one.id !== id) }
  })
}

const deliveryNote = (ready: Question[]) =>
  [
    '[scrumia-questions] The person answered questions you parked. The question texts are yours; the answers and notes are theirs.',
    ...ready.map(
      one =>
        `- #${one.id}${one.ticket ? ` (${one.ticket})` : ''} ${one.question}\n  Answer: ${one.answer!.text}${one.answer!.notes ? `\n  Additional notes: ${one.answer!.notes}` : ''}`,
    ),
  ].join('\n')

export const register: Register = on => {
  on('session.start', async ($, e, next) => {
    await $.command.register({
      name: 'questions',
      description: 'Open the inbox of questions parked by the model',
    })
    await $.tool.register({
      name: 'ask_later',
      isDeferred: false,
      description:
        'Park a question for the person instead of blocking the session on it. Use it when a decision belongs to them. Give the context, the linked ticket, the impact of the choice, whether it blocks work that cannot proceed without the answer, 1-6 suggested answers and which one you recommend (copied from the options). Their answer comes back in a later prompt. The call is refused when a field is missing or malformed: read the reason and call again.',
      inputSchema: {
        type: 'object',
        properties: {
          context: { type: 'string', description: 'Situation the question arises from' },
          ticket: { type: 'string', description: 'Linked ticket, e.g. #3528' },
          question: { type: 'string' },
          impact: { type: 'string', description: 'What changes depending on the answer' },
          isBlocking: {
            type: 'boolean',
            description: 'true when part of the work cannot proceed without the answer, false when it can wait',
          },
          options: { type: 'array', items: { type: 'string' }, description: 'Suggested answers' },
          recommended: { type: 'string', description: 'The recommended option, copied from options' },
        },
        required: ['context', 'question', 'impact', 'isBlocking', 'options'],
      },
    })

    return next(e)
  })

  on('tool.call', { tool: ASK_TOOL }, async ($, e) => {
    const input = e as unknown as Record<string, unknown>
    const problem = problemWith(input)
    if (problem !== undefined) {
      return { deny: `scrumia-questions: ${problem}` }
    }
    const asked = input as unknown as Omit<Question, 'id' | 'askedAt' | 'isDelivered'>
    const askedAt = await $.clock.now()
    const project = await change($, current => ({
      ...current,
      nextId: current.nextId + 1,
      questions: [
        ...current.questions,
        {
          id: current.nextId,
          context: asked.context,
          ticket: asked.ticket,
          question: asked.question,
          impact: asked.impact,
          isBlocking: asked.isBlocking,
          options: asked.options,
          recommended: asked.recommended,
          askedAt,
          isDelivered: false,
        },
      ],
    }))
    const id = project.nextId - 1
    $.ui.toast(`Question parked (${project.questions.filter(isPending).length} pending)`)

    return {
      result: asked.isBlocking
        ? `Question #${id} parked and it blocks. Do not go ahead on the part that depends on it; carry on with what does not. The answer arrives in a later prompt.`
        : `Question #${id} parked. Carry on without waiting; the answer arrives in a later prompt.`,
    }
  })

  on('prompt.submit', async ($, e, next) => {
    const ready = (await load($)).questions.filter(isUndelivered)
    if (ready.length === 0) {
      return next(e)
    }
    const ran = await next({ ...e, context: [...(e.context ?? []), deliveryNote(ready)] })
    if (ran.drop === undefined) {
      const ids = new Set(ready.map(one => one.id))
      const now = await $.clock.now()
      await change($, project => ({
        ...project,
        questions: project.questions
          .map(one => (ids.has(one.id) ? { ...one, isDelivered: true } : one))
          .filter(one => !(one.isDelivered && now - one.askedAt > KEEP_DELIVERED_MS)),
      }))
    }

    return ran
  })

  on('command.run', { command: 'questions' }, async $ => {
    await $.ui.open({ id: PANE, title: 'Questions' })

    return { text: 'Questions pane opened.' }
  })

  on('ui.render', { component: 'AbovePrompt' }, async ($, e, next) => {
    const pending = (await load($)).questions.filter(isPending)
    if (e.props.hasSurvey || pending.length === 0) {
      return next(e)
    }
    const blocking = pending.filter(isBlockingQuestion).length
    const { Box, Button, Text } = $.ui.resolve(e)

    return (
      <Box gap={1}>
        <Text bold>
          {pending.length} question{pending.length > 1 ? 's' : ''} waiting
        </Text>
        {blocking > 0 && (
          <Text color="error" bold>
            {blocking} blocking
          </Text>
        )}
        <Button key="open" label="Open" onPress={() => $.ui.open({ id: PANE, title: 'Questions' })} />
      </Box>
    )
  })

  on('ui.render', { component: 'Pane', requestId: PANE }, async ($, e) => {
    const { Box, Button, Input, Markdown, Select, Text } = $.ui.resolve(e)
    const project = await load($)
    const everything = project.questions.filter(isPending)
    const filter = view.filter
    const shown = everything.filter(matchesFilter(filter)).sort(blockingFirst)
    const current = shown.find(one => one.id === view.selectedId) ?? shown[0]
    const blockingCount = everything.filter(isBlockingQuestion).length
    const draftOf = (one: Question) => project.drafts[one.id]
    const draft = current === undefined ? undefined : draftOf(current)
    const readyCount = shown.filter(one => readyAnswer(one, draftOf(one)) !== undefined).length
    const show = () => $.ui.invalidate('ui.render')
    const filters: { value: Filter; label: string; count: number }[] = [
      { value: 'all', label: 'All', count: everything.length },
      { value: 'blocking', label: 'Blocking', count: blockingCount },
      { value: 'non-blocking', label: 'Non-blocking', count: everything.length - blockingCount },
    ]

    return (
      <Box flexDirection="column" gap={1}>
        <Box gap={2}>
          <Text bold>Questions</Text>
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
        {current !== undefined && (
          <Box gap={2}>
            <Button key="send-all" onPress={() => sendAll($, filter)}>
              <Text bold inverse={readyCount > 0} dimColor={readyCount === 0}>
                {' '}
                Send {readyCount} answer{readyCount === 1 ? '' : 's'}{' '}
              </Text>
            </Button>
            <Text dimColor>
              {shown.length - readyCount > 0 ? `${shown.length - readyCount} not ready` : 'all ready'}
            </Text>
          </Box>
        )}
        {current === undefined && <Text dimColor>No question here. Nothing waits on you.</Text>}
        {current !== undefined && (
          <Box flexDirection="column">
            {shown.map(one => (
              <Button
                key={`q${one.id}`}
                onPress={() => {
                  view.selectedId = one.id
                  show()
                }}
              >
                <Text color={isBlockingQuestion(one) ? 'error' : 'suggestion'} bold>
                  {one.id === current.id ? '▶ ' : '  '}
                  {isBlockingQuestion(one) ? '● BLOCKING ' : '○ can wait '}
                </Text>
                <Text color={readyAnswer(one, draftOf(one)) ? 'success' : 'warning'}>
                  {readyAnswer(one, draftOf(one)) ? '✓ ready ' : `… ${missing(one, draftOf(one))} `}
                </Text>
                <Text bold={one.id === current.id}>
                  #{one.id} {one.ticket ? `${one.ticket} · ` : ''}
                  {one.question.slice(0, 60)}
                </Text>
              </Button>
            ))}
          </Box>
        )}
        {current !== undefined && (
          <Box
            flexDirection="column"
            gap={1}
            padding={1}
            borderStyle="round"
            borderColor={isBlockingQuestion(current) ? 'error' : 'suggestion'}
          >
            <Box gap={2}>
              <Text color={isBlockingQuestion(current) ? 'error' : 'suggestion'} bold>
                {isBlockingQuestion(current) ? '● BLOCKING' : '○ CAN WAIT'}
              </Text>
              {current.ticket && <Text dimColor>{current.ticket}</Text>}
              <Text dimColor>#{current.id}</Text>
              <Button key="remove" label="Remove" onPress={() => remove($, current.id)} />
            </Box>
            <Text bold>{current.question}</Text>
            <Box flexDirection="column">
              <Text color="subtle" bold>
                CONTEXT
              </Text>
              <Markdown text={current.context} />
            </Box>
            <Box flexDirection="column">
              <Text color="subtle" bold>
                IMPACT
              </Text>
              <Markdown text={current.impact} />
            </Box>
            <Select
              key={`pick${current.id}`}
              label="Answer"
              options={[
                ...current.options.map(option => ({
                  value: option,
                  label: option === current.recommended ? `★ ${option} (recommended)` : option,
                })),
                { value: OTHER, label: OTHER },
              ]}
              value={draft?.choice ?? current.recommended}
              onSelect={value => amend($, current.id, { choice: value }, true)}
            />
            <Input
              key={`notes${current.id}`}
              label="Additional notes"
              placeholder={
                (draft?.choice ?? current.recommended) === OTHER
                  ? 'required with Other: say what you decide'
                  : 'always sent with your answer (optional)'
              }
              value={draft?.notes}
              submitLabel="keep notes"
              onInput={text => amend($, current.id, { notes: text }, false)}
              onSubmit={text => amend($, current.id, { notes: text }, true)}
            />
          </Box>
        )}
      </Box>
    )
  })
}
