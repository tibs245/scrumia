---
name: scrumia-compose
description: Inspects, modifies, or diagnoses the module composition of a ScrumIA project. Use it to find out which module does what, plug in a new one, replace one, or understand why a capability is missing.
---

# Compose

The composition is the choice of modules that drive a project. This skill reads it, modifies it, and checks that it is consistent.

## View the active composition

Read `.scrumia/config.yaml` and present:

- Each slot, the plugged-in module, and whether it is actually installed — read `enabledPlugins` in `.claude/settings.json` and `.claude/settings.local.json` (an agent cannot run the interactive `/plugin list`)
- Empty slots, and what the project loses as a result
- Each app's own `extends` list (`apps[].extends`), with the apps that carry none
- **Each app's `path`** — required for per-app activation to resolve at all; flag any app entry missing it
- **Whether a per-app `CLAUDE.md` stub exists at `apps[].path`** for apps that have a module plugged in, and whether it still names the modules actually configured — a stale stub misleads an agent working inside that app just as a stale root section does
- Gaps between `.scrumia/config.yaml` and the `CLAUDE.md` section

A gap between the two is the most common defect: the config changed, `CLAUDE.md` didn't, and agents follow a stale composition. Offer to regenerate via `scrumia-init`.

## Where a module may be, and where it actually was

A module lives in one of three places, and the composition names which by the source half
of its key: `<owner>/<repo>` for a marketplace, `shared` for a directory of checkouts a
person shares between their projects, `local` for `.scrumia/modules/<module>/` inside the
project. The same artefact, the same anatomy standard, in all three — the rules are
`features/business/local-extension/`'s.

What the config says is a declaration. What resolution found is a fact, and they are not
the same question:

```bash
scrumia-extends --modules            # every declaration, and the location it resolved from
```

Four states come back, and each means something different to whoever is composing:

- **resolved** — bound to exactly one directory, which is printed. Nothing to do.
- **absent** — nothing answered it here. For a marketplace module, it is installed
  nowhere or the session has not been restarted; for `shared`, the machine has no
  `SCRUMIA_SHARED_DIR` in `.scrumia/.env.local`, or the checkout is not in it. This is the
  ordinary state of a fresh clone and it is not a failure: every register renders without
  that module, and the report says which capability is gone.
- **shadow** — the declaration names no location (the retired list shape does not), and
  more than one answered it. The narrowest is running. Nothing is broken; the fix is to
  key the declaration `<source>:<module>` so the file says which copy, rather than the
  resolver deciding. Propose it.
- **conflict** — two distinct modules answer one declaration. It binds neither, so that
  module contributes nothing anywhere. Say which two directories, and let the human
  choose; nothing here picks.

A capability that comes from `shared` is a capability the project cannot be handed to
someone else with. Say so when you plug one in — it is the cost of that location, and it
is only visible at the moment of choosing.

## What the composition claims, against what it resolves

`CLAUDE.md` resolves nothing. It is written once, on one machine, and read on every other
one — so a module it names by its bare name is a capability asserted to whoever cloned,
whether or not that clone can reach it. One command reconciles the two:

```bash
scrumia-extends --claims             # CLAUDE.md against the states above
```

Every declaration comes back with a verdict. `honoured` and `not claimed` need nothing.
`named as absent` means the file names the declaration key, so it states the source a
reader cannot reach — correct, and the shape to aim for. `claimed` is the defect, and it
exits non-zero: the file promises a capability this reader has no way to get. The fix is
one of two, and the human picks — name the module by its key so the file says where it
comes from, or say nothing about it there.

Run it on a clone, not only where the composition was written: on the authoring machine
everything resolves and the answer is vacuous. That asymmetry is the criterion, not a
limitation of the command — the rule is
`features/business/local-extension/`'s AC-7.

## Plug in or replace a module

1. Check that the module is installed, **and reachable from the location its key names** —
   `scrumia-extends --modules` answers both at once. If not, give the install command, or
   name the directory the checkout is missing from, and stop.
