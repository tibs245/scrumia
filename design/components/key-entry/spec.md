# key-entry

One field that takes a **whole qualified key** — `<source>:<module>` — where the
source is typed as part of the answer rather than picked beside it.

Introduced for the composer's additions block (#298), where a visitor names a
module the site has never heard of.

## When to use it

When the answer you need is one identifier whose parts are a grammar, not
separate questions. The grammar is the picker: `local:acme-docs-rules`,
`shared:acme-conventions`, `tibs245/scrumia:scrumia-rules`.

Reach for it when all three hold:

- The value is one string with an internal shape a reader can be taught by
  example.
- The set of valid prefixes is **open** — a control that enumerates them would
  need an `other…` escape, which is the second field this component exists to
  avoid.
- The answer may legitimately be *absent a part*, and that absence must be
  refusable. A picker always has a value, so it can never produce "stated no
  source", and a refusal that can never fire is not a rule.

## Anatomy

`label` · `field` · `refusal`, in that order, as a grid inside its parent.

| Part | Class | Register |
|---|---|---|
| Label | `.key-entry-label` | `--font-mono`, `--text-xs`, `--tracking-label`, uppercase, `--text-faint` — the label register `.presets-label` already wears |
| Field | `.key-entry-field` | `--font-mono`, `--text-sm`, `--text` on `--surface-sunken`, `--border-strong` at `--radius-sm` |
| Refusal | `.key-entry-refused` | the **gap idiom** — see `slot-index/spec.md` |

**The label is mandatory and may not be the placeholder alone.** A placeholder
vanishes on the first keystroke, so a field labelled only by one is unlabelled
for everyone who has begun to answer, and for every assistive technology from
the start. The placeholder's job is different and also mandatory: it carries one
complete, valid, real-shaped specimen, because one specimen teaches the grammar
faster than a sentence can.

The grammar is taught a third time, in words, wherever the component is used —
in the composer, in the option's own description. Teaching it there rather than
inside the component is deliberate: the sentence states the *refusal rule before
it can fire*, and that belongs beside the decision, not beside the box.

## States

| State | Reads as |
|---|---|
| Resting | absent — `display: none` until whatever reveals it says so |
| Revealed | the field arrives with `fill-in`, the shelf's own keyframe: a thing that appears because you asked for it is summoned |
| Refused | `aria-invalid="true"` — dashed border, the `--human` wash withdrawn from the enclosing option, and the gap-idiom line in words |

**Empty is not refused.** A revealed field nobody has typed into is unanswered.
Painting it as an error is how a composition starts reading as a form.

**Refusal fires on blur and clears on the next keystroke.** Validating per
keystroke tells a visitor their correctly-typed key is wrong for its first six
characters — the field calling them wrong mid-word.

## Why the refusal carries no colour

`design/tokens.css` has no error token and must not gain one for this. Every
token that could carry a refusal names something else: `--human` is a person
deciding, `--agent` is an agent running, `--ok` is a success, `--accent` is the
one thing on a screen that points. A refusal is none of the four, and inventing
a fifth semantic hue would put a second pointer on a page whose identity
decision 4 is *one accent*.

What it wears instead is stronger than a colour anyway. **Dashed already means
"a decided absence"** in this system — it is the empty slot's leader, and
`slot-index/spec.md` says why: *"A missing row says we forgot. A dashed leader
says we decided."* A key that will not be emitted is exactly a decided absence.
Withdrawing the `--human` wash says the decision did not land. And the words
carry the message, so the reading survives colour-blindness, a monochrome
screenshot, and WCAG 1.4.1 with two channels to spare.

## What it refuses

- **A source picker beside the field.** Two controls collecting one answer is
  the name-plus-origin pairing [ADR-0021](https://github.com/tibs245/scrumia/blob/main/docs/adr/0021-modules-keyed-by-source.md)
  rejected, and `slot-index` already refuses a `<select>` in a section arguing
  it is not a form. An open prefix set cannot be enumerated anyway.
- **A label that is only a placeholder.** See above; this is the refusal the
  component was specified around.
- **Echoing what the visitor typed.** The refusal states the rule — *a key needs
  its source* — never *"‹whatever they pasted›" is invalid*. That removes the
  whole class of arbitrary-user-text-in-narrow-prose defects at the source, and
  it is better copy: it tells the visitor the thing they do not know.
- **A component-local focus ring.** The global `:focus-visible` already draws
  `--focus-width` of `--accent` at `--radius-sm`, which is this field's own
  radius. A second focus treatment is a second language.
- **A UA-default input.** Background, border, radius, font family, font size and
  colour are all set explicitly. An input keeping its browser chrome is the one
  thing in a composition-not-a-form section that genuinely reads as an OS form.
- **Being the section's resting state.** It is revealed by a decision — a
  checked option, an opened row — never standing empty from load.

## Constraints a later edit must not undo

- **`min-width: 0` on the wrapper and the field.** A text input's intrinsic
  min-content width is about 20ch; in a `1fr` grid track that overflows its
  parent below roughly 420px. This is the component's real overflow risk.
- **`width: 100%` on the field must keep beating `.opt input`'s `16px`.** It
  does today by specificity, not by source order — assert it if the selectors
  are ever reorganised.
- **`autocapitalize="none"`.** Without it iOS Safari turns `local:` into
  `Local:` and refuses a visitor who typed the right answer.
- **A length cap** (`maxlength`), as plausibility rather than security. The
  longest real key in this repository is 46 characters.

## When not to use it

- **A choice between known alternatives.** That is a shelf of options —
  `slot-index`'s choosable state.
- **Free prose.** This takes an identifier with a grammar. A field that accepts
  anything has nothing to refuse, and the refused state is half this component.
- **Anything that must work without script.** Text cannot become a structured
  value through `:has()`, so this component is gated on `.has-js` and is
  *absent* without it, never present-and-inert.
