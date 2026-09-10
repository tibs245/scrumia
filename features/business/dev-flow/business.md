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
least one verifiable acceptance criterion and names the feature it belongs to. A
ticket whose deliverable is the parent feature itself — the bootstrap case —
names that feature the same way; what carries the intent is the acceptance
criteria, since the feature is what the ticket produces. A ticket is refused only
when it names no feature, not when the named feature does not yet exist.

## Who decides, on each path

**Brainstorming**

- The human decides whether the idea proceeds, its scope, its priority, and any
  business rule invented along the way to move it forward.
- The agent (`scrumia-discovery`, when plugged in) challenges: it questions the
  problem, the edge cases, the unstated assumptions, the legal exposure. It never
  decides in the human's place.
- If the discovery slot is empty, the human scopes by hand and says so rather than
  improvising a scoping pass. This is a degraded path, not a broken one.
- **Before an idea becomes a ticket**, it passes a content-validation gate (Gate 0,
  per ADR-0005). An agent proposes a verdict against five criteria: the problem is
  real; the solution solves it; it belongs to a named feature (or is a stated
  bootstrap exception); it does not contradict an existing rule (if it restates one,
  the replacement test decides which feature owns it — a re-route, not a refusal); it
  carries at least one verifiable acceptance criterion. The human decides on the
  agent's proposal in all cases. Four outcomes: **refused** (reason recorded), **routed**
  (belongs elsewhere), **pending** (questions remain open), **ready** (becomes ticket(s)).

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

Four gates govern both paths. Gate 0 is on brainstorming; Gates 1–3 are on execution.

| Gate | Path | Who | Blocks on |
|---|---|---|---|
| 0 — Content validation | Brainstorming | Agent proposes; human decides | Refusal, re-route, or pending clarity |
| 1 — Automatic | Execution | CI, linter, tests | A red check |
| 2 — Agent | Execution | The roles, routed by the diff's actual scope | A **Blocked** verdict |
| 3 — Human | Execution | The human | The merge — always, unless `settings.autonomy.auto_merge` names a category whose allowed-path set contains every file in the change, **and** the other three cumulative conditions (level, CI, verdict) hold |

`settings.autonomy.level` (`.scrumia/config.yaml`) widens or narrows how far into
execution the human reaches, without ever removing gate 3: `guided` adds a human
check on each ticket's scoping before execution starts; `assisted` and `autonomous`
don't. Only `autonomous`, and only where `auto_merge` reaches past its `none`
default, lets gate 3 itself go unattended — the conditions for that are ADR-0005's,
not re-decided here.

`auto_merge` is a list of named categories for the whole project, not a scalar
and not a per-ticket category. Each category names an eligible **kind of change**
and the path set whose presence proves the kind; absence of named categories
means none. There is no `all` — no general rule, no "everything not explicitly
named" — and removing the value-space entry from the configuration does not
produce it as an implicit default.

An **eligible change** is one whose full file set matches the rule below; the
conditions any unattended merge must satisfy, and the constraints any category
list must satisfy, are stated here, in this feature. The category list itself
is project data in `.scrumia/config.yaml` (same pattern as the model grid in
`features/business/execution-policy/business.md` § *The grid is project data;
what it must satisfy is not*). The trace — how the verdict is read and the
file list obtained on this tracker — is `features/business/github-tracking/`'s
to say.

### Gate 3 opens only on four cumulative conditions

Gate 3 opens unattended **only when all four hold**:

1. `settings.autonomy.level` is `autonomous`. `guided` and `assisted` retain the
   human at gate 3 unconditionally — a level below `autonomous` does not open
   the gate.
2. **Every** path in the change's full file set is matched by an active
   category. Universally, over the whole diff: one path outside any active
   category disqualifies the entire change. There is no partial credit and no
   "mostly eligible".
