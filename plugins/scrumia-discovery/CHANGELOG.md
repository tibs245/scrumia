# Changelog — scrumia-discovery

All notable changes to this module, on [Keep a Changelog 1.0.0](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]

## [0.4.1] - 2026-09-10
- `scrumia-split` step 4 — a ticket is created with the footprint at the grain a split can
  know: apps, what it creates for the units after it, what it reuses (#476).
### Added
- `registers.json` and `dependencies.jsonl` — this module opens the `scope-idea` and
  `split` registers, and both skills ask what this project scopes against.

### Changed
- `README.md` — addressed to whoever is deciding whether to run this module, not to the
  agent that already does: what it answers, what it refuses, what it ships.

## [0.4.0] - 2026-08-10
### Added
- The `discovery` slot: scope an idea before it becomes a ticket.
- `scrumia-brainstorm` — challenges a brief until it is ready to be split.
- `scrumia-split` — turns a scoping into a feature tree and the matching issues.

Earlier versions shipped without a changelog; `0.4.0` is the first version this file
describes, and it states what the module carries rather than reconstructing how it got
there. That history is in the repository's git log and its issues.
