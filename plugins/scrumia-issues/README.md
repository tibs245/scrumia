# scrumia-issues

Experimental. A Claude Code **mod** — function hooks, not a skill module — that answers one
question during a long session: which tickets have we talked about, and where does each stand?

Specified in [`features/business/session-mods/`](https://github.com/tibs245/scrumia/blob/main/features/business/session-mods/business.md)
(section `scrumia-issues`); where it lives is
[ADR-0026](https://github.com/tibs245/scrumia/blob/main/docs/adr/0026-session-mods-are-plugins-of-their-own.md).

## What it answers

A session names many tickets, some worked on, some only mentioned. Reconstructing which is
which means rereading the conversation. This mod keeps the table as the session goes and
asks the agent to say, for each ticket, what precisely remains.

| Column | Meaning |
|---|---|
| Ticket | The number, as named by the person or by the agent. |
| In session | `✓ yes` when the session worked on or covered it, `no` when it was only named, `?` when nobody has assessed it yet. |
| Status | A column of the tracker (see below), or `Unknown`. |
| Remaining | Free text from the agent: exactly what is left to do, or `nothing`. |

## How it works

| Piece | Role |
|---|---|
| `track_issue` tool | The agent records a ticket: `number`, `isTakenIntoAccount`, `status`, `remaining`, and an optional `title`. Its description tells the agent to read the status from the board first (for example with `scrumia-board` when it is available) and report it. |
| Status vocabulary | At session start the mod runs `scrumia-extends --modules --json` to find the tracker module (`scrumia-github-project`), then `scrumia-extends --settings <its key>` and takes its `columns` (or, failing that, the keys of `board.options`), plus `Unknown`. The tool's schema lists them. A failed read is not kept: the defaults serve that call and the next call reads again. The last column, or the one `board.flow.done` names, closes a ticket. |
| Prompt detector | Every ticket number written with a leading hash in a prompt the person typed is added at once as not assessed; the next prompt carries a reminder, once. |
| Turn detector | The final text of each completed turn is read the same way, so a ticket the agent names alone reaches the table without the agent calling the tool. |
| `/issues` and its pane | One row per ticket — ticket, in session, status, remaining — open tickets first, a summary line, and a line saying where the statuses come from. |
| `$.store` | One entry per session id, `ledger:<session id>`. The thirty most recent sessions are kept. |

## What it refuses

- A ticket silently forgotten: a ticket named in a typed prompt or in the agent's final text
  is listed at once as `?` / `Unknown`, and the agent is asked to assess it.
- A status without its reason: `remaining` must be non-empty text, `nothing` when it is done.
- A malformed call: refused with its reason when the number is not an integer from 1,
  `isTakenIntoAccount` is not a boolean, the status is not one of the tracker's columns (the
  reason lists them), `remaining` is empty, or a title is not text. Nothing is stored.
- A lost ticket: writes go through one queue, so parallel calls and detections keep every ticket.
- A ticket read where nobody wrote one: a prompt the person did not type (an agent's
  hand-back, a background-task notification, a peer or coordinator message, a scheduled
  trigger, another plugin's prompt, a prompt of unknown origin) is never read. Only the
  prompt box, the Remote Control bridge, and a plugin submitting as the person count.
- The mod reading itself: lines carrying its own `[scrumia-issues]` label are left out of
  every scan, so its reminder, pasted or quoted, names nothing. Code spans, fenced code, a
  number glued to a word, `&` or `/` (entities, link fragments) and a number with a leading zero
  (`#0012`, `#000`) are not tickets either.
- Mixing sessions: the table belongs to the session id; another id starts empty.

## What it expects to find

- A Claude Code that loads plugins made of hooks modules (`hooks/hooks.json` naming
  `modules`). Older versions ignore the plugin without saying so.
- Optionally, `scrumia-extends` on the `PATH` and a project with `scrumia-github-project`
  declared in `.scrumia/config.yaml`. With neither, or when the command fails, the mod falls
  back to the six default columns (`Backlog`, `Ready for dev`, `To dev`, `In progress`,
  `In review`, `Done`) plus `Unknown`, and the pane says so with the reason. It never stops
  working for want of a tracker.
- Nothing from the network: the status is what the agent reports. The mod does not read the
  board, so it cannot tell a stale status from a right one.

## What "this session" means

The table belongs to the session id (`$.session.id()`).

| Case | What the table holds |
|---|---|
| The same session id comes back (a resume under its own id) | The same table. |
| After `/clear` | The id changes: the table starts empty, the previous one stays stored under its id. |
| A resume that goes on under a new id (a fork) | An empty table. |
| Another session | Never the tickets of this one. |

Tests change the id the mocked session answers to; whether a real resume keeps its id is
not provable with the kit and is to be tried by a person (AC-47 of the feature).

## What it ships

| What | Role |
|---|---|
| `hooks/register.tsx` | The tool, the detectors, the command and the pane, all in one module. |
| `hooks/register.test.ts` | Sixty-two tests: recording and updating in place, parallel writes, eleven malformed calls, the statuses from the tracker (its done column, a failed read read again) and the defaults in seven unreadable cases, the detector (once per ticket, the origins it refuses, its own note, code, colours and leading zeros), the agent's final text, the scope of a session (same id, `/clear`, another session, the thirty least recently touched dropped), and the pane on two surfaces, its sort included. |

## Public contract

What a later version must keep reading or announce in the changelog: the plugin name
`scrumia-issues`; the tool name `mcp__scrumia-issues__track_issue` and its `inputSchema`
(the `status` enum follows the tracker); the `/issues` command; the shape stored under
`ledger:<session id>` in `$.store` (`sessionId`, `touchedAt`, `issues`); the label
`[scrumia-issues]` that marks the mod's own text.

## Install

```
/plugin install scrumia-issues --marketplace tibs245/scrumia
```

While it is experimental, from a checkout:

```bash
claude --plugin-dir plugins/scrumia-issues
```

## Known limits

- The agent's final text is the only agent text read. A ticket named only in text written
  before a tool call within a turn reaches the table only if the agent records it. A number
  the agent writes for something else (`#1 priority`) is listed as a ticket, not assessed.
- A three-digit colour made of digits other than zeros (`#111`) outside code is read as a
  ticket.
- Whether the pane draws depends on the surface the session runs in; it is tried by a person
  on a terminal and on the desktop app.
- The status is what the agent reports; the mod does not read the board.
- Once the columns have been read successfully they are kept for the process; a change of
  tracker settings needs a new process. A failed read is retried at the next call.
- The `scrumia-questions` mod writes its numbers with a hash too (`#1`): an agent citing
  "question #2" adds a ticket that does not exist to the table, as not assessed. The mod
  cannot tell the two apart.
- The queue serialises writes inside one process; two processes writing the same session at
  the same instant are not protected.
- Interface strings are English; the free text is in whatever language the agent writes.

## Tests

```bash
claude plugin validate plugins/scrumia-issues
claude plugin test plugins/scrumia-issues
```
