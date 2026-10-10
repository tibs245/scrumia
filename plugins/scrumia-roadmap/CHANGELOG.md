# Changelog — scrumia-roadmap

All notable changes to this module, on [Keep a Changelog 1.0.0](https://keepachangelog.com/en/1.0.0/).

## [0.1.0] - 2026-10-10
### Added
- The module, a proof of concept: a Claude Code mod (function hooks), not a skill module.
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
