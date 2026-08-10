# Feature format

**Status**: active

## In brief

The contextual file catalogue that replaces the monolithic PRD. A feature is a
directory of targeted files, each with a defined reader — not a single
document that grows without bound. Two strata carry it: Business (the *what*)
and App (the *how*, one app each). The operational catalogue lives in
`plugins/scrumia-specs/skills/scrumia-feature/references/catalog.md`; the
rules it implements are in `business.md`.

## Links

- Implemented by: no App feature — purely technical, enacted by
  `plugins/scrumia-specs` (`scrumia-feature` scaffolds a feature,
  `scrumia-specs-find` walks them), which fills the `specs` slot.
- Authority: `plugins/scrumia-specs/skills/scrumia-feature/references/catalog.md`
  — the operational catalogue: each file's three-part boundary, the three
  existence categories, the membership tests.

## Files present

| File | Read it when |
|---|---|
| `business.md` | the two strata, the reference direction, and the absolute rules for this format |
| `qa.md` | acceptance criteria for a correctly-applied catalogue |
| `CHANGELOG.md` | history of changes to this spec |

No `legal.md`: the format itself processes no personal data, payment, or
regulated content — it is a documentation convention. No `archi.md`: this
feature's own implementation does not touch two or more apps. No
`security.md`: a documentation convention carries no risk on any of the four
axes. No `api-contract.md`, `tech.md`, `ux.md`, `devx.md`: none apply to a
documentation convention with no interface or exposed library of its own.

