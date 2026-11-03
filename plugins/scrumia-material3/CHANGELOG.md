# Changelog — scrumia-material3

All notable changes to this module, on [Keep a Changelog 1.0.0](https://keepachangelog.com/en/0.1.0/).

## [Unreleased]

## [0.2.0] - 2026-11-03
### Added
- `rules/navigation-stack-idempotent.md` — a gesture that opens a screen does not push
  a destination already on top (one guard where screens are added), and an action
  closing several screens stops at a named destination instead of a fixed count; the
  rule states how to prove it in a test. Contributed to `implement` and `review`.
- `skills/material3-audit/SKILL.md` — a ninth check for the navigation stack.

### Changed
- `README.md`, `SKILL.md` — the new refusal is listed.

## [0.1.0] - 2026-08-22
### Added
- `extends.json`, `dependencies.jsonl` — the module contributes to `implement`,
  `review` and `audit` through the seven refusals below; no register is opened
  because no skill ships its own `scrumia-extends` call.
- `SKILL.md` — the entry point, restating the dissociation boundary with
  `scrumia-design` inline (BR-7 + AC-23).
- `rules/compose-default.md`, `rules/views-explicit-choice.md` — Compose is the
  default UI toolkit; Views is an explicit choice requiring a stated justification.
- `rules/tokens-from-material3.md` — hardcoded UI values are refused; Material 3
  tokens (`MaterialTheme.colorScheme`, `Typography`, `Shapes`, `elevation`,
  state layers) are the only declarations worth keeping in step.
- `rules/components-from-material3.md` — Material 3 components are the only
  buttons, cards, app bars, navigation, lists, dialogs and snackbars worth using;
  a custom-built equivalent is refused.
- `rules/dynamic-color.md` — dynamic color (Material You) is the default on Android
  12 and above; a static brand palette requires a stated justification.
- `rules/touch-target-size.md` — interactive controls are 48dp × 48dp or larger;
  the Material 3 minimum is the threshold.
- `rules/contrast-ratios.md` — body text 4.5:1, large text 3:1, against WCAG 2.1.
- `rules/content-description.md` — every icon-only control carries a
  `contentDescription` (TalkBack label).
- `skills/material3-audit/SKILL.md` — the audit against the seven refusals above;
  registered in `implement`, `review` and `audit` so a reviewer or auditor sees
  it beside the refusal entries.

### Changed
- `README.md` — addressed to whoever is deciding whether to run this module: what
  it answers, what it refuses, what it ships, and the dissociation boundaries with
  sibling modules.

- First release of `scrumia-material3`: the Material 3 UI capability for an Android
  or Kotlin Multiplatform Mobile project. Tokens, components, theming and
  accessibility, stated as falsifiable directives, with Compose as the default
  toolkit and Views as an explicit choice.

Earlier versions did not exist — this is the module's first release.