2. Read its documentation to learn the settings it expects under `settings`.
3. Update `.scrumia/config.yaml`.
4. Invoke its install skill if it exists.
5. Regenerate the `CLAUDE.md` section.
6. For an `implementation` or `practices` change, flag the app's per-app `CLAUDE.md` stub (if one exists at `apps[].path`) as out of date — `scrumia-init` checks and reports drift on it, it does not overwrite it for you.

**When replacing, delete nothing the old module produced.** Specs written in a module's format stay readable; tickets created in a tool stay there. Flag what becomes orphaned and let the user decide — a migration is a job in its own right, not a side effect of a config change.

## Diagnose

When something doesn't work, check in this order:

1. **Did the declaration resolve, and to what?** `scrumia-extends --modules` is the first call, not a later one: a module present in the config but absent from `enabledPlugins` — or missing from the shared directory, or answered by two directories at once — is invisible to the agent, and every register renders shorter with nothing else said. Read the state before reading anything else, and read a conflict as a stop: that module contributes nothing until someone picks.
2. **Does `CLAUDE.md` reflect the config, and does it survive a clone?** If not, agents read a stale composition. `scrumia-extends --claims` answers the second half, which staleness alone would miss: a file perfectly matching the config still lies to every clone when it names a module only one machine can reach.
3. **Is the slot empty?** A missing capability is not a failure. Just say which module would provide it.
4. **Does the app have an implementation module, and practices?** Without an implementation module, the agent follows the conventions of neighboring code; without practices, the implementation module's conventions suffice — acceptable behavior, not an error.
5. **Does the app have a `path`, and does its per-app `CLAUDE.md` stub (if any) match it?** No `path` means no per-app activation — an agent editing a file there can't resolve which app it belongs to. A stub naming modules that were since replaced is the same failure as a stale root section, one level down.
6. **Are the settings read by the right module?** Each module documents the keys it consumes under `settings`.

## Write a module

A module is an ordinary Claude Code plugin. What makes it a ScrumIA module comes down to three points:

1. **It occupies a slot** — `specs`, `tracker`, `team`, `discovery`, `implementation`, `practices`, `design`, or a new slot it defines and documents.
2. **It documents the settings it reads** under `settings.<slot>` in `.scrumia/config.yaml`.
3. **It provides the `CLAUDE.md` line that describes it** — one sentence that tells an agent what it needs to know, without forcing it to read the module.

A module never assumes another module is present. If it needs a missing capability, it says so and proposes the next step instead of failing.

A new slot is justified when a real project would want to fill it **differently**. Otherwise, it's one more skill in an existing module.

## What the composition is not

It is not a resolution system: no module queries a registry to find out who calls whom. Modules refer to each other by name, and `CLAUDE.md` says which one is plugged in.

This is a deliberate choice. An extra layer of indirection would cost reliability — the agent would have to keep it in mind on every call — for flexibility we don't need, since a slot rarely changes.

## End every pass by printing the composition

Whatever you did above — viewed, plugged in, replaced, diagnosed — close on the composition as it now stands, and let the script say it rather than saying it yourself:

```bash
${CLAUDE_SKILL_DIR}/../../scripts/compose-status.sh
```

On a view, that output is most of the answer already: the slots, their modules, the ones empty on purpose, and the per-app implementation and practices columns.

What it does **not** claim is the rest of this skill's job. It reads `.scrumia/config.yaml` and only that — it prints the declarations as written, resolving nothing — so it cannot tell you where a module actually came from, whether a named module is enabled in `.claude/settings.json`, whether the `CLAUDE.md` section still matches, or whether a per-app stub went stale. The first of those is `scrumia-extends --modules`, and the half of the third that a clone would trip on is `scrumia-extends --claims`; the rest are yours to check and report alongside its output. A status printer that guessed at them would be the least trustworthy thing in the composition.
