# Contrast ratios meet WCAG 2.1 AA

*Refusal.* A text-on-background pair below 4.5:1 (body) or 3:1 (large) is
refused. The numbers are WCAG 2.1, not aesthetic judgement.

## What is the threshold

| Pair | Minimum ratio | Notes |
|---|---|---|
| Body text on its background | **4.5 : 1** | WCAG 1.4.3, "normal text" |
| Large text on its background | **3 : 1** | WCAG 1.4.3, "large text" — 18pt regular or 14pt bold (≈24sp regular / ≈18.66sp bold) |
| Non-text UI components (icon-only buttons, focus indicators) | **3 : 1** | WCAG 1.4.11 |
| Logotypes (brand text treated as a logotype) | **none** | WCAG 1.4.3 exception |

"Body text" is anything not in the large-text row — captions, helper text, list
rows, paragraph text. "Large text" is 18pt regular or 14pt bold and above.
The unit conversion matters: a 16sp body and a 22sp headline, both regular,
land in different rows — the body fails below 4.5:1, the headline fails below
3:1.

## What is refused

A text-on-background pair below the threshold. The threshold is computed
against the **rendered** colour pair, not the design system's nominal colour
pair — a `colorScheme.onSurface` rendered against a dynamic-color-derived
`colorScheme.surface` is the pair that matters, and that pair is what the
audit measures:

```kotlin
// ❌ a Text composable with a color that fails against its background
Text(
    text = "Submit",
    color = Color(0xFFCCCCCC),          // hardcoded — see tokens-from-material3
    modifier = Modifier
        .background(Color(0xFFEEEEEE)) // hardcoded background
        .padding(16.dp),
)

// ✓ a Text composable reading from MaterialTheme.colorScheme — and the pair
//   it produces against the dynamic-color surface is what dynamic color
//   guarantees to be at or above WCAG AA
Text(
    text = "Submit",
    color = MaterialTheme.colorScheme.onSurface,
    style = MaterialTheme.typography.bodyMedium,
)
```

A `MaterialTheme.colorScheme.onSurface` against `MaterialTheme.colorScheme.surface`
is the Material 3 contract: the dynamic palette is generated against WCAG AA,
the default light and dark palettes are checked against it, and a project's
static override is held to the same numbers by this rule.

## What is measured

The contrast ratio is `(L1 + 0.05) / (L2 + 0.05)`, where `L1` is the relative
luminance of the lighter colour and `L2` of the darker. The audit reads the
rendered pair from the screen, not the named tokens from the source — a
`onSurface` token whose dynamic derivation produces a 3.8:1 pair against the
current wallpaper is a finding, even though the source names a pair that
*should* pass.

## Why

4.5:1 body / 3:1 large is the WCAG 2.1 Level AA threshold, and AA is the
floor Material 3 commits to in its generated palettes. A project that holds
UI to a lower standard than the design system generates is opting out of the
accessibility work the platform already did, and the next accessibility audit
will land with no record of the choice.

## What it pairs with

- [`tokens-from-material3`](tokens-from-material3.md) — the tokens come from
  `MaterialTheme.colorScheme`, and the contrast is the test those tokens pass.
- [`touch-target-size`](touch-target-size.md) — touch target and contrast are
  the two halves of WCAG 2.1 Level AA.
- [`dynamic-color`](dynamic-color.md) — the dynamic palette is generated
  against these numbers; a static override is held to them by this rule.

## Sources complémentaires

- [`https://www.w3.org/WAI/WCAG21/Understanding/contrast-minimum.html`](https://www.w3.org/WAI/WCAG21/Understanding/contrast-minimum.html) — WCAG 2.1, 1.4.3 contrast minimum. The 4.5:1 and 3:1 numbers.
- [`https://www.w3.org/WAI/WCAG21/Understanding/non-text-contrast.html`](https://www.w3.org/WAI/WCAG21/Understanding/non-text-contrast.html) — WCAG 2.1, 1.4.11 non-text contrast. The 3:1 number for UI components.
