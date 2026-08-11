# Acceptance criteria — dev-flow

Given/When/Then, one scenario per case. These are process-level criteria: verified
by reading the ticket, its labels, `.scrumia/config.yaml` and the specs — not by
application code.

## Nominal

### AC-1 — No verifiable acceptance criterion, no execution

```gherkin
Given a ticket with no acceptance criterion that can fail
When execution starts (`scrumia-ticket` Step 0)
Then it is refused, a comment on the issue names precisely what's missing, and
  nothing is executed on a guessed intent
```

## Edge cases

### AC-2 — A business rule found missing mid-execution is escalated, not invented

```gherkin
Given an execution run that finds a business rule missing, or contradicted by
  another feature
When the contradiction surfaces
Then the run stops, comments on the issue, and calls on the business role instead
  of deciding the rule itself
```

### AC-3 — Discovery absent: the human scopes directly, and says so

```gherkin
Given the discovery slot is empty in `.scrumia/config.yaml`
When an idea needs scoping
Then the human scopes it by hand into a ticket, and the absence of a scoping pass
  is stated rather than silently improvised
```

### AC-4 — Guided autonomy adds a human check before execution starts

```gherkin
Given `settings.autonomy.level` is `guided`
When a ticket finishes scoping
Then the human validates the transition to execution before an agent starts it
```

### AC-5 — Only an explicitly widened `auto_merge` lets gate 3 go unattended

```gherkin
Given `settings.autonomy.level` is `autonomous` and `settings.autonomy.auto_merge`
  is `docs-only`
When CI is green, gate 2 raised no blocker, and the PR touches documentation only
Then the PR merges without an additional human step
```

```gherkin
Given `settings.autonomy.auto_merge` is `none` — its default
When CI is green and gate 2 raised no blocker
Then nothing merges without the human, whatever `settings.autonomy.level` says
```

### AC-6 — A label that under-states the diff does not shrink the review

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
When the PR is written
Then the gap between the label and the diff is flagged as a scoping failure per
  ADR-0015
```

```gherkin
Given a ticket labelled `scope/M` whose diff touches `features/business/**`, and the
  rule it changes is consumed by nothing beyond its own feature — so the axis's own
  second question answers no
When the PR is written
Then the extra review still happens and the gap is not reported as a scoping
  failure — `scope/M` was the correct label, a rule having changed, and the axis's
  spec clause keeps it below `scope/L` (`features/business/execution-policy/` AC-3);
  the two grids disagreeing here is them measuring different things, not the manager
  having mislabelled
```

### AC-7 — Where a tracker feature and this one disagree on the process, this one governs

```gherkin
Given a tracker feature's spec states a code-cycle process rule that contradicts
  this feature's
When the contradiction surfaces, in refinement or in a spec review
Then this feature's rule stands and the tracker feature's is the one corrected,
  without the reader having to infer which of the two governs
```

### AC-8 — A code-cycle rule is filed on exactly one side, by the replacement test

```gherkin
Given a new rule about how code ships, being filed to a parent feature
When it is checked against the replacement test in `business.md` — restate it for a
  tracker with no PR and no board
Then it is filed here if it stays true word for word, to the tracker feature if it
  becomes meaningless, and to exactly one of the two — never to both
```

### AC-9 — A review reads a commit, never a dirty working tree

```gherkin
Given an execution that has written its implementation
When it spawns a role agent for review
Then the work is already committed on the ticket's branch, and the reviewer reads a
  commit rather than a dirty tree
```

### AC-10 — A yield that is not a review commits too

```gherkin
Given an execution that stops mid-run and hands the next move to someone else — an
  escalation, a blocked run, a wait on a human verdict
When it yields control
Then its in-flight work is already committed on the ticket's branch, so the branch it
  leaves behind carries that work rather than resolving to its base commit
```

### AC-11 — A commit carries a type, a scope, and a reference to its work item

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

### AC-12 — Rewriting history stops at the branch boundary

```gherkin
Given a correction squashed into an earlier commit with a force push
When the target is the ticket's own branch, and the executor that owns it runs the rewrite
Then it is allowed; and when the target is the default branch, or a branch another run is
  reading, it is refused — the force push would destroy work a sibling worktree already
  fetched
```

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

## Out of scope

- Which model executes a ticket (`scope/*` × `risk/*` → `pick-model.sh`) — specified
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
