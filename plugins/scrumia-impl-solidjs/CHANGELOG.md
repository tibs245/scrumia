# Changelog — scrumia-impl-solidjs

All notable changes to this module, on [Keep a Changelog 1.0.0](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]
### Fixed
- The opening paragraph is gone. It narrated how this module is composed — an action name
  from a vocabulary that no longer exists, and a claim of authority over apps it does not
  name — none of which a reader needs in order to use the skill. Which registers this
  module contributes to is `extends.json`'s to declare, and `scrumia-extends` reads it.

### Added
- `extends.json` — the six guides and four refusals are contributed to the `implement`,
  `review` and `audit` registers, so a skill applies them without naming this module.

### Changed
- **Breaking — the project override moves to `.scrumia/overrides/scrumia-impl-solidjs.md`,
  from `.scrumia/impl/scrumia-impl-solidjs.md`.** `.scrumia/impl/` and
  `.scrumia/practices/` only ever differed by a category of module that no longer
  exists, so they collapse into one directory
  ([ADR-0024](https://github.com/tibs245/scrumia/blob/main/docs/adr/0024-no-category-of-module.md)).
  A project with an override file must move it; left where it is, it is not read.
- `README.md` — addressed to whoever is deciding whether to run this module, not to the
  agent that already does: what it answers, what it refuses, what it ships.

## [0.4.0] - 2026-08-10
### Added
- The `implementation` slot for SolidJS, plugged in app by app: fine-grained reactivity without defensive memoisation, behaviour-first component tests, feature-based structure.
- `scrumia-solidjs` — the routing index; `scrumia-solidjs-audit` — the audit against it.

Earlier versions shipped without a changelog; `0.4.0` is the first version this file
describes, and it states what the module carries rather than reconstructing how it got
there. That history is in the repository's git log and its issues.
