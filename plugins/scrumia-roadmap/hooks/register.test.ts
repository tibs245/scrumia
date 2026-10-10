import { describe, expect, mock, test } from 'claude-code/testing'

const PLAN = {
  tool: 'mcp__scrumia-roadmap__plan_sprint',
  name: 'Sprint 1',
  order: 1,
  source: { kind: 'milestone', reference: 'Session mods' },
  objective: 'Ship the first two mods',
  testableAtEnd: ['Park a question and answer it'],
  state: 'planned',
  tickets: [
    { number: 483, title: 'Questions inbox', description: 'The **inbox** mod', status: 'Done' },
    { number: 484, title: 'Issues view', description: 'The issues mod', status: 'In progress' },
  ],
}
const PANE = { component: 'Pane', props: {}, requestId: 'roadmap' } as const

type World = Parameters<Parameters<typeof test>[1]>[1]

type Options = { entries?: Record<string, unknown> }

const prepare = (on: World, options: Options = {}) => {
  const seen = { root: '/project-a' }
  const clock = mock.clock(on)
  mock.store(on, options.entries)
  on('session.root', () => ({ value: seen.root }))

  return Object.assign(seen, { clock })
}

const said = (ran: { text?: string; result?: unknown; deny?: string }) =>
  ran.deny ?? ran.text ?? JSON.stringify(ran.result)

const plan = (changes: Record<string, unknown>) => ({ ...PLAN, ...changes }) as typeof PLAN

