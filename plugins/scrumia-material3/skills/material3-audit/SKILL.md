---
name: material3-audit
description: Audits an Android or Kotlin Multiplatform Mobile app against the seven Material 3 refusals this module ships — Compose as default, tokens from Material 3, components from Material 3, dynamic color, touch target size, contrast ratios, contentDescription on icon-only controls. Use it before adopting the module on an existing codebase, when a UI bug ships, or to take stock after a phase of rapid screen additions.
---

# Auditing a Material 3 surface

Seven questions, one per rule. Answer them in order — the first three are read
from the Kotlin source, the fourth from the manifest, the last three from a
rendered surface. Report findings; change nothing without being asked.

The seven refusals are stated in `rules/`:

1. [`rules/compose-default.md`](../../rules/compose-default.md) — Compose is the
   default toolkit.
2. [`rules/views-explicit-choice.md`](../../rules/views-explicit-choice.md) —
   Views is an explicit choice requiring a stated justification.
3. [`rules/tokens-from-material3.md`](../../rules/tokens-from-material3.md) —
   tokens come from `MaterialTheme.*`, not raw hex / sp / dp values.
4. [`rules/components-from-material3.md`](../../rules/components-from-material3.md) —
   components come from `androidx.compose.material3.*`.
5. [`rules/dynamic-color.md`](../../rules/dynamic-color.md) — dynamic color is
   the default on Android 12+; static palette needs justification.
6. [`rules/touch-target-size.md`](../../rules/touch-target-size.md) — 48dp × 48dp
   minimum.
7. [`rules/contrast-ratios.md`](../../rules/contrast-ratios.md) — 4.5:1 body /
   3:1 large (WCAG AA).
8. [`rules/content-description.md`](../../rules/content-description.md) —
   `contentDescription` on icon-only controls.

(That's eight — `compose-default` and `views-explicit-choice` are the same
question from two sides, and both are listed in `extends.json`.)

## Step 1 — Establish the toolkit

Before answering any of the seven questions, confirm the project is set up to
answer them:

```bash
grep -r "androidx\.compose\.material3" --include=*.gradle.kts --include=*.gradle .
grep -r "androidx\.compose:compose-bom" --include=*.gradle.kts --include=*.gradle .
```

A project without `material3` on the classpath cannot satisfy the
[`components-from-material3`](../../rules/components-from-material3.md) rule —
adding the dependency is the prerequisite for adopting the module, and the
audit says so on the first question if it is missing.

For a Kotlin Multiplatform Mobile project, confirm the same dependency is in
`androidMain` (the Android target) and that iOS targets are untouched by
`material3` — `scrumia-kotlin-multiplatform-mobile`'s lane is the iOS side.

## Step 2 — Toolkit (Compose vs Views)

Find what kind of surface the project ships.

```bash
# Count Composable functions vs Activity/Fragment-based View surfaces
grep -rn "@Composable" --include=*.kt src | wc -l
grep -rn "AppCompatActivity\|setContentView" --include=*.kt src | wc -l
```

A project whose ratio is heavily View-based without a stated justification for
each View surface is a finding of
[`views-explicit-choice`](../../rules/views-explicit-choice.md). The
[`compose-default`](../../rules/compose-default.md) rule says greenfield is
Compose; existing Views surfaces are kept only with a justification in the PR
that introduced them.

## Step 3 — Tokens

Find hardcoded UI values that bypass `MaterialTheme.*`:

```bash
# Hex colors in Kotlin source
grep -rn "Color(0x[0-9A-Fa-f]\{6\})" --include=*.kt src
# Raw sp / dp typography outside MaterialTheme.typography
grep -rn "fontSize\s*=\s*[0-9]\+\.sp" --include=*.kt src
# Hardcoded RoundedCornerShape / CircleShape sizes
grep -rn "RoundedCornerShape([0-9]" --include=*.kt src
```

Each is a finding of
[`tokens-from-material3`](../../rules/tokens-from-material3.md). The exception:
a one-off decorative value (an illustration, a brand asset) that is genuinely
used once and is marked as such in a comment. The audit reads the comment.

