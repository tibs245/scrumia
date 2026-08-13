# Acceptance criteria — Form management

One scenario per rule in `business.md`. Each scenario must be able to fail.

## Resolver

### AC-1 — A form without a resolver is refused

```gherkin
Given a React component that calls `useForm` with no second argument, and
  no `Resolver` import in the file
When the plugin's `implement` register contribution runs against it
Then a finding names the file, the rule (`form-management/BR-1`), and one
  line of what was not met — that a form declares a resolver so validation
  is one schema, not per-field logic
And the finding cites `https://react-hook-form.com` as its source
```

## Registration, not control

### AC-2 — Inputs are registered, not controlled

```gherkin
Given a form input managed with `useState` paired with `onChange` that
  could have been a `register("name")` call
When the plugin's `implement` register contribution runs against it
Then a finding names the file, the rule (`form-management/BR-2`), and one
  line of what was not met — that the library owns registered inputs, and
  `useState` reimplements what the library already provides
And an input that genuinely needs control (a non-library-managed value)
  is not subject to this rule, the case named in the rejection
```

## State through the library

### AC-3 — Form state is read through the library's API

```gherkin
Given a form whose state is read via `document.querySelector("form")…` or
  via direct DOM access rather than `watch`, `getValues`, `formState` or
  `handleSubmit`
When the plugin's `implement` register contribution runs against it
Then a finding names the file, the rule (`form-management/BR-3`), and one
  line of what was not met — that the library's API is the source of truth
  for form state
```

## Sources and version

### AC-4 — The plugin cites the source with a version pin

```gherkin
Given the plugin's README
When it is read for the form-library citation
Then `https://react-hook-form.com` is present, and the major version the
  rules were written against is named beside it
And a citation without the version is a finding
```

## Plumbing

### AC-5 — The plugin composes and passes the marketplace gate

```gherkin
Given the plugin's tree, with its `extends.json` declaring contributions to
  `implement` and `review` scoped to `scrumia-impl-reactjs` only
When `python3 tools/validate.py` runs from the repository root
Then the gate passes, naming the plugin once in its listing
And a project running `scrumia-impl-solidjs` without `scrumia-impl-reactjs`
  pays no cost for this plugin — no directive from it appears in the
  directive table
And the plugin's entry in `site/modules.json` carries an emoji distinct
  from every other module's, and the i18n files for both `en` and `fr`
  carry the prose the marketplace page reads
```
