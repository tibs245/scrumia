# Changelog — scrumia-core

All notable changes to this module, on [Keep a Changelog 1.0.0](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]
### Added
- `scrumia-assemble` — builds, prints and checks the composed assemblies: one file per
  action naming which module's fragment to open, in an order it computes rather than
  one an author typed. `load` reads a built file and refuses when its inputs moved,
  rather than recomputing an answer at call time.
- `composition.json` and `scrumia-core-manifest` — this module describes itself by a
  name another module can run, instead of being described from outside.
- `data/actions.json` — the kernel's closed action vocabulary. Providers are declared
  by each module, never listed here.
### Changed
- `compose-status.sh` reports `extends` and the project's own `actions:` answers. The
  retired `composition:`/`practices:` shape is still read, and now says so.
- `/next` and the config `scrumia-init` writes cite the tracker and team modules' published
  names — `scrumia-board`, `scrumia-pick-model` — rather than paths into those modules.

## [0.4.0] - 2026-08-10
### Added
- `scrumia-init` — installs or verifies a project's composition: writes `.scrumia/config.yaml`, the specs tree, and the composition table in `CLAUDE.md`.
- `scrumia-compose` — inspects, changes or diagnoses which module fills which slot.
- `/next` — reads the composition and the tracker and says which step of the workflow comes next.
- `compose-status.sh` — prints the active composition as data, so a skill reads it instead of retyping it.

Earlier versions shipped without a changelog; `0.4.0` is the first version this file
describes, and it states what the module carries rather than reconstructing how it got
there. That history is in the repository's git log and its issues.
