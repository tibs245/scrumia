# scrumia-html-css

The HTML, CSS and accessibility capability — semantic elements over ARIA roles, the element follows the purpose, and tests query what the user meets. Plugs in app by app, scoped to React and SolidJS by default; a project running neither, or one that opts to take the module standalone, pays no cost for the contributions it does not enable.

## What it answers

A web app that ships with this module asks the same question the same way on every component: did the developer reach for the native element, or did they style their way around it? Did the test pass through the layer an assistive technology would use, or did it reach the implementation detail? The audit skill measures the gap rather than asserting it.

## What it refuses

- **Semantic element over ARIA role** — `<div role="button">` (or any non-semantic element with a role that names a behaviour a native element already implements) fails. A native `<button>` carries keyboard activation, focus and announcement for free.
- **Element follows the purpose** — a `<div>` or `<span>` styled to look like a button, with `cursor: pointer` and an `onClick`, fails. The element must match the purpose, not the appearance.
- **Tests query by accessibility role** — when vitest is present, a component test that queries through `data-testid` or a CSS-class selector fails. The accessibility-based selector is the default; the implementation-detail selector is the exception, and is commented to say why.

Each rule is a short file under `rules/`: one paragraph, the source URL, the licence line.

## What it ships

| Skill | Role |
|---|---|
| `html-css-audit` | The audit against the three rules above. Reports; rewrites nothing without agreement. |

The vitest detection is a shell script the plugin publishes under `bin/` (`bin/detect-vitest.sh`); the conditional directive `tests-query-by-role` activates on zero and otherwise contributes nothing.

## Sources

The plugin's authority is the W3C and Mozilla corpus, never opinion. Each rule cites one source; the licence travels with the citation.

| Source | URL | Licence |
|---|---|---|
| MDN — Web HTML | `https://developer.mozilla.org/en-US/docs/Web/HTML` | MDN content is CC BY-SA 4.0 |
| MDN — Learn web development / HTML Accessibility | `https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Accessibility/HTML` | MDN content is CC BY-SA 4.0 |
| MDN — WAI-ARIA basics | `https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Accessibility/WAI-ARIA_basics` | MDN content is CC BY-SA 4.0 |
| W3C — HTML | `https://www.w3.org/html/` | W3C documents ship under the W3C Document Licence |
| W3C — ARIA Authoring Practices Guide (APG) | `https://www.w3.org/WAI/ARIA/apg/patterns/` | W3C documents ship under the W3C Document Licence |

A rule whose source URL has rotted is a finding against the plugin, not the project. The fix is to rewrite the rule's principle against a source that still resolves — not to remove the rule, which would leave the contribution without a citation.

## Settings it reads

None — the module is configuration-free. The vitest detection is a runtime check, not a setting, and the conditional directive's silence is its answer when the detector returns false.

## What it expects to find

An app that extends this module; within it, the JSX/TSX files are what the rules apply to. A project that does not run either React or SolidJS — a server-rendered app, a static site, an HTML-only prototype — takes the module standalone and the rules apply to the rendered HTML and CSS, regardless of framework.

## Decisions

Three, `BR-1` through `BR-3` — one per refusal above, for a reviewer who wants the reasoning rather than just the rule. They live in `features/business/html-css-and-accessibility/business.md`, not in the plugin.
