# Changelog — dev-flow

Reverse-chronological. One entry per notable change, one category each.
The reasoning is in the issues; earlier history is in git and the tracker.

## 2026-09-14 — Gate 1 is no longer one undifferentiated "tests": three moments, an impacted selection derived from the diff, a full run at the end of the sprint (AC-56 to AC-62)
- Issue: #480
- Category: Added
- Breaking: no — a gate that already ran everything everywhere still satisfies the table;
  what changes is that it may now run less, and owes a named reason for every level it
  skips. `scrumia-ticket`, `scrumia-sprint` and `scrumia-sprint-fast` cite the section
  rather than carrying a cadence of their own, and the per-level commands and the
  path-to-test mapping become project data under the testing module's `params:`.

## 2026-09-10 — A sprint is designed once before its first worktree; its durable decisions ride the sprint branch, its ephemeral part the draft sprint PR (AC-51 to AC-55)
- Issue: #476
- Category: Added
- Breaking: yes — `scrumia-sprint` gains a design step between the batch and its
  validation, and Step 4b does not cut a worktree before the design commit is on
  `sprint/<milestone-slug>` and the draft sprint PR is open on it. `scrumia-ticket`
  reads the draft sprint PR before the ticket. `sprint-fast` inherits the step by
  citing Steps 1–3 and its global review reads the aggregate against the design.

## 2026-08-27 — A sprint runs on its own integration branch; ticket branches are cut from it
- Issue: #468
- Category: Added
- Breaking: yes — `scrumia-sprint` Step 4 now requires `sprint/<milestone-slug>` to
  exist before the first worktree is cut, and uses it as the start point of every
  ticket branch. `scrumia-ticket` resolves its base to the sprint branch when one
  exists, falling back to the default branch otherwise. The ticket PR targets the
  sprint branch and carries only `Refs:`; the close is carried by the sprint's own
  PR. The sprint branch merges as a merge commit (never a squash) and is deleted
  on merge. A ticket branch is named after its final intent, not its first phase.
  Both skills cite the rule from `business.md` § *The sprint branch* rather than
  restating it.

## 2026-08-20 — The orchestrator decides the execution mode; the executor does not isolate itself
- Issue: #124
- Category: Added
- Breaking: yes — `scrumia-ticket` no longer creates a worktree and states a precondition
  instead. `scrumia-sprint` is now the sole authority on isolation for batched runs.
  A direct invocation of `scrumia-ticket` outside a sprint is covered (the human is the
  orchestrator). Both skills cite this feature rather than restate the command.

## 2026-08-17 — Gate 2's verdict is recorded by the role, not asserted by the executor
- Issue: #125
- Category: Added
- Breaking: yes — the gate-2 outcome now has three states (`run`, `not_required`,
  `not_run`) and the verdict is read from the ticket's issue, not from the executor's
  report. A gather that does not know the new state cannot run.

## 2026-08-17 — `auto_merge` becomes a closed allowlist of named categories; the self-widening rule lands
- Issue: #218
- Category: Changed
- Breaking: yes

The `settings.autonomy.auto_merge` value space changes from a scalar
(`none | docs-only | all`) to a list of named categories; `all` is removed.
Gate 3's opening conditions are stated as four cumulative ones (level,
every path matched by an active category, CI green, clean attributable
verdict); `.scrumia/**` is excluded from every category by construction; a
`not_run` or absent verdict never opens gate 3; the constraints any category
list must satisfy (closed, explicit, excluding product/specs/decisions/
autonomy config) are stated here. The category list itself is project data
in `.scrumia/config.yaml`; the trace is in `features/business/github-tracking/`.
Downstream consumer wiring (eligibility script, skill citations, site
regeneration) is the sibling implementation sub-issue (#219).

## 2026-08-17 — A ticket that names the feature it produces is not refused at Step 0
- Issue: #18
- Category: Added
- Breaking: no


## 2026-08-16 — Gate 2's scoping signal: owed to the manager, recorded against the work item
- Issue: #222
- Category: Added
- Breaking: no

## 2026-08-11 — The multi-scope comma form generalizes past modules, and `*` covers what isn't worth naming
- Issue: #232
- Category: Changed
- Breaking: no

## 2026-08-11 — Brainstorming content validation gate (Gate 0)
- Issue: #142
- Category: Added
- Breaking: yes

## 2026-08-10 — A commit's mandatory shape, and the branch boundary on rewriting history
- Issue: #7
- Category: Added
- Breaking: no

## 2026-08-10 — Changelog rebuilt on Keep a Changelog's categories
- Issue: #213
- Category: Changed
- Breaking: no
