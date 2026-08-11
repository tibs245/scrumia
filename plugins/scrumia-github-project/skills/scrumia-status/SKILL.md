---
name: scrumia-status
description: Takes stock of a ScrumIA project — GitHub board state, features and their health, gaps between specs and code. Use it to know where the project stands, what's blocking, and what deserves attention.
---

# Project status

A view computed on demand. Nothing is written to disk: a persisted state diverges, a computed state cannot lie.

## What you read

1. `.scrumia/config.yaml` — if absent, say to run `/scrumia-core:scrumia-init` and stop.
2. The board, primary source — read it through the tool, never by composing `gh project` calls yourself:

   ```bash
   scrumia-board read
   ```

   It returns the items grouped by status, already filtered to `-status:Done`. Each item carries its type (`Issue` or `PullRequest`), so one read covers tickets and open PRs together. Scope it further when the question is narrower — `--query 'milestone:"Sprint 12"'` for one sprint, `--milestone` via `scrumia-board ready` for what's ready to start.

   **Check two fields before you report anything.** `truncated: true` means you are looking at part of the board, not the board — narrow the query rather than raising the limit, or say the count is partial. `filter_suspect: true` means the query matched nothing while the board is not empty: an unknown column, a milestone that doesn't exist, or a typo all look identical to a genuinely empty result. Reporting "nothing in progress" off a suspect filter is the one failure this skill must never produce. Why these guards exist: [`references/projects-v2.md`](${CLAUDE_SKILL_DIR}/references/projects-v2.md).
3. Fallback, when `tracker.project_number` is missing from the config, `scrumia-board` errors, or `gh` lacks the `project` scope: `gh issue list --state open --json number,title,labels,assignees,createdAt` and `gh pr list --json number,title,isDraft,reviewDecision,headRefName`. Say explicitly in the report that it reflects issue/PR state, not the board's actual columns, whenever this path is taken. `scrumia-board doctor` names which of the three is missing.
4. If `CLAUDE.md` carries a `## Specs contract` section (`docs/adr/0012-specs-contract.md`), the files named by `feature_index` under `specs_root` — **the indexes only**. Only go down into a feature if a signal demands it. **If the section is absent** — no specs module documented, or `scrumia-init` not yet run — say so: *"no specs module documented — ask the human or proceed without spec updates"*, and skip this source; the board alone still gives a status.

**If `gh` fails** — not authenticated: say so and point to `gh auth login`; the human runs it, this skill doesn't. Network or API error: retry once, then report and stop, don't loop on a flaky call. No repo or no remote: name the missing prerequisite (`.git`, a GitHub remote) and stop. Any of these takes the board out of reach — fall back to local git (`git log`, `git status`, `git branch -vv`) and mark the report as local state, not the board's: a status flagged partial beats one that's confidently wrong.

Board columns map directly to the sections below: `To dev` / `In progress` / `In review` tickets and open PRs feed **In progress**; `Ready for dev` feeds **Ready to go**. `Backlog` and `Done` don't get enumerated — they only surface if something in them triggers a point of attention.

## What the project measures itself against

```bash
scrumia-extends audit
```

The `audit` register is where the installed modules contribute the methods for measuring
an existing codebase against the rules it claims to follow — a SOLID audit, a TDD audit, a
design audit. They are `optional` by nature: this skill takes stock, and reaches for one
when the gap it is describing is that module's to measure. Name the ones it did not run,
so "nothing found" is never mistaken for "nothing looked".

## What you report

Short. Three blocks, in this order.

### In progress

The open PRs and the assigned tickets. For each PR: how long it's been there, and what it's waiting for (agent review, human validation, CI). A PR waiting on the human for more than two days is a point to flag, not a table row.

### Ready to go

The tickets with no blocker, with their `scope/*` and `risk/*` labels. Flag the ones with no scope label — they haven't been refined and won't enter a sprint. Flag the ones with a scope but no risk: they will execute on an assumed risk level, which is a decision nobody made.

For an epic, report GitHub's own count rather than recounting its children: `scrumia-board epic <n>` returns `progress: {completed, total, percentCompleted}`.

### Points of attention

Only what deserves an action. Look for:

- Tickets open for a long time with no movement
- Tickets with no acceptance criterion
- An epic whose children are all closed while the epic itself stays open
- Tickets in the current milestone that no longer fit the sprint's remaining time
- `draft` features referenced by active tickets
- Silent files named by `changelog` while the feature has recent commits
- App features with no Business parent and no justification
- PRs waiting for human validation

If there's nothing to flag, say so in one sentence. Don't invent a concern to fill the section.

## What you don't do

- No file written. No report, no snapshot.
- No exhaustive enumeration of the backlog: the user has GitHub for that. You bring the reading, not the list.
- No spontaneous fixing. You flag, the user decides.
