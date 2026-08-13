# Acceptance criteria — HTML, CSS and accessibility

One scenario per rule in `business.md`. Each scenario must be able to fail.

## Refusal rules

### AC-1 — A semantic element beats an ARIA role

```gherkin
Given an interactive component implemented as `<div role="button" onClick={…}>`
When the plugin's `implement` register contribution runs against it
Then a finding names the file, the rule (`html-css-and-accessibility/BR-1`),
  and one line of what was not met — that a native `<button>` element carries
  keyboard activation and announcement for free
And the finding cites MDN's accessibility guidance as its source
```

### AC-2 — The element follows the purpose

```gherkin
Given an interactive widget styled to look like a button, implemented as `<div>`
  or `<span>` with `cursor: pointer`
When the plugin's `implement` register contribution runs against it
Then a finding names the file, the rule (`html-css-and-accessibility/BR-2`),
  and one line of what was not met — that the element follows the purpose
  (`<button>`, `<a>`), not the appearance
And the finding cites W3C ARIA Authoring Practices as its source
```

## Tests query what the user meets

### AC-3 — Accessibility-based selectors are advised when vitest is present

```gherkin
Given a project where vitest is installed (`vitest` in `devDependencies`) and
  at least one component test file (`*.test.tsx` or `*.test.ts`) exists
When the plugin's `implement` register contribution runs against the project
Then a directive advises the use of `getByRole`, `getByLabelText` or
  `getByText` over `data-testid` and CSS-class queries, citing WAI-ARIA's
  testing guidance
And the directive names the vitest detection condition it activated on

Given instead a project where vitest is absent, or no component test exists
When the same contribution runs
Then no such directive is contributed — the plugin's silence is its
  statement
```

## Sources and licence

### AC-4 — Each refusal cites its source, with the licence

```gherkin
Given any refusal rule the plugin ships
When the plugin's README is read
Then the rule's source URL is present, and the licence line — "MDN content is
  CC BY-SA 4.0" or "W3C documents ship under the W3C Document Licence" — is
  present beside it
And a rule without both URL and licence line is a finding
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
