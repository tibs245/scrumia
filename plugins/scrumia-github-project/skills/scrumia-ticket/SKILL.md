---
name: scrumia-ticket
description: Executes a GitHub ticket end to end — isolated branch, spec updates, implementation, tests, review, PR. Use it to handle a specific issue autonomously.
---

# Execute a ticket

A ticket goes in, a PR comes out. The human validates at the end of the chain, not in the middle.

Usage: `/scrumia-github-project:scrumia-ticket 42`

## Step 0 — Refuse what isn't executable

Read the issue (`gh issue view <n> --json title,body,labels`). Stop immediately if:

- No verifiable acceptance criterion
- No parent feature

In those cases, comment on the issue stating precisely what's missing, and point back to the Manager or to `scrumia-brainstorm`. **Do not guess the intent.** A ticket executed on an assumed intent produces a PR to throw away, and that costs more than asking for clarification.

Then, if a team module is plugged in, ask what this ticket's size and risk imply. `scrumia-teams` ships the policy as a script; in a standard marketplace install it sits alongside this plugin:

```bash
${CLAUDE_SKILL_DIR}/../../../scrumia-teams/scripts/pick-model.sh <n>
```

**If that path doesn't resolve** — a different team module fills the slot, or the plugins aren't installed side by side — don't hunt for it and don't reimplement the policy from the labels: execute on the current model and say so in the PR. This skill must not depend on another module's layout.

Do what `instruction` says; don't re-derive it from the labels. Three answers are possible:

- `decision: "model"` — execute here, on the model named.
- `decision: "split_or_model"` — the ticket is oversized. **Try to split it first** (`scrumia-refine` Step 4, or the discovery module). Splitting is the preferred outcome, not a formality. If the work is genuinely indivisible — one migration, one contract that cannot be delivered by halves — execute it on the fallback model and state in the PR why the split was refused. An oversized ticket is a reason to think again, not a wall.
- `decision: "split"` — return it to refinement; this cell allows no fallback.

If no team module is plugged in, there is no policy to read: execute on the current model and say so in the PR.

**If `gh` fails** — not authenticated: say so and point to `gh auth login`; the human runs it, this skill doesn't. Network or API error: retry once, then report and stop, don't loop on a flaky call. No repo or no remote: name the missing prerequisite (`.git`, a GitHub remote) and stop. This is the ticket's first `gh` call — stop here, before opening a worktree or touching the board: nothing half-started is easier to clean up than a stray branch and a stuck card.

## Step 1 — Load the context, not the repo

Read `CLAUDE.md`'s `## Specs contract` section first — it names the specs module's own vocabulary (`specs_root`, `feature_index`, `acceptance_file`, `ac_id_format`, `changelog`, `catalog`), written there by `scrumia-init` from that module's own `## Composition block` (`docs/adr/0012-specs-contract.md`). Never assume `scrumia-specs`'s file names directly: a different module can occupy the `specs` slot with a different layout, and this step must keep working unchanged.

**If the section is absent** — no specs module documented, or `scrumia-init` not yet run — say so: *"no specs module documented — ask the human or proceed without spec updates"*, and go straight to the code neighboring the area to modify. Degraded, not blocked.

Otherwise, read, in this order, and stop as soon as you know enough:

1. The parent feature's file named by `feature_index` — it says which files exist and why
2. The file named by `acceptance_file` — the criteria you must satisfy, identified in `ac_id_format`
3. Whichever other files listed under `catalog` the index marks relevant — a rule, an interface, or a technical choice the ticket touches
4. The code neighboring the area to modify

Do not load all of the directory named by `specs_root`. The format exists so you don't have to.

## Step 2 — Isolate

Work in a dedicated worktree, never in the main working tree:

```bash
git worktree add .worktrees/<type>/<n>-<slug> -b <type>/<n>-<slug>
```

`<type>`: `feat`, `fix`, `refactor`, `docs`, `chore`.

Inside the project directory, not `../<repo>-<n>`: Claude Code's permissions are scoped to the project directory, and a worktree created outside it triggers extra prompts or fails outright in restricted modes. The cost is a folder to keep out of the diff — `.worktrees/` is gitignored by `scrumia-project-setup`.

This isolation is what makes several tickets parallelizable without conflict.

Move the card to the `in_progress` step:

```bash
${CLAUDE_SKILL_DIR}/../../scripts/board.sh move <n> in_progress
```

The flow step maps to this board's actual column name through the config ([`projects-v2.md`](${CLAUDE_SKILL_DIR}/../scrumia-status/references/projects-v2.md)). If the move fails, continue anyway and say so in the final report: a dead column is not a blocked ticket.

## Step 3 — Update the spec first

Skip this step in the degraded case from Step 1: no specs module documented, no spec to update — go straight to Step 4.

Otherwise, if the ticket changes a behavior, the spec changes **before** the code — not after:

