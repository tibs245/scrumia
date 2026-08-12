# Changelog — scrumia-core

All notable changes to this module, on [Keep a Changelog 1.0.0](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]
### Added
- `scrumia-extends` — prints the directives that extend one register, for this project:
  name, type, whether it is required, one line of what it says, and the file to open.
  It computes on demand and stores nothing, so there is no artefact to rebuild or to
  find stale. `--list` names every register the installed modules open; `--check`
  reports a declared edge nothing satisfies.
- `scrumia-extend` — the extension protocol itself: what a register is, what the three
  data files a module may ship declare, and how to open an extension point in a skill.
- `dependencies.jsonl` — this module declares the published names it runs, each qualified
  by the source that publishes it (`tibs245/scrumia:scrumia-board`). PATH is one flat
  namespace shared with every enabled plugin, so a bare name says which command and never
  whose; `--check` resolves the name and compares the publisher's own declared source
  against the claim. What a skill invokes stays the bare name.
### Changed
- Both readers of the composition — `scrumia-extends` and `compose-status.sh` — take the
  modules a project runs from `modules:`, a mapping keyed `<source>:<module>`
  (`tibs245/scrumia:scrumia-specs`, `shared:…`, `local:…`). A bare name is reported as not
  a declaration and resolves to nothing, rather than matching whichever module of that
  name happens to be installed. `extends:` and the older `composition:`/`practices:` keys
  are still read for one more minor, with a warning naming the migration.
- `scrumia-extends --settings [<key>]` answers what a module's configuration resolves to:
  `settings:`, then that module's `params:`, then `.scrumia/config.local.yaml`, which is
  per-machine and never committed. The layers that answered are named on stderr, so two
  machines resolving different values can be told apart from a misread file.
- `compose-status.sh` shows each module under its declared key with its `params:`. Its
  migration notices, and the line naming a local layer in effect, moved to stderr: the
  report on stdout is published verbatim on the site and gated by a fixture, so neither a
  migration nor a machine-local override belongs in it.
- `compose-status.sh` reports `extends` and the apps' own lists, and points at
  `scrumia-extends --list` for what each module contributes. The retired
  `composition:`/`practices:` shape is still read, and now says so.
- `scrumia-init` Step 5 states that everything between the `scrumia:start`/`scrumia:end`
  markers is regenerated in full — so a skill must never depend on a hand-written
  sentence there, and a rule that belongs to a module is contributed by that module
  rather than added to the template every project receives.
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
