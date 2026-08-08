# button

Three of them, and the difference between the first two is how loud they are
allowed to be.

| Variant | Class | Use for |
|---|---|---|
| Primary | `.btn.btn-primary` | the one next step on the screen — accent fill, accent glow |
| Ghost | `.btn.btn-ghost` | every other route out — outline only |
| Copy | `.copy-btn` | a control acting on the thing next to it |

## The one-primary rule

Cyan points, and if two things point neither does. **One `.btn-primary` per
screen** — not per section. A screen with a second one has two next steps, which
means it has none, and the fix is upstream in the copy rather than in the CSS.

`.cta-row` is the only place these appear. A button outside one is a button that
lost its pair.

## When not to use it

- **Navigation.** The header's links are links. A button in the header would claim
  an importance the nav does not have.
- **A command.** `/plugin install …` is copyable text in `.mod-cmd`, not a button;
  see `module-card`.
- **A destructive action.** There is none on this site, and the day there is, it
  gets its own variant rather than a red override of this one.

## What it refuses

- **Size variants.** One size. A button that needs to be smaller is a `.copy-btn`,
  and one that needs to be bigger is a hero that is not carrying its weight.
- **An icon-only form.** Every button says a word. `.theme-btn` is the deliberate
  exception and it carries `aria-label` plus `aria-pressed`.
- **Its own hover colour.** Primary lifts 1px on `--ease-summon`; ghost borrows the
  accent for its border. Neither invents a hue, and both flatten under
  `prefers-reduced-motion`.
