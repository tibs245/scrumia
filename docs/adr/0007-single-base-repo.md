# ADR-0007 — A single base repo, not one repo per module

**Status**: accepted — 2026-08-07

## Context

BMAD separates: one repo for the base, and a distinct repo per external module (`bmad-builder`, `bmad-loop`, `bmad-game-dev-studio`…), referenced from a central `bmad-modules.yaml`. Six repos for the official ecosystem.

That separation is necessary at BMAD because the modules have different authors and independent release cycles (npm, `stable`/`next` channels).

ScrumIA has a single author.

## Decision

**A single repo**, which is both the marketplace and the full set of modules:

```
ScrumIA/
├── .claude-plugin/marketplace.json
├── plugins/
│   ├── scrumia-core/
│   ├── scrumia-specs/
│   ├── scrumia-github-project/
│   ├── scrumia-teams/
│   └── scrumia-discovery/
└── docs/
```

Marketplace entries use relative paths (`"source": "./plugins/scrumia-core"`).

A third-party module remains possible without changing this structure: `marketplace.json` accepts `github`, `git-subdir`, `npm` and `archive` sources for external entries.

## Consequences

**What we gain**

- A cross-cutting change (a convention touching all three modules) fits in a single, atomic PR. At BMAD, the same change requires coordinating several repos and synchronizing versions.
- One history, one CI, one set of issues.
- Relative paths avoid any network resolution between modules.

**What we accept**

- *Modules are versioned together* by the repo's tags. You cannot publish one module at v2 while keeping the core at v1. For a single author, that is more an advantage than a constraint: the modules share conventions, and desynchronizing them would create combinations to test for no benefit.
- *An external contributor wanting an independent module* will have to publish their own repo and their own entry. The case does not arise today, and `marketplace.json` supports it when it does.
- *The `version` field of each entry must be maintained by hand* at release time. To be automated in CI if the frequency justifies it.

## Rejected alternative

**One repo per module, BMAD-style.** Replicates a coordination cost that only exists because BMAD has multiple authors and multiple release channels. Without those constraints, it is pure complexity: three times more repos, CI and synchronization, for no gain.
