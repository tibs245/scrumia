---
name: scrumia-init
description: Installs or verifies a project's ScrumIA composition — creates .scrumia/config.yaml, the specs tree, and writes into CLAUDE.md which modules are plugged in and where. Use it on first installation, or after adding or changing a module.
---

# Installing the composition

ScrumIA does not ship a single method. It ships modules, and a project picks a **composition** of them. This skill installs the chosen composition and makes it readable by every agent.

Idempotent: run again, it compares and reports drift instead of overwriting.

## The principle

An agent does not guess which module does what. It reads it in `CLAUDE.md`, written by this skill from `.scrumia/config.yaml`.

Deliberately simple: no registry, no dynamic resolution. A plain sentence in `CLAUDE.md` is more reliable than an indirection the agent would have to hold in mind on every call.

## Step 0 — Check the prerequisites

Before anything else:

- **A git repository** (`git rev-parse --show-toplevel`). If not, stop: ScrumIA assumes a versioned repo.
- **`gh` authenticated** (`gh auth status`) — only needed if the tracker slot will be GitHub-based. If missing, say what will be degraded (no issues, no board, no PRs) and continue.
- **`jq` installed** — the tracker module's guard hook silently disables itself without it. If missing, say so; it is a one-line install.

Report what's missing in one block. Degrade explicitly, never silently.

If `.scrumia/config.yaml` already exists, you are in **verification mode**: compare, report, propose fixes one by one. Overwrite nothing.

## Step 1 — Map the project

Don't ask what you can deduce. Inspect:

- `apps/`, `packages/`, npm/pnpm workspaces, `turbo.json`, `Cargo.toml`, `go.work`
- Which applications exist, and above all **on which stack** — that determines each app's implementation module
- New project or existing one
- `git remote get-url origin` for the repo

Present what you found in one pass, and ask for confirmation.

## Step 2 — Establish the composition

List the installed modules by reading `enabledPlugins` in `.claude/settings.json` and `.claude/settings.local.json` (an agent cannot run the interactive `/plugin list`). It is an **object**, keyed by `"<plugin>@<marketplace>"`, whose value is a boolean:

```json
"enabledPlugins": {
  "scrumia-core@scrumia": true,
  "github@claude-plugins-official": false
}
```

Read the keys whose value is `true`, and split each on `@` to get the module name. **A key set to `false` is installed but disabled** — treating it as plugged in would promise a capability the session doesn't have. Check both files: a module enabled in `settings.local.json` is real but not shared with whoever clones the repo.

Then propose a composition. A need nothing covers is acceptable — the project runs in degraded mode, it just has to be said.

| Question | Reference module |
|---|---|
| Where specs live, in what shape | `scrumia-specs` |
| Where state lives: tickets, columns, PRs | `scrumia-github-project` |
| Standing roles and sprint execution | `scrumia-teams` |
| Scoping an idea into framed work | `scrumia-discovery` |
| How we code, **per app** | one module per stack (`scrumia-impl-rust`, `scrumia-impl-solidjs`) |
| Cross-cutting practices, **per app** | `scrumia-practice-tdd`, `scrumia-practice-solid` |
| The design system | `scrumia-design` |

The last two are declared **per app** rather than once for the project: a SolidJS app and a Rust app share no stack, and TDD can apply to the API and not to the prototype next door. Each app carries its own `extends` list for exactly that.

If a slot the user wants is not installed, give the command (`/plugin install <module>@scrumia`) and note that newly enabled plugins load **at the next session**.

## Step 3 — Write `.scrumia/config.yaml`

