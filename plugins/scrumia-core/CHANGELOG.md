# Changelog — scrumia-core

All notable changes to this module, on [Keep a Changelog 1.0.0](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]
### Changed
- `/next` and the config `scrumia-init` writes cite the tracker and team modules' published
  names — `scrumia-board`, `scrumia-pick-model` — rather than paths into those modules.
- The config `scrumia-init` writes declares modules through `extends:` — one flat, unordered
  list per project, plus one per app carrying that app's implementation module and its
  practice modules together. **Run `scrumia-init` to convert your `.scrumia/config.yaml`**; it
  reads the old keys and rewrites them, and shows you the conversion before writing it.
  `scrumia-compose` reads and edits the same key.
- **A slot you deliberately set to `null` is dropped by that conversion**, and the new schema
  has nowhere to put it back: `extends` names the modules that are there, so "not chosen yet"
  and "deliberately without" now read the same. The conversion names every dropped `null` in
  its run report — read that report, because nothing records the choice afterwards. Declaring
  an exclusion explicitly is not yet possible and is tracked as its own change.
- A capability nothing covers is reported rather than written into your config as a
  placeholder. `compose-status.sh` does not read `extends:` yet, so on a migrated project it
  calls every module "not declared" and advises adding the slots back as explicit nulls —
  don't. `scrumia-init` and `scrumia-compose` both flag that output as stale and tell you what
  `extends` actually names. This entry goes away with the same change that fixes the script.

### Deprecated
- `composition:`, and the per-app `implementation:` and `practices:` keys. `scrumia-init` still
  reads them, converts them to `extends:` and warns once per run; they are removed no earlier
  than the second release after this one, in a change carrying the breaking signal.

### Fixed
- The per-app `CLAUDE.md` stub `scrumia-init` offers to write cited each module by a
  `plugins/<module>/…` path — a form that does not exist in an installed session and that
  `tools/validate.py` could not see, since it is neither a markdown link nor a script call.
  It now names each module instead, the form AC-11 requires.

## [0.4.0] - 2026-08-10
### Added
- `scrumia-init` — installs or verifies a project's composition: writes `.scrumia/config.yaml`, the specs tree, and the composition table in `CLAUDE.md`.
- `scrumia-compose` — inspects, changes or diagnoses which module fills which slot.
- `/next` — reads the composition and the tracker and says which step of the workflow comes next.
- `compose-status.sh` — prints the active composition as data, so a skill reads it instead of retyping it.

Earlier versions shipped without a changelog; `0.4.0` is the first version this file
describes, and it states what the module carries rather than reconstructing how it got
there. That history is in the repository's git log and its issues.
