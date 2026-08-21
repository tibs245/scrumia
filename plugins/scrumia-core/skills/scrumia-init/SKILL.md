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

List the installed modules by reading `enabledPlugins` in `.claude/settings.json` and `.claude/settings.local.json`. (The interactive slash command `/plugin list` is for a human at the prompt; `claude plugin list --json` is the agent-runnable source — it returns `id`, `enabled`, `scope`, `installPath` and `projectPath`.) It is an **object**, keyed by `"<plugin>@<marketplace>"`, whose value is a boolean:

```json
"enabledPlugins": {
  "scrumia-core@scrumia": true,
  "github@claude-plugins-official": false
}
```

Read the keys whose value is `true`, and split each on `@` into the module's name and the marketplace it came from. **A key set to `false` is installed but disabled** — treating it as plugged in would promise a capability the session doesn't have. Check both files: a module enabled in `settings.local.json` is real but not shared with whoever clones the repo.

The half after the `@` is a local alias, not a source. Resolve it through `extraKnownMarketplaces` in the same file — `"scrumia": { "source": { "repo": "tibs245/scrumia" } }` — and it is `tibs245/scrumia` that keys the module in Step 3. Two projects can alias the same marketplace differently, so the alias is exactly what must not reach a versioned file.

Then propose a composition. A need nothing covers is acceptable — the project runs in degraded mode, it just has to be said.

| Question | Reference module |
|---|---|
| Where specs live, in what shape | `scrumia-specs` |
| Where state lives: tickets, columns, PRs | `scrumia-github-project` |
| Standing roles and sprint execution | `scrumia-teams` |
| Scoping an idea into framed work | `scrumia-discovery` |
| How we code, **per app** | one module per stack (`scrumia-impl-rust`, `scrumia-impl-solidjs`) |
| What sharpens how we code, **per app** | `scrumia-tdd`, `scrumia-solid-principles` |
| The design system | `scrumia-design` |

The last two are declared **per app** rather than once for the project: a SolidJS app and a Rust app share no stack, and TDD can apply to the API and not to the prototype next door. Each app carries its own `modules` mapping for exactly that.

If a slot the user wants is not installed, give the command (`/plugin install <module>@scrumia`) and note that newly enabled plugins load **at the next session**.

## Step 3 — Write `.scrumia/config.yaml`

```yaml
# ScrumIA composition. Describes the project and its tooling, never its state.
project:
  name: "<name>"
  repo: "<owner>/<repo>"

# The modules this project runs, keyed <source>:<module>. Unordered, present modules only.
# A module's own configuration sits under its `params:` — the key names its reader.
modules:
  "tibs245/scrumia:scrumia-specs":
    params:
      root: "features"
      strates: [business, app]

  "tibs245/scrumia:scrumia-github-project":
    params:
      autonomy:
        level: guided        # guided | assisted | autonomous — gates ticket-transition approval
        auto_merge: none     # none | docs-only | all — checked before a merge, defaults to none
      project: "<board name>"
      # The board's number, columns and field/option ids are the tracker module's to add
      # in Step 4 — it reads the board, so it is the only thing that can. Where it writes
      # them is its own to say; do not seed them here.

  "tibs245/scrumia:scrumia-teams":
    params:
      execution:             # scrumia-pick-model's grid; scrumia-sprint and scrumia-ticket ask it
        unlabeled: sonnet    # ticket with no scope label: run here and ask for refinement, never guess a size
        unrated_risk: medium # risk column assumed when the ticket carries no risk label — the answer says so
        labels:              # this project's own words for size and risk; the matrix speaks S/M/L/XL and low..critical
          scope_prefix: "scope/"
          risk_prefix: "risk/"
        # Capability order, weakest to strongest: sonnet < opus < fable. The matrix
        # below climbs it; state it wherever the grid is seeded, because the model
        # names carry no ordering and an inverted grid still parses and still runs.
        # Opus is the ceiling a seeded grid may name: fable bills at twice opus per
        # token, so a human opts into it per ticket rather than a cell doing it for them.
        matrix:              # scope × risk → the model to run on, or split_or_<model> when the work is oversized
          S:  { low: sonnet,        medium: sonnet,        high: sonnet,        critical: opus }
          M:  { low: sonnet,        medium: opus,          high: opus,          critical: opus }
          L:  { low: opus,          medium: opus,          high: opus,          critical: opus }
          XL: { low: split_or_opus, medium: split_or_opus, high: split_or_opus,  critical: split_or_opus }
      escalation:
        to_human:
          - disagreement between roles
          - missing business rule
          - contract change consumed by another app
      sprint:
        max_tickets: 5       # caps the batch — beyond it, human review saturates

  "tibs245/scrumia:scrumia-discovery": {}

  "tibs245/scrumia:scrumia-design":
    params:
      root: "design"

  # Delete this line unless the project ships a module to itself. Copied through as-is it
  # is a declared absence under a placeholder name, which resolves to nothing forever.
  "local:<house-module>": {}   # at .scrumia/modules/<house-module>/, travels with the clone

apps:
  - name: "<app>"
    path: "apps/<app>"      # required, repo-relative — the boundary an agent resolves a file against
    type: "frontend | backend | mobile | worker | cli"
    modules: {}             # this app's own, keyed the same way, e.g. "tibs245/scrumia:scrumia-impl-rust": {}

# Layer 1 of the cascade: what belongs to no single module. A block only one module
# reads belongs in that module's `params:` above, not here.
settings:
  team:                      # three modules read this: it declares the team, it is no module's configuration
    roles:
      - name: manager
        enabled: true
      - name: business
        enabled: true
      - name: tech
        enabled: true
```

