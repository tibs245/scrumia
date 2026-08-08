---
name: scrumia-design-audit
description: Audits an existing interface against the design system — the drift (invented values, duplicated components) and, on equal footing, the mutedness (consistent but with no identity). Use it before a redesign, when plugging this module into an existing app, or to take stock after a phase of rapid growth.
---

# Auditing an interface

This audit has two columns, of equal importance: **the drift** (the system exists and the screen ignores it) and **the mutedness** (the screen obeys the system and still looks like nobody's product). Delivering one without the other produces a tidy interface with nothing to say — a deliberate choice, not an oversight: see [D-01](../scrumia-design-system/decisions/D-01-two-columns.md).

This is the skill that decides adoption. Plugging a design module into screens that predate it is the real moment; a module that can only judge interfaces born under its rules will never be plugged into anything.

## Step 1 — Establish the yardstick

Read the `## Design contract` in `CLAUDE.md`, then `identity.md` and `tokens.css`.

If `identity.md` is empty or absent, **stop and say so**. The drift column can be produced without it; the mutedness column cannot, because "has no identity" is only measurable against a stated one. Offer [scrumia-design-setup](../scrumia-design-setup/SKILL.md) Step 3 and audit the drift alone, saying explicitly that half the audit is missing.

## Step 2 — Sweep, then look

Three cheap entry points first:

- Hard-coded values in the stylesheets — hex colors, `px` spacings, `rem` type sizes that no token carries
- Component names that repeat with a suffix (`-alt`, `-2`, `-new`, `-old`)
- Screens whose stylesheet is longer than the components they compose

Then a targeted pass over what those three designated — and, separately, an actual look at the rendered result. The drift column can be greped; the mutedness column cannot. A screen where every value is a token and nothing is memorable passes every mechanical check.

## Step 3 — The two columns

**Drift** — for each finding: the file and selector, the invented value, the token that should have carried it. A value with no token is a two-part finding: name the missing token as well.

**Mutedness** — for each finding: the screen, and what the identity claims that the screen does not deliver. Anchor it in `identity.md`: "identity says *dense and fast*; this page is three cards of body text at 16px" is a finding. "It feels bland" is not.

What is **not** a finding:

- A young screen in a zone declared as exploration — drift is judged on stabilized interfaces
- A one-off value in a component that genuinely exists once, and is marked as such
- Your own taste, in either column

## Step 4 — Accessibility, separately

Contrast on real pairs in every theme, visible focus, `prefers-reduced-motion`, target sizes. These are not drift findings and they are not opinions: they pass or they fail. List them apart, with the measured ratio and the pair.

## Step 5 — The synthesis

Three lines: the state of the interface in one sentence, the two most profitable findings to address, what can wait.

Then say plainly whether this is a repair or a redesign. An interface with heavy drift and a working identity gets repaired, finding by finding. An interface whose mutedness column is the long one is not repaired by fixing tokens — it needs an identity first, and every drift fix applied before that is work done against a yardstick nobody believes in.
