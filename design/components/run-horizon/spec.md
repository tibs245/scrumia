# run-horizon

One run drawn as a single line with its steps standing on either side of it.
Replaces `flow-column`, which drew the same run as seven boxes: the boxes made
the sequence readable and the ratio invisible, and the ratio is the argument.

## When to use it

A sequence where **who acts** changes from step to step, and where *how often*
each actor acts is the point.

On the horizon, position carries the split before a word is read — human steps
above the line, agent steps below — so a reader who never gets past the diagram
still leaves with three-of-seven. **That is a property of the horizon, not of the
component.** On the rail there is no above and no below, and the seven marks are
too far apart to take in at once; there the ratio is stated in words above the
run and in digits in the legend, which is why the legend moves to the top of the
rail and back under the horizon. That is accepted, not overlooked.

There is exactly one on the site, in `#flow` on the home page.

Two variants, and there are only two:

| Variant | Class | Means |
|---|---|---|
| Human | `.step.step-human` | a person decides here — blue, **filled** mark, copy above the line |
| Agent | `.step` | an agent runs here — coral, hollow mark, copy below the line |

Four slots inside `.step-body`, all four filled or the step reads as broken:

- `.step-no` — the ordinal, mono, two digits
- `.step-title` — the step, one word where possible
- `.step-out` — what it leaves behind; the board transition, if there is one,
  in a `<b>` that takes its own line
- `.step-who` — the actor, uppercase mono, on **both** variants

## The rules it enforces

**Two lines of `.step-out`, never three.** An agent step spends line one on the
clause and line two on the transition; a human step spends both on the clause.
The two bands are then the same height and the line reads as a horizon rather
than a skyline. At `--page-wide` that is a budget of 22 characters a line, and
French is the language it has to hold in.

**The transition is a board move, not an actor signal.** Steps 01 and 04 carry
no `→` because nothing moves on the board there — 07 carries `→ Done` and is a
human step. The asymmetry is the fact, not an oversight to tidy up.

**It never scrolls sideways.** Four of seven columns in view is the ratio
telling a lie until the reader drags. Where seven columns do not fit, the whole
thing turns and becomes a vertical rail — same marks, same order, same words,
nothing cut. That threshold is `--page-wide` plus the page's own gutters, and it
is written once in `style.css`.

**One flare, three instances.** The human mark blooms on arrival, staggered
along the line. Three blooms of one idiom are one flare: each stands for the
same state change — *this step is waiting for you* — which is what
`design/identity.md` decision 2 asks of any animation. The agent marks never
bloom; what is abundant does not get to flare.

## What it refuses

- **A wash.** Coral marks the abundant actor after #52, and washing four of
  seven columns would make the page's most common state its loudest. Colour is
  spent on the mark, the title, the actor word, and — on the horizon only — the
  rule that ties a human step's copy back to the line, at 45% of `--human`.
  Nothing wider, and nothing that fills an area.
- **A spine drawn in the page's hairline.** The line is the component; drawn in
  `--border` it measures 1.29:1 against the cream ground and reads as one more
  background grid line, weaker than the rules that hang off it. It takes
  `--border-strong`, the token that exists to carry a boundary you have to see.
- **A third actor colour.** Cold is human, warm is agent. A step that fits
  neither is a step described wrong.
- **The accent.** Cyan points at one thing per screen and a diagram is not it.
  `--human` is not a way to smuggle it in either: the two are a hue category
  apart precisely so the human mark never reads as the thing that points.
- **A colour-only distinction.** Three things carry the split independently:
  the word in `.step-who`, the side of the line, and filled versus hollow. The
  last one is load-bearing — `--human` and `--agent` sit at nearly the same
  luminance in both themes, so two rings are the same mark in greyscale.
- **A module label per step.** The old `.fm-mod` named `discovery` on step 02,
  which the slots section three sections down makes a point of *not* having
  installed. A diagram that asserts what the page denies is worse than a
  diagram that says less.
- **More than seven steps.** Seven fit `--page-wide` at two lines each; the
  eighth is a step nobody reads. Split the run instead of widening the line.
