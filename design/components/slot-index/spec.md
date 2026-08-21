# slot-index

One composition, read top to bottom: seven rows, each a slot's question and
what currently answers it.

Replaces `slot-card` (#61). The card drew the same information as isolated
rectangles; the designer's ruling was that the card goes and the index stays
— a design system with two ways to draw a slot has decided nothing. This file
carries forward everything from the card's spec that still holds.

## When to use it

To show a composition — which capabilities exist and what fills them. Each
row carries four things, in this order, and the order is the argument: the
slot's name, its **question**, a dotted leader, and what fills it. The
answer — the prose that used to sit on a card's face — opens on demand, in a
native `<details name="slot">` so the seven rows behave as one accordion
with no script reading or writing that state.

| State | Class | Reads as |
|---|---|---|
| Filled | `.slot` | dotted leader, accent sign and fill when open, module name in the row |
| Empty | `.slot.slot-empty` | dashed leader, muted name, `nothing installed` |
| Choosable | `.slots-choose .slot` | the same row, but the fill is a decision the reader makes — `--human`, because choosing is the human act |

## The choosable state (#56)

An index can report a composition or take one. Reporting is the default;
`.slots-choose` on the container turns the same seven rows into the choice.
Nothing about the anatomy changes — only what sits in the `<details>` body, and
what colour the fill carries.

- **The body is a shelf of native inputs**, one `<label class="opt">` per
  option: radios for a slot that takes one module, checkboxes for the two that
  repeat per app. `leave it empty` is an option in every group, never an
  absence of options.
- **`--human` marks the fill**, against `--text-soft` in a reporting index.
  A reported fill is a fact; a chosen one is a decision, and
  `design/identity.md` decision 1 says who decisions belong to.
- **CSS reports the choice, not script.** `.slot-fill` holds one pre-rendered
  span per option and `:has()` reveals the checked one. The index therefore
  keeps the property that made it worth choosing over a card: it opens, chooses
  and reports with no JavaScript running.
- **`name=` must differ per index.** Two indexes on one page grouped under the
  same `name` become one accordion across sections — opening a composer row
  would close a reporting row two sections away.

The empty state is unchanged in meaning: `.slot-empty` for a reported absence,
and `:has(.opt-empty input:checked)` for a chosen one. Both draw the same row,
because a slot only ever knows decided states — and both draw their fill at
body weight, because bold on the word `nothing installed` sends two signals at
once.

### The gap idiom

What an empty slot costs is stated in the **gap idiom**: `--font-mono` at
`--text-xs`, `--text-soft`, indented `--space-4` behind a `--space-tight`
`--border-strong` rule. No human blue and no accent — a capability reported
absent is the system saying what it cannot do, not a person deciding and not
something pointing. It is the one register in which a degradation is allowed to
speak, and any new place that needs to say "this is what you gave up" wears it
rather than inventing a variant.

## Row anatomy

`sign` · `name` · `question` · dotted leader · `fill` — in that order, inside
a `<summary class="slot-row">`. The answer is a `<p class="slot-answer">`, the
`<details>` element's only other child, indented to align under the question.
`+` is the sign at rest; open, it rotates and turns accent-coloured, which is
the only motion a script-free control needs to announce its own state.

## Why the empty state is drawn rather than omitted

A missing row says "we forgot". A dashed leader says "we decided". ScrumIA's
whole position on absent capabilities — agents are told the capability is
missing and say so instead of improvising it — is only legible if the
absence has a shape. That makes `.slot-empty` load-bearing, not a courtesy
variant.

## When not to use it

- **A module.** A module is an answer, not a question — use `module-card`.
- **A feature list.** The question is mandatory. A row with a claim where its
  question should be is a row in the wrong component.

## What it refuses

- **A "coming soon" state.** A slot is filled or it is not. Roadmap belongs on
  the module, which can say `soon`; the slot only reports today.
- **A count.** Several modules may fill one slot (`implementation`); they are
  listed in `.slot-fill`, never summarised as a number.
- **Dashes as the only signal.** `.slot-fill` spells the state out in words,
  because a dashed leader is not perceivable to everyone.
- **A second way to draw a slot.** One drawing exists in `design/`, here —
  never a card alongside the index for the same information, and never a
  separate drawing for a slot the reader chooses rather than reads.
- **A `<select>` for the choice.** The native popup escapes both the theme and
  the drawing, and reads as a form control in a section whose whole argument is
  that it is not a form.
- **A "not yet chosen" state.** The choosable index loads with a composition
  already decided. A third empty-ish state would need a third drawing, and a
  slot only reports what was decided.
- **JavaScript for open/close.** `<details name="slot">` is the accordion;
  anything reaching for a script to expand a row is solving an already-solved
  problem.
