# Changelog — scrumia-teams

All notable changes to this module, on [Keep a Changelog 1.0.0](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]
### Added
- `registers.json` and `dependencies.jsonl` — this module opens the `convene` and `sprint`
  registers, and declares the names it runs, qualified by their source. `scrumia-standup` picks up a role another module ships from the `convene`
  register rather than from a list it maintained about modules it does not own.
### Changed
- `scrumia-pick-model` resolves the execution policy through `scrumia-extends --settings`,
  the composition's three-layer cascade, instead of reading `settings.team.execution` out of
  `.scrumia/config.yaml`. A matrix cell overridden in `.scrumia/config.local.yaml` now
  actually changes the answer, and a project that has moved the block into this module's
  `params:` keeps working — both shapes are read and merged key by key while the migration
  is in flight, the migrated key winning **within a layer**; across layers the cascade's
  order decides, so a machine still writing `settings.team.execution` outranks a repository
  that has migrated. This module names that nest when it asks rather than leaving
  `scrumia-core` to guess it — through `scrumia-extends --legacy`, so **this release
  requires the `scrumia-core` that ships it**; against an older one it stops and names what
  it could not resolve rather than answering a model. The key its `params:` sit under comes from the
  project's own declaration, so a `local:` or `shared:` source resolves like a marketplace
  one.
- `scrumia-pick-model` answers **no model at all** when no layer carries a grid — including
  when `scrumia-core` is absent from the session — instead of falling back to `unlabeled`
  and returning a plausible model name nobody configured. A grid with a hole in one cell is
  unchanged: that is data, and it still answers. The values around the grid (`unlabeled`,
  `unrated_risk`, the label prefixes) keep their built-in defaults, and each one that stands
  in is now named on stderr.
- `scrumia-core` is now load-bearing for this module: `scrumia-extends` was already declared
  in `dependencies.jsonl`, but a project that ran this module without it used to get answers
  anyway. It now stops. Nothing that composes correctly is affected; a composition that was
  quietly incomplete finds out.
- The execution-policy tool is published as the name `scrumia-pick-model`, which the harness
  puts on the session's PATH, and every skill and role runs that name instead of a path.
  Reaching it by path only ever worked in this module's own repository: installed, the module
  sits one version segment deeper and the path resolved to nothing at all.
- `scrumia-sprint` reads the board by the tracker module's published name rather than by a
  path into it, and says what to do when the name is not found — never read the board by hand.
- Every link into this repository's ADRs and specs is an absolute URL: a relative one assumed
  a consuming project had files it has never had.
- `README.md` — addressed to whoever is deciding whether to run this module, not to the
  agent that already does: what it answers, what it refuses, what it ships.

### Deprecated
- `settings.team.execution` in `.scrumia/config.yaml` — this module's policy moves into its
  own `params:` under the `modules:` mapping (ADR-0021). Both shapes are read and merged key
  by key, so a project migrates one key at a time; the retired nest is removed at the second
  release after the one shipping this, and this module stops naming it before `scrumia-core`
  stops accepting the name. `settings.team.roles` is unaffected — it declares the team, not
  this module's configuration.
- `scripts/pick-model.sh` — kept as a shim that warns and delegates. It is removed at the
  second release after the one shipping this; run `scrumia-pick-model`.

## [0.4.0] - 2026-08-10
### Added
- The `team` slot: standing roles and sprint execution.
- The `manager`, `business` and `tech` standing roles.
- `scrumia-standup` — convenes the roles without starting anything; `scrumia-sprint` — runs a batch of ready tickets, one isolated worktree each; `scrumia-team-setup` — configures which roles run on which models.
- `pick-model.sh` — answers which model a ticket runs on, so a skill acts on its instruction instead of re-reading the matrix.

Earlier versions shipped without a changelog; `0.4.0` is the first version this file
describes, and it states what the module carries rather than reconstructing how it got
there. That history is in the repository's git log and its issues.
