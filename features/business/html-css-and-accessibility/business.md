# HTML, CSS and accessibility — business rules

## Value

For whoever ships a React or SolidJS app — a project's interfaces stay
semantic, accessible, and aligned with the W3C and MDN guidance the
contemporary web is documented against. It matters because a `<div>` that
behaves like a button is a defect no design system catches: the visual layer
passes, the assistive layer fails, and the bug ships. Not instrumented today:
nothing counts how many refusals a project triggered during implementation.

## A semantic element beats an ARIA role

When a native HTML element expresses the same intent as a `role` attribute, the
native element wins. `<button>` carries keyboard activation, focus management
and announcement for free; `<div role="button">` reimplements them, and the
reimplementation is the place the bug lives. The plugin's refusal rules cite
WAI-ARIA's "ARIA in HTML" guidance, which states the same principle for every
landmarked widget.

## The element follows the purpose

An interactive widget's element is decided by what the widget *does*, not by
how it looks. A CTA is a `<button>`. A navigation link is `<a href>`. A text
field is `<input type>` or `<textarea>`. CSS handles the appearance — the
plugin does not refuse a styled `<button>` — but it refuses a styled `<div>`
whose only justification is appearance.

## Tests query what the user meets

When vitest is present in a project and the project ships component tests,
the plugin offers a directive: prefer accessibility-based selectors
(`getByRole`, `getByLabelText`, `getByText`) over `data-testid` or CSS-class
queries. The point is not style — it is that a test querying by role catches
the same defects a screen reader would surface, and a test querying by class
catches nothing the class itself does not assert.

The directive is conditional, not unconditional: vitest absent, or no
component tests, and the directive contributes nothing. A project that does
not write component tests pays no cost for this capability.

## Sources are cited, with their licence

MDN content is CC BY-SA 4.0. W3C documents ship under the W3C Document
Licence. Both require attribution. The plugin's README names each source it
draws a refusal from, with the URL and the licence line, so a project adopting
the plugin sees what it ships under.

## What the plugin contributes

The plugin contributes refusal rules to two registers, scoped to two
implementation modules:

| Register | Module that opens it | Scope |
|---|---|---|
| `implement` | `scrumia-github-project` (via `scrumia-ticket`) | `scrumia-impl-reactjs`, `scrumia-impl-solidjs` |
| `review` | `scrumia-github-project` (via `scrumia-review`) | same |

A project that does not run either implementation module pays no cost. The
contributions appear in the directive table printed by `scrumia-extends`, and
a finding against any of them names the source it cites.

## Business rules

- **BR-1** — A semantic HTML element is preferred over an ARIA role when
  both express the same intent.
- **BR-2** — An interactive widget's element is decided by its purpose
  (`<button>`, `<a>`, `<input>`, …), not by CSS styling alone.
- **BR-3** — When vitest is present and component tests exist, accessibility-
  based selectors are advised in place of `data-testid` or class queries;
  absent either condition, the directive contributes nothing.
- **BR-4** — The plugin's README cites every source a refusal draws from,
  with the URL and the licence line, so attribution travels with the rule.
- **BR-5** — The plugin contributes to the `implement` and `review`
  registers, scoped to `scrumia-impl-reactjs` and `scrumia-impl-solidjs`.

## Vocabulary

**"Semantics"** names the contract between an element and the assistive
layer — what a screen reader announces, what keyboard activation does, what
focus management expects. **"ARIA role"** names the override that lets a
non-semantic element opt into the same contract, at the cost of carrying it
by hand. **"Compound component"** is not used here — see
`features/business/compound-components/`.
