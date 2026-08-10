# UX — Run horizon

## Screen / flow

The `#flow` section of the home page, between the hero and the composer section.
Entry point: scrolling into view, or the `#flow` anchor. Nothing here is a
control — the section is read, not acted on. The legend and the three moments
sit directly under the run.

## Composition

- The run — `.run`, one instance on the page — per
  `design/components/run-horizon/spec.md`: the two variants, the two-line copy
  budget, and everything it refuses (scrolling sideways, a wash, more than one
  flare, a colour-only split, a third actor colour). None of that is restated
  here.
- `.run-legend`, directly under the run on the horizon and moved above it on
  the rail: states the ratio in digits — `3 of 7`, `4 of 7` — never a
  positional phrase such as "above the line", because the rail has no line to
  be above and the legend has to stay true there too.
- The three moments below the legend: the same three human steps, named in
  prose.

## Interface constraints

- The run is the only element on this page allowed past `--page-max`
  (`design/tokens.css`): it spends `--page-wide` only where the viewport can
  pay for the extra out of its own margins, never out of the page's gutter.
- The actor split must survive a reader who cannot tell the human blue from
  the agent coral, or a greyscale printout of the page: `.step-who` names the
  actor in words on every step, and the mark is filled versus hollow rather
  than two colours of ring — the anatomy that carries this is
  `design/components/run-horizon/spec.md`'s refusal of a colour-only
  distinction. Tested by `qa.md` AC-3.
