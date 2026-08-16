Tests query by accessibility role

*Refusal.* A component test that queries the component through an implementation-detail selector when an accessibility-based selector would have reached the same target.

*Activation.* This directive is conditional. The plugin's `bin/detect-vitest.sh` returns true when `vitest` is in the project's `devDependencies` and at least one `*.test.ts(x)` file exists in the source tree. When the detector returns false, this directive contributes nothing — silence is the plugin's statement.

## What is refused

A test that locates a control through the implementation rather than the interface.

```tsx
❌ const button = container.querySelector('[data-testid="save"]');
```

```tsx
❌ const button = container.querySelector('.save-button');
```

A test that passes by `data-testid` proves nothing about the user experience. A test that passes by class name proves nothing about the assistive layer.

## What is written instead

A test that locates the control the way a screen-reader user does — by role and accessible name. The shape comes from Testing Library's [Queries / ByRole](https://testing-library.com/docs/queries/byrole) reference:

```tsx
const button = screen.getByRole('button', { name: /save/i });
```

```tsx
const search = screen.getByRole('searchbox', { name: /search/i });
```

`getByRole` is the preferred query because it most closely resembles the user experience: a button is reached as "the button labelled Save", not as "the element with class save-button".

## Why

The same test, written two ways, catches two different regressions. A test through `data-testid` will keep passing while the button loses its accessible name, while focus becomes unreachable, while the role is removed. A test through `getByRole` fails in all three cases, because it queries the same path an assistive technology queries. From Testing Library:

> "`getByRole` is the most preferred query to use as it most closely resembles the user experience."

The cost is a slightly slower query (the role calculation walks the accessibility tree, which is more expensive than a CSS selector on large DOMs). The gain is that the test reflects the contract the component owes its users: the test cannot pass while the assistive layer cannot find the control.

## Sources complémentaires

- Testing Library — [Queries / ByRole](https://testing-library.com/docs/queries/byrole) — version pin: HTML living standard; WAI-ARIA 1.2. Licence: MIT.
- MDN — Learn web development / [WAI-ARIA basics](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Accessibility/WAI-ARIA_basics) — version pin: HTML living standard; WAI-ARIA 1.2. Licence: CC BY-SA 4.0.
- MDN — ARIA [`button` role](https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/button_role) — version pin: HTML living standard; WAI-ARIA 1.2. Licence: CC BY-SA 4.0.
