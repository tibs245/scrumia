# ADR-0013 — The `tracker` slot stays one slot, for now

**Status**: accepted — 2026-08-08

## Context

`scrumia-github-project` fills the `tracker` slot alone, and carries three concerns that are only accidentally related:

1. **The work items** — issues, labels, milestones, epics-as-sub-issues, issue templates.
2. **The board** — columns, the Status field, transitions between them.
3. **The code cycle** — branches, worktrees, PR creation, review routing, merge.

The first two are "what is to be done and where it stands". The third is "how the change reaches `main`". A single module owns all three because GitHub happens to offer all three, not because they belong together.

The combination that exposes this is not hypothetical: **issues in Jira or Linear, pull requests on GitHub** is one of the most common setups in real teams. Today it cannot be composed. A `scrumia-jira` module filling the `tracker` slot would have to reimplement branches, worktrees and PRs — code-cycle mechanics that have nothing to do with Jira — or leave `scrumia-ticket` without a way to open a PR at all. The slot's boundary forces an all-or-nothing choice that the underlying tools don't.

Two things have changed since this was first noted as a weakness, and they pull in opposite directions.

**Against scinding now**: the other half of the original problem is gone. The coupling that made this urgent was `scrumia-ticket` hard-coding `scrumia-specs`'s file names, and ADR-0012 fixed that separately. What remains is a real design flaw, but no longer a compounding one.

**In favour of scinding later, cheaply**: the seam is already half-cut. `scripts/board.sh` now owns every interaction with the board and the work items — it reads, filters, moves cards, resolves epics, and touches **no** branch, worktree or PR. The code cycle stayed in prose, in `scrumia-ticket` steps 2 and 7. Nobody designed that split as a preparation for scinding; it fell out of putting the board's traps behind one tool. It means a future split has a natural cut line already drawn, and drawn by usage rather than by speculation.

## Decision

**The `tracker` slot stays a single slot until a pilot has run. The split is not rejected — it is deferred, with explicit conditions for reopening.**

No `forge` slot, no `scrumia-github-forge` module, no change to `composition.tracker` in the config schema. `scrumia-github-project` keeps its three concerns.

What is done now instead, because it costs little and preserves the option:

- **The seam stays clean.** `board.sh` handles work items and the board; it must not grow a `pr` or `branch` subcommand. Code-cycle steps stay in `scrumia-ticket`'s prose. Whoever splits later gets a boundary that already holds.
- **The cost is written down rather than discovered.** `docs/modules.md` states that the `tracker` slot bundles the code cycle, so a reader evaluating a Jira module learns the limitation from the docs and not from a failure.

**Reopen this when any of these becomes true:**

1. A real project needs issues in one tool and PRs in GitHub. This is the decisive one: it turns an aesthetic objection into a blocked user.
2. `scrumia-tracker-local` gets written (`docs/roadmap.md`). A file-based tracker has no PRs at all, so it will either prove the code cycle separates cleanly, or prove the slot needs the split before the module can exist.
3. The pilot shows `scrumia-review` and `scrumia-status` diverging — one reasoning about PRs, the other about columns, sharing no configuration. That divergence is the split asking to happen.

## Consequences

**What we gain**

- No slot invented before a user needs it. A `forge` slot designed against an imagined Jira integration would be shaped by guesses about Jira; one designed against a real project would not.
- The dogfooding pilot runs on the composition as it is, and the split gets argued from what it does wrong in practice rather than from a diagram.
- The refactor stays cheap. The seam is drawn and enforced by `board.sh`'s scope, so deferring costs option value, not future work.

**What we accept**

- **Jira + GitHub is not composable today, and won't be until this is reopened.** That is a real capability gap, and it is the single strongest argument against this decision. Anyone hitting it is blocked, not inconvenienced.
- The `tracker` slot is the largest in the composition and the least honest about it: its name says "tracking" while it also owns how code ships. A name that undersells its scope is a name that misleads.
- ADR-0007's claim that every slot is replaceable holds less firmly here than elsewhere. Replacing `tracker` means reimplementing the code cycle, which is more than "replaceable" suggests.
- Deferring twice would be a decision by inertia. If a pilot runs and none of the three conditions is examined, this ADR has failed regardless of what the pilot found.

## Rejected alternatives

**Split now into `tracker` + `forge`.** The honest architecture, and it stays the likely endpoint. Rejected on sequencing, not on merit: the boundary between "the board" and "the code cycle" is currently drawn from reasoning about GitHub alone. A split placed there and found wrong by the first real Jira project costs a slot rename across every module's documentation, plus a config migration for existing projects — more than deferring costs.

**Split the module without splitting the slot** — ship `scrumia-github-project` as two plugins that both declare `tracker`. Rejected: two plugins filling one slot is exactly the ambiguity ADR-0009's one-module-per-slot table exists to prevent. It would buy internal tidiness at the cost of the composition's central invariant.

**Declare the slot's scope as "GitHub, wholesale" and close the question.** Rejected: it would make the limitation permanent by definition rather than by decision, and `docs/modules.md` already lists `scrumia-tracker-local` as the test of the slot's replaceability. Closing the question would contradict a commitment already written down.
