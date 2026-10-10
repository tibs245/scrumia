# Changelog — scrumia-questions

All notable changes to this module, on [Keep a Changelog 1.0.0](https://keepachangelog.com/en/1.0.0/).

## [0.1.0] - 2026-10-10
### Added
- The module, a proof of concept: a Claude Code mod (function hooks), not a skill module.
- `mcp__scrumia-questions__ask_later` — the tool the model calls to park a question with
  its context, linked ticket, impact, suggested answers and a recommended one.
- A band above the prompt counting the questions waiting, and `/questions` to open the pane.
- A pane listing the waiting questions, a picker over the suggested answers (the
  recommended one preselected) and a field for a free answer.
- Answers return once, appended to the next prompt; questions persist across sessions.
