---
name: scrumia-material3
description: The Material 3 entry point for an Android or Kotlin Multiplatform Mobile app — Compose is the default, Views is an explicit choice, and every token, component, theming and accessibility rule is stated as a falsifiable directive. Load before writing UI in an app that extends this module.
---

# Material 3 in ScrumIA

This module teaches Material 3 as **the system** — tokens, components, theming, and
accessibility — and refuses to read it as a vocabulary instantiated in some other
repository. What it owns is the rules an Android or Kotlin Multiplatform Mobile project
applies; what it does not own is the project's own brand or the iOS-native side of
Kotlin Multiplatform Mobile.

## What this module owns

- **Tokens** — color (`MaterialTheme.colorScheme`), typography (`Typography`),
  shape (`Shapes`), elevation, state layers. Stated as Material 3 tokens, never as
  raw hex / sp / dp values.
- **Components** — buttons, cards, app bars, navigation, lists, dialogs, snackbars.
  Each is a refusal to reinvent it under `androidx.compose.material3` (or the matching
  Material Components for Android on the Views side, when Views is the chosen toolkit).
- **Theming** — dynamic color (Material You) on Android 12 and above; static brand
  palettes with a stated justification when dynamic color is refused.
- **Accessibility** — touch target ≥ 48dp × 48dp; contrast 4.5:1 body / 3:1 large;
  `contentDescription` on icon-only controls; numbers, not aesthetic judgement.

## What this module refuses

- **Compose is the default.** A View-based widget is an explicit choice requiring a
  stated justification in the PR — legacy migration, View-only third-party
  dependency, performance constraint. Anything else is refused.
- **Hardcoded values.** A color, a typography step, a shape corner, an elevation or a
  state-layer value pulled from outside `MaterialTheme.*` is refused. The token is
  the only declaration worth keeping in step.
- **Reinvented components.** A Button, Card, AppBar, NavigationBar, ListItem, Dialog
  or Snackbar built from `Box` / `Row` / `Card { ... }` primitives instead of the
  matching Material 3 component is refused.
- **Icon-only controls without a label.** An `IconButton` (or its View-side
  equivalent) without `contentDescription` is refused — the TalkBack label is part
  of the contract, not a finishing touch.

Each rule is a short file under `rules/`; each contributes to the `implement` and
`review` registers through `extends.json`, so the same rule applies while code is
written and again while it is reviewed.

## Dissociation boundary with `scrumia-design` (BR-7 + AC-23)

Restated inline so this skill can be applied without resolving any link: `scrumia-design`
owns the **web** design slot (`tokens.css`, `identity.md`, `components/<name>/`,
React / SolidJS components); `scrumia-material3` owns the **Android / Kotlin
Multiplatform Mobile** Material 3 slot (`MaterialTheme.*`, `androidx.compose.material3`,
Kotlin rules, Compose and Views). A Material 3 token has no equivalent in
`scrumia-design`; a CSS custom property under `design/tokens.css` has no equivalent
here. Reaching for one in the other's lane is a refusal on both sides.

Provenance pointer: this dissociation is stated in the home-repo's
[`features/business/modular-composition/business.md`](https://github.com/tibs245/scrumia/blob/main/features/business/modular-composition/business.md)
§ *Lanes — Material 3, distinct from `scrumia-design`*. The inline statement above
is what an agent applies; the URL is where the rule is owned in source. This restate
is required by the home-repo's BR-7 and AC-23 because this plugin owns its source
file but not the consumer's `features/` tree — a consumer's `scrumia-specs` instance
ships its own `features/` with the same path shape and content that may differ.

## Dissociation from sibling modules

- **`scrumia-design`** — web design system, distinct lane (see above).
- **`scrumia-kotlin-multiplatform-mobile`** — Kotlin Multiplatform Mobile project
  layout, shared modules, iOS-native UI. Material 3 is the Android-side UI system;
  iOS-native UI lives in that module.
- **`scrumia-kotlin`** — Kotlin language rules. The Composable is still Kotlin;
  language-level rules apply through that module, Material 3 rules through this one.
- **Domain components** — a project's own business widgets (a domain card, an order
  summary) live in the project's own code, built from Material 3 primitives. This
  module does not own them.

## Settings it reads

None. Material 3 tokens, theming, and component choices are made in the project's
Kotlin source, not in `.scrumia/config.yaml`. The vitest-style runtime detector does
not exist here: Compose is detected by `androidx.compose.material3` being on the
classpath, which is the project's `build.gradle(.kts)` to declare, not this module's
to check.

## The other skill

`material3-audit` — measures the gap between an existing Android / Kotlin Multiplatform
Mobile app and these refusals, finding by finding.

## Sources

| Source | Authority |
|---|---|
| [`https://m3.material.io`](https://m3.material.io) | Material 3 system — tokens, components, theming |
| [`https://developer.android.com/jetpack/compose`](https://developer.android.com/jetpack/compose) | Jetpack Compose reference — the default toolkit |
| [`https://www.w3.org/WAI/WCAG21/Understanding/contrast-minimum.html`](https://www.w3.org/WAI/WCAG21/Understanding/contrast-minimum.html) | WCAG 2.1 contrast thresholds — the source of the 4.5:1 / 3:1 numbers |
| [`https://developer.android.com/guide/topics/ui/accessibility`](https://developer.android.com/guide/topics/ui/accessibility) | Android accessibility — touch targets, `contentDescription` |

The numbers (48dp, 4.5:1, 3:1) are the WCAG / Material 3 contract, not a preference.
A rule whose source URL has rotted is a finding against the plugin, not the project.

## Project override

If `.scrumia/overrides/scrumia-material3.md` exists, its content takes precedence
over this skill and its rules. A project records its house exceptions there — a
forced brand palette that overrides dynamic color, an accessibility floor higher
than 48dp — without forking the module.

## Standing role — open question

The home-repo's `features/business/agent-team/` AC-16 says a module ships the
standing role that guards its capability. `scrumia-design` ships `designer` for the
web lane; whether `scrumia-material3` ships its own `material3-guardian` for the
Android lane, or relies on `scrumia-design`'s `designer` for both lanes, is a
human call surfaced on the implementing ticket (#454). Until that call lands, this
module ships no role of its own.
