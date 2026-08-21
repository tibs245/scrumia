# Icon-only controls carry a contentDescription

*Refusal.* An `IconButton` (or its View-side equivalent — an `ImageButton`, an
`ImageView` with `clickable`, a `MaterialButton` with an `Icon` and no text) is
refused if it carries no `contentDescription`. The TalkBack label is part of
the contract, not a finishing touch.

## What is refused

An interactive control whose only visible content is an icon and which does
not declare what the icon means to a screen reader:

```kotlin
// ❌ an IconButton without a contentDescription — TalkBack reads nothing
IconButton(onClick = onClick) {
    Icon(Icons.Default.Add, contentDescription = null)
}

// ❌ an IconButton with an empty contentDescription — TalkBack reads nothing
IconButton(onClick = onClick) {
    Icon(Icons.Default.Add, contentDescription = "")
}

// ❌ an Icon whose only purpose is to be clicked — no Button, no label
Icon(
    Icons.Default.Delete,
    modifier = Modifier.clickable(onClick = onClick),
    contentDescription = null,
)
```

The same shape on the Views side:

```xml
<!-- ❌ an ImageButton with no contentDescription -->
<ImageButton
    android:id="@+id/delete_button"
    android:layout_width="wrap_content"
    android:layout_height="wrap_content"
    android:src="@drawable/ic_delete" />

<!-- ❌ an ImageButton with a contentDescription set to an empty string -->
<ImageButton
    android:id="@+id/delete_button"
    android:layout_width="wrap_content"
    android:layout_height="wrap_content"
    android:src="@drawable/ic_delete"
    android:contentDescription="" />
```

A null or empty `contentDescription` reads as "this control has no semantic
name"; TalkBack skips it, the user has no way to know what the icon does, and
the control is broken on the device the user is holding.

## What is written instead

A `contentDescription` that names what the control does, in the user's
language:

```kotlin
// ✓ an IconButton with a contentDescription that names the action
IconButton(onClick = onClick) {
    Icon(Icons.Default.Add, contentDescription = "Add item")
}

// ✓ an IconButton whose label comes from a string resource, localised
IconButton(onClick = onClick) {
    Icon(
        Icons.Default.Add,
        contentDescription = stringResource(R.string.action_add_item),
    )
}
```

The label names the **action**, not the icon. "Add" / "Delete" / "Share" are
actions; "plus icon" / "trash can" / "share arrow" are descriptions of pixels
the user does not see and TalkBack does not announce. The label is what the
control does when activated, and it is what a sighted user would say if asked
"what does this button do?"

### Decorative icons

An icon that is purely visual — a separator, a logo in a corner, an
illustration with no interactive role — is marked `contentDescription = null`
**and** `Modifier.semantics { contentDescription = null }` is unnecessary
because the null already signals "decorative, skip me." The rule says
*interactive* controls carry a label; a non-interactive icon does not, and
the null is the correct annotation, not a missing one. The audit's question
is *is this icon the only visible content of an interactive control*, and a
null is only the answer when the icon is not interactive.

### Toggle buttons

A toggle button — favourite / unfavourite, mute / unmute — carries a
`contentDescription` that names the **current state** the user is moving
*from*, and the role announces the change. The Material 3 pattern:

```kotlin
val label = if (isFavourite) "Remove from favourites" else "Add to favourites"
IconButton(onClick = { isFavourite = !isFavourite }) {
    Icon(
        imageVector = if (isFavourite) Icons.Default.Favorite else Icons.Default.FavoriteBorder,
        contentDescription = label,
    )
}
```

## Why

A user on TalkBack — blind, low-vision, or with motor impairment that makes
the screen impossible to read — has no other way to know what an icon-only
control does. The `contentDescription` is the only channel; a null or empty
value is the control saying "I am not labelled," and the user is not
magically able to guess. The label is the contract the project owes every
user regardless of how they reach the screen.

## What it pairs with

- [`touch-target-size`](touch-target-size.md) — the touch target and the
  label are the two halves of the interactive accessibility contract.
- [`contrast-ratios`](contrast-ratios.md) — an icon-only control whose icon
  fails the 3:1 contrast against its background fails the non-text contrast
  threshold (WCAG 1.4.11) as well.

## Sources complémentaires

- [`https://developer.android.com/guide/topics/ui/accessibility/apps`](https://developer.android.com/guide/topics/ui/accessibility/apps) — Android accessibility — labels, contentDescription, TalkBack.
- [`https://m3.material.io/foundations/accessible-design/accessibility-basics`](https://m3.material.io/foundations/accessible-design/accessibility-basics) — Material 3 accessibility baseline.
