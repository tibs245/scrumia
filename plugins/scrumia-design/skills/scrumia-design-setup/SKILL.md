---
name: scrumia-design-setup
description: Installs the design system in a project — the design/ tree, its tokens and identity files, and the optional link to a Claude Design project. Invoked by scrumia-init when this module fills the design slot, or by hand to check the installation.
---

# Installing the design system

Creates the ground this module works on. Idempotent: run again, it checks without overwriting.

## What this module assumes

One thing only: the design system lives **in the repository, next to the code**. A remote Claude Design project is a review surface, not the source of truth.

That's a choice, not a given. It costs: designers review in a tool that mirrors the repo rather than owning it, and the mirror can go stale. It pays: the agent that writes a component reads the tokens in the same place as the code, offline, at the commit it is working on — and a design system that cannot be read at a given commit cannot be trusted by an agent.

## Step 1 — Read the configuration

In `.scrumia/config.yaml`:

```yaml
settings:
  design:
    root: "design"          # where the design system lives
    remote: claude-design   # claude-design | none — read by scrumia-design-sync
    project_id: null        # the claude.ai/design project UUID, once linked
```

If `settings.design` is absent, propose these defaults and write them. An implicit setting is a setting you cannot change.

**`settings.design.root` is this module's own setup-time choice — not what consumers read.** The authoritative value other modules act on is the `## Design contract` block `scrumia-init` copies into `CLAUDE.md` from this module's `## Composition block` (`skills/scrumia-design-system/SKILL.md`). If this step sets `root` to something other than that block's `design_root`, update the `## Composition block` to match, or tell the user to re-run `scrumia-init` so `CLAUDE.md` catches up.

## Step 2 — Create the tree

```
<root>/
├── identity.md
├── tokens.css
└── components/
```

A `.gitkeep` in `components/` while it is empty.

Do not scaffold example components. A design system seeded with a fake button teaches the project that its components are decorative.

## Step 3 — Write the identity

This is the step that cannot be automated, and the one the whole module rests on. Do not generate a plausible identity and move on — an invented identity is worse than none, because it will be cited.

Ask, and write down the answers:

- **What should someone feel** in the first three seconds? Name a feeling, not an adjective for the interface.
- **What must it never look like?** Usually the sharper answer. A named anti-reference decides more cases than a mood board.
- **What already carries the identity** — an existing deck, a product it should feel adjacent to, a palette in use somewhere?

If the project has no answer yet, say so in `identity.md` in one line and stop. A slot honestly marked empty is the ScrumIA default; a fabricated one is a lie the agents will act on.

## Step 4 — Seed the tokens

From the identity, not from a default palette. Each token is named for its **job**, never its value:

```css
:root {
  --surface: ...;        /* what a card sits on */
  --accent: ...;         /* the one thing the eye should find */
}
```

Cover only what the project actually uses today. An unused token is a decision nobody made.

Check contrast at this step, on the real pairs, in every theme the project ships. A palette that fails contrast is cheap to fix now and expensive once forty components consume it.

## Step 5 — Register the designer role

This module ships `scrumia-designer`, and a role is only routable if it appears in the single list the team module's Manager reads. Add it to `settings.team.roles` in `.scrumia/config.yaml`:

```yaml
    roles:
      - name: designer
        enabled: true
        from: scrumia-design    # names the providing module — see docs/adr/0014
```

The `from:` key is what tells `scrumia-team-setup` this entry is not its own to remove. If `settings.team` is absent because no team module is plugged in, skip this step and say so: the role definition still works when invoked directly, it is only the automatic routing that is missing.

## Step 6 — Link the remote, if any

Only if `settings.design.remote` is `claude-design`. Hand off to [scrumia-design-sync](../scrumia-design-sync/SKILL.md), Step 1: it lists the writable design-system projects, links or creates one, and writes `project_id` back into the configuration.

A project can stay at `remote: none` indefinitely. Everything in this module works without an upstream — the sync adds review by humans in a rendering tool, nothing more.

## Step 7 — Report

State what was created, what already existed, and what is still empty. Name the empty parts explicitly: an identity left blank at Step 3, or an unlinked remote, changes what the other skills can do — say which, rather than letting the next agent discover it.
