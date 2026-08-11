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

## Step 3 — Load the directives this project reviews against

```bash
scrumia-extends review --app <app>      # omit --app for a change outside every app
```

Every `required` row is a rule this project's composition says a change is judged
against; every `optional` row is a method offered. A finding cites the row it comes from —
the module and the file — so the author can go read it, and so a verdict is never this
skill's opinion about a module it does not own.

An empty table means the composition contributes nothing to a review here; judge on the
criteria below alone, and say so rather than inventing rules.

## Step 4 — Check what is not in the diff

These gaps are invisible to a reviewer who only looks at the code:

- An identifier in `ac_id_format` in the file named by `acceptance_file` with no matching test
- An API contract changed without updating its interface-contract file from `catalog`, or without updating the consumers
- A behavior changed with no entry in the file named by `changelog`
- A spec modified without code, or the reverse, when the ticket asked for both
- A missing `Closes #<n>`

## Step 5 — Synthesize

Deliver a synthesis, not a compilation. The human must be able to decide in one read:

- **The overall verdict**: mergeable, mergeable with reservations, or blocked
- **What blocks**, if anything: file, line, concrete failure scenario
- **The reservations** and the issues created for them
- **The disagreements between reviewers**, passed on as is, without merging them into an average opinion

When Business and Tech diverge, that is first-order information: it's exactly the case that calls for human arbitration. Don't smooth it over.

## Step 6 — Publish

Post the synthesis as a comment on the PR (`gh pr comment`). Blocking objections go into a GitHub review on the relevant lines, where they'll be read in the right place.

**Do not merge.** Do not approve the PR in the GitHub sense in the human's place: that would consume the only guarantee the system leaves them — unless `settings.autonomy.auto_merge` in `.scrumia/config.yaml` explicitly says otherwise. Read it before deciding: `none` (its absence defaults to the same) merges nothing, ever; `docs-only` merges when the diff touches no code — specs, docs, config; `all` merges any PR this skill verdicted mergeable. In every case CI must be green and the verdict clean — reservations or a block always fall back to the human, whatever the setting says.
