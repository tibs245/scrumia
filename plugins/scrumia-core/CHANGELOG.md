# Changelog — scrumia-core

All notable changes to this module, on [Keep a Changelog 1.0.0](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]
### Added
- `scrumia-extends` — prints the directives that extend one register, for this project:
  name, type, whether it is required, one line of what it says, and the file to open.
  It computes on demand and stores nothing, so there is no artefact to rebuild or to
  find stale. `--list` names every register the installed modules open; `--check`
  reports a declared edge nothing satisfies.
- `scrumia-module` — states whether one module meets the anatomy standard, from that
  module's tree alone: `scrumia-module check [<path>]`, `--json` for the same verdict
  unrendered. It reads no project config and needs the module installed nowhere, so it
  answers on a module still being written. It writes nothing — no fix, no scaffold. Its
  exit status separates five states a boolean collapses, which `--help` enumerates: read
  `state`, never the length of `findings`, because a non-zero exit is not a finding.
- `scrumia-extend` — the extension protocol itself: what a register is, what the three
  data files a module may ship declare, and how to open an extension point in a skill.
- `dependencies.jsonl` — this module declares the published names it runs, each qualified
  by the source that publishes it (`tibs245/scrumia:scrumia-board`). PATH is one flat
  namespace shared with every enabled plugin, so a bare name says which command and never
  whose; `--check` resolves the name and compares the publisher's own declared source
  against the claim. What a skill invokes stays the bare name.
### Changed
- `compose-status.sh` reports `extends` and the apps' own lists, and points at
  `scrumia-extends --list` for what each module contributes. The retired
  `composition:`/`practices:` shape is still read, and now says so.
- `scrumia-init` Step 5 states that everything between the `scrumia:start`/`scrumia:end`
  markers is regenerated in full — so a skill must never depend on a hand-written
  sentence there, and a rule that belongs to a module is contributed by that module
  rather than added to the template every project receives.
- `/next` and the config `scrumia-init` writes cite the tracker and team modules' published
  names — `scrumia-board`, `scrumia-pick-model` — rather than paths into those modules.
- `README.md` — addressed to whoever is deciding whether to run this module, not to the
  agent that already does: what it answers, what it refuses, what it ships.

## [0.4.0] - 2026-08-10
### Added
- `scrumia-init` — installs or verifies a project's composition: writes `.scrumia/config.yaml`, the specs tree, and the composition table in `CLAUDE.md`.
- `scrumia-compose` — inspects, changes or diagnoses which module fills which slot.
- `/next` — reads the composition and the tracker and says which step of the workflow comes next.
- `compose-status.sh` — prints the active composition as data, so a skill reads it instead of retyping it.

Earlier versions shipped without a changelog; `0.4.0` is the first version this file
describes, and it states what the module carries rather than reconstructing how it got
there. That history is in the repository's git log and its issues.
