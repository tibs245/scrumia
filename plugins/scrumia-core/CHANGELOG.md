# Changelog — scrumia-core

All notable changes to this module, on [Keep a Changelog 1.0.0](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]
### Added
- `scrumia-extends --modules` — every module the project declares, with the location it
  actually resolved from and the directory it resolved to. A declaration nothing answers
  is reported as an absence naming where it would have come from, which is the ordinary
  state of a clone without a machine's shared checkouts, and is not a failure.

- `scrumia-place` — one tree from something just learned to exactly one destination: a
  module, this project, a feature, a ticket, the change itself, or agent memory. Memory is
  bounded by the handover test — *would this survive being handed to someone else,
  usefully?* — applied to what an entry says and never to the directory it sits in, so a
  committed memory directory exempts nothing in it. It reminds after the write; it
  intercepts nothing.
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
- **Breaking.** `scrumia-extends` now looks for each source in its own place, all three in
  one pass: `<owner>/<repo>` through the harness's PATH, `shared` under the directory
  `SCRUMIA_SHARED_DIR` names in `.scrumia/.env.local`, `local` at
  `.scrumia/modules/<module>/`. A `local:` or `shared:` key stops binding whichever
  marketplace module carried the name — which it used to do, reporting it as local. A
  project relying on that declares the marketplace source instead.
- A declaration two distinct modules both answer is a conflict: it binds neither, is named
  with both directories wherever it is reached, and fails `--check`. Two routes to one
  directory are one module. A declaration naming no location — the retired list shape —
  answered in several is a shadow: the narrowest wins, is used, and is reported with the
  fix, so promoting a module never disables it.
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
- `README.md` — addressed to whoever is deciding whether to run this module, not to the
  agent that already does: what it answers, what it refuses, what it ships.
- `scrumia-place` routes a discussion to an existing issue before creating one: it searches
  issues in every state, never the board — something settled has left the board — and
  a new issue carries the label the tracker declares so the readings that count work
  subtract it. With no tracker in the composition it names the gap and writes nothing.
  `/next` recommends on what is waiting to be started, discussions excluded.

## [0.4.0] - 2026-08-10
### Added
- `scrumia-init` — installs or verifies a project's composition: writes `.scrumia/config.yaml`, the specs tree, and the composition table in `CLAUDE.md`.
- `scrumia-compose` — inspects, changes or diagnoses which module fills which slot.
- `/next` — reads the composition and the tracker and says which step of the workflow comes next.
- `compose-status.sh` — prints the active composition as data, so a skill reads it instead of retyping it.

Earlier versions shipped without a changelog; `0.4.0` is the first version this file
describes, and it states what the module carries rather than reconstructing how it got
there. That history is in the repository's git log and its issues.
