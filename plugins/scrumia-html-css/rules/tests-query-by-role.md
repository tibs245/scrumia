# Tests query by accessibility role

When vitest is present in the project, component tests query the component through what the user meets — `getByRole`, `getByLabelText`, `getByText` — not through implementation details like `data-testid` or CSS-class selectors. A test that passes by `data-testid` proves nothing about the user experience; a test that passes by `getByRole` proves the assistive layer can find the control. The same test, written two ways, catches two different regressions.

**Source:** MDN — WAI-ARIA basics (`https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Accessibility/WAI-ARIA_basics`). Licence: MDN content is CC BY-SA 4.0.

**Activation:** this directive is conditional. The plugin's `bin/detect-vitest.sh` returns true when `vitest` is in the project's `devDependencies` and at least one `*.test.ts(x)` file exists in the source tree. When the detector returns false, this directive contributes nothing — silence is the plugin's statement.

**Refusal:** a component test that queries the component through `data-testid`, a CSS class selector, or any other implementation-detail selector, when an accessibility-based selector (`getByRole`, `getByLabelText`, `getByText`) would have reached the same target. The accessibility-based selector is the default; the implementation-detail selector is the exception, and is commented to say why.
