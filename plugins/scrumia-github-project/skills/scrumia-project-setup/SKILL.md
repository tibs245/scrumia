---
name: scrumia-project-setup
description: Sets up a project's GitHub tracking — board columns, labels, issue templates. Invoked by scrumia-init when this module fills the tracker slot, or by hand to check the installation.
---

# Set up tracking

Prepares GitHub Projects to carry the project's state. Idempotent.

## What this module assumes

**State lives in the tracking tool, not in the repository.**

This is the module's central bet: a versioned state file has two writers, no lock and no consistency constraint — it can only drift, and a wrong state gets noticed long after it was believed.

The cost of the opposite choice is real: dependence on GitHub, nothing readable offline, and an authenticated `gh` required. An equivalent module for Jira, Linear or a local file would fill the same slot differently.

## Step 1 — Check access

`gh auth status` and `gh repo view`. Without access, still create the local files (issue templates) and list what remains to be done by hand. Do not block the entire installation on missing authentication.

## Step 2 — Read the configuration

```yaml
settings:
  tracker:
    project: "My project"     # name of the GitHub Project
    columns:                  # the states of the flow
      - Backlog
      - Ready for dev
      - To dev
      - In progress
      - In review
      - Done
```

If absent, propose these values and write them. The columns reflect the real flow: a raw ticket lands in `Backlog`, leaves it once refined and scoped (`Ready for dev`), enters a sprint (`To dev`), then follows its execution.

## Step 3 — Create the labels

| Label | Usage | Read by |
|---|---|---|
| `scrumia` | Marks tickets driven by the composition | filters, to separate them from tickets opened by hand |
| `scope/S` `scope/M` `scope/L` `scope/XL` | How far the change reaches, set at refinement | `scrumia-pick-model`, and `scrumia-manager` at entry (routes who is asked); the PR review is routed by the diff, not by this label |
| `risk/low` `risk/medium` `risk/high` `risk/critical` | What it costs to get this wrong | `scrumia-pick-model` |
| `needs-<role>` | Escalation requested to a role — one per active role in `settings.team.roles`, including those a non-team module provides (`needs-design`) | `scrumia-manager` |
| `epic` | Marks a unit of value; its children are **native sub-issues** | `scrumia-status`, `scrumia-board epic` |

`gh label create <name> --color <hex> --description <text>`, ignoring duplicate errors.

### The scope and risk descriptions are seeded verbatim, not improvised

A label's description is the only statement of the axis a labeller gets without leaving GitHub, and it outlives the repository it was copied from. Seed these exactly — a description typed from memory at install time becomes one more independent rendering of a test, and a test rendered independently in four places is how this axis came to say four different things:

```bash
gh label create "scope/S"  --color c2e0c6 --description "≤1 app, no rule changes: it is already written — features/business/execution-policy/"
gh label create "scope/M"  --color fef2c0 --description "≤1 app, a rule changes, read only in its feature, or unclear — features/business/execution-policy/"
gh label create "scope/L"  --color f9d0c4 --description "≥2 apps, a rule read beyond its feature, or interface contract — features/business/execution-policy/"
gh label create "scope/XL" --color e99695 --description "New value unit, pivot, data migration: back to scoping — features/business/execution-policy/"
gh label create "risk/low"      --color 0e8a16 --description "Reversible in a commit, no data, no user-visible behaviour"
gh label create "risk/medium"   --color fbca04 --description "Visible to users, but a revert restores the previous state"
gh label create "risk/high"     --color d93f0b --description "Money, personal data, auth, or a contract other apps consume"
gh label create "risk/critical" --color b60205 --description "Irreversible: destructive migration, payment, outbound notification"
```

