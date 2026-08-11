# Acceptance criteria — Composer

One scenario per rule in `ux.md`, `tech.md`, `business.md` and `api-contract.md`. Each scenario must be able to fail.

## Nominal

### AC-1 — The composer shows a composition assembling, not a form being filled

```gherkin
Given the `#composer` section of the home page
When it is inspected
Then it draws six rows with `slot-index`'s anatomy — sign, name, question,
  leader, fill — one per question of `modular-composition`, and no `<fieldset>`,
  `<legend>` or step number survives
And every row's fill restates the current composition, so answering a question
  changes what the index says rather than adding to a list of answers
```

### AC-2 — Leaving a slot empty is offered as a choice, and its consequence is stated

```gherkin
Given any of the six rows
When its row is opened
Then a `leave it empty` option is among its choices, and its description states
  what that absence costs — a named degradation, never a claim that the agents
  break
And when it is chosen, the row falls to the empty state — muted name, dashed
  leader, `nothing installed` in words — and the emitted YAML carries the same
  consequence as a comment on the `null`
```

### AC-3 — The output is copyable and matches what `scrumia-init` would verify

```gherkin
Given a composition chosen in the composer
When the two artifacts are read
Then the install block lists `/plugin install` for exactly the modules the
  six rows name, and the config block carries `project:`, a project-level
  `extends:` list naming only the non-empty project-wide rows (an unchosen
  one is absent, never spelled as `null` — `extends` has no per-row key to
  leave empty), and one `apps[]` entry per chosen stack with `name`, `path`,
  `type` and its own `extends:` list carrying that app's implementation
  module and its chosen practices together
And a practice appears only under the apps whose type it applies to
And each artifact has its own copy button, which copies that artifact's text
And with JavaScript disabled both artifacts still show the default
  composition's real output, not an empty block
```

## Edge cases

### AC-4 — Keyboard-operable end to end, both languages, both themes (a11y)

```gherkin
Given a reader operating by keyboard alone
When they tab through the composer
Then every row's summary, every radio and checkbox, and both copy buttons are
  reachable, arrow keys cycle within one slot's radio group and not across
  slots, and a visible focus ring is drawn in both the light and the dark theme
And the same holds on the French page, where every string comes from
  `site/i18n/fr/index.json` and no English text is hard-coded in the template
  or in `composer.js`
```

### AC-5 — The two indexes stay two accordions

```gherkin
Given `#slots` and `#composer`, drawn with the same component two sections apart
When a row is opened in one of them
Then no row closes in the other, because the composer's rows are grouped under
  `name="composer-slot"` and never under `#slots`' `name="slot"`
```

### AC-6 — No slot is answered without being asked

```gherkin
Given the emitted `.scrumia/config.yaml`
When a project-wide module is absent from the `extends:` list
Then a row of the composer offered that choice and the visitor or a preset
  left it empty — in particular `design`, which has its own row rather than a
  silent default
```

### AC-7 — Choosing works with JavaScript disabled

```gherkin
Given a reader with JavaScript disabled
When they open a row and pick an option
Then the row's `<details>` opens on the native toggle, the option's radio or
  checkbox is checked on click alone, and the row's fill updates to the
  chosen option through CSS `:has()` — no state above the pre-rendered
  default artifacts (AC-3) requires script to exist
```

### AC-8 — The composer's fills read as decisions, not reports

```gherkin
Given `#slots` and `#composer` on the same rendered page
When a filled row is inspected in each
Then `#slots`' fill computes to `--text-soft` and `#composer`'s computes to
  `--human`, in both the light and the dark theme
```

## Out of scope

- What the six rows are, their questions, and what an absent capability
  means — owned by `features/business/modular-composition/`.
- The `#slots` section that reports this repo's own composition — owned by
  `features/app/site/slot-index/`.
- The captured `compose-status.sh` output in `#install`, a different section
  of the home page.
- The run section — owned by `features/app/site/run-horizon/`.