```yaml
# ScrumIA composition. Describes the project and its tooling, never its state.
project:
  name: "<name>"
  repo: "<owner>/<repo>"

# The modules this project runs. Flat, unordered, present modules only.
extends:
  - scrumia-specs
  - scrumia-github-project
  - scrumia-teams
  - scrumia-discovery
  - scrumia-design

apps:
  - name: "<app>"
    path: "apps/<app>"      # required, repo-relative — the boundary an agent resolves a file against
    type: "frontend | backend | mobile | worker | cli"
    extends: []             # this app's own modules, e.g. [scrumia-impl-rust, scrumia-practice-tdd]

# Settings passed to modules. Every key below is commented with what reads it —
# a setting with no named reader does not belong here (see CLAUDE.md instead).
settings:
  autonomy:
    level: guided            # guided | assisted | autonomous — read by scrumia-refine to gate ticket-transition approval; scrumia-ticket and scrumia-sprint read nothing here
    auto_merge: none         # none | docs-only | all — read by scrumia-review before merging, defaults to none
  team:                      # schema owned by scrumia-team-setup, written here in the exact shape it reads
    roles:                   # enabled is read by scrumia-manager, which routes only to active roles
      - name: manager
        enabled: true
      - name: business
        enabled: true
      - name: tech
        enabled: true
    execution:               # read by scrumia-pick-model, which scrumia-sprint and scrumia-ticket call before running a ticket
      unlabeled: sonnet      # ticket with no scope label: run here and ask for refinement, never guess a size
      unrated_risk: medium   # risk column assumed when the ticket carries no risk label — the answer says so
      labels:                # this project's own words for size and risk; the matrix below speaks S/M/L/XL and low..critical
        scope_prefix: "scope/"
        risk_prefix: "risk/"
      # Capability order, weakest to strongest: sonnet < opus < fable. The matrix
      # below climbs it; state it wherever the grid is seeded, because the model
      # names carry no ordering and an inverted grid still parses and still runs.
      # Opus is the ceiling a seeded grid may name: fable bills at twice opus per
      # token, so a human opts into it per ticket rather than a cell doing it for them.
      matrix:                # scope × risk → the model to run on, or split_or_<model> when the work is oversized
        S:  { low: sonnet,        medium: sonnet,        high: sonnet,        critical: opus }
        M:  { low: sonnet,        medium: opus,          high: opus,          critical: opus }
        L:  { low: opus,          medium: opus,          high: opus,          critical: opus }
        XL: { low: split_or_opus, medium: split_or_opus, high: split_or_opus,  critical: split_or_opus }
    escalation:
      to_human:               # read by scrumia-team-setup on re-run to check drift; the team agents' arbitration mirrors these defaults
        - disagreement between roles
        - missing business rule
        - contract change consumed by another app
    sprint:
      max_tickets: 5          # read by scrumia-sprint to cap the batch — beyond it, human review saturates
```

`extends` lists only what is present — a flat list has no per-slot key to leave empty, so a need nobody covers is reported rather than written back as a null. A module installed but named in no `extends` is inert: it is on disk, and this project does not run it. An app with no modules of its own carries `extends: []`; the surrounding code's conventions apply. `path` is required on every entry: it is what lets an agent, given the file it is about to touch, resolve which app's modules apply — without it, per-app activation has nothing to key on.

**The list is not ordered.** ESLint's `extends` carries last-wins semantics this one does not have: precedence is stated, never positional (see the `## Shared rules` block in Step 5).

`roles[].model` is gone too, and its disappearance is the interesting one. A standing role's model lives in its agent's own frontmatter, which the platform reads at load time — no config key can change it at runtime, so the one that sat here only ever described the frontmatter without governing it. What replaces it is `execution.matrix`, which applies where a model is genuinely chosen at call time: the per-ticket executor `scrumia-sprint` launches. To change a standing role's model, edit its agent file; to change how tickets are executed, edit the matrix.

Two further keys an earlier version of this template carried are gone on purpose. `settings.specs.root` is superseded by the `## Specs contract` block (Step 5): the hard path lives in `CLAUDE.md` now, where every consumer already has to look; `scrumia-specs-setup` still proposes its own `root`/`strates` defaults if it needs them at install time, but this template no longer pre-seeds a value nothing here reads. `paths.adr` had no reader anywhere in the codebase — `docs/adr/` is a hard path stated directly in prose (`scrumia-tech`, `scrumia-rules`), which the house's anti-indirection stance prefers over a config key nobody consults. The cost: a project that genuinely wants a different ADR location has no config knob for it, only a doc to edit. If a module starts reading either key, put it back and name the reader.

### Two neighbours of that file are never committed

`.scrumia/` holds one more pair, and both are per-machine by construction:

| File | Holds | Read by |
|---|---|---|
| `.scrumia/config.local.yaml` | this machine's overrides of `settings:` and a module's `params:` | the settings cascade |
| `.scrumia/.env.local` | `SCRUMIA_SHARED_DIR=<path>` — where a `shared:` module's checkout sits here | resolution |

**Make sure the project's `.gitignore` excludes both, and create neither.** They are
written by whoever installs on a machine, and a repository that commits either has put one
machine's layout into a versioned file — which is the thing the `<source>:<module>` key
exists to keep out of it (`features/business/local-extension/` BR-6). Their absence is the
correct state of a fresh clone: a module declared `shared:` then reports as a declared
absence, every register renders without it, and nothing fails.

A module the project ships to itself needs neither. It sits at
`.scrumia/modules/<module>/`, travels with the clone, and is declared `local:<module>`.

## Step 4 — Let each module install itself

The kernel does not know the modules' needs. For each plugged module, invoke its setup skill if it has one:

