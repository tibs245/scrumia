# Dev flow — business rules

## Value

For the humans steering brainstorming and the agents executing tickets — everyone
whose next move depends on which of the two paths they are on. It brings a clean split
of who decides what, plus the code-cycle rules (branch per ticket, commit before every
yield, the three gates) that any tracker must trace rather than redefine. It matters
because a ticket with no verifiable acceptance criterion, or a run whose in-flight work
is not committed before it yields, is exactly the drift this feature refuses — and a
tracker feature restating the process instead of tracing it is the same drift one plane
over. Not instrumented today: no measure counts refused executions or commit-before-
yield compliance; both are read from the ticket and the branch, not from a dashboard.

## The two paths

**Brainstorming** — from an idea to a scoped ticket. **Execution** — from a scoped
ticket to a PR. A ticket is the boundary between them: it exists once it carries at
least one verifiable acceptance criterion and names the feature it belongs to (or,
for the bootstrap case — a ticket whose deliverable is the parent feature itself,
normally refused at Step 0 and admitted only by a stated exception — is what it
produces).

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
- **An execution commits its in-flight work to the ticket's branch before the run
  yields control.** A yield is any pause that hands the next move to someone else —
  a role review, a sub-agent, a human verdict, a wait on a check. The rule is stated
  as the general case on purpose: it covers every yield point, including the ones no
  skill enumerates yet, because a pause added later is exactly the one an enumeration
  would leave uncovered.
- What carries an execution's output is **the branch**, not the working tree. The
  working tree belongs to whatever process happens to hold it, and that process can
  vanish while the run is paused; a branch survives it. Uncommitted work is therefore
  not work the run may assume it still has — and a reviewer asked for a verdict is
  reading the branch, so uncommitted work is also not under review.
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
PR mixing docs and code, is not yet pinned down.

## What a commit carries, and who may rewrite one

**Every commit carries a type and a scope**: `<type>(<scope>): <subject>`. The scope is
mandatory here, on top of a standard that makes it optional, because which modules a
change touches has to be readable from history without opening a diff. Which types exist,
which namespaces a scope may draw its token from, and what each is worth for a version
are `docs/adr/0017-version-bump-and-commit-signal.md`'s — defined there once and
enumerated in no spec, this one included. `features/business/release-versioning/` states
what they are worth; this feature states that they are written.

**A commit spanning several scopes is split into one commit per scope by default.** Where
the change genuinely doesn't make sense split apart, the scope carries them comma-separated
(`feat(specs,core): …`) — across any of ADR-0017 §2's four namespaces, not modules only. The
repo's own instance: `design/tokens.css` (`repo`) mirrored into `site/assets/tokens.css`
(`site`) by one commit (`ec58969`), across `repo` and an app, not two modules. Naming more
than one token changes nothing about what bumps: only the module tokens actually named still
bump, at ADR-0017 §2's level and no other — an app, a feature or `repo` token riding
alongside one buys it nothing.

**`<type>(*):` is a separate escape hatch, not a fifth namespace.** `*` stands for "touches
more scopes than are worth naming individually" — useful once a commit spans more than
three, where listing them all stops being informative. It carries no bump derivation of its
own; a commit that also needs a module to bump still names that module's real token
alongside it, e.g. `refactor(specs,*): …`.

**The same vocabulary names the branch and titles the reviewable proposal.** One list,
three uses, so a branch prefix that appears in no type list cannot exist.

A commit's **scope** and a ticket's `scope/*` label are different words that happen to
match. The label measures how far a change reaches and decides which model runs it
(`features/business/execution-policy/`); a commit's scope names *what* the change touches
and carries no size judgement. Neither is derivable from the other, and neither is read
where the other is expected.

**Every commit of a branch references the work item it belongs to.** Redundant is fine;
incomplete is not — a lookup that returns some of a ticket's commits is worse than one
that returns none, because it reads complete. **Exactly one closing statement per change,
carried by the reviewable proposal rather than by a commit**, so that what closed a work
item stays answerable. The concrete spellings of both — the trailer, the keyword, and
which of them the tool acts on — belong to whichever feature fills the tracker slot;
neither survives a tracker with no issues, and neither is restated here.

**Rewriting a branch's own history is allowed; rewriting the default branch's is not.**
Squashing a correction into the commit it fixes is blessed on epic and ticket branches
and banned on the default branch, and only the executor that owns a branch may do it
there. The cost is why the boundary exists: the targets are commits that are already
pushed, so the rewrite needs a force push — and during a sprint several worktrees share
one `.git`, where a sibling may already have fetched the branch. A force push on anything
a sibling reads destroys work that was committed precisely so it could not be lost, which
is the same failure the commit-before-yield rule above exists to prevent.

## The code cycle: this feature is the process, a tracker feature is its trace

**This feature owns the code cycle.** How a scoped ticket becomes a reviewable
change — isolation per ticket, when work is committed, what must be reviewed and
when, what may merge unattended — is specified here, and only here. Not all of it is
written down yet: worktree ownership is not yet written down in this file. When work
is committed is written above, under § *Who decides, on each path* → **Execution**.
Ownership is settled; the wording of what remains follows.

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
  one branch per ticket, commit before the run yields control, review before merge,
  the three gates, `auto_merge`, a commit's mandatory type and scope, one reference per
  commit to its work item, the branch boundary on rewriting history. None of them
  mentions a tracker to be stated.
- **The rule becomes meaningless → it belongs to the tracker feature.** Opening a PR
  and linking it to its issue, column transitions, milestone-as-sprint,
  epic-as-native-sub-issues, board reading discipline, the spelling of the reference
  trailer and of the closing keyword. Each names an artefact that ceases to exist.

Apply it to one atomic statement at a time. A rule that returns both answers is two
rules — splitting it is the first step, not a sign the test failed.

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
