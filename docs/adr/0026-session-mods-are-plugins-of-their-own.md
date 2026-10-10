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

No slot: the composition's six slots (`specs`, `tracker`, `team`, `discovery`,
`implementation`, `design`, listed by [ADR-0009](0009-documented-composition.md)) are filled
by the specs, tracker, team, discovery, implementation and design modules;
[ADR-0024](0024-no-category-of-module.md) settles that a module filling none of them is not
lesser for it, and the inbox fills none of them.
A project that leaves it out loses nothing another module owes.

This is the verdict of the review of PR #482: a plugin of its own, no slot, and
`scrumia-teams` the honest alternative, refused below.

## Rejected alternatives

**`scrumia-core`.** Refused: its README says the kernel has no capability of its own; a mod
that adds a tool, a pane and a command to every session is a capability.

**`scrumia-github-project`.** Refused: the inbox needs no tracker, and a project on another
tracker would lose it.

**`scrumia-teams`.** The honest alternative: parking a decision for the human is the
escalation the roles already know. Refused because it would impose a hooks module on every
adopter of the team, and a project filling the team slot with another module would lose the
inbox with it.

**One plugin grouping the session mods.** Refused for two reasons. Installing the inbox
would install the roadmap: a project wanting one would carry the other, and the three
could no longer be versioned or removed alone. And the project owner decided it so. No
rule of the repository says that a module is one concern (module-anatomy BR-2 is about
files: one file answers one question), so this is a choice, not a consequence of a rule;
they also share a technique, not a need.

## Consequences

**What we gain**: each mod installs, versions and is removed alone, and its specification
is one section of `features/business/session-mods/`.

**What we accept**: three plugins to name and publish where one would do; the shared
technique (hooks modules, tests on a mocked surface) is repeated rather than factored.
This is reopened if the session mods come to share code a plugin cannot import from
another.