3. CI is green. A red check never opens gate 3, whatever the other conditions say.
4. A clean, attributable verdict is on the record — produced by a reviewer, not
   standing in by absence. A verifier that did not run, errored before
   reporting, or was not triggered at all is not a clean verdict, and what it
   carries to gate 3 is the same no-clean-verdict answer as a blocker would.

Each is necessary; none is sufficient alone. Failing any one falls back to the
human, with no overlap between conditions: a `not_run` verdict cannot be made
up by widened paths, and CI cannot be made up by a clean verdict.

### A delegation never widens itself

`.scrumia/**` is excluded from every category's allowed-path set — by
construction, not by a rule that names it. No category lists a path under
`.scrumia/**`, and no category excludes it as a named carve-out: the protection
is the shape of the predicate, not a clause in any list a future editor might
rephrase.

The generalisation matters beyond `auto_merge`. The same rule, applied
uniformly, covers `settings.autonomy.level` (lowering it empties gate 3 by
failing condition (1)), `settings.team.roles` (disabling a reviewer empties
gate 2 by leaving no role to author a clean verdict), and the execution matrix
and its declared ceiling (silently rewriting either is a path under `.scrumia/**`
and therefore ineligible by condition (2)). A special case is a rule someone
forgets to restate when a third, fourth, fifth category joins; the construction
closes that gap by including `.scrumia/**` in nothing at all.

### An absent or `not_run` verdict never opens gate 3

A verdict that did not run is a verdict that was not produced. Gate 3's fourth
condition is a clean, attributable verdict **on the record**, and "on the
record" requires a verdict there: one was posted, by a reviewer, with a
verdict and a person attributed. An empty verifier, a verifier that errored
before reporting, a verifier whose step was not triggered, and a verifier no
reviewer asked for each read the same way — as a refusal to author condition
(4), not as its satisfaction.

This is the only reading that survives a verifier that silently never fired.
The pre-condition for unattended merge is the verdict; the verdict that says
nothing says nothing.

### What shape a category list must satisfy

A category list is data the project keeps beside the rules. The rules any list
must satisfy are stated here, once:

- **Closed.** Every category is named in the list. A category that is not on
  the list does not exist for eligibility purposes. The list is read off the
  default branch at evaluation time, so two changes widening the list in
  parallel cannot both benefit in the same window.
- **Explicit.** A category names its allowed paths. No inference from "no file
  outside X" runs at evaluation time: the predicate quantifies over an
  enumerated set, not over a complement.
- **Excludes the product, the specs, the decisions and the autonomy config.**
  No category admits paths under `plugins/**` (the product — a `SKILL.md` is
  executable prose every consuming project runs), `features/**` (specs — the
  rules this feature states), `docs/adr/**` (decisions, distinct from the
  documentation they live alongside), or `.scrumia/**` (the composition,
  including the autonomy config and the category list itself). A category
  naming any of these on its allowed-path set is non-conforming, irrespective
  of what file list it produces — the rule is on the shape of the list, not
  on what an evaluation of it returns.

A list that violates any of the three is a list the rule cannot be evaluated
against — it is reported as malformed, not silently narrowed.

### Gate 2's scoping signal

Gate 2 routes by the change's actual reach and reads no scope label, because a wrong
label is precisely the failure a review exists to catch. The two therefore disagree
routinely and correctly, and a disagreement on its own reports nothing. **The gap
becomes a scoping signal on one further condition: the scope axis's own questions,
applied to what the change actually touched, would have answered higher than the label
carries** (`docs/adr/0015-scope-measures-reach.md`, whose test is stated once in
`features/business/execution-policy/`). Both conditions together, and only then, gate 2
owes the signal — reported when the gap is found, not deferred to whatever comes after.

**The signal is addressed to the manager**, the role that set the label and routes on
it. `features/business/agent-team/` states who that role is and what it owns; this
feature states only that the signal is addressed there, so that a project reshuffling
its roles changes one spec and not two.

