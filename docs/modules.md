# The modules

Eleven modules exist. Each fills a slot, each can be replaced — except the two slotless ones, `scrumia-core` and `scrumia-rules`, which describe the composition instead of being part of it.

## `scrumia-core` — the kernel

Fills no slot and does nothing on its own. It describes the composition and makes it readable by agents.

| Skill | Role |
|---|---|
| `scrumia-init` | Installs or verifies the composition, generates the `CLAUDE.md` section |
| `scrumia-compose` | Inspects, modifies or diagnoses the composition |

It is the only non-optional module — without it there is no composition, just plugins side by side.

## `scrumia-rules` — no slot either

The rules-hierarchy format itself, not a topic: an **index** an agent reads first and always, **guides** it loads only on demand — one concern each — and **decisions** it loads only when a rule is being challenged. Sits beside `scrumia-core`: any module's knowledge skill, or a project's own conventions, can take this shape once it outgrows a single file — none has to.

| Skill | Role |
|---|---|
| `scrumia-rules` | The format reference: anatomy, navigation, precedence between sections — read first |
| `scrumia-rules-setup` | Scaffolds a project-local section: interview, harvest from code and lint configs, write, register in `CLAUDE.md` |
| `scrumia-rules-update` | Evolves a rule: challenges its decision, refines or supersedes it, updates the guide, logs the change |

**What it assumes**: nothing beyond `scrumia-core`.
**What it costs**: more files per rule — a guide and a decision instead of one paragraph — accepted so loading a rule for one task doesn't reload a whole corpus. Precedence itself is unchanged: **specific beats generic** still means project-local section over implementation module over practice module, per [ADR-0010](adr/0010-cross-cutting-practices.md). See [ADR-0011](adr/0011-rules-hierarchy.md).

## `scrumia-specs` — `specs` slot

Per-feature, TDD-oriented specs. A contextual file catalog instead of a single document.

| Skill | Role |
|---|---|
| `scrumia-specs-setup` | Creates the specs tree |
| `scrumia-feature` | Creates, updates or audits a feature |
| `scrumia-specs-find` | Navigates: finds the rule, walks the dependencies, loads minimal context |

**What it assumes**: specs live in the repo, next to the code.
**What it costs**: more judgment at writing time than with a fixed template.

## `scrumia-github-project` — `tracker` slot

Issues, sub-issues, GitHub Projects columns, branches and PRs.

| Skill | Role |
|---|---|
| `scrumia-project-setup` | Columns, labels, issue templates |
| `scrumia-refine` | Moves a ticket from Backlog to Ready for dev |
| `scrumia-ticket` | Executes a ticket: worktree, spec, code, tests, review, PR |
| `scrumia-review` | Routes a PR review and synthesizes |
| `scrumia-status` | On-demand progress view |

A `PreToolUse` hook blocks the creation of state files in the repo. It only sees `Write`/`Edit` — a Bash redirect is not covered. It narrows the main door, it is not a sandbox.

**What it assumes**: `gh` authenticated, and state outside the repo.
**What it costs**: GitHub dependency, nothing offline.

## `scrumia-teams` — `team` slot

Standing roles and sprint execution.

| Component | Role |
|---|---|
| `agents/scrumia-manager.md` | Board, splitting, routing, cadence — Opus |
| `agents/scrumia-business.md` | Business rules, vocabulary, compliance — Fable |
| `agents/scrumia-tech.md` | Architecture, contracts, debt, quality — Fable |
| `scrumia-team-setup` | Configures active roles, their models, escalation |
| `scrumia-sprint` | Prepares a sprint and consumes it as dynamic workflows |

Roles are enabled, disabled and added through configuration. Disabling a role is a documented trade-off, not a degradation.

## `scrumia-discovery` — `discovery` slot

Scoping an idea.

| Skill | Role |
|---|---|
| `scrumia-brainstorm` | Challenges an idea until it can be split |
| `scrumia-split` | Splits into features, creates the issues, ships the specs on a branch |

## `scrumia-impl-rust` — `implementation` slot

How we code in Rust: invalid states made unrepresentable, `Result` at the boundaries, typed errors per layer, one test per invariant.

| Skill | Role |
|---|---|
| `scrumia-rust` | The reference, loaded before writing Rust code in a covered app |
| `scrumia-rust-audit` | Measures the gap between an existing app and the rules |

**What it assumes**: nothing beyond Cargo.
**What it costs**: opinionated — `unwrap` refused, single-implementer traits refused; it says so and says why.

## `scrumia-impl-solidjs` — `implementation` slot

How we code in SolidJS: fine-grained reactivity without React reflexes, behaviour-first component tests, structure by feature.

| Skill | Role |
|---|---|
| `scrumia-solidjs` | The reference, loaded before writing SolidJS code in a covered app |
| `scrumia-solidjs-audit` | Measures the gap between an existing app and the rules |