describe('roadmap', () => {
  test('records a sprint, then updates it in place by name', async ($, on) => {
    prepare(on)
    expect(said(await $.tool.call(PLAN))).toContain('recorded')
    expect(said(await $.tool.call(plan({ objective: 'Changed objective', state: 'running' })))).toContain('updated')
    await $.tool.call(plan({ name: 'Sprint 2', order: 2, objective: 'Another objective' }))
    const ui = await $.ui.mount({ plugin: 'scrumia-roadmap', surface: 'terminal', ...PANE })
    expect(await ui.find({ type: 'Markdown', text: /Changed objective/ })).toBeDefined()
    expect(await ui.find({ type: 'Markdown', text: /Ship the first two mods/ })).toBeUndefined()
    expect(await ui.find({ key: 'sprint-Sprint 1' })).toBeDefined()
    expect(await ui.find({ key: 'sprint-Sprint 2' })).toBeDefined()
    await ui.unmount()
  })

  describe('a malformed call is refused with its reason and stores nothing', () => {
    const bad: [string, Record<string, unknown>, string][] = [
      ['no name', { name: undefined }, 'name'],
      ['an order that is not an integer', { order: 1.5 }, 'order'],
      ['an unknown source kind', { source: { kind: 'wish', reference: 'x' } }, 'source'],
      ['an empty source reference', { source: { kind: 'column', reference: ' ' } }, 'source'],
      ['an empty objective', { objective: '' }, 'objective'],
      ['no testable list', { testableAtEnd: undefined }, 'testableAtEnd'],
      ['an empty testable list without nothingTestable', { testableAtEnd: [] }, 'nothingTestable'],
      ['nothingTestable with a testable list', { nothingTestable: true }, 'contradicts'],
      ['an unknown state', { state: 'cancelled' }, 'state'],
      ['no tickets', { tickets: [] }, 'tickets'],
      ['a ticket without description', { tickets: [{ number: 1, title: 't', description: '', status: 'Done' }] }, 'ticket'],
      [
        'a ticket number twice',
        {
          tickets: [
            { number: 1, title: 'a', description: 'a', status: 'Done' },
            { number: 1, title: 'b', description: 'b', status: 'Done' },
          ],
        },
        'twice',
      ],
    ]
    for (const [name, changes, reason] of bad) {
      test(name, async ($, on) => {
        prepare(on)
        const ran = await $.tool.call(plan(changes))
        expect(ran.deny).toContain(reason)
        const ui = await $.ui.mount({ plugin: 'scrumia-roadmap', surface: 'terminal', ...PANE })
        expect(await ui.find({ key: 'sprint-Sprint 1' })).toBeUndefined()
        await ui.unmount()
      })
    }
  })

  test('a sprint with nothing testable says so in words', async ($, on) => {
    prepare(on)
    expect(said(await $.tool.call(plan({ testableAtEnd: [], nothingTestable: true })))).toContain('recorded')
    const ui = await $.ui.mount({ plugin: 'scrumia-roadmap', surface: 'terminal', ...PANE })
    expect(await ui.find({ type: 'Text', text: /Nothing testable/ })).toBeDefined()
    await ui.unmount()
  })

  test('three parallel calls keep three sprints', async ($, on) => {
    prepare(on)
    await Promise.all([
      $.tool.call(plan({ name: 'A', order: 1 })),
      $.tool.call(plan({ name: 'B', order: 2 })),
      $.tool.call(plan({ name: 'C', order: 3 })),
    ])
    const ui = await $.ui.mount({ plugin: 'scrumia-roadmap', surface: 'terminal', ...PANE })
    for (const name of ['A', 'B', 'C']) {
      expect(await ui.find({ key: `sprint-${name}` })).toBeDefined()
    }
    await ui.unmount()
  })

  test('the sprints are drawn in their order, not in the order they were recorded', async ($, on) => {
    prepare(on)
    await $.tool.call(plan({ name: 'Zeta', order: 2 }))
    await $.tool.call(plan({ name: 'Alpha', order: 1 }))
    const ui = await $.ui.mount({ plugin: 'scrumia-roadmap', surface: 'terminal', ...PANE })
    const titles = (await ui.findAll({ type: 'Text', text: /^\d\. / })).map(one => one.text)
    expect(titles).toEqual(['1. Alpha', '2. Zeta'])
    await ui.unmount()
  })

  test('the stamp is the clock at recording', async ($, on) => {
    const seen = prepare(on)
    await seen.clock.advance(1000)
    await $.tool.call(PLAN)
    const ui = await $.ui.mount({ plugin: 'scrumia-roadmap', surface: 'terminal', ...PANE })
    expect(await ui.find({ type: 'Text', text: /resolved 1970-01-01 00:00 UTC/ })).toBeDefined()
    await ui.unmount()
  })

  test('a sprint stored by an earlier session is marked possibly stale, one recorded now is not', async ($, on) => {
    prepare(on, {
      entries: {
        'project:/project-a': {
          sprints: [{ ...PLAN, name: 'Old sprint', order: 5, resolvedAt: 0 }],
        },
      },
    })
    await $.tool.call(plan({ name: 'Fresh sprint', order: 6 }))
    const ui = await $.ui.mount({ plugin: 'scrumia-roadmap', surface: 'terminal', ...PANE })
    expect(await ui.find({ key: 'sprint-Old sprint' })).toBeDefined()
    expect(await ui.find({ type: 'Text', text: 'possibly stale' })).toBeDefined()
    await $.tool.call(plan({ name: 'Old sprint', order: 5 }))
    expect(await ui.find({ type: 'Text', text: 'possibly stale' })).toBeUndefined()
    await ui.unmount()
  })

  test('two project roots do not see each other', async ($, on) => {
    const seen = prepare(on)
    await $.tool.call(plan({ name: 'Only in A' }))
    seen.root = '/project-b'
    await $.tool.call(plan({ name: 'Only in B' }))
    const ui = await $.ui.mount({ plugin: 'scrumia-roadmap', surface: 'terminal', ...PANE })
    expect(await ui.find({ key: 'sprint-Only in B' })).toBeDefined()
    expect(await ui.find({ key: 'sprint-Only in A' })).toBeUndefined()
    await ui.unmount()
  })

  test('a sprint stored in an older shape still draws', async ($, on) => {
    prepare(on, {
      entries: { 'project:/project-a': { sprints: [{ name: 'Ancient', order: 1, objective: 'Old objective' }] } },
    })
    const ui = await $.ui.mount({ plugin: 'scrumia-roadmap', surface: 'terminal', ...PANE })
    expect(await ui.find({ key: 'sprint-Ancient' })).toBeDefined()
    expect(await ui.find({ type: 'Text', text: /source not recorded/ })).toBeDefined()
    expect(await ui.find({ type: 'Text', text: /Not recorded/ })).toBeDefined()
    await ui.unmount()
  })

  for (const surface of ['terminal', 'desktop'] as const) {
    test(`the pane draws sprints as cards with tickets and progress (${surface})`, async ($, on) => {
      prepare(on)
      await $.tool.call(plan({ name: 'Second', order: 2 }))
      await $.tool.call(plan({ name: 'First', order: 1 }))
      const ui = await $.ui.mount({ plugin: 'scrumia-roadmap', surface, ...PANE })
      const first = await ui.find({ key: 'sprint-First' })
      const second = await ui.find({ key: 'sprint-Second' })
      expect(first).toBeDefined()
      expect(second).toBeDefined()
      expect(await ui.find({ type: 'Text', text: /1\/2 done/ })).toBeDefined()
      expect(await ui.find({ type: 'Text', text: /Park a question and answer it/ })).toBeDefined()
      expect(await ui.find({ key: 'ticket-First-483' })).toBeDefined()
      expect(await ui.find({ type: 'Markdown', text: /The \*\*inbox\*\* mod/ })).toBeDefined()
      expect(await ui.find({ type: 'Text', text: /milestone: Session mods/ })).toBeDefined()
      await ui.unmount()
    })

    test(`the state filter narrows the view (${surface})`, async ($, on) => {
      prepare(on)
      await $.tool.call(plan({ name: 'P', order: 1 }))
      await $.tool.call(plan({ name: 'R', order: 2, state: 'running' }))
      const ui = await $.ui.mount({ plugin: 'scrumia-roadmap', surface, ...PANE })
      await ui.press({ key: 'filter-running' })
      expect(await ui.find({ key: 'sprint-R' })).toBeDefined()
      expect(await ui.find({ key: 'sprint-P' })).toBeUndefined()
      await ui.press({ key: 'filter-planned' })
      expect(await ui.find({ key: 'sprint-P' })).toBeDefined()
      expect(await ui.find({ key: 'sprint-R' })).toBeUndefined()
      await ui.press({ key: 'filter-all' })
      expect(await ui.find({ key: 'sprint-R' })).toBeDefined()
      await ui.unmount()
    })

    test(`Remove takes a sprint out (${surface})`, async ($, on) => {
      prepare(on)
      await $.tool.call(PLAN)
      const ui = await $.ui.mount({ plugin: 'scrumia-roadmap', surface, ...PANE })
      await ui.press({ key: 'remove-Sprint 1' })
      expect(await ui.find({ key: 'sprint-Sprint 1' })).toBeUndefined()
      await ui.unmount()
    })
  }
})
