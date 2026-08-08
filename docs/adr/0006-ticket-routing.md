# ADR-0006 — Ticket routing by measurable scope

**Status**: accepted — 2026-08-07

## Context

The open question was: "what counts as a big-context ticket versus a small-context one, and who decides?"

"Big" and "small" are not decidable. Two agents, or an agent and a human, will classify the same ticket differently, and the classification will drift over time. We need a criterion that can be checked without judgment.

## Decision

**Four levels, decided by three objective questions**, carried by a GitHub `scope/*` label. The Manager sets the label at scoping.

The three questions:

1. How many apps are touched?
2. Does a file in `features/` change?
3. If so, which one?

| Label | Condition | Handling |
|---|---|---|
| `scope/S` | 1 app, no spec modified, rule already written | Autonomous execution alone |
| `scope/M` | 1 app, but a spec changes or the scope is fuzzy | Autonomous execution + `scrumia-tech` review |
| `scope/L` | ≥2 apps, or touches `features/business/**`, or changes an API contract | Manager + `scrumia-tech`, + `scrumia-business` if business is touched |
| `scope/XL` | New EPIC, pivot, data migration | Leaves execution: sent back to scoping |

Two application rules:

- **When hesitating between two levels, take the higher one.** One review too many costs a few minutes; a missing review costs a revert.
- **The label conditions the entry, the diff conditions the exit.** A PR whose diff exceeds its label is reviewed according to its actual diff (ADR-0005), and the gap is flagged — it is a signal of failed scoping.

A ticket without a `scope/*` label is an unscoped ticket: it does not enter a sprint and shows up as such in `scrumia-status`.

## Consequences

**What we gain**

- The criterion is verifiable: the number of apps and the file paths are facts.
- The label lives in GitHub, so it is filterable, and consistent with "state lives in GitHub" (ADR-0008).
- Classification does not depend on a complexity estimate, which would be an invention made before splitting.

**What we accept**

- *The criterion ignores intrinsic difficulty.* A delicate algorithm in a single file of a single app is `scope/S`, when it may deserve a review. Mitigated by two things: the "when in doubt, go one level up" rule, and the fact that the diff's actual scope re-triggers the review at Gate 2. If the case turns out to be frequent, add a `needs-tech` label that can be set by hand rather than complicating the grid.
- *`scope/XL` is not an execution level*, it is a switch back to scoping. That is deliberate: there is no good way to autonomously execute what has not been scoped.

## Rejected alternative

**Estimating in points or in number of files touched.** Estimation precedes the work: it is wrong by construction, and it drifts over time without anyone noticing. The number of apps and the type of spec touched are known at scoping time, and can be verified after the fact.
