# flow-column

One step of a run, drawn as a labelled column. Several of them side by side, in
`.flowmap`, make the diagram — the idiom the REX deck uses to explain a mechanism
instead of asserting a benefit.

## When to use it

A sequence where **who acts** changes from step to step. That is the whole reason
the component exists: the cold/warm split is the argument, not decoration.

Two variants, and there are only two:

| Variant | Class | Means |
|---|---|---|
| Human | `.fm.fm-human` | a person decides here — blue top edge, blue wash |
| Agent | `.fm.fm-ai` | an agent runs here — warm coral top edge, no wash |

The wash marks the human and stays there. It is the *rare* actor — three of the
reference run's seven steps — and marking the rare one is what makes the diagram
readable at a glance. Washing four columns coral would make the page's most common
state its loudest, which is the emphasis backwards.

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

- **A third actor colour.** Cold is human, warm is agent, and there is no third
  thing. A step that fits neither is a step described wrong.
- **The accent.** Cyan points at one thing per screen and a diagram is not it. The
  column never uses `--accent` — and `--human` is not a way to smuggle it in: the
  two are a hue category apart precisely so the human column never reads as the
  thing that points.
- **A colour-only distinction.** `.fm-who` names the actor in words, always: the
  human/agent split survives being read by someone who cannot see the hues.
