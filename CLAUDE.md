<!-- scrumia:start -->
## ScrumIA composition

This project is driven by a composition of modules. Each module has a scope.
Before acting, check which module covers what you are about to do.

ScrumIA is the composition it ships: this repo runs on its own plugins.

| Slot | Plugged module | What to know |
|---|---|---|
| Specs | `scrumia-specs` | Specs live in `features/`, per feature, as targeted files. |
| Tracking | `scrumia-github-project` | Tickets, columns and PRs on GitHub. Nothing in the repo. |
| Team | `scrumia-teams` | Standing roles: manager, business, tech. Convene them with `scrumia-standup`. |
| Discovery | `scrumia-discovery` | Scope an idea before it becomes a ticket: `scrumia-brainstorm`, then `scrumia-split`. |
| Design | `scrumia-design` | Identity, tokens and components in `design/`. Never inline a value. |

`scrumia-design` also ships the `designer` standing role, registered in
`settings.team.roles` like the other three (`docs/adr/0014`). Route interface questions
to it — it is the only role that judges what a user actually sees.

### Implementation and practices, per app

| App | Path | Implementation | Practices |
|---|---|---|---|
| `site` | `site` | none | none |
| `tools` | `tools` | none | none |

Both apps carry no implementation module, so follow the conventions of the neighboring
code. `plugins/` is the product itself — markdown, not code — and is deliberately absent
from this table: no implementation module speaks for it.

When an implementation module does get plugged in, resolve the app from the path of the
file you're about to edit, open that module's `SKILL.md`, and load only the guides its
routing table points to. The implementation module wins over a generic practice; a
project override (`.scrumia/impl/`, `.scrumia/practices/`) wins over both.

### Specs contract

`scrumia-specs` — this project's specs module — describes itself with the block below.
Read the file named by `acceptance_file` for its acceptance criteria, identifiers in
`ac_id_format`; the other per-feature files it may carry are listed under `catalog`.

```
specs_root: features/
feature_index: index.md
acceptance_file: qa.md
ac_id_format: AC-<n>
changelog: CHANGELOG.md
catalog: business.md, legal.md, archi.md, api-contract.md, tech.md, ux.md, a11y.md, devx.md
```

### Design contract

`scrumia-design` — this project's design module — describes itself with the block below.
Read `identity_file` for the intent and `tokens_file` for the vocabulary before writing
any interface; `components_dir` holds one directory per component.

```
design_root: design/
identity_file: identity.md
tokens_file: tokens.css
components_dir: components/
component_preview: preview.html
component_spec: spec.md
card_marker: @dsCard
remote: claude-design
```

`site/` is the only app this contract applies to. `design/tokens.css` is the vocabulary;
`tools/build_site.py` mirrors it into `site/assets/tokens.css`, which is generated and
must never be edited. `site/assets/style.css` consumes those tokens and holds no literal
colour, spacing or duration of its own — a value it needs and the tokens do not carry is
a finding, not an exception.

### Shared rules

- Project state lives in the tracker, not in the repo.
- A spec contains only its current version; history lives in git and the tickets.
- The composition's configuration is in `.scrumia/config.yaml`.
- Talk to the board through `scrumia-github-project/scripts/board.sh`, never by composing
  `gh project` calls: a board read without a filter is silently truncated at 30 items.
- Before executing a ticket, ask `scrumia-teams/scripts/pick-model.sh <n>` which model it
  runs on, and act on its `instruction` rather than re-reading the matrix.
<!-- scrumia:end -->

## Working on this repo

The deliverable is prose that an agent executes. A skill that reads well but sends an
agent to a file that doesn't exist is broken, so `python3 tools/validate.py` gates the
marketplace, the frontmatter, every relative link, the scripts skills invoke, and the
skills commands hand off to. Run it before pushing; CI runs it too.

Files are in English — including comments, commit messages and workflow names. Only
`site/fr/` is French.

Comments earn their place by explaining a non-obvious **why**, roughly one line in ten.
Module narration and multi-paragraph docblocks belong in the PR body or in `docs/`.
