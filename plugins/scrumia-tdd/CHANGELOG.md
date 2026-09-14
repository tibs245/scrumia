# Changelog — scrumia-tdd

All notable changes to this module, on [Keep a Changelog 1.0.0](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]

## [0.5.0] - 2026-09-14
### Added
- `guides/06-test-levels.md` — unit, integration and end-to-end defined by what a test
  needs to run and what it asserts, with the tie-break when the two disagree (an
  in-process screen or route test stays in the unit suite, counted apart as *in-process
  integration*), the invariant-to-level decision table, how each level is written, and
  the dated up-front deferral of end-to-end automation (#480).
- `levels` and `impact` under this module's `params:` — the per-level commands and the
  mapping from changed paths to the integration tests they reach, per app. Every command
  is the project's: no guide or skill of this module carries a stack's test command (#480).
- `extends.json` — the cycle, the mock boundary, the AC mapping and the useless-tests
  catalog are contributed to the `implement`, `review` and `audit` registers; the test
  levels join `implement` and `review`.

### Changed
- `guides/02-mock-boundary.md` — a unit-level double stands at a port we own, over the
  external functionality behind it; "unit tests use doubles" licenses nothing about a
  sibling module, at any level (#480).
- `guides/03-ac-mapping.md` — a criterion is covered at the lowest level that can fail on
  it, and may need more than one level (#480).
- `guides/05-useless-tests-catalog.md` — Rule 7 names the misclassification's twin, a
  unit-level invariant filed in a slow suite, and points at the level definitions (#480).
- `scrumia-tdd-audit` — a seventh pass reports coverage per level and as a union, with
  the union as the headline figure, measures a shared module with every suite that
  exercises it, and sets no threshold; pass 2 counts misclassified tests in both
  directions (#480).

- **Breaking — this module is now `scrumia-tdd`, renamed from `scrumia-practice-tdd`.**
  There is no category of module and no vocabulary naming one, so the prefix that
  named one is gone ([ADR-0024](https://github.com/tibs245/scrumia/blob/main/docs/adr/0024-no-category-of-module.md)).
  A project that installed the old name has an unresolved key until it updates
  `.scrumia/config.yaml` and reinstalls; the marketplace carries no redirect.
- Its configuration is read from this module's own `params:`, through
  `scrumia-extends --settings`, like every other module's.
- `README.md` — addressed to whoever is deciding whether to run this module, not to the
  agent that already does: what it answers, what it refuses, what it ships.

### Deprecated
- `settings.practices.scrumia-tdd` and `.scrumia/practices/scrumia-tdd.md` — read for now.
  Use this module's own `params:` and `.scrumia/overrides/scrumia-tdd.md`; both retired
  names go in the release that closes the window
  [`release-versioning`](https://github.com/tibs245/scrumia/blob/main/features/business/release-versioning/business.md) fixes.

## [0.4.0] - 2026-08-10
### Added
- Test-driven development, applied app by app, with or without an implementation module.
- `scrumia-tdd`, `scrumia-tdd-audit`, `scrumia-tdd-refactor` — the reference, the audit and the refactor.

Earlier versions shipped without a changelog; `0.4.0` is the first version this file
describes, and it states what the module carries rather than reconstructing how it got
there. That history is in the repository's git log and its issues.
