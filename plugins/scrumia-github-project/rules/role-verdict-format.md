# The role review verdict — vocabulary and format

The vocabulary the role writes, and the fixed shape it takes. Transcribed here so
the skills that read it (refinement, execution, review) carry the rule rather than
reach outside the module for it. The vocabulary is the gate's; this file states
what the gate reads.

## The three states

A role review produces one of three states, of which one is a failure:

- **`run`** — the review ran *as the role*, and a verdict is attached. The
  transport that reached the role is not a state in itself: a `claude -p --agent`
  subprocess is `run` when it ran as the role, and `not_run` when it did not —
  what matters is who answered, not how the answer was reached.
- **`not_required`** — the ticket's scope prescribes no review (`scope/S`). This
  is a label-derived state: the executor does not declare it. An executor that
  asserts `not_required` on a `scope/M` or `scope/L` is asserting a substitution
  the gate refuses, and the record is read as non-compliant.
- **`not_run`** — a required review did not run as its role. **Cause is
  mandatory** in the carrier: the same record that names the state names the
  reason — the role's agent type did not resolve, the role disclaimed, the
  executor fell back to a self-applied review, the review was unreachable for
  whatever reason. "Skipped" and "unreachable" are *causes* of `not_run`, not
  states: at gate 3 the human takes the same decision for any required-and-absent
  review, regardless of cause.

A self-applied review — the executor running its own diff through a general agent
handed the role's `agents/` file — is not a role review. At the role gate, a
self-applied review counts as `not_run` with that cause; the verdict the gate
reads is the role's, and a verdict that came from no role is no verdict.

## The format the role writes

**The verdict is posted by the role, not by the executor.** The role's agent
writes its own verdict, in a form a later reader can find without re-running the
review. The format is:

```
Verdict: Approved | Reservations | Blocked — #<n> — by scrumia-<role>
```

`Approved`, `Reservations` and `Blocked` are the three outcomes the role can
sign; the ticket number ties the verdict to its work item; the `by scrumia-*`
token names the role that produced it. The format is not negotiated per role or
per ticket — it is the vocabulary the gate reads, and a verdict that does not
match the format is read as absent (`not_run`).

## Attribution is required

A verdict that does not name the role that produced it is treated as absent:
`not_run`. The `by scrumia-<role>` token is not a courtesy — it is what lets the
gate tell a role verdict from a comment that happens to match the format, and
closes the substitution path a structured field written by the executor's
return would reopen.

## Sources

Transcribed here rather than linked, so this module carries what its skills
apply. Open these to argue with the rule, never to apply it — what runs is the
text above.

| What it owns | Where |
|---|---|
| The three states, the cause requirement, the self-applied clause | `features/business/agent-team/business.md` § *The verdict vocabulary, posted by the role* |
| Why the role posts its own verdict, not the executor | `features/business/dev-flow/business.md` § *Who decides, on each path* |
| Acceptance criteria that close the rule | `features/business/agent-team/qa.md` AC-10, AC-20 |

Those paths name files in the ScrumIA repository, which is not installed beside
this module. They are provenance: if one of them cannot be reached, nothing
above stops working. When one of them changes, this file is what has to be
brought back into line.
