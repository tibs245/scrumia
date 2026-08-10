# GitHub tracking

**Status**: active

## In brief

How ScrumIA tracks work when the `tracker` slot is filled by `scrumia-github-project`:
the ticket's lifecycle across the board's six columns, what a milestone and an epic
mean, which label is read by which consumer, and the reading discipline that keeps a
partial board read from being reported as a complete one. Per ADR-0013, the module
filling this slot also implements the code cycle (branches, worktrees, PRs) — a scope
wider than its name suggests — but the cycle's process is specified by
`features/business/dev-flow/`. This feature traces that process onto GitHub: it says
which artefact each step becomes here, and redefines none of them.

## Links

- Implemented by: `plugins/scrumia-github-project/` (the `tracker` slot). Not an App
  feature under `features/app/`: the plugin is the product ScrumIA ships, not one of
  this project's own `site`/`tools` apps — see `.scrumia/config.yaml`'s `apps` table.
- Authority: `features/business/dev-flow/` — that feature specifies the code-cycle
  process; this one only binds it to GitHub's artefacts (`business.md` § *Scope of
  this slot* says which plane governs).

## Files present

| File | Read it when |
|---|---|
| `business.md` | the ticket lifecycle, the milestone/epic vocabulary, label consumers, where a deviation from the execution policy is recorded, the slot's scope per ADR-0013 |
| `qa.md` | checking the board-reading discipline against a falsifiable scenario |
| `tech.md` | how `board.sh` and `gh` carry out a rule stated in `business.md` — a retry, a field shape, a search command |
| `CHANGELOG.md` | tracing when a rule above last changed and under which issue |

