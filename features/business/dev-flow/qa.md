# Acceptance criteria — dev-flow

Given/When/Then, one scenario per case. These are process-level criteria: verified
by reading the ticket, its labels, `.scrumia/config.yaml` and the specs — not by
application code.

## Brainstorming content validation (Gate 0)

### AC-1 — An agent proposes verdict on five criteria; the human decides

```gherkin
Given an idea an agent assesses against five criteria: the problem is real, the
  solution solves it, it belongs to a named feature, it contradicts no existing rule,
  it carries at least one verifiable acceptance criterion
When the agent proposes a verdict (refused, routed, pending, or ready)
Then the human decides — no agent closes or routes an idea without the human's decision
```

### AC-2 — Refused ideas state their reason; the reason survives the refusal

```gherkin
Given an idea an agent judges non-pertinent or contradicted by an existing rule
When the agent reports the refusal
Then it cites the rule or principle it contradicts, and this reason is recorded so it
  can be revisited if the idea is re-proposed
```

### AC-3 — An idea that lacks a verifiable criterion or a feature name is not refused; it is pending

```gherkin
Given an idea that carries no verifiable acceptance criterion, or is not assigned to
  a named feature
When it is checked against the ticket boundary
Then it is marked pending rather than refused — the agent names what is missing, and
  the idea remains available for the human to address
```

### AC-4 — An idea that is well-formed but belongs to another feature is routed, not refused

```gherkin
Given an idea that is sound and verifiable, but the replacement test says it belongs
  to a different feature than where it was proposed
When the agent makes this assessment
Then it proposes re-routing with the target feature named, and the human decides
  whether to move it or close it
```

### AC-5 — A ready idea becomes one or more tickets

```gherkin
Given an idea that passes all five criteria and carries at least one verifiable
  acceptance criterion and a feature name
When it is marked ready
Then it becomes a ticket (or multiple tickets, if the idea spans more than one) that
  names the feature and carries its acceptance criteria
```

## Nominal execution

### AC-6 — No verifiable acceptance criterion, no execution

```gherkin
Given a ticket with no acceptance criterion that can fail
When execution starts (`scrumia-ticket` Step 0)
Then it is refused, a comment on the issue names precisely what's missing, and
  nothing is executed on a guessed intent
```

### AC-18 — A ticket that names the feature it produces is not refused at Step 0

```gherkin
Given a ticket whose deliverable is the parent feature it names — the bootstrap case,
  an empty `specs_root` on the project's first ticket being the canonical instance
When execution starts (`scrumia-ticket` Step 0)
Then it runs and produces the feature, rather than being refused for the feature's
  absence — the refusal fires on a ticket that names no feature, not on one that
  names a feature that does not yet exist
```

## Edge cases

### AC-7 — A business rule found missing mid-execution is escalated, not invented

```gherkin
Given an execution run that finds a business rule missing, or contradicted by
  another feature
When the contradiction surfaces
Then the run stops, comments on the issue, and calls on the business role instead
  of deciding the rule itself
```

### AC-8 — Discovery absent: the human scopes directly, and says so

```gherkin
Given the discovery slot is empty in `.scrumia/config.yaml`
When an idea needs scoping
Then the human scopes it by hand into a ticket, and the absence of a scoping pass
  is stated rather than silently improvised
```

### AC-9 — Guided autonomy adds a human check before execution starts

```gherkin
Given `settings.autonomy.level` is `guided`
When a ticket finishes scoping
Then the human validates the transition to execution before an agent starts it
```

### AC-10 — Gate 3 opens only on four cumulative conditions

```gherkin
Given `settings.autonomy.level` is `autonomous`, every path in the change's
  full file set is matched by an active category of `settings.autonomy.auto_merge`,
  CI is green, and a clean attributable verdict is on the record
When gate 3 is evaluated
Then the change merges unattended — all four conditions hold simultaneously
```

```gherkin
Given exactly one of the four conditions holds — `level` is `autonomous`, or
  every path matches an active category, or CI is green, or a clean verdict is
  on the record — and the other three do not
When gate 3 is evaluated
Then the change does not merge unattended; any one condition is necessary but
  none is sufficient alone
```

