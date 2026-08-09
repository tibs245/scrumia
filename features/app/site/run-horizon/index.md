# Run horizon — the home page's run section

**Status**: active
**Stratum**: app (`site`)

## In brief

The `#flow` section of the home page: one reference run, seven steps, drawn as a
single hairline with human steps standing above it and agent steps hanging
below. It is the only section of the site that encodes the human/agent colour
rule, and the only one that spends `--page-wide`. Under it sit the legend and
the three moments — the same three human steps, named in prose.

Orbit's contribution here was to replace seven boxed columns with a line. The
boxes made the sequence readable and the ratio invisible; the ratio is the
argument.

## Where the authority sits

| Question | Answered by |
|---|---|
| Which hue marks which actor? | `design/identity.md`, decision 1 — inverted by #52 |
| How is a step drawn, and what does it refuse? | `design/components/run-horizon/spec.md` |
| Which values may be used? | `design/tokens.css` — the vocabulary |
| What are the seven steps? | `features/business/dev-flow/index.md` |
| Which direction is this built in? | `design/explorations/orbit.html`, adopted by #53 |

This feature renders the run; it does not define it. A step appearing,
disappearing or changing actor is a `dev-flow` change first, carried here
second.

## The rules this feature owns

**The horizon never scrolls sideways.** Four of seven columns in view is the
three-of-seven ratio telling a lie until the reader drags, and the ratio is the
whole argument. Where seven columns cannot hold two lines, the run turns and
becomes a vertical rail — same marks, same order, same words, nothing cut. That
threshold is `--page-wide` plus the gutters `main` already reserves, and it is
written exactly once in `site/assets/style.css`.

**Copy gives way before layout does.** No `.step-out` runs past two lines, in
either language, at any width. An agent step spends line one on the clause and
line two on the board transition; a human step spends both on the clause, so
the band above the line and the band below it are the same height. French is
the binding language: it runs about 15% longer than the English.

**The run is the only thing on the page allowed past `--page-max`.** It takes
`--page-wide` only where the viewport can pay for the extra out of its own
margins — never out of the page's gutter.

**The split survives without colour.** Three independent signals carry it: the
actor named in words in `.step-who` on *both* variants, the side of the line the
copy stands on, and a filled mark versus a hollow one. The fill is
load-bearing rather than decorative — `--human` and `--agent` sit at nearly the
same luminance in both themes, so two rings would be the same mark in greyscale.

**No wash in this section.** #52 moved coral onto the agent, which is the
abundant actor — four of seven. A wash would make the page's most common state
its loudest, which is the emphasis backwards. Colour is spent on the mark, the
step title and the actor word, and nowhere else.

**One flare on the page, in three instances.** The human mark blooms on arrival,
staggered along the line. Three blooms of one idiom are one flare: each stands
for the same state change — *this step is waiting for you*. The agent marks
never bloom. The limb's rim light is the page's other light and stays legal
because it is standing scenery in the accent, not a transient actor colour;
`design/tokens.css` records that distinction next to `--limb-glow`.

**The legend states the ratio in digits.** `3 of 7` and `4 of 7`, never a
positional phrase: the run is a rail below `--page-wide` and a legend has to be
true at every width.

## Files present

| File | Why it exists |
|---|---|
| `qa.md` | The criteria the run must keep passing — the two-line budget in both languages, the ratio, the greyscale read, the single flare |
| `CHANGELOG.md` | History of changes to this spec |

No `business.md`: the seven steps are `features/business/dev-flow`'s, not this
feature's own. No `ux.md`: `design/components/run-horizon/spec.md` carries the
step anatomy and its refusals, and restating them here would be the second copy
the design contract exists to prevent. No `a11y.md`: the colour-free read is a
rule above and a criterion in `qa.md`, and it is the only accessibility concern
this section raises beyond the shell's.

## Open issues

- #56 — the composer. The legend promises *swap a module and this line changes
  shape*; nothing on the page keeps that promise until the composer does.
- "Sub-issues per context", cut from step 03's copy, has no home on this page.
  It belongs on the `scrumia-github-project` module page — see
  `features/app/site/module-pages/`.
