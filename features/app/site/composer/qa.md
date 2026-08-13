# Acceptance criteria — Composer

One scenario per rule in `ux.md`, `tech.md`, `business.md` and `api-contract.md`. Each scenario must be able to fail.

## Nominal

### AC-1 — The composer shows a composition assembling, not a form being filled

```gherkin
Given the `#composer` section of the home page
When it is inspected
Then it draws seven rows with `slot-index`'s anatomy — sign, name, question,
  leader, fill — one per slot of `modular-composition`, and no `<fieldset>`,
  `<legend>` or step number survives
And every row's fill restates the current composition, so answering a question
  changes what the index says rather than adding to a list of answers
```

### AC-2 — Leaving a slot empty is offered as a choice, and its consequence is stated

```gherkin
Given any of the seven slots
When its row is opened
Then a `leave it empty` option is among its choices, and its description states
  what that absence costs — a named degradation, never a claim that the agents
  break
And when it is chosen, the row falls to the empty state — muted name, dashed
  leader, `nothing installed` in words — and the emitted YAML carries the same
  consequence as a comment: standing where the module would have been keyed for
  the five slots the project declares, and on the empty mapping of an app left
  with no module of its own
```

Every comment starts with `#`, and the marker is asserted rather than assumed:
one that lost it would not read as a weaker statement of the cost, it would be
parsed as configuration. A project-level comment is the whole of its line; the
one an emptied app carries trails its `modules: {}` on the same line, and loses
that line to a parse error rather than to a misreading.

An app that keeps an implementation module but no practice carries no separate
comment. The mapping it does carry already names what runs, and this feature
takes a note asserting a second thing is absent, beside a key stating what is
present, to be worth less than the noise it adds to every app block. The two
per-app slots reach the file through that mapping or not at all.

### AC-3 — The output is copyable and carries the shape ADR-0021 defines

```gherkin
Given a composition chosen in the composer
When the two artifacts are read
Then the install block lists `/plugin install` for exactly the modules the
  seven rows name, and the config block carries `project:`, a `modules:` mapping
  carrying one `<source>:<module>` key per module those rows chose, and one
  `apps[]` entry per chosen stack with `name`, `path`, `type` and its own
  `modules:` mapping
And no key is emitted for a slot left empty, and no key is a bare name
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
When a slot's module is named by no key of the `modules:` mapping
Then a row of the composer offered that absence and the visitor or a preset
  selected it — in particular `design`, which has its own row rather than a
  silent default
And the absence is stated as a comment in the mapping rather than left to the
  mapping's silence, which reads the same whether a slot was refused or forgotten
```

The comment is verified on the option that causes it, not on a generated file:
the composition the page loads with answers every slot, so no absence is ever
pre-rendered to read. What is checked is that every option offering an absence
carries the note the file will carry — the failure being guarded against is an
option that emits silence, and that is decidable at the option.

`a tracker of your own` is an absence for today and not a refusal: what was
chosen is a future presence, so its comment names the gap and the next step
rather than a decision to go without.

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

### AC-9 — A composition can be extended past the seven slots

```gherkin
Given a visitor who has answered the seven slots
When they look for a module that adds a capability without replacing any of them
Then the composer offers the modules that fill no slot, stated as additions rather
  than as an eighth slot, and picking one changes both artifacts it takes away —
  the install commands, and one more key in the `modules` mapping of the config
And leaving every addition unpicked is a complete composition, not an unanswered
  question
And the block carries no sign, no leader, no fill and no `<details>` — it is a
  shelf of options, drawn as the body of a slot row without the row
```

The seven rows are choices between alternatives; an addition is not. The last
clause is not styling: `design/components/slot-index/spec.md` refuses *"a row with
a claim where its question should be"* and refuses a second way to draw a slot, so
three of the row's five cells would have nothing true in them. `.shelf` and `.opt`
are what the seven rows already open into, so the shelf reads as continuous with
them without impersonating one.

### AC-10 — A visitor's own module reaches the config, and only the config

```gherkin
Given a visitor who runs a module this site has never heard of
When they name it in the additions block, choosing its source
Then it appears in the emitted `modules` mapping keyed `<source>:<module>` like
  every other entry, per
  [ADR-0021](../../../../docs/adr/0021-modules-keyed-by-source.md)
And no install command is emitted for it — the site cannot know how to install what
  it does not ship, and saying so is what keeps the other commands trustworthy
And an entry whose key does not match `<source>:<module>` is refused rather than
  emitted
And a key a chosen module already put in the mapping is emitted once, while the
  same name under a different source stands beside it
```

The location is not a second answer to collect: it is the `<source>:` half of the
key, so the entry is one field with an inline source choice, never a name plus a
separate origin — that pairing is what ADR-0021 rejected.

### AC-11 — The free entry is script-gated, and absent without script

```gherkin
Given the home page with JavaScript disabled
When the additions block is rendered
Then the free entry is not present, while every other choice in `#composer` — the
  seven rows and the shelf of known additions — still works through `:has()` alone
Given the page with script
Then the free entry appears as the last option of the shelf and reveals its field
  only when checked, so the section's resting state contains no empty box
```

Text cannot become YAML through `:has()`. Without the gate a no-JS visitor meets a
field that silently does nothing under seven rows that all work — the precedent for
the fix is two rules away, `.presets { display: none } .js .presets { … }`.

Siting it as the last `.opt` is what keeps AC-1 true: a free-text field is a
stronger form signal than the `<select>` `slot-index` already refuses, and an empty
box in the resting state would make the section read as a form being filled rather
than a composition assembling. The field is a component this site does not have
yet — `design/components/` must carry it before it is written, and its label may
not be the placeholder alone.

A custom **slot** is deliberately absent, and not as an omission: the configuration
carries no slot key for one to be written into. A visitor wanting their own step
contributes a directive to a register — `features/business/local-extension/` BR-3 —
which needs no module and no slot at all.

## Out of scope

- What the seven slots are, their questions, and what an absent capability
  means — owned by `features/business/modular-composition/`.
- The `#slots` section that reports this repo's own composition — owned by
  `features/app/site/slot-index/`.
- The captured `compose-status.sh` output in `#install`, a different section
  of the home page.
- The run section — owned by `features/app/site/run-horizon/`.
