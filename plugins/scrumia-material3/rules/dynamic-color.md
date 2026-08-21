# Dynamic color on Android 12 and above

*Norm.* Dynamic color (Material You) is the default theming approach on Android 12
and above. A static brand palette is the explicit choice and requires a stated
justification.

## What is the default

On Android 12 (API 31) and above, the `colorScheme` is derived from the user's
wallpaper through `dynamicLightColorScheme(context)` and `dynamicDarkColorScheme(context)`:

```kotlin
// ✓ dynamic color on Android 12+; falls back to a static palette below
val dynamic = supportsDynamicColor()
val colorScheme = when {
    dynamic && isSystemInDarkTheme() -> dynamicDarkColorScheme(LocalContext.current)
    dynamic -> dynamicLightColorScheme(LocalContext.current)
    isSystemInDarkTheme() -> darkColorScheme()
    else -> lightColorScheme()
}

MaterialTheme(
    colorScheme = colorScheme,
    typography = Typography,
    shapes = Shapes,
) {
    // composables
}
```

The Material 3 components, the state layers, the typography, the shapes — all
read from `colorScheme` and follow whatever the wallpaper-derived palette says.
The user gets an app that visually belongs on their device, and the project gets
the accessibility work (contrast, luminance, color-blindness) for free because
the dynamic palette is generated against Material 3's contrast targets.

`supportsDynamicColor()` is the gate: true on Android 12+, false below. Below
that, the app uses the static `lightColorScheme()` / `darkColorScheme()` defaults,
which is the only choice the platform offers.

## What is the static palette — and when

A project brand colour overrides dynamic color only when one of the following
applies, and the PR states which one:

- **Brand book obligation.** The product has a brand book the legal or marketing
  team owns, and the wallpaper-derived palette is forbidden from shipping under
  the brand. The PR references the brand book and the owner.
- **Cross-platform visual consistency.** The same product ships on iOS with a
  static palette, and the Android side is asked to match for screenshots,
  marketing material and recognition. The PR names the iOS palette.
- **Accessibility floor above Material 3.** The project's accessibility audit
  has identified a contrast pair or a color-blind failure in dynamic palettes
  the project cannot ship. The PR names the audit and the pair.

A preference for one brand colour over another — "we like the blue better" —
is not a justification. Dynamic color is the default that holds while each
product decision is debated, and a static override is a justified exception.

## Why

Dynamic color is the answer Material 3 ships against "the user's device is
theirs, and an app that looks like it belongs there is one they keep." A
project that hardcodes a brand palette on Android 12+ opts out of that answer
without naming why, and the next time the brand asks "why does the app look
wrong on this user's phone", the question lands with no record of the choice.

## What it pairs with

- [`tokens-from-material3`](tokens-from-material3.md) — the tokens still come
  from `MaterialTheme.colorScheme`; the question is where `colorScheme` comes
  from.
- [`contrast-ratios`](contrast-ratios.md) — Material 3's dynamic palette is
  generated against the WCAG AA contrast thresholds, and a project's static
  override is held to the same numbers.

## Sources complémentaires

- [`https://m3.material.io/styles/color/dynamic-color`](https://m3.material.io/styles/color/dynamic-color) — Material You dynamic color.
- [`https://developer.android.com/develop/ui/views/theming/look-and-feel`](https://developer.android.com/develop/ui/views/theming/look-and-feel) — Android 12+ wallpaper-based theming.
