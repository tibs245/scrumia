import { describe, expect, mock, test } from 'claude-code/testing'

const TRACK = 'mcp__scrumia-issues__track_issue'
const PANE = { component: 'Pane', props: {}, requestId: 'issues' } as const
const COMPOSER = { kind: 'composer' } as const
const TRACKER_KEY = 'tibs245/scrumia:scrumia-github-project'
const SIX = ['Backlog', 'Ready for dev', 'To dev', 'In progress', 'In review', 'Done']
const OWN_NOTE = '[scrumia-issues] Tickets named and not yet recorded: #77. Read each one'

const CALL = {
  tool: TRACK,
  number: 3528,
  isTakenIntoAccount: true,
  status: 'In progress',
  remaining: 'Write the spec of the quota',
}

type World = Parameters<Parameters<typeof test>[1]>[1]

type Options = { columns?: unknown; isTrackerBroken?: boolean }

const prepare = (on: World, options: Options = {}) => {
  const seen = { id: 'session-1', contexts: [] as (readonly string[])[], refuseNext: false, runs: [] as string[], registered: [] as unknown[] }
  mock.clock(on)
  mock.store(on)
  on('session.id', () => ({ value: seen.id }))
  on('process.run', (_$, e) => {
    seen.runs.push(e.argv.join(' '))
    if (options.isTrackerBroken) {
      return { value: { exitCode: 127, stdout: '', stderr: 'scrumia-extends: not found' } }
    }
    if (e.argv[1] === '--modules') {
      return {
        value: {
          exitCode: 0,
          stdout: JSON.stringify([
            { key: 'tibs245/scrumia:scrumia-specs', module: 'scrumia-specs', state: 'absent' },
            { key: TRACKER_KEY, module: 'scrumia-github-project', state: 'resolved' },
          ]),
          stderr: '',
        },
      }
    }

    return { value: { exitCode: 0, stdout: JSON.stringify({ columns: options.columns ?? SIX }), stderr: '' } }
  })
  on('session.start', (_$, e) => ({ cwd: e.cwd }))
  on('command.register', (_$, e) => ({ value: { command: e.name } }))
  on('tool.register', (_$, e) => {
    seen.registered.push(e)

    return { value: { tool: e.name } }
  })
  on('turn.complete', (_$, e) => ({ text: e.answer }))
  on('prompt.submit', ($, e) => {
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

const start = ($: Parameters<Parameters<typeof test>[1]>[0]) =>
  $.session.start({ cwd: '/project', surface: 'terminal', isInteractive: true })

const typed = ($: Parameters<Parameters<typeof test>[1]>[0], text: string) =>
  $.prompt.submit({ text, origin: COMPOSER })

const rows = async ($: Parameters<Parameters<typeof test>[1]>[0], numbers: number[]) => {
  const ui = await $.ui.mount({ plugin: 'scrumia-issues', surface: 'terminal', ...PANE })
  const found = await Promise.all(numbers.map(number => ui.find({ key: `issue-${number}` })))
  const text = (await ui.findAll({ type: 'Text' })).map(one => one.text).join(' | ')
  await ui.unmount()

  return { found, text }
}

describe('recording', () => {
  test('records a ticket with its status and what remains', async ($, on) => {
    prepare(on)
    const ran = await $.tool.call(CALL)
    expect(ran.deny).toBeUndefined()
    expect(said(ran)).toContain('#3528 recorded as In progress')
    expect(said(ran)).toContain('1 open of 1')
  })

  test('updates a ticket in place instead of listing it twice', async ($, on) => {
    prepare(on)
    await $.tool.call({ ...CALL, number: 12, isTakenIntoAccount: false, status: 'Backlog', remaining: 'Refine' })
    const ran = await $.tool.call({ ...CALL, number: 12, status: 'Done', remaining: 'nothing' })
    expect(said(ran)).toContain('0 open of 1')
  })

  test('three parallel calls keep three tickets', async ($, on) => {
    prepare(on)
    const ran = await Promise.all([1, 2, 3].map(number => $.tool.call({ ...CALL, number })))
    expect(ran.map(said).join(' ')).toMatch(/of 1 .*of 2 .*of 3 /)
    const { found } = await rows($, [1, 2, 3])
    expect(found.every(one => one !== undefined)).toBe(true)
  })

  test('parallel calls and a prompt naming tickets lose nothing', async ($, on) => {
    prepare(on)
    await Promise.all([$.tool.call({ ...CALL, number: 4 }), typed($, 'see #5 and #6'), $.tool.call({ ...CALL, number: 7 })])
    const { found } = await rows($, [4, 5, 6, 7])
    expect(found.every(one => one !== undefined)).toBe(true)
  })

  describe('a malformed call is refused with its reason and stores nothing', () => {
    const bad: [string, Record<string, unknown>, string][] = [
      ['a number that is text', { number: '12' }, 'number'],
      ['a number with a fraction', { number: 1.5 }, 'number'],
      ['a number below one', { number: 0 }, 'number'],
      ['no number', { number: undefined }, 'number'],
      ['no isTakenIntoAccount', { isTakenIntoAccount: undefined }, 'isTakenIntoAccount'],
      ['an isTakenIntoAccount that is text', { isTakenIntoAccount: 'yes' }, 'isTakenIntoAccount'],
      ['a status outside the columns', { status: 'Somewhere' }, 'Backlog, Ready for dev'],
      ['no status', { status: undefined }, 'status'],
      ['an empty remaining', { remaining: '   ' }, 'remaining'],
      ['no remaining', { remaining: undefined }, 'remaining'],
      ['a title that is not text', { title: 4 }, 'title'],
    ]
    for (const [name, change, reason] of bad) {
      test(name, async ($, on) => {
        prepare(on)
        const ran = await $.tool.call({ ...CALL, number: 9, ...change } as typeof CALL)
        expect(ran.deny).toContain(reason)
        expect((await rows($, [9])).found[0]).toBeUndefined()
      })
    }
  })

  test('the status is matched whatever its case, and kept as the board spells it', async ($, on) => {
    prepare(on)
    expect(said(await $.tool.call({ ...CALL, status: 'in review' }))).toContain('recorded as In review')
  })

  test('Unknown is always accepted', async ($, on) => {
    prepare(on)
    expect(said(await $.tool.call({ ...CALL, status: 'Unknown' }))).toContain('recorded as Unknown')
  })
})

describe('the status vocabulary comes from the tracker', () => {
  test('the columns of the tracker are read at session start and others are refused with the list', async ($, on) => {
    const seen = prepare(on, { columns: ['Todo', 'Doing', 'Shipped'] })
    await start($)
    expect(seen.runs).toEqual([
      'scrumia-extends --modules --json',
      `scrumia-extends --settings ${TRACKER_KEY}`,
    ])
    expect(said(await $.tool.call({ ...CALL, status: 'Doing' }))).toContain('recorded as Doing')
    const refused = await $.tool.call({ ...CALL, status: 'In progress' })
    expect(refused.deny).toContain('Todo, Doing, Shipped, Unknown')
  })

  test('the last column counts as done', async ($, on) => {
    prepare(on, { columns: ['Todo', 'Shipped'] })
    await start($)
    const ran = await $.tool.call({ ...CALL, status: 'Shipped', remaining: 'nothing' })
    expect(said(ran)).toContain('0 open of 1')
  })

  test('the six default columns serve when the tracker cannot be read, and the pane says so', async ($, on) => {
    prepare(on, { isTrackerBroken: true })
    await start($)
    expect(said(await $.tool.call({ ...CALL, status: 'Ready for dev' }))).toContain('recorded as Ready for dev')
    expect((await $.tool.call({ ...CALL, status: 'Elsewhere' })).deny).toContain(`${SIX.join(', ')}, Unknown`)
    const { text } = await rows($, [3528])
    expect(text).toContain('default columns')
    expect(text).toContain('could not be read')
  })

  test('the pane says when it uses the tracker columns', async ($, on) => {
    prepare(on, { columns: ['Todo', 'Shipped'] })
    await start($)
    expect((await rows($, [])).text).toContain("the tracker's columns (Todo, Shipped, Unknown)")
  })

  test('the status is read lazily when no session start came first', async ($, on) => {
    prepare(on, { columns: ['Todo', 'Shipped'] })
    expect((await $.tool.call({ ...CALL, status: 'Todo' })).deny).toBeUndefined()
  })

  test('the tool description tells the agent to read the board and the schema lists the columns', async ($, on) => {
    const seen = prepare(on, { columns: ['Todo', 'Shipped'] })
    await start($)
    const spec = JSON.stringify(seen.registered)
    expect(spec).toContain('Read the ticket')
    expect(spec).toContain('this tool does not check the board')
    expect(spec).toContain('"enum":["Todo","Shipped","Unknown"]')
  })
})

describe('what is detected, and from where', () => {
  test('a prompt the person typed that names new tickets asks the agent to record them, once', async ($, on) => {
    const seen = prepare(on)
    await typed($, 'look at #3528 and #12')
    await typed($, 'again #3528, plus #99')
    expect(seen.contexts[0]![0]).toContain('#3528, #12')
    expect(seen.contexts[1]![0]).toContain('#99')
    expect(seen.contexts[1]![0]).not.toContain('#3528')
  })

  test('a prompt without a ticket number passes untouched', async ($, on) => {
    const seen = prepare(on)
    await typed($, 'hello')
    expect(seen.contexts[0]).toEqual([])
  })

  test('a reminder carried by a prompt refused below is carried again', async ($, on) => {
    const seen = prepare(on)
    seen.refuseNext = true
    await typed($, 'see #8')
    await typed($, 'and now')
    expect(seen.contexts[1]![0]).toContain('#8')
  })

  test('a ticket recorded by the agent is not reminded', async ($, on) => {
    const seen = prepare(on)
    await $.tool.call({ ...CALL, number: 8 })
    await typed($, 'see #8')
    expect(seen.contexts[0]).toEqual([])
  })

  describe('a prompt the person did not type is not read', () => {
    const origins = [
      { kind: 'task-notification' },
      { kind: 'peer' },
      { kind: 'coordinator' },
      { kind: 'scheduled-trigger' },
      { kind: 'unclassified' },
      { kind: 'plugin', name: 'another-plugin' },
    ] as const
    for (const origin of origins) {
      test(origin.kind, async ($, on) => {
        const seen = prepare(on)
        await $.prompt.submit({ text: 'the sub-agent handed back #55', origin })
        expect(seen.contexts[0]).toEqual([])
        expect((await rows($, [55])).found[0]).toBeUndefined()
      })
    }

    test('a prompt with no origin at all', async ($, on) => {
      const seen = prepare(on)
      await $.prompt.submit({ text: 'see #55' })
      expect(seen.contexts[0]).toEqual([])
      expect((await rows($, [55])).found[0]).toBeUndefined()
    })

    test('a plugin that submits as the person is read', async ($, on) => {
      prepare(on)
      await $.prompt.submit({ text: 'see #56', origin: { kind: 'plugin', name: 'another-plugin', asUser: true } })
      expect((await rows($, [56])).found[0]).toBeDefined()
    })
  })

  test('the Remote Control bridge is the person typing', async ($, on) => {
    prepare(on)
    await $.prompt.submit({ text: 'see #57', origin: { kind: 'bridge' } })
    expect((await rows($, [57])).found[0]).toBeDefined()
  })

  test('the note the mod injected is not read, even pasted into a prompt', async ($, on) => {
    prepare(on)
    await typed($, `${OWN_NOTE}\nbut #78 matters`)
    const { found } = await rows($, [77, 78])
    expect(found[0]).toBeUndefined()
    expect(found[1]).toBeDefined()
  })

  test('numbers in code, a colour of zeros, a url fragment and an entity are not tickets', async ($, on) => {
    prepare(on)
    await typed($, 'colour #000, `#41`, a url /page#42, &#43; and\n```\n#44\n```\nbut #45')
    const { found } = await rows($, [0, 41, 42, 43, 44, 45])
    expect(found.map(one => one !== undefined)).toEqual([false, false, false, false, false, true])
  })

  describe('what the agent says', () => {
    const answered = (text: string, reason: 'answer' | 'aborted' | 'error' = 'answer') => ({
      answer: text,
      durationMs: 10,
      isAborted: reason === 'aborted',
      turnId: 'turn-1',
      reason,
    })

    test('a ticket the agent names alone reaches the table, as not assessed', async ($, on) => {
      prepare(on)
      await $.turn.complete(answered('I looked at #321 and it is blocked.'))
      const { found, text } = await rows($, [321])
      expect(found[0]).toBeDefined()
      expect(text).toContain('Not assessed yet')
    })

    test('the next prompt the person types asks the agent to record it, once', async ($, on) => {
      const seen = prepare(on)
      await $.turn.complete(answered('Next is #321.'))
      await typed($, 'go on')
      await typed($, 'and on')
      expect(seen.contexts[0]![0]).toContain('#321')
      expect(seen.contexts[1]).toEqual([])
    })

    test('the mod\'s own note quoted by the agent is not read', async ($, on) => {
      prepare(on)
      await $.turn.complete(answered(`You wrote: "${OWN_NOTE}"\nI will record #78 now.`))
      const { found } = await rows($, [77, 78])
      expect(found[0]).toBeUndefined()
      expect(found[1]).toBeDefined()
    })

    test('a turn that was interrupted or failed is not read', async ($, on) => {
      prepare(on)
      await $.turn.complete(answered('half of #400', 'aborted'))
      await $.turn.complete(answered('error on #401', 'error'))
      expect((await rows($, [400, 401])).found).toEqual([undefined, undefined])
    })

    test('a ticket already known is not listed twice', async ($, on) => {
      prepare(on)
      await $.tool.call({ ...CALL, number: 321 })
      await $.turn.complete(answered('Back to #321.'))
      expect(said(await $.tool.call({ ...CALL, number: 321 }))).toContain('1 open of 1')
    })
  })
})

describe('the scope of the session', () => {
  test('the table of a session is back when the same session id returns, as after a resume', async ($, on) => {
    const seen = prepare(on)
    await $.tool.call(CALL)
    seen.id = 'session-other'
    seen.id = 'session-1'
    expect((await rows($, [3528])).found[0]).toBeDefined()
    expect(said(await $.tool.call({ ...CALL, number: 1 }))).toContain('of 2')
  })

  test('after a /clear the id changes and the table starts empty, the old one kept under its id', async ($, on) => {
    const seen = prepare(on)
    await $.tool.call(CALL)
    seen.id = 'session-cleared'
    expect((await rows($, [3528])).found[0]).toBeUndefined()
    expect(said(await $.tool.call({ ...CALL, number: 1 }))).toContain('1 open of 1')
    seen.id = 'session-1'
    expect((await rows($, [3528, 1])).found.map(one => one !== undefined)).toEqual([true, false])
  })

  test('a different session never sees the tickets of another', async ($, on) => {
    const seen = prepare(on)
    await typed($, 'see #61')
    seen.id = 'session-2'
    expect((await rows($, [61])).found[0]).toBeUndefined()
    await typed($, 'see #61')
    expect(seen.contexts[1]![0]).toContain('#61')
  })

  test('only the thirty most recent sessions are kept', async ($, on) => {
    const seen = prepare(on)
    for (let one = 1; one <= 32; one++) {
      seen.id = `session-${one}`
      await $.tool.call({ ...CALL, number: one })
    }
    seen.id = 'session-1'
    expect((await rows($, [1])).found[0]).toBeUndefined()
    seen.id = 'session-32'
    expect((await rows($, [32])).found[0]).toBeDefined()
    seen.id = 'session-3'
    expect((await rows($, [3])).found[0]).toBeDefined()
  })
})

describe('the pane', () => {
  for (const surface of ['terminal', 'desktop'] as const) {
    test(`lists a mentioned ticket and a recorded one (${surface})`, async ($, on) => {
      prepare(on)
      await typed($, 'see #7')
      await $.tool.call({ ...CALL, number: 8, status: 'In review', remaining: 'Merge the PR' })
      const ui = await $.ui.mount({ plugin: 'scrumia-issues', surface, ...PANE })
      expect(await ui.find({ key: 'issue-7' })).toBeDefined()
      expect(await ui.find({ key: 'issue-8' })).toBeDefined()
      expect((await ui.find({ key: 'issue-8' }))?.text).toContain('Merge the PR')
      await ui.unmount()
    })
  }

  test('says so when no ticket was mentioned', async ($, on) => {
    prepare(on)
    expect((await rows($, [])).text).toContain('No ticket mentioned')
  })
})