**And it is recorded against the work item, not merely mentioned in passing**, because
a second reader depends on it: the retrospective's trigger counts label/diff gaps among
the facts that make the ceremony worth holding (`features/business/ceremonies/`), and
that trigger reads records, not conversations. A signal that exists only inside a run is
a signal the run takes with it when it dies. What the manager owes on receipt, beyond
the record existing, is written nowhere — deliberately, and it is not to be inferred
from the fact that the signal arrives.

Which artefact holds the record, and whether anything restates it for a human reading
the change, is whichever feature fills the tracker slot to say. Strip the tracker and
the obligation above still stands word for word; only its venue evaporates.

### Gate 2's verdict — recorded by the role, not asserted by the executor

**A ticket is not complete at gate 2 unless the outcome of its review is recorded.**
The outcome is one of three states, named here once and reused by every reader of the
review:

- **`run`** — the review ran *as the role*, and a verdict is attached. The transport
  that reached the role (`claude -p --agent`, a subagent invocation, anything else) is
  not a state in itself: what makes a review `run` is that it ran *as the role*, not
  that the transport happened.
- **`not_required`** — the ticket's scope prescribes no review. This is the case
  `scope/S` reaches, and only this one — `not_required` is **derived from the scope
  label, never asserted** by an executor. An executor cannot declare a ticket
  `not_required` on a `scope/M` or `scope/L`; doing so reads as the executor choosing
  which role reviews it, which is the gate-2-substitution failure the rule exists to
  prevent.
- **`not_run`** — a required review did not run as its role. **Cause is mandatory:**
  the same record that names the state names the reason the role did not run.
  `not_run` is the only failure state at this gate; everything else is reporting.

**Skip** and **unreachable** are *causes* of `not_run`, not states. A self-applied
review — the executor reading its own diff through a general agent handed the role's
definition — is not a role review; it is gate 2's self-review equivalent
(`features/business/agent-team/`'s AC-10 names why the substitution is invisible to the
reader it fools), and at the role gate it counts as `not_run`. The human at gate 3
takes the same decision for any required-and-absent review, regardless of cause.

**The verdict is recorded by the role, not by the executor.** The role's agent posts
its own verdict on the ticket's issue, in a form a later reader can find; the executor
neither writes the verdict nor writes a declaration that the review did not run.
A record written by the same run that ran the review is exactly the record that
fails on the executor's death, and an executor asserting that a review did not run
is the executor whose report the gate-3 read cannot trust — both at once. The
vocabulary the role uses and the markers it posts are `features/business/agent-team/`'s
to define; this feature states only that the verdict is the role's, and that an
absent role-signed entry makes the ticket's report incomplete.

**A verdict counts only if it is attributable.** A verdict that does not name the
role that produced it is treated as absent: `not_run`. This closes the substitution
path that a structured field written by the executor's own return would reopen —
the executor's report is not the record, and a record that the executor could have
written is not the record either.

**The orchestrator runs the role review as a net, on the absence of the carrier.**
Where the role's verdict is not on the ticket at gate 3, the orchestrator triggers
the review on that absence — a checkable fact, not a declaration by the executor. A
PR for which the tracker holds no role-signed verdict goes through the net.

`features/business/github-tracking/` materialises the carrier — the issue comment,
the pull-request body echo, the read that finds it. `features/business/agent-team/`
carries the verdict vocabulary and the rule that the role posts its own verdict;
this feature cites rather than restates it. Strip the tracker and the obligation
stands word for word: the verdict is the role's; a missing verdict is `not_run`
with a stated cause; the report is incomplete either way.

## What a commit carries, and who may rewrite one

**Every commit carries a type and a scope**: `<type>(<scope>): <subject>`. The scope is
mandatory here, on top of a standard that makes it optional, because which modules a
change touches has to be readable from history without opening a diff. Which types exist,
which namespaces a scope may draw its token from, and what each is worth for a version
are `docs/adr/0017-version-bump-and-commit-signal.md`'s — defined there once and
enumerated in no spec, this one included. `features/business/release-versioning/` states
what they are worth; this feature states that they are written, and, below, how many
tokens one commit's scope may carry.

