# Acceptance criteria — Runtime validation

One scenario per rule in `business.md`. Each scenario must be able to fail.

## Schema authority

### AC-1 — A hand-written twin of an inferable type is refused

```gherkin
Given a Zod schema and a TypeScript interface that declares the same shape
  hand-written beside it
When the plugin's `implement` register contribution runs against the file
Then a finding names the file, the rule (`runtime-validation/BR-1`), and
  one line of what was not met — that the type is derived from the schema,
  not declared separately
And the finding cites the schema-library docs as its source
```

## Errors and boundaries

### AC-2 — A schema at a user-facing boundary declares error messages

```gherkin
Given a Zod schema used to parse user input (form submission, API response
  consumed by a UI) with no `errorMap` and no per-field `.message()` calls
When the plugin's `implement` register contribution runs against it
Then a finding names the file, the rule (`runtime-validation/BR-2`), and one
  line of what was not met — that errors at a user-facing boundary are
  field-targeted, not generic
And a schema used only in internal call paths is not subject to this rule
```

### AC-3 — Validation in internal call paths is refused

```gherkin
Given a function whose arguments were constructed by the same module two
  lines up, and that calls `Schema.parse` on them
When the plugin's `implement` register contribution runs against it
Then a finding names the file, the rule (`runtime-validation/BR-3`), and one
  line of what was not met — that runtime validation is at trust boundaries,
  not on internal values the type system already proved
And a function that takes its argument across a boundary (network, file,
  user input, message queue) is not subject to this rule
```

## Sources and version

### AC-4 — The plugin cites the source with a version pin

```gherkin
Given the plugin's README
When it is read for the schema-library citation
Then `https://zod.dev/llms.txt` is present, and the major version the rules
  were written against is named beside it
And a citation without the version is a finding
```

## Plumbing

### AC-5 — The plugin composes and passes the marketplace gate

```gherkin
Given the plugin's tree, with its `extends.json` declaring contributions to
  `implement` and `review` scoped to `scrumia-impl-reactjs` and
  `scrumia-impl-solidjs`
When `python3 tools/validate.py` runs from the repository root
Then the gate passes, naming the plugin once in its listing
And the plugin's entry in `site/modules.json` carries an emoji distinct from
  every other module's, and the i18n files for both `en` and `fr` carry the
  prose the marketplace page reads
```
