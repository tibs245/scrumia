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

## Covering a criterion

An execution must show, for each acceptance criterion it is answerable for, something
that could have failed. **Falsifiability is the requirement; a test file is the form it
takes where the criterion's subject is executable behaviour.** The form follows the
**criterion's own subject**, never the deliverable's overall nature:

- **A criterion whose subject is executable behaviour** — covered by a test that can
  fail. A ticket carrying code never trades such a criterion for a section reference,
  whatever prose it also delivers.
- **A criterion whose subject is prose** — a rule, a specification, a piece of
  agent-executed text — covered by the section that satisfies it, the criterion itself
  written so that a concrete case could contradict it. A criterion no case could
  contradict is not covered; pointing at a section does not rescue it.

**Which side a criterion falls on is decided by its subject, not by the tooling that
happens to exist.** Its subject is prose where there is nothing to execute: a rule, a
wording, a document. Its subject is executable behaviour where something the project
runs would behave differently depending on whether the criterion holds. **An absent
harness does not make a criterion prose** — where a behaviour criterion has no test to
run yet, writing that test is part of the work, not a reason to reclassify it. Asking
which runner could exercise an artefact settles a borderline case; it never settles
whether a behaviour owes a test.

Keying the form to the criterion rather than to the deliverable is what keeps a mixed
ticket answerable. One shipping code *and* a spec change owes tests for its behaviour
criteria and sections for its prose criteria, in the same proposal, with no reading
under which either half escapes — where the deliverable decided the form, such a ticket
would face an impossible instruction and pick its way out of it.

The second form is not a softening of the first. It exists because a criterion with
nothing to execute cannot satisfy the first at all, and an execution meeting that wall
invents a substitute of its own.

**This is what *verifiable* means** in § *The two paths*, what `qa.md` AC-1 calls "an
acceptance criterion that can fail", and what ADR-0004 calls verifiable — one property
under three names, not three requirements.

**Which criteria an execution is answerable for**: the ticket's own, plus those it adds
to or amends in the feature's acceptance file. A criterion already standing in that
file and untouched by the ticket is not this execution's to re-cover; it was covered
when it was written.

**Not being answerable for a standing criterion is no licence to break one.** A
criterion the ticket contradicts without touching is a contradiction surfacing
mid-execution: the run stops and escalates under § *Who decides, on each path* →
**Execution**, `qa.md` AC-2's case. And the project's tests and linter run in every
case, whatever the execution is answerable for.

A ticket whose entire deliverable is the specification satisfies the spec-before-code
sequencing rather than waiving it: there is no second half to sequence against. Its
implementation step finding no code to write is a legitimate outcome, not a skipped
step.

## The ticket's criteria and the feature's are two namespaces

A ticket carries acceptance criteria and so does the feature it belongs to. The two
sets are complementary, and they are not interchangeable:

- **A ticket's criteria are a work order.** They say what this ticket must deliver,
  and they expire when it closes. "Remove the placeholder file" is a legitimate
  delivery criterion and will never be a standing guarantee.
- **A feature's criteria are a standing contract.** They say what the feature
  guarantees from now on, and they must keep holding long after every ticket that
  touched them is closed.

Their counts therefore need not match, and a difference between them is not a defect:
one delivery criterion can produce two standing guarantees, some standing guarantees
predate the ticket, and some delivery acts produce none at all. A 1:1 mapping is not
achievable and is not to be demanded.

**A reviewable proposal maps its delivery against the ticket's criteria** — the first
question a reviewer asks is whether the ticket delivered what it promised, and the work
order is what it promised. **It states separately, in its own list, which of the
feature's criteria it added or amended.** Two lists, two purposes, never merged.

**A criterion is cited with its namespace.** Both sets are numbered in the same format,
so a bare identifier means two different things depending on which document the reader
has open. A feature criterion is cited with its file (`dev-flow/qa.md AC-3`); a ticket
criterion is cited bare (`AC-3`). Naming a criterion without saying which namespace it
belongs to is the defect, whichever document does it.

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
written down yet: worktree ownership lands in this file through #20. When work is
committed is written above, under § *Who decides, on each path* → **Execution**.
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
  the three gates, `auto_merge`. None of them mentions a tracker to be stated.
- **The rule becomes meaningless → it belongs to the tracker feature.** Opening a PR
  and linking it to its issue, column transitions, milestone-as-sprint,
  epic-as-native-sub-issues, board reading discipline. Each names an artefact that
  ceases to exist.

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
