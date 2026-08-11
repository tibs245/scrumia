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

Then propose a composition. A need nobody covers is acceptable — the project runs in degraded mode, it just has to be said.

**Slot** is the word for the question you ask a human here — "which module fills this need" — and it is the only place that word does any work. The config below records modules, not slots.

| Slot | Role | Reference module |
|---|---|---|
| `specs` | Where specs live, in what shape | `scrumia-specs` |
| `tracker` | Where state lives: tickets, columns, PRs | `scrumia-github-project` |
| `team` | Standing roles and sprint execution | `scrumia-teams` |
| `discovery` | Scoping an idea into framed work | `scrumia-discovery` |
| `design` | The design system | `scrumia-design` |
| how an app is built, **per app** | what that app's code is written against — an implementation module, plus any cross-cutting practices | `scrumia-impl-rust`, `scrumia-impl-solidjs`, `scrumia-practice-tdd`, `scrumia-practice-solid` |

The last row is one question, not two, and it is asked once per app: a SolidJS app and a Rust app are built differently, and TDD applies to the API without applying to the prototype next door. Implementation and practices were always two answers at two granularities to that same question, so they are declared together, in the app's own list — never project-wide.

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
    # What this app is built against: its implementation module and its
    # cross-cutting practices, together. Omit the key for an app that has neither.
    extends: [scrumia-impl-rust, scrumia-practice-tdd]

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

**`extends` lists the modules that are there, and nothing else.** A module nobody chose is simply absent from the list — there is no `null` placeholder, because a flat list has no per-slot key to leave empty. That is a change of where the absence is written, not a decision to stop writing it: the need still exists whether or not a module covers it, and Step 8's report is what names it, rather than a line in this file ([ADR-0019](https://github.com/tibs245/scrumia/blob/main/docs/adr/0019-extends-replaces-composition-and-practices.md)). Writing `specs: null` back in to make the gap visible would put the same claim in two places, one of which goes stale.

**The list is not ordered.** It is shaped like ESLint's `extends` and carries none of its last-wins semantics: nothing in the composition is arbitrated by list position. Where two modules would both make the same decision — who moves a card, which model runs a ticket — that is a conflict to name to the user at composition time, not something the order settles.

**An app's `extends` carries its implementation module and its practice modules together**, in one list, because they are two answers to one question about that app. Precedence between them stays in prose and is unchanged: the implementation module wins over a practice module where they contradict each other, and a project override (`.scrumia/impl/<module>.md`, `.scrumia/practices/<module>.md`) wins over both. Do not try to read that order out of the list — the list has none.

`path` is required on every entry: it is what lets an agent, given the file it is about to touch, resolve which app's modules apply — without it, per-app activation has nothing to key on.

`roles[].model` is gone too, and its disappearance is the interesting one. A standing role's model lives in its agent's own frontmatter, which the platform reads at load time — no config key can change it at runtime, so the one that sat here only ever described the frontmatter without governing it. What replaces it is `execution.matrix`, which applies where a model is genuinely chosen at call time: the per-ticket executor `scrumia-sprint` launches. To change a standing role's model, edit its agent file; to change how tickets are executed, edit the matrix.

Two further keys an earlier version of this template carried are gone on purpose. `settings.specs.root` is superseded by the `## Specs contract` block (Step 5): the hard path lives in `CLAUDE.md` now, where every consumer already has to look; `scrumia-specs-setup` still proposes its own `root`/`strates` defaults if it needs them at install time, but this template no longer pre-seeds a value nothing here reads. `paths.adr` had no reader anywhere in the codebase — `docs/adr/` is a hard path stated directly in prose (`scrumia-tech`, `scrumia-rules`), which the house's anti-indirection stance prefers over a config key nobody consults. The cost: a project that genuinely wants a different ADR location has no config knob for it, only a doc to edit. If a module starts reading either key, put it back and name the reader.

## Step 3b — Migrate a project already written on `composition:`

