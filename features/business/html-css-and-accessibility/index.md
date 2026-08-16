# HTML, CSS and accessibility

**Status**: draft

## In brief

Modern HTML and CSS, with accessibility as a first-class concern, applicable to
React and SolidJS implementations. The capability names the principle — a
semantic element beats an ARIA role when both express the same intent, an
interactive widget uses the element that matches its purpose, and tests query
the component the way a screen reader does. The plugin that carries it
(`scrumia-html-css`) is one realisation; future plugins may add to the same
register without rewriting this feature.

## Links

- Implemented by: `plugins/scrumia-html-css/` — `extends.json` contributes
  refusal rules to the `implement` and `review` registers, scoped to
  `scrumia-impl-reactjs` and `scrumia-impl-solidjs`.
- Authority: MDN HTML (`https://developer.mozilla.org/fr/docs/Web/HTML`),
  MDN HTML Accessibility
  (`https://developer.mozilla.org/fr/docs/Learn_web_development/Core/Accessibility/HTML`),
  WAI-ARIA basics
  (`https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Accessibility/WAI-ARIA_basics`),
  W3C HTML (`https://www.w3.org/html/`), W3C ARIA Authoring Practices
  (`https://www.w3.org/WAI/ARIA/apg/patterns/`). Each source is cited in the
  plugin's README with its licence — MDN content is CC BY-SA 4.0, W3C
  documents ship under the W3C Document Licence.
- Defers to: `features/business/modular-composition/` for how a module
  declares its contributions and what its `extends.json` owes to compose.
- Defers to: `features/business/module-anatomy/` for the procedural check
  every plugin passes.

## Files present

| File | Read it when |
|---|---|
| `business.md` | deciding what the plugin refuses, what it requires, and which sources are authoritative |
| `qa.md` | writing or running the acceptance scenarios for the refusal rules |
| `tech.md` | tracing how the plugin contributes to the `implement` and `review` registers |
| `CHANGELOG.md` | history of changes to this spec |

No `ux.md`, `legal.md`, `security.md`: this capability carries no interface,
no personal data, and no privileged surface. The licence attribution lives in
the plugin's README, not in a feature file.
