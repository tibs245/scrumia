import { describe, expect, mock, test } from 'claude-code/testing'

const ASK = {
  tool: 'mcp__scrumia-questions__ask_later',
  context: 'Refining #3528',
  ticket: '#3528',
  question: 'Quota par abonné ?',
  impact: 'Fixe le prix du lot',
  isBlocking: true,
  options: ['20 euros / 4', '30 euros / 6'],
  recommended: '20 euros / 4',
}
const PANE = { component: 'Pane', props: {}, requestId: 'questions' } as const
const BAND = { component: 'AbovePrompt', props: { hasSurvey: false } } as const

type World = Parameters<Parameters<typeof test>[1]>[1]

type Options = { entries?: Record<string, unknown> }

const prepare = (on: World, options: Options = {}) => {
  const seen = { root: '/project-a', refuseNext: false, texts: [] as string[], contexts: [] as (readonly string[])[] }
  mock.clock(on)
  mock.store(on, options.entries)
  on('session.root', () => ({ value: seen.root }))
  on('prompt.submit', ($, e) => {
    seen.texts.push(e.text)
    seen.contexts.push(e.context ?? [])
    if (seen.refuseNext) {
      seen.refuseNext = false

      return { drop: 'refused below' }
    }

    return { text: e.text, context: e.context }
  })

  return seen
}

const said = (ran: { text?: string; result?: unknown; deny?: string }) =>
  ran.deny ?? ran.text ?? JSON.stringify(ran.result)

