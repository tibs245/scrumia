# Changelog — scrumia-issues

All notable changes to this module, on [Keep a Changelog 1.0.0](https://keepachangelog.com/en/1.0.0/).

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
