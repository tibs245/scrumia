# Architecture

## The intent

ScrumIA is a composition of Claude Code modules for steering a project. It comes from six months of using BMAD, from which it keeps a lot — the modular base, the versioned installation, the separation between tooling and project.

What changed is the starting conviction. On these topics, **nobody has the right answer**, and pretending otherwise forces you to take everything or leave everything. What suits a monorepo of five apps does not suit a personal script; what suits a regulated team does not suit a prototype.

So: separate the questions, provide a replaceable answer to each one, and document why that answer.

**What is meant to be reusable is the composition — not the answers we put into it.**

## The slots

| Slot | The question | Reference module |
|---|---|---|
| `specs` | Where do the specs live, in what form? | `scrumia-specs` |
| `tracker` | Where does state live: tickets, columns, PRs? | `scrumia-github-project` |
| `team` | Which standing roles, with what scope? | `scrumia-teams` |
| `discovery` | How does an idea become scoped work? | `scrumia-discovery` |
| `implementation` | How we code — **per app** | `scrumia-impl-rust`, `scrumia-impl-solidjs` |
| `practices` | Which cross-cutting practices — **per app** | `scrumia-practice-tdd`, `scrumia-practice-solid`, `scrumia-practice-tanstack-query` |
| `design` | Where does the design system live? | coming |

An empty slot is not a breakdown: it is a capability the project does not have, and the agents adapt what they propose.

The `scrumia-core` kernel fills no slot. It describes the composition and nothing else. `scrumia-rules` fills no slot either: it is the index/guides/decisions format a module's knowledge skill — or a project's own conventions — takes once it outgrows a single file, so an agent loads only the guide its task routes to. See [ADR-0011](adr/0011-rules-hierarchy.md).

Details in [`composition.md`](composition.md).

## How the modules plug in

Through generated documentation. `scrumia-init` reads `.scrumia/config.yaml` and writes into `CLAUDE.md` a table of the plugged-in modules. The agent reads it like any other project context — there is nothing to resolve.

A design based on declared verbs and dynamic resolution was rejected: the indirection would be paid on every call, while a slot changes a few times in a project's life. See [ADR-0009](adr/0009-documented-composition.md).

## The reference composition's choices

They are its author's, on his projects. Each one is a module, so each one can be replaced.

### `scrumia-specs` — per-feature specs, TDD-oriented

A feature is a directory of targeted files, created only if they have content. The absence of a file then becomes an assertion: no `legal.md` means "nothing legal at stake".

`qa.md` is central rather than an appendix: acceptance criteria carry stable identifiers, are written before the implementation, and become the tests.

The price: a bit more judgment at writing time than with a fixed template. See [`format-feature.md`](format-feature.md) and [ADR-0004](adr/0004-feature-splitting.md).

### `scrumia-github-project` — state outside the repo

Tickets, columns and PRs live in GitHub. The repo contains only what lasts: specs, code, architecture decisions.

The reasoning: a versioned state file has two writers, no lock and no consistency constraint — it drifts, and a wrong state gets noticed long after it was believed.

The price: dependency on GitHub, nothing readable offline. An equivalent module for Jira or Linear would fill the same slot differently. See [ADR-0008](adr/0008-state-lives-in-github.md).

### `scrumia-teams` — three roles, configurable

Manager (Opus), Business and Tech (Fable). Each boundary is a **refusal line**: without it, the three converge toward the same generalist agent.

Three is not a magic number — roles are enabled, disabled and added through configuration. See [`agents.md`](agents.md).

### `scrumia-discovery` — scoping produces a branch

An idea is challenged, split into features, and delivered like any other change: on a branch, in a PR, with the associated issues. The human reviews the design in the same tool as the code.

## Distribution

A single repo, which is also the marketplace:

```
ScrumIA/
├── .claude-plugin/marketplace.json
├── plugins/
│   ├── scrumia-core/              ← the kernel: describes the composition
│   ├── scrumia-specs/
│   ├── scrumia-github-project/
│   ├── scrumia-teams/
│   └── scrumia-discovery/
├── docs/
└── site/
```

On the project side, nothing is copied. Two keys in a committed file are enough:

```jsonc
// <project>/.claude/settings.json
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

The composition is therefore versioned with the project: it goes through a PR, it has a `git blame`. See [ADR-0001](adr/0001-distribution-as-plugins.md) and [ADR-0007](adr/0007-single-base-repo.md).

## What a project contains

```
my-project/
├── apps/                    ← the code
├── features/                ← if the specs module is plugged in
│   ├── business/
│   └── app/<app>/
├── docs/adr/
├── .scrumia/config.yaml     ← the composition and its settings
├── .claude/settings.json    ← the enabled modules
└── CLAUDE.md                ← the composition, in a delimited section
```

One repo per project. The feature lives next to the code it describes, so the agent that implements reads both in the same place.

## Documents

- [`composition.md`](composition.md) — the slots, the config, how to write a module
- [`modules.md`](modules.md) — the existing modules and their scope
- [`modules-implementation.md`](modules-implementation.md) — the contract of an implementation module
- [`agents.md`](agents.md) — the three roles
- [`format-feature.md`](format-feature.md) — the chosen spec format
- [`dev-flow.md`](dev-flow.md) — the end-to-end flow
- [`roadmap.md`](roadmap.md) — the current progress
- [`adr/`](adr/) — the decisions, with their rejected alternatives
