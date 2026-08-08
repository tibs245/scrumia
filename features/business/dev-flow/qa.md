# Acceptance criteria — dev-flow

Given/When/Then, one scenario per case. These are process-level criteria: verified
by reading the ticket, its labels, and `.scrumia/config.yaml` — not by application
code.

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

## Out of scope

- Which model executes a ticket (`scope/*` × `risk/*` → `pick-model.sh`) — specified
  by `features/business/execution-policy/`, not here.
- The ceremonies (retrospective, refactor session, debt audit): trigger, cadence,
  artefact — specified by #11, not here.
