# Slot index — the home page's composition section

**Status**: active
**Stratum**: app (`site`)

## In brief

The `#slots` section of the home page: the seven questions `modular-composition`
defines, each row showing what currently answers it in this repo's own
`.scrumia/config.yaml` — or that nothing does. Orbit's contribution here was to
replace a grid of eight cards with one typographic index: name, question, dotted
leader, fill, with the answer opening in a native `<details name="slot">`.

## Where the authority sits

| Question | Answered by |
|---|---|
| What is a slot, and which seven exist? | `features/business/modular-composition/index.md` |
| How is a slot row drawn? | `design/components/slot-index/spec.md` |
| Which values may be used? | `design/tokens.css` — the vocabulary |

This feature renders the business concept; it does not define it. A slot's name
or question changing is a `modular-composition` change first, carried here
second.

## The rules this feature owns

**Exactly seven rows, no eighth example.** Every row is one of the project's
real slots, read from `.scrumia/config.yaml` at the time this was written —
`specs`, `tracker`, `team`, `discovery`, `implementation`, `practices`, `design`.
None is illustrative; a made-up "and if you leave a slot empty?" row would be
exactly the kind of claim `design/identity.md`'s "mechanism over claim" rule
exists to block.

**An empty row states its emptiness in words.** `.slot-fill` reads
`nothing installed`, never only a dashed leader — a stroke style alone is not
perceivable to everyone.

**No JavaScript opens or closes a row.** `name="slot"` groups the seven
`<details>` elements into one native accordion; opening one closes the last,
entirely through the browser's own semantics.

**One drawing of a slot.** `slot-index` is the only component in `design/` that
draws a slot; the card it replaces (`slot-card`) carries no spec of its own
after this feature landed — see `design/components/slot-index/spec.md` for
what was carried forward from the card's refusals.

## Files present

| File | Why it exists |
|---|---|
| `qa.md` | The criteria the index must keep passing — no-JS, the empty state, one component, keyboard and both themes |
| `CHANGELOG.md` | History of changes to this spec |

No `business.md`: the business rule is `modular-composition`'s, not this
feature's own. No `ux.md`: the interaction is fully specified by
`design/components/slot-index/spec.md`'s row anatomy, and restating it here
would be the second copy the design contract exists to prevent.

## Open issues

- #57 — retires `design/components/slot-card/preview.html` and its Claude
  Design card. Left for that ticket on purpose: it batches with the removal of
  the other unchosen explorations.
