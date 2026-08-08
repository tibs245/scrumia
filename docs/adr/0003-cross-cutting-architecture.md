# ADR-0003 — Cross-cutting architecture: `archi.md` in the EPIC + project ADR

**Status**: accepted — 2026-08-07

## Context

When an EPIC touches several apps (an authentication overhaul = backend + frontend + mobile), you need an overall view: how the apps talk to each other, which contracts are at stake, what deployment order. That view doesn't fit in any App feature taken in isolation.

Three options were open:

- **A** — an `archi.md` in the EPIC feature
- **B** — a cross-cutting architecture file, outside `features/`
- **C** — each App feature's `tech.md`, plus an ADR under `docs/`

## Decision

**A and C, with a clear boundary: lifespan.**

- **`archi.md` in the Business EPIC feature** — how the apps talk to each other **for this EPIC**. Contracts at stake, data flows, deployment order, degraded modes. This document dies with the EPIC.
- **ADR in `docs/adr/`** — a structural decision that outlives the EPIC. "We're going event-driven between backend and worker" is an ADR, not an `archi.md`.

The test to decide: *if the EPIC is shipped and closed, does this document still have value?* Yes → ADR. No → `archi.md`.

**B is rejected.**

## Consequences

**What we gain**

- The cross-cutting document is loaded exactly when you work on the EPIC, because it lives in its directory.
- It dies with it, instead of piling up.
- Durable decisions live in a single, dated, chronological place, which is already the convention.

**What we accept**

- *A decision can be misfiled at the moment it's made*: what looked local becomes structural. The remedy is simple — promote it to an ADR, leave a pointer in the `archi.md`. The Technical Lead watches for this case in review.
- *A very long EPIC produces an `archi.md` that ages.* It stays bounded by the EPIC, which is enough to contain the problem.

## Rejected alternative

**B — a cross-cutting architecture file outside `features/`.** That's exactly the monolithic PRD relocated: a single document, read in full every time, growing without bound, where no one knows anymore which part is authoritative. That's the flaw ScrumIA exists to fix.
