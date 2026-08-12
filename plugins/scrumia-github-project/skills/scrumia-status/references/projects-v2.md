# GitHub Projects v2 — operational reference

Skills don't talk to `gh project` directly. They call `scrumia-board`, which is the single implementation of everything below. This file explains **what the tool does and why**, so that a reader can extend it or diagnose it — not so that a skill can reimplement it.

Read by: whoever maintains `scrumia-board`. Called by: `scrumia-ticket`, `scrumia-status`, `scrumia-refine`, `scrumia-sprint`, `scrumia-project-setup`.

## The interface

| Command | Answers |
|---|---|
| `scrumia-board doctor` | Is auth, scope and board reachability in order? |
| `scrumia-board columns` | The Status field id and every option id |
| `scrumia-board find <issue>` | Which card is this issue, on which project? |
| `scrumia-board move <issue> <step>` | Move a card to a flow step |
| `scrumia-board read [--query Q] [--limit N]` | The board, grouped by status, filtered |
| `scrumia-board ready [--milestone M]` | What is ready to start, optionally for one sprint |
| `scrumia-board epic <issue>` | An epic and its native sub-issues |
| `scrumia-board issues --search <terms>` | Issues in every state — **not** the board |

Every command prints JSON on stdout and diagnostics on stderr. `SCRUMIA_CONFIG` overrides the config path.

`issues` is the one command here that leaves Projects v2 alone, and the distinction is the point rather than an implementation detail: a board read is scoped to live work — `Done` filtered out by default, and a discussion issue never carded at all — so a board search for something already settled comes back empty and reads as "never raised". It takes no `--state` flag — a search reaching only what is open cannot answer the question it exists for — and its answer carries `surface` and `states` so a board read can never be mistaken for it. It needs `project.repo` and nothing the board contributes, so it still answers on a project whose board ids are unresolved.

`read` lifts items labelled `discussion` out of `columns` into a `discussions` group, counted in `discussion_count`: an issue holding something unresolved is not work waiting to be started. It is separated, never dropped — `count` and `total_matching` still include it, and it is listed — because a read returning fewer items than the board holds is the filtered read that lies. The subtraction sits here rather than in each reading's prose so that neither the status nor the next-step reading can forget it on its own.

## Flow steps, not column names

Skills name a step — `ready`, `in_progress`, `in_review`, `done`. The board names a column, and it may name it anything. The mapping lives in `settings.tracker.board.flow`, and only `scrumia-board` consults it.

This is what lets ScrumIA adopt an existing board. On a board created by `scrumia-project-setup` the two sides read the same and the mapping looks redundant; on a board that already exists, with columns called `TODO`, `Ready to Dev` and `IN PROGRESS`, it is the only reason the skills keep working without renaming anything.

## The three traps

These are not hypotheticals. Each was found by running these commands against a live 95-item board on `gh` 2.96.

**1. `item-list` returns 30 items by default.** Not an error, not a warning — just the first page, shaped exactly like a complete answer. A skill that reads a 95-item board without `--limit` sees 30 cards and reports them as the board. `scrumia-board` always passes an explicit limit and compares the result against `totalCount`, which is why its output carries `truncated`.

**2. An invalid filter returns zero items, silently.** `--query 'zorglub:nawak'` yields `{"items": [], "totalCount": 0}` — byte for byte what a valid filter matching nothing returns. A typo, a column that doesn't exist, a milestone misspelled: all of them read as "nothing to do". `scrumia-board` re-reads the board unfiltered whenever a filtered read comes back empty, and sets `filter_suspect` when the board is demonstrably not empty. **Never report "nothing in progress" from a response carrying `filter_suspect: true`.**

