# Changelog — scrumia-core

All notable changes to this module, on [Keep a Changelog 1.0.0](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]
### Changed
- `/next` and the config `scrumia-init` writes cite the tracker and team modules' published
  names — `scrumia-board`, `scrumia-pick-model` — rather than paths into those modules.
- The config `scrumia-init` writes declares modules through `extends:` — one flat, unordered
  list per project, plus one per app carrying that app's implementation module and its
  practice modules together. A module you did not choose is absent from the list rather than
  present as `null`, so what nothing covers is now stated in the composition report instead of
  as a placeholder in your config. `scrumia-compose` reads and edits the same key.

### Deprecated
- `composition:`, and the per-app `implementation:` and `practices:` keys. `scrumia-init` still
  reads them, converts them to `extends:` and warns once per run; they are removed no earlier
  than the second release after this one, in a change carrying the breaking signal.

## [0.4.0] - 2026-08-10
### Added
- `scrumia-init` — installs or verifies a project's composition: writes `.scrumia/config.yaml`, the specs tree, and the composition table in `CLAUDE.md`.
- `scrumia-compose` — inspects, changes or diagnoses which module fills which slot.
- `/next` — reads the composition and the tracker and says which step of the workflow comes next.
- `compose-status.sh` — prints the active composition as data, so a skill reads it instead of retyping it.

Earlier versions shipped without a changelog; `0.4.0` is the first version this file
describes, and it states what the module carries rather than reconstructing how it got
there. That history is in the repository's git log and its issues.
