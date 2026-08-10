# UX — Slot index

## Composition

One component: `design/components/slot-index/spec.md`. It draws every row —
sign, name, question, dotted leader, fill — and is the only component in
`design/` allowed to draw a slot; its own refusals cover the second-drawing
case, not restated here.

## States

**Exactly seven rows, no eighth example.** Every row is one of the project's
real slots, read from `.scrumia/config.yaml` at the time this was written —
`specs`, `tracker`, `team`, `discovery`, `implementation`, `practices`,
`design`. None is illustrative; a made-up "and if you leave a slot empty?"
row would be exactly the kind of claim `design/identity.md`'s "mechanism over
claim" rule exists to block.

**An empty row states its emptiness in words.** `.slot-fill` reads `nothing
installed`; the dashed leader reinforces that word but is never the only
signal — a stroke style alone is not perceivable to everyone. Tested by
AC-2.