## Step 4 — Components

Find custom-built Buttons, Cards, TopAppBars, NavigationBars and the rest:

```bash
# Clickable Boxes / Rows / Surfaces that look like Buttons
grep -rn "Modifier\.clickable" --include=*.kt src | head -50
# Card-shaped Surfaces that bypass Card
grep -rn "Surface($\|tonalElevation\s*=" --include=*.kt src | head -50
# Top-bar-shaped Rows
grep -rn "TopAppBar\|@OptIn.*TopAppBar" --include=*.kt src
```

Each candidate is read against
[`components-from-material3`](../../rules/components-from-material3.md)'s *When
a custom component is the answer* list: a genuinely new pattern, a domain
composite, a wrapper. Anything else is a finding.

## Step 5 — Dynamic color

Find the colour scheme construction:

```bash
grep -rn "dynamicLightColorScheme\|dynamicDarkColorScheme\|lightColorScheme\|darkColorScheme" --include=*.kt src
```

A project that uses `lightColorScheme()` / `darkColorScheme()` directly with
no dynamic-color branch on Android 12+ is a finding of
[`dynamic-color`](../../rules/dynamic-color.md). A project whose `minSdk` is
below 31 is exempt — dynamic color is API 31+ — and the audit says so rather
than reporting it as a finding.

## Step 6 — Touch targets

This question is answered from a rendered surface, not the source. The
source tells you which controls exist; the renderer tells you their size.

For each interactive control in the surface:

```bash
grep -rn "IconButton\|Button(\|ClickableText\|Switch(\|Checkbox(" --include=*.kt src
```

Read the modifier chain. A control without `Modifier.size(48.dp)`,
`Modifier.defaultMinSize(minWidth = 48.dp, minHeight = 48.dp)`, or a parent
container that supplies the minimum size is a finding of
[`touch-target-size`](../../rules/touch-target-size.md). The Material 3
`IconButton` and `Switch` defaults are 48dp when used as the Material 3 API
intends; a project that strips the default is held to the explicit modifier.

## Step 7 — Contrast

This question is answered from a rendered surface, in both themes. The
threshold is the **rendered** pair, not the source pair:

| Pair | Minimum ratio |
|---|---|
| Body text against its background | 4.5 : 1 |
| Large text (≥18sp regular / ≥14sp bold) against its background | 3 : 1 |
| Icon-only controls against their background | 3 : 1 |

A `MaterialTheme.colorScheme.onSurface` against a wallpaper-derived
`colorScheme.surface` is the Material 3 contract: the dynamic palette is
generated against WCAG AA, and the audit confirms the rendered pair on a real
device. A project's static palette override is held to the same numbers.

## Step 8 — contentDescription

Find every interactive control whose only visible content is an icon:

```bash
grep -rn "IconButton\|Icon(.*clickable" --include=*.kt src
```

For each, the `contentDescription` parameter is read. A null, an empty
string, or a description that names the pixels rather than the action
("plus icon" instead of "Add item") is a finding of
[`content-description`](../../rules/content-description.md). The rule for
decorative icons — non-interactive icons, separators, logos — is that `null`
is correct; the audit only reports `null` when the icon is interactive.

## Reporting

One finding per line: the file, the line, the rule's name, and one line of
what was not met. Group by rule so a reader can see the cluster. Close with
a count of "controls without a label" and "tokens outside `MaterialTheme.*`"
— those two numbers are usually the ones worth acting on first.

When a finding is borderline (a custom control that is genuinely a domain
composite, a hardcoded value in a decorative-only context), say so and let
the human decide. The audit reports; it does not invent certainty.

## Standing role — open question

The dissociation boundary with `scrumia-design` is exactly the question a
designer must guard, and whether that role is filled by `scrumia-design`'s
`designer` or by a future `material3-guardian` is a human call on the
implementing ticket (#454). Until the call lands, escalate interface
judgement to `scrumia-design`'s `designer` role (if the project has it
enabled), and report the rest as findings.