The `scope/*` wording turns on **a rule's blast radius, not a file's location**: a rule read beyond its feature is a contract another app depends on, a vocabulary another feature reads, an invariant another feature enforces. A ticket that edits files under the specs root and changes no such rule is not `scope/L` on that clause, however many spec files its diff lists. The test is the execution policy's to state — [`features/business/execution-policy/business.md`](https://github.com/tibs245/scrumia/blob/main/features/business/execution-policy/business.md) § *The scope axis measures reach, not medium* here, or whichever feature owns the axis in the project being set up — and each description carries the tier condition [ADR-0015](https://github.com/tibs245/scrumia/blob/main/docs/adr/0015-scope-measures-reach.md) states, word for word, followed by the path of the feature that owns the test. Substitute that path when another feature owns it; do not re-word the condition to make room. A longer path than this project's needs the owning feature's name instead of its full path — `scope/L` above sits at exactly 100 characters, so anything longer is rejected with a 422 and `gh label create` fails mid-setup. The reference has to stay findable, not stay long. Read the descriptions back with `gh label list` once seeded: nothing else catches an over-budget one.

A GitHub label description stops at 100 characters, and the owner reference spends 38 of them. That budget is why the conditions are written as tightly as they are — and why the same tight wording is what the refinement skill's table, the manager's routing table and ADR-0015 all carry. The narrowest surface sets the wording for every surface, so that a labeller reading one of them is reading the same sentence as a labeller reading any other. Re-run this step after the test changes; nothing else propagates it to GitHub.

Scope and risk are two axes, not one scale. A one-line change to a payment rule is `scope/S` and `risk/critical`; a large but mechanical rename is `scope/L` and `risk/low`. Collapsing them into a single "priority" is what makes small dangerous changes get executed casually.

If the project already labels its tickets, keep its vocabulary and map it in `settings.team.execution.labels` (`scrumia-team-setup`, Step 3) rather than relabelling an existing backlog.

## Step 3b — Set up what keeps the board readable

A board is not a list you scroll; past a hundred cards, nobody reads it whole and neither should a skill. Three GitHub mechanisms carry that, and ScrumIA uses all three rather than paginating:

- **Milestones are sprints.** One milestone per sprint gives every read a natural boundary: `scrumia-board ready --milestone "Sprint 12"` is a question with an answer, `scrumia-board ready` is a backlog dump. Create them as sprints are planned, not upfront.
- **Epics are native sub-issues**, not a naming convention. GitHub computes `subIssuesSummary` itself; a hand-maintained checklist in a parent issue's body is a second source of truth that drifts the first time someone closes a child without ticking the box.
- **Labels are filters before they are documentation.** Every label above earns its place by being something a query selects on.

None of this is cosmetic: `gh project item-list` silently returns only its first 30 items by default, so a board that is never filtered is a board that is silently half-read. The tool guards against it (see the reference below), and good filing is what makes the guard rarely fire.

## Step 4 — Create the issue templates

The plugin ships ready-made ones — don't author them by hand. Copy them from the plugin's own `templates/` directory into `.github/ISSUE_TEMPLATE/`:

- [`templates/ISSUE_TEMPLATE/ticket.yml`](${CLAUDE_SKILL_DIR}/../../templates/ISSUE_TEMPLATE/ticket.yml) — a piece of work to execute. Fields: parent feature, context, targeted acceptance criteria (identifiers in the format named by `ac_id_format` in the Specs contract), scope (anticipated apps and files). Default label: `scrumia`.
- [`templates/ISSUE_TEMPLATE/epic.yml`](${CLAUDE_SKILL_DIR}/../../templates/ISSUE_TEMPLATE/epic.yml) — a unit of value to scope. Fields: problem, expected value, anticipated apps, open questions. Labels: `scrumia`, `epic`, `scope/XL`.

```bash
mkdir -p .github/ISSUE_TEMPLATE
cp ${CLAUDE_SKILL_DIR}/../../templates/ISSUE_TEMPLATE/*.yml .github/ISSUE_TEMPLATE/
```

Re-run: if a file already exists at that path, check it against the shipped version instead of overwriting it — a project may have edited its copy on purpose, and silently clobbering that is worse than leaving a stale template in place. Report the drift and let the user decide whether to refresh it.

The templates only ask for what cannot be inferred. A form that is too long doesn't get filled in, and an empty field is worth less than an absent one.

While here, make sure `.gitignore` lists `.worktrees/` and `review-prompt.txt` — append either line if it's missing, skip what's already present.

