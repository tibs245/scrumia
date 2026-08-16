# The gate-2 scoping signal

When a review's own measurement of a diff disagrees with the `scope/*` label the ticket
carries, that disagreement is reported — to the manager, recorded against the ticket — but
**only** under the condition below. This file carries the test, so the skills that apply it
do not reach outside this module for it.

## The three questions the axis asks

Copied word for word from the axis that owns them, never reworded — a rewording is a second
definition of one test, which is the drift the axis was written to end.

1. **How many apps are touched?**
2. **Does a rule consumed beyond one feature or app change?** — a contract another app
   depends on, a vocabulary another feature reads, an invariant another feature enforces.
   Not "does a file under the specs root change".
3. **Does an interface contract change?**

| Label | Condition |
|---|---|
| `scope/S` | ≤1 app, no rule changes: it is already written |
| `scope/M` | ≤1 app, a rule changes, read only in its feature, or unclear |
| `scope/L` | ≥2 apps, a rule read beyond its feature, or interface contract |
| `scope/XL` | New value unit, pivot, data migration: back to scoping |

**On question 2, the reading that matters is reach, not medium.** A ticket that edits files
under the specs root without changing any rule another feature or app consumes does not
reach `scope/L` on that clause; it is judged on the other two questions. The
file-location reading fails on a whole class of repository — where the deliverable *is*
specs, every ticket touches a spec file by construction, every ticket is `scope/L`, and the
axis stops discriminating.

**Hesitating between two levels, take the higher one.** One tier too high costs a stronger
model than the ticket needed; one tier too low costs a botched ticket. Round up for
capability — the label buys no reviewer.

## When the disagreement is a signal, and when it is nothing

**The label conditions the entry; the diff conditions the exit.** Who is asked *while* the
ticket runs comes from the label. Who reviews the PR comes from the diff's actual scope,
which reads no label at all.

The two grids therefore **disagree routinely and correctly**. A specs-only diff whose rule
nothing else consumes is a correct `scope/M` that still draws a business reviewer. Reporting
that as a mislabel would fire on a whole class of correctly-labelled ticket.

> The gap is a reportable scoping signal **only when the three questions above, applied to
> what the diff actually touched, would have answered higher than the label carries.**

A disagreement on its own reports nothing.

## What is recorded, and where

Record it **on the issue**, addressed to the manager — the role that set the label and
routes on it — and echo it in the pull request. The record has to outlive the run: a run
that dies before the pull request exists must still leave one behind, because the
retrospective's trigger counts these gaps by reading records against tickets, not
pull-request threads. The echo is a copy; the record is the artefact.

## Sources

Transcribed here rather than linked, so this module carries what its skills apply. Open
these to argue with the rule, never to apply it — what runs is the text above.

| What it owns | Where |
|---|---|
| The decision to adopt this axis, and the label table | `docs/adr/0015-scope-measures-reach.md` |
| The live statement of question 2 — reach, not medium | `features/business/execution-policy/business.md` § *The scope axis measures reach, not medium* |
| When the signal is owed, and to whom | `features/business/dev-flow/business.md` § *Gate 2's scoping signal* |
| The record's venue, and the echo | `features/business/github-tracking/business.md` |
| Why the retrospective needs the record | `features/business/ceremonies/business.md` |
| That the exit grid reads the diff and no label | `docs/adr/0005-validation-gates.md` |

Those paths name files in the ScrumIA repository, which is not installed beside this
module. They are provenance: if one of them cannot be reached, nothing above stops working.
When one of them changes, this file is what has to be brought back into line.
