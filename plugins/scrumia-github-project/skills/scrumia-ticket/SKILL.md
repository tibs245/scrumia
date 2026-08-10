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
- `decision: "split_or_model"` — the ticket is oversized. **Try to split it first** (`scrumia-refine` Step 4, or the discovery module). Splitting is the preferred outcome, not a formality. If the work is genuinely indivisible — one migration, one contract that cannot be delivered by halves — execute it on the fallback model and record the refused split as a deviation, below. An oversized ticket is a reason to think again, not a wall.
- `decision: "split"` — return it to refinement; this cell allows no fallback.

If no team module is plugged in, there is no policy to read: execute on the current model and say so in the PR.

### Record a deviation before the work starts

Two things make this run deviate from the policy: **a human overrode the model** — you were told to run on something other than what `pick-model.sh` answered — or **you refused the split** a `split_or_<model>` cell preferred. Either one gets one comment on the issue, posted **now**, before Step 2:

```bash
gh issue comment <n> --body-file - <<'EOF'
Deviation: override — cell L/low — policy opus — ran sonnet — by human @<handle>
Reason: <why, in the words of whoever decided it>
EOF
```

Use the heredoc, not `--body '…'`: a reason is English prose and the first apostrophe in it ends the quote and breaks the command.

- `<kind>` is `override` or `split_refused`. An **override is a human's decision by definition** — if nobody chose it, you have not overridden the policy, you have failed to follow it. Do not file that as an override.
- `cell` is the scope and risk `pick-model.sh` read back, in the axes' own vocabulary (`L/low`), not the project's label spelling. Where it reports `scope_rated: false`, write `unlabeled/<risk>`.
- `policy` is what it answered, verbatim — a model name, `split_or_<model>`, or `split`.
- `ran` is the model you are actually executing on.
- `by` is `human` and the handle whose decision it was for an override; for a refused split it is you — name this skill.
- **`Reason:` is mandatory.** A deviation with no reason cannot be reviewed and cannot be told apart from a mistake; a record missing it is non-compliant, not a note to complete later.

Now, not at PR time: the record has to survive a run that dies before opening one. The PR echoes it in Step 7 for a human reading the diff, and the echo is a copy — this comment is the record. Prose in five PR bodies is exactly what this replaces.

**If the comment cannot be posted, stop** — same discipline as any other failing `gh` call in this step, and for a sharper reason: a deviation that runs unrecorded is the exact failure this record exists to end, and it is invisible afterwards. Report it and let the human decide.

This record is written and never read back. It is evidence for editing the grid in `.scrumia/config.yaml`, not a precedent that changes what a cell answers today — the policy's answer stays the only way a model is chosen.

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

During a sprint, several siblings run this same command concurrently against the same
`.git` — by design. It is safe because `<type>/<n>-<slug>` makes each branch, path and
worktree registration unique; the only shared state is transient lock files.

If the command fails with a `.lock: File exists` error, a sibling holds it briefly: retry,
up to three times, a few seconds apart. If it still fails after that, the lock is stale —
its owner died holding it. Report the lock file's path and stop; never delete a lock file
in a shared `.git` yourself: four siblings may be live inside it.

`<type>`: `feat`, `fix`, `refactor`, `docs`, `chore`.

Inside the project directory, not `../<repo>-<n>`: Claude Code's permissions are scoped to the project directory, and a worktree created outside it triggers extra prompts or fails outright in restricted modes. The cost is a folder to keep out of the diff — `.worktrees/` is gitignored by `scrumia-project-setup`.

This isolation is what makes several tickets parallelizable without conflict. The number
of siblings is `sprint.max_tickets`, a human-review cap — git is not the limiting factor.
Raising it is a review-bandwidth decision, never a git one.

Move the card to the `in_progress` step:

```bash
${CLAUDE_SKILL_DIR}/../../scripts/board.sh move <n> in_progress
```

The flow step maps to this board's actual column name through the config ([`projects-v2.md`](${CLAUDE_SKILL_DIR}/../scrumia-status/references/projects-v2.md)). If the move fails, continue anyway and say so in the final report: a dead column is not a blocked ticket.

## Commit before you yield

From here on, what carries this run's output is the branch created in Step 2 — not the working tree. The working tree belongs to whatever process happens to hold it, and that process can vanish while the run is paused. So commit to the ticket's branch before the run hands control to anyone else:

```bash
git add -A && git commit -m "<type>: <what changed>"
```

The rule, and what counts as yielding control, are stated once in [`features/business/dev-flow/business.md`](../../../../features/business/dev-flow/business.md) § *Who decides, on each path* → **Execution**. Read it there rather than inferring it from this skill: it is written as the general case, so it covers yields the steps below do not name — including ones added to this skill after this sentence.

This sits before Step 3 because Step 2 is where the branch starts existing and Step 3 can already yield. The steps that name it — 3, 5, 6, and *When you're blocked* — are where it bites in practice, not the extent of it.

