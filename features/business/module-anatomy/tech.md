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
list is the output; the exit status separates three states that a single boolean would
collapse:

| State | Exit | Meaning |
|---|---|---|
| checked, no finding | `0` | the module meets the standard |
| checked, findings | `1` | the module was fully read, and did not |
| could not check | `2` | the target is unreadable, or is not a module at all |

The third is why a boolean is not enough. A gate that treats "could not check" as "clean"
passes exactly the modules most likely to be broken, and a gate that treats it as
"findings" makes an unrelated I/O error look like a non-conformity. A consumer that reads
only the exit status must therefore distinguish `1` from `2`; one that reads `--json` gets
the state named in full and never infers it from whether the finding list is empty.

`--json` is the same flag `scrumia-extends` already carries, and for the same reason: a
consumer filters, counts or annotates without parsing a table meant for a terminal.

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
