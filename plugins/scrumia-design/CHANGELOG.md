# Changelog — scrumia-design

All notable changes to this module, on [Keep a Changelog 1.0.0](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]
### Added
- `registers.json`, `extends.json` and `dependencies.jsonl` — this module opens the
  `design` register and contributes to `implement`, `review`, `audit` and `convene`;
  the designer role reaches the team through `convene` rather than through prose.

## [0.4.0] - 2026-08-10
### Added
- The `design` slot: identity, tokens and components under `design/`, one directory per component.
- `scrumia-design-system` — the reference to load before writing anything a user will look at.
- `scrumia-design-setup`, `scrumia-design-audit`, `scrumia-design-sync` — install the tree, audit an existing interface for drift *and* for mutedness, and publish a component to a Claude Design project.
- The `designer` standing role — the only role that judges what a user actually sees.

Earlier versions shipped without a changelog; `0.4.0` is the first version this file
describes, and it states what the module carries rather than reconstructing how it got
there. That history is in the repository's git log and its issues.