**Every key is `<source>:<module>`, and a bare name is not one.** Three sources exist: a marketplace as `<owner>/<repo>`, `shared` for a directory of checkouts this machine holds, `local` for a module inside the project. A name with no source makes the file mean whatever happens to be installed, which is the failure the qualified key removes — the readers report it and resolve nothing for it, so writing one produces a file that parses and composes nothing.

`modules` names only what is present — a mapping has no per-slot key to leave empty, so a need nobody covers is reported rather than written back as a null. A module installed and named nowhere is inert: it is on disk, and this project does not run it. An app with no modules of its own carries `modules: {}`; the surrounding code's conventions apply. `path` is required on every entry: it is what lets an agent, given the file it is about to touch, resolve which app's modules apply — without it, per-app activation has nothing to key on.

**The mapping is not ordered.** ESLint's `extends` carries last-wins semantics this one does not have: precedence is stated, never positional (see the `## Shared rules` block in Step 5).

### Where a setting goes, and why the template stopped commenting most of them

A module's configuration resolves from three layers, each overriding the one before ([ADR-0021](https://github.com/tibs245/scrumia/blob/main/docs/adr/0021-modules-keyed-by-source.md)):

1. `settings:` — what is no module's, versioned
2. `modules["<source>:<module>"].params:` — that module's own, versioned, overriding the base
3. `.scrumia/config.local.yaml` — per-machine, never committed, overriding both

**A block one module reads goes in that module's `params:`.** The rule that every key here carry a comment naming its reader existed because `settings:` was one flat bag in which nothing said who read what; under `params:` the key above the block says it, and a comment restating it is one more thing to keep in sync. What still earns a comment is a value whose *meaning* is not obvious — a grid's capability order, an enum's spelling — and every key left in `settings:`, where the reader is genuinely not written down.

Dropping those comments removes a copy, not the answer: what a module reads is declared in that module's own `README.md`, which is where a project looks it up (`features/business/modular-composition/`'s *Out of scope*, handing it to `features/business/module-anatomy/`). A comment in a consumer's config was a second answer free to drift from the first.

The cost of layer 3 is stated rather than hidden: two machines resolve different values from one repository. A composition is reproducible in its **modules**, which the qualified key guarantees, and not necessarily in its **values**.

`roles[].model` is gone, and its disappearance is the interesting one. A standing role's model lives in its agent's own frontmatter, which the platform reads at load time — no config key can change it at runtime, so the one that sat here only ever described the frontmatter without governing it. What replaces it is `execution.matrix`, which applies where a model is genuinely chosen at call time: the per-ticket executor `scrumia-sprint` launches. To change a standing role's model, edit its agent file; to change how tickets are executed, edit the matrix.

`paths.adr` is gone too, and had no reader anywhere in the codebase — `docs/adr/` is a hard path stated directly in prose, which the house's anti-indirection stance prefers over a config key nobody consults. The cost: a project that genuinely wants a different ADR location has no config knob for it, only a doc to edit. If a module starts reading it, put it back — under that module's `params:`.

`specs.root` comes back, which an earlier version of this template had dropped. It was dropped as an unread duplicate of the `## Specs contract` block in Step 5, and the two answer different questions: the contract block is what a *consumer* reads to find the specs, and `params:` is what the specs module itself is configured with. Under a mapping keyed by its reader there is no longer a bag for it to get lost in.

### Migrating a configuration that predates this shape

Two retired shapes exist, and both are still read, with a warning on every call. How long that lasts is not this skill's to promise — the window is counted in releases by [`features/business/release-versioning/`](https://github.com/tibs245/scrumia/blob/main/features/business/release-versioning/business.md) § *What a module owes to be upgradable*, and the module's own changelog names the release that removes them. What is worth saying here is that leaving a project on a retired shape is not a neutral choice in the meantime: a warning that fires on every command is a warning nobody reads by the end of the week.