`scrumia-ticket` creates its per-ticket worktrees under `.worktrees/` instead of `../<repo>-<n>`, so the working tree stays inside the directory Claude Code's permissions actually cover, and an untracked folder in the diff isn't a surprise. `review-prompt.txt` is what the role-review fallback writes into the worktree; a ticket run must reach a clean `git status` before it spawns a role, so an unignored copy either blocks that check or rides into the PR on the next `git add -A`.

## Step 5 — Create the board

Check that the project exists (`gh project list --owner <owner> --format json`). If it's missing, offer to create it:

```bash
gh project create --owner <owner> --title "<tracker.project>"
```

**The columns then have to be set separately.** A new board ships `Todo` / `In Progress` / `Done`, and no `gh` subcommand can change them — it takes an `updateProjectV2Field` mutation, whose exact form (required fields, the enum colours, and the fact that the option list *replaces* rather than extends) is in [`projects-v2.md`](${CLAUDE_SKILL_DIR}/../scrumia-status/references/projects-v2.md#creating-the-boards-columns). Run it while the board is still empty: replacing an option deletes the status of every card in it.

If the user would rather keep an existing board with its own column names, don't rename anything — record the mapping in `board.flow` at the end of this step instead.

The Projects v2 API requires specific scopes. If `gh` doesn't have them, give the command `gh auth refresh -s project` and let the user decide — it's a privilege elevation on their account, and it belongs to them.

Once the project exists (created or found), resolve and persist what the other skills need to move a card — they must not re-discover these on every call:

- `tracker.project_number` — the project's number, the entry point every other lookup starts from.
- `tracker.board.field_id` — the Status field's ID.
- `tracker.board.options.<column>` — one option ID per configured column.

`scrumia-board columns` returns the field id and every option id in the shape above — run it and copy the result rather than composing `gh project field-list` by hand. Readers of these fields: `scrumia-ticket` (card moves at execution), `scrumia-status` (board read), `scrumia-refine` (`Backlog` → `Ready for dev`), all of them through `scrumia-board`. The syntax and the traps behind it are in [`scrumia-status`'s reference](${CLAUDE_SKILL_DIR}/../scrumia-status/references/projects-v2.md).

Once written, verify the whole chain in one call:

```bash
scrumia-board doctor
```

It reports authentication, the `project` scope, and whether the board is actually reachable under the configured owner. A green `doctor` is the difference between "setup finished" and "setup will fail on the first ticket".

Write them into `.scrumia/config.yaml` under `tracker:`, next to `project` and `columns`:

```yaml
settings:
  tracker:
    project: "My project"
    columns: [Backlog, Ready for dev, To dev, In progress, In review, Done]
    project_number: 7
    board:
      field_id: "PVTSSF_xxxxx"
      options:                      # one option id per column, exactly as the board spells it
        Backlog: "xxxxxxx"
        Ready for dev: "xxxxxxx"
        To dev: "xxxxxxx"
        In progress: "xxxxxxx"
        In review: "xxxxxxx"
        Done: "xxxxxxx"
      flow:                         # which column plays which role — skills name the step, not the column
        ready: "Ready for dev"
        in_progress: "In progress"
        in_review: "In review"
        done: "Done"
```

`flow` is what lets ScrumIA adopt a board instead of imposing one. Skills ask to move a card to `in_progress`; the board may call that column `IN PROGRESS`, `Doing`, or anything else, and only this mapping has to know. On a board created by this skill the two sides look redundant — on an existing board they are not, and the redundancy costs four lines.

These IDs are stable once the board exists. Re-running this step compares them against a fresh `field-list` and reports drift instead of silently overwriting — same discipline as every other value this skill writes.

## Step 6 — Provide its composition line

```markdown
| Tracker | `scrumia-github-project` | Tickets, columns and PRs on GitHub. No state in the repository: no `sprint-status.md`, no `backlog.md`. A hook blocks their creation. |
```

## Step 7 — Report back

What was created, what already existed, what remains to be done by hand for lack of permissions.
