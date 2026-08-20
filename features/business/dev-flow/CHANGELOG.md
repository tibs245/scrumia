# Changelog — dev-flow

Reverse-chronological. One entry per notable change, one category each.
The reasoning is in the issues; earlier history is in git and the tracker.

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
