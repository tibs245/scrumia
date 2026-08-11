---
name: scrumia-review
description: Reviews a ScrumIA PR by routing to the right reviewers according to what it touches. Use it to review an open PR, or before approving a merge.
---

# Review a PR

Route the review to the right agents according to what the PR actually touches, then synthesize for the human who decides.

Usage: `/scrumia-github-project:scrumia-review 17`

## Step 1 — Measure the actual scope

```bash
gh pr view <n> --json title,body,files,headRefName
gh pr diff <n>
```

The scope that matters is the diff's, not the one announced in the issue. A `scope/S` ticket whose PR touches three apps is a badly scoped ticket: treat it according to what it does, and flag the gap.

Never trust a commit SHA a review brief or ticket names as the tip: run `git log --oneline origin/<branch>..HEAD` and `git status --short` in the worktree first. The brief's named commit, the worktree `HEAD` and `origin/<branch>` can all differ — reviewing the named SHA can reproduce findings the author already fixed, and reviewing without checking `origin` can let a verdict land on bytes the PR does not contain. Report an unpushed tip as a precondition on the verdict.

**If `gh` fails** — not authenticated: say so and point to `gh auth login`; the human runs it, this skill doesn't. Network or API error: retry once, then report and stop, don't loop on a flaky call. No repo or no remote: name the missing prerequisite (`.git`, a GitHub remote) and stop. If the PR's branch is checked out locally, fall back to a local diff against the base branch instead of `gh pr diff` — the review can still happen; publishing the synthesis (`gh pr comment`) and merging stay out of reach until `gh` is back.

## Step 2 — Route

**Read `CLAUDE.md`'s `## Specs contract` section first** — it names the specs module's own vocabulary (`specs_root`, `feature_index`, `acceptance_file`, `ac_id_format`, `changelog`, `catalog`; `docs/adr/0012-specs-contract.md`), used below to tell what kind of spec a PR touches. **If the section is absent** — no specs module documented, or `scrumia-init` not yet run — say so: *"no specs module documented — ask the human or proceed without spec updates"*, and route by the code-only rows.

| What the PR touches | Reviewers |
|---|---|
| 1 app, no spec | self-review only, already done at execution |
| Code, an App spec | `scrumia-tech` |
| A business feature under `specs_root`, or a `catalog` legal/compliance file | `scrumia-tech` + `scrumia-business` |
| ≥2 apps, or an interface-contract file from `catalog` | `scrumia-tech` + `scrumia-business` if business is at stake |

Run the reviewers in parallel when there are two: they don't depend on each other, and their angles are deliberately different.

**Without a team module plugged in**, do the review yourself, following the same grid: the tech angle (architecture, contracts, failure scenarios) and, if a business spec is touched, the business angle (rules, vocabulary, compliance). Say so explicitly in the synthesis — the human must know this review had a single reviewer wearing two hats.

## Step 3 — Check what is not in the diff

These gaps are invisible to a reviewer who only looks at the code:

- An identifier in `ac_id_format` in the file named by `acceptance_file` with no matching test
- An API contract changed without updating its interface-contract file from `catalog`, or without updating the consumers
- A behavior changed with no entry in the file named by `changelog`
- A spec modified without code, or the reverse, when the ticket asked for both
- A missing `Closes #<n>`
- A `gh search` command written into a spec, skill or script, not run against a negative control before approval — this failure mode returns full recall with exit 0, so eyeballing the rows proves nothing
- A restated rule sitting beside a `features/` citation that duplicates the source's *trigger* or *obligation* rather than its *reason* — the test is whether the two copies could ever command different behavior, not whether the wording overlaps; a duplicated reason is allowed, since a citation with no inline summary degrades to nothing once the link can't be followed
- A cross-cutting rule newly nested under one `## Step N` of a SKILL.md, when the skill has an earlier yield point — a role spawn, a human escalation, a wait — the rule's wording doesn't reach
- A PR changing a `plugins/` behavior, without a grep of the whole tree for prose in *other* skills and agents that still asserts the old one — `tools/validate.py` checks that a link resolves, never that a sentence stays true, and skills routinely state what a sibling does. Grep the old rule's phrasing *and* any new phrasing the PR itself introduces — a rule re-keyed mid-review can leave the previous sweep's replacement wording stale too

## Step 4 — Synthesize

Deliver a synthesis, not a compilation. The human must be able to decide in one read:

- **The overall verdict**: mergeable, mergeable with reservations, or blocked
- **What blocks**, if anything: file, line, concrete failure scenario
- **The reservations** and the issues created for them
- **The disagreements between reviewers**, passed on as is, without merging them into an average opinion

When Business and Tech diverge, that is first-order information: it's exactly the case that calls for human arbitration. Don't smooth it over.

## Step 5 — Publish

Post the synthesis as a comment on the PR (`gh pr comment`). Blocking objections go into a GitHub review on the relevant lines, where they'll be read in the right place.

A reservation's ticket is not done at `gh issue create`: a bare `gh issue create` lands the issue with no board card at all, and `gh issue create --project "<title>"` lands one with no Status — either way `scrumia-board find <n>` must report `found: true` before the reservation counts as handled. `scrumia-board read` and `scrumia-board ready` only see cards, so a cardless issue is exactly as forgotten as no issue, and a card with no Status is invisible to a sprint prepared from `ready`. If the card is missing, add it (`gh project item-add`) before calling the reservation closed.

**Do not merge.** Do not approve the PR in the GitHub sense in the human's place: that would consume the only guarantee the system leaves them — unless `settings.autonomy.auto_merge` in `.scrumia/config.yaml` explicitly says otherwise. Read it before deciding: `none` (its absence defaults to the same) merges nothing, ever; `docs-only` merges when the diff touches no code — specs, docs, config; `all` merges any PR this skill verdicted mergeable. In every case CI must be green and the verdict clean — reservations or a block always fall back to the human, whatever the setting says.
