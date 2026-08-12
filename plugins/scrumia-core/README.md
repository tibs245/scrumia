# scrumia-core

The kernel: describes a project's active composition, its configuration, and the shared
conventions every other module builds on. Fills no slot of its own — every other module
can build on it, none has to.

## What it answers

Which modules are plugged into this project, what each one owns, and what governs the
file you are about to touch — answered by reading `.scrumia/config.yaml` and the
marketplace's own manifests on demand, rather than by memorizing a table that goes stale.

## What it refuses

- No capability of its own. It describes the composition; it does not run a board, write
  a spec or hold a design system — those are the slots other modules fill.
- No hardcoded path into another module. A cross-module reference goes through a name
  published on `PATH` (`scrumia-board`, `scrumia-pick-model`) or through the extension
  protocol's own tables, never a relative path into a sibling plugin.
- No silent rewrite. `scrumia-init` reports drift on a re-run rather than overwriting what
  a project already decided.

## What it ships

| Skill | Role |
|---|---|
| `scrumia-init` | Installs or verifies a project's composition: `.scrumia/config.yaml`, the specs tree, and the composition table in `CLAUDE.md`. |
| `scrumia-compose` | Inspects, changes or diagnoses which module fills which slot. |
| `scrumia-extend` | The extension protocol itself — what a register is, what the three data files a module may ship declare, and how a skill opens an extension point. |
| `scrumia-extends` | Published on `PATH`. Prints, for one register, every directive the installed modules contribute — name, type, required or not, one line, the file to open. `--list` names every open register; `--modules` says where each declared module resolved from, of the three places one may live; `--check` reports a declared dependency nothing satisfies. |
| `/next` | Reads the composition and the tracker, and recommends the next workflow step. Recommends; launches nothing. |

## Settings it reads

`.scrumia/config.yaml` itself — `project.name`, `project.repo`, `extends`, and each app's
`name`/`path`/`type`/`extends`. The schema is `scrumia-init`'s.

## What it expects to find

A git repository; `jq`; either `yq` or `python3` with PyYAML, to parse the config. A
`gh`-authenticated remote if the tracker slot is filled by a GitHub-based module —
degrades to "no issues, no board" rather than failing if it isn't.
