# slot-card

One slot: the question a capability answers, and what currently answers it.

## When to use it

To show a composition — which capabilities exist and what fills them. The card
carries four things, in this order, and the order is the argument: the slot's
name, its **question**, the answer in prose, and the module that supplies it.

| State | Class | Reads as |
|---|---|---|
| Filled | `.slot` | solid border, accent name, module in the footer |
| Empty | `.slot.slot-empty` | dashed border, muted name, `nothing installed` |

## Why the empty state is drawn rather than omitted

A missing card says "we forgot". A dashed card says "we decided". ScrumIA's whole
position on absent capabilities — agents are told the capability is missing and
say so instead of improvising it — is only legible if the absence has a shape.
That makes `.slot-empty` load-bearing, not a courtesy variant.

## When not to use it

- **A module.** A module is an answer, not a question — use `module-card`.
- **A feature list.** The question is mandatory. A slot-card with a claim where
  its question should be is a card in the wrong component.

## What it refuses

- **A "coming soon" state.** A slot is filled or it is not. Roadmap belongs on the
  module, which can say `soon`; the slot only reports today.
- **A count.** Several modules may fill one slot (`implementation`, `practices`);
  they are listed in `.slot-fill`, never summarised as a number.
- **Dashes as the only signal.** `.slot-fill` spells the state out in words,
  because a dashed border is not perceivable to everyone.
