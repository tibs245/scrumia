# scrumia-roadmap

Experimental. A Claude Code **mod** — function hooks, not a skill
module — that keeps the roadmap of the sprints the agent planned, with what will really be
testable at the end of each.

Specified in [`features/business/session-mods/`](https://github.com/tibs245/scrumia/blob/main/features/business/session-mods/business.md)
(section `scrumia-roadmap`); where it lives is
[ADR-0026](https://github.com/tibs245/scrumia/blob/main/docs/adr/0026-session-mods-are-plugins-of-their-own.md).

## What it answers

A person steering several lots of tickets wants to know what they will be able to try, and
when, without rebuilding it from the board and the conversation. A *lot* is whatever the
person asks the session to take into account: a milestone, a list of ticket numbers, a
column, or something else. The agent resolves it, plans it as sprints and records them
here with their source; the person reads them in a pane.

## How it works

| Piece | Role |
|---|---|
| `plan_sprint` tool | The agent records or updates one sprint by `name`: `order` (integer), `source` (`kind` milestone, tickets, column or other, and a `reference`), `objective`, `testableAtEnd` (texts a person can try), `nothingTestable` (true when that list is empty), `state` (planned, running, done) and `tickets` (`number`, `title`, `description`, `status`, a column of the tracker or `Unknown`). The mod stamps `resolvedAt` and the session id itself. |
| `/roadmap` and its pane | An All / Planned / Running / Done filter with counts, then the sprints in order, each a bordered card: a coloured state badge, its order and name, progress `done/total`, its source, `resolved <when>`, a `possibly stale` mark and a state mark when needed, the objective, `TESTABLE AT THE END`, its tickets (number, title, status in colour, description as Markdown) and a `Remove` button. |
| `$.store` | One entry per project root, `project:<root>`: the sprints. |

The statuses are the columns of `scrumia-github-project`, read through
`scrumia-extends` when the session starts (the six default columns plus `Unknown`, and a
line in the pane saying so, when they cannot be read; a failed read is read again). Progress counts the
tickets in the done column: `board.flow.done`, else the last column; any case. Status colours: the done
column green, `Unknown` red, the columns after the first and before the done column yellow, the
others dim.

## What it refuses

- A malformed sprint: the call is refused with its reason when the name or objective is
  empty, the order is not an integer, the source has an unknown kind or an empty
  reference, the state is unknown, the tickets are empty or a ticket lacks a positive
  number, title, description or status, a ticket status is not a column of the tracker
  (the list is given), or a ticket number appears twice. A sprint recorded under a new
  name with the `order` of another is refused too: the order is unique. Nothing is
  stored, so the pane never holds a sprint it cannot draw.
- A silently empty testable list: an empty `testableAtEnd` needs `nothingTestable: true`,
  which the pane shows in words; `nothingTestable: true` beside a non-empty list is
  refused as contradictory.
- A lost sprint: writes go through one queue, so parallel calls keep every sprint.
- A sprint passing for fresh: one not recorded under the current session id is marked
  `possibly stale`.
- A state that contradicts the tickets is not refused but marked: "state done, N
  ticket(s) not done" on a done sprint, "state planned, all N ticket(s) done" on a planned one.

## What it expects to find

- A Claude Code that loads plugins made of hooks modules (`hooks/hooks.json` naming
  `modules`). Older versions ignore the plugin without saying so.
- No ticket state, only the tracker's list of columns: the agent resolves the lots and
  records them; the mod reads nothing of the board but those columns, through
  `scrumia-extends`. The module `scrumia-github-project` is optional: without it the
  default columns apply. Ticket statuses shown are the ones last recorded.

## What it ships

| What | Role |
|---|---|
| `hooks/register.tsx` | The tool, the command and the pane, all in one module. |
| `hooks/register.test.ts` | Tests: upsert in place, each refusal case, the nothing-testable statement, parallel calls, the clock stamp, the stale mark under a changing session id, the tracker's columns and the done column, the unique order, the state mark, isolation between two project roots, a sprint stored in an older shape, the order, and on two surfaces the cards, the filter and `Remove`. |

## Public contract

What a later version must keep reading or announce in the changelog: the plugin name
`scrumia-roadmap`; the tool name `mcp__scrumia-roadmap__plan_sprint` and its
`inputSchema`; the `/roadmap` command; the shape stored under `project:<root>` in
`$.store` (`sprints`, each with `name`, `order`, `source`, `objective`, `testableAtEnd`,
`nothingTestable`, `state`, `tickets`, `resolvedAt`).

## Install

```
/plugin install scrumia-roadmap --marketplace tibs245/scrumia
```

For development, from a checkout of the repository:

```bash
claude --plugin-dir plugins/scrumia-roadmap
```

## Known limits

- Whether the pane draws depends on the surface the session runs in; it is tested here
  with mocked terminal and desktop surfaces, and not yet tried by a person on the real ones.
- Chrome strings are English; sprint texts are whatever language the agent writes in.
- The roadmap belongs to the machine and to the project root it was recorded in: nothing
  is written in the repo, and two sessions open on the same project share it. The
  tracker stays the source of truth; the roadmap is the agent's last reading of it.
- The mod cannot know that the board moved: `possibly stale` only says the sprint was not
  recorded under this session id. The filter is per process and starts again after a reload.
- The mod checks the form of `testableAtEnd`, not its truth: it cannot judge whether a
  line is something a person can really try. That stays with the agent and the person who reads the card.
- A sprint has no age limit and is never dropped except by `Remove`.
- The queue serialises writes inside one process; two processes writing the same project
  at the same instant are not protected.

## Tests

```bash
claude plugin validate plugins/scrumia-roadmap
claude plugin test plugins/scrumia-roadmap
```
