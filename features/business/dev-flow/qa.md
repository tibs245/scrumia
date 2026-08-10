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

### AC-11 — The criterion's own subject decides the form its coverage takes

```gherkin
Given a criterion whose subject is a judgement about a rule's wording, which no program
  decides — is it consistent with another spec, is it ambiguous
When the reviewable proposal is reviewed
Then the audit that returned a verdict on it is accepted as its coverage — the gate 2
  role review, or an executed checklist where no role owns the judgement — and no
  finding is raised for the absence of a test file
```

```gherkin
Given a criterion whose subject is a property of the project's own text that a program
  decides — a link that resolves, a file that exists, a generated file in sync
When the reviewable proposal is reviewed
Then it owes an automated check in the harness CI runs, written if none exists, and the
  deliverable carrying no code buys it no exemption
```

```gherkin
Given a criterion whose subject is executable behaviour, on a ticket that also
  delivers a spec change
When the reviewable proposal is reviewed
Then that criterion is blocked unless a test that can fail covers it, the prose half
  of the same ticket buying it no exemption
```

```gherkin
Given a criterion whose subject is executable behaviour, the project having no harness
  able to run it yet
When the reviewable proposal is reviewed
Then the criterion still owes a test and writing the harness is part of the work — the
  absence of a runner does not reclassify its subject as prose
```

```gherkin
Given a criterion whose subject no program decides exactly, and a proposal offering an
  approximate check that would pass on a case the criterion forbids
When the reviewable proposal is reviewed
Then the criterion is reported as uncovered — the approximation may ship as a warning,
  and it does not stand in for the audit or checklist the subject calls for
```

```gherkin
Given a criterion that no concrete case could contradict
When the reviewable proposal is reviewed
Then it is reported as uncovered, whichever section the proposal points at
```

### AC-12 — An execution answers for the criteria it touched, not for the whole file

```gherkin
Given a ticket that amends one criterion in its feature's acceptance file, that file
  holding nine others it does not touch
When gate 2 checks what the proposal covers
Then it checks only the ticket's own criteria and the one amended, and raises no
  finding on the nine standing criteria the ticket left alone
```

### AC-13 — The two acceptance namespaces stay two lists, each citation carrying its own

```gherkin
Given a ticket that delivers its work order and also amends its feature's acceptance
  file
When its reviewable proposal states what it delivered
Then it maps its delivery against the ticket's own criteria, cited bare, and lists the
  feature criteria it added or amended in a separate list, each cited with its file
```

```gherkin
Given a ticket carrying five acceptance criteria whose feature's acceptance file ends
  at seven
When the proposal is reviewed
Then no finding is raised on the difference in counts
```

### AC-14 — A section reference locates what satisfies a criterion; it never covers it

```gherkin
Given a proposal whose mapping answers a criterion with a section reference and nothing
  else
When the reviewable proposal is reviewed
Then the criterion is reported as uncovered: the reference says where what satisfies it
  lives, and names no act that could have come out otherwise
```

```gherkin
Given a criterion covered by an agent audit at gate 2
When the proposal writes its line in the criterion-by-criterion mapping
Then that line carries both the location of what satisfies the criterion and the form
  that checked it with its outcome, rather than either one alone
```

## Out of scope

- Which model executes a ticket (`scope/*` × `risk/*` → `pick-model.sh`) — specified
  by `features/business/execution-policy/`, not here.
- The ceremonies (retrospective, refactor session, debt audit): trigger, cadence,
  artefact — specified by #11, not here.
- The concrete artefacts the code cycle is traced through — the pull request, the
  board column, the milestone. This feature owns the process; whichever feature
  fills the tracker slot (today `features/business/github-tracking/`) specifies its
  materialisation.
