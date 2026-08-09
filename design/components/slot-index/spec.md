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
- **A count.** Several modules may fill one slot (`implementation`,
  `practices`); they are listed in `.slot-fill`, never summarised as a number.
- **Dashes as the only signal.** `.slot-fill` spells the state out in words,
  because a dashed leader is not perceivable to everyone.
- **A second way to draw a slot.** One drawing exists in `design/`, here —
  never a card alongside the index for the same information.
- **JavaScript for open/close.** `<details name="slot">` is the accordion;
  anything reaching for a script to expand a row is solving an already-solved
  problem.
