---
name: scrumia-extend
description: The ScrumIA extension protocol — how a main skill opens a register, how any module contributes directives to it as pure data, and how scrumia-extends renders the table an agent picks from. Load it before writing or changing a module's extends.json, registers.json or dependencies.jsonl, or before adding an extension point to a skill.
---

# Extending a skill

A main skill states a **description** and a **goal**, and stops there. What it must
actually apply — the principles, the norms, the methods, the refusals — is not written
inside it. It is contributed by whichever modules the project runs, and assembled at the
moment the skill needs it:

```bash
scrumia-extends implement            # every directive that extends `implement` here
scrumia-extends implement --app api  # …plus the ones that app's own modules add
```

The skill gets a table. It takes what the task needs. Nothing about that table is written
into the skill, so a project that runs different modules gets different directives from
the same skill, and adding a module changes what the skill applies without editing it.

## The three files a module may ship

All three sit at the **module root**, next to `.claude-plugin/`. All three are pure data:
no path outside the module, no condition, no prose that instructs. A module ships the ones
it needs and omits the rest — omitting all three is a valid module.

The first two are JSON because they are keyed — a register groups its directives, and the
key is written once. The third is JSONL because it is a flat list, where a grouping key
would have nothing to group.

| File | Answers | Shape |
|---|---|---|
| `registers.json` | which registers this module **opens** | register → `{ skill, purpose }` |
| `extends.json` | what this module **contributes** | register → array of directives |
| `dependencies.jsonl` | what this module **runs** | one `<source>:<name>` per line |

### `registers.json` — what this module opens

A **register** is a named extension point. Opening one is a promise: this module has a
main skill that will ask for the register's directives and apply them.

```json
{
  "implement": {
    "skill": "scrumia-ticket",
    "purpose": "Write the code that satisfies a ticket's acceptance criteria"
  }
}
```

The register vocabulary is **open**. It is not a list this module owns and hands out: it
is the union of what every installed module opens, which is why a new module can introduce
a register nobody had, and why `scrumia-extends --list` is the only honest answer to
"which registers exist here".

### `extends.json` — what this module contributes

The keys are register names. **Nothing here names a consumer.** A module that contributes
SOLID does not know, and must not encode, which skill will read it — that is the whole
point, and it is why the same fragment reaches implementation, review and audit without
being written three times.

```json
{
  "implement": [
    { "name": "Single Responsibility",
      "type": "norm",
      "when": "required",
      "summary": "One reason to change per unit — where a responsibility is cut, and where it is not",
      "read": "skills/scrumia-solid-principles/guides/01-srp.md" }
  ]
}
```

| Field | Means |
|---|---|
| `name` | what the directive is called, as a reader would name it |
| `type` | `norm` (a rule that governs), `method` (a way of working that is offered), `refusal` (something this module forbids), `reference` (context, governs nothing) |
| `when` | `required` — applies to every unit of work in scope; `optional` — offered, the agent decides |
| `summary` | one line, what the fragment *says*, not what it is about |
| `read` | the fragment's path **inside this module**, resolved by the tool at print time |

