# scrumia-questions

Experimental. A proof of concept of a Claude Code **mod** — function hooks, not a skill
module — that gives questions to the person a place to wait.

## What it answers

A session often reaches a decision that belongs to the person while the work could go on
without it. Asking in chat blocks the session or buries the question. This mod parks it
in an inbox, in one format, and the person answers when they choose.

## How it works

| Piece | Role |
|---|---|
| `ask_later` tool | The model parks a question: `context`, `ticket`, `question`, `impact`, `options`, `recommended`. It then carries on. |
| Band above the prompt | `N questions waiting`, with an Open button. Absent when nothing waits. |
| `/questions` and its pane | The waiting questions, the detail of one, a picker over the suggested answers (the recommended one preselected), a field for any other answer. |
| `prompt.submit` hook | The answers not yet delivered are appended to the next prompt, once. |
| `$.store` | Questions and answers survive the session. |

## What it refuses

- A question that blocks the session when the work could continue without the answer.
- A question without its context, impact and a recommended answer: the tool schema
  requires them, so an unstructured question has nowhere to go.
- A silent answer: it returns once, appended to the prompt, never re-delivered.

## What it ships

| What | Role |
|---|---|
| `hooks/register.tsx` | The tool, the band, the command, the pane and the prompt hook, all in one module. |
| `hooks/register.test.ts` | Five tests: parking, numbering, the untouched prompt, and the pane answer on two surfaces. |

## Install while it is a POC

```bash
claude --plugin-dir plugins/scrumia-questions
```

## Known limits

- Whether the pane draws depends on the surface the session runs in; the band and the
  command are the safer entry points. Verify on the desktop app before relying on it.
- Chrome strings are English; the question text is whatever language the model writes in.
- A question belongs to the machine, not to the project: nothing is written in the repo.
  The decision taken still belongs in the linked ticket.

## Tests

```bash
claude plugin validate plugins/scrumia-questions
claude plugin test plugins/scrumia-questions
```
