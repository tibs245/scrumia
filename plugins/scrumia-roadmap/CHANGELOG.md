# Changelog — scrumia-roadmap

All notable changes to this module, on [Keep a Changelog 1.0.0](https://keepachangelog.com/en/1.0.0/).

## [0.1.2] - 2026-10-10
### Changed
- Documentation and a test, no behaviour change: the tool description and the README say
  the mod reads no ticket state, only the tracker's list of columns, and that
  `scrumia-github-project` is optional. The test of `board.flow.done` now fails if the done
  column is taken from the last one.

## [0.1.1] - 2026-10-10
### Changed
- A ticket's status is a column of the tracker, read as `scrumia-issues` reads them
  (`scrumia-extends`, the six default columns plus `Unknown` when it cannot be read, a
  failed read not kept). Any other status is refused with the list. The hard-coded
  `done`/`closed`/`merged` and running lists are gone: a ticket is done in the tracker's
  done column (`board.flow.done`, else the last).
- "This session" is the host's session id, not the process: a sprint recorded under
  another session id is `possibly stale`. A sprint stored before this version has no id
  and shows the mark until it is recorded again.
- Two sprints cannot share an `order`: the second is refused, naming the first.
- A sprint whose state disagrees with its tickets carries a mark ("state done, N
  ticket(s) not done", "state planned, all N ticket(s) done") instead of being refused.
- README: `## Install`, "Experimental", the casing of `Testable at the end`, which
  statuses are coloured, and the limit that only the form of a testable line is checked.
- Tests: ticket number of zero or below, a "no name" case that can fail, ticket title and
  status drawn, the tracker's columns, the session id, the order, the state mark.

## [0.1.0] - 2026-10-10
### Added
- The module, experimental: a Claude Code mod (function hooks), not a skill module.
- `mcp__scrumia-roadmap__plan_sprint` — the tool the agent calls to record or update a
  sprint by name, with its order, source, objective, what is testable at its end (or an
  explicit `nothingTestable`), state and tickets; the mod stamps `resolvedAt`.
- `/roadmap` and its pane: sprints in order as bordered cards with a coloured state badge,
  objective, `Testable at the end`, tickets with description and status colour, progress
  `done/total`, `resolved <when>`, a `possibly stale` mark for a sprint not recorded in the
  session, an All / Planned / Running / Done filter and a `Remove` button.
- A malformed call is refused with its reason and nothing is stored; writes go through one
  queue, per project root.
- Data shape, to read again by any later version: `$.store`, key `project:<root>`:
  `{ sprints }`. A sprint stored with parts missing still draws.
