# Changelog — scrumia-github-project

All notable changes to this module, on [Keep a Changelog 1.0.0](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]

## [0.4.0] - 2026-08-10
### Added
- The `tracker` slot on GitHub Projects: issues, native sub-issues, columns, branches and PRs — no project state in the repository.
- `scrumia-refine`, `scrumia-ticket`, `scrumia-review`, `scrumia-status` — and their `/refine`, `/ticket`, `/review`, `/status` commands.
- `scrumia-project-setup` — seeds columns, labels and issue templates.
- `board.sh` — the only supported way to talk to the board: a `gh project` read without a filter is silently truncated at 30 items.

Earlier versions shipped without a changelog; `0.4.0` is the first version this file
describes, and it states what the module carries rather than reconstructing how it got
there. That history is in the repository's git log and its issues.
