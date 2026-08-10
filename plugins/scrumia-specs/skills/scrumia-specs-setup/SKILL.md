---
name: scrumia-specs-setup
description: Installs the specs tree in a project — features/business and features/app per application. Invoked by scrumia-init when this module occupies the specs slot, or by hand to check the installation.
---

# Installing the specs

Creates the ground this module works on. Idempotent: run again, it checks without overwriting.

## What this module assumes

One thing only: the specs live **in the repository, next to the code**. No separate specs repository.

That's a choice, not a given. It costs: the repository grows, and the specs follow the code's lifecycle. It pays: no synchronization between two repositories, and the agent that implements reads the spec in the same place as the code.

## Step 1 — Read the configuration

In `.scrumia/config.yaml`:

```yaml
settings:
  specs:
    root: "features"        # where the specs live
    strates: [business, app]  # the chosen splitting
```

If `settings.specs` is absent, propose these defaults and write them. An implicit setting is a setting you cannot change.

**`settings.specs.root` is this module's own setup-time choice — not what consumers read.** The authoritative value other modules act on is the `## Specs contract` block `scrumia-init` copies into `CLAUDE.md` from this module's `## Composition block` (`skills/scrumia-feature/SKILL.md`, `docs/adr/0012-specs-contract.md`). If this step sets `root` to something other than that block's `specs_root`, update the `## Composition block` to match, or tell the user to re-run `scrumia-init` so `CLAUDE.md` catches up. `settings.specs.root` alone is read by nobody else, by design.

## Step 2 — Create the tree

```
<root>/
├── business/          # the "what" — business value, business rules
└── app/
    └── <app>/         # the "how" — one directory per declared app
```

A `.gitkeep` in each empty directory.

The apps come from `apps:` in the configuration. An app not listed there has no specs directory — that's consistent, not an oversight.

**No example feature.** An example never deleted becomes a reference by accident, and it's then harder to fix than to write.

Seed the global index too — run `python3 tools/build_features_index.py` from the repo root to write `<root>/index.md` (the file named by the contract's `global_index` key). Re-run it whenever the tree changes and the index would otherwise drift; the tool ships with this repo's own layout, so a project that vendors this module without its `tools/` directory regenerates the file some other way.

## Step 3 — Provide its composition line

This module describes itself in `CLAUDE.md`. Return to `scrumia-init` the line to insert:

```markdown
| Specs | `scrumia-specs` | Specs live in `features/`, one per feature, as targeted files. `index.md`, `business.md`, `qa.md` and `CHANGELOG.md` are mandatory; the rest exist only if they have content. See the `scrumia-feature` skill. |
```

## Step 4 — Report back

What was created, what already existed, the apps without a specs directory.

Then state what's next: `scrumia-feature` to write a first feature, or the scoping module if it's plugged in.
