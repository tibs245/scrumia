# scrumia-roadmap

Experimental. A proof of concept of a Claude Code **mod** — function hooks, not a skill
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
| `plan_sprint` tool | The agent records or updates one sprint by `name`: `order` (integer), `source` (`kind` milestone, tickets, column or other, and a `reference`), `objective`, `testableAtEnd` (texts a person can try), `nothingTestable` (true when that list is empty), `state` (planned, running, done) and `tickets` (`number`, `title`, `description`, `status`). The mod stamps `resolvedAt` itself. |
| `/roadmap` and its pane | An All / Planned / Running / Done filter with counts, then the sprints in order, each a bordered card: a coloured state badge, its order and name, progress `done/total`, its source, `resolved <when>`, a `possibly stale` mark when needed, the objective, `Testable at the end`, its tickets (number, title, status in colour, description as Markdown) and a `Remove` button. |
| `$.store` | One entry per project root, `project:<root>`: the sprints. |

Progress counts the tickets whose status is `done`, `closed` or `merged` (any case). Status
colours: those green, `in progress` and `in review` yellow, anything else dim.

## What it refuses

- A malformed sprint: the call is refused with its reason when the name or objective is
  empty, the order is not an integer, the source has an unknown kind or an empty
  reference, the state is unknown, the tickets are empty or a ticket lacks a positive
  number, title, description or status, or a ticket number appears twice. Nothing is
  stored, so the pane never holds a sprint it cannot draw.
- A silently empty testable list: an empty `testableAtEnd` needs `nothingTestable: true`,
  which the pane shows in words; `nothingTestable: true` beside a non-empty list is
  refused as contradictory.
- A lost sprint: writes go through one queue, so parallel calls keep every sprint.
- A sprint passing for fresh: one not recorded in the current session is marked
  `possibly stale`.

## What it expects to find

- A Claude Code that loads plugins made of hooks modules (`hooks/hooks.json` naming
  `modules`). Older versions ignore the plugin without saying so.
- Nothing from the other ScrumIA modules and no tracker: the agent resolves the lots and
  records them; the mod reads nothing. Ticket statuses shown are the ones last recorded.

## What it ships

| What | Role |
|---|---|
| `hooks/register.tsx` | The tool, the command and the pane, all in one module. |
| `hooks/register.test.ts` | Tests: upsert in place, each refusal case, the nothing-testable statement, parallel calls, the clock stamp, the stale mark, isolation between two project roots, a sprint stored in an older shape, the order, and on two surfaces the cards, the filter and `Remove`. |

## Public contract

What a later version must keep reading or announce in the changelog: the plugin name
`scrumia-roadmap`; the tool name `mcp__scrumia-roadmap__plan_sprint` and its
`inputSchema`; the `/roadmap` command; the shape stored under `project:<root>` in
`$.store` (`sprints`, each with `name`, `order`, `source`, `objective`, `testableAtEnd`,
`nothingTestable`, `state`, `tickets`, `resolvedAt`).

## Install while it is a POC

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
  recorded in this session. The mark and the filter are per session and start again after
  a reload.
- A sprint has no age limit and is never dropped except by `Remove`.
- The queue serialises writes inside one process; two processes writing the same project
  at the same instant are not protected.

## Tests

```bash
claude plugin validate plugins/scrumia-roadmap
claude plugin test plugins/scrumia-roadmap
```
