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

**An addition is a shelf without a row.** The modules that fill no slot are not
a choice between alternatives, so they take none of the anatomy that exists to
frame one: no sign, no leader, no fill, no `<details>`. They reuse `.shelf` and
`.opt` — what the seven rows already open into — so the block reads as
continuous with them without impersonating one. Three of a row's five cells
would have nothing true in them, and `design/components/slot-index/spec.md`
refuses both a second drawing of a slot and *"a row with a claim where its
question should be"*.

The block carries a heading, and that is not decoration. Without one, a shelf
appearing straight after the seventh `</details>`, at the shelf's own indent, is
exactly what an *open row's body* looks like — a visitor who left `design` open
reads `scrumia-rules` as one of its options. The heading wears the label
register `.presets-label` already uses, never `slot-name`'s: borrowing the row's
typography is borrowing the row. It is also what the shelf's `role="group"`
points at, having no row's question to be labelled by.

**The visitor's own module is one field, not two.** The location is the
`<source>:` half of the key, so it is typed as part of the answer rather than
picked beside it — the name-plus-origin pairing ADR-0021 rejected, arrived at by
a shorter road. The prefix set is open, so no control could enumerate it; and a
picker always has a value, which would make *"named with no location stated"*
unreachable and the refusal it must produce a rule that can never fire. The
field is `design/components/key-entry/`, and its refused state is drawn there.

## States

**The consequence survives the copy.** An emptied slot the project declares
states its cost three times, each in the idiom of where it sits: in the
option's description at decision time, in the open row's gap line after the
fact, and as a comment in the emitted YAML — the only one of the three that
survives being pasted into a repo. The comment stands where the module would
have been keyed; an app left with no module of its own carries the same
consequence on its empty mapping.

## Interface constraints

**`implementation` and `practices` are per app.** They are the two slots
that repeat, so they are checkbox rows, and a practice attaches only to the
app types it applies to. Assigning a frontend data-fetching practice to a
backend app is the bug this rule exists to prevent.
