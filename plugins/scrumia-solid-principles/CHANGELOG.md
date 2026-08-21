# Changelog — scrumia-solid-principles

All notable changes to this module, on [Keep a Changelog 1.0.0](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]
### Added
- `extends.json` — the five principles and the over-application refusal are contributed
  to the `implement`, `review` and `audit` registers.

### Changed
- **Breaking — this module is now `scrumia-solid-principles`, renamed from `scrumia-practice-solid`.**
  There is no category of module and no vocabulary naming one, so the prefix that
  named one is gone ([ADR-0024](https://github.com/tibs245/scrumia/blob/main/docs/adr/0024-no-category-of-module.md)).
  A project that installed the old name has an unresolved key until it updates
  `.scrumia/config.yaml` and reinstalls; the marketplace carries no redirect.
- Its configuration is read from this module's own `params:`, through
  `scrumia-extends --settings`, like every other module's.
- `README.md` — addressed to whoever is deciding whether to run this module, not to the
  agent that already does: what it answers, what it refuses, what it ships.

### Deprecated
- `settings.practices.scrumia-solid-principles` and `.scrumia/practices/scrumia-solid-principles.md` — read for now.
  Use this module's own `params:` and `.scrumia/overrides/scrumia-solid-principles.md`; both retired
  names go in the release that closes the window
  [`release-versioning`](https://github.com/tibs245/scrumia/blob/main/features/business/release-versioning/business.md) fixes.

## [0.4.0] - 2026-08-10
### Added
- SOLID, applied app by app: each principle with the limit past which applying it costs more than it saves.
- `scrumia-solid-principles`, `scrumia-solid-audit`, `scrumia-solid-refactor` — the reference, the audit for violations *and* over-applications, and the refactor.

Earlier versions shipped without a changelog; `0.4.0` is the first version this file
describes, and it states what the module carries rather than reconstructing how it got
there. That history is in the repository's git log and its issues.
