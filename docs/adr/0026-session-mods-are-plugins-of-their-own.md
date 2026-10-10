# ADR-0026 — A session mod is a plugin of its own, without a slot

**Status**: accepted — 2026-10-10

## Context

The questions inbox started as a proof of concept in PR #482, a Claude Code mod that lets
the model park a decision that is the person's instead of blocking the session on it. The
review of that PR asked where such a mod lives, since two more session mods are planned
beside it (a view of the tracker, a view of the roadmap) and the answer would be copied.

The candidates were an existing module, a plugin of its own, and one plugin grouping the
session mods. The plugin's name is part of the tool name the model calls
(`mcp__<plugin>__<tool>`), so the choice cannot be revisited once a project's prompts
and permissions name it.

## Decision

**Each session mod is a plugin of its own, and fills no slot.** The questions inbox is the
plugin `scrumia-questions`, whose tool is `mcp__scrumia-questions__ask_later`. Both names
are frozen at merge.

No slot: the composition's questions are answered by the specs, tracker, team, discovery
and design modules, and the inbox answers none of them. A project that leaves it out loses
nothing another module owes.

## Rejected alternatives

**`scrumia-core`.** Refused: its README says the kernel has no capability of its own; a mod
that adds a tool, a pane and a command to every session is a capability.

**`scrumia-github-project`.** Refused: the inbox needs no tracker, and a project on another
tracker would lose it.

**`scrumia-teams`.** The honest alternative: parking a decision for the human is the
escalation the roles already know. Refused because it would impose a hooks module on every
adopter of the team, and a project filling the team slot with another module would lose the
inbox with it.

**One plugin grouping the session mods.** Refused: they share a technique, not a need, and
a module is one concern (`features/business/module-anatomy/`, BR-2). A project wanting
the inbox would also install a view of the roadmap.

## Consequences

**What we gain**: each mod installs, versions and is removed alone, and its specification
is one section of `features/business/session-mods/`.

**What we accept**: three plugins to name and publish where one would do; the shared
technique (hooks modules, tests on a mocked surface) is repeated rather than factored.
This is reopened if the session mods come to share code a plugin cannot import from
another.
