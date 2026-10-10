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
}

type Project = { sprints: Sprint[] }

type Filter = 'all' | SprintState

const PANE = 'roadmap'
const PLAN_TOOL = 'mcp__scrumia-roadmap__plan_sprint'
const KINDS: SourceKind[] = ['milestone', 'tickets', 'column', 'other']
const STATES: SprintState[] = ['planned', 'running', 'done']
const DONE_STATUSES = ['done', 'closed', 'merged']
const RUNNING_STATUSES = ['in progress', 'in review', 'running']

let queue: Promise<unknown> = Promise.resolve()
const view: { filter: Filter; recorded: Set<string> } = { filter: 'all', recorded: new Set() }

const isText = (value: unknown): value is string => typeof value === 'string' && value.trim() !== ''
const isRecord = (value: unknown): value is Record<string, unknown> =>
  typeof value === 'object' && value !== null && !Array.isArray(value)

const stateOf = (one: Sprint): SprintState => (one.state !== undefined && STATES.includes(one.state) ? one.state : 'planned')
const ticketsOf = (one: Sprint): Ticket[] => (Array.isArray(one.tickets) ? one.tickets : [])
const isTicketDone = (one: Ticket) => DONE_STATUSES.includes(String(one.status).trim().toLowerCase())
const statusColor = (one: Ticket) =>
  isTicketDone(one) ? 'success' : RUNNING_STATUSES.includes(String(one.status).trim().toLowerCase()) ? 'warning' : 'subtle'
const stateColor = (state: SprintState) => (state === 'done' ? 'success' : state === 'running' ? 'warning' : 'suggestion')
const byOrder = (first: Sprint, second: Sprint) => first.order - second.order || first.name.localeCompare(second.name)
const staleKey = (root: string, name: string) => `${root}\u0000${name}`
const whenText = (at: number | undefined) =>
  at === undefined ? 'at an unknown time' : `${new Date(at).toISOString().slice(0, 16).replace('T', ' ')} UTC`

function problemWith(input: Record<string, unknown>): string | undefined {
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
  on('session.start', async ($, e, next) => {
    await $.command.register({
      name: 'roadmap',
      description: 'Open the roadmap of sprints the agent planned',
    })
    await $.tool.register({
      name: 'plan_sprint',
      isDeferred: false,
      description:
        'Record or update, by name, one sprint of the roadmap. A lot is whatever the person asked you to take into account (a milestone, a list of ticket numbers, a column, something else): resolve it yourself and give its source. Give the sprint order, objective, what a person can really try at its end (testableAtEnd; if nothing, an empty list with nothingTestable: true), its state (planned, running, done) and its tickets with number, title, description and board status. The call is refused when a field is missing or malformed: read the reason and call again. The mod reads no tracker: it shows only what you record.',
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
                status: { type: 'string', description: 'Board status, e.g. Ready for dev, In progress, Done' },
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
    const problem = problemWith(input)
    if (problem !== undefined) {
      return { deny: `scrumia-roadmap: ${problem}` }
    }
    const planned = input as unknown as Sprint
    const resolvedAt = await $.clock.now()
    const root = await $.session.root()
    let isReplaced = false
    await change($, project => {
      isReplaced = project.sprints.some(one => one.name === planned.name)
      const sprint: Sprint = {
        name: planned.name,
        order: planned.order,
        source: planned.source,
        objective: planned.objective,
        testableAtEnd: planned.testableAtEnd,
        nothingTestable: planned.nothingTestable === true,
        state: planned.state,
        tickets: planned.tickets,
        resolvedAt,
      }

      return {
        sprints: isReplaced
          ? project.sprints.map(one => (one.name === planned.name ? sprint : one))
          : [...project.sprints, sprint],
      }
    })
    view.recorded.add(staleKey(root, planned.name))
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
    const root = await $.session.root()
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
        {shown.length === 0 && <Text dimColor>No sprint here. The agent records them with plan_sprint.</Text>}
        {shown.map(sprint => {
          const state = stateOf(sprint)
          const tickets = ticketsOf(sprint)
          const doneCount = tickets.filter(isTicketDone).length
          const testable = Array.isArray(sprint.testableAtEnd) ? sprint.testableAtEnd : []
          const isStale = !view.recorded.has(staleKey(root, sprint.name))

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
                      <Text color={statusColor(ticket)} bold>
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
