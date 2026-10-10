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
- Answers return once, as context beside the next prompt, once it went through; questions
  persist across sessions, per project root.
- A malformed call is refused with its reason, a blocking question tells the model not to go
  ahead on what depends on it, and `Remove` takes a question out; delivered questions are
  dropped after 30 days.
- Data shape, to read again by any later version: `$.store`, key `project:<root>`: `{ nextId, questions, drafts }`. A question stored without
  `isBlocking` still draws, as one that can wait.
