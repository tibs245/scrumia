# Acceptance criteria — Slot index

One scenario per rule in `index.md`. Each scenario must be able to fail.

## Nominal

### AC-1 — The index reads and opens with JavaScript disabled

```gherkin
Given a reader with JavaScript disabled, or whose script failed to run
When the home page loads and they activate a row's summary
Then all seven rows and their names, questions and fills are readable
And the activated row's answer opens, and the previously open row closes,
  entirely through the browser's native `<details name="slot">` behaviour
```

### AC-2 — The empty state is stated in words, not only in stroke style

```gherkin
Given the `discovery`, `implementation` and `practices` rows, which are empty
  in this repo's real composition
When any of them is read, with or without colour vision
Then its `.slot-fill` reads `nothing installed`, and its dashed leader is a
  reinforcement of that word, never the only signal
```

### AC-3 — Exactly one slot component exists in `design/`

```gherkin
Given `design/components/`
When it is searched for a component that draws a slot
Then `slot-index/spec.md` is the only spec doing so, and it carries the
  card's own refusals (no "coming soon", no count, no dashes-only signal,
  no JavaScript for open/close)
And `slot-card/spec.md` no longer exists — migrated, not duplicated
```

## Edge cases

### AC-4 — Keyboard-operable, focus visible, both themes

```gherkin
Given a reader operating by keyboard alone
When they tab to a row's summary and press Enter or Space
Then the row opens, a visible focus ring is drawn around the summary in both
  the light and dark themes, and the same holds for every one of the seven
  rows
```

## Out of scope

- What the seven slots are, and their questions — owned by
  `features/business/modular-composition/index.md`.
- Retiring `design/components/slot-card/preview.html` and its Claude Design
  card — #57.