**How many tokens a commit's scope may carry, and across which of ADR-0017's four
namespaces, is this feature's to state — below.** Which types exist and what each is
worth for a version stays ADR-0017 §2's alone.

**A commit spanning several scopes is split into one commit per scope by default.** Where
the change genuinely doesn't make sense split apart, the scope carries them comma-separated
(`feat(specs,core): …`) — across any of the four namespaces, not modules only. A commit
mirroring `design/tokens.css` (`repo`) into `site/assets/tokens.css` (`site`) takes the
shape `repo,site`: atomic across `repo` and an app, not two modules. Naming more than one
token changes nothing about what bumps: only the module tokens actually named still bump,
at ADR-0017 §2's level and no other — an app, a feature or `repo` token riding alongside
one buys it nothing. `*` never stands in for a module: every module a commit changes is
still named individually, comma-separated alongside `*` or any other token — the mandatory
scope exists so a per-module bump is derivable from history, and a module hidden under `*`
would defeat that.

**`<type>(*):` is a separate escape hatch, not a fifth namespace.** `*` stands for "touches
more scopes than are worth naming individually" — typically past three, where listing them
all stops being informative; nothing forbids it earlier, and nothing requires it once the
count is crossed; it names an informativeness judgement, not a count. It carries no bump
derivation of its own; a commit that also needs a module to bump still names that module's
real token alongside it, e.g. `refactor(specs,*): …`.

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
when, what may merge unattended — is specified here, and only here. When work is
committed is written above, under § *Who decides, on each path* → **Execution**.
The decision of how each run is isolated is below; the wording of what it implies
for the executor follows.

**A tracker feature owns the tracing and relaying of that cycle.** It states which
concrete artefact each abstract step becomes on its tool: that the reviewable
proposal is a GitHub PR opened this way, that entering execution shows up as a
column move, that a sprint is a milestone. It adapts to this feature; it does not
define it.

### Isolation: the orchestrator decides the execution mode, the executor does not isolate itself

How a batch of runs is executed — one worktree per ticket in parallel, sequentially
after the previous one, in the main tree without isolation — depends on facts only the
layer that assembled the batch holds: how many tickets, whether they conflict, whether
they can run at once. A ticket executing alone cannot know any of them, and so must
not decide for itself.

**The orchestrator decides the execution mode.** Where the batch is a sprint
assembled by `scrumia-teams`, it sets the mode (one worktree per ticket, sequential,
or another shape) and creates the worktree, citing this section. Where the batch is a
single ticket invoked directly by a human, the human is the orchestrator: the call to
`scrumia-ticket` arrives with a working tree already on the ticket's branch, the
executor reads that precondition, and the human — outside any sprint — decides whether
to isolate and how.

**One layer creates the worktree, never two.** Both `scrumia-teams:scrumia-sprint` and
`scrumia-github-project:scrumia-ticket` cite this rule and never restate it. The
executor never calls `git worktree add`: a ticket that finds no branch on its cwd has
been handed an inconsistent invocation, and stops with a comment on the issue rather
than silently isolating. Two layers writing the same isolation is the drift this rule
refuses — the second one reads as a feature, the first one is the bug.

**A relative worktree path resolves against the invoking agent's cwd.** The path
`.worktrees/<type>/<n>-<slug>` names no absolute location: it is the cwd of whoever
runs `git worktree add` that decides where it lands. Claude Code's project-scoped
permissions and harness-owned working trees mean that cwd may be a directory the
harness later tears down — a pause that hands control to a sibling, a sub-agent whose
workspace is reclaimed on return, the normal end of a session. **What carries an
execution's output is the branch, not the directory.** A commit taken before a pause
survives even if the directory is deleted afterwards; uncommitted work in a torn-down
tree is work the run may not assume it still has. The rule is the same for
`scrumia-sprint` (the orchestrator) and for a human invoking `scrumia-ticket` directly
(also the orchestrator, in that call): what they create may not survive them, so what
they commit must.

