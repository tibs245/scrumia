# Composition

This is ScrumIA's central idea, and the only thing it truly defends.

## The starting observation

Running a project with an AI raises a series of questions — where do specs live, how is progress tracked, who decides what, how is code written — and **none of them has a universal answer**. What works on a five-app monorepo doesn't work on a personal script. What suits a regulated team doesn't suit a weekend prototype.

A method that answers all these questions as one block forces you to take everything or leave everything. In practice you take, you adapt, you diverge, and you end up with a fork that no longer receives updates.

ScrumIA therefore separates the questions, and provides a replaceable answer to each.

## The slots

A slot is a question. A module is one answer.

| Slot | The question | Reference module |
|---|---|---|
| `specs` | Where do specs live, in what shape? | `scrumia-specs` |
| `tracker` | Where does state live: tickets, columns, PRs? | `scrumia-github-project` |
| `team` | Which standing roles, with what scope? | `scrumia-teams` |
| `discovery` | How does an idea become framed work? | `scrumia-discovery` |
| `implementation` | How we code — **per app** | `scrumia-impl-rust`, `scrumia-impl-solidjs` |
| `design` | Where does the design system live? | `scrumia-design` |

An empty slot is not a failure: it is a capability the project doesn't have, and agents adapt what they propose.

One slot is multiple and maps app by app:

- **`implementation`** — a SolidJS app and a Rust app share no stack. One module per stack.

An app lists more than its stack. A module that fills no slot at all — `scrumia-tdd`,
`scrumia-solid-principles` — refines one named point of the implementation contract and is
shared across stacks; the implementation module *situates* it for its own. Where they
disagree, **specific beats generic** — the implementation module wins, and the project
override wins over both. See [ADR-0019](adr/0019-extends-replaces-composition-and-practices.md).

## How modules connect

**Through generated documentation, not through resolution.**

`scrumia-init` reads `.scrumia/config.yaml` and writes into `CLAUDE.md` a section saying which module fills which slot, and what an agent must know about it:

```markdown
<!-- scrumia:start -->
## ScrumIA composition

| Slot | Plugged module | What to know |
|---|---|---|
| Specs | `scrumia-specs` | Specs live in `features/`, per feature, as targeted files. |
| Tracking | `scrumia-github-project` | Tickets, columns and PRs on GitHub. Nothing in the repo. |

### Per app

| App | Path | Modules |
|---|---|---|
| `web` | `apps/web` | `scrumia-impl-solidjs`, `scrumia-tdd` |
<!-- scrumia:end -->
```

The agent reads this table like any project context. There is nothing to resolve, nothing to query.

### From the table to the file: how a module is actually consumed

The table above says *which* module applies to an app. It does not say how much of that module an agent loads to make one edit — loading a whole implementation module's reference set for a one-line fix would burn context for no benefit. The consumption model has three steps:

1. **Resolve the app by path.** The file about to be touched is matched against `apps[].path`. Every app entry carries a `path`, precisely so this step never stalls for lack of a boundary to test against.
2. **Open the index, not the module.** Each module an app draws on exposes a skill index — its `SKILL.md` — and nothing else is read yet. A project can shortcut straight to it: `scrumia-init` can write, at `apps[].path`, a per-app `CLAUDE.md` stub naming the app's modules and pointing at their indexes, picked up by Claude Code's native nested-`CLAUDE.md` loading.
3. **Load only what the index routes to.** The index carries a routing table from kind-of-change to reference guide. Only the guides it selects for the task at hand are loaded — and only within the module's `section.json` globs, the file patterns it actually claims inside the app; outside them it has nothing to say.

`scrumia-ticket`'s implementation step (Step 4) runs exactly this procedure before writing any code. **Specific beats generic** still governs once guides are loaded: implementation module over the module it situates, project override (`.scrumia/overrides/`) over both. See [ADR-0011](adr/0011-rules-hierarchy.md).

### The specs contract

The composition table says *which* module fills the `specs` slot. It doesn't say what that module calls its own files — and for a long time nothing did, so `scrumia-ticket` and `scrumia-split` simply wrote `features/`, `qa.md`, `business.md`, `AC-n` into their own prose, as if `scrumia-specs`'s choices were universal. Swap the specs module and both keep reading and writing the wrong files, silently.

