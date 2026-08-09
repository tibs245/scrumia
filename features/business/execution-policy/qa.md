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
When the execution policy reads it for capability and the manager's entry routing reads
  it for who is asked while the ticket runs
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

### AC-17 — Both kinds of deviation land in the same record, which says which kind it is

```gherkin
Given one ticket whose model a human overrode, and another whose split the executor
  refused as indivisible
When a later reader asks, of either, whether it ran the way the policy preferred and why
  not
Then both answers are found in the same venue, each record naming its kind — a second
  venue for either kind fails this, and so does one venue that cannot tell the two apart
```

### AC-18 — Deviations on one cell are countable by query, not by re-reading tickets

```gherkin
Given several tickets that deviated on the same scope × risk cell
When someone asks how often that cell was deviated from, and in which direction
Then the records are queried on the cell they name and returned together; a record that
  can only be found one ticket at a time fails this, whether or not each entry is complete
```

Nothing is required to raise this on its own. Automatic surfacing is explicitly not owed
here — a human running the query is what this criterion asks for. Who runs it and when is
#167's, per `business.md` § *Reading the record is a human's job*.

### AC-19 — The record is written, never read back to choose a model

```gherkin
Given a cell whose recorded deviations all lean the same way
When the execution policy is asked which model runs the next ticket on that cell
Then it answers what the cell says, unchanged — the history is evidence for editing the
  grid, and a caller that consults past deviations to pick a model is running a second
  policy, which AC-2 already forbids
```

### AC-20 — An agent's unilateral departure is not recorded as an override

```gherkin
Given a run that used a model the policy did not name, and that no human chose
When it is recorded
Then it is not filed as a human override — the override kind names the human whose
  decision it was, and a departure nobody decided is not counted among the deviations the
  grid is judged by
```

Only the negative half is a criterion. What *should* happen to such a run — who is told,
and in what shape — is not specified here, because nothing today can tell an agent's
unilateral departure from a human's override in the first place: both arrive as the same
comment. Attribution that a machine can check is #42's, and until it lands this criterion
guards the vocabulary rather than the behaviour.

## Out of scope

- Who reads the accumulated records, and on what occasion. This feature requires that
  repetition be countable (AC-18) and states that counting it is a human's job; the reader
  and the moment are #167's.
- The grid's cells, the capability order they climb, and the ceiling they stop below:
  project data, declared in `.scrumia/config.yaml` under `settings.team.execution`,
  beside each other. Restating any of them here would create the second statement AC-2
  exists to prevent.
- The mechanics of the script that enacts this policy — its flags, its output shape,
  how it detects a broken grid. It implements these criteria; it is not specified by
  them.
- Which concrete artefact the durable record is. This feature requires one venue for both
  kinds, fielded and queryable by cell; which artefact that becomes —
  an issue comment, a row in a file — is the tracker feature's, and
  `features/business/github-tracking/` states it for GitHub.
- Which model a *role* runs as, as opposed to which model runs a *ticket*: that lives
  in the role's own agent frontmatter, per `features/business/agent-team/`.
