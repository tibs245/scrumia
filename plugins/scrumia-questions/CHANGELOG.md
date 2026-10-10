# Changelog — scrumia-questions

All notable changes to this module, on [Keep a Changelog 1.0.0](https://keepachangelog.com/en/1.0.0/).

## [0.1.0] - 2026-10-10
### Added
- The module, a proof of concept: a Claude Code mod (function hooks), not a skill module.
- `mcp__scrumia-questions__ask_later` — the tool the model calls to park a question with
  its context, linked ticket, impact, whether it blocks (`isBlocking`), suggested answers
  and a recommended one. A question stored without the field counts as non-blocking.
- A band above the prompt counting the questions waiting, and `/questions` to open the pane.
- A pane: an All / Blocking / Non-blocking filter with counts, the waiting questions
  blocking first with a coloured badge, the open one as a bordered card, a picker over the
  suggested answers (the recommended one starred and preselected) that always ends with
  `Other`, an `Additional notes` field always sent with the answer (required with `Other`),
  a `ready` mark per question and one `Send N answers` button that sends the ready answers
  of the filtered view. The preselected recommendation is the answer unless another is picked.
- Answers return once, appended to the next prompt; questions persist across sessions.