**What it assumes**: Vitest available; Playwright if journeys are wanted.
**What it costs**: refuses habits imported from React, even comfortable ones.

## `scrumia-practice-tdd` — `practices` slot

Test-driven development, situated for an agent. Refines one point of the implementation contract: **how we test**.

| Skill | Role |
|---|---|
| `scrumia-tdd` | The reference: the cycle, the mock boundary, AC-to-test mapping |
| `scrumia-tdd-audit` | The state of an app's test safety net |
| `scrumia-tdd-refactor` | Puts a zone under test before touching it |

## `scrumia-practice-solid` — `practices` slot

The SOLID principles, each with its application limit. Refines one point of the implementation contract: **which design principles**.

| Skill | Role |
|---|---|
| `scrumia-solid-principles` | The reference: the five principles and their limits, in OO and functional alike |
| `scrumia-solid-audit` | Violations **and** over-applications, on equal footing |
| `scrumia-solid-refactor` | Resolves one finding, in safe steps |

## `scrumia-practice-tanstack-query` — `practices` slot

TanStack Query as the answer to server state. Refines one point of the implementation contract: **how server state is fetched, cached and mutated**. One rule underneath it all: every query goes through a `queryOptions()` factory built on a key from a centralized `queryKeys.ts` — never an inline `queryKey`/`queryFn` pair.

| Skill | Role |
|---|---|
| `scrumia-tanstack-query` | The reference: query keys, `queryOptions()`, `useQuery` through testing, as guides loaded on demand |

**What it assumes**: a stack TanStack Query ships an adapter for (React, Solid, Vue, Svelte, Angular).
**What it costs**: a caching model to learn — this is not "just fetch"; the audit and refactor skills that would measure and close the gap on an existing codebase are not built yet, see [the roadmap](roadmap.md).

## How `implementation` and `practices` compose

Both slots are multiple and map app by app. The implementation module owns the stack-specific "how"; a practice module owns one cross-cutting answer (how we test, which design principles) shared across stacks. The implementation module **situates** each practice for its stack — `scrumia-rust` explains what red-green looks like when the compiler is part of the safety net; `scrumia-solidjs` explains what SOLID means for components.

One precedence rule: **specific beats generic**. Implementation module over practice, project override (`.scrumia/impl/`, `.scrumia/practices/`) over both. See [ADR-0010](adr/0010-cross-cutting-practices.md).

Consumption doesn't mean loading every module's full reference. Following the rules-hierarchy format ([ADR-0011](adr/0011-rules-hierarchy.md)), a knowledge skill's `SKILL.md` stops carrying content directly and becomes an **index**: a routing table (task phrasing → guide) plus a decisions table, with the actual content split into `guides/` (loaded on demand, one concern each) and `decisions/` (loaded only when a rule is challenged). An agent reads the index first, then opens only the guide its task routes it to — not the whole corpus. `scrumia-rules` (see above) is that format itself, plus the tooling to scaffold and evolve a project-local section in the same shape.

## Slots without a module

**`design`** — a module building on Claude Design, reachable from Claude Code through the `DesignSync` tool and the `/design-sync` skill. Sketched in [`modules-implementation.md`](modules-implementation.md), not implemented.

## Possible compositions

| Situation | Composition |
|---|---|
| Personal script, one app | `core` + `specs` |
| Project in exploration | `core` + `specs` + `discovery` |
| Framed backlog, in production | all, plus one implementation module per app |
| Team already on Jira | `core` + `specs` + a tracker module to write |
| Stable code conventions | everything except `implementation` |
| Legacy code to bring under test | add `scrumia-practice-tdd`, start with its audit |

## Adding a module

A new module is justified when **a real project would want to fill that slot differently**. Otherwise, it's one more skill in an existing module.

1. Create `plugins/scrumia-<name>/` with its `.claude-plugin/plugin.json`
2. Fill a slot — existing, or new and documented
3. Document the settings read under `settings.<slot>`
4. Provide its `CLAUDE.md` line
5. Add the marketplace entry, then `claude plugin validate`

And the prohibition that matters: **never assume another module is present**. If a capability is missing, say so and propose the next step, rather than failing.

## Modules under consideration

- **`scrumia-ceremonies`** — fact-fed retrospective, refactoring session, debt audit. Paced differently: one-off, human-triggered.
- **`scrumia-migrate`** — convert an existing project to the specs format. Used only once.
- **`scrumia-tracker-local`** — a file-based tracker for projects without a remote. Would fill the same slot as `scrumia-github-project`, with the opposite trade-off — and writing it is the real test that the `tracker` slot is replaceable.
- **`scrumia-practice-hexagonal`** — ports-and-adapters as a practice module, refining "how the code is structured". A candidate third practice once the first two have survived a pilot.