The fix is the same mechanism, one level down: `scrumia-specs` documents a fixed six-key vocabulary — `specs_root`, `feature_index`, `acceptance_file`, `ac_id_format`, `changelog`, `catalog` — in its own `SKILL.md`, and `scrumia-init` copies it verbatim into `CLAUDE.md`'s `## Specs contract` section. Consumers read the keys, never the specs module's own file names. A specs module absent from the composition means an absent `## Specs contract` block, and every consumer says so and degrades — it does not guess a layout. See [ADR-0012](adr/0012-specs-contract.md).

### Why not a capability registry

A first design planned declared verbs (`ticket.create`, `spec.read`) and resolution toward the plugged module. It was rejected: the agent would have had to hold that indirection in mind on every call, which costs reliability on all calls — while a slot changes a couple of times in a project's life.

The cost of the retained choice is real and owned: modules cite each other by name. Replacing the tracker module means checking the other modules that mention it. A few minutes of work, done rarely.

See [ADR-0009](adr/0009-documented-composition.md).

## The configuration

`.scrumia/config.yaml` describes the project and its tooling — never its state.

```yaml
project:
  name: "my-project"
  repo: "tibs245/my-project"

modules:
  "tibs245/scrumia:scrumia-specs":
    params:
      root: "features"
  "tibs245/scrumia:scrumia-github-project":
    params:
      project: "My project"
      columns: [Backlog, Ready for dev, To dev, In progress, In review, Done]
  "tibs245/scrumia:scrumia-teams":
    params:
      sprint:
        max_tickets: 5

apps:
  - name: web
    path: apps/web
    type: frontend
    modules:
      "tibs245/scrumia:scrumia-impl-solidjs": {}
      "tibs245/scrumia:scrumia-tdd": {}
  - name: api
    path: apps/api
    type: backend
    modules:
      "tibs245/scrumia:scrumia-impl-rust":
        params:
          test_runner: cargo
      "tibs245/scrumia:scrumia-tdd":
        params:
          ac_mapping: strict
      "tibs245/scrumia:scrumia-solid-principles": {}

settings:
  autonomy:
    level: guided
    auto_merge: none
  team:
    roles: [manager, business, tech]

paths:
  adr: "docs/adr"
```

Two conventions that matter:

- **A module the project does not run is simply not named.** Presence on disk is not participation: a module installed and named in no `modules` mapping is inert.
- **Each module documents the keys it reads** under its own `params:`; `settings:` holds only what several modules read. An implicit setting is a setting you can't change.

## Overriding without forking

A module must be adjustable by a project without being copied. Two mechanisms, available to every module an app draws on:

- **Declared settings** — the module documents what it reads under its own `params:`.
- **Project override file** — `.scrumia/overrides/<module>.md`. Its content wins over the module's own rules.

A module that provides neither will be forked at the first disagreement, and the fork will never receive updates.

## What a module must respect

Three rules, no more:

1. **Fill a slot** — an existing one, or a new one it defines and documents.
2. **Document its settings** under `settings.<slot>`.
3. **Provide its `CLAUDE.md` line** — the sentence that tells an agent what it must know without reading the module.

And one prohibition: **a module never assumes another is present**. If it needs an absent capability, it says so and proposes the next step, rather than failing.

## Composing differently

The reference composition is only an example — the one its author uses.

| Situation | Plausible composition |
|---|---|
| Personal script, single app | `core` + `specs` only |
| Project in exploration | `core` + `discovery` + `specs` |
| Framed backlog, in production | `core` + `specs` + `tracker` + `team` + one implementation module per app |
| Team already tooled on Jira | `core` + `specs` + a Jira tracker module to write |
| Code conventions already stable | everything except `implementation` |
| Legacy codebase to bring under test | add `scrumia-tdd` and start with its audit |

Writing a tracker module for Jira or Linear is bounded work: the slot is defined, the contract holds in three rules, and nothing else needs to change.

## What ScrumIA does not claim

That these splits are right for everyone. That the catalog-based feature format beats any other. That three roles is the right number.

These are choices, made for a context, documented with their alternatives in the [ADRs](adr/). What aims to be reusable is the separation into replaceable modules — not the answers put into them.
