# Acceptance criteria — work item format

One scenario per case. Each scenario must be able to fail.

## Nominal

### AC-1 — The form survives a change of tracker

```gherkin
Given a project running a work-item form module and a tracker module
When the tracker module is replaced by one addressing a different tool
Then issues written after the change carry the same sections, in the same
  order, under the same headings as those written before it
And no file inside the form module was edited to make that true
```

### AC-2 — The tracker renders the form and states none of it

```gherkin
Given a project running a work-item form module
When the tracker module is read for what an issue must contain
Then it names no section, no field and no writing rule of its own
And every such statement it makes is a reference to the form module
```

### AC-3 — One rule, one responsibility, one file

```gherkin
Given a work-item form module
When its rules are read
Then each file states one rule
And a file stating two rules is reported as a defect, not accepted as a
  grouping of related material
```

### AC-4 — Readiness and executability are one judgement written once

```gherkin
Given a work-item form module supplying a judgement
When the text deciding that an issue may be started is compared with the text
  deciding that it may be executed
Then they are the same text, read from one file
```

### AC-5 — The caller chooses the severity

```gherkin
Given one issue and one verdict reporting a missing element
When refinement asks for that verdict, and execution asks for the same verdict
Then the verdict returned is identical in both cases
And refinement may decline to promote the issue while execution proceeds once
  authorised, with neither outcome coming from the form
```

### AC-6 — A gap is closed by a fix or by an authorisation, never by neither

```gherkin
Given a verdict reporting a missing element on an issue
When work on that issue goes on
Then either the missing element was supplied, or a human authorised proceeding
  without it
And the authorisation names the gap it was given for
```


### AC-7 — Readiness and doneness come from the modules, not from the form

```gherkin
Given two apps in one project whose module lists differ
When the definition of ready is composed for an issue in each app
Then the two lists differ by exactly the rules those modules contribute
And the form module carries neither list in its own files
```

## Edge cases

### AC-8 — A rule that does not apply is not read

```gherkin
Given a project that runs no testing practice module
And a contributed rule whose condition names a testing practice
When the rules for writing an issue are assembled
Then that rule is absent from what the reader receives
```

### AC-9 — A condition that cannot be answered without the rule is a defect

```gherkin
Given a contributed rule whose condition is "when relevant", or any wording
  answerable only by reading the rule itself
When the module carrying it is checked
Then that condition is reported as a defect
And the check names the rule's file
```

### AC-10 — A work item is not recomputed when a rule changes

```gherkin
Given an open issue written under a set of rules
When one of those rules changes
Then the issue's body is unchanged
And nothing marks it as out of date on its own
```

### AC-11 — With nobody to decide, the work stops instead of proceeding

```gherkin
Given a verdict reporting a missing element on an issue
And a run with no human available to answer it
When the work would otherwise go on
Then it stops and escalates
And no authorisation is inferred from the absence of an answer, from a level
  of autonomy, or from a mode set earlier
```

### AC-12 — A verdict and its answer outlive the run that produced it

```gherkin
Given a run that starts work on an issue under an authorised gap
When that run is interrupted before it produces any other artefact
Then both the verdict and the authorisation are still readable against that
  issue afterwards
And the issue can be counted among those authorised rather than fixed
```

### AC-13 — A rule conditioned on one level does not reach the other

```gherkin
Given a contributed rule whose condition names one work-item level
When the rules are assembled for a work item at the other level
Then that rule is absent from what the reader receives
And the level was read from the module that owns it, not decided by the form
```

### AC-14 — A form requiring more than a tracker can render says so

```gherkin
Given a form requiring something a title, a body and labels cannot express
When that form is read
Then it states which trackers can carry it
And a project composing it with a tracker that cannot is told at composition
  time, not on the first issue
```
