# Architecture decisions

Each ADR freezes a decision, its reasoning and what was rejected. An accepted ADR is never modified: write a new one that replaces it, and mark the old one as *superseded by*.

**A decision *not* to build something is a decision, not an absence of one.** A no-new-slot or no-split call at the composition level belongs here, not only in `../modules.md`'s candidate list, which registers intent but reasons about nothing. [0013](0013-tracker-stays-one-slot.md) is the pattern: an explicit *"Reopen this when…"* list and a *"what we accept"* naming who is blocked by the deferral. A feature's own boundary — a capability this feature will not grow into, stated as an enduring rule of what it is — can instead live in that feature's `business.md`, as `features/business/ceremonies/`'s *"Refactor session — dropped"* does: it holds because it is the feature's current shape, not a history of the debate. What does not survive there is a *rejected alternative*'s reasoning argued in passing — a spec carries only its current version (`CLAUDE.md`, *Shared rules*), so an argument not restated as the feature's shape is gone on the next edit, with nothing left recording it was ever weighed.

| # | Decision | Status |
|---|---|---|
| [0001](0001-distribution-as-plugins.md) | Distribution as native Claude Code plugins | accepted — one accepted cost superseded by [0017](0017-version-bump-and-commit-signal.md) |
| [0002](0002-standing-roles.md) | Three standing roles, without depending on agent teams | accepted |
| [0003](0003-cross-cutting-architecture.md) | `archi.md` in the EPIC + project ADRs | accepted |
| [0004](0004-feature-splitting.md) | Feature splitting criterion | accepted |
| [0005](0005-validation-gates.md) | Validation gates and autonomy levels | accepted |
| [0006](0006-ticket-routing.md) | Ticket routing by measurable scope | superseded by [0015](0015-scope-measures-reach.md) |
| [0007](0007-single-base-repo.md) | A single base repo | accepted |
| [0008](0008-state-lives-in-github.md) | State lives in GitHub | accepted |
| [0009](0009-documented-composition.md) | Documented composition, no dynamic resolution | accepted — amended by [0019](0019-extends-replaces-composition-and-practices.md) and [0020](0020-skill-extension-protocol.md) |
| [0010](0010-cross-cutting-practices.md) | Cross-cutting practices as composable modules | superseded by [0019](0019-extends-replaces-composition-and-practices.md) |
| [0011](0011-rules-hierarchy.md) | A rules hierarchy for knowledge skills | accepted |
| [0012](0012-specs-contract.md) | The specs contract: documented, not hard-coded | superseded by [0016](0016-global-feature-index.md) |
| [0013](0013-tracker-stays-one-slot.md) | The `tracker` slot stays one slot, for now | accepted |
| [0014](0014-roles-ship-with-their-capability.md) | A standing role ships with the module that gives it something to guard | accepted |
| [0015](0015-scope-measures-reach.md) | The scope axis measures reach, not medium | accepted |
| [0016](0016-global-feature-index.md) | The specs contract gains a global index; keys stop freezing values | accepted |
| [0017](0017-version-bump-and-commit-signal.md) | What a version bump promises, and the commit signal it derives from | accepted |
| [0018](0018-modules-reach-by-name.md) | A module reaches another by a published name, never by a path | accepted — extended by [0020](0020-skill-extension-protocol.md), second mechanism amended by [0022](0022-a-skill-carries-the-doc-it-needs.md) |
| [0019](0019-extends-replaces-composition-and-practices.md) | `extends` replaces `composition:`, and folds `practices` into it | accepted — its `extends:` key superseded by [0021](0021-modules-keyed-by-source.md) |
| [0020](0020-skill-extension-protocol.md) | A skill is extended by data, and the table is computed when asked | accepted |
| [0021](0021-modules-keyed-by-source.md) | `modules` keyed by source, with a settings cascade | accepted — its `<owner>/<repo>` source-row clause superseded by [0023](0023-source-key-comes-from-the-manifest.md) |
| [0022](0022-a-skill-carries-the-doc-it-needs.md) | A skill carries the doc it needs, and `docs/` points inward | accepted — amends [0018](0018-modules-reach-by-name.md) |
| [0023](0023-source-key-comes-from-the-manifest.md) | A module's `<owner>/<repo>` source is its manifest's claim, not the marketplace | accepted |

## Scope of the decisions

Not all carry the same weight. Some commit the whole project, others commit only one module — and a module can be replaced.

| Scope | ADR |
|---|---|
| **The project** | 0001 (distribution), 0007 (single repo), 0009 (composition) |
| **The `team` module** | 0002 (standing roles), 0005 (gates), 0015 (routing, superseding 0006) |
| **The `specs` module** | 0003 (cross-cutting architecture), 0004 (splitting) |
| **The `tracker` module** | 0008 (state outside the repo), 0013 (one slot, for now) |
| **The `design` module** | 0014 (a role ships with its capability) |
| **The `implementation` slot, plus `scrumia-core`** | 0011 (rules hierarchy — its `practices` citations point to 0019 pending a housekeeping pass) |
| **The `specs` module, plus its consumers (`tracker`, `discovery`, `team`) and `scrumia-core`** | 0016 (specs contract, superseding 0012) |
| **The project** — every module it ships, and every project consuming one | 0017 (what a version bump promises, and the commit signal) |
| **The project** — every module it ships | 0018 (a module reaches another by name, refining 0009) |
| **The project** — every project's `.scrumia/config.yaml` | 0019 (`extends` replaces `composition:`, folding in the `practices` slot, superseding 0010) |
| **The project** — every module it ships, and what an agent reads before acting | 0020 (a skill is extended by data, amending 0009 and extending 0018) |

A module decision is contested by writing another module, not by debating this one.

## To revisit first

- **0002** — when agent teams leave experimental status, in particular if nested teams or session resumption appear
- **0004** — after three real projects, with the feature sizes actually observed
- **0009** — if a project changes modules frequently on the same slot
- **0011** — if the three-concern floor for staying single-file proves wrong once real modules have gone through the migration
- **0016** — if a specs module ships with a fundamentally different shape (no per-feature catalog) than the seven-key vocabulary assumes
- **0013** — as soon as a project needs its issues in one tool and its PRs in GitHub; that case is blocked until the slot splits
- **0018** — if the harness stops putting every enabled plugin's `bin/` on the session PATH, or publishes a contract that supersedes the observation this rests on
- **0017** — when the first module reaches `1.0.0`, which lifts the `0.x` shift; or the first time a type in daily use is missing from its vocabulary, since admitting one takes a superseding ADR
- **0020** — if the harness publishes a contract for plugin PATH, or withdraws the behaviour: this one and 0018 move together
- **0022** — if a doc turns out to be needed unchanged by several modules at once, ask `module-authoring`'s threshold question — whether it is a module of its own — not whether the direction was right
- **0019** — if folding `practices` into `extends` loses an override granularity a project actually needed, that is #184's "rule addressability" wave, not a reason to reopen 0019
- **0020** — if two modules opening the same register turns out to be legitimate, the check that reports it moves first

## Format

Context → Decision → Consequences (what we gain / what we accept) → Rejected alternatives.

The "what we accept" section is not optional. A decision without a stated cost has not been examined.
