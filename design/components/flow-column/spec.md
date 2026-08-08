# flow-column

One step of a run, drawn as a labelled column. Several of them side by side, in
`.flowmap`, make the diagram — the idiom the REX deck uses to explain a mechanism
instead of asserting a benefit.

## When to use it

A sequence where **who acts** changes from step to step. That is the whole reason
the component exists: the warm/cold split is the argument, not decoration.

Two variants, and there are only two:

| Variant | Class | Means |
|---|---|---|
| Human | `.fm.fm-human` | a person decides here — coral top edge, coral wash |
| Agent | `.fm.fm-ai` | an agent runs here — cold blue top edge, no wash |

Four slots inside, all four filled or the column reads as broken:

- `.fm-who` — the actor, uppercase mono
- `.fm-title` — the step, two words at most
- `.fm-out` — what comes out; `<b>→ result</b>` on its own line when the step
  moves a card on the board
- `.fm-mod` — which module does it, or `—` when a human does

## When not to use it

- **A list of features.** Columns imply order. Use `.principles` or `.grid`.
- **More than seven steps.** Seven fit `--page-max` without scrolling; the eighth
  is a step nobody sees. Split the run instead of widening the diagram.
- **A single step.** One column is a card wearing a diagram's clothes.

## What it refuses

- **A third actor colour.** Warm is human, cold is agent, and there is no third
  thing. A step that fits neither is a step described wrong.
- **The accent.** Cyan points at one thing per screen and a diagram is not it. The
  column never uses `--accent`.
- **A colour-only distinction.** `.fm-who` names the actor in words, always: the
  human/agent split survives being read by someone who cannot see the hues.
