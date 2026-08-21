# Touch target size ≥ 48dp × 48dp

*Refusal.* An interactive control smaller than 48dp × 48dp is refused. The
Material 3 minimum is the threshold, not the recommendation.

## What is refused

Any interactive element — `Button`, `IconButton`, `ClickableText`, a clickable
`Box` / `Row`, a `Switch`, a `Checkbox`, a custom clickable — whose touch target
is below 48dp × 48dp:

```kotlin
// ❌ an IconButton with no size modifier — defaults to the icon's intrinsic size
IconButton(onClick = onClick) {
    Icon(Icons.Default.Add, contentDescription = "Add")
}

// ❌ a clickable Box without a size modifier — the Box shrinks to its content
Box(
    modifier = Modifier.clickable(onClick = onClick)
) {
    Text("Add", style = MaterialTheme.typography.labelSmall)
}

// ❌ a Switch without the recommended 48dp track height
Switch(checked = checked, onCheckedChange = onCheckedChange)
```

The size is the touch target — the area the user can actually tap — not the
visual size of the icon or label inside it. An `Icon` 24dp wide inside a 24dp
clickable area is a 24dp touch target, and 24dp is below 48dp regardless of how
the icon looks.

## What is written instead

A touch target of at least 48dp × 48dp, declared with a `size` or `defaultMinSize`
modifier:

```kotlin
// ✓ an IconButton sized to the minimum touch target
IconButton(
    onClick = onClick,
    modifier = Modifier.size(48.dp),  // the touch target
) {
    Icon(Icons.Default.Add, contentDescription = "Add")
}

// ✓ a clickable Box sized to the minimum touch target
Box(
    modifier = Modifier
        .clickable(onClick = onClick)
        .sizeIn(minWidth = 48.dp, minHeight = 48.dp),
) {
    Text("Add")
}

// ✓ a Switch in its Material 3 default sizing — already 48dp on the track
Switch(checked = checked, onCheckedChange = onCheckedChange)
```

Material 3's `IconButton` defaults its minimum interactive size to 48dp when
wrapped in a `ButtonDefaults.IconButtonSize` container; the explicit
`Modifier.size(48.dp)` is the assertion that survives a refactor that strips
the wrapper. A custom `ClickableBox` carries its `sizeIn(minWidth = 48.dp,
minHeight = 48.dp)` modifier.

## What about visual size

The 48dp touch target and the 24dp icon are not the same thing. The touch
target is the clickable area; the icon is what the user sees. Compose's pattern
is `Box(contentAlignment = Alignment.Center) { Box(modifier = Modifier.size(48.dp).clickable {}); Icon(size = 24.dp) }` — the visible icon sits
inside a larger touch target, and the user's finger lands on something the
icon does not need to fill.

A visual size larger than the touch target is also a finding when the visual
is the click target — a `Button { Text }` that fills its container to 24dp tall
is reading its own height as the touch target, and a finger lands on the
margin.

## Why

48dp is the Material 3 minimum, derived from the average finger-pad size and
the WCAG 2.5.5 target size guideline. Below it, a user with a finger larger
than the developer's, or a hand tremor, or a screen-protector-induced offset,
misses the control or hits the wrong one. The number is not a recommendation
— it is the threshold below which the control is broken on devices the
project will never see in QA.

## What it pairs with

- [`contrast-ratios`](contrast-ratios.md) — touch target and contrast are
  the two halves of WCAG 2.1 Level AA for interactive UI.
- [`content-description`](content-description.md) — a touch target without a
  TalkBack label is half the accessibility contract.

## Sources complémentaires

- [`https://m3.material.io/foundations/accessible-design/accessibility-basics`](https://m3.material.io/foundations/accessible-design/accessibility-basics) — Material 3 accessibility baseline, including the 48dp touch target.
- [`https://www.w3.org/WAI/WCAG21/Understanding/target-size.html`](https://www.w3.org/WAI/WCAG21/Understanding/target-size.html) — WCAG 2.5.5 target size.
- [`https://developer.android.com/guide/topics/ui/accessibility`](https://developer.android.com/guide/topics/ui/accessibility) — Android accessibility guidelines.
