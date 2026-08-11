# UX — Composer

## Composition

**One drawing of a slot, in a third state.** The composer does not draw its
own slot. It reuses `slot-index`'s row — `sign · name · question · leader ·
fill` — and adds *choosable* as a third state alongside filled and empty,
per `design/components/slot-index/spec.md`. A second drawing of a slot would
undo the ruling that gave `slot-index` its one authoritative drawing.

**The two indexes are told apart by colour, not by shape.** `#slots` reports
this repo's composition and its fills are `--text-soft`; `#composer` records
the visitor's decisions and its fills are `--human`, because choosing is the
one human act in the section. That is `design/identity.md`'s decision 1
applied, not a decoration.

## States

**The consequence survives the copy.** An empty slot's cost is stated three
times, each in the idiom of where it sits: in the option's description at
decision time, in the open row's gap line after the fact, and as a comment
on the `null` in the emitted YAML — the only one of the three that survives
being pasted into a repo.

## Interface constraints

**`implementation` is per app, and its row now carries practices too.** Since
`docs/adr/0019-extends-replaces-composition-and-practices.md`, a practice is
declared in the same `extends` list as the app's implementation module — the
composer's `implementation` row keeps its single-select radio for the
implementation module and gains checkbox sub-choices for the practices that
apply to the app's type, both feeding the same per-app `extends` list. A
practice attaches only to the app types it applies to; assigning a frontend
data-fetching practice to a backend app is the bug this rule exists to
prevent, unchanged from before the merge.
