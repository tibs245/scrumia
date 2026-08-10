# Acceptance criteria — ceremonies

Given/When/Then, one scenario per case. These are process-level criteria: verified by
reading a proposal, the specs, `.scrumia/config.yaml` and the tracker — not by
application code.

## Nominal

### AC-1 — An admitted ceremony states its trigger, its input and its artefact

```gherkin
Given a ceremony admitted by this feature — the retrospective or the debt audit
When its section in `business.md` is read
Then it states what fires it (an event or a human call), what it reads that already
  exists, and what it leaves behind that outlives it — all three, not two
```

### AC-2 — An admitted ceremony states synchronous or asynchronous, with its reason

```gherkin
Given a ceremony admitted by this feature
When its section is read
Then it names async or synchronous and gives the reason for that answer, so a project
  changing the answer knows which premise it is contradicting
```

## Edge cases

### AC-3 — A candidate that fires on a date alone is refused

```gherkin
Given a ceremony proposed as "every two weeks" with no recorded fact behind it
When it is checked against the three admission tests
Then it is refused on test 1, and the calendar is allowed back only as a bound on when
  it is convenient to look — never as what says there is something to look at
```

### AC-4 — A candidate producing no artefact of its own is dropped

```gherkin
Given the refactor session, whose output is a change to the code proposed as a pull
  request
When it is checked against test 3
Then it is dropped, because the pull request is the execution path's artefact and not
  the ceremony's own — and refactoring stays a ticket rather than becoming a second,
  ungated route into execution
```

### AC-5 — A retrospective with no new facts does not run

```gherkin
Given a sprint ends and no deviation, gate-2 blocker, label/diff gap, reopened ticket
  or refused split has been recorded since the last retrospective read
When the boundary is reached
Then no retrospective is held, and nobody is mobilised to confirm that nothing happened
```

### AC-6 — A retrospective that changes nothing still leaves its mark

```gherkin
Given a retrospective reads the period's records and judges that none of them warrants
  an edit
When it closes
Then it produced no grid edit, no spec change and no issue — which is a correct outcome
  and not a failed ceremony — and it still left a queryable mark of how far it read, so
  the next one can tell "read and judged harmless" from "never opened"
```

### AC-7 — The debt audit files and never fixes

```gherkin
Given a debt audit on a named area finds code worth refactoring
When it closes
Then it has filed issues carrying scope and risk labels, and has changed no code — the
  fix goes through a ticket with an acceptance criterion, like any other change
```

### AC-8 — An audit with no named area is refused before it starts

```gherkin
Given a debt audit is requested over "the project", with no area named
When the request is read
Then it is refused as unscoped, because an unbounded audit returns a list nobody
  triages, and the area is named before the audit starts
```

### AC-9 — No ceremonies module, and the answer holds against a proposal to build one

```gherkin
Given someone proposes `scrumia-ceremonies` as a module, or a `ceremonies` slot
When the proposal is checked against this feature
Then it is answered by the three reasons in `business.md` § *Where the ceremonies live*
  — no question left for a slot to ask, a module that could not degrade with an empty
  tracker slot, and slotless being reserved for modules that describe the composition
  rather than consume it — and any automation lands as one more skill in the module that
  already owns the ceremony's output
```

### AC-10 — Naming the retrospective as a reader does not close #167

```gherkin
Given `features/business/execution-policy/` leaves open who counts deviations on a cell,
  at what threshold, and whether anything surfaces the record unprompted
When this feature names the retrospective as a venue where that record is read
Then #167 stays open, because a venue is not an accountable reader and this feature sets
  no threshold — the two specs complement each other rather than one answering the other
```

## Out of scope

- The gates (`ADR-0005`) — they sit inside the execution path, on one change, and are
  specified by `features/business/dev-flow/`. A gate is not a ceremony, and counting it
  as one is what this feature's vocabulary section exists to prevent.
- What a deviation record contains and where it lives — `features/business/execution-policy/`
  and, for its venue on this tracker, `features/business/github-tracking/`. This feature
  reads that record; it does not shape it.
- Building either ceremony as a skill. The spec says which module would own each one if
  it is ever automated, and stops there.