`type` and `when` are open vocabularies too — an unknown value is printed as written
rather than rejected. What is *not* open is `read`: a path that leaves the module is
refused by `tools/validate.py`, for the reason
[ADR-0018](https://github.com/tibs245/scrumia/blob/main/docs/adr/0018-modules-reach-by-name.md)
gives.

### `dependencies.jsonl` — what this module runs

The outward edges, declared by the caller rather than inferred from prose. One record per
line, because the content is a list and nothing else — a wrapper object around a single
array would be ceremony, and a line-per-entry file appends cleanly and diffs as one line:

```jsonl
"tibs245/scrumia:scrumia-board"
"tibs245/scrumia:scrumia-pick-model"
```

A line is a published name. An object carrying one under `run` is accepted too, so a
second field can arrive later without every module's file changing shape at once.

`runs` lists the published names this module executes, each **qualified by its source** —
`<source>:<name>`, where the source is the marketplace the publishing module ships from
(`owner/repo` for a GitHub marketplace). The qualification exists because PATH is one flat
namespace shared with every enabled plugin: a bare `scrumia-board` says *which command*
and never *whose*, so two marketplaces publishing the same name resolve first-come, with
nothing to notice it.

**What is executed stays the bare name.** A skill runs `scrumia-board`, exactly as
[ADR-0018](https://github.com/tibs245/scrumia/blob/main/docs/adr/0018-modules-reach-by-name.md)
says; the source is a claim to check, not something to invoke. Qualifying it does not name
a module either — the dependency is still the name, not whoever publishes it this month;
what is added is *from which marketplace*, which is the thing that stays true when the
publishing module is renamed or replaced.

**Registers are not declared here.** A module that opens one has already said so in
`registers.json`, and that declaration *is* the promise to consult it — restating it as a
dependency would be a second list that must agree with the first and eventually will not.
Every register a module opens must appear in one of its own skills as
`scrumia-extends <register>`; `tools/validate.py` greps for exactly that, because a skill
that opens an extension point and never asks reads as covered and applies nothing.

`scrumia-extends --check` fails on a name nothing publishes, on a name whose actual
publisher ships from a different source than the one declared, on two modules opening the
same register, and on a contribution to a register nobody opens — that last one being the silent case:
directives that will never be printed, and nothing else would ever say so. An unqualified
entry is reported without failing: this repository's own validator refuses one, but a
consuming project is not blocked by another author's laxness. A publisher that declares no
repository makes the source *unchecked*, reported as such and never as a match.

## One fragment, several registers

A fragment is a file with **one scope, one purpose**: one principle, one method, one
refusal. That is what lets the same file appear under `implement`, under `review` and
under `audit` with a different `type`, a different `when` and a different `summary` each
time — the fragment states the rule once, and each register says what that rule *does*
there.

Splitting a skill into fragments is therefore not cosmetic. A guide that covers three
principles can only ever be contributed as a whole, to every register at once, at whatever
obligation level fits the loosest of the three.

## Where the order comes from

`scrumia-extends` prints project-local rows first, then the ones the app's own modules
contribute, then the project-wide ones; `required` before `optional` within a tier, then
alphabetical. **A module never ranks itself.** The precedence is the project's
composition — which modules it runs, and which of them it runs for which app — so
"specific beats generic, and a project override beats both" is expressed where the project
can see and change it.

A project adds its own rows in `.scrumia/extends.json`, same shape as a module's, read
first. That is how a house rule wins without forking the module it disagrees with.

## What the table does not do

**It does not arbitrate.** Two directives whose prose contradicts each other are both
printed, in the stated order, because a generator cannot read English. What changed is
that they are now visible in one place, which they never were when each lived in a
different module's prose.

**It does not resolve a slot.** Nothing here decides *which* module answers a question:
every module the project runs contributes, and the agent reads the whole table. There is
no lookup from a verb to a module, which is the thing
[ADR-0009](https://github.com/tibs245/scrumia/blob/main/docs/adr/0009-documented-composition.md)
rejected.

**It computes nothing that is stored.** There is no built artefact, no digest, no drift
gate — the table is produced when asked and thrown away. Nothing can be stale, and nothing
has to be committed after adding a module.

## Adding an extension point to a skill

1. Add the register to the module's `registers.json`, naming the skill and its purpose.
2. In the skill, at the step where the directives apply, run
   `scrumia-extends <register>` — with `--app` or `--path` when the work is an app's —
   and state that the rows are applied, `required` first.
3. Leave `dependencies.jsonl` alone — it lists names this module *runs*, not registers.
   A register you open belongs in `registers.json` and nowhere else.
4. Run `scrumia-extends --check`, then this repository's validator if you are working in
   it — step 2 is checked by a grep, not by a declaration.
