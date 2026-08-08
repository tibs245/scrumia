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

### AC-2 — A rubric that doesn't apply produces no file

```gherkin
Given a feature whose rubric does not apply
When the feature is written
Then no file exists for that rubric — not a file saying "N/A"
```

### AC-3 — `index.md` exists before anything else does

```gherkin
Given a feature just started, with no business rule and no scenario written yet
When the feature is written
Then `index.md` exists regardless, because it is the entry point the format
  requires unconditionally
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

## Out of scope

- The numeric splitting guardrails (`business.md` around 200 lines, `qa.md`
  around 12 scenarios) belong to the feature-splitting criterion
  (ADR-0004) — this feature specifies the catalogue and the two strata, not
  when a feature should become two.
- Automated enforcement (a linter that deletes an empty file, or that flags a
  duplicated rule) is a tooling concern for whichever App feature implements
  it — not a guarantee this Business feature makes on its own.
