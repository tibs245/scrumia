# ScrumIA

My AI workflow, as modules you can replace.

Running a project with an AI raises a handful of questions — where specs live, how work is tracked, who decides what, how code is written. None has a universal answer. ScrumIA separates them and gives each one a replaceable Claude Code module.

This is the composition I use. Yours will likely differ, and that is the point.

**📖 [Documentation site](https://tibs245.github.io/scrumia/)** — [English](https://tibs245.github.io/scrumia/) · [Français](https://tibs245.github.io/scrumia/fr/)

## Where it comes from

Six months of building with Claude Code and BMAD. BMAD taught me a lot, and plenty of it remains here: a modular base, versioned installations, tooling kept separate from the projects that use it.

What changed is the starting assumption. I don't believe there is a single right answer to how a project should be run with an AI — not BMAD's, not mine. What I can share is a set of separable parts, each with its reasoning, so you keep what fits and replace the rest.

**What aims to be reusable is the composition — not the answers I put in it.**

## The slots

A slot is a question. A module is one answer.

| Slot | The question | My module |
|---|---|---|
| `specs` | Where do specs live, in what shape? | `scrumia-specs` |
| `tracker` | Where does state live: tickets, columns, PRs? | `scrumia-github-project` |
| `team` | Which standing roles, with what scope? | `scrumia-teams` |
| `discovery` | How does an idea become framed work? | `scrumia-discovery` |
| `implementation` | How we code — **per app** | `scrumia-impl-rust`, `scrumia-impl-solidjs` |
| `practices` | Which cross-cutting practices — **per app** | `scrumia-practice-tdd`, `scrumia-practice-solid`, `scrumia-practice-tanstack-query` |
| `design` | Where does the design system live? | `scrumia-design` |

An empty slot is not a failure: it is a capability the project doesn't have, and agents adapt what they propose.

`implementation` and `practices` are the two multiple slots, mapped app by app. An implementation module owns the stack-specific "how" (Rust, SolidJS); a practice module owns one cross-cutting answer (TDD, SOLID, TanStack Query) that the implementation module situates for its stack. Where they disagree, specific beats generic — see [ADR-0010](docs/adr/0010-cross-cutting-practices.md).

Sitting beside `scrumia-core`, `scrumia-rules` fills no slot either: it is the rules-hierarchy format — index, guides, decisions — that lets a module's knowledge skill, or a project's own conventions, load only the guide a task routes to instead of one growing file. See [ADR-0011](docs/adr/0011-rules-hierarchy.md).

## How modules connect

Through generated documentation, not through resolution. `scrumia-init` reads `.scrumia/config.yaml` and writes into `CLAUDE.md` a table saying which module fills which slot. Agents read it like any project context.

A design based on declared verbs and dynamic resolution was rejected: the agent would have carried that indirection on every call, while a slot changes twice in a project's life. See [ADR-0009](docs/adr/0009-documented-composition.md).

## Prerequisites

- **git** — ScrumIA assumes a versioned repo.
- **`gh` CLI, authenticated** (`gh auth status`) — required by the GitHub tracker module; without it you lose issues, board and PRs, nothing else.
- **`jq`** — used by the tracker module's guard hook; without it the hook disables itself silently.

`scrumia-init` checks all three and tells you what degrades if one is missing.

## Installation

```bash
/plugin marketplace add tibs245/scrumia
/plugin install scrumia-core@scrumia
```

Then, in the repo to set up:

```
/scrumia-core:scrumia-init
```

The skill maps your apps, proposes a composition, offers the install command for each module the composition needs, lets each module install what it requires, and writes the composition into `CLAUDE.md`. Newly enabled plugins load at the next session — finish the init, then restart. Re-run, it verifies instead of overwriting.

The project versions only its selection, in a committed file:

```json
{
  "extraKnownMarketplaces": {
    "scrumia": { "source": { "source": "github", "repo": "tibs245/scrumia" } }
  },
  "enabledPlugins": {
    "scrumia-core@scrumia": true,
    "scrumia-specs@scrumia": true
  }
}
```

## Usage

Each step of the workflow has a command, carried by the module that owns that step:

```
/scrumia-core:next                  # where the project stands, and the step it calls for
/scrumia-teams:standup              # convene the roles
/scrumia-github-project:status      # state of the board
/scrumia-specs:feature <name>       # specify a feature
/scrumia-github-project:refine 42   # take a ticket to Ready for dev
/scrumia-github-project:ticket 42   # execute it end to end, up to the PR
/scrumia-teams:sprint               # run a batch, one isolated worktree per ticket
/scrumia-github-project:review 49   # review an open PR
```

Start with `next` when you don't know which applies: it reads the composition and the board, then names one step instead of listing them all. None of these merge — that stays with you.

The remaining skills are reached by name. They run once, or on demand, and don't belong in a flow:

```
/scrumia-discovery:scrumia-brainstorm   # frame an idea until it can be split
/scrumia-core:scrumia-compose           # what the composition is
/scrumia-impl-rust:scrumia-rust-audit   # audit an app before plugging a module in
/scrumia-practice-tdd:scrumia-tdd-audit
```

Roles are convened by `standup`, asked for in natural language — "ask the tech lead to review PR 17" — or run as a session's main agent:

```bash
claude --agent scrumia-teams:scrumia-manager
```

Installing or updating a module that ships agents requires a **restart**: `/reload-plugins` refreshes skills but not the roles, and the failure is silent — see `docs/agents.md`.

## Composing differently

| Situation | Composition |
|---|---|
| Personal script, one app | `core` + `specs` |
| Project in exploration | `core` + `specs` + `discovery` |
| Framed backlog, in production | all, plus one implementation module per app |
| Team already on Jira | `core` + `specs` + a tracker module to write |
| Stable code conventions | everything except `implementation` |
| Legacy code to bring under test | add `scrumia-practice-tdd`, start with its audit |

## Documentation

- [Composition](docs/composition.md) — the slots, the config, how to write a module
- [Architecture](docs/architecture.md) — the intent and the choices
- [Modules](docs/modules.md) — the twelve modules and their scope
- [Implementation modules](docs/modules-implementation.md) — the contract and how practices compose
- [The three roles](docs/agents.md)
- [Feature format](docs/format-feature.md)
- [The end-to-end flow](docs/dev-flow.md)
- [Architecture decisions](docs/adr/) — twelve ADRs, with their rejected alternatives
- [Roadmap](docs/roadmap.md)

## Repository layout

```
ScrumIA/                              ← the repo is also the marketplace
├── .claude-plugin/marketplace.json
├── plugins/
│   ├── scrumia-core/                 ← the kernel: describes the composition
│   ├── scrumia-rules/                ← slotless: the rules hierarchy
│   ├── scrumia-specs/
│   ├── scrumia-github-project/
│   ├── scrumia-teams/
│   ├── scrumia-discovery/
│   ├── scrumia-impl-rust/            ← implementation, per app
│   ├── scrumia-impl-solidjs/
│   ├── scrumia-practice-tdd/         ← cross-cutting practices, per app
│   ├── scrumia-practice-solid/
│   └── scrumia-practice-tanstack-query/
├── docs/
├── site/                             ← static site, EN at root, FR under fr/
├── tools/validate.py                 ← marketplace validation, run by CI
└── .github/workflows/                ← pages.yml (site), validate.yml (CI)
```

One repo for all modules ([ADR-0007](docs/adr/0007-single-base-repo.md)): a cross-cutting change fits in one atomic PR.

## Development

```bash
# Validate before publishing
python3 tools/validate.py
claude plugin validate .

# Test without installing
claude --plugin-dir ./plugins/scrumia-core
```

### The site

Static pages generated from one template per page plus one string file per language — no dependency beyond Python's standard library. English at the root, French under `fr/`; a key missing in either language fails the build, which is the anti-divergence guard.

```bash
# edit site/templates/*.html and site/i18n/{en,fr}/*.json, then:
python3 tools/build_site.py

# preview
python3 -m http.server -d site 8000
```

The generated pages are committed; CI rebuilds and fails if they drift. The `.github/workflows/pages.yml` workflow deploys on every push to `main` touching `site/`. To enable it once the repo is published: **Settings → Pages → Source: GitHub Actions**. Adding a language = one folder under `site/i18n/` and one entry in `LANGS` in `tools/build_site.py`.

## Status

Design settled, working skeleton, **not yet proven on a real project**. The next milestone is a pilot — see [the roadmap](docs/roadmap.md) for the questions it must answer.

One point deserves flagging: as long as a single module fills a slot, nothing proves that slot is truly replaceable. Writing a second `tracker` module is the real test of the architecture.
