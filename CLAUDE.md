<!-- scrumia:start -->
## ScrumIA composition

This project is driven by a composition of modules. Each module has a scope.
Before acting, check which module covers what you are about to do.

ScrumIA is the composition it ships: this repo runs on its own plugins.

| Module | What to know |
|---|---|
| `scrumia-specs` | Specs live in `features/`, per feature, as targeted files. |
| `scrumia-github-project` | Tickets, columns and PRs on GitHub. Nothing in the repo. |
| `scrumia-teams` | Standing roles: manager, business, tech. Convene them with `scrumia-standup`. |
| `scrumia-discovery` | Scope an idea before it becomes a ticket: `scrumia-brainstorm`, then `scrumia-split`. |
| `scrumia-design` | Identity, tokens and components in `design/`. Never inline a value. |

`scrumia-design` also ships the `designer` standing role, registered in
`settings.team.roles` like the other three (`docs/adr/0014`). Route interface questions
to it — it is the only role that judges what a user actually sees.

### Per app

| App | Path | Extends |
|---|---|---|
| `site` | `site` | none |
| `tools` | `tools` | none |

Both apps extend nothing of their own, so follow the conventions of the neighbouring
code. `plugins/` is the product itself — markdown, not code — and is deliberately absent
from this table: no module speaks for it. `.scrumia/config.yaml` records that as
`build/apply-implementation: not-applicable` rather than leaving it to be inferred.

### What to load, and in what order

Do not work it out from the tables above. Ask:

```bash
scrumia-assemble load <action>          # e.g. build/execute-ticket, scoping/write-spec
```

It prints the contributing modules in the order that applies here, each with a resolved
path. Inside a module, that module's own routing table decides what to open next. The
built files live in `.scrumia/assemblies/`; they are generated, committed and gated —
edit the manifests, then run `scrumia-assemble build`, never the artefact.

### Specs contract

`scrumia-specs` — this project's specs module — describes itself with the block below.
Read the file named by `acceptance_file` for its acceptance criteria, identifiers in
`ac_id_format`; the file named by `global_index` at the root of `specs_root` lists every
feature; the other per-feature files it may carry are listed under `catalog`.

```
specs_root: features/
feature_index: index.md
global_index: index.md
acceptance_file: qa.md
ac_id_format: AC-<n>
changelog: CHANGELOG.md
catalog: business.md, legal.md, archi.md, api-contract.md, tech.md, ux.md, security.md, devx.md
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
- Talk to the board through `scrumia-board` — the name the tracker module publishes on
  PATH, never a path into it, and never a composed `gh project` call: a board read
  without a filter is silently truncated at 30 items.
- Before executing a ticket, ask `scrumia-pick-model <n>` which model it runs on, and act
  on its `instruction` rather than re-reading the matrix.
- Before acting on a step, ask `scrumia-assemble load <action>` what to open. Never
  recompose that yourself out of one module's prose about another.
<!-- scrumia:end -->

## Working on this repo

The deliverable is prose that an agent executes. A skill that reads well but sends an
agent to a file that doesn't exist is broken, so `python3 tools/validate.py` gates the
marketplace, the frontmatter, every relative link, the scripts skills invoke, and the
skills commands hand off to. Run it before pushing; CI runs it too.

Nothing written inside `plugins/<module>/` may resolve outside it — the rule is
`features/business/modular-composition/`'s BR-7, and `docs/adr/0018` says why a name on
PATH is not the resolution ADR-0009 rejected. Here that means: reach another module's
script by the name it publishes under its `bin/`, and cite this repository's own `docs/`
and `features/` by absolute URL. `tools/validate.py` refuses the rest.

Files are in English — including comments, commit messages and workflow names. Only
`site/fr/` is French.

A commit is `<type>(<scope>): <subject>` with a `Refs: #<n>` trailer, and its type comes
from the one vocabulary that also names branches and titles PRs — defined in
`docs/adr/0017-version-bump-and-commit-signal.md`, cited here and enumerated nowhere else.
The scope is mandatory: a module's version bump is derived from it. What each bump
promises is `features/business/release-versioning/`'s; where the close is written is
`features/business/github-tracking/`'s.

Comments earn their place by explaining a non-obvious **why**, roughly one line in ten.
Module narration and multi-paragraph docblocks belong in the PR body or in `docs/`.
