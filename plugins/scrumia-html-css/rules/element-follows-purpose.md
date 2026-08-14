Element follows the purpose

*Refusal.* A non-semantic or mismatched element presented as a native control — styled to look like it, not built from it.

## What is refused

A `<div>` or `<span>` styled like a button, with no `role` attribute, no native semantics, and no keyboard contract. Transcribed from MDN's [HTML Accessibility guide](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Accessibility/HTML):

```html
❌ <div>Play video</div>
```

A `<div>` styled like a button is not a button — it is a non-interactive element that mimics one. Removing the styling leaves a generic flow container; removing the class leaves a screen-reader announcement of "Play video, group".

The same trap reaches links. From MDN's [`<a>` reference](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/a):

> "Anchor elements are often abused as fake buttons by setting their `href` to `#` or `javascript:void(0)` to prevent the page from refreshing, then listening for their `click` events. These bogus `href` values cause unexpected behavior when copying/dragging links, opening links in a new tab/window, bookmarking, or when JavaScript is loading, errors, or is disabled. […] Use a `<button>` instead. In general, **you should only use a hyperlink for navigation to a real URL**."

```html
❌ <a href="#" onClick="submit()">Save</a>
```

The third shape is the region trap. A region whose name is a heading is named by wiring the heading to a `div` through `aria-labelledby` instead of using the element that already takes a heading as its accessible name.

```html
❌ <div role="region" aria-labelledby="filters-title">
  <h2 id="filters-title">Filters</h2>
  …
</div>
```

## What is written instead

The element whose contract matches the action. From MDN's [HTML Accessibility guide](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Accessibility/HTML), the same "Play video" content as a button:

```html
<button type="button">Play video</button>
```

For navigation, the `<a>` element with a real `href`:

```html
<a href="/save">Save</a>
```

For a region whose name is a heading, the native sectioning element with the heading as a child. From MDN's [`<section>` reference](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/section), the implicit ARIA role is `region` whenever the element has an accessible name — and a heading child provides that name implicitly:

```html
<section>
  <h2>Filters</h2>
  …
</section>
```

No `aria-labelledby`. No id reference. The `<section>` and the heading live in the same node; the role and the accessible name follow.

## Why

Each native element exposes a contract: keyboard interaction, focus behaviour, screen-reader announcement. Removing the element removes the contract. A `<div>` styled like a button is invisible to a screen reader's interactive-element search and unreachable by Tab; an `<a>` without `href` is announced as text, not as a link. Reaching for the generic element to inherit its appearance is reaching for the wrong element — the appearance and the contract are not separable.

For regions, the native sectioning element + heading pattern is the path that does not need maintenance. The `<section>` reference states:

> "Each `<section>` should be **identified, typically by including a heading (h1–h6) as a child**, wherever possible. Headings benefit: All readers; Users of assistive technologies like screen readers; SEO."

Wiring `aria-labelledby` works, but it forces the author to keep the id reference in sync with the heading, keep the referenced element in the DOM, and reason about what happens when the heading is removed, moved, or translated. The native sectioning element exposes the same accessible name through its own heading child, so the name survives copy edits, partial renders, and translations with no extra wiring — assistive technology, search engines, in-page anchors, CSS, and selectors all read the same name from the same source.

## Sources complémentaires

- MDN — Learn web development / [HTML Accessibility](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Accessibility/HTML) — version pin: HTML living standard; WAI-ARIA 1.2. Licence: CC BY-SA 4.0.
- MDN — HTML [`<a>` element](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/a) — version pin: HTML living standard; WAI-ARIA 1.2. Licence: CC BY-SA 4.0.
- MDN — HTML [`<button>` element](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/button) — version pin: HTML living standard; WAI-ARIA 1.2. Licence: CC BY-SA 4.0.
- MDN — HTML [`<section>` element](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/section) — version pin: HTML living standard; WAI-ARIA 1.2. Licence: CC BY-SA 4.0.
- MDN — [`aria-labelledby`](https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-labelledby) — version pin: HTML living standard; WAI-ARIA 1.2. Licence: CC BY-SA 4.0.
- W3C WAI — [ARIA Authoring Practices Guide / Button pattern](https://www.w3.org/WAI/ARIA/apg/patterns/button/) — version pin: WAI-ARIA 1.2. Licence: W3C Document Licence.
