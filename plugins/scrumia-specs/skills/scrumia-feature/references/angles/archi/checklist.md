# Review guard-rails: archi

## Lifespan

- The file contains a decision that survives the EPIC. Apply the test: if the EPIC
  ships and closes, does this still have value? If yes, it is an ADR — move it and
  cite it from here.
- The EPIC is closed or abandoned and the file is still there. It should have been
  deleted with it; every day it stays, it is read as current architecture.
- The file has quietly become the app's general architecture document, with content
  no longer scoped to this EPIC.

## Scope

- It exists on an App feature. This angle is Business-stratum only.
- It exists on a Business feature implemented by a single app. That app's internal
  complexity is `tech.md`'s.
- It describes a flow that never leaves one app's boundary.

## Content

- A schema is copied here instead of the `api-contract.md` that owns it being
  cited.
- The contracts at stake are named without paths, so nobody can follow them.
- Deployment order is stated as a sequence with no consequence attached — nobody
  knows whether it matters.
- No degraded mode is described, in an EPIC where one app can plainly be down while
  the other is up.
- A business rule appears here rather than in `business.md`.

## Hygiene

- A ticket, issue or PR number appears.
- The previous integration is described alongside the current one.
