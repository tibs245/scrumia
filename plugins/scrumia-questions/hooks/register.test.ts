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

type World = Parameters<Parameters<typeof test>[1]>[1]

const prepare = (on: World) => {
  const reached = { texts: [] as string[] }
  mock.clock(on)
  mock.store(on)
  on('prompt.submit', ($, e) => {
    reached.texts.push(e.text)

    return { text: e.text }
  })

  return reached
}

describe('questions inbox', () => {
  test('parks a question and tells the model to carry on', async ($, on) => {
    prepare(on)
    const ran = await $.tool.call(ASK)
    expect(ran.deny).toBeUndefined()
    expect(ran.text ?? JSON.stringify(ran.result)).toContain('#1 parked')
  })

  test('numbers questions in order', async ($, on) => {
    prepare(on)
    await $.tool.call(ASK)
    const second = await $.tool.call(ASK)
    expect(second.text ?? JSON.stringify(second.result)).toContain('#2 parked')
  })

  test('a prompt passes untouched while nothing is answered', async ($, on) => {
    const reached = prepare(on)
    await $.tool.call(ASK)
    await $.prompt.submit({ text: 'hello' })
    expect(reached.texts).toEqual(['hello'])
  })

  for (const surface of ['terminal', 'desktop'] as const) {
    test(`a pick in the pane returns on the next prompt, once (${surface})`, async ($, on) => {
      const reached = prepare(on)
      await $.tool.call(ASK)
      const ui = await $.ui.mount({ plugin: 'scrumia-questions', surface, ...PANE })
      await ui.select({ key: 'pick1', value: '30 euros / 6' })
      await $.prompt.submit({ text: 'go on' })
      await $.prompt.submit({ text: 'and again' })
      expect(reached.texts[0]).toContain('Answer: 30 euros / 6')
      expect(reached.texts[0]).toContain('#1 (#3528)')
      expect(reached.texts[1]).toBe('and again')
      await ui.unmount()
    })
  }

  for (const surface of ['terminal', 'desktop'] as const) {
    test(`the filter keeps blocking questions apart (${surface})`, async ($, on) => {
      prepare(on)
      await $.tool.call(ASK)
      await $.tool.call({ ...ASK, isBlocking: false, question: 'Libell\u00e9 du bouton ?' })
      const ui = await $.ui.mount({ plugin: 'scrumia-questions', surface, ...PANE })
      expect(await ui.find({ key: 'q1' })).toBeDefined()
      expect(await ui.find({ key: 'q2' })).toBeDefined()
      await ui.press({ key: 'filter-blocking' })
      expect(await ui.find({ key: 'q1' })).toBeDefined()
      expect(await ui.find({ key: 'q2' })).toBeUndefined()
      await ui.press({ key: 'filter-non-blocking' })
      expect(await ui.find({ key: 'q1' })).toBeUndefined()
      expect(await ui.find({ key: 'q2' })).toBeDefined()
      await ui.unmount()
    })
  }
})
