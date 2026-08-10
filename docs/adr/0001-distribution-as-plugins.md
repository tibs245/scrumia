# ADR-0001 — Distribution as native Claude Code plugins

**Status**: accepted — 2026-08-07
**Partly superseded by**: [0017](0017-version-bump-and-commit-signal.md) — 2026-08-10. The decision below stands as it was taken; one of its accepted costs, *"Versioning is coarser than per-module npm semver. We pin by tag and by commit, which is enough"*, no longer holds — a module's version now carries a promise a tag cannot. Nothing else here was edited.

## Context

BMAD distributes its base through an npm package with a CLI (`npx bmad install`), a YAML registry of external modules, a version `manifest.yaml`, and a copy of the files into each project's `_bmad/`. That amounts to roughly forty Node installer files to maintain.

That cost exists because BMAD targets several tools (Claude Code, Cursor, Codex…). ScrumIA deliberately locks itself to Claude Code.

Claude Code natively provides a marketplace and plugin system that covers the same need: catalog, installation, updates, scopes, version pinning.

## Decision

ScrumIA is distributed as a **Claude Code plugin marketplace**. No CLI, no installer, no files copied into projects.

A project declares what it uses in its committed `.claude/settings.json`:

```json
{
  "extraKnownMarketplaces": {
    "scrumia": { "source": { "source": "github", "repo": "tibs245/scrumia" } }
  },
  "enabledPlugins": { "scrumia-core@scrumia": true }
}
```

## Consequences

**What we gain**

- Zero installation code to maintain. The mechanism is Claude Code's.
- The module selection is versioned with the project: it goes through PR, it has a `git blame`.
- Three scopes available: user (`~/.claude/settings.json`), project (`.claude/settings.json`, committed, shared), local (`.claude/settings.local.json`, gitignored).
- Real pinning: each plugin entry in `marketplace.json` accepts `ref` (branch or tag) and `sha` (exact commit). That is stronger than BMAD's `manifest.yaml`, which pins nothing verifiable.
- Optional automatic updates, per marketplace.
- Native access to `agents/`, `hooks/`, `skills/`, `monitors/`, `bin/`, `.mcp.json`.

**What we accept**

- *Plugin content is not in the project repo.* It lives in the user cache (`~/.claude/plugins/cache/`). A project cloned without network access has no tooling. Acceptable: the tooling is not the deliverable, and `CLAUDE_CODE_PLUGIN_SEED_DIR` covers the CI/container case.
- *Marketplace state is per user, not per project* (`~/.claude/plugins/known_marketplaces.json`). Two projects of the same user cannot track two different versions of the base under the same marketplace name. Workaround if the need arises: name by major version (`scrumia-v1`, `scrumia-v2`). For personal use, a single version of the base is preferable anyway.
- *Versioning is coarser than per-module npm semver.* We pin by tag and by commit, which is enough.
- *Plugin subagents ignore* `hooks`, `mcpServers` and `permissionMode` in their frontmatter. Hooks therefore go through `hooks/hooks.json` at the plugin level. A real constraint, with no impact on the chosen design.

## Rejected alternatives

**BMAD-style npm CLI.** Replicates a mechanism Claude Code already provides, with a permanent maintenance cost, for a single target tool. The only net advantage would be fine-grained per-module semver — not enough to justify the installer.

**Hybrid (plugins + init script).** Project initialization is a real need, but it doesn't need to be a script: it's a core skill (`scrumia-init`), which benefits from the project's context and can ask questions. A shell script would do worse for more.
