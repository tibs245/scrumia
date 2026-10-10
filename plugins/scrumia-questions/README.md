# scrumia-questions

Experimental. A Claude Code **mod** — function hooks, not a skill
module — that gives questions to the person a place to wait.

Specified in [`features/business/session-mods/`](https://github.com/tibs245/scrumia/blob/main/features/business/session-mods/business.md)
(section `scrumia-questions`); where it lives is
[ADR-0026](https://github.com/tibs245/scrumia/blob/main/docs/adr/0026-session-mods-are-plugins-of-their-own.md).

## What it answers

A session often reaches a decision that belongs to the person while the work could go on
without it. Asking in chat blocks the session or buries the question. This mod parks it
in an inbox, in one format, and the person answers when they choose.

## How it works

| Piece | Role |
|---|---|
| `ask_later` tool | The model parks a question: `context`, `ticket`, `question`, `impact`, `isBlocking`, `options` (1 to 6), `recommended` (optional, copied from the options). `question`, `ticket`, the options and `recommended` are single lines; `context` and `impact` may span several. A blocking question tells the model not to go ahead on what depends on it; the others tell it to carry on. |
| Band above the prompt | `N questions waiting`, the blocking ones counted in red, with an Open button. Absent when nothing waits. |
| `/questions` and its pane | A filter (All / Blocking / Non-blocking, with counts), the waiting questions blocking first with a coloured badge, one question as a bordered card (context, impact in Markdown) with a `Remove` button, a picker over the suggested answers (the recommended one starred and preselected) that always ends with `Other`, an `Additional notes` field, a `ready` mark per question, and one `Send N answers` button on top. |
| `prompt.submit` hook | The answers not yet delivered ride the next prompt the person typed (prompt box, Remote Control bridge, or a plugin submitting as the person) as context for the model, once, and are marked delivered only after the prompt went through. A task notification, a sub-agent's return or a scheduled trigger leaves them waiting. |
| `$.store` | One entry per project root: questions, drafts and the next number. Delivered questions are dropped thirty days after their delivery, at a later delivery. Unanswered or undelivered questions are never purged. |

## What it refuses

- A malformed question: the call is refused with its reason when the context, question or
  impact is empty, `isBlocking` is missing, there are no options or more than six, the
  recommendation is not one of the options, or the question, ticket, an option or the
  recommendation holds a line break or a control character. Nothing is stored, so the pane never holds a
  question it cannot draw.
- A lost answer: the answers are marked delivered only once the prompt carrying them was
  accepted; a prompt refused further down leaves them to the next one.
- A lost question: writes go through one queue, so parallel calls keep every question.
- A silent answer: it is delivered once, never twice, and only on a prompt the person typed.
- A forged answer: the single-line fields cannot carry a line break, so the model cannot write a line that passes for the person's answer in the delivered note.
- An `Other` answer without a note: it is not ready, since it would say nothing.
- One click per question: choices and notes are kept as drafts, and a single button sends
  every ready answer of the filtered view. The preselected recommendation counts as the
  answer when nothing else is picked.
- Notes left behind: `Additional notes` travel with the answer whichever choice is picked.
- The model's words in the person's voice: the question texts reach the model beside the
  prompt, labelled as the model's own, never inside the text the person typed.

## What it expects to find

- A Claude Code that loads plugins made of hooks modules (`hooks/hooks.json` naming
  `modules`). Older versions ignore the plugin without saying so.
- Nothing from the other ScrumIA modules: `ticket` is free text, no tracker is read.

## What it ships

| What | Role |
|---|---|
| `hooks/register.tsx` | The tool, the band, the command, the pane and the prompt hook, all in one module. |
| `hooks/register.test.ts` | Tests: parking and numbering, parallel calls, malformed calls, the context delivery once and labelled, a prompt refused below, one project not seeing another's questions, more than six options refused, a line break refused in each single-line field, answers kept for a prompt the person typed, the thirty-day purge counted from the delivery, a question stored in an older shape, the band, the send limited to the filtered view, and on two surfaces the pane answer, the filter, `Other`, the default recommendation, the grouped send and `Remove`. |

## Public contract

What a later version must keep reading or announce in the changelog: the tool name
`mcp__scrumia-questions__ask_later` and its `inputSchema`; the `/questions` command; the
shape stored under `project:<root>` in `$.store` (`nextId`, `questions`, `drafts`; a question may carry `deliveredAt`).

## Install

```
/plugin install scrumia-questions --marketplace tibs245/scrumia
```

For development, from a checkout of the repository:

```bash
claude --plugin-dir plugins/scrumia-questions
```

## Known limits

- Whether the pane draws depends on the surface the session runs in; it draws on the
  desktop app. The band and the command are the safer entry points elsewhere.
- Chrome strings are English; the question text is whatever language the model writes in.
- A question belongs to the machine and to the project root it was asked in: nothing is
  written in the repo, and two sessions open on the same project share its inbox, and an answer given in one is delivered at the next typed prompt of whichever session reads the project first. The
  decision taken still belongs in the linked ticket: the inbox is a buffer, and an answer
  returns with the ticket's number so the decision can be reported there, since state
  lives in the tracker.
- The filter and the open question are per session and start again after a reload.
- The queue serialises writes inside one process; two processes writing the same project
  at the same instant are not protected.

## Tests

```bash
claude plugin validate plugins/scrumia-questions
claude plugin test plugins/scrumia-questions
```
