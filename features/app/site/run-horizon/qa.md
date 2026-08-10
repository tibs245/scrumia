# Acceptance criteria — Run horizon

One scenario per rule in `ux.md`. Each scenario must be able to fail.

`tools/check_run_horizon.py` is the runnable form of AC-1, AC-2, AC-3 and AC-4's
first scenario: it renders the built pages in headless Chrome at nine widths in
both languages and reads the line counts, the marks, the actor words, the run's
own edges and the legend's digits back out. It is not a spec file, and it exits 2
rather than 0 when it finds no browser — a check that passes because it could not
run is worse than one that is missing.

**AC-4's second scenario is the one thing here no script can prove.** Forcing
reduced motion is exactly what stops the `.js` gate being set, so the code path
that would bloom is never the code path under test. It is verified by reading the
selectors, and the rule it depends on is that every animated descendant of the
run appears in the `prefers-reduced-motion` block in `site/assets/style.css` —
including `.step-dot`, which is a great-grandchild of the `.summon` container and
so is missed by any blanket `> * ` reset.

## Nominal

### AC-1 — No step runs past two lines, in either language, at any width

```gherkin
Given the site built by `tools/build_site.py`
When the run is rendered at every width from 390px to 1920px, in English and in
  French
Then every `.step-title` occupies exactly one line
And every `.step-out` occupies at most two — the clause, and the board
  transition on its own line where there is one
And nothing was cut by widening the layout instead: the copy is what gave way
```

### AC-2 — Three of seven is legible before a word is read

```gherkin
Given the run at a width that fits the horizon
When it is looked at rather than read
Then exactly three marks stand above the line and four hang below it
And nothing horizontal has to be scrolled to see all seven
And below that width the run is a vertical rail carrying the same seven marks in
  the same order, with the same three filled
And the legend states the ratio in digits — `3 of 7`, `4 of 7` — so it stays
  true on the rail, where there is no line to be above
```

## Edge cases

### AC-3 — The split survives being read without colour (a11y)

```gherkin
Given a reader who cannot distinguish the human blue from the agent coral, or a
  greyscale printout of the page
When any step is read
Then `.step-who` names the actor in words on both variants — an agent step is
  labelled `agent`, never left blank
And the human mark is filled where the agent mark is a ring, which is what
  carries the split when the two hues resolve to the same grey
And no step depends on which side of the line it stands on to be understood
```

### AC-4 — Exactly one animated flare, and it stands for a state change

```gherkin
Given the whole home page
When every `@keyframes` in `site/assets/style.css` is inspected
Then exactly one of them animates a `box-shadow`, and it is `bloom`
And the only selector that spends it contains `.step-human`: the three human
  marks pulse on arrival, one idiom in three instances, each standing for the
  same state change — this step is waiting for you
And the agent marks never bloom
And the page's standing lights — the primary control's glow, the limb's rim
  light, Hop's lit eye — are not animated, and so are not flares

Given a reader with `prefers-reduced-motion: reduce`, or with JavaScript disabled
When the run loads
Then no mark blooms, every step is readable from the first frame, and the marks
  are drawn in their resting state
```

## Out of scope

- What the seven steps are — owned by `features/business/dev-flow/`.
- The promise in the legend that swapping a module changes the line's shape:
  #56 is what keeps it.
- The composition output block in `#install` (#64) and the twelve module
  micro-identities (#66), which share these files but not this section.
