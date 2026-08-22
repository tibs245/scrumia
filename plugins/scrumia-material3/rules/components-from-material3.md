# Components come from Material 3

*Refusal.* A Button, Card, TopAppBar, NavigationBar, ListItem, Dialog or Snackbar
built from `Box` / `Row` / `Card { ... }` primitives instead of the matching
`androidx.compose.material3.*` component is refused. Reach for the Material 3
component first.

## What is refused

A custom-built equivalent of a Material 3 component:

```kotlin
// ❌ a Button built from a Box — there is a Material 3 Button for this
@Composable
fun CustomButton(onClick: () -> Unit, label: String) {
    Box(
        modifier = Modifier
            .background(MaterialTheme.colorScheme.primary, RoundedCornerShape(8.dp))
            .clickable(onClick = onClick)
            .padding(horizontal = 16.dp, vertical = 8.dp),
    ) {
        Text(label, color = MaterialTheme.colorScheme.onPrimary)
    }
}

// ❌ a Card built from Surface — there is a Material 3 Card for this
@Composable
fun ProductCard(product: Product) {
    Surface(
        modifier = Modifier.padding(8.dp),
        color = MaterialTheme.colorScheme.surface,
        tonalElevation = 2.dp,
    ) {
        Column { Text(product.name); Text(product.price) }
    }
}

// ❌ a TopAppBar built from Row — there is a Material 3 TopAppBar for this
@Composable
fun Header(title: String) {
    Row(
        modifier = Modifier.fillMaxWidth().padding(16.dp),
        verticalAlignment = Alignment.CenterVertically,
    ) {
        Text(title, style = MaterialTheme.typography.titleLarge)
    }
}
```

The same shape on the Views side: a `Button` extended from `LinearLayout` to
add rounded corners, a `Card` built from `CardView` with hardcoded elevation, a
toolbar extended from `Toolbar` to add a navigation icon button. Each is a
re-implementation of what `com.google.android.material.button.MaterialButton`
already provides, and each is what a project discovers when the Material 3
component would have been the obvious reach.

## What is written instead

The matching Material 3 component:

```kotlin
// ✓ a Button — material3
Button(onClick = onClick) {
    Text(label)
}

// ✓ a Card — material3
Card {
    Column { Text(product.name); Text(product.price) }
}

// ✓ a TopAppBar — material3
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun Header(title: String) {
    TopAppBar(title = { Text(title) })
}
```

A project that adopts Material 3 reaches for `androidx.compose.material3.Button`,
`androidx.compose.material3.Card`, `androidx.compose.material3.TopAppBar`,
`androidx.compose.material3.NavigationBar`, `androidx.compose.material3.ListItem`,
`androidx.compose.material3.AlertDialog`, `androidx.compose.material3.Snackbar`,
and the rest of the surface. The components compose Material 3's tokens
([`tokens-from-material3`](tokens-from-material3.md)) and the state-layer system,
so a button's hover, focus and press states arrive without further work.

On the Views side: `MaterialButton`, `MaterialCardView`, `MaterialToolbar`,
`BottomNavigationView` with the Material 3 theme, `MaterialAlertDialog`,
`Snackbar` from `BaseTransientBottomBar`, all under a `Theme.Material3.*` style.

## When a custom component is the answer

Three cases, each with its own discipline:

- **A genuinely new pattern.** No Material 3 component covers the shape; the
  PR names the gap. The new component is built from Material 3 primitives
  (`Surface`, `Box`) and reads from `MaterialTheme.*`.
- **A domain composite.** A `ProductCard` that composes a `Card` with a `Row`
  of two `Text`s and an `IconButton` is the expected use of `Card`; the
  component is the project owning its shape, not the project reinventing
  `Card`.
- **A wrapper around a Material 3 component.** A `PrimaryButton` that wraps
  `Button` with project-specific copy and disabled-state defaults. The wrapper
  delegates; the wrapper does not reinvent.

A `Box { Row { Text } }` shaped like a Button is none of these, and it is the
finding.

## Why

Material 3 components are the tested, accessible, token-reading shapes the
project already has. A reinvented version is a parallel component the project
maintains, the next theme change has to update twice, and accessibility
([`touch-target-size`](touch-target-size.md),
[`content-description`](content-description.md)) is whatever the author
remembered to set. Reaching for the Material 3 component first is the discipline
that catches the reinvention before it lands.

## Sources complémentaires

- [`https://m3.material.io/components`](https://m3.material.io/components) — Material 3 component catalogue.
- [`https://developer.android.com/jetpack/compose/components`](https://developer.android.com/jetpack/compose/components) — Compose Material 3 component reference.
