# Composer — the home page's build-your-composition section

**Status**: active
**Stratum**: app (`site`)

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
  - `features/business/modular-composition/business.md` (BR-2, AC-4) — what
    an empty slot costs
  - `design/components/slot-index/spec.md` — how a slot row is drawn, and its
    choosable state
  - `plugins/scrumia-core/skills/scrumia-init/SKILL.md` — the schema the
    emitted config must match
  - `design/tokens.css` — which values may be used

## Files present

| File | Read it when |
|---|---|
| `business.md` | Checking what a chosen or emptied slot must say, or what the install claim may promise |
| `ux.md` | Changing the composer's rows, states or copy |
| `tech.md` | Touching `composer.js` or the scripting boundary |
| `qa.md` | Verifying the composer against its criteria |
| `api-contract.md` | Changing the emitted `.scrumia/config.yaml` shape |
| `CHANGELOG.md` | Checking the history of this spec |

## Open issues

- #106 — Whether a preset that sets the five process slots should leave
  `implementation` and `practices` untouched, or whether a preset like
  `Solo script` should propose a stack too. A business call, not a design one.
- The `aria-live` delta line announces the slot and its new fill. Whether it
  should also announce the artifacts changing is untested with a real screen
  reader — noted for a follow-up, not guessed at here.
- `--human` on `--ground` is a new contrast pair: the composer is the first
  place a fill carries the human hue. It belongs in `tools/check_contrast.py`.
- run-horizon's own open issue says the legend's promise — *swap a module and
  the line changes shape* — is the composer's to keep, and nothing here keeps
  it yet: `#flow` still draws one fixed reference run regardless of what is
  chosen in `#composer`. The rejected "swap" exploration
  (`design/explorations/swap.html`, retired by #57) carried the idiom this
  would need for an app whose implementation or practices slot the visitor
  leaves empty: a step's module chip drawn `.is-missing` — struck through,
  dashed border, no fill, but its text kept at full contrast rather than
  dimmed, so the absence stays readable rather than fading into the ground.
  Worth reusing verbatim if this ever gets built, rather than re-deriving it.
