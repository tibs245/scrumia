---
name: html-css-audit
description: Audits a web app against the HTML, CSS and accessibility rules — semantic elements over ARIA roles, the element follows the purpose, and tests query what the user meets. Use it before merging a feature that touches rendering or component tests, or when a screen reads correctly but behaves wrongly for assistive technology.
---

# Auditing HTML, CSS and accessibility

Three refusal rules, each catching a defect the visual layer cannot see. A `<div>` styled to look like a button passes every design review; the screen-reader journey is the failed layer. The audit walks the source tree, names the rule each finding breaks, and cites the source the rule is derived from.

## Step 1 — Establish the rules

Read the plugin's three rules, each in `rules/<name>.md`:

- `semantic-over-aria.md` — a `<div role="button">` (or any non-semantic element carrying a role that names a behaviour a native element already implements) fails.
- `element-follows-purpose.md` — a `<div>` or `<span>` styled as a button, link, or other native control, with no native semantics, fails.
- `tests-query-by-role.md` — when vitest is present, a component test that queries through `data-testid` or a CSS-class selector rather than `getByRole` / `getByLabelText` / `getByText` fails.

When `tests-query-by-role` is in scope, the run starts with the plugin's `bin/detect-vitest.sh`. If the detector returns 1, the rule is out of scope for this audit and the report says so.

## Step 2 — Sweep, then look

Three cheap entry points first:

- Non-semantic elements with `role="button"`, `role="link"`, `role="checkbox"` or any role a native element already implements.
- `<div>` or `<span>` with `cursor: pointer` and an `onClick` (or click handler) but no `role` and no native semantics.
- `*.test.ts(x)` files containing `getByTestId`, `container.querySelector`, or `findByClass*` (the shapes that reach the same target an accessibility selector would have reached).

Then a targeted pass over what those three designated, and a check that the conditional detector's answer matched the project's actual test setup.

## Step 3 — The report

Each finding names:

- the file and line,
- the rule and its identifier (`html-css-and-accessibility/BR-1`, `BR-2`, `BR-3`),
- one line of what was not met,
- the source URL the rule cites, with its licence line.

A finding without a source citation is a finding against the plugin, not the project — the rule's own citation has rotted and the audit reports it as such.

## Step 4 — Accessibility, separately

These are not refusal rules and not opinions: contrast, visible focus, `prefers-reduced-motion`, target sizes, label association. Tests fail or they pass, with the measured ratio and the pair. List them apart, distinct from the three refusals.
