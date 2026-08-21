# Compose is the default UI toolkit

*Norm.* A Composable is the default unit of UI in an Android or Kotlin Multiplatform
Mobile app that adopts this module. Views is the explicit choice and is governed by
[`views-explicit-choice`](views-explicit-choice.md).

## What is the default

A greenfield surface — a new screen, a new feature, a new widget — is written in
Compose. The default UI toolkit is Jetpack Compose with `androidx.compose.material3`
as the component layer; `MaterialTheme { ... }` is the entry point every Composable
sits under, and tokens (`colorScheme`, `Typography`, `Shapes`) flow from there.

```kotlin
@Composable
fun Greeting(name: String) {
    Text(
        text = stringResource(R.string.greeting, name),
        style = MaterialTheme.typography.bodyLarge,
        color = MaterialTheme.colorScheme.onSurface,
    )
}
```

The default is also a **rule about what to reach for first.** When a component does
not exist as a Material 3 building block, the question is *is there a Material 3
component for this*, not *can I build this from primitives*. The second question is
the failure mode — a `Box { Row { Text(...) } }` shaped like a Button is a
reinvented Button, and it is [`components-from-material3`](components-from-material3.md)'s
finding.

## What is not the default

Anything View-based — `Activity` inflating an XML layout, a custom `View`,
`ViewBinding`, `RecyclerView` with a `ViewHolder`. See
[`views-explicit-choice`](views-explicit-choice.md) for what a Views surface owes in
return for the choice.

## Why

Compose is Google's stated default for new Android UI, and `material3` is the
component layer that ships with it. A project whose rule book does not say
"Compose by default" reaches for what each developer happens to know — XML layouts,
custom `View`s, half a `Fragment` — and produces an app whose screens disagree on
which toolkit they were written for. The default is the answer that holds while
each individual developer decides, and it is the refusal that catches the drift
later.

## What it pairs with

- [`views-explicit-choice`](views-explicit-choice.md) — the companion refusal that
  names what a Views surface must justify.
- [`tokens-from-material3`](tokens-from-material3.md) — Compose is the default,
  and the tokens come from Material 3, never from raw hex / sp / dp values.
- [`components-from-material3`](components-from-material3.md) — the components
  come from `androidx.compose.material3.*`, not from `Box` / `Row` primitives.

## Sources complémentaires

- [`https://developer.android.com/jetpack/compose`](https://developer.android.com/jetpack/compose) — Jetpack Compose reference. Authority: Google's stated default for new Android UI.
- [`https://developer.android.com/develop/ui/compose`](https://developer.android.com/develop/ui/compose) — Compose UI toolkit overview.
