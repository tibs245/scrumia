# Contrast left incomplete is contrast not measured

*Refusal.* An audit that reports contrast as passing while the automated measure left text unresolved because its background is a gradient or an image.

## What is refused

A contrast tool that cannot determine the colour behind a piece of text does not report it as a violation: it sets it aside. axe-core's `color-contrast` check files such text under `incomplete`, with the message key `bgGradient` ("background color could not be determined due to a background gradient") or `bgImage` (the same, for a background image). Those results are not passes. The text in them has not been measured.

```text
❌ color-contrast: 0 violations   (73 incomplete, bgGradient)  →  "contrast: pass"
```

An audit that reports "0 violations" while such cases remain unresolved has not measured contrast, whatever the summary line says. The count of violations covers only what the tool could compute; on a page whose floor is a gradient, that can be almost nothing.

## What is written instead

Each unresolved case is recomputed by hand and reported like any other measure, as Step 4 of `html-css-audit` asks: the measured ratio and the pair.

- **The background to measure against is the lightest colour actually painted behind the text** when the text is light, the darkest when it is dark — the point of lowest contrast. For a gradient, read its stops and composite each one with every translucent background layered above it (an overlay, a tinted card, an `rgba` panel) before computing; a stop never seen bare is not the colour behind the text. For an image, sample the region the text actually covers.
- **The threshold is 4.5:1, or 3:1 for large text** — at least 18pt (about 24px), or 14pt bold (about 18.5px). The ratio is a threshold and is not rounded: 4.49:1 fails.
- **The report names the pair and the ratio**, for instance `#e8e2d4 on #5a5f78 (lightest stop, under its overlay) — 4.86:1`, and says the case came from the tool's `incomplete` list, so a reader can tell a computed result from a recomputed one.

A case that cannot be recomputed — a photograph behind text with no region that stays above the threshold — is reported as a failure, not left out.

## Why

WCAG 2.2's success criterion 1.4.3 measures text against the background "over which the text is rendered in normal usage", and lists background images that do not give sufficient contrast with the text above them as a failure of the criterion (F83). A tool that cannot resolve that background has answered nothing about it. Counting its silence as a pass reports a measure no one took, on exactly the surfaces — hero sections, gradient floors, text over photographs — where contrast is most likely to fail.

## Sources complémentaires

- W3C — [Understanding SC 1.4.3: Contrast (Minimum)](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html) — version pin: WCAG 2.2. Licence: W3C Document Licence.
- MDN — [Color contrast](https://developer.mozilla.org/en-US/docs/Web/Accessibility/Guides/Understanding_WCAG/Perceivable/Color_contrast) — the ratios and the large-text definition. Licence: CC BY-SA 4.0.
- axe-core — [`locales/_template.json`](https://github.com/dequelabs/axe-core/blob/develop/locales/_template.json), the `color-contrast` check's `incomplete` messages — the tool's vocabulary, not the rule's authority. Licence: MPL-2.0.
