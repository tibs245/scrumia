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
- The human's unconditional decision point is the merge, per gate 3 below. Under
  `guided` autonomy the human also validates each ticket's transition into
  execution — a second decision, before any agent starts.

## Where the human gate sits (ADR-0005)

The three-gate model governs the **execution** path. Brainstorming carries no gate
of its own, because the human is already the decision-maker throughout it.

| Gate | Path | Who | Blocks on |
|---|---|---|---|
| 1 — Automatic | Execution | CI, linter, tests | A red check |
| 2 — Agent | Execution | The roles, routed by the diff's actual scope | A **Blocked** verdict |
| 3 — Human | Execution | The human | The merge — always, unless `settings.autonomy.auto_merge` is set past `none` and the PR falls within what it covers |

`settings.autonomy.level` (`.scrumia/config.yaml`) widens or narrows how far into
execution the human reaches, without ever removing gate 3: `guided` adds a human
check on each ticket's scoping before execution starts; `assisted` and `autonomous`
don't. Only `autonomous`, and only where `auto_merge` reaches past its `none`
default, lets gate 3 itself go unattended — the conditions for that are ADR-0005's,
not re-decided here.

`auto_merge` is one scalar for the whole project, not a per-ticket category:
`none` (nothing merges unattended), `docs-only` (a PR touching documentation and
nothing else), or `all`. What exactly counts as docs-only, and what happens to a
PR mixing docs and code, is #17's to pin down.

## The code cycle: this feature is the process, a tracker feature is its trace

**This feature owns the code cycle.** How a scoped ticket becomes a reviewable
change — isolation per ticket, when work is committed, what must be reviewed and
when, what may merge unattended — is specified here, and only here. Not all of it is
written down yet: worktree ownership and commit-before-pause land in this file
through #118 and #20. Ownership is settled; the wording of those rules follows.

**A tracker feature owns the tracing and relaying of that cycle.** It states which
concrete artefact each abstract step becomes on its tool: that the reviewable
proposal is a GitHub PR opened this way, that entering execution shows up as a
column move, that a sprint is a milestone. It adapts to this feature; it does not
define it.

**Precedence, where the two disagree: this feature governs.** A tracker feature
found stating a different process rule is the one that must change — not this one,
and not "whichever was written last". A tracker materialises a process it does not
define, so a divergence is a defect on the tracker's side by construction. This is
part of the ownership decision, not a tie-break added after the fact.

That precedence is worth stating rather than leaving to inference, because both
features read as authoritative in isolation: each is a spec, written in the same
voice, and an agent that opens only one has no way to tell it is reading the
subordinate half.

### The replacement test — which feature does a rule belong to?

Apply it before filing any rule about how code ships, at refinement time and when
reviewing a spec change. Replace the tracker with a hypothetical
`scrumia-tracker-local` — a file-based tracker, no PR, no board:

- **The rule stays true, word for word → it belongs here.** One worktree per ticket,
  one branch per ticket, commit before any pause or review, review before merge, the
  three gates, `auto_merge`. None of them mentions a tracker to be stated.
- **The rule becomes meaningless → it belongs to the tracker feature.** Opening a PR
  and linking it to its issue, column transitions, milestone-as-sprint,
  epic-as-native-sub-issues, board reading discipline. Each names an artefact that
  ceases to exist.

Every rule has exactly one answer, and a rule is written on one side only: this
feature states the abstract ("an execution ends in a reviewable proposal; gate 3
governs its merge"), the tracker feature binds it to the concrete ("that proposal is
a GitHub PR, opened this way"). Restating the abstract rule alongside its binding
creates a second copy that drifts — the same trap `scope/*` avoids by being
specified once in `features/business/execution-policy/` and restated by neither
consumer.

This is a question about **spec files**, not about modules.
`docs/adr/0013-tracker-stays-one-slot.md` decides something else — that the `tracker`
slot is not split into a `forge` slot — and assigns no ownership of specs. The
tracker module implementing the code cycle and this feature specifying it are both
true at once; they are different planes, and neither overrides the other.