## Step 3 — Update the spec first

Skip this step in the degraded case from Step 1: no specs module documented, no spec to update — go straight to Step 4.

Otherwise, if the ticket changes a behavior, the spec changes **before** the code — not after:

- Consult the feature's `feature_index` file for which of its `catalog` files covers what changed — its "why this file exists" listing is what points you there without this skill assuming a fixed name. On the producer side if it's an interface contract.
- Update that file, and the file named by `acceptance_file` if the criteria themselves move.
- In every case, add an entry to the file named by `changelog`, with the issue number.

Writing the spec first surfaces contradictions before they get encoded in code. That's where the cost is lowest.

If while writing the spec you discover a contradiction with another feature: stop, commit the spec changes you have — calling the role is a yield, and it is your spec edits that expose the contradiction — then comment on the issue and call on the business role. Do not decide a business rule yourself.

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

Commit those fixes before going further, per *Commit before you yield* above.

## Step 6 — Agent review according to the diff

**Do not spawn a role while the working tree is dirty** — spawning one is a yield, per *Commit before you yield* above. Check it:

```bash
git status --porcelain   # must print nothing before a role is spawned
```

`git diff <base>...HEAD` below reads committed history, so a role routed off it reviews the branch and nothing else.

If a team module is plugged in, route the review by what your diff actually touches. List it first — `git diff <base>...HEAD --name-only` from the worktree — then apply gate 2's table ([`docs/adr/0005-validation-gates.md`](../../../../docs/adr/0005-validation-gates.md)), in the specs module's own vocabulary from Step 1:

| What the diff touches | Required review |
|---|---|
| 1 app, no spec | your Step 5 self-review, already done |
| Code, an App spec | the tech role |
| A business feature under `specs_root`, or a `catalog` legal/compliance file | the tech role + the business role |
| ≥2 apps, or an interface-contract file from `catalog` | the tech role, + the business role if business is at stake |

This is the same table `scrumia-review` applies at gate 2, deliberately: the two must never disagree about who owed this PR a review.

**Do not gate this on the `scope/*` label.** The label says which review to *expect*, and comparing the two is worth a line in the PR — but a wrong label is precisely the failure a review exists to catch, so it cannot be what decides whether the review runs. Where the diff's row asks for more than the label implied, say so in the PR: per [ADR-0015](../../../../docs/adr/0015-scope-measures-reach.md), that gap is a signal of failed scoping, not a detail.

The table has no scope tier in it, `scope/XL` included: ADR-0015 sends an `XL` ticket back to scoping rather than into execution, and where Step 0's split was refused as genuinely indivisible so it executed anyway on the fallback model (`features/business/execution-policy/`), its diff routes its review like every other diff's. No tier is left without a stated review, because no tier states one.

Spawn the role by its agent type — `scrumia-teams:scrumia-tech`, `scrumia-teams:scrumia-business`. If the type does not resolve, the module that ships it was installed or updated without a restart since; say so rather than reviewing anyway, and fall back to a subprocess, prompt on stdin:

```bash
claude -p --agent scrumia-teams:scrumia-tech \
  --allowedTools "Read,Glob,Grep,Bash" < review-prompt.txt
```

Both run the actual role. [The roles' doc](../../../../docs/agents.md) carries the restart rule and why the failure is silent.

A **Blocked** review gets fixed before opening the PR — and the fix is committed before the role is asked again, which is another yield. An **Approved with reservations** review goes out as is, with the reservations carried into the PR description and turned into issues.

Without a team module plugged in, your self-review from step 5 is the only review before the human. Say so explicitly in the PR: the reviewer must know what was checked and by whom.

The same holds when the role itself could not be reached. Handing your own general agent the role's `.md` file is not that role, and the difference is measured: on one sprint's five PRs, self-applied reviews returned five approvals and two reservations where the actual roles returned one blocker and nine. Report which one ran. A fallback that reads as the real thing is worse than a fallback that names itself.

## Step 7 — Open the PR

```bash
gh pr create --title "<type>: <expected outcome>" --body "..."
```

The description contains: what was done, the `Closes #<n>` link, the criterion-by-criterion mapping (each acceptance identifier in `ac_id_format` → its test, if a specs module is documented), the specs modified, the verdict of the agent reviews — with the label/diff gap from Step 6, where there was one — and the open reservations with their issues.

If Step 0 recorded a deviation, echo it here — kind, cell, what the policy chose, what ran, why — for a human reading the diff. The echo, not the record: the comment on the issue is what a later reader queries, and the PR body is a copy of it.

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

Commit what you have first: stopping hands the next move to a human, and a branch left in place with an uncommitted tree carries nothing. Then comment on the issue with: what you tried, what's blocking, and the options you see. Leave the branch in place. Do not open a half-done PR — an incomplete PR costs more to review than a clear comment.
