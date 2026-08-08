# Architecture decisions

Each ADR freezes a decision, its reasoning and what was rejected. An accepted ADR is never modified: write a new one that replaces it, and mark the old one as *superseded by*.

| # | Decision | Status |
|---|---|---|
| [0001](0001-distribution-as-plugins.md) | Distribution as native Claude Code plugins | accepted |
| [0002](0002-standing-roles.md) | Three standing roles, without depending on agent teams | accepted |
| [0003](0003-cross-cutting-architecture.md) | `archi.md` in the EPIC + project ADRs | accepted |
| [0004](0004-feature-splitting.md) | Feature splitting criterion | accepted |
| [0005](0005-validation-gates.md) | Validation gates and autonomy levels | accepted |
| [0006](0006-ticket-routing.md) | Ticket routing by measurable scope | accepted |
| [0007](0007-single-base-repo.md) | A single base repo | accepted |
| [0008](0008-state-lives-in-github.md) | State lives in GitHub | accepted |
| [0009](0009-documented-composition.md) | Documented composition, no dynamic resolution | accepted |
| [0010](0010-cross-cutting-practices.md) | Cross-cutting practices as composable modules | accepted |
| [0011](0011-rules-hierarchy.md) | A rules hierarchy for knowledge skills | accepted |
| [0012](0012-specs-contract.md) | The specs contract: documented, not hard-coded | accepted |
| [0013](0013-tracker-stays-one-slot.md) | The `tracker` slot stays one slot, for now | accepted |

## Scope of the decisions

Not all carry the same weight. Some commit the whole project, others commit only one module — and a module can be replaced.

| Scope | ADR |
|---|---|
| **The project** | 0001 (distribution), 0007 (single repo), 0009 (composition) |
| **The `team` module** | 0002 (standing roles), 0005 (gates), 0006 (routing) |
| **The `specs` module** | 0003 (cross-cutting architecture), 0004 (splitting) |
| **The `tracker` module** | 0008 (state outside the repo), 0013 (one slot, for now) |
| **The `practices` slot** | 0010 (cross-cutting practices) |
| **The `implementation` and `practices` slots, plus `scrumia-core`** | 0011 (rules hierarchy) |
| **The `specs` module, plus its consumers (`tracker`, `discovery`, `team`) and `scrumia-core`** | 0012 (specs contract) |

A module decision is contested by writing another module, not by debating this one.

## To revisit first

- **0002** — when agent teams leave experimental status, in particular if nested teams or session resumption appear
- **0004** — after three real projects, with the feature sizes actually observed
- **0009** — if a project changes modules frequently on the same slot
- **0011** — if the three-concern floor for staying single-file proves wrong once real modules have gone through the migration
- **0012** — if a specs module ships with a fundamentally different shape (no per-feature catalog) than the six-key vocabulary assumes
- **0013** — as soon as a project needs its issues in one tool and its PRs in GitHub; that case is blocked until the slot splits

## Format

Context → Decision → Consequences (what we gain / what we accept) → Rejected alternatives.

The "what we accept" section is not optional. A decision without a stated cost has not been examined.
