# Standard work item form

**Status**: draft

## In brief

The form this repository ships: five sections, three of them written by whoever
opens the issue and two composed from the modules the project runs. It is one
instance of what its parent requires of any form — the general rules are stated
there and none of them is repeated here.

It sits inside its parent's directory because it is one answer to that
feature's question, not a neighbouring subject: a second form would sit beside
it, under the same parent, without either restating what both are held to.

Its bet is that an issue reads the same everywhere while staying short to
write: a title, a need, criteria that can fail, and a rattachement. Everything
else an issue eventually carries is contributed rather than typed.

## Links

- Parent: `features/business/work-item-format/` — the standard every form is
  held to. This feature is one instance of it.
- Implemented by: no App feature — purely technical, enacted by the
  `scrumia-ticket-writer` module. Neither app in this repository is involved.
- Boundary: the sections are this feature's; what a classification level means
  is `execution-policy`'s, and where the issue sits in its flow is
  `github-tracking`'s.

## Files present

| File | Read it when |
|---|---|
| `business.md` | the sections, what each holds, and when each is filled |
| `qa.md` | acceptance criteria for a correctly-written issue |
| `CHANGELOG.md` | history of changes to this spec |

No `legal.md`: the form processes no personal data and mandates no legal
rubric of its own — a project needing one contributes it, which is that
module's subject. No `archi.md`: this feature's own implementation touches no
app. No `api-contract.md`, `tech.md`, `ux.md`, `security.md`, `devx.md`: none
applies to a writing convention with no interface of its own.
