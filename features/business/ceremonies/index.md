# Ceremonies

**Status**: active

## In brief

Which occasions beside the ticket path this project keeps, and on what terms — as
distinct from a gate, which decides on one change in flight rather than reading across
several finished ones. `business.md` sets the admission tests and applies them to four
candidates: the retrospective, the debt audit, the refactor session and
`scrumia-sprint`'s closing gather.

## Links

- Implemented by: none — no module and no slot enact this feature; `business.md` §
  *Where the ceremonies live* states why.
- Authority: `features/business/dev-flow/` — owns the two paths and the three gates
  ceremonies sit beside.
- Authority: `features/business/execution-policy/` — owns the deviation record the
  retrospective reads.
- Authority: [`docs/adr/0005-validation-gates.md`](../../../docs/adr/0005-validation-gates.md)
  — defines the gate this feature must not be confused with.

## Files present

| File | Read it when |
|---|---|
| `business.md` | deciding whether a candidate occasion qualifies as a ceremony, or checking why no `ceremonies` module or slot exists |
| `qa.md` | writing or checking a test against a ceremony rule |
| `CHANGELOG.md` | checking what changed here and when |

No `legal.md`: a ceremony reads the project's own records — no personal data, payment,
user content or regulated sector. No `security.md`: neither ceremony changes code or
user-facing behaviour; both read tracker records and write issues or spec edits, so no
axis in the risk grid rates a meaningful surface. No `archi.md`: this feature's
enactment touches neither `site` nor `tools`. No `tech.md`, `api-contract.md`, `ux.md`
or `devx.md`: it specifies occasions and their artefacts, with no interface, no exposed
library and no implementation of its own.

