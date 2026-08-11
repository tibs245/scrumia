---
name: scrumia-compose
description: Inspects, modifies, or diagnoses the module composition of a ScrumIA project. Use it to find out which module does what, plug in a new one, replace one, or understand why a capability is missing.
---

# Compose

The composition is the choice of modules that drive a project. This skill reads it, modifies it, and checks that it is consistent.

## View the active composition

Read `.scrumia/config.yaml` and present:

- Each module in `extends`, and whether it is actually installed — read `enabledPlugins` in `.claude/settings.json` and `.claude/settings.local.json` (an agent cannot run the interactive `/plugin list`)
- What the project needs and nothing in `extends` covers, and what it loses as a result. `extends` lists only the modules that are there: an absence has no line of its own to read, so it is derived and reported, never looked up
- What each app is built against (`apps[].extends` — its implementation module and its practice modules in one unordered list), with the apps that name none
- **Each app's `path`** — required for per-app activation to resolve at all; flag any app entry missing it
- **Whether a per-app `CLAUDE.md` stub exists at `apps[].path`** for apps that have a module plugged in, and whether it still names the modules actually configured — a stale stub misleads an agent working inside that app just as a stale root section does
- Gaps between `.scrumia/config.yaml` and the `CLAUDE.md` section

A gap between the two is the most common defect: the config changed, `CLAUDE.md` didn't, and agents follow a stale composition. Offer to regenerate via `scrumia-init`.

## Plug in or replace a module

1. Check that the module is installed. If not, give the install command and stop.
2. Read its documentation to learn the settings it expects under `settings`.
3. Update `.scrumia/config.yaml` — add or remove the module's name in `extends`, project-level or under the app it is being plugged into. A config still written on the old `composition:` and per-app `practices:` keys is converted by `scrumia-init`; do not convert it here, and do not write a module into one spelling while the rest of the file uses the other.
4. Invoke its install skill if it exists.
5. Regenerate the `CLAUDE.md` section.
6. For a change to an app's `extends`, flag the app's per-app `CLAUDE.md` stub (if one exists at `apps[].path`) as out of date — `scrumia-init` checks and reports drift on it, it does not overwrite it for you.

**When replacing, delete nothing the old module produced.** Specs written in a module's format stay readable; tickets created in a tool stay there. Flag what becomes orphaned and let the user decide — a migration is a job in its own right, not a side effect of a config change.

## Diagnose

When something doesn't work, check in this order:

1. **Is the module installed and enabled?** A module present in the config but absent from `enabledPlugins` is invisible to the agent.
2. **Does `CLAUDE.md` reflect the config?** If not, agents read a stale composition.
3. **Does anything in `extends` cover the capability?** A capability nobody covers is not a failure. Just say which module would provide it.
4. **What does the app's `extends` name?** With no implementation module, the agent follows the conventions of neighboring code; with no practice module, the implementation module's conventions suffice — acceptable behavior, not an error.
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

On a view, that output is meant to be most of the answer already: the modules `extends` names, what nothing covers, and what each app is built against.

**One caveat, until the script moves to `extends`:** it still reads the retired `composition:` and per-app keys, so on a config written in the current schema it reports every module as `not declared` and every app as having none, and advises adding the slots back as explicit nulls. Say which modules `extends` actually names and that the script has not caught up — reading the config against a report that disagrees with it is this skill's job, not a paraphrase of a report you were told to relay.

What it does **not** claim is the rest of this skill's job. It reads `.scrumia/config.yaml` and only that — so it cannot tell you whether a named module is actually enabled in `.claude/settings.json`, whether the `CLAUDE.md` section still matches, or whether a per-app stub went stale. Those gaps are yours to check and report alongside its output. A status printer that guessed at them would be the least trustworthy thing in the composition.
