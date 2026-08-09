---
name: vocab-scope-label-readers
description: The scope/* label has entry readers and no exit reader — the vocabulary trap behind every routing contradiction in the business specs
metadata:
  type: project
---

`scope/*` is read at **entry** and never at **exit**. Since #130 (2026-08-09):

- `pick-model.sh` reads it for capability — the *only programmatic* reader
  (`features/business/execution-policy/`, `features/business/github-tracking/business.md`).
- The manager reads it at entry to route who is *asked* while the ticket runs
  (`features/business/agent-team/business.md`) — a reading, not a program.
- Gate 2's **exit review** reads no label at all: it routes by the diff
  (ADR-0005, owned by `features/business/dev-flow/`).

So "one reader" and "two readers" are both true depending on whether you count
programmatic readers or readings. Any spec that states a bare count without saying
which it counts creates a contradiction with the other feature.

**Why:** the same word "review" was used for entry routing and for the exit gate,
which is how #79 shipped `scope/S` with the business review it was owed skipped.
The specs now say "asked at entry" / "routed to" for entry and reserve "required
review" for gate 2.

**How to apply:** when a change touches label routing, check all five statements
(`execution-policy/business.md` + its AC-5, `github-tracking/business.md` + its
table + its CHANGELOG headline, `agent-team/business.md` + AC-1, `dev-flow/qa.md`
AC-6, and the plugin prose in `scrumia-refine`, `scrumia-ticket`, `scrumia-project-setup`,
`scrumia-manager.md`). Boundaries: dev-flow owns gate 2 (`github-tracking/qa.md`
sends PR review routing there explicitly); agent-team owns entry triggers;
github-tracking owns the label's consumer list; execution-policy owns the
blast-radius test.
