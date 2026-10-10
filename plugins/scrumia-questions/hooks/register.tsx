import type { EngineInterface, Register } from 'claude-code'

type Answer = { text: string; isFree: boolean }

type Question = {
  id: number
  context: string
  ticket?: string
  question: string
  impact: string
  options: string[]
  recommended?: string
  askedAt: number
  answer?: Answer
  isDelivered: boolean
}

type AskInput = {
  context: string
  ticket?: string
  question: string
  impact: string
  options: string[]
  recommended?: string
}

const PANE = 'questions'
const QUESTIONS_KEY = 'questions'
const SELECTED_KEY = 'selected'
const ASK_TOOL = 'mcp__scrumia-questions__ask_later'

const isPending = (one: Question) => one.answer === undefined
const isUndelivered = (one: Question) => one.answer !== undefined && !one.isDelivered

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
        'Park a question for the person instead of blocking the session on it. Use it when a decision belongs to them but you can continue meanwhile. Give the context, the linked ticket, the impact of the choice, 2-4 suggested answers and which one you recommend. Their answer comes back in a later prompt.',
      inputSchema: {
        type: 'object',
        properties: {
          context: { type: 'string', description: 'Situation the question arises from' },
          ticket: { type: 'string', description: 'Linked ticket, e.g. #3528' },
          question: { type: 'string' },
          impact: { type: 'string', description: 'What changes depending on the answer' },
          options: { type: 'array', items: { type: 'string' }, description: 'Suggested answers' },
          recommended: { type: 'string', description: 'The recommended option, copied from options' },
        },
        required: ['context', 'question', 'impact', 'options'],
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
    const pending = (await load($)).filter(isPending).length
    if (e.props.hasSurvey || pending === 0) {
      return next(e)
    }
    const { Box, Button, Text } = $.ui.resolve(e)

    return (
      <Box>
        <Text>
          {pending} question{pending > 1 ? 's' : ''} waiting{' '}
        </Text>
        <Button key="open" label="Open" onPress={() => $.ui.open({ id: PANE, title: 'Questions' })} />
      </Box>
    )
  })

  on('ui.render', { component: 'Pane', requestId: PANE }, async ($, e) => {
    const { Box, Button, Input, Select, Text } = $.ui.resolve(e)
    const pending = (await load($)).filter(isPending)
    const picked = (await $.store.get(SELECTED_KEY)) as number | undefined
    const current = pending.find(one => one.id === picked) ?? pending[0]

    if (current === undefined) {
      return <Text dimColor>No question waiting.</Text>
    }

    return (
      <Box flexDirection="column">
        <Box flexDirection="column">
          {pending.map(one => (
            <Button
              key={`q${one.id}`}
              onPress={async () => {
                await $.store.set(SELECTED_KEY, one.id)
                $.ui.invalidate('ui.render')
              }}
            >
              {one.id === current.id ? '> ' : '  '}#{one.id} {one.question.slice(0, 50)}
            </Button>
          ))}
        </Box>
        <Text bold>{current.question}</Text>
        {current.ticket && <Text dimColor>Ticket: {current.ticket}</Text>}
        <Text dimColor>Context</Text>
        <Text>{current.context}</Text>
        <Text dimColor>Impact</Text>
        <Text>{current.impact}</Text>
        <Select
          key={`pick${current.id}`}
          label="Answer"
          options={current.options.map(option => ({
            value: option,
            label: option === current.recommended ? `${option} (recommended)` : option,
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
    )
  })
}
