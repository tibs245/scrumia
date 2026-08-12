# Changelog — scrumia-rules

All notable changes to this module, on [Keep a Changelog 1.0.0](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]
### Changed
- `README.md` reordered into the module-anatomy template — the four required sections,
  in order, and nothing else: "When you need it" folds into "What it answers", "Skills"
  is renamed "What it ships". The `section.json`/anatomy detail from "What it is" moves
  into "What it answers"; the ASCII directory tree under "Format at a glance" is dropped —
  the format reference (`scrumia-rules`'s own `SKILL.md`) is where that belongs, not a
  README addressed to someone who hasn't adopted the module yet.

## [0.4.0] - 2026-08-10
### Added
- The rules-hierarchy format itself — index, guides, decisions. Fills no slot.
- `scrumia-rules`, `scrumia-rules-setup`, `scrumia-rules-update` — consume, create and evolve rule sections, module-shipped or project-local.

Earlier versions shipped without a changelog; `0.4.0` is the first version this file
describes, and it states what the module carries rather than reconstructing how it got
there. That history is in the repository's git log and its issues.
