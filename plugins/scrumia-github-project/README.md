# scrumia-github-project

The tracker slot: issues, sub-issues, GitHub Projects columns, branches and PRs — the
whole path from a backlog ticket to a merged change, with state living on the board and
nowhere in the repository.

## What it answers

Where a project's state actually lives, and how a ticket moves through it: refine a
backlog item into something executable, run it in an isolated worktree to an open PR,
review that PR by what its diff actually touches, and take stock of the board without
truncating it at 30 items.

## What it refuses

- No state file in the repository. A `PreToolUse` hook blocks writing `sprint-status.md`,
  `backlog.md`, `todo.md` and their like — the board is the only source of truth.
- No merge. `scrumia-ticket` and `scrumia-review` stop at an open PR, except what
  `settings.autonomy.auto_merge` explicitly allows.
- No composed `gh project` call from outside `scrumia-board`. A board read without its
  filters silently truncates; every consumer, inside this module or out, goes through the
  one script that applies them.

## What it ships

| Skill | Role |
|---|---|
| `scrumia-project-setup` | Provisions the board's columns, labels and issue templates. |
| `scrumia-refine` | Brings a backlog ticket to "ready for dev": acceptance criteria, scope and risk labels, a split if it is oversized. |
| `scrumia-ticket` | Executes one ticket end to end — isolated worktree, spec first, implementation, tests, review, PR. Never merges. |
| `scrumia-review` | Reviews an open PR by routing to the reviewers its diff actually calls for. |
| `scrumia-status` | A read-only snapshot of the board, the features and the gaps between them — computed live, nothing stored. |
| `scrumia-board` | Published on `PATH`. The only way any skill or human talks to the board: `move`, `find`, `read`, `ready`, `epic`, `doctor`. |
| `/refine`, `/ticket`, `/review`, `/status` | Slash commands — each loads the matching skill above and passes its arguments through. |

## Settings it reads

Under `settings.tracker` in `.scrumia/config.yaml`: the project's owner and number, the
board's field and column ids, and the flow-step → column mapping `scrumia-board move`
resolves through. `scrumia-refine`, `scrumia-review` and `scrumia-ticket` also read
`settings.autonomy.level` and `settings.autonomy.auto_merge`.

## What it expects to find

An authenticated `gh` with the `project` scope, a git repository with a GitHub remote, and
a GitHub Project (v2) board — `scrumia-board doctor` checks reachability. A specs module
and a team module are each optional: every skill here degrades gracefully — spec updates
skipped, review done solo — when one is absent.
