# Changelog — scrumia-specs

All notable changes to this module, on [Keep a Changelog 1.0.0](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]
### Added
- The catalog states where a feature-format rule is restated — the five sites a sweep
  has to reach, ordered by damage — and distinguishes a criterion's own falsifiability
  (`qa.md`, "must be able to fail") from ADR-0004's feature-splitting *verifiable*, which
  is a different property under a shared word.

### Changed
- The changelog entry drops its `PR:` field and gains a `Category:` — an entry names
  only what exists when it is written. The catalog and the template state the new shape.
- `scrumia-feature/SKILL.md`'s history rule is now an explicit must/must-not checklist
  instead of prose alone, and states `business.md`'s sourcing boundary against ADRs and
  acceptance criteria explicitly — an executor following only `scrumia-ticket` had no
  reason to open this file's rule before writing.

## [0.4.0] - 2026-08-10
### Added
- The `specs` slot: per-feature specs as a contextual file catalogue under `features/`, not a monolithic PRD.
- `scrumia-feature` — creates, updates and audits a feature, applying the catalogue rather than a fixed template; `/feature` invokes it.
- `scrumia-specs-find` — finds the feature that owns a rule, so a ticket loads its context instead of the whole tree.
- `scrumia-specs-setup` — installs the tree.

Earlier versions shipped without a changelog; `0.4.0` is the first version this file
describes, and it states what the module carries rather than reconstructing how it got
there. That history is in the repository's git log and its issues.
