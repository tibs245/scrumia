# Changelog — scrumia-teams

All notable changes to this module, on [Keep a Changelog 1.0.0](https://keepachangelog.com/en/1.0.0/).
Entries are written by a human for someone deciding whether to take the version, never
generated from the commit log. Versions move per module: a number here promises that
*this* module changed, not that the repository published.

## [Unreleased]

## [0.4.0] - 2026-08-10
### Added
- The `team` slot: standing roles and sprint execution.
- The `manager`, `business` and `tech` standing roles.
- `scrumia-standup` — convenes the roles without starting anything; `scrumia-sprint` — runs a batch of ready tickets, one isolated worktree each; `scrumia-team-setup` — configures which roles run on which models.
- `pick-model.sh` — answers which model a ticket runs on, so a skill acts on its instruction instead of re-reading the matrix.

Earlier versions shipped without a changelog; `0.4.0` is the first version this file
describes, and it states what the module carries rather than reconstructing how it got
there. That history is in the repository's git log and its issues.
