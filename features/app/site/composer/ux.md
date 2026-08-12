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
standing where the module would have been keyed in the emitted YAML — the
only one of the three that survives being pasted into a repo.

## Interface constraints

**`implementation` and `practices` are per app.** They are the two slots
that repeat, so they are checkbox rows, and a practice attaches only to the
app types it applies to. Assigning a frontend data-fetching practice to a
backend app is the bug this rule exists to prevent.