| What the file carries | What it becomes |
|---|---|
| `extends: [<name>, …]` | one `modules:` key per name, each sourced |
| `composition: {<slot>: <name>}` and `practices: [<name>]` | the same, slots discarded — `practices` is not a slot |
| `apps[].extends: []`, or the retired `apps[].implementation` and `apps[].practices` | that app's `modules: {}` |
| `settings.<block>` read by exactly one module | that module's `params:`, with the nest kept as written |
| `settings.<block>` several modules read | left in `settings:` |

**Source each name; never guess one.** Ask the resolver rather than searching the three tiers by hand — it already binds a bare name in any of them, and it is the only thing that can say *how many* answered:

```bash
scrumia-extends --modules --json     # run on the file as it still is, before the rewrite
```

Each name comes back with a `state` and the `roots` that answered it. Only one state is safe to write:

| `state` | What it means | What to write |
|---|---|---|
| `resolved` | exactly one directory answered | `local:` or `shared:` straight from `location`; for `marketplace`, the source below |
| `shadow` | several tiers answered, and the narrowest is in use | **nothing** — report all of them |
| `conflict` | two directories in one tier answered | **nothing** — report both |
| `absent` | nothing answered | **nothing** — report where it would have come from |

**A marketplace source is the module's own claim, not the marketplace you installed it from.** Take `<owner>/<repo>` from `repository` — or `homepage` — in the resolved root's `.claude-plugin/plugin.json`, stripped of scheme, host and any `.git`. That is the value the resolver matches a marketplace key against, so it is the only one that binds.

The alias in `extraKnownMarketplaces` is a **cross-check, not the source**. The two agree for a marketplace serving its own single repository and part company for a fork or an aggregator: fork `tibs245/scrumia` to `acme/scrumia`, install it under the alias `acme`, and the manifest still says `tibs245/scrumia` because forking does not rewrite it. Source from the alias there and every migrated key becomes a declared absence — the module stops contributing, every register renders shorter, and nothing fails, because `--check` inspects the modules it discovered and never the declarations. Where the two disagree, report it and let a person choose; a module whose manifest claims no repository at all cannot be sourced as a marketplace key, and is reported like an `absent` one.

**A name none of this sources is reported, not written.** Say which name, what its state was, and which directories answered; leave it out of the migrated file until a person says where it comes from. A key guessed onto a marketplace makes the file resolve to whatever that marketplace happens to publish under that name, which is precisely what the source exists to prevent. The rest of the migration still lands — one unsourced name is a gap to close, not a reason to leave the whole file on a retired key.

`shadow` is the other case worth being slow about. The reader picks the narrowest tier and says so on every call, which is right for something that resolves each time — but writing that choice into a versioned key freezes one machine's layout into the file, and the next machine to lose that local checkout reads a key that now names a module it never had. A name a person has not disambiguated is a name a migration does not get to disambiguate.

**Check the rewrite before you hand it over.** Run `scrumia-extends --modules` again on the migrated file and compare, name by name, against the run you started from: every key must resolve to the same root it resolved to before. A key that now reads `absent` was sourced wrong. Nothing else catches this — `--check` will not, and the tables will simply render shorter.

**Migrate the whole file in one pass, `settings:` included.** A file carrying `modules:` beside an unmigrated `settings.<block>` still resolves — layer 1 is read whole — but the block then belongs to no module, and the next person to move it has to work out who read it. Where a module's own text still names a retired nest, that module passes it to the resolver as `--legacy <nest>`; that is the module's to say, and not something to write back into the config.

**Do not migrate a file you have not been asked to.** In verification mode this is a drift to report with the table above and the sourcing it would produce, then apply on a yes — never an overwrite in passing.

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

A module without a setup skill has nothing to create — a module loaded when coding configures nothing. Never create in a module's place: the kernel must not know the specs format or the column names.

## Step 5 — Write the composition into `CLAUDE.md`

This is the step that makes the composition operative. Replace only what sits between the markers; create the file if it doesn't exist.

**Everything between `<!-- scrumia:start -->` and `<!-- scrumia:end -->` is generated, in full, by this step.** A re-run — first install, or after adding a module — replaces it wholesale. A skill, in this repository or any other module, must never depend on a hand-written sentence sitting inside that region: it survives only until the next `scrumia-init` run, and a fresh install never had it at all. Nor is the template the place to put it: a line added there reaches every project, whether it runs the module that needs it or not. A rule that belongs to a module is contributed by that module, as a directive under a register, and reaches an agent through `scrumia-extends` — the protocol is `scrumia-core`'s `scrumia-extend` skill. What stays in the template is the instruction to ask.

````markdown
<!-- scrumia:start -->
## ScrumIA composition

