# Acceptance criteria — standard work item form

One scenario per case. Each scenario must be able to fail.

## Nominal

### AC-1 — An issue carries the five sections in order

```gherkin
Given a project running the standard work item form
When an issue is opened through it
Then it carries a title and the sections Need, Acceptance criteria,
  Definition of Done, Definition of Ready and Additional information
And they appear in that order
```

### AC-2 — Opening an issue asks for three things

```gherkin
Given a project running the standard work item form
When an issue is opened
Then whoever opens it supplies the need, the criteria and the rattachement
And neither composed section is asked of them
```

### AC-3 — The need is written as one user story

```gherkin
Given an issue being written
When its need is read
Then it names a user, a capability and an outcome in one sentence
And a need naming no beneficiary is reported as incomplete
```

### AC-4 — A criterion that cannot fail is reported

```gherkin
Given an issue whose acceptance criteria include "the experience is smooth"
When the issue is judged against this form
Then that criterion is reported as one that cannot fail
And the report names it rather than reporting the section as a whole
```

### AC-5 — The parent feature is named through the specs contract

```gherkin
Given a project whose specs module roots its features somewhere other than the
  default
When an issue names its parent feature
Then the name resolves under that project's own root
And no path from another project's layout appears in the issue
```

## Edge cases

### AC-6 — The composed sections are filled when the issue is judged ready

```gherkin
Given an issue just opened
When its body is read
Then Definition of Ready and Definition of Done are present and unanswered
And when the issue is later judged ready to start, both are resolved and
  written into the body at that moment
```

### AC-7 — A subject the project does not have produces no heading

```gherkin
Given a project running no module that contributes a security requirement
When an issue is opened and later judged ready
Then no security heading appears anywhere in it
And no section reads "N/A"
```

### AC-8 — A title stating a task is reported

```gherkin
Given an issue titled with a task rather than an outcome
When the issue is judged against this form
Then the title is reported
And the report says which of the two it read
```

### AC-9 — A derivable field is not written into the issue

```gherkin
Given an issue conforming to this form
When its body is read
Then it carries no branch name and no value a tool derives from the issue
  itself
```

### AC-10 — Two issues written by two agents match

```gherkin
Given one project running this form
When two different agents each open an issue on unrelated subjects
Then both carry the same sections under the same headings in the same order
And the difference between them is content only
```
