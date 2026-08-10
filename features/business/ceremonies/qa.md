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

### AC-5 — The drop applies to the occasion, not to the paired refactor skills

```gherkin
Given `scrumia-tdd-refactor` or `scrumia-solid-refactor` is opened on one named finding —
  from its paired audit's list, from an issue, or stated by the person opening it
When the work runs
Then it is the scoped intent this feature asks for and nothing refuses it, whatever venue
  the finding was written in — whereas the same skill opened on nothing named, at nobody's
  request, is the dropped session: a change with nothing behind it that could fail
```

### AC-6 — The sprint's gather is judged, and fails the same test

```gherkin
Given `scrumia-sprint`'s closing gather — a named occasion at a boundary, reading across
  several runs
When it is checked against test 3
Then it is not admitted as a ceremony, because everything it reports is a second copy of
  something already recorded and the gather itself survives nothing; the retrospective is
  the occasion for acting on what it surfaced
```

### AC-7 — A retrospective with no new records does not run, and the zero claims nothing

```gherkin
Given a sprint ends and the tracker holds no deviation record, gate-2 blocker, label/diff
  gap or reopened ticket since the last retrospective's mark
When the boundary is reached
Then no retrospective is held, and no one writes that the period was clean — the zero
  says nothing was recorded, which is not the same claim
```

### AC-8 — A retrospective that changes nothing still leaves its mark

```gherkin
Given a retrospective reads the period's records and judges that none of them warrants
  an edit
When it closes
Then it produced no grid edit, no spec change and no issue — which is a correct outcome
  and not a failed ceremony — and it still left a queryable mark of how far it read, so
  the next one can tell "read and judged harmless" from "never opened"
```

### AC-9 — A retrospective counts on a cell, never on a person

```gherkin
Given the deviation records the retrospective reads name the human who decided each
  override
When it looks for what to change
Then it counts repetition on a grid cell and proposes an edit to that cell — a handle
  appearing twice is not a finding, and this ceremony produces nothing about a person
```

### AC-10 — The debt audit files and never fixes

```gherkin
Given a debt audit on a named area finds code worth refactoring
When it closes
Then it has filed situated issues and has changed no code — the fix goes through a ticket
  with an acceptance criterion, like any other change
```

```gherkin
Given the audit was run through the shipped audit skills, which end at a list of findings
  in the session
When the ceremony closes
Then the findings have been filed, because a list that dies with the session is not the
  artefact that admits this ceremony — the skills enact its reading, not its filing
```

```gherkin
Given a debt audit files its findings as issues
When they reach the board
Then they carry no `scope/*` or `risk/*` label of the audit's own making — those are set
  at refinement, and an audit rating the batch it just wrote would be refining its own
  findings
```

### AC-11 — An audit with no named area is refused before it starts

```gherkin
Given a debt audit is requested over "the project", with no area named
When the request is read
Then it is refused as unscoped, because an unbounded audit returns a list nobody
  triages, and the area is named before the audit starts
```

### AC-12 — A proposal to build the module is refused on a named reason

```gherkin
Given someone proposes `scrumia-ceremonies` as a module, or a `ceremonies` slot
When the proposal is checked against this feature
Then it is refused, and the refusal names which of the three reasons in `business.md`
  § *Where the ceremonies live* it fails — a refusal that cites none of them has not
  applied this rule
```

```gherkin
Given a candidate capability whose question no existing slot asks, and which would still
  have something to do with the tracker slot empty
When it is checked against those same three reasons
Then none of them refuses it, and the answer to "module or practice" is reopened rather
  than settled by this feature's precedent
```

### AC-13 — Naming the retrospective as a venue settles none of the three open questions

```gherkin
Given `features/business/execution-policy/` leaves open who counts deviations on a cell,
  at what threshold, and whether anything surfaces the record unprompted
When this feature names the retrospective as a venue where that record is read
Then all three stay open, because a venue is not an accountable reader and this
  feature sets no threshold — it specifies only the retrospective's own timing, and
  speaks for neither of the other two candidate venues
```

## Out of scope

- The gates (`ADR-0005`) — they sit inside the execution path, on one change, and are
  specified by `features/business/dev-flow/`. A gate is not a ceremony, and counting it
  as one is what this feature's vocabulary section exists to prevent.
- What a deviation record contains and where it lives — `features/business/execution-policy/`
  and, for its venue on this tracker, `features/business/github-tracking/`. This feature
  reads that record; it does not shape it.
- The venue and shape of the retrospective's read-mark — required by BR-6, owned by
  whichever feature fills the tracker slot, and open.
- Building either ceremony as a skill. The spec says where a skill for each would land if
  it is ever written, and stops there.