This project is driven by a composition of modules. Each module has a scope.
Before acting, check which module covers what you are about to do.

Each is named by the key it is declared under, `<source>:<module>` — the source is where
it comes from, and a module named without one is not declared at all.

| Module | What to know |
|---|---|
| `tibs245/scrumia:scrumia-specs` | Specs live in `features/`, per feature, as targeted files. |
| `tibs245/scrumia:scrumia-github-project` | Tickets, columns and PRs on GitHub. Nothing in the repo. |
| `tibs245/scrumia:scrumia-teams` | Standing roles: manager, business, tech. |
| `tibs245/scrumia:scrumia-discovery` | An idea goes through scoping before becoming a ticket. |
| `tibs245/scrumia:scrumia-design` | Identity, tokens and components in `design/`. Never inline a value. |
| `local:acme-house-rules` | This project's own module, at `.scrumia/modules/acme-house-rules/`. |

Each module's own configuration sits under its `params:` beside that key; `settings:`
holds only what several modules read. Read either through `scrumia-extends --settings`,
never out of the file — that is the one call that applies all three layers, the last of
them per-machine.

### Per app

| App | Path | Modules |
|---|---|---|
| `web` | `apps/web` | `tibs245/scrumia:scrumia-impl-solidjs`, `tibs245/scrumia:scrumia-tdd` |
| `api` | `apps/api` | `tibs245/scrumia:scrumia-impl-rust`, `tibs245/scrumia:scrumia-tdd`, `tibs245/scrumia:scrumia-solid-principles` |

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
then the app's own modules, then the project-wide ones. That is *specific beats generic,
and a project override beats both*, and it is why `modules` carries no order of its own.
Nothing is stored — the table is computed when asked, so it cannot be stale, and adding a
module changes it with nothing to rebuild.

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

**A module declared `shared:` is named in this table by its declaration key, never by its bare name.** That is the one location whose files travel with nobody: this section is written on one machine and read on every other, so a row saying `acme-conventions` claims a capability whoever clones may simply not have, while `shared:acme-conventions` states the module and where it would come from, which a reader can check. The rule is `features/business/local-extension/`'s AC-7. Apply it while writing, not by checking afterwards — on this machine the checkout resolves, so nothing run here can see the difference.

**The `## Specs contract` block is copied, never composed.** If the `specs` slot is filled, open the plugged module's main `SKILL.md`, find its own `## Composition block` section, and copy that block verbatim under `## Specs contract` — do not write it from memory of `scrumia-specs`'s shape, another module may occupy the slot with different keys' values. This is ADR-0009's documented-composition rule applied to a module's internal vocabulary, formalized in `docs/adr/0012-specs-contract.md`: consumers (`scrumia-ticket`, `scrumia-split`, the team agents) read this block instead of hard-coding a specs module's file names.

**The `## Design contract` block follows the same rule**, copied from the plugged design module's `## Composition block` (`scrumia-design`: `skills/scrumia-design-system/SKILL.md`). Same reason, same discipline — and same omission when the slot is empty.

If the `specs` slot is empty — no module in `modules:` answers that question — write no `## Specs contract` section at all, and note its absence in the Step 8 report — a section with nothing to copy would either be blank or invented, and both are worse than omitted. On re-run, compare the block on disk against the plugged module's current `## Composition block` and report drift instead of silently overwriting — same discipline as every other marker section.

## Step 6 — Offer per-app `CLAUDE.md` stubs (optional)

For each app whose own `modules` mapping carries at least one key, offer to write a short stub at `<path>/CLAUDE.md`, between markers so it can be checked and regenerated like the root section:

```markdown
<!-- scrumia:start -->
This app follows `scrumia-impl-solidjs`, `scrumia-tdd`.
Before writing code here, read plugins/scrumia-impl-solidjs/skills/scrumia-solidjs/SKILL.md
and plugins/scrumia-tdd/skills/scrumia-tdd/SKILL.md — load only the guides you need.
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

Its output *is* the closing summary — every module the project declares, under its key with its `params:`, and the apps with their own. Don't paraphrase it afterwards, and don't announce a section it did not print. A composition an agent retypes from memory drifts from `.scrumia/config.yaml` the moment one is edited and the other isn't, and the drift is invisible precisely because the prose still reads plausibly; the script re-reads the file on every run, so the user sees what the project is configured to do rather than what this session recalled.

If `--check` reports an unmet edge, that is a finding to report, not something to write back into the config: `modules` names the modules this project runs, and a gap it exposes is answered by plugging a module in or by accepting the gap — never by a placeholder that makes the check pass.

## What you don't do

- No commit: the user reviews.
- No sample spec or ticket.
- No rewriting of `CLAUDE.md` outside the markers, root or per-app.
- No creating an artifact that belongs to a module: its setup skill owns that.