- Consult the feature's `feature_index` file for which of its `catalog` files covers what changed — its "why this file exists" listing is what points you there without this skill assuming a fixed name. On the producer side if it's an interface contract.
- Update that file, and the file named by `acceptance_file` if the criteria themselves move.
- In every case, add an entry to the file named by `changelog`, with the issue number.

Writing the spec first surfaces contradictions before they get encoded in code. That's where the cost is lowest.

If while writing the spec you discover a contradiction with another feature: stop, comment on the issue, call on the business role. Do not decide a business rule yourself.

## Step 4 — Implement according to the app's module

**Before writing code, resolve which implementation module and which practices cover the file you're about to touch.** The procedure:

1. **Resolve the app by path** — match the file against `apps[].path` in `.scrumia/config.yaml`. No match, no module: follow the conventions of the neighboring code. That's normal behavior, not a gap.
2. **Open the index, not the whole module** — for the app's `implementation` module and each of its `practices`, read only the skill's `SKILL.md`. If the app carries a per-app `CLAUDE.md` stub at its path, it points straight there.
3. **Load only the routed guides** — the index's routing table tells you which reference guide(s) apply to the kind of change you're making (tests, structure, a specific pattern). Load those, not the module's full reference set.
4. **Respect each module's `section.json` globs** — a module only speaks for the files it claims within the app; outside its globs, it has nothing to say and neighboring conventions apply.

Precedence, once the relevant guides are loaded: the implementation module is authoritative on the "how" — its way of writing tests, its design principles, its file structure — including against your preferences. Where a practice (`scrumia-practice-tdd`, `scrumia-practice-solid`, …) and the implementation module disagree, the implementation module wins — **specific beats generic**. A project override (`.scrumia/impl/`, `.scrumia/practices/`) wins over both.

Whether an implementation module is plugged in or not: if a specs module is documented, cover each criterion in `ac_id_format` from the file named by `acceptance_file` with a test that can fail; in every case, run the project's tests and linter.

Stay within the ticket's scope. What you notice in passing that exceeds it becomes an issue, not an extra line of diff. A PR that overflows is hard to validate — and human validation is the system's bottleneck.

## Step 5 — Self-review

Reread your own diff before proposing it. Look for: an uncovered `AC`, an ignored error case, a contract modified without its file, dead code, a secret, an out-of-scope file.

Fix what you find. What you can't fix here becomes an explicit note in the PR.

## Step 6 — Agent review according to scope

If a team module is plugged in, apply the label's grid:

| Label | Required review |
|---|---|
| `scope/S` | none |
| `scope/M` | the tech role |
| `scope/L` | the tech role, plus the business role if a business spec is touched |

Spawn the role by its agent type — `scrumia-teams:scrumia-tech`, `scrumia-teams:scrumia-business`. If the type does not resolve, the module that ships it was installed or updated without a restart since; say so rather than reviewing anyway, and fall back to a subprocess, prompt on stdin:

```bash
claude -p --agent scrumia-teams:scrumia-tech \
  --allowedTools "Read,Glob,Grep,Bash" < review-prompt.txt
```

Both run the actual role. [The roles' doc](../../../../docs/agents.md) carries the restart rule and why the failure is silent.

A **Blocked** review gets fixed before opening the PR. An **Approved with reservations** review goes out as is, with the reservations carried into the PR description and turned into issues.

Without a team module plugged in, your self-review from step 5 is the only review before the human. Say so explicitly in the PR: the reviewer must know what was checked and by whom.

The same holds when the role itself could not be reached. Handing your own general agent the role's `.md` file is not that role, and the difference is measured: on one sprint's five PRs, self-applied reviews returned five approvals and two reservations where the actual roles returned one blocker and nine. Report which one ran. A fallback that reads as the real thing is worse than a fallback that names itself.

## Step 7 — Open the PR

```bash
gh pr create --title "<type>: <expected outcome>" --body "..."
```

The description contains: what was done, the `Closes #<n>` link, the criterion-by-criterion mapping (each acceptance identifier in `ac_id_format` → its test, if a specs module is documented), the specs modified, the verdict of the agent reviews, and the open reservations with their issues.

Then comment on the issue with the PR link, and move the card to the `in_review` step:

```bash
${CLAUDE_SKILL_DIR}/../../scripts/board.sh move <n> in_review
```

If the move fails, continue anyway and say so in the final report: a dead column is not a blocked ticket.

## Step 8 — Stop

**You do not merge.** Final validation belongs to the human, except for a category explicitly listed in `autonomy.auto_merge` of `.scrumia/config.yaml` — and even then, CI must be green.

Clean up the worktree once the PR is open:

```bash
git worktree remove .worktrees/<type>/<n>-<slug>
```

## When you're blocked

Comment on the issue with: what you tried, what's blocking, and the options you see. Leave the branch in place. Do not open a half-done PR — an incomplete PR costs more to review than a clear comment.