A short but non-empty filtered read is the same trap with `totalCount` non-zero: the project search index can lag a just-made write by a few seconds, so a read taken right after a `move` can report 4 of 5 cards with nothing marking it incomplete (#26). `scrumia-board` re-issues a filtered, non-empty read and backs off until two consecutive counts agree — this changes no JSON field, so a caller sees the same shape whether the first read landed at rest or had to converge.

**3. Column matching is case-sensitive where it counts.** `field-list` returns option names verbatim, so `select(.name == "In progress")` finds nothing on a board whose column reads `IN PROGRESS` — and GitHub's own default is `In Progress`, with a capital P that the obvious spelling misses. `scrumia-board` falls back to a case-insensitive match and warns that config and board disagree, rather than failing on a capital letter.

Filter *values*, by contrast, are case-insensitive: `-status:DONE` and `-status:Done` return the same 57 items. The asymmetry is real — the filter syntax forgives, the JSON does not.

**4. A card added to a board has no Status at all.** `gh issue create --project "<title>"` and `gh project item-add` both put the card on the board and leave its Status empty — not `Backlog`, empty. It shows up in no column, and `read` groups it under `(no status)`. So the first column is not a default anything lands in: it has to be set, once, per card.

```bash
scrumia-board move <n> Backlog     # right after creating the issue
```

This is why `scrumia-board read` reports `(no status)` as its own group rather than folding those cards into the first column — a card nobody placed is a fact worth seeing, not one to paper over.

## Addressing beats enumerating

To move a card you need its `item-id`, which is not the issue number. The obvious way to get it is to list the board and search for the issue — which reintroduces trap 1 for every single move, and fails on any ticket past the limit.

`scrumia-board find` asks the issue for its card instead:

```bash
gh api graphql -f query='
  query($owner:String!,$repo:String!,$number:Int!){
    repository(owner:$owner,name:$repo){
      issue(number:$number){
        projectItems(first:20){ nodes{ id project{ id number title } } }
      }
    }
  }' -F owner=<owner> -F repo=<repo> -F number=<n>
```

One call, no pagination, and it returns the project's node id too — which `item-edit` requires. Board size becomes irrelevant. This is the same principle as filtering instead of scrolling, applied to a single card.

## Verified JSON shapes

Against `gh` 2.96, live board:

- `field-list` → `.fields[]` = `{id, name, type}`; a single-select field also carries `.options[]` = `{id, name}`
- `item-list` → `.items[]` = `{id, title, status, labels, repository, priority, content}`
- `.content` = `{number, type, title, url, body, repository}`, where `type` is exactly `Issue` or `PullRequest`
- `.totalCount` is the count **after** filtering, and is correct even when `--limit` truncates the items — which is what makes `truncated` exact rather than a guess

`item-edit` requires `--project-id` for non-draft items and updates **one field per invocation**. Omitting `--project-id` is the most common failure.

## Creating the board's columns

`gh project create` makes a board with `Todo` / `In Progress` / `Done` and offers **no** way to change them — no `gh` subcommand edits a single-select field's options. This is the one place `scrumia-board` doesn't cover, because it happens once at setup; do it in GraphQL:

```bash
gh api graphql -f query='
mutation {
  updateProjectV2Field(input: {
    fieldId: "<status-field-id>"
    singleSelectOptions: [
      {name: "Backlog",       color: GRAY,   description: "Raw intent, not yet refined"}
      {name: "Ready for dev", color: BLUE,   description: "Refined: criteria written, scope and risk set"}
      {name: "To dev",        color: PURPLE, description: "Selected into the current sprint"}
      {name: "In progress",   color: YELLOW, description: "Being executed in its own worktree"}
      {name: "In review",     color: ORANGE, description: "PR open, awaiting review"}
      {name: "Done",          color: GREEN,  description: "Merged"}
    ]
  }) { projectV2Field { ... on ProjectV2SingleSelectField { options { id name } } } }
}'
```

Three things to know. `name`, `color` and `description` are all **required** per option — omitting `description` fails the mutation. `color` is an enum, unquoted: `GRAY`, `BLUE`, `GREEN`, `YELLOW`, `ORANGE`, `RED`, `PINK`, `PURPLE`. And **the list replaces the field's options wholesale**: an option whose `id` you don't pass back is deleted, along with the status of every card sitting in it. Safe on a board you just created; on a populated board, pass the existing `id` for every option you intend to keep.

The mutation returns the new option ids — that is the moment to persist them, rather than re-reading them later.

## Milestones, epics, labels

The board stays readable through filing, not through pagination.

- **Milestones are sprints.** `scrumia-board ready --milestone "Sprint 12"` is a bounded question. Without the milestone, the same call returns the whole ready column.
- **Epics are native sub-issues.** `gh issue edit <parent> --add-sub-issue <child>` links them; `--json subIssuesSummary,parent` reads them; GitHub computes the progress. A checklist in the parent's body is a second count that drifts the moment a child closes without someone ticking the box.
- **Labels are filters.** `scope/*` and `risk/*` are read by `scrumia-pick-model`; `--query` selects on them server-side.

## Fallback

Any command can fail for reasons unrelated to the ticket: missing `project` scope, `project_number` absent, a `gh` too old, a renamed field. `scrumia-board doctor` names which one.

- **Reading the board** (`scrumia-status`) — fall back to `gh issue list --state open --json number,title,labels,assignees,createdAt` and `gh pr list --json number,title,isDraft,reviewDecision,headRefName`, and say plainly in the report that it reflects issue/PR state, not the board's columns.
- **Moving a card** (`scrumia-ticket`, `scrumia-refine`) — continue the ticket's own work regardless, and report the failed move. A dead column is not a blocked ticket.

Stale ids survive a column being renamed in place, but not one deleted and recreated. If a move fails with "field/option not found", re-run `scrumia-project-setup` to refresh them before assuming the board is broken.

## Verification status

Everything above was exercised against live boards on `gh` 2.96 — reads against a 95-item board, writes against a throwaway project since deleted.

The write path is confirmed end to end: `scrumia-board move` changed a card's Status and the board reflected it, the reverse move restored it, and a second board carrying the **same issue** was left untouched — which is what proves `find`'s project filter actually discriminates rather than returning the first card it sees. A column name absent from the config fails with the known columns listed, instead of silently doing nothing.

Two behaviours worth keeping in mind, both observed rather than assumed:

- A freshly created project ships `Todo` / `In Progress` / `Done` — note the capital P, which is exactly why the case-insensitive fallback exists.
- `totalCount` tracks the filtered count, so `truncated` is exact rather than inferred from whether the page came back full.

What is still unverified: nothing in this file. What is untested elsewhere is board **creation** with custom columns — `updateProjectV2Field` exists and can redefine the Status options, but `scrumia-project-setup` has not been run against a real board yet.
