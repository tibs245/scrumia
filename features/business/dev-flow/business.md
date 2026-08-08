# Dev flow — business rules

## The two paths

**Brainstorming** — from an idea to a scoped ticket. **Execution** — from a scoped
ticket to a PR. A ticket is the boundary between them: it exists once it carries at
least one verifiable acceptance criterion and names the feature it belongs to (or,
for the bootstrap case, is what it produces — see #18).

## Who decides, on each path

**Brainstorming**

- The human decides whether the idea proceeds, its scope, its priority, and any
  business rule invented along the way to move it forward.
- The agent (`scrumia-discovery`, when plugged in) challenges: it questions the
  problem, the edge cases, the unstated assumptions, the legal exposure. It never
  decides in the human's place.
- If the discovery slot is empty, the human scopes by hand and says so rather than
  improvising a scoping pass. This is a degraded path, not a broken one.

**Execution**

- Agents decide the implementation, within the ticket's scope.
- The standing roles decide within what they own — `scrumia-tech` on architecture
  and implementation quality, `scrumia-business` on business-rule consistency —
  never outside it.
- Neither role settles a business rule found missing mid-execution: that stops the
  run and escalates instead, per `settings.team.escalation.to_human` in
  `.scrumia/config.yaml`.
- The human decides only the merge, per the gate below.

## Where the human gate sits (ADR-0005)

The three-gate model governs the **execution** path. Brainstorming carries no gate
of its own, because the human is already the decision-maker throughout it.

| Gate | Path | Who | Blocks on |
|---|---|---|---|
| 1 — Automatic | Execution | CI, linter, tests | A red check |
| 2 — Agent | Execution | The roles, routed by the diff's actual scope | A **Blocked** verdict |
| 3 — Human | Execution | The human | The merge — always, except a category explicitly listed in `settings.autonomy.auto_merge` |

`settings.autonomy.level` (`.scrumia/config.yaml`) widens or narrows how far into
execution the human reaches, without ever removing gate 3: `guided` adds a human
check on each ticket's scoping before execution starts; `assisted` and `autonomous`
don't. Only `autonomous`, and only for the categories named in `auto_merge`, lets
gate 3 itself go unattended — the conditions for that are ADR-0005's, not
re-decided here.