| Module | Setup skill | What it creates |
|---|---|---|
| `scrumia-specs` | `scrumia-specs-setup` | The specs tree |
| `scrumia-github-project` | `scrumia-project-setup` | Labels, issue templates, columns |
| `scrumia-teams` | `scrumia-team-setup` | Active roles, their models, escalation |

A module without a setup skill has nothing to create — implementation and practice modules configure nothing, they are loaded when coding. Never create in a module's place: the kernel must not know the specs format or the column names.

## Step 5 — Write the composition into `CLAUDE.md`

This is the step that makes the composition operative. Replace only what sits between the markers; create the file if it doesn't exist.

**Everything between `<!-- scrumia:start -->` and `<!-- scrumia:end -->` is generated, in full, by this step.** A re-run — first install, or after adding a module — replaces it wholesale. A skill, in this repository or any other module, must never depend on a hand-written sentence sitting inside that region: it survives only until the next `scrumia-init` run, and a fresh install never had it at all. Nor is the template the place to put it: a line added there reaches every project, whether it runs the module that needs it or not. A rule that belongs to a module is contributed by that module, as a directive under a register, and reaches an agent through `scrumia-extends` — the protocol is `scrumia-core`'s `scrumia-extend` skill. What stays in the template is the instruction to ask.

````markdown
<!-- scrumia:start -->
## ScrumIA composition

This project is driven by a composition of modules. Each module has a scope.
Before acting, check which module covers what you are about to do.

| Module | What to know |
|---|---|
| `scrumia-specs` | Specs live in `features/`, per feature, as targeted files. |
| `scrumia-github-project` | Tickets, columns and PRs on GitHub. Nothing in the repo. |
| `scrumia-teams` | Standing roles: manager, business, tech. |
| `scrumia-discovery` | An idea goes through scoping before becoming a ticket. |
| `scrumia-design` | Identity, tokens and components in `design/`. Never inline a value. |

### Per app

| App | Path | Extends |
|---|---|---|
| `web` | `apps/web` | `scrumia-impl-solidjs`, `scrumia-practice-tdd` |
| `api` | `apps/api` | `scrumia-impl-rust`, `scrumia-practice-tdd`, `scrumia-practice-solid` |

### What rules apply, and where they are written

Do not work this out from the tables above, and do not take one module's word for what
another one says. Ask:

```bash
scrumia-extends implement --path <the file you are about to edit>
scrumia-extends review --app <app>
scrumia-extends --list                    # every register the installed modules open
```

It prints one table — the directive's name, its type, whether it is required, one line of
what it says, and the file to open — assembled from the modules this project runs. Take
what the task needs; `required` rows apply to every unit of work in scope.

The order is computed, not authored: this project's own `.scrumia/extends.json` first,
then the modules an app extends, then the project-wide ones. That is *specific beats
generic, and a project override beats both*, and it is why `extends` carries no order of
its own. Nothing is stored — the table is computed when asked, so it cannot be stale, and
adding a module changes it with nothing to rebuild.

### Specs contract

`scrumia-specs` — this project's specs module — describes itself with the block below.
Read the file named by `acceptance_file` for its acceptance criteria, identifiers in
`ac_id_format`; the file named by `global_index` at the root of `specs_root` lists every
feature; the other per-feature files it may carry are listed under `catalog`.

```
specs_root: features/
feature_index: index.md
global_index: index.md
acceptance_file: qa.md
ac_id_format: AC-<n>
changelog: CHANGELOG.md
catalog: business.md, legal.md, archi.md, api-contract.md, tech.md, ux.md, security.md, devx.md
```

### Design contract

`scrumia-design` — this project's design module — describes itself with the block below.
Read `identity_file` for the intent and `tokens_file` for the vocabulary before writing
any interface; `components_dir` holds one directory per component.

```
design_root: design/
identity_file: identity.md
tokens_file: tokens.css
components_dir: components/
component_preview: preview.html
component_spec: spec.md
card_marker: @dsCard
remote: claude-design
```

### Shared rules

- Project state lives in the tracker, not in the repo.
- A spec contains only its current version; history lives in git and the tickets.
- The composition's configuration is in `.scrumia/config.yaml`.
- Before applying a rule that belongs to another module, ask `scrumia-extends <register>`
  for it. Never restate it from one module's prose about another, and never infer it from
  which modules are listed above.
<!-- scrumia:end -->
````

Write only the lines of modules actually plugged in. A table naming an absent module sends agents to a skill that doesn't exist.

**A module a clone will not be able to reach is named by its declaration key, never by its bare name.** This file is written on one machine and read on every other one, so a row saying `acme-conventions` claims a capability whoever cloned may simply not have; `shared:acme-conventions` states the module and where it would come from, which a reader can check. Run `scrumia-extends --claims` after writing the section and act on what it says — the rule is `features/business/local-extension/`'s AC-7, and it is the one thing in this table a re-run on the authoring machine cannot notice by itself.