describe('questions inbox', () => {
  test('parks a question and numbers them in order', async ($, on) => {
    prepare(on)
    expect(said(await $.tool.call(ASK))).toContain('#1 parked')
    expect(said(await $.tool.call(ASK))).toContain('#2 parked')
  })

  test('a blocking question says not to go ahead, a non-blocking one says to carry on', async ($, on) => {
    prepare(on)
    expect(said(await $.tool.call(ASK))).toContain('Do not go ahead')
    expect(said(await $.tool.call({ ...ASK, isBlocking: false }))).toContain('Carry on')
  })

  test('three parallel calls keep three questions', async ($, on) => {
    prepare(on)
    const ran = await Promise.all([$.tool.call(ASK), $.tool.call(ASK), $.tool.call(ASK)])
    expect(ran.map(said).join(' ')).toMatch(/#1 .*#2 .*#3/)
    const ui = await $.ui.mount({ plugin: 'scrumia-questions', surface: 'terminal', ...PANE })
    for (const key of ['q1', 'q2', 'q3']) {
      expect(await ui.find({ key })).toBeDefined()
    }
    await ui.unmount()
  })

  describe('a malformed call is refused with its reason', () => {
    const bad: [string, Record<string, unknown>, string][] = [
      ['no options', { ...ASK, options: undefined }, 'options'],
      ['empty options', { ...ASK, options: [] }, 'options'],
      ['a question that is not text', { ...ASK, question: 42 }, 'non-empty text'],
      ['no isBlocking', { ...ASK, isBlocking: undefined }, 'isBlocking'],
      ['a recommendation outside the options', { ...ASK, recommended: 'autre' }, 'recommended'],
    ]
    for (const [name, input, reason] of bad) {
      test(name, async ($, on) => {
        prepare(on)
        const ran = await $.tool.call(input as typeof ASK)
        expect(ran.deny).toContain(reason)
        const ui = await $.ui.mount({ plugin: 'scrumia-questions', surface: 'terminal', ...PANE })
        expect(await ui.find({ key: 'q1' })).toBeUndefined()
        await ui.unmount()
      })
    }
  })

  test('a prompt passes untouched while nothing is answered', async ($, on) => {
    const seen = prepare(on)
    await $.tool.call(ASK)
    await $.prompt.submit({ text: 'hello' })
    expect(seen.contexts[0]).toEqual([])
  })

  for (const surface of ['terminal', 'desktop'] as const) {
    test(`an answer with its notes reaches the model by the context, once (${surface})`, async ($, on) => {
      const seen = prepare(on)
      await $.tool.call(ASK)
      const ui = await $.ui.mount({ plugin: 'scrumia-questions', surface, ...PANE })
      await ui.select({ key: 'pick1', value: '30 euros / 6' })
      await ui.input({ key: 'notes1', text: 'surtout pas plus de 6', kind: 'change' })
      await ui.press({ key: 'send-all' })
      await $.prompt.submit({ text: 'go on' })
      await $.prompt.submit({ text: 'and again' })
      expect(seen.texts[0]).toBe('go on')
      expect(seen.contexts[0]!.join('\n')).toContain('Answer: 30 euros / 6')
      expect(seen.contexts[0]!.join('\n')).toContain('Additional notes: surtout pas plus de 6')
      expect(seen.contexts[0]!.join('\n')).toContain('#1 (#3528)')
      expect(seen.contexts[1]).toEqual([])
      await ui.unmount()
    })

    test(`Other needs a note, and the note travels with it (${surface})`, async ($, on) => {
      const seen = prepare(on)
      await $.tool.call(ASK)
      const ui = await $.ui.mount({ plugin: 'scrumia-questions', surface, ...PANE })
      await ui.select({ key: 'pick1', value: 'Other' })
      await ui.press({ key: 'send-all' })
      await $.prompt.submit({ text: 'first' })
      expect(seen.contexts[0]).toEqual([])
      await ui.input({ key: 'notes1', text: 'on verra' })
      await ui.press({ key: 'send-all' })
      await $.prompt.submit({ text: 'second' })
      expect(seen.contexts[1]!.join('\n')).toContain('Answer: Other')
      expect(seen.contexts[1]!.join('\n')).toContain('Additional notes: on verra')
      await ui.unmount()
    })

    test(`the recommended answer is sent as is when nothing else is touched (${surface})`, async ($, on) => {
      const seen = prepare(on)
      await $.tool.call(ASK)
      const ui = await $.ui.mount({ plugin: 'scrumia-questions', surface, ...PANE })
      await ui.press({ key: 'send-all' })
      await $.prompt.submit({ text: 'go' })
      expect(seen.contexts[0]!.join('\n')).toContain('Answer: 20 euros / 4')
      expect(seen.contexts[0]!.join('\n')).not.toContain('Additional notes')
      await ui.unmount()
    })

    test(`the filter keeps blocking questions apart (${surface})`, async ($, on) => {
      prepare(on)
      await $.tool.call(ASK)
      await $.tool.call({ ...ASK, isBlocking: false, question: 'Libellé du bouton ?' })
      const ui = await $.ui.mount({ plugin: 'scrumia-questions', surface, ...PANE })
      await ui.press({ key: 'filter-blocking' })
      expect(await ui.find({ key: 'q1' })).toBeDefined()
      expect(await ui.find({ key: 'q2' })).toBeUndefined()
      await ui.press({ key: 'filter-non-blocking' })
      expect(await ui.find({ key: 'q1' })).toBeUndefined()
      expect(await ui.find({ key: 'q2' })).toBeDefined()
      await ui.press({ key: 'filter-all' })
      await ui.unmount()
    })

    test(`one button sends every ready answer and leaves the others (${surface})`, async ($, on) => {
      const seen = prepare(on)
      await $.tool.call(ASK)
      await $.tool.call({ ...ASK, question: 'Sans recommandation ?', recommended: undefined })
      const ui = await $.ui.mount({ plugin: 'scrumia-questions', surface, ...PANE })
      await ui.press({ key: 'send-all' })
      await $.prompt.submit({ text: 'go' })
      expect(seen.contexts[0]!.join('\n')).toContain('#1')
      expect(seen.contexts[0]!.join('\n')).not.toContain('#2')
      expect(await ui.find({ key: 'q1' })).toBeUndefined()
      expect(await ui.find({ key: 'q2' })).toBeDefined()
      await ui.unmount()
    })

    test(`Remove takes a question out (${surface})`, async ($, on) => {
      prepare(on)
      await $.tool.call(ASK)
      const ui = await $.ui.mount({ plugin: 'scrumia-questions', surface, ...PANE })
      await ui.press({ key: 'remove' })
      expect(await ui.find({ key: 'q1' })).toBeUndefined()
      expect(said(await $.tool.call(ASK))).toContain('#2 parked')
      await ui.unmount()
    })
  }

  test('a prompt refused further down does not consume the answers', async ($, on) => {
    const seen = prepare(on)
    await $.tool.call(ASK)
    const ui = await $.ui.mount({ plugin: 'scrumia-questions', surface: 'terminal', ...PANE })
    await ui.press({ key: 'send-all' })
    seen.refuseNext = true
    await $.prompt.submit({ text: 'refused' })
    await $.prompt.submit({ text: 'accepted' })
    expect(seen.contexts[0]!.join('\n')).toContain('Answer: 20 euros / 4')
    expect(seen.contexts[1]!.join('\n')).toContain('Answer: 20 euros / 4')
    await $.prompt.submit({ text: 'again' })
    expect(seen.contexts[2]).toEqual([])
    await ui.unmount()
  })

  test('questions belong to the project they were asked in', async ($, on) => {
    const seen = prepare(on)
    await $.tool.call(ASK)
    const ui = await $.ui.mount({ plugin: 'scrumia-questions', surface: 'terminal', ...PANE })
    await ui.press({ key: 'send-all' })
    seen.root = '/project-b'
    await $.prompt.submit({ text: 'elsewhere' })
    expect(seen.contexts[0]).toEqual([])
    expect(said(await $.tool.call(ASK))).toContain('#1 parked')
    seen.root = '/project-a'
    await $.prompt.submit({ text: 'back' })
    expect(seen.contexts[1]!.join('\n')).toContain('#1 (#3528)')
    await ui.unmount()
  })

  test('a question stored without isBlocking still draws, as one that can wait', async ($, on) => {
    prepare(on, {
      entries: {
        'project:/project-a': {
          nextId: 2,
          drafts: {},
          questions: [
            {
              id: 1,
              context: 'old',
              question: 'Ancienne question ?',
              impact: 'none',
              options: ['a'],
              askedAt: 0,
              isDelivered: false,
            },
          ],
        },
      },
    })
    const ui = await $.ui.mount({ plugin: 'scrumia-questions', surface: 'terminal', ...PANE })
    expect(await ui.find({ key: 'q1' })).toBeDefined()
    await ui.press({ key: 'filter-blocking' })
    expect(await ui.find({ key: 'q1' })).toBeUndefined()
    await ui.unmount()
  })

  test('the band offers to open the inbox when a question waits', async ($, on) => {
    prepare(on)
    await $.tool.call(ASK)
    const ui = await $.ui.mount({ plugin: 'scrumia-questions', surface: 'terminal', ...BAND })
    expect(await ui.find({ key: 'open' })).toBeDefined()
    expect(await ui.find({ type: 'Text', text: /1 blocking/ })).toBeDefined()
    await ui.unmount()
  })
})
