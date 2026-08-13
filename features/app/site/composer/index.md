# Composer — the home page's build-your-composition section

**Status**: active

## In brief

The `#composer` section of the home page: the same seven slots the `slot-index`
feature *reports*, offered as choices. The visitor answers each slot — or leaves
it empty on purpose — and takes away two artifacts: the install commands for the
modules they picked, and the `.scrumia/config.yaml` that declares the
composition.

It is the only place on the site where a visitor does something rather than
reads, which is why it is drawn as a composition assembling rather than as a
form being filled.

## Links

- Business parent: none beyond the site epic. This feature is purely
  technical — the business rules it draws from (what an empty slot costs, the
  no-fabricated-claims rule) belong to `features/business/modular-composition/`
  and are referenced, not copied, from `business.md`.
- Authority:
  - `features/business/modular-composition/index.md` — what a slot is, and
    which seven exist
  - `features/business/modular-composition/business.md` (BR-3) — what an empty
    slot costs, and in whose voice it is said
  - `design/components/slot-index/spec.md` — how a slot row is drawn, and its
    choosable state
  - `design/components/key-entry/spec.md` — how the field taking a whole
    `<source>:<module>` key is drawn, and what it refuses
  - `docs/adr/0021-modules-keyed-by-source.md` — the shape the emitted config
    must carry, and the grammar of every key in it
  - `design/tokens.css` — which values may be used

## Files present

| File | Read it when |
|---|---|
| `business.md` | Checking the value this section brings, what a chosen or emptied slot must say, or what the install claim may promise |
| `ux.md` | Changing the composer's rows, states or copy |
| `tech.md` | Touching `composer.js` or the scripting boundary |
| `qa.md` | Verifying the composer against its criteria |
| `api-contract.md` | Changing the emitted `.scrumia/config.yaml` shape |
| `CHANGELOG.md` | Checking the history of this spec |