**The `## Specs contract` block is copied, never composed.** If the `specs` slot is filled, open the plugged module's main `SKILL.md`, find its own `## Composition block` section, and copy that block verbatim under `## Specs contract` — do not write it from memory of `scrumia-specs`'s shape, another module may occupy the slot with different keys' values. This is ADR-0009's documented-composition rule applied to a module's internal vocabulary, formalized in `docs/adr/0012-specs-contract.md`: consumers (`scrumia-ticket`, `scrumia-split`, the team agents) read this block instead of hard-coding a specs module's file names.

**The `## Design contract` block follows the same rule**, copied from the plugged design module's `## Composition block` (`scrumia-design`: `skills/scrumia-design-system/SKILL.md`). Same reason, same discipline — and same omission when the slot is empty.

If the `specs` slot is empty (`composition.specs: null`), write no `## Specs contract` section at all, and note its absence in the Step 8 report — a section with nothing to copy would either be blank or invented, and both are worse than omitted. On re-run, compare the block on disk against the plugged module's current `## Composition block` and report drift instead of silently overwriting — same discipline as every other marker section.

## Step 6 — Offer per-app `CLAUDE.md` stubs (optional)

For each app that has at least one module plugged in (`implementation` set, or `practices` non-empty), offer to write a short stub at `<path>/CLAUDE.md`, between markers so it can be checked and regenerated like the root section:

```markdown
<!-- scrumia:start -->
This app follows `scrumia-impl-solidjs`, `scrumia-practice-tdd`.
Before writing code here, read plugins/scrumia-impl-solidjs/skills/scrumia-solidjs/SKILL.md
and plugins/scrumia-practice-tdd/skills/scrumia-tdd/SKILL.md — load only the guides you need.
<!-- scrumia:end -->
```

This rides Claude Code's native nested-`CLAUDE.md` loading: an agent already working inside `apps/web/` picks up its scope without detouring through the root file first. Keep it to 3-5 lines — a pointer to the skill indexes, not a copy of their content.

An app with no module plugged in gets no stub — nothing to point to. On re-run, replace only what sits between the markers, same as the root file; content a project added outside them stays untouched. If the file exists with no markers at all, check it against the config, report drift, and ask before touching it — never overwrite unmarked content.

## Step 7 — Enable the plugins for the project

The simplest path is to let the CLI write this file rather than editing it by hand — it produces exactly the shape below, and it also fetches the marketplace:

```bash
claude plugin marketplace add tibs245/scrumia --scope project
claude plugin install scrumia-core@scrumia --scope project    # one per module
```

If you do merge it by hand, **merge — don't overwrite**. `enabledPlugins` is an **object** keyed by `"<plugin>@<marketplace>"` with boolean values; add your keys to whatever is already there, and never rewrite the object wholesale (another marketplace's plugins live in the same one).

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

This file being committed, the composition is versioned with the project. Tell the user: plugins enabled here load **at the next Claude Code session** — finish the setup, then restart. Their `scripts/` keep their executable bit through the install, so nothing needs `chmod` afterwards.

## Step 8 — Report back

Summarize what this run *did*: what was created, what drifted, what remains to be done by hand. Then point the way based on the project's actual state: no spec → scoping; specs but no ticket → the tracker module; tickets ready → the team.

**Check the composition's edges, then close by printing it instead of retyping it:**

```bash
scrumia-extends --check
${CLAUDE_SKILL_DIR}/../../scripts/compose-status.sh
```

`scrumia-extends --check` reports the declared edges nothing satisfies: a published name
no installed module provides, a register a module reads that nobody opens, a contribution
to a register nobody opens. There is nothing to build and nothing to commit — the
directive table is computed on demand. A name reported missing usually means the plugin is
enabled but the session has not restarted since; say so rather than working around it.

Its output *is* the closing summary — the slot table, the slots left empty on purpose, the apps carrying no implementation module. Don't paraphrase it afterwards. A composition an agent retypes from memory drifts from `.scrumia/config.yaml` the moment one is edited and the other isn't, and the drift is invisible precisely because the prose still reads plausibly; the script re-reads the file on every run, so the user sees what the project is configured to do rather than what this session recalled.

If `--check` reports an unmet edge, that is a finding to report, not something to write back into the config: `extends` names the modules this project runs, and a gap it exposes is answered by plugging a module in or by accepting the gap — never by a placeholder that makes the check pass.

## What you don't do

- No commit: the user reviews.
- No sample spec or ticket.
- No rewriting of `CLAUDE.md` outside the markers, root or per-app.
- No creating an artifact that belongs to a module: its setup skill owns that.
