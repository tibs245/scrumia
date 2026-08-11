# UX — Slot index

## Composition

One component: `design/components/slot-index/spec.md`. It draws every row —
sign, name, question, dotted leader, fill — and is the only component in
`design/` allowed to draw a slot; its own refusals cover the second-drawing
case, not restated here.

## States

**Exactly six rows, no seventh example.** Every row is one of the project's
real questions, read from `.scrumia/config.yaml` at the time this was written —
`specs`, `tracker`, `team`, `discovery`, `implementation`, `design`. The row
that used to be `practices` no longer exists on its own: since
`docs/adr/0019-extends-replaces-composition-and-practices.md`, a practice is
declared through the same `extends` list as the app's implementation module,
so the `implementation` row's fill is what that app's `extends` list names —
implementation module and practices together, comma-separated, or `nothing
installed` when the list is empty. None of the six is illustrative; a
made-up "and if you leave a slot empty?" row would be exactly the kind of
claim `design/identity.md`'s "mechanism over claim" rule exists to block.

**An empty row states its emptiness in words.** `.slot-fill` reads `nothing
installed`; the dashed leader reinforces that word but is never the only
signal — a stroke style alone is not perceivable to everyone. Tested by
AC-2.