```gherkin
Given `settings.autonomy.level` is `guided` or `assisted`
When gate 3 is evaluated
Then the human merges, whatever the other three conditions say — a level below
  `autonomous` does not open gate 3, on its own
```

```gherkin
Given `settings.autonomy.auto_merge` is `[]` — its current default in this
  repository
When gate 3 is evaluated
Then nothing merges unattended, whatever the other three conditions say — the
  default has no named category to match the file set against
```

### AC-11 — A label that under-states the diff does not shrink the review, and the gap is signalled durably

```gherkin
Given a ticket labelled `scope/S` whose diff touches `features/business/**` and
  changes no rule — so `scope/S` is the correct label
When gate 2 runs
Then the business role reviews it, alongside tech, because the diff routes the
  review and the label does not
```

```gherkin
Given a ticket labelled `scope/S` whose diff changes a rule another feature or
  another app consumes — so the axis's own second question answers yes and the
  label should have been `scope/L`
When gate 2 runs
Then the gap between the label and the diff is reported as a scoping signal per
  ADR-0015, addressed to the manager, and recorded against the work item so the
  retrospective's trigger can read it afterwards
```

```gherkin
Given the same ticket, and a run that reports the signal only inside itself — spoken
  to no one and written down nowhere that outlives the run
When the run ends, whether or not it got as far as proposing its change
Then this criterion fails: the signal is owed to a named recipient and owed durably,
  and a gap nobody can read afterwards is the gap that was never reported
```

```gherkin
Given a ticket labelled `scope/M` whose diff touches `features/business/**`, and the
  rule it changes is consumed by nothing beyond its own feature — so the axis's own
  second question answers no
When gate 2 runs
Then the extra review still happens and the gap is not reported as a scoping
  signal — `scope/M` was the correct label, a rule having changed, and the axis's
  spec clause keeps it below `scope/L` (`features/business/execution-policy/` AC-3);
  the two grids disagreeing here is them measuring different things, not the manager
  having mislabelled
```

### AC-12 — Where a tracker feature and this one disagree on the process, this one governs

```gherkin
Given a tracker feature's spec states a code-cycle process rule that contradicts
  this feature's
When the contradiction surfaces, in refinement or in a spec review
Then this feature's rule stands and the tracker feature's is the one corrected,
  without the reader having to infer which of the two governs
```

### AC-13 — A code-cycle rule is filed on exactly one side, by the replacement test

```gherkin
Given a new rule about how code ships, being filed to a parent feature
When it is checked against the replacement test in `business.md` — restate it for a
  tracker with no PR and no board
Then it is filed here if it stays true word for word, to the tracker feature if it
  becomes meaningless, and to exactly one of the two — never to both
```

### AC-14 — A review reads a commit, never a dirty working tree

```gherkin
Given an execution that has written its implementation
When it spawns a role agent for review
Then the work is already committed on the ticket's branch, and the reviewer reads a
  commit rather than a dirty tree
```

### AC-15 — A yield that is not a review commits too

```gherkin
Given an execution that stops mid-run and hands the next move to someone else — an
  escalation, a blocked run, a wait on a human verdict
When it yields control
Then its in-flight work is already committed on the ticket's branch, so the branch it
  leaves behind carries that work rather than resolving to its base commit
```

### AC-16 — A commit carries a type, a scope, and a reference to its work item

```gherkin
Given a commit written as `feat: <subject>`, with no scope
When it is checked against this feature's commit rule
Then it is non-conforming — the scope is mandatory here even though the standard makes it
  optional, because which modules a change touches must be readable from history alone
```

```gherkin
Given a branch delivering one work item, where some of its commits reference that item
  and some do not
When the item's commits are looked up from history
Then the lookup is incomplete and the branch is non-conforming — a partial answer that
  reads as a complete one is the failure the per-commit reference exists to remove, and
  referencing every commit is redundant rather than wrong
```

### AC-17 — Rewriting history stops at the branch boundary

```gherkin
Given a correction squashed into an earlier commit with a force push
When the target is the ticket's own branch, and the executor that owns it runs the rewrite
Then it is allowed; and when the target is the default branch, or a branch another run is
  reading, it is refused — the force push would destroy work a sibling worktree already
  fetched
```

### AC-18 — A ticket at gate 2 reads as complete only with a role-signed verdict, or a stated `not_run` cause

```gherkin
Given a ticket at gate 2 whose role review ran as the role and posted its verdict on
  the ticket's issue
When the gather reads the verdict
Then the ticket is reported complete, citing the role and the verdict it signed
```

```gherkin
Given a ticket at gate 2 whose role review did not run — the role's agent type did
  not resolve, the role disclaimed, or the executor fell back to a self-applied
  review
When the gather reads the ticket
Then it reports `not_run` with the cause, never an absence that reads as approval —
  the report is incomplete without the outcome, and the outcome is not an approval
  by default
```

```gherkin
Given a ticket at gate 2 whose scope is `scope/S` and which therefore requires no
  review
When the gather reads the ticket
Then it reports `not_required` — derived from the scope label, not asserted by the
  executor
```

```gherkin
Given a ticket at gate 2 whose scope is `scope/M` or `scope/L` and whose executor
  asserts `not_required` on the record
When the gather reads the ticket
Then the record is non-compliant: `not_required` is derived from the scope label,
  never declared, and an executor cannot substitute its own judgement for the gate
```

```gherkin
Given a verdict posted on the ticket's issue that does not name the role that
  produced it — a comment whose body matches the verdict format but lacks the
  `by scrumia-*` token
When the gather reads the verdict
Then the verdict is treated as absent and the state is `not_run` — an unattributed
  verdict is not a role verdict, and the substitution path the attribution clause
  closes is the one a structured field written by the executor's return would reopen
```

```gherkin
Given a PR whose gate 2 returns a **Blocked** verdict, and the orchestrator's net
  ran on the absence of the verdict rather than on the executor's "I did not run it"
  declaration
When the verdict lands on the open PR
Then the PR stays open, the card returns to `in_progress`, and the gather flags the
  ticket; gate 3 keeps the merge regardless of where the net ran
```

The state vocabulary is `run`, `not_required`, `not_run`; `not_run` carries a cause
and is the only failure state. "Skipped" and "unreachable" are causes of `not_run`,
not states. These are cited here rather than restated; the verdict format and the
carrier are `features/business/agent-team/`'s and `features/business/github-tracking/`'s
to materialise.

### AC-13 — A commit's multi-scope form generalizes past modules, and `*` covers what isn't worth naming

```gherkin
Given a commit atomic across a `repo`-scoped file and an app-scoped file — `design/tokens.css`
  mirrored into `site/assets/tokens.css` by one commit, the change not sensibly splittable
When the commit is written
Then the scope carries both tokens comma-separated (`design(repo,site): …`) rather than being
  refused for naming two tokens outside two modules — ADR-0017 §2's comma form generalizes to
  any of the four namespaces, not modules only
```

```gherkin
Given a commit whose comma-separated scope names a module alongside an app, a feature or `repo`
When the version bump is derived
Then only the module token named bumps, at ADR-0017 §2's level and no other — the non-module
  tokens change nothing about what bumps
```

```gherkin
Given a commit that changes a module, scoped `refactor(*): …` with the module named nowhere
When it is checked against this feature's commit rule
Then it is non-conforming — `*` never stands in for a module, so a per-module bump stays
  derivable from history; the conforming form names the module alongside `*`
  (`refactor(<module>,*): …`)
```

```gherkin
Given a commit spanning more scopes than are worth naming individually — more than three
When the scope is written
Then it may use the `*` escape hatch (`refactor(*): …`), which derives no bump on its own; a
  commit that also needs a module to bump still names that module's real token alongside it
  (`refactor(specs,*): …`)
```

### AC-18 — `auto_merge` eligibility rules (value-space, not-run verdict, partial-credit, self-widening, single-definition)

**Spec note.** Each scenario below states the rule unambiguously, on the
ticket's own reading (its Scope section) — *here* "blocks the merge" /
"is not eligible" mean *the rule is stated* in this feature. The eligibility
script that makes them checkable at run time is the sibling implementation
sub-issue's job, which depends on this spec landing first. A criterion that
names gate 3's runtime outcome therefore passes in this feature when the spec
says what gate 3's input must look like, regardless of whether anything runs
gate 3 yet.

#### AC-18.1 — `auto_merge` is a list of named categories; `all` does not exist

```gherkin
Given the value space of `settings.autonomy.auto_merge` offered by this repository
When it is read
Then it is a list of named categories, never a scalar — `all`, `none` as a
  scalar, `docs-only` as a scalar, or any synonym of "everything merges" is
  not in the value space; absence of categories is expressed as an empty list,
  not as a scalar default
```

```gherkin
Given a config, skill, doc or site page offered by this repository
When its `auto_merge` setting is read
Then the value space is the list form above and nothing else offers `all` or
  any synonym of it
```

#### AC-18.2 — A `not_run` or absent verdict blocks an unattended merge

```gherkin
Given a change for which gate 2's reviewer produced no verdict — a verifier
  that did not run, errored before reporting, or simply was not triggered
When gate 3 is evaluated
Then the change does not merge unattended, by the rule that condition (4)
  requires a verdict on the record — "no verdict" reads as a refusal to
  author the fourth condition, never as a silent approval
```

#### AC-18.3 — A mixed change (one eligible path plus one ineligible) is not eligible

```gherkin
Given a change whose file set contains one path matched by an active category
  and one path not matched by any active category of `settings.autonomy.auto_merge`
When gate 3 is evaluated
Then the change is not eligible — the universal quantification over the whole
  file set admits no partial-credit reading, and one ineligible path
  disqualifies the entire change
```

#### AC-18.4 — A change touching `.scrumia/**` is never eligible, without a rule naming `auto_merge`

```gherkin
Given a change whose file set contains any path under `.scrumia/**`, including
  `settings.autonomy.auto_merge` itself and the rest of the autonomy config
When gate 3 is evaluated
Then the change is not eligible — by the universal quantification over an
  empty intersection with `.scrumia/**` in every category's allowed-path set,
  with no rule naming `.scrumia/**` or `auto_merge` specifically; the
  protection is the predicate itself, not a clause in any list
```

#### AC-18.5 — The single definition lives in `features/business/dev-flow/`

```gherkin
Given the rules an unattended merge must satisfy and the constraints any
  category list must satisfy
When a reader — human or skill — looks them up
Then they are stated once, in `features/business/dev-flow/business.md` § *Gate
  3 opens only on four cumulative conditions* and following sections; the
  category list itself lives in `.scrumia/config.yaml` (project data); the
  trace — how the verdict is read and the file list obtained on this tracker
  — lives in `features/business/github-tracking/`; downstream consumers
  (`scrumia-review`, `scrumia-init`, `scrumia-ticket`) cite this definition
  rather than restating the predicate alongside their reading of it
```

## Out of scope

- Which model executes a ticket (`scope/*` × `risk/*` → `scrumia-pick-model`) — specified
  by `features/business/execution-policy/`, not here.
- The ceremonies (retrospective, refactor session, debt audit): trigger, cadence,
  artefact, and which of the three are admitted at all — specified by
  `features/business/ceremonies/`, not here. A gate is not a ceremony: the gates above
  stay this feature's.
- The concrete artefacts the code cycle is traced through — the pull request, the
  board column, the milestone, and the spellings of a commit's reference and of the
  closing keyword. This feature owns the process; whichever feature fills the tracker
  slot (today `features/business/github-tracking/`) specifies its materialisation.
- What a commit's type and scope are *worth* — which version bump each earns, what a
  bump promises, and how long a renamed thing keeps working. Specified by
  `features/business/release-versioning/`, not here: this feature says a commit carries
  them, that one says what they buy.
