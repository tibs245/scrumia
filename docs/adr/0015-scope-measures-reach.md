# ADR-0015 — The scope axis measures reach, not medium

**Status**: accepted — 2026-08-10
**Supersedes**: [0006](0006-ticket-routing.md)

## Context

ADR-0006 settled that a ticket's scope is decided by objective questions rather than by an impression, and that part holds. What it got wrong is one of the questions.

0006's second question was *"does a file in `features/` change?"*, and its table rendered `scope/L` as "≥2 apps, or touches `features/business/**`, or changes an API contract". That is a test on a file's **location**, and it fails on a whole class of repository. Where the deliverable *is* specs, every ticket touches a spec file by construction, every ticket is `scope/L`, and the axis stops discriminating — it no longer separates the tickets it exists to separate.

ScrumIA is such a repository, so the failure is not hypothetical here. The 2026-08-08 sprint overrode the resulting answer on all five of its tickets, in the same direction (#32), and the refinement of #34, #35 and #36 hit it again. An axis that has to be overridden systematically is not a strict axis.

`features/business/execution-policy/business.md` specified the correction when that feature was written (#13): the clause reads a rule's **blast radius**. But the surfaces an agent actually reads still rendered the old test — this ADR's predecessor, `scrumia-refine`'s Step 5 table, `scrumia-manager`'s routing table, and the `scope/*` label descriptions on GitHub. Three of those four were patchable. This one was not: an accepted ADR is never modified ([`README.md`](README.md)), so aligning it takes a superseding ADR, which is this one (#78).

## Decision

**Four levels, decided by three objective questions**, carried by a GitHub `scope/*` label that the manager sets at refinement. Unchanged from 0006.

The three questions, with the second and third re-stated:

1. How many apps are touched?
2. **Does a rule consumed beyond one feature or app change?** — a contract another app depends on, a vocabulary another feature reads, an invariant another feature enforces. Not "does a file under the specs root change".
3. Does an interface contract change?

| Label | Condition | Asked at entry |
|---|---|---|
| `scope/S` | At most 1 app, and no rule changes — it is already written | executes alone |
| `scope/M` | At most 1 app, and a rule changes that nothing beyond it consumes, or the scope is fuzzy | + the tech role |
| `scope/L` | ≥2 apps, or a rule consumed beyond one feature or app changes, or an interface contract changes | + the manager and the tech role, + the business role if a business rule is at stake |
| `scope/XL` | New unit of value, pivot, data migration | leaves execution: sent back to scoping |

Three application rules:

- **The live statement of question 2 is the spec's, not this table's.** `features/business/execution-policy/business.md` § *The scope axis measures reach, not medium* owns the test; this ADR records the decision to adopt it, and the surfaces that route a labeller cite the spec rather than paraphrasing it. That is what keeps the next drift to one place to fix instead of five.
- **When hesitating between two levels, take the higher one.** One tier too high costs a stronger model than the ticket needed; one tier too low costs a botched ticket. Round up for capability — not to buy a reviewer, because the label buys none.
- **The label conditions the entry, the diff conditions the exit.** Who is asked *while* the ticket runs comes from the label; who reviews the PR comes from the diff's actual scope ([ADR-0005](0005-validation-gates.md)), which reads no label at all. Where the two disagree, the gap is flagged — it is a signal of failed scoping, not a skipped review. 0006 stated this rule with a "Handling" column that read as though the label bought a reviewer; it does not, and has not since #130.

A ticket without a `scope/*` label is an unscoped ticket: it does not enter a sprint, and it shows up as such in `scrumia-status`.

## Consequences

**What we gain**

- The axis discriminates again in a specs-first repository. A ticket that rewrites a vocabulary three features read and a ticket that fixes a typo in one feature's own prose no longer land on the same label.
- The correction has one home. The test is one section of one spec, and every surface that routes a labeller points at it, so the next change to the test is one edit rather than five that drift apart.
- The systematic override disappears with its cause. #32's five overrides in one sprint were the axis reporting a defect; the defect is now named and fixed rather than absorbed by the executors.

**What we accept**

- *Question 2 is a judgement about reach, not a path glob.* "Is this rule consumed beyond its feature?" is checkable — a feature's `index.md` Links section names its consumers — but it is checkable by reading, not by matching a pattern. That is a real loss of mechanical verifiability against 0006, and we take it, because a mechanical test that answers "yes" for every ticket in the repository verifies nothing.
- *Labels set under the old reading do not migrate themselves.* Twelve open tickets carried the file-location reading and had to be re-judged by hand when this landed (#78). Any project adopting this change inherits the same one-off pass.
- *`scope/XL` is still not an execution level*, it is a switch back to scoping. Kept from 0006 deliberately: there is no good way to autonomously execute what has not been scoped.

## Rejected alternatives

**Editing 0006 in place.** Cheaper by every measure except the one that matters: a reader following a link to 0006 from a six-month-old PR has to find what was decided *then*. An ADR that changes under its readers is a document nobody can cite.

**Dropping the spec question entirely**, leaving scope on app count and interface contracts alone. That makes every specs-only change `scope/S` in this repository, including one that rewrites a vocabulary three features read. The failure is symmetrical to 0006's and harder to notice, because under-labelling is silent where over-labelling at least produced #32's overrides.

**A fifth level, or a second axis, to carry spec reach.** Rejected for the reason the execution policy already gives about aliasing: the grid is defined over four values per axis, and a fifth is a different grid, not a finer one. The clause needed a correct test, not more room.
