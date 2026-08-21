# Tokens come from Material 3

*Refusal.* A hardcoded color, typography step, shape corner, elevation or state-layer
value is refused. The token is the only declaration worth keeping in step.

## What is refused

A raw value used directly inside a Composable or a View:

```kotlin
// ❌ a raw hex color in a Composable
Text(
    text = "Hello",
    color = Color(0xFF6200EE),  // hardcoded — not in MaterialTheme
)

// ❌ a typography step outside MaterialTheme.typography
Text(
    text = "Hello",
    fontSize = 14.sp,           // hardcoded — not a Material 3 typography step
    fontWeight = FontWeight.Medium,
)

// ❌ a shape corner outside MaterialTheme.shapes
Card(
    shape = RoundedCornerShape(8.dp),  // hardcoded — not Material 3 shape
)

// ❌ an elevation outside MaterialTheme / state layers
Card(
    elevation = CardDefaults.cardElevation(defaultElevation = 6.dp),  // raw dp
)
```

The same shape on the Views side, with `ContextCompat.getColor`, `Resources.getColor`,
or `TypedValue` reaching into a raw resource:

```xml
<!-- ❌ a raw color resource -->
<color name="brand_primary">#FF6200EE</color>

<TextView
    android:layout_width="wrap_content"
    android:layout_height="wrap_content"
    android:textColor="@color/brand_primary"
    android:textSize="14sp" />
```

A `colors.xml` defining brand colors that bypass Material 3's `colorScheme` is
the failure mode on the Views side: the project owns two color systems, neither
of them refactors through the other, and the next theme change is the migration
nobody scheduled.

## What is written instead

Tokens from `MaterialTheme.*` — `colorScheme`, `Typography`, `Shapes`,
`elevation`, the state-layer system:

```kotlin
// ✓ color from MaterialTheme.colorScheme
Text(
    text = "Hello",
    color = MaterialTheme.colorScheme.primary,
)

// ✓ typography step from MaterialTheme.typography
Text(
    text = "Hello",
    style = MaterialTheme.typography.bodyMedium,
)

// ✓ shape from MaterialTheme.shapes
Card(
    shape = MaterialTheme.shapes.medium,
)

// ✓ elevation through CardDefaults (which reads MaterialTheme.elevation)
Card(
    elevation = CardDefaults.cardElevation(),
)
```

On the Views side, a `Theme.Material3.*` style — every attribute resolves through
the theme, and the color and typography resources the theme binds are the only
declarations of color and typography in the project.

## Why

Hardcoded values are the death of a design system by a thousand reasonable
exceptions: each one looks defensible alone, and together they are an unmaintained
parallel vocabulary that drifts the day the theme changes. Material 3's tokens
exist so that one declaration — `MaterialTheme.colorScheme.primary`,
`MaterialTheme.typography.bodyLarge`, `MaterialTheme.shapes.medium` — is the
only thing every screen reads from, and the only thing the next theme change
has to update.

## What it pairs with

- [`compose-default`](compose-default.md) — the Compose default makes
  `MaterialTheme` available at every Composable.
- [`components-from-material3`](components-from-material3.md) — components
  compose the tokens; a `Button` reads `MaterialTheme.colorScheme.primary` and
  the state-layer system for hover / focus / press.
- [`dynamic-color`](dynamic-color.md) — on Android 12+, `colorScheme` is
  derived from the user's wallpaper; the rule still holds.

## Sources complémentaires

- [`https://m3.material.io/styles/color/the-color-system/key-colors-tones`](https://m3.material.io/styles/color/the-color-system/key-colors-tones) — `colorScheme` keys (primary, secondary, tertiary, error, surface, etc.).
- [`https://m3.material.io/styles/typography/type-scale-tokens`](https://m3.material.io/styles/typography/type-scale-tokens) — typography scale (displayLarge, headlineSmall, bodyMedium, labelSmall, …).
- [`https://m3.material.io/styles/shape/shape-scale-tokens`](https://m3.material.io/styles/shape/shape-scale-tokens) — shape scale (extraSmall, small, medium, large, extraLarge).
- [`https://m3.material.io/styles/elevation/elevation-tokens`](https://m3.material.io/styles/elevation/elevation-tokens) — elevation scale.
