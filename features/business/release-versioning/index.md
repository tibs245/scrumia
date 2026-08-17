# Release versioning

**Status**: active

## In brief

What a module's version number promises a project that has already adopted it, and
what moves that number. A module versions on its own, so a bump is a statement about
that module's published surface and nothing else. The signal the bump is derived from
is the commit — its type and its mandatory scope — so this feature owns the mapping
from one to the other, the window a renamed thing keeps working for, and how a project
finds out that something broke.

## Links

- Implemented by: no App feature, and no script today. The rule is documented and
  nothing derives a number from it — see `business.md` § *Nothing computes this yet*.
- Authority: `docs/adr/0017-version-bump-and-commit-signal.md` — the decision, the one
  definition of the type vocabulary, and the rejected alternatives. This feature states
  the live rule; it enumerates the vocabulary nowhere.
- Defers to: `features/business/dev-flow/` for what a commit message must carry and who
  may rewrite a branch. This feature says what the type and scope are *worth*; that one
  says they are mandatory and where they are written.
- Consumed by: `features/business/github-tracking/` for the GitHub spellings of a commit's
  reference to its work item.
- Consumed by: `features/business/modular-composition/` establishes that
  a module can be composed and points here for how it evolves once adopted.

## Files present

| File | Read it when |
|---|---|
| `business.md` | deciding what a bump promises, which bump a change earns, what a module may rename and for how long, or when a project is told |
| `qa.md` | writing or checking a test against one of these rules |
| `CHANGELOG.md` | tracing when a rule here last changed |

No `tech.md` or `api-contract.md`: nothing computes a version today, so there are no
mechanics to specify — a file here would describe a tool that does not exist. No
`legal.md`, `security.md` or `ux.md`: a version number carries no personal data, no risk
surface and no interface.
