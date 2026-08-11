# Changelog — scrumia-design

All notable changes to this module, on [Keep a Changelog 1.0.0](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]
### Added
- The designer's "What you write to your project memory" section names the check to run
  before writing an entry — would this note land elsewhere, even if that hasn't happened
  yet — and cites `features/business/agent-team/business.md` § *What role memory may
  hold* for the full test.

## [0.4.0] - 2026-08-10
### Added
- The `design` slot: identity, tokens and components under `design/`, one directory per component.
- `scrumia-design-system` — the reference to load before writing anything a user will look at.
- `scrumia-design-setup`, `scrumia-design-audit`, `scrumia-design-sync` — install the tree, audit an existing interface for drift *and* for mutedness, and publish a component to a Claude Design project.
- The `designer` standing role — the only role that judges what a user actually sees.

Earlier versions shipped without a changelog; `0.4.0` is the first version this file
describes, and it states what the module carries rather than reconstructing how it got
there. That history is in the repository's git log and its issues.
