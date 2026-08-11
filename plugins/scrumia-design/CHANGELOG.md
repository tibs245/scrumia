# Changelog — scrumia-design

All notable changes to this module, on [Keep a Changelog 1.0.0](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]
### Added
- `composition.json` and `scrumia-design-manifest` — this module declares the actions it
  provides, the fragment to open for each, and how a person reaches it, so the
  composed assemblies are built from it rather than from prose about it.

## [0.4.0] - 2026-08-10
### Added
- The `design` slot: identity, tokens and components under `design/`, one directory per component.
- `scrumia-design-system` — the reference to load before writing anything a user will look at.
- `scrumia-design-setup`, `scrumia-design-audit`, `scrumia-design-sync` — install the tree, audit an existing interface for drift *and* for mutedness, and publish a component to a Claude Design project.
- The `designer` standing role — the only role that judges what a user actually sees.

Earlier versions shipped without a changelog; `0.4.0` is the first version this file
describes, and it states what the module carries rather than reconstructing how it got
there. That history is in the repository's git log and its issues.
