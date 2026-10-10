# Changelog — scrumia-issues

All notable changes to this module, on [Keep a Changelog 1.0.0](https://keepachangelog.com/en/1.0.0/).

## [0.1.2] - 2026-10-10
### Fixed
- The colour of a status in the pane is derived from the tracker's columns (the done column
  in the success colour, `Unknown` in the error colour, the columns between the first and the
  done column in the warning colour, the others dim) instead of four names written in the mod.

## [0.1.1] - 2026-10-10
### Fixed
- A failed read of the tracker's columns is no longer kept for the whole process: the
  defaults serve that call and the next one reads again.
- `#0012` and any number with a leading zero is no longer read as a ticket.
- Removed a decorative `.catch` after the `prompt.submit` hook.

### Changed
- The tool description names `scrumia-board` as an example, "when it is available".
- Documented limit: the `scrumia-questions` mod writes its numbers as `#1` too: an agent citing "question #2"
  adds a false ticket to the table. Known limit, no code.
- More tests: the done column named by `board.flow.done`, the other cases of an unreadable
  tracker, the open-first sort, a real second id in the resume test, and a purge order that
  differs from the insertion order.

## [0.1.0] - 2026-10-10
### Added
- The module: a Claude Code mod (function hooks), not a skill module, placed as a plugin of
  its own by ADR-0026 and specified in `features/business/session-mods/`.
- `mcp__scrumia-issues__track_issue` — the tool the agent calls to record a ticket: its
  number, whether the session took it into account, its status, and what remains to do. Its
  description tells the agent to read the status on the board first. A malformed call is
  refused with its reason and stores nothing; writes go through one queue.
- The statuses are the tracker's columns, read at session start through `scrumia-extends`,
  plus `Unknown`; the six default columns serve when they cannot be read, and the pane says so.
- A detector on the prompts the person typed, and on the final text of each completed turn:
  every new ticket number is listed as not assessed and the next typed prompt carries a
  reminder, once. Prompts the person did not type, the mod's own label, code, entities, link
  fragments and zeros are not read.
- `/issues` and its pane: one row per ticket — ticket, in session, status, remaining — open
  tickets first, a summary line, and where the statuses come from.
- Data shape, to read again by any later version: `$.store`, key `ledger:<session id>`:
  `{ sessionId, touchedAt, issues }`; the thirty most recent sessions are kept.
