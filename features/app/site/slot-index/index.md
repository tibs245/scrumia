# Slot index — the home page's composition section

**Status**: active

## In brief

The `#slots` section of the home page: the seven questions `modular-composition`
defines, each row showing what currently answers it in this repo's own
`.scrumia/config.yaml` — or that nothing does. Orbit's contribution here was to
replace a grid of eight cards with one typographic index: name, question, dotted
leader, fill, with the answer opening in a native `<details name="slot">`.

## Links

- Business parent: none. `features/business/modular-composition/index.md` names
  its own mechanism as implemented by no App feature — this feature renders that
  business concept without being its implementation.
- Authority:
  - `features/business/modular-composition/index.md` — what a slot is, and
    which seven exist
  - `design/components/slot-index/spec.md` — how a slot row is drawn, and the
    refusals that keep it the only drawing (no card alongside it, no script for
    open/close)
  - `design/tokens.css` — the vocabulary of values this feature may use

## Files present

| File | Read it when |
|---|---|
| `ux.md` | Checking which rows may appear, and the empty state's wording rule |
| `tech.md` | Checking why no script opens or closes a row |
| `qa.md` | The criteria the index must keep passing — no-JS, the empty state, one component, keyboard and both themes |
| `business.md` | Checking the value this section brings, or why the business rule is `modular-composition`'s, not this feature's own |
| `CHANGELOG.md` | History of changes to this spec |
