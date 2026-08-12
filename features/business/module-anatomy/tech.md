# Module anatomy — how the two surfaces resolve

What each surface reads, what it returns, and what it refuses to do. The rules they
enforce are `business.md`'s; this file states only how a consumer reaches them and what it
can rely on.

## Reached by name, never by path

The procedural check is published under `bin/` by the module that owns this standard,
which puts it on `PATH` for every enabled plugin. Its name is **`scrumia-module`**, and
the conformity verdict is its `check` subcommand:

```
scrumia-module check [<path>]     # judge one module; defaults to the working directory
scrumia-module check --json       # the same verdict, unrendered
```

A subcommand rather than a bare name, on one precedent and one expectation: `scrumia-board`
already carries subcommands, and authoring will need a sibling on the same noun rather than
a second binary answering about the same object.

A consumer invokes the name. It never composes a path into the owning module, for the
reason [ADR-0018](../../../docs/adr/0018-modules-reach-by-name.md) states and
`modular-composition`'s BR-7 enforces — a path into another module is exactly what this
tool reports as a finding.

This is also what makes it usable in a project that has never heard of this repository:
the name is on `PATH` because the module is installed, and nothing else has to be true.

## What it reads

A module's own tree, and nothing else. It does not read `.scrumia/config.yaml`, does not
ask which modules a project runs, and does not care whether the module it is checking is
installed — conformity is a property of the module, not of the composition it happens to
sit in.

That boundary is what lets it run on a module being authored, before it has been declared
anywhere. It is also what bounds it: a rule about the specs tree, or about the relationship
between two modules, is invisible from here and cannot be delegated to it.

**A directory is a module when it carries a plugin manifest at `.claude-plugin/plugin.json`.**
That file, and only that file, is the entry condition. A directory without one is refused
as not-a-module rather than judged against every rule it happens not to meet — which is
the difference between a usable refusal and an unbounded finding list on an arbitrary
folder.

## What it returns

A finding carries the module, the file, the rule and one line of what was not met. The
list is the output; the exit status separates five states that a single boolean would
collapse:

| State | Exit | Meaning |
|---|---|---|
| checked, no finding | `0` | the module meets the standard |
| the tool failed | `1` | a dependency is missing, an input could not be read |
| bad usage | `2` | an unknown flag, a missing argument |
| checked, findings | `3` | the module was fully read, and did not meet the standard |
| not a module | `4` | the target carries no plugin manifest |

**`1` and `2` are not free to reassign.** Every name already published from a
`plugins/*/bin/` — `scrumia-extends`, `scrumia-board` — exits `1` from `die()` and `2` from
`usage()`. This tool ships in the same directory as one of them, and a reader who learns
one convention there must not meet its inverse next door. So the two states this tool adds
take codes of their own rather than the two that were taken.

The consequence a consumer must hold: **a non-zero exit is not a finding.** `1` on a
missing `jq` and `3` on a malformed module are both non-zero and mean opposite things, so
a gate that branches on truthiness reports a clean module as non-conformant the day a
dependency goes missing.

The `not a module` state is why a boolean is not enough. A gate that treats it as "clean"
passes exactly the targets most likely to be broken, and one that treats it as "findings"
makes an unreadable directory look like a non-conformity.

`--json` is the same flag `scrumia-extends` already carries, and for the same reason: a
consumer filters, counts or annotates without parsing a table meant for a terminal. The
envelope is fixed here, because two independent surfaces must emit it and prose describing
four fields is not a schema two implementers converge on:

```json
{
  "ok": true,
  "state": "clean" | "findings" | "not_a_module" | "error",
  "module": "scrumia-teams",
  "findings": [
    { "module": "scrumia-teams",
      "file": "skills/scrumia-sprint/SKILL.md",
      "rule": "module-anatomy/BR-4",
      "message": "no README addressed to a reader who has not adopted the module" }
  ]
}
```

`state` is authoritative and a consumer never infers it from whether `findings` is empty.
`rule` is qualified by the feature that owns it — `module-anatomy/BR-4`,
`modular-composition/BR-7` — because both namespaces appear in one list and a bare `BR-7`
names two different rules. Where a finding cites a document rather than a rule, it emits an
**absolute URL**: the checker runs in projects that never had this repository's
`features/` tree, and a relative path there is a dead reference
([ADR-0020](../../../docs/adr/0020-skill-extension-protocol.md)).

## What the audit is, and how it is reached

The audit is a skill, not a binary. It answers the rules that must be read to be judged,
as a closed checklist over one module — one question at a time, one file at a time, each
answerable without holding the rest of the module in context.

That shape is what lets it run on the cheapest model available, and running cheaply is not
an optimisation here but the condition of it running at all: an audit that costs as much as
a review is one that gets run once, at the moment the standard is written, and never again.

It reports in the same finding shape as the procedural check — module, file, rule, one line
— so a consumer merges the two lists without knowing which surface produced which row.

## What neither surface does

- **Neither writes anything.** No `--fix`, no formatting pass, no scaffolding of the file
  it found missing. Scaffolding belongs to authoring, which is a different feature with a
  human in front of it.
- **Neither resolves a composition.** Whether a module *should* be present is
  `scrumia-extends`'s question; whether it is well-formed is this one's. Two tools, two
  questions, neither answering the other's.
- **Neither ranks anything.** A finding is a finding, and both surfaces emit the same
  shape. Severity tiers would order a list nobody has seen yet.

## Crossing the process boundary

The procedural check is reached by name and speaks through its exit status and `--json`.
Nothing in this feature fixes what it is written in, and no consumer may depend on that:
this repository's gate is Python and invokes it as a subprocess, which is the only
integration this standard guarantees.

Any consumer wanting more than an exit status parses `--json`. A consumer importing the
tool as a library would be reaching into another module, which BR-7 forbids and which this
tool reports.

**Its only named consumer cannot reach it by name.** `tools/validate.py` runs in CI, where
no harness is running and therefore no plugin's `bin/` is on `PATH` — the asymmetry
ADR-0020 records as accepted, and which `validate.py` already documents for
`scrumia-extends`, reaching it through `$SCRUMIA_MODULE_DIR`. `scrumia-module` needs the
same escape, and it is stated here so an implementer does not write a bare-name subprocess
call and meet it as a CI failure instead of as a decision.

**Checking many modules is the consumer's loop, not a batch flag.** The gate runs the check
once per module and aggregates: any `4` or `1` is a run that could not conclude and is
reported as such rather than folded into the finding count.
