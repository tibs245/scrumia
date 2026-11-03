# The navigation stack tolerates a double touch

*Refusal.* A gesture that opens a screen must not push the same destination twice, and
an action that closes several screens must stop at a named destination, never after a
fixed count.

## The platform fact

A touch is delivered the moment it arrives, but the next screen only appears on the
following frame, then transitions for about 300 ms while staying touchable. Two touches
less than 50 ms apart on a real phone therefore run the gesture twice, and an app that
owns its stack (for example Navigation 3, where the stack is a `NavBackStack` list the
app fills) pushes the same destination twice without a word.

While nothing counts the screens, the duplicate only costs one extra Back. It becomes a
real defect as soon as an action closes a fixed number of screens ("confirm removes two
screens"): the duplicate shifts everything and the user lands on the wrong screen.

## What is refused

1. A gesture that opens a screen without checking the top of the stack. The guard lives
   in **one place**, where the app adds a screen (one extension function or one
   navigation operation), and is never copied screen by screen.
2. A bare `backStack.add(...)` called from a gesture.
3. An action that closes several screens by count: two or more `removeLastOrNull()` in a
   row, or `repeat(n) { removeLast… }`.

```kotlin
// ❌ pushes twice when the gesture runs twice
onClick = { backStack.add(DetailRoute(id)) }

// ❌ lands on the wrong screen when the stack holds a duplicate
fun confirm(backStack: NavBackStack) {
    backStack.removeLastOrNull()
    backStack.removeLastOrNull()
}
```

## What is written instead

```kotlin
// ✓ one guard, in one place: a destination already on top is not pushed again
fun NavBackStack.pushIfNotOnTop(destination: NavKey) {
    if (lastOrNull() != destination) add(destination)
}

onClick = { backStack.pushIfNotOnTop(DetailRoute(id)) }

// ✓ close down to a named destination, with a defined fallback when it is absent
fun List<NavKey>.closedThrough(target: KClass<out NavKey>): List<NavKey> {
    val index = indexOfLast { target.isInstance(it) }
    return if (index == -1) dropLast(1) else take(index)
}

backStack.replaceAll(backStack.closedThrough(ChoiceRoute::class))
```

The fallback is a decision the function states, not an accident: here, one screen back
when `ChoiceRoute` is not in the stack.

## How to prove it in a test

Two `performClick()` calls in a row do **not** reproduce the defect: the test lets a
frame pass between them. The same holds for `performTouchInput { click(); click() }` and
for a frozen clock.

What reproduces it: take
`fetchSemanticsNode().config[SemanticsActions.OnClick].action`, call it twice inside a
single `composeTestRule.runOnUiThread { }`, then perform a system Back and assert the
user is back on the origin screen (`ListRoute`, say) rather than on a second `DetailRoute`.

For the second half, a unit test of the pure function that computes the stack after
closing, fed a stack that contains a duplicate (`ListRoute, ChoiceRoute, EditRoute,
EditRoute`), asserting the result ends at the expected destination.

## Why

The defect cannot be seen by hand: a person never touches twice within 50 ms in a demo,
and a test that lets a frame pass never does either. Only a guard at the single push
point and a stop at a named destination make the stack correct whatever the timing.

## What it pairs with

- [`touch-target-size`](touch-target-size.md) — the other rule about how a touch reaches
  a control: size decides whether it lands, this rule decides what a doubled one does.
