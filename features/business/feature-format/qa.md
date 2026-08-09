# Acceptance criteria — feature format

One scenario per case. Each scenario must be able to fail.

## Nominal

### AC-1 — A file is created because it has content

```gherkin
Given a feature being written, and a catalogue file for which the author has
  something concrete to say
When the feature is written
Then that file exists and carries that content
```

## Edge cases

### AC-2 — An optional rubric that doesn't apply produces no file

```gherkin
Given a feature whose optional rubric does not apply
When the feature is written
Then no file exists for that rubric — not a file saying "N/A"
```

### AC-3 — The mandatory files exist whatever the feature has to say

```gherkin
Given a feature with no legal, cross-app, interface or technical rubric that
  applies to it
When the feature is written
Then the files the plugged specs module declares mandatory exist regardless —
  for `scrumia-specs`: `index.md`, `qa.md` and `CHANGELOG.md`
And an audit of that feature reports any one of them missing as a defect,
  never as the assertion "nothing to say"
```

### AC-4 — An App feature references its Business parent instead of duplicating it

```gherkin
Given a business rule already stated in a Business feature's `business.md`
When an App feature implementing it is written
Then that App feature's `business.md` references the Business parent and
  records only what is specific to this app, and the rule's wording is not
  copied
```

### AC-5 — An App feature never spans two apps

```gherkin
Given a Business feature implemented by more than one app
When the App layer is written
Then each app gets its own App feature directory, and no single App feature
  covers two apps
```

### AC-6 — A changelog entry carries no reasoning

```gherkin
Given a notable change to a feature
When the entry is added to `CHANGELOG.md`
Then the entry states the date, a one-line title, the issue, the PR, and
  whether it is breaking — and nothing that explains why the change was made
```

### AC-7 — `archi.md` exists only in the Business EPIC, and only while it lives

```gherkin
Given an EPIC whose implementation touches two or more apps
When the cross-cutting view of how those apps talk to each other is written
Then it is written as `archi.md` inside that Business feature, not inside an
  App feature and not outside `features/`
And when that same view describes a decision meant to outlive the EPIC
Then it is written as an ADR under `docs/adr/` instead of into `archi.md`
```

### AC-8 — The mandatory set is read from the plugged module, never assumed

```gherkin
Given a consumer that needs to know which files a feature must carry
When it resolves that set
Then it reads the declaration of the module filling the `specs` slot, rather
  than treating `scrumia-specs`'s three as a property of the format
And it does not infer the set from `CLAUDE.md`'s `## Specs contract` block,
  which names the module's files without marking any of them required
```

## Out of scope

- The numeric splitting guardrails (`business.md` around 200 lines, `qa.md`
  around 12 scenarios) belong to the feature-splitting criterion
  (ADR-0004) — this feature specifies the catalogue and the two strata, not
  when a feature should become two.
- Automated enforcement (a linter that deletes an empty file, or that flags a
  duplicated rule) is a tooling concern for whichever App feature implements
  it — not a guarantee this Business feature makes on its own.
