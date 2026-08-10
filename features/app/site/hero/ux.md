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
  for that choice.
- The hero never spends `--human` or `--agent`. Only `--accent`, `--text` and the
  surfaces — the human/agent colour rule is a different feature's decision and
  the hero does not anticipate it either way. Tested by `qa.md` AC-5.
