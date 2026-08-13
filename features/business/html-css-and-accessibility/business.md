# HTML, CSS and accessibility — business rules

## Value

For whoever ships a web app — the project's interfaces stay accessible and
aligned with the W3C and Mozilla guidance the contemporary web is documented
against. It matters because a `<div>` that behaves like a button is a defect
no design system catches: the visual layer passes, the assistive layer fails,
and the bug ships. Not instrumented today: nothing counts how many refusals
a project triggered during implementation.

## Sources

This module's authority is the W3C and Mozilla corpus, not opinion. Every
rule the plugin ships cites one of the five sources below; a rule without a
citation is not shipped, and a citation that 404s is rewritten against a
source that still resolves.

| Source | URL | What it provides |
|---|---|---|
| MDN — Web HTML | `https://developer.mozilla.org/fr/docs/Web/HTML` | The reference for every HTML element and attribute; the ground truth on what a `<button>` does, what `<input type>` accepts, what `<a href>` requires. |
| MDN — Learn web development / HTML Accessibility | `https://developer.mozilla.org/fr/docs/Learn_web_development/Core/Accessibility/HTML` | The pedagogical HTML-accessibility path: how to write HTML that works with assistive technology without reaching for ARIA. |
| MDN — WAI-ARIA basics | `https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Accessibility/WAI-ARIA_basics` | When ARIA *is* the answer: roles, states, properties, and the boundaries HTML sets on them. |
| W3C — HTML | `https://www.w3.org/html/` | The HTML specification itself, including the conformance requirements an element either meets or doesn't. |
| W3C — ARIA Authoring Practices Guide (APG) | `https://www.w3.org/WAI/ARIA/apg/patterns/` | Concrete UI patterns — tabs, dialogs, menus, comboboxes, listboxes — written as reference implementations with keyboard interaction, focus management, and ARIA markup included. |

Licences: MDN content is CC BY-SA 4.0; W3C documents ship under the W3C
Document Licence. Both require attribution, which travels with each rule
the plugin ships.

## The module's role

The module's business rules are statements about *what this module is and
what it does for the project that adopts it*. They are not a list of good
practices — those live in the plugin's `rules/` directory, one file per
behavioural rule, each citing one of the sources above.

- **BR-1** — The module extends the implementation modules that ship with
  ScrumIA: `scrumia-impl-reactjs` and `scrumia-impl-solidjs`. A project
  running either gains the module's accessibility directives; a project
  running neither pays no cost, and a project that adopts the module
  without either still composes — the module stands on its own.

- **BR-2** — The module can be taken directly as an implementation module
  by a project that has no React or SolidJS framework at all — a server-
  rendered app, a static site, an HTML-only prototype. The framework-
  specific scoping in `extends.json` is the *default*, not a requirement.

- **BR-3** — Every accessibility rule the module ships cites its source
  in W3C or Mozilla — never a blog post, never an opinion piece, never a
  Stack Overflow answer. A rule whose citation has rotted is rewritten
  against a source that still resolves; a rule whose source no longer
  states the principle is removed, not paraphrased.

- **BR-4** — The module helps web development carry solid notions of
  accessibility. "Solid" means durable across browser generations, derived
  from a specification, and grounded in established assistive-technology
  behaviour — not fashionable, not minimal, not framework-specific.

- **BR-5** — The module anchors accessibility in the application's DNA,
  not in a separate audit pass. Tests query components through
  accessibility-based selectors — `getByRole`, `getByLabelText`,
  `getByText` — so a test that passes catches what a screen reader would
  surface, and a test that fails catches the regression. The conditional
  directive that activates on a vitest detection is what does the
  anchoring.

- **BR-6** — The module provides patterns and solutions for the recurring
  accessibility problems a web app meets: navigation landmarks, form
  labelling, focus management, modal focus trapping, live regions, error
  messaging. Each pattern carries its source citation, its trade-offs,
  and the failure mode it prevents.

- **BR-7** — The module teaches how to design and audit features for
  accessibility — not only *what* to design. The audit skill answers
  "is this component accessible?" the way an implementation module
  answers "is this code correct?" — by refusing the shape that would
  otherwise pass. A reader of the module's docs finishes with both the
  rules and the practice of catching a violation.

## What the plugin contributes

The plugin (`scrumia-html-css`) carries refusal rules to two registers,
scoped to two implementation modules by default:

| Register | Module that opens it | Default scope |
|---|---|---|
| `implement` | `scrumia-github-project` (via `scrumia-ticket`) | `scrumia-impl-reactjs`, `scrumia-impl-solidjs` |
| `review` | `scrumia-github-project` (via `scrumia-review`) | same |

A project that does not run either implementation module — or that
overrides the scope to take the module standalone, per BR-2 — pays no cost
for the contributions it does not enable. The contributions appear in the
directive table printed by `scrumia-extends`, and a finding against any of
them names the source it cites.

## Vocabulary

**"Semantics"** names the contract between an element and the assistive
layer — what a screen reader announces, what keyboard activation does,
what focus management expects. **"ARIA role"** names the override that
lets a non-semantic element opt into the same contract, at the cost of
carrying it by hand. **"Solid"** in BR-4 means grounded in a specification
and durable across browser generations, not framework-specific. **"DNA"**
in BR-5 names the test suite: a project's accessibility culture is what
its tests assert, not what its docs claim.
