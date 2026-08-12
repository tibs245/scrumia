# ADR-0021 — `modules` keyed by source, with a settings cascade

**Status**: accepted — 2026-08-12

Supersedes the `extends:` key of [ADR-0019](0019-extends-replaces-composition-and-practices.md).
Everything else that ADR decided stands: `practices` is not a slot, the list is unordered,
and a module named nowhere is inert.

## Context

ADR-0019 replaced the slot-keyed `composition:` with a flat list, one day before this
decision. Three limits surfaced immediately, while specifying how a project extends
ScrumIA with modules of its own (`features/business/local-extension/`).

**One word carries two meanings.** `extends:` in `.scrumia/config.yaml` lists the modules
a project runs. `extends.json` inside a module lists the directives it contributes to
registers. A reader meeting both in the same session has no way to know they are unrelated,
and the second is the harder concept.

**A flat list cannot say where a module comes from.** ADR-0018 lets a module be reached by
name; nothing says which name resolves where. Once a module may live in a marketplace, in
a directory shared between a person's projects, or inside the project itself, the list
stops describing the composition — two machines read the same file and run different code.
The first draft of `local-extension` answered this with a second field beside each name,
which is a field to keep in sync with the name it annotates.

**`settings:` is still keyed by a slot that no longer exists.** ADR-0019 removed
`composition.specs` and left `settings.specs`. The configuration has a flat half and a
slot-keyed half, and nothing states which is authoritative for a module that reads both.

## Decision

**`modules:` — a mapping, keyed by the qualified source of each module a project runs.**

```yaml
modules:
  "tibs245/scrumia:scrumia-specs":
    params:
      root: features
  "tibs245/scrumia:scrumia-github-project": {}
  "local:acme-docs-rules": {}
  "shared:acme-conventions": {}

apps:
  - name: api
    path: apps/api
    modules:
      "tibs245/scrumia:scrumia-impl-rust": {}
      "tibs245/scrumia:scrumia-practice-tdd": {}
```

### The key is `<source>:<module>`, always

One grammar, no exception and no bare name. Three sources exist, matching the three
locations `features/business/local-extension/` defines:

| Source | Where the module is |
|---|---|
| `<owner>/<repo>` | a marketplace |
| `shared` | a directory of checkouts shared between a person's projects |
| `local` | inside the project |

A bare name was rejected: it makes the file's meaning depend on what happens to be
installed, which is the failure the qualified key exists to remove. The prefix also
retires the origin field the first `local-extension` draft carried — the origin is the
name, so the two cannot disagree.

Where a `shared` checkout sits on a given machine stays out of version control, in
`.scrumia/.env.local`. The key says *which of the three*; the environment says *where*.
No versioned file names a path outside the project.

### Settings cascade, in a stated order

A module's configuration is resolved from three layers, each overriding the one before:

1. `settings:` — what is no module's, versioned
2. `modules[<key>].params:` — this module's own, versioned, overriding the base
3. `.scrumia/config.local.yaml` — per-machine, **never committed**, overriding both

**A key one module reads moves into that module's `params:`.** Of the five `settings.*`
blocks this repository runs, `specs`, `design`, `tracker` and `autonomy` each have one
reader and descend; `team.roles` stays, because it declares the team rather than a module's
configuration and three modules read it. That migration is part of this decision rather
than a consequence left implicit — it is the half that makes `settings:` stop being keyed
by a vocabulary the composition retired.

`team.roles` also changes shape here: an entry becomes the agent's name and whether the
project wants it, and the `from:` field is deleted. It existed to name the module a role
came from, which was only necessary because the declaration sat outside that module; the
agent's own file already carries its description, and resolving a name to a runnable agent
is the harness's job. `features/business/agent-team/` owns that rule.

**Layer 3's cost is stated rather than hidden.** Two machines can resolve different values
from one repository, so a composition is reproducible in its *modules* — which the
qualified key guarantees — and not necessarily in its *values*. That is the price of a
per-machine override, and it is paid knowingly: the alternative, a versioned override
block, leaves a reader asking why the value was not edited in `settings:` directly.

The order is stated rather than implied, for the reason ADR-0019 gave about ESLint: a
reader brings a precedence reflex uninvited, and an order nobody can check is one that can
invert without anything failing.

### What does not change

`modules:` is unordered. A module installed and named nowhere is inert. `practices` is not
a slot. A contribution still names a **register and never a module** — `modules:` says who
runs, `extends.json` says what each contributes, and nesting the second under the first was
considered and rejected below.

## Arguments for

- One word, one meaning: the configuration says `modules`, a module says `extends`.
- The composition is reproducible **in its modules**: the same file resolves to the same
  set on any machine, or reports what it cannot reach. Values are a separate question,
  answered by layer 3 above.
- A local module costs one line and is expressible at all, which the flat list made
  impossible without a second field.
- `settings:` stops being the only half keyed by a retired vocabulary.

## Arguments against

- **It is more verbose in the majority case.** Three published modules now repeat their
  marketplace three times. Accepted: the repetition is what makes the file readable
  without knowing what is installed.
- **It changes a decision one day old.** ADR-0019 is not wrong about what it decided —
  flat, unordered, no slot key — and this ADR keeps all of it. What it changes is the key's
  name and shape, which ADR-0019 had no reason to question because local modules were not
  yet specified.
- **A migration, and larger than the key.** `scrumia-init` writes it, `scrumia-extends` and
  `compose-status.sh` read it, the site's composer emits it, and every project on `extends:`
  must be migrated. Beyond those: `tests/fixtures/composition-output.txt`,
  `check_composition_drift()` in `tools/validate.py`, `site/i18n/*/index.json`, this
  repository's own `CLAUDE.md` and `.scrumia/config.yaml`, and `scrumia-init`'s own skill
  text. Plus the `settings:` migration above, which is the larger half. The reader count is
  two, which is why the shape change is affordable; the writer count is what makes this a
  real piece of work rather than a rename.
- **A half-migrated file must not resolve to nothing.** Both readers currently gate on
  `has("extends")`, so a correctly migrated config makes them warn about
  `composition:`/`practices:` and resolve zero modules — and a register with no
  contributions is an *answer* under BR-1, so every table renders empty and nothing fails.
  The three-way precedence is stated in `features/business/modular-composition/`'s `tech.md`
  for that reason, and the empty composition is named rather than left silent.
- **Three homes for a setting.** The cascade is a rule to learn, and the boundary between
  layer 1 and layer 2 will be argued. Accepted because the alternative for layer 1 was
  making one module's block hold what three modules read, and the alternative for layer 3
  was no per-machine override at all.

## Rejected — a module's `extends:` nested under it

The shape considered first:

```yaml
modules:
  "tibs245/scrumia:scrumia-core":
    extends:
      - local:acme-docs-rules
```

It reads well and it does not work. A contribution names a register, never a module
(`modular-composition` BR-9), and that is what lets one fragment serve `implement`,
`review` and `audit` without being written three times. Attached to a module instead:

- house rules wanted by three registers opened by two different modules must be declared
  under each of them
- replacing the module they hang on takes them with it
- and in the example that prompted it, `scrumia-core` opens no register at all, so nothing
  attached there would reach anything

What the shape was reaching for already exists one level down, keyed by register rather
than by module: a project contributes directives in `.scrumia/extends.json`, with no module
of its own. That file is unchanged by this ADR.
