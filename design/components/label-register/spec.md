# label-register

The mono, uppercase, faint-tracked typography that names what the nearby
controls are for. It is the register that sits next to a "Start from" row, an
"Additions" section, a declares/register/contributes cell, and the slot names
inside a slot accordion — the typographic move that says *this is a label of
something, not a value of its own*.

Five declarations compose it, and they appear together exactly once, in
`site/assets/style.css` under `.label-register`:

| Declaration | Token |
|---|---|
| `font-family` | `var(--font-mono)` |
| `font-size` | `var(--text-xs)` |
| `letter-spacing` | `var(--tracking-label)` |
| `text-transform` | `uppercase` |
| `color` | `var(--text-faint)` |

The five call sites consume the class and add only their own contextual layout
and (for `.slot-name`) the slot-state colour override:

| Call site | What it adds on top of `.label-register` |
|---|---|
| `.presets-label` | `margin-right: var(--space-1)` |
| `.ext-label` | `display: inline-block; min-width: var(--ext-label-w); flex: none;` |
| `.shelf-label` | `[data-weight="medium"]`; `margin: 0 0 var(--space-2)` |
| `.key-entry-label` | — (the class is the whole rule) |
| `.slot-name` | `[data-size="sm"]`; `color: var(--slot-name-color)`; `width: 9.5rem; flex: none;` |

## The variant API

Two documented variants, both attribute selectors. The selector pair composes —
a label can carry both attributes, and the rules do not collide.

| Attribute | Effect | Carried by |
|---|---|---|
| `data-weight="medium"` | `font-weight: var(--weight-medium)` | `.shelf-label` (an `<h3>` pulling weight down to match the register) |
| `data-size="sm"` | `font-size: var(--text-sm)` | `.slot-name` (the slot row's larger name, so the slot's content reads as one line) |

Attributes are the API because the component will grow — a third variant
(strength, language, anything decided later) composes with the existing two
under the same selector pair, where modifier classes accumulate into a third
positional token each. The site-header's `data-variant="rail"` precedent
answers the same question the same way.

## `.slot-name` colour

The `--slot-name-color` is **not** a token. It is locally scoped on `.slot`
itself, set between `var(--text)` (default slot) and `var(--text-faint)`
(empty slot), and consumed by `.slot-name` via `color: var(--slot-name-color)`.
It is a slot-state response, not a palette decision — `design/tokens.css`
preamble: "a value that cannot be justified from `identity.md` is a value
nobody chose". The empty-slot dimming is the colour carrying meaning, and the
meaning is the slot's emptiness, not the label register's.

## When to use it

Any label that names the row, column, group or control it sits next to. The
register is the deliberate voice for "this is a label" — quiet, mono, set in
the faint colour that says it does not need to be read first.

## When not to use it

- **A heading that does not label a control or row.** A `<h2>` for a section is
  not a label register; it is at `--text-2xl` and carries the section's own
  argument. The `.kicker` on `page-head` is the closest near-relation, and it
  is its own typography (dash before, accent-tinted surface), not the register.
- **A value inline.** A `<code>` element inside a list is a value; setting it
  in the register would say the value is a label of itself, which is what the
  register is *not* for.
- **A button or a link.** The register is a label, not an interactive surface.
  `button` is the component for that.
- **A form `<label>`.** When a `<label>` is paired to a single input by
  `for`/`id`, the label's job is the screen-reader announcement, not the
  visual cue. `.key-entry-label` is the one exception, and even there it sits
  outside the input — the input's own label is the `<label>` element, and the
  register class on it is purely typographic.

## What it refuses

- **A colour variant.** The register is faint and stays faint. Two shades of
  faint is a third place that needs a token; the empty-slot dimming above is
  the one place the colour moves, and it does so on the slot, not on the
  label register.
- **A weight variant beyond `medium`.** A bold weight would say the label is
  the most important thing on the row, which is the row's own argument
  making. The medium weight is the one already on `.shelf-label`; it exists
  to pull an `<h3>` down to the register, not to make a label louder.
- **A second size variant.** Anything smaller than `--text-xs` is too small
  to read; anything between `--text-xs` and `--text-sm` is a rung the
  `tokens.css` scale does not carry, and a rung nobody decided is a rung
  nobody owns.
- **A new restatement of the five declarations.** The component is the whole
  point. A fifth call site that writes the five declarations again is the
  defect this component was added to remove.
