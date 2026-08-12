# Changelog — scrumia-teams

All notable changes to this module, on [Keep a Changelog 1.0.0](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]
### Added
- `registers.json` and `dependencies.jsonl` — this module opens the `convene` and `sprint`
  registers, and declares the names it runs, qualified by their source. `scrumia-standup` picks up a role another module ships from the `convene`
  register rather than from a list it maintained about modules it does not own.
### Changed
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
