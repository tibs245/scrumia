# Feature format

**Status**: active
**Stratum**: business

## In brief

The contextual file catalogue that replaces the monolithic PRD. A feature is a
directory of targeted files, each with a defined reader — not a single
document that grows without bound. Two strata carry it: Business (the *what*)
and App (the *how*, one app each). Two rules keep it from decaying back into
the thing it replaces: a file exists only when it has content, and a spec
never carries its own history. `plugins/scrumia-specs` is the operational
implementation of what this feature specifies.

## Links

- Implemented by: no App feature. The format this feature specifies is enacted by
  `plugins/scrumia-specs` (`scrumia-feature` scaffolds a feature, `scrumia-specs-find`
  walks them), which fills the `specs` slot. The operational catalogue it reads lives
  at `plugins/scrumia-specs/skills/scrumia-feature/references/catalog.md`.

## The catalogue

The rule that governs every row below: **a file is created only when it has
content.** Its absence is an assertion — "nothing to say here" — not an
oversight and not a placeholder. `index.md` is the sole file the format
requires unconditionally: a feature needs one entry point so it can be found
and understood before anything else is opened. Every other file, `qa.md` and
`CHANGELOG.md` included, is subject to the same content test as the rest of
the catalogue — see `business.md` for why the two of them are, in practice,
never actually absent from a real feature.

| File | Business | App Backend | App Frontend |
|---|---|---|---|
| `index.md` | required | required | required |
| `business.md` | the rules themselves | reference to the parent | reference to the parent |
| `qa.md` | the business criteria | this implementation's criteria | this implementation's criteria |
| `CHANGELOG.md` | one entry per notable change | one entry per notable change | one entry per notable change |
| `legal.md` | if personal data, payment, user content, or a regulated sector is at stake | same | same |
| `archi.md` | if the EPIC's implementation touches two or more apps | never | never |
| `api-contract.md` | never | often — the schema it exposes | if it consumes an API |
| `tech.md` | never | often — choices specific to this app | sometimes |
| `ux.md` | never | never | often |
| `a11y.md` | never | never | often, when there is an interface |
| `devx.md` | never | if it exposes a lib or an SDK | if it exposes components |

The catalogue is open: a new file earns its place only if it has a reader no
existing file already serves, and only if its addition is documented where
the catalogue lives operationally
(`plugins/scrumia-specs/skills/scrumia-feature/references/catalog.md`) —
otherwise the next feature invents another name for the same thing, and the
catalogue loses the predictability that makes it useful.

## Files present

| File | Why it exists |
|---|---|
| `business.md` | the two strata, the reference direction, and the two absolute rules |
| `qa.md` | acceptance criteria for a correctly-applied catalogue |
| `CHANGELOG.md` | history of changes to this spec |

No `legal.md`: the format itself processes no personal data, payment, or
regulated content — it is a documentation convention. No `archi.md`: this
feature's own implementation does not touch two or more apps. No
`api-contract.md`, `tech.md`, `ux.md`, `a11y.md`, `devx.md`: none apply to a
documentation convention with no interface or exposed library of its own.

## Open issues

- #2 — [EPIC] Spec the data organisation: the feature format and the monorepo layout (parent)
- #22 — `validate.py`'s link gate doesn't cover `features/`
- #25 — Reconcile `catalog.md` / `format-feature.md` wording with this feature's mandatory-file rule
