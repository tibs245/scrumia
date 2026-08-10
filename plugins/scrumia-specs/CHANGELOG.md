# Changelog — scrumia-specs

All notable changes to this module, on [Keep a Changelog 1.0.0](https://keepachangelog.com/en/1.0.0/).
Entries are written by a human for someone deciding whether to take the version, never
generated from the commit log. Versions move per module: a number here promises that
*this* module changed, not that the repository published.

## [Unreleased]

## [0.4.0] - 2026-08-10
### Added
- The `specs` slot: per-feature specs as a contextual file catalogue under `features/`, not a monolithic PRD.
- `scrumia-feature` — creates, updates and audits a feature, applying the catalogue rather than a fixed template; `/feature` invokes it.
- `scrumia-specs-find` — finds the feature that owns a rule, so a ticket loads its context instead of the whole tree.
- `scrumia-specs-setup` — installs the tree.

Earlier versions shipped without a changelog; `0.4.0` is the first version this file
describes, and it states what the module carries rather than reconstructing how it got
there. That history is in the repository's git log and its issues.
