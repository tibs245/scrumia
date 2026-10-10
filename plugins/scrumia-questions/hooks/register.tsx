import type { EngineInterface, Register } from 'claude-code'

type Answer = { text: string; isFree: boolean }

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

type Filter = 'all' | 'blocking' | 'non-blocking'

type AskInput = {
  context: string
  ticket?: string
  question: string
  impact: string
  isBlocking?: boolean
  options: string[]
  recommended?: string
}

const PANE = 'questions'
const QUESTIONS_KEY = 'questions'
const SELECTED_KEY = 'selected'
const FILTER_KEY = 'filter'
const ASK_TOOL = 'mcp__scrumia-questions__ask_later'

const isPending = (one: Question) => one.answer === undefined
const isUndelivered = (one: Question) => one.answer !== undefined && !one.isDelivered
const isBlockingQuestion = (one: Question) => one.isBlocking === true
const matchesFilter = (filter: Filter) => (one: Question) =>
  filter === 'all' || (filter === 'blocking') === isBlockingQuestion(one)
const blockingFirst = (first: Question, second: Question) =>
  Number(isBlockingQuestion(second)) - Number(isBlockingQuestion(first)) || first.id - second.id

async function load($: EngineInterface) {
  return ((await $.store.get(QUESTIONS_KEY)) ?? []) as Question[]
}

async function save($: EngineInterface, change: (list: Question[]) => Question[]) {
  const next = change(await load($))
  await $.store.set(QUESTIONS_KEY, next)
  $.ui.invalidate('ui.render')

  return next
}

function answer($: EngineInterface, id: number, given: Answer) {
  return save($, list => list.map(one => (one.id === id ? { ...one, answer: given } : one)))
}

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
        'Park a question for the person instead of blocking the session on it. Use it when a decision belongs to them but you can continue meanwhile. Give the context, the linked ticket, the impact of the choice, whether it blocks work that cannot proceed without the answer, 2-4 suggested answers and which one you recommend. Their answer comes back in a later prompt.',
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
    const input = e as unknown as AskInput
    const askedAt = await $.clock.now()
    const list = await save($, current => [
      ...current,
      {
        id: Math.max(0, ...current.map(one => one.id)) + 1,
        context: input.context,
        ticket: input.ticket,
        question: input.question,
        impact: input.impact,
        isBlocking: input.isBlocking === true,
        options: input.options,
        recommended: input.options.includes(input.recommended ?? '') ? input.recommended : undefined,
        askedAt,
        isDelivered: false,
      },
    ])
    $.ui.toast(`Question parked (${list.filter(isPending).length} pending)`)

    return {
      result: `Question #${list[list.length - 1]!.id} parked. Carry on without waiting; the answer arrives in a later prompt.`,
    }
  })

  on('prompt.submit', async ($, e, next) => {
    const ready = (await load($)).filter(isUndelivered)
    if (ready.length === 0) {
      return next(e)
    }
    const lines = ready.map(
      one => `- #${one.id}${one.ticket ? ` (${one.ticket})` : ''} ${one.question}\n  Answer: ${one.answer!.text}`,
    )
    await save($, list => list.map(one => (isUndelivered(one) ? { ...one, isDelivered: true } : one)))

    return next({ ...e, text: `${e.text}\n\n[Answers to the questions you parked]\n${lines.join('\n')}` })
  }).catch(($, e, next) => next(e))

  on('command.run', { command: 'questions' }, async $ => {
    await $.ui.open({ id: PANE, title: 'Questions' })

    return { text: 'Questions pane opened.' }
  })

  on('ui.render', { component: 'AbovePrompt' }, async ($, e, next) => {
    const pending = (await load($)).filter(isPending)
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
    const everything = (await load($)).filter(isPending)
    const filter = (((await $.store.get(FILTER_KEY)) as Filter | undefined) ?? 'all') as Filter
    const shown = everything.filter(matchesFilter(filter)).sort(blockingFirst)
    const picked = (await $.store.get(SELECTED_KEY)) as number | undefined
    const current = shown.find(one => one.id === picked) ?? shown[0]
    const blockingCount = everything.filter(isBlockingQuestion).length
    const choose = async (key: string, value: unknown) => {
      await $.store.set(key, value)
      $.ui.invalidate('ui.render')
    }
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
            <Button key={`filter-${one.value}`} onPress={() => choose(FILTER_KEY, one.value)}>
              <Text bold={filter === one.value} inverse={filter === one.value} dimColor={filter !== one.value}>
                {' '}
                {one.label} {one.count}{' '}
              </Text>
            </Button>
          ))}
        </Box>
        {current === undefined && <Text dimColor>No question here. Nothing waits on you.</Text>}
        {current !== undefined && (
          <Box flexDirection="column">
            {shown.map(one => (
              <Button key={`q${one.id}`} onPress={() => choose(SELECTED_KEY, one.id)}>
                <Text color={isBlockingQuestion(one) ? 'error' : 'suggestion'} bold>
                  {one.id === current.id ? '▶ ' : '  '}
                  {isBlockingQuestion(one) ? '● BLOCKING ' : '○ can wait '}
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
              options={current.options.map(option => ({
                value: option,
                label: option === current.recommended ? `★ ${option} (recommended)` : option,
              }))}
              value={current.recommended}
              onSelect={value => answer($, current.id, { text: value, isFree: false })}
            />
            <Input
              key={`free${current.id}`}
              label="Or your own answer"
              placeholder="free text, Enter to send"
              submitLabel="answer"
              onSubmit={text => (text.trim() === '' ? undefined : answer($, current.id, { text, isFree: true }))}
            />
          </Box>
        )}
      </Box>
    )
  })
}
