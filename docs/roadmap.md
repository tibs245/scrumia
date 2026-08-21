# Roadmap

## Done — design and skeleton (2026-08-07)

- [x] Composable-slot architecture, twelve decisions documented as ADRs
- [x] `scrumia-core` kernel: configuration, composition, generation of the `CLAUDE.md` section
- [x] `scrumia-specs` — per-feature TDD-oriented specs, with navigation
- [x] `scrumia-github-project` — refinement, execution, review, tracking, anti-state hook
- [x] `scrumia-teams` — three configurable roles, sprints as dynamic workflows
- [x] `scrumia-discovery` — scoping producing issues and a specs branch
- [x] `scrumia-impl-rust` and `scrumia-impl-solidjs` — the first two implementation modules
- [x] `scrumia-tdd` and `scrumia-solid-principles` — cross-cutting modules, per app ([ADR-0010](adr/0010-cross-cutting-practices.md), superseded by [ADR-0019](adr/0019-extends-replaces-composition-and-practices.md))
- [x] `scrumia-tanstack-query` — TanStack Query for server state; reference skill only, audit and refactor below
- [x] Rules hierarchy adopted ([ADR-0011](adr/0011-rules-hierarchy.md)): knowledge skills restructured into index + guides + decisions, with the slotless `scrumia-rules` module providing the format and its scaffold/update tooling
- [x] Bilingual English/French site
- [x] `LICENSE`, `tools/validate.py`, CI validation workflow
- [x] Validation: 11 plugins and the marketplace pass, 29 skills and 3 agents load
- [x] Repo fully in English

## Next milestone — validate on a pilot project

The only step that can invalidate the design.

- [ ] Pick a real personal project, preferably with ≥2 apps — **ScrumIA itself is a candidate**: initializing the repo on its own method is the cheapest test of `scrumia-init`, the hook and the full flow
- [ ] `scrumia-init`, fix whatever sticks
- [ ] Scope one unit of value, refine it, run a sprint of 3 to 5 tickets
- [ ] Measure: context consumed per ticket, actual human time, rejected PRs and why

What the pilot must settle:

- Does the composition documented in `CLAUDE.md` hold without drifting from the configuration? → ADR-0009
- Do the splitting thresholds match reality? → ADR-0004
- Does the `scope/*` grid classify correctly? → ADR-0015
- Is running two parallel sessions workable? → ADR-0002
- Does refinement produce tickets that are actually executable on the first try?
- Do the modules an app draws on actually change what agents produce? → ADR-0010

## Then — harden

- [ ] Publish the repo (`git init`, push to `tibs245/scrumia`), enable Pages and the CI
- [ ] Pin the marketplace entries by `sha` at the first stable tag
- [x] Real issue templates in `scrumia-project-setup` — shipped as `templates/ISSUE_TEMPLATE/*.yml`, copied into `.github/ISSUE_TEMPLATE/` at setup instead of described in prose
- [x] Board wiring: `scrumia-ticket` moves the card through the columns, `scrumia-status` reads the real board, `scrumia-refine` moves `Backlog` → `Ready for dev` — concrete `gh project`/`jq` commands and the IDs they need now live in `scrumia-status/references/projects-v2.md`; **the pilot must still confirm the commands against a real Projects v2 board**, this closes the "under-specified" gap, not the "unverified against GitHub" one
- [ ] `scrumia-tanstack-query` — audit and refactor skills, closing the loop the reference skill opened
- [x] Decide each ghost setting (`settings.specs.root`, `paths.adr`, `settings.team.sprint.parallel`): make it read, or remove it — all three removed from `scrumia-init`'s (or `scrumia-team-setup`'s) template, no reader existed for any
- [x] Team config schema divergence: `scrumia-init` and `scrumia-team-setup` disagreed on the shape of `settings.team` (a plain string list vs. objects with `enabled`/`model`) — unified on the object shape, `scrumia-team-setup` now states `scrumia-init` as the schema's writer instead of redefining it
- [x] `gh` failure branches specified: `scrumia-ticket`, `scrumia-status`, `scrumia-refine`, `scrumia-review` and `scrumia-project-setup` each now name the concrete recovery for "not authenticated", "network/API error" and "no repo or remote", instead of leaving the failure mode implicit
- [x] Worktrees relocated to `.worktrees/<type>/<n>-<slug>` inside the project directory (was `../<repo>-<n>`, outside Claude Code's permission scope) — `scrumia-project-setup` gitignores the directory
- [x] Hook false positives: `no-state-files.sh` now exempts `docs/*` and `.scrumia/*` before matching on basename, so `docs/notes/TODO.md` is allowed while a root `TODO.md` is still blocked

## Later — extend

- [ ] **`scrumia-design`** — build on `DesignSync` and the `/design-sync` skill
- [x] **`scrumia-ceremonies`** — not built. The retrospective and the debt audit are specified in `features/business/ceremonies/` and enacted through the plugged-in modules; the refactor session is dropped, its only artefact being the PR a ticket already produces
- [ ] **`scrumia-tracker-local`** — a file-based tracker, to prove that the `tracker` slot is actually replaceable
- [ ] **`scrumia-hexagonal`** — ports-and-adapters, once the first two survive the pilot
- [ ] Re-examine [ADR-0002](adr/0002-standing-roles.md) if agent teams leave experimental status

The `scrumia-tracker-local` module has a particular value: as long as a single module occupies a slot, nothing proves that slot is truly replaceable.

## Out of scope, and why

- **Support for tools other than Claude Code** — the lock-in is what makes it possible to maintain no installer.
- **A CLI** — [ADR-0001](adr/0001-distribution-as-plugins.md).
- **A capability registry with dynamic resolution** — [ADR-0009](adr/0009-documented-composition.md).
- **A single method** — that is the opposite of the intent. Every answer is a module.
