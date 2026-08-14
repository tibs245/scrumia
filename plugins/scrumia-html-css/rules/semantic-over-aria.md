Semantic element over ARIA role

*Refusal.* A non-semantic element with a `role` attribute that names a behaviour a native HTML element already implements.

## What is refused

A `<div>` or `<span>` with a `role` attribute that names a control the native element already exposes. Transcribed from MDN's [`button` role reference](https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/button_role):

```html
❌ <div id="saveChanges" tabindex="0" role="button" aria-pressed="false">Save</div>
```

The same page gives a working pair — a `<span role="button">` with `tabindex="0"` and a key handler that gates on `Enter` or `Space`. Each piece exists only because the native element was bypassed.

## What is written instead

The native element whose contract matches the action. From MDN's [`<button>` element reference](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/button), the implicit ARIA role is `button` and the element is interactive content — no `tabindex`, no manual key handler, no override needed.

```html
<button type="button" id="saveChanges" aria-pressed="false">Save</button>
```

The `type="button"` prevents the implicit submit that would otherwise reload the page — the same pitfall the `<button>` reference calls out in its Notes section. The `aria-pressed` survives because toggle state is what ARIA is for: the native element carries the role and the keyboard contract, the attribute carries the *state* the native element cannot express on its own.

## Why

A native `<button>` exposes focus, keyboard activation (Enter *and* Space), click handling, and an implicit ARIA role to assistive technology without any of them being authored. A `<div role="button">` exposes only the role: focus has to be added with `tabindex="0"`, the click handler responds to the mouse only, and keyboard activation requires a separate key handler that triggers on `Enter` or `Space`. The ARIA reference is explicit:

> "Adding `role="button"` tells the screen reader the element is a button, but does not provide other typical button functionality such as click events and keyboard handling. You can add these yourself, but you should generally use `<button>` or `<input>` with `type="button"` instead."

Skipping any one of the pieces the author must add by hand leaves a control a sighted-mouse-only user can reach but a keyboard or screen-reader user cannot. The native element removes the failure mode by removing the build list.

## Sources complémentaires

- MDN — ARIA [`button` role](https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/button_role) — version pin: HTML living standard; WAI-ARIA 1.2. Licence: CC BY-SA 4.0.
- MDN — HTML [`<button>` element](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/button) — version pin: HTML living standard; WAI-ARIA 1.2. Licence: CC BY-SA 4.0.
- MDN — Learn web development / [HTML Accessibility](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Accessibility/HTML) — version pin: HTML living standard; WAI-ARIA 1.2. Licence: CC BY-SA 4.0.
- MDN — Learn web development / [WAI-ARIA basics](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Accessibility/WAI-ARIA_basics) — version pin: HTML living standard; WAI-ARIA 1.2. Licence: CC BY-SA 4.0.