`extends` replaced a `composition:` map keyed by slot, and per-app `implementation` and `practices` keys. Projects installed before that change still carry the old spelling, and there is no installer to run against them ([ADR-0001](https://github.com/tibs245/scrumia/blob/main/docs/adr/0001-distribution-as-plugins.md)) — this skill is the migration path. In verification mode, if the config on disk carries any of the three old keys, convert it and say what you did.

The conversion is mechanical:

| On disk | Becomes |
|---|---|
| `composition:` — each slot whose value names a module | one entry in the project-level `extends` list |
| `composition:` — each slot whose value is `null` | nothing. The slot key disappears; report each one dropped |
| `apps[].implementation` naming a module | an entry in that app's `extends` |
| `apps[].practices` — each module listed | an entry in that same app's `extends` |
| `apps[].implementation: null`, `apps[].practices: []` | nothing. An app left with an empty list carries no `extends` key at all |

Write the implementation module first in an app's list, for a reader's benefit only — the list carries no precedence, and a converted config must not be presented as though the order it came out in meant something.

**Name every dropped `null` in the report.** A slot deliberately left empty was a decision someone made, and the conversion deletes the only place that decision was written. The report is where it survives — "`design` was empty and is now simply absent from `extends`" — so the user can tell a converted gap from one this run invented.

**Never rewrite the old keys away silently, and never in the same pass that installs a project.** Show the conversion, then write it. Deleting a key a project's own tooling might still read is exactly the failure the window below exists to prevent.

**Both spellings keep working, for a window counted in releases.** `composition:` and the per-app keys stay readable through the release that deprecates them and the one after it, and may be removed no earlier than the second release after that — the window `features/business/release-versioning/` defines for anything a module publishes, which this is ([business.md](https://github.com/tibs245/scrumia/blob/main/features/business/release-versioning/business.md) § *What a module owes to be upgradable*). ADR-0019 says "one minor" in passing; the release-counted window is the one that governs, since `modular-composition` defers this question to `release-versioning` by name rather than answering it itself.

While the window is open, reading an old key emits **one** warning — naming the key, its replacement, and the fact that removal is coming — and then proceeds. Not one per key, not one per app: a config carrying `composition:` plus three apps still on both old per-app keys would otherwise emit seven, for a single decision the user has already been told about.

**If a config carries both `extends` and `composition:`, `extends` is what the project runs on.** Report the difference between the two rather than merging them: a stale `composition:` left beside a hand-edited `extends` is a leftover, and silently unioning the two would install modules nobody chose. Then offer to delete the leftover.

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

````markdown
<!-- scrumia:start -->
## ScrumIA composition

This project is driven by a composition of modules. Each module has a scope.
Before acting, check which module covers what you are about to do.

| Slot | Plugged module | What to know |
|---|---|---|
| Specs | `scrumia-specs` | Specs live in `features/`, per feature, as targeted files. |
| Tracking | `scrumia-github-project` | Tickets, columns and PRs on GitHub. Nothing in the repo. |
| Team | `scrumia-teams` | Standing roles: manager, business, tech. |
| Discovery | `scrumia-discovery` | An idea goes through scoping before becoming a ticket. |
| Design | `scrumia-design` | Identity, tokens and components in `design/`. Never inline a value. |

### What each app is built against

| App | Path | Extends |
|---|---|---|
| `web` | `apps/web` | `scrumia-impl-solidjs`, `scrumia-practice-tdd` |
| `api` | `apps/api` | `scrumia-impl-rust`, `scrumia-practice-tdd`, `scrumia-practice-solid` |

When you write code in an app, load the main skill of each module in its `extends`.
The implementation module wins over a generic practice; the project override
(`.scrumia/impl/`, `.scrumia/practices/`) wins over both — the list itself carries no
order and settles nothing. An app with an empty `extends` follows the neighboring
code's conventions.

Concretely: resolve the app from the path of the file you're about to edit (`apps[].path`
above), open the skill index (`SKILL.md`) of each module declared for that app, and load
only the guides its routing table points you to for the change at hand — not the whole
module. Within the app, stay inside each module's `section.json` globs; outside them, the
module has nothing to say and neighboring conventions apply.

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
<!-- scrumia:end -->
````

Write only the lines of modules actually plugged in. A table naming an absent module sends agents to a skill that doesn't exist.

**The `## Specs contract` block is copied, never composed.** If a specs module appears in `extends`, open that module's main `SKILL.md`, find its own `## Composition block` section, and copy that block verbatim under `## Specs contract` — do not write it from memory of `scrumia-specs`'s shape, another module may occupy the slot with different keys' values. This is ADR-0009's documented-composition rule applied to a module's internal vocabulary, formalized in `docs/adr/0012-specs-contract.md`: consumers (`scrumia-ticket`, `scrumia-split`, the team agents) read this block instead of hard-coding a specs module's file names.

**The `## Design contract` block follows the same rule**, copied from the plugged design module's `## Composition block` (`scrumia-design`: `skills/scrumia-design-system/SKILL.md`). Same reason, same discipline — and same omission when no design module appears in `extends`.

If no specs module appears in `extends`, write no `## Specs contract` section at all, and note its absence in the Step 8 report — a section with nothing to copy would either be blank or invented, and both are worse than omitted. On re-run, compare the block on disk against the plugged module's current `## Composition block` and report drift instead of silently overwriting — same discipline as every other marker section.

## Step 6 — Offer per-app `CLAUDE.md` stubs (optional)

For each app whose `extends` names at least one module, offer to write a short stub at `<path>/CLAUDE.md`, between markers so it can be checked and regenerated like the root section:

```markdown
<!-- scrumia:start -->
This app follows `scrumia-impl-solidjs`, `scrumia-practice-tdd`.
Before writing code here, read plugins/scrumia-impl-solidjs/skills/scrumia-solidjs/SKILL.md
and plugins/scrumia-practice-tdd/skills/scrumia-tdd/SKILL.md — load only the guides you need.
<!-- scrumia:end -->
```

This rides Claude Code's native nested-`CLAUDE.md` loading: an agent already working inside `apps/web/` picks up its scope without detouring through the root file first. Keep it to 3-5 lines — a pointer to the skill indexes, not a copy of their content.

An app with an empty or absent `extends` gets no stub — nothing to point to. On re-run, replace only what sits between the markers, same as the root file; content a project added outside them stays untouched. If the file exists with no markers at all, check it against the config, report drift, and ask before touching it — never overwrite unmarked content.

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

**Close by printing the composition instead of retyping it:**

```bash
${CLAUDE_SKILL_DIR}/../../scripts/compose-status.sh
```

Its output *is* the closing summary — what each declared need resolves to, what nothing covers, and the apps built against no module at all. Don't paraphrase it afterwards. A composition an agent retypes from memory drifts from `.scrumia/config.yaml` the moment one is edited and the other isn't, and the drift is invisible precisely because the prose still reads plausibly; the script re-reads the file on every run, so the user sees what the project is configured to do rather than what this session recalled.

A need the script reports as covered by nothing is **not** a defect in this skill's output. Under `extends` there is no key to write for it — the list names the modules that are there, and the report is where the gap is stated. Say it in the report as a gap the project owns, and name the module that would cover it; do not go back and invent a placeholder in the config to make the line disappear.

## What you don't do

- No commit: the user reviews.
- No sample spec or ticket.
- No rewriting of `CLAUDE.md` outside the markers, root or per-app.
- No creating an artifact that belongs to a module: its setup skill owns that.
