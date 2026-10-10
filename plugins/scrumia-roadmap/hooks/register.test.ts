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

const TRACKER_KEY = 'tibs245/scrumia:scrumia-github-project'
const SIX = ['Backlog', 'Ready for dev', 'To dev', 'In progress', 'In review', 'Done']

type Options = { entries?: Record<string, unknown>; settings?: unknown; isTrackerBroken?: boolean; isFirstReadFailing?: boolean }

const prepare = (on: World, options: Options = {}) => {
  const seen = { root: '/project-a', id: 'session-1', reads: 0, registered: [] as unknown[] }
  const clock = mock.clock(on)
  mock.store(on, options.entries)
  on('session.root', () => ({ value: seen.root }))
  on('session.id', () => ({ value: seen.id }))
  on('process.run', (_$, e) => {
    if (options.isTrackerBroken) {
      return { value: { exitCode: 127, stdout: '', stderr: 'scrumia-extends: not found' } }
    }
    if (e.argv[1] === '--modules') {
      seen.reads += 1
      if (options.isFirstReadFailing && seen.reads === 1) {
        return { value: { exitCode: 1, stdout: '', stderr: 'transient' } }
      }

      return {
        value: { exitCode: 0, stdout: JSON.stringify([{ key: TRACKER_KEY, module: 'scrumia-github-project', state: 'resolved' }]), stderr: '' },
      }
    }

    return { value: { exitCode: 0, stdout: JSON.stringify(options.settings ?? { columns: SIX }), stderr: '' } }
  })
  on('session.start', (_$, e) => ({ cwd: e.cwd }))
  on('command.register', (_$, e) => ({ value: { command: e.name } }))
  on('tool.register', (_$, e) => {
    seen.registered.push(e)

    return { value: { tool: e.name } }
  })

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
      ['no name', { name: undefined }, 'name must be non-empty text'],
      ['a ticket number of zero', { tickets: [{ number: 0, title: 't', description: 'd', status: 'Done' }] }, 'positive integer'],
      ['a negative ticket number', { tickets: [{ number: -3, title: 't', description: 'd', status: 'Done' }] }, 'positive integer'],
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
        expect(await ui.find({ type: 'Text', text: /No sprint here/ })).toBeDefined()
        expect(await ui.find({ type: 'Text', text: /^\d\. / })).toBeUndefined()
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

  test('a sprint recorded under another session id is possibly stale', async ($, on) => {
    const seen = prepare(on)
    await $.tool.call(PLAN)
    const ui = await $.ui.mount({ plugin: 'scrumia-roadmap', surface: 'terminal', ...PANE })
    expect(await ui.find({ type: 'Text', text: 'possibly stale' })).toBeUndefined()
    await ui.unmount()
    seen.id = 'session-2'
    const later = await $.ui.mount({ plugin: 'scrumia-roadmap', surface: 'terminal', ...PANE })
    expect(await later.find({ type: 'Text', text: 'possibly stale' })).toBeDefined()
    await later.unmount()
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

  describe('the statuses are the columns of the tracker', () => {
    const SHIPPED = { columns: ['Todo', 'Doing', 'Shipped'] }
    const tickets = (...statuses: string[]) =>
      statuses.map((status, index) => ({ number: index + 1, title: `T${index}`, description: 'd', status }))

    test('a tracker whose last column is Shipped counts it as done', async ($, on) => {
      prepare(on, { settings: SHIPPED })
      await $.tool.call(plan({ tickets: tickets('Shipped') }))
      const ui = await $.ui.mount({ plugin: 'scrumia-roadmap', surface: 'terminal', ...PANE })
      expect(await ui.find({ type: 'Text', text: /1\/1 done/ })).toBeDefined()
      await ui.unmount()
    })

    test('the done column named by board.flow.done wins over the last', async ($, on) => {
      prepare(on, { settings: { columns: ['Todo', 'Shipped', 'Archived'], board: { flow: { done: 'Shipped' } } } })
      await $.tool.call(plan({ tickets: tickets('Shipped') }))
      const ui = await $.ui.mount({ plugin: 'scrumia-roadmap', surface: 'terminal', ...PANE })
      expect(await ui.find({ type: 'Text', text: /1\/1 done/ })).toBeDefined()
      await ui.unmount()
    })

    test('a status outside the columns is refused with the list; Unknown is allowed', async ($, on) => {
      prepare(on, { settings: SHIPPED })
      const refused = await $.tool.call(plan({ tickets: tickets('Done') }))
      expect(refused.deny).toContain('Todo, Doing, Shipped, Unknown')
      expect(said(await $.tool.call(plan({ tickets: tickets('unknown', 'shipped') })))).toContain('recorded')
    })

    test('the tool registered at start lists the columns', async ($, on) => {
      const seen = prepare(on, { settings: SHIPPED })
      await $.session.start({ cwd: '/project', surface: 'terminal', isInteractive: true })
      expect(JSON.stringify(seen.registered)).toContain('"enum":["Todo","Doing","Shipped","Unknown"]')
    })

    test('an unreadable tracker falls back to the default columns, says so, and reads again next time', async ($, on) => {
      prepare(on, { isTrackerBroken: true })
      await $.tool.call(plan({ tickets: tickets('Done', 'Backlog') }))
      expect((await $.tool.call(plan({ tickets: tickets('Shipped') }))).deny).toContain(`${SIX.join(', ')}, Unknown`)
      const ui = await $.ui.mount({ plugin: 'scrumia-roadmap', surface: 'terminal', ...PANE })
      expect(await ui.find({ type: 'Text', text: /Default columns in use/ })).toBeDefined()
      expect(await ui.find({ type: 'Text', text: /1\/2 done/ })).toBeDefined()
      await ui.unmount()
    })

    test('a failed first read is not kept: the next call reads the tracker', async ($, on) => {
      prepare(on, { isFirstReadFailing: true, settings: SHIPPED })
      expect((await $.tool.call(plan({ tickets: tickets('Backlog') }))).deny).toBeUndefined()
      expect((await $.tool.call(plan({ name: 'Other', order: 2, tickets: tickets('Backlog') }))).deny).toContain('Todo, Doing, Shipped')
    })
  })

  test('two sprints with the same order: the second is refused and the first stays', async ($, on) => {
    prepare(on)
    await $.tool.call(PLAN)
    const refused = await $.tool.call(plan({ name: 'Sprint 2' }))
    expect(refused.deny).toContain('order 1')
    expect(refused.deny).toContain('Sprint 1')
    expect(said(await $.tool.call(plan({ objective: 'Same name, same order' })))).toContain('updated')
    const ui = await $.ui.mount({ plugin: 'scrumia-roadmap', surface: 'terminal', ...PANE })
    expect(await ui.find({ key: 'sprint-Sprint 2' })).toBeUndefined()
    await ui.unmount()
  })

  for (const surface of ['terminal', 'desktop'] as const) {
    test(`a state that disagrees with the tickets is marked, not refused (${surface})`, async ($, on) => {
      prepare(on)
      const ticket = (number: number, status: string) => ({ number, title: `T${number}`, description: 'd', status })
      expect(said(await $.tool.call(plan({ name: 'Claims done', order: 1, state: 'done', tickets: [ticket(1, 'Done'), ticket(2, 'In progress'), ticket(3, 'Backlog')] })))).toContain('recorded')
      expect(said(await $.tool.call(plan({ name: 'Claims planned', order: 2, state: 'planned', tickets: [ticket(4, 'Done'), ticket(5, 'Done')] })))).toContain('recorded')
      await $.tool.call(plan({ name: 'Consistent', order: 3, state: 'running', tickets: [ticket(6, 'Done'), ticket(7, 'Backlog')] }))
      const ui = await $.ui.mount({ plugin: 'scrumia-roadmap', surface, ...PANE })
      expect(await ui.find({ type: 'Text', text: 'state done, 2 ticket(s) not done' })).toBeDefined()
      expect(await ui.find({ type: 'Text', text: 'state planned, all 2 ticket(s) done' })).toBeDefined()
      expect(await ui.findAll({ type: 'Text', text: /^state (done|planned),/ })).toHaveLength(2)
      await ui.unmount()
    })
  }

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
      expect(await ui.find({ type: 'Text', text: 'Questions inbox' })).toBeDefined()
      expect(await ui.find({ type: 'Text', text: 'Issues view' })).toBeDefined()
      expect(await ui.find({ type: 'Text', text: 'Done' })).toBeDefined()
      expect(await ui.find({ type: 'Text', text: 'In progress' })).toBeDefined()
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