**Precedence, where the two disagree: this feature governs.** A tracker feature
found stating a different process rule is the one that must change — not this one,
and not "whichever was written last". A tracker materialises a process it does not
define, so a divergence is a defect on the tracker's side by construction. This is
part of the ownership decision, not a tie-break added after the fact.

That precedence is worth stating rather than leaving to inference, because both
features read as authoritative in isolation: each is a spec, written in the same
voice, and an agent that opens only one has no way to tell it is reading the
subordinate half.

### The sprint branch — every ticket branch of a sprint is cut from it

**A sprint runs on its own integration branch.** `sprint/<milestone-slug>`, cut from the
default branch at sprint opening and pushed before the first worktree exists. The
milestone is the sprint's boundary — two successive sprints cannot share a branch
by accident, and the name says which sprint it is. The sprint branch is deleted
when it merges into the default branch; one left in place becomes the next sprint's
ancestor by accident, which is the drift "one branch per ticket" refuses by
construction.

**`<milestone-slug>` is the milestone title lowercased, with runs of non-alphanumeric
characters collapsed to a single `-` and leading/trailing `-` trimmed.** Both the
sprint orchestrator (creating the branch) and the ticket executor (resolving its
base) derive the slug the same way — divergence here is a defect, since the
ticket skill would then resolve a branch that does not exist.

**Every ticket branch of the sprint is cut from the sprint branch, never from the
default branch.** A ticket branch's merge base at the moment of the cut is the sprint
branch's tip — `git merge-base sprint/<slug> <ticket-branch>` returns the sprint
branch's tip. A `git worktree add` that carries no start point returns whatever the
orchestrator happened to have checked out, in practice the default branch: that is
the bug the rule exists to remove.

**A ticket branch is named after its final intent — what it delivers at merge — never
after the phase it starts in.** A ticket that begins with spec commits and continues
into implementation carries the implementation's type from its first commit; the
specs phase and the implementation phase share one branch, closed by one PR. There
is no second branch and no handover between two. The type vocabulary that names the
branch — `[ADR-0017](https://github.com/tibs245/scrumia/blob/main/docs/adr/0017-version-bump-and-commit-signal.md)`
§3 — stays one list with three uses; what this rule fixes is which type a given
branch takes, not which types exist.

**A ticket's PR targets the sprint branch, not the default branch.** `gh pr create
--base sprint/<slug>`, and the PR body carries `Refs: #<n>` without a closing keyword.
The close is carried exactly once per ticket, by the sprint's own PR into the
default branch. A closing keyword in a ticket PR closes the issue the moment the
sprint branch merges, which is earlier than the ticket's own merge into the default
branch — that early close is the drift this rule refuses.

**The review's diff reads against the sprint branch.** `git diff sprint/<slug>...HEAD`,
not `origin/<default>`. A fix landed early in the sprint branch would otherwise
appear inside every later ticket's diff, and gate 2 would route on another ticket's
changes.

**The sprint branch merges into the default branch as a merge commit, never a squash.**
A squash leaves one `Refs:` trailer standing for N tickets' commits, and *What a
commit carries* (above) requires every commit of a branch to reference its own work
item. The merge commit carries the close for the whole sprint; each ticket PR carries
only `Refs:`.

**The sprint branch is not rewritten while any ticket branch cut from it is live.**
A force push on the sprint branch invalidates every ticket branch cut from it —
which is the work-loss failure *Who may rewrite* (above) forbids. The autosquash
case that needs more than this belongs to its own ticket (`sprint-fast`), where the
conditions for rewriting under live ticket branches are written.

