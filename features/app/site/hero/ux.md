# UX — Hero

## Screen / flow

Entry point: the top of the home page, in both languages. Exit points: the primary
control (`#composer`, the composer section) and the ghost control (`workflow.html`).
Nothing below the hero is this feature's scope.

## Composition

- Eyebrow, three-line headline, one sentence of lead copy — plain text, no component.
- `.cta-row` with one `.btn.btn-primary` and one `.btn.btn-ghost`, per
  `design/components/button/spec.md`'s one-primary rule: a screen carries one filled
  control, not one per section, and this feature owns none of that rule's substance —
  it only spends it once, correctly.
- `.hero-figure`, Hop at default size, per `design/components/hop/spec.md`.
- `.counts`, three literals; their derivation is `tech.md`'s concern, not this file's.

## States

Single state: no empty, loading or error variant. The hero renders from the build or
not at all.

Reduced motion / no script: a reader with no JavaScript, a script that failed, or
`prefers-reduced-motion` set never sees Hop travel — it is already assembled, its eye
already lit, from the first frame. `tech.md` names the gate that withholds the `.js`
class; the criterion is `qa.md` AC-4 (a11y).

## Navigation

Reading order: eyebrow, headline, lead, controls, Hop, counts. The ring
(`.hero-figure`) is visible from the first frame — it never waits behind the arrival
fade the rest of the hero gets. The eyebrow, headline and lead fade in after the ring,
never before it: motion stands for causality here (`design/identity.md`, decision 2),
and Hop arriving before anything summoned it is the one order this page must never
show.

## Interface constraints

- The headline breaks are authored, not computed: `hero_title` carries `<br>` where
  the line should end, in both languages, and no CSS `text-wrap: balance` substitutes
  for that choice. A copy change re-checks the line silhouettes in both languages.
- The headline carries no emphasised word when its clauses are parallel: pointing at
  one of three equals makes the other two read as lesser. The filled control is then
  the hero's only accent, which is what `design/identity.md` decision 4 asks for.
- The hero never spends `--human` or `--agent`. Only `--accent`, `--text` and the
  surfaces — the human/agent colour rule is a different feature's decision and
  the hero does not anticipate it either way. Tested by `qa.md` AC-5.
- The headline states no model of the composition that a section further down the
  same page contradicts. It is checked against what `#slots` and `#extends` (or
  their successors) actually describe, not asserted on its own — a headline that
  still claims "every capability is a slot" once a section describes capabilities
  filling no slot has drifted from the page it opens. Tested by `qa.md` AC-6.
