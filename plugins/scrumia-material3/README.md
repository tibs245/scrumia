# scrumia-material3

The Material 3 UI capability for a Kotlin Multiplatform Mobile or Android project —
tokens, components, theming and accessibility, stated as falsifiable directives an
agent applies or refuses. Compose is the default toolkit; Views is an explicit choice
with a stated justification. Plugs in app by app.

## What it answers

A Kotlin Multiplatform Mobile or Android app that ships with this module asks the
same question the same way on every surface: did the developer reach for Material 3
or reinvent it? Did the colour come from `MaterialTheme.colorScheme` or from a hex
literal? Did the touch target clear 48dp or sit below it? Did the icon-only control
carry a TalkBack label or stay silent? The audit skill measures the gap rather than
asserting it.

## What it refuses

- **Compose is the default** — a View-based widget without a stated justification
  (legacy migration, View-only third-party library, performance) fails. Anything
  written greenfield is Composables, period.
- **Tokens come from Material 3** — a hardcoded color, typography step, shape
  corner, elevation or state-layer value fails. `MaterialTheme.colorScheme`,
  `Typography`, `Shapes`, `elevation`, and the state-layer system are the only
  declarations worth keeping in step.
- **Components come from Material 3** — a custom Button, Card, AppBar,
  NavigationBar, ListItem, Dialog or Snackbar built from primitives fails. Reach
  for `androidx.compose.material3.*` (or its View-side equivalent on the
  explicitly-chosen Views toolkit).
- **Dynamic color on Android 12+** — a static brand palette without a stated
  justification fails on Android 12 and above.
- **Touch target ≥ 48dp × 48dp** — an interactive control smaller than this fails.
  The Material 3 minimum is the threshold, not the recommendation.
- **Contrast ratio meets WCAG AA** — body text 4.5:1, large text (≥18sp regular or
  ≥14sp bold) 3:1. Numbers, not aesthetic judgement.
- **Icon-only controls carry `contentDescription`** — an `IconButton` without a
  TalkBack label fails. The label is part of the contract.

Each rule is a short file under `rules/`; each contributes to `implement` and
`review` through `extends.json`, so the same rule applies while code is written and
again while it is reviewed.

## What it ships

| Skill | Role |
|---|---|
| `scrumia-material3` | The entry point — Compose default, Views explicit, dissociation boundaries, the contract with the rest of the composition. |
| `material3-audit` | The audit against the seven refusals above. Reports; rewrites nothing without agreement. |

No `material3-setup` (no design tree to install — Material 3 tokens live in the
Kotlin source). No `material3-guardian` role shipped today — see
[`SKILL.md`](SKILL.md)'s *Standing role — open question* for the unresolved human
call on whether this module ships its own role or relies on `scrumia-design`'s
`designer`.

## Dissociation boundaries

`scrumia-material3` is a **UI system**, not a product. It refuses to overlap with:

- **`scrumia-design`** — web design slot, owned by `scrumia-design`. The boundary
  is restated inline in [`SKILL.md`](SKILL.md) and in
  `features/business/modular-composition/business.md`'s § *Lanes* — Material 3 is
  Android / Kotlin Multiplatform Mobile; the web style is `scrumia-design`.
- **`scrumia-kotlin-multiplatform-mobile`** — iOS-native UI (SwiftUI, UIKit)
  belongs to that module. Material 3 is the Android side of the same project.
- **`scrumia-kotlin`** — Kotlin language rules used inside Composables; this
  module owns Material 3 specifically.
- **Domain components** — the project's own business widgets (a domain card, an
  order summary) are built from Material 3 primitives, in the project's own code.
  This module does not own them.

## Sources

| Source | Pinned to |
|---|---|
| [`https://m3.material.io`](https://m3.material.io) | Material 3 system — tokens, components, theming |
| [`https://developer.android.com/jetpack/compose`](https://developer.android.com/jetpack/compose) | Jetpack Compose — the default toolkit |
| [`https://www.w3.org/WAI/WCAG21/Understanding/contrast-minimum.html`](https://www.w3.org/WAI/WCAG21/Understanding/contrast-minimum.html) | WCAG 2.1 contrast thresholds |

A rule whose source URL has rotted is a finding against the plugin, not the
project.

## Settings it reads

None — the module is configuration-free. Material 3 tokens, theming and component
choices are made in the Kotlin source, and the project's `build.gradle(.kts)`
declares the `androidx.compose.material3` dependency. The module reads nothing
under its own `params:` and the project's `.scrumia/config.yaml` carries no
Material 3 block.

## What it expects to find

An app that lists `scrumia-material3` in its own `modules` mapping; within it, the
Kotlin source files (`*.kt` under `androidMain/` or `src/main/`) are what the
rules apply to. A pure-Android project (no Kotlin Multiplatform Mobile) takes the
module standalone; a Kotlin Multiplatform Mobile project takes it alongside
`scrumia-kotlin-multiplatform-mobile` and `scrumia-kotlin`, and the three together
apply the rules without overlap.

A project override in `.scrumia/overrides/scrumia-material3.md` wins over this
module, as everywhere else in ScrumIA.

## Not shipped yet

No `material3-guardian` role — the dissociation boundary with `scrumia-design` is
exactly the question a designer must guard, and whether that role lives here or in
`scrumia-design` is a human call recorded on the implementing ticket (#454). No
`material3-setup` skill — there is no design tree to install; Material 3 tokens
live in Kotlin source. No `material3-refactor` skill — the audit reports and a
human fixes; the seven refusals do not lend themselves to a wholesale rewrite
pass, and a refactor that automates "rewrite a custom Button as `Button(...)`"
already exists in IDE tooling the project owns.

## Decisions

Open: standing role. Recorded on #454 — the human's call, not this module's to
make silently.