**A ticket's card stays in `in_review` from the moment its PR merges into the sprint
branch until the sprint itself is validated; it reaches `done` when the sprint's PR
lands.** The intermediate state is read off the PR (merged, base = the sprint branch),
never off the board — a column for it would be a second copy of state already
derivable from the PR.

**A ticket invoked outside any sprint keeps working unchanged.** With no milestone, or
a milestone whose `sprint/<slug>` branch does not exist, the base falls back to the
default branch. The fallback is the same as before this rule existed — the ticket
skill does not require a sprint branch to run, and an orchestrator that never
assembles a sprint is not asked to start one.

**This section is the one statement of the sprint branch rule.** Both `scrumia-teams:
scrumia-sprint` and `scrumia-github-project:scrumia-ticket` cite it; neither
restates a trigger or an obligation beside the citation. A restated trigger is a
finding — the test is whether two copies could ever command different behaviour.

### Sprint design — one analysis before the sprint; its decisions ride the sprint branch

**A sprint is designed once, between its batch and its launch, and no ticket worktree is
cut before the design's durable decisions are on the sprint branch.** The design is one
analysis of the batch — specs and code together — made by the roles the batch's surfaces
draw: tech always, business when a rule moves, design when a screen does. Executors
implement, test and debug along the lines it states; they do not redo the analysis.
Decided in [ADR-0025](https://github.com/tibs245/scrumia/blob/main/docs/adr/0025-sprint-design-one-analysis-before-the-sprint.md).

**Its input is the tickets' footprints, crossed by a tool.** Every ticket of the batch
carries a footprint — what it reuses, creates, retires, and which surfaces it touches —
under the work-item form's rattachement (`work-item-format/standard` BR-5). The tracker
module crosses them against the tree as it is that day (`scrumia-board overlap`) and
reports what only their meeting shows: a non-spec surface two tickets share, a retirement
another ticket reuses, two identical creations, a surface that no longer exists. The
crossing computes; the design decides.

**Seams first, then one section per app.** The design opens with what crosses apps — a
shared contract that changes, a migration and its order, a port two tickets need, a spec
file two tickets write, a retirement another ticket reads — because that is where lots
merge, order is set and a shared surface gets its name. Then one section per app, on the
files that app's tickets touch, consuming the seams. Per app is the grain of the modules
and the reviewers; it is the wrong grain to start from, since the collisions this rule
exists for were never inside an app.

**Written on the model the project names.** One setting of the team module's configuration
(`sprint.design.model`), resolved through the cascade and passed to the role that writes
the page; absent, the module's ceiling stands in and the presentation says so. The
project chooses the exact model because the design is the one moment the batch is read for
everybody.

**Bounded.** The design names surfaces, an order and shared decisions; it does not design
the inside of a ticket. A line that changes neither a file, nor an order, nor a lot has no
place in it. One page, one convening.

**Durable decisions are spec edits committed on the sprint branch before the first
worktree** — the named port, the changed contract, the reserved migration number, written
into the features' own files under the specs module's authoring rules, with a changelog
entry naming the sprint. Every ticket branch inherits them at its cut, so two executors
find the same name in the same file. A decision that exists only in the design page and
not in a spec has not been made: the page is a copy, the spec is the record.

**The ephemeral part is the body of the sprint's own PR, opened as a draft on the design
commit.** The order, the merged lots, a condition ("this ticket leaves the batch if that
PR is not merged") — what is true for this sprint and false after it. The sprint's PR
already exists in this flow (§ *The close lives on the sprint's PR*, in the tracker
feature); opening it first makes the design the first thing the sprint shows, what
`scrumia-ticket` reads before the ticket, and what gate 3 reads last against the
aggregate.

**The human validates the batch and the design together**, at the same moment and in the
same presentation as Step 3 of the sprint skill. Launching stays a human decision; the
design adds no gate (ADR-0005).

**What it does not prevent, named.** A lot that removes a symbol another lot uses in a
file it *creates during the sprint* is invisible to any footprint written before it. The
design's *retires* list tells the global review which symbols to grep over the merged
tree; that grep stays the last net.

**This section is the one statement of the sprint design rule.** `scrumia-teams:
scrumia-sprint` performs it, `scrumia-sprint-fast` inherits it by citing the sprint's
Steps 1–3, `scrumia-github-project:scrumia-ticket` reads its carrier, `scrumia-refine`
and `scrumia-split` fill the footprint it consumes. None restates a trigger beside the
citation.

### sprint-fast — one global review at the end, fixups autosquashed under the orchestrator

`sprint-fast` is the mode a small batch of tickets chooses when N per-ticket role reviews
cost more than they protect. Its steps 1–3 are the sprint's — batch from the milestone,
conflicts discarded, model per ticket, human validation before anything runs. What
differs is everything after execution:

1. **Each ticket runs `scrumia-ticket` without its per-ticket role review.** Its PR
   merges into the sprint branch as soon as CI is green — gate 1 alone. A
   `process/sprint-fast` label carries what the per-issue verdict no longer does
   (`features/business/github-tracking/`), so a reader two months later can tell that
   this ticket's gate 2 was a sprint-level verdict and knows where to find it.
2. **When every ticket is merged, one global review runs** on the sprint branch against
   the default branch. Its reviewers are the union of gate 2's answers over each
   ticket's own file set: each ticket's file set is still knowable because its PR is
   merged, not lost, so the table in `scrumia-review` applies per ticket and the
   reviewers are the union. A single ticket touching a business feature draws the
   business role for the whole review. The global review also reads the aggregate
   diff for what no per-ticket review could see — two tickets that each make sense
   alone and contradict each other, a rule changed by one and consumed by another,
   a style drift visible only across five diffs. One pass, both readings.
3. **The findings are applied by one or more fix agents as `fixup!` commits**, on
   fix branches cut from the sprint branch's tip, never on the sprint branch
   itself. The orchestrator alone collects those commits and runs `git rebase
   --autosquash` on the sprint branch, exactly once.
4. **A full re-check runs on the post-squash state** before the sprint's PR opens
   against the default branch. Gate 1 and the global review both run again — a
   green CI taken before the squash is not a certification of the state after it.
   Gate 3 stays human on the sprint's PR, whatever the autonomy level: `sprint-fast`
   is not a category that opens it unattended.

**A `fixup!` carries the scope of the commit it corrects.** Autosquash keeps the
target's subject and drops the fixup's, so a fix that widens the scope would land
under an incomplete one — that fix is a commit of its own, not a fixup.

**The autosquash does not start while any ticket worktree of the sprint is open or
any ticket branch cut from the sprint branch is live.** That is a precondition to
verify, not an assumption: the gather is what answers it. A force push on the
sprint branch while a sibling holds it would destroy work a sibling committed
precisely so it could not be lost, which is the failure `docs/adr/0017` §9
already names for epic and ticket branches — the sprint branch becomes a blessed
surface for autosquash under the same boundary, **bounded to the post-execution
phase and to the orchestrator**.

**The sprint's PR opens against the default branch and carries the close once per
ticket** — exactly one `Closes #<n>` line per ticket of the sprint, and no closing
keyword in any ticket PR. A ticket PR closing on its merge into the sprint branch
is earlier than the ticket's own merge into the default branch, which is the drift
this rule refuses.

**The `sprint-fast` skill owns only what actually differs from the normal sprint.**
Steps 1–3 — batch assembly, conflict discard, model per ticket, human validation
before execution — are the normal sprint's and the new skill cites them
(`plugins/scrumia-teams/skills/scrumia-sprint-fast/` cites
`plugins/scrumia-teams/skills/scrumia-sprint/` for the shared steps). The
`scrumia-sprint` skill is unchanged in its review policy: a per-ticket review and a
per-issue verdict remain its path. Anything that copies that prose into the new
skill is restating a rule this section already states, which is the drift the
"stated once" form exists to refuse.

### Gate 2's verdict — recorded by the role, not asserted by the executor

**A ticket is not complete at gate 2 unless the outcome of its review is recorded.**
The outcome is one of three states, named here once and reused by every reader of the
review:

- **`run`** — the review ran *as the role*, and a verdict is attached. The transport
  that reached the role (`claude -p --agent`, a subagent invocation, anything else) is
  not a state in itself: what makes a review `run` is that it ran *as the role*, not
  that the transport happened.
- **`not_required`** — the ticket's scope prescribes no review. This is the case
  `scope/S` reaches, and only this one — `not_required` is **derived from the scope
  label, never asserted** by an executor. An executor cannot declare a ticket
  `not_required` on a `scope/M` or `scope/L`; doing so reads as the executor choosing
  which role reviews it, which is the gate-2-substitution failure the rule exists to
  prevent.
- **`not_run`** — a required review did not run as its role. **Cause is mandatory:**
  the same record that names the state names the reason the role did not run.
  `not_run` is the only failure state at this gate; everything else is reporting.

**Skip** and **unreachable** are *causes* of `not_run`, not states. A self-applied
review — the executor reading its own diff through a general agent handed the role's
definition — is not a role review; it is gate 2's self-review equivalent
(`features/business/agent-team/`'s AC-10 names why the substitution is invisible to the
reader it fools), and at the role gate it counts as `not_run`. The human at gate 3
takes the same decision for any required-and-absent review, regardless of cause.

**The verdict is recorded by the role, not by the executor.** The role's agent posts
its own verdict on the ticket's issue, in a form a later reader can find; the executor
neither writes the verdict nor writes a declaration that the review did not run.
A record written by the same run that ran the review is exactly the record that
fails on the executor's death, and an executor asserting that a review did not run
is the executor whose report the gate-3 read cannot trust — both at once. The
vocabulary the role uses and the markers it posts are `features/business/agent-team/`'s
to define; this feature states only that the verdict is the role's, and that an
absent role-signed entry makes the ticket's report incomplete.

**A verdict counts only if it is attributable.** A verdict that does not name the
role that produced it is treated as absent: `not_run`. This closes the substitution
path that a structured field written by the executor's own return would reopen —
the executor's report is not the record, and a record that the executor could have
written is not the record either.

**The orchestrator runs the role review as a net, on the absence of the carrier.**
Where the role's verdict is not on the ticket at gate 3, the orchestrator triggers
the review on that absence — a checkable fact, not a declaration by the executor. A
PR for which the tracker holds no role-signed verdict goes through the net.

**A `sprint-fast` sprint carries its gate-2 verdict on the sprint's PR, not on each
ticket's issue.** The verdict is still role-signed and still attributable; the venue
differs because the review itself is sprint-level. A ticket of a `sprint-fast`
sprint is `run` at gate 2 once the sprint's PR carries a role-signed verdict in the
format `features/business/agent-team/` defines, and is `not_run` otherwise — for the
same reason a single ticket is: the orchestrator's net reads the carrier's absence
as `not_run` with a cause, never as approval. The carrier is the comment on the
sprint's PR; the role's name and verdict are written there once, and every ticket
of the sprint reads from the same place. This is the human override of the
business role's "verdict per ticket" rule, and the override is recorded here once
so neither the skill nor a spec reads it as a divergence: the verdict is still
role-signed and attributable, only the venue moves.

`features/business/github-tracking/` materialises the carrier — the issue comment,
the pull-request body echo, the read that finds it. `features/business/agent-team/`
carries the verdict vocabulary and the rule that the role posts its own verdict;
this feature cites rather than restates it. Strip the tracker and the obligation
stands word for word: the verdict is the role's; a missing verdict is `not_run`
with a stated cause; the report is incomplete either way.

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
