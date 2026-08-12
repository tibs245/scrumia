# Acceptance criteria — Extends map

One scenario per rule in `business.md` and `ux.md`. Each scenario must be able to fail.

## Nominal

### AC-1 — The mechanism is shown, not asserted

```gherkin
Given the `#extends` section as rendered
When it is read
Then it shows a skill declaring a register, more than one module contributing to that
  register, and a table of real directives — and the claim that a project extends without
  forking is nowhere stated as a bare assertion unaccompanied by the mechanism producing
  it
```

### AC-2 — Every name shown is one this repository runs

```gherkin
Given the section's figure and its table
When each module, register and directive named in them is checked against this
  repository's composition
Then all of them exist, and none is illustrative
```

### AC-3 — The empty register appears

```gherkin
Given at least one register in this repository carrying no contribution
When the section is rendered
Then that state is shown and stated in words as a legitimate outcome, not omitted and not
  drawn only as an absence of lines
```

### AC-4 — The reader can reach the reference and the slot section

```gherkin
Given a reader who has finished the section
When they look for how to write a contribution
Then the section points at where that is explained rather than explaining it, and a path
  exists from here to the slot section and back
```

## Constraints

### AC-5 — Legible with no script

```gherkin
Given JavaScript disabled
When the section is loaded
Then the claim, the figure and the table are all present and readable, and nothing in the
  section requires interaction to be understood
```

### AC-6 — Both themes, through tokens

```gherkin
Given the page rendered in each theme
When the figure is inspected
Then it carries no literal colour, spacing or duration of its own, every value it uses
  comes from `design/tokens.css`, and every stroke and label remains legible in both
```

### AC-7 — The figure contains its own overflow

```gherkin
Given a viewport narrower than the figure's natural width
When the page is displayed
Then the figure scrolls within its own container and the page body does not scroll
  horizontally
```

### AC-8 — The figure is not the only carrier

```gherkin
Given a reader who cannot see the figure
When the section is read as text
Then the four things the figure makes visible are each stated in the section's prose or
  in the figure's text alternative, and that alternative describes the mechanism rather
  than the shapes
```

## Drift

### AC-9 — A changed mechanism makes this section wrong, and something says so

```gherkin
Given a change to what `features/business/modular-composition/` states about registers,
  contributions or rendering order
When the site is built
Then the mismatch surfaces — the section is not merely out of date, it is stating
  something no longer true, and it is treated as a defect rather than as pending work
```

### AC-10 — No number that rots silently

```gherkin
Given the section as written
When it is checked for claims about the composition
Then any count of registers, modules or directives is generated with the page, and no
  such count is hard-written into the prose
```
