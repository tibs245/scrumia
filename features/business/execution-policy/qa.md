# Acceptance criteria — execution policy

Given/When/Then, one scenario per case. These are process-level criteria: verified by
reading a ticket, its labels, `.scrumia/config.yaml` and the policy's answer — not by
application code.

## Nominal

### AC-1 — The two axes are read independently

```gherkin
Given a ticket that changes one line of a payment rule, labeled scope/S risk/critical
When the execution policy is asked which model runs it
Then it answers from the S × critical cell — the risk axis is not inferred from the
  size, and a ticket small enough to look harmless does not inherit a small ticket's
  model
```

### AC-2 — A caller acts on the answer, not on the grid

```gherkin
Given a caller about to execute a labeled ticket
When it needs to know which model to run on
Then it asks the policy and acts on the instruction it answers with, and it does not
  read the matrix or re-derive the decision from the labels itself
```

## Edge cases

### AC-3 — A spec-only change nobody else consumes stays below scope/L

```gherkin
Given a ticket that edits only files under the specs root, changing a rule no other
  feature and no other app consumes
When the manager sets its scope label
Then the spec clause does not carry it to scope/L — the clause measures a rule's reach,
  not a file's location — and the label is decided on the axis's remaining questions
```

### AC-4 — A rule consumed beyond its own feature reaches scope/L

```gherkin
Given a ticket that changes a rule another feature or another app consumes — a contract,
  a shared vocabulary, an invariant enforced elsewhere
When the manager sets its scope label
Then it is scope/L on the spec clause, whether or not the change is small in lines
```

### AC-5 — Both readers of scope/* read the same test

```gherkin
Given a ticket whose scope label was set on the blast-radius test
When the execution policy reads it for capability and review routing reads it for who
  must review
Then both apply the same reading of what "a business rule changes" means, and neither
  restates the test in its own words
```

### AC-6 — An oversized cell prefers a split, and the fallback is earned

```gherkin
Given a ticket whose cell says split_or_<model>
When the executor judges the work genuinely indivisible — one migration, one contract
  that cannot ship by halves
Then it runs on the fallback the cell names, and the refusal of the split is recorded
  with its reason
```

```gherkin
Given the same ticket, but the work can be delivered as parts that each ship on their own
When the executor decides
Then it splits, and does not take the fallback — the cell states a preference, and the
  fallback is what the preference falls back to, not an alternative of equal standing
```

### AC-7 — A deviation without its reason is non-compliant

```gherkin
Given a ticket that ran on a model other than the one the policy chose — by human
  override or by refused split
When the deviation is recorded
Then the record carries what the policy chose, what actually ran, and why; a record
  missing the reason is reported as non-compliant rather than accepted as a note to
  complete later
```

### AC-8 — A ticket with no scope label is not given a guessed size

```gherkin
Given a ticket carrying no scope/* label
When the execution policy is asked which model runs it
Then it answers with the configured unlabeled default and states that the ticket
  carried no scope label, so refinement can be asked for rather than an estimate
  inherited that nobody made
```

### AC-9 — A ticket with no risk label states the risk it assumed

```gherkin
Given a ticket carrying no risk/* label
When the execution policy is asked which model runs it
Then it names the risk value it assumed in its answer, so a ticket that is in fact
  riskier can be contradicted on the spot instead of running on a silent default
```

### AC-10 — A grid with no cell for the pair reports the hole

```gherkin
Given a scope and risk pair the configured grid defines no cell for
When the execution policy is asked which model runs the ticket
Then it answers with the unlabeled default and reports the missing cell, rather than
  choosing a neighbouring cell on its own authority
```

### AC-11 — A project keeps its own labels

```gherkin
Given a project labelling its backlog size:S and risk:red, with the matching prefixes
  and aliases configured
When the execution policy reads one of its tickets
Then it resolves them to the axes' own values and answers normally — the project
  relabels nothing, and no fifth level enters the axes through a synonym
```

### AC-12 — A grid that descends as risk climbs is reported, not executed

```gherkin
Given a matrix whose cells descend along the declared capability order as risk climbs
When the policy is read
Then the inconsistency is reported rather than executed
```

### AC-13 — A split-preferring cell is not read as a descent

```gherkin
Given a grid where a row's cell names a bare model and the row above it names
  split_or_<model>
When the climbing invariant is checked
Then the pair is not reported as a descent — split_or_<model> is the fallback taken if
  the split is refused, not a placement on the capability order — and a correct grid is
  not reported as broken
```

### AC-14 — Fallbacks are still compared against fallbacks

```gherkin
Given a row of split-preferring cells whose fallback descends along the declared order
  as risk climbs
When the climbing invariant is checked
Then the row is reported as inverted, exactly as a row of bare models would be — the
  carve-out compares like with like, it does not exempt split-preferring cells from
  the invariant
```

### AC-15 — A grid with no declared capability order is reported, not assumed sound

```gherkin
Given a configuration carrying a matrix beside which no capability order is declared
When the policy is read
Then the missing declaration is reported — the invariant cannot be checked against
  nothing, and a check that silently does not run is not a grid that passed
```

### AC-16 — A cell above the declared ceiling is reported, not executed

```gherkin
Given a grid whose cell — a bare model, or the fallback a split_or_<model> cell carries
  — names a model above the ceiling declared beside the capability order
When the policy is read
Then the cell is reported rather than executed — above the ceiling is reachable only as
  a human override recorded as a deviation, never as a default a table applies
```

## Out of scope

- The grid's cells, the capability order they climb, and the ceiling they stop below:
  project data, declared in `.scrumia/config.yaml` under `settings.team.execution`,
  beside each other. Restating any of them here would create the second statement AC-2
  exists to prevent.
- The mechanics of the script that enacts this policy — its flags, its output shape,
  how it detects a broken grid. It implements these criteria; it is not specified by
  them.
- Where a deviation is durably recorded — a label, a field, a structured comment. This
  feature specifies the record's content; #32 chooses its venue.
- Which model a *role* runs as, as opposed to which model runs a *ticket*: that lives
  in the role's own agent frontmatter, per `features/business/agent-team/`.
