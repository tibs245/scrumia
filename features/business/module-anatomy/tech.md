# Module anatomy — how the checker resolves

What the checker reads, what it returns, and what it refuses to do. The rules it enforces
are `business.md`'s; this file states only how a consumer reaches it and what it can rely
on.

## Reached by name, never by path

The checker is published under `bin/` by the module that owns this standard, which puts
it on `PATH` for every enabled plugin. A consumer invokes the name. It never composes a
path into the owning module, for the reason [ADR-0018](../../../docs/adr/0018-modules-reach-by-name.md)
states and `modular-composition`'s BR-7 enforces — a path into another module is exactly
what the checker itself reports as a finding.

This is also what makes the checker usable in a project that has never heard of this
repository: the name is on `PATH` because the module is installed, and nothing else has
to be true.

## What it reads

A module's own tree, and nothing else. It does not read `.scrumia/config.yaml`, does not
ask which modules a project runs, and does not care whether the module it is checking is
installed — conformity is a property of the module, not of the composition it happens to
sit in.

That boundary is what lets it run on a module being authored, before it has been declared
anywhere.

## What it returns

A finding carries the module, the file, the rule and one line of what was not met. The
list is the output; the exit status separates three states that a single boolean would
collapse:

| State | Meaning |
|---|---|
| checked, no finding | the module meets the standard |
| checked, findings | the module was fully read, and did not |
| could not check | the target is unreadable, or is not a module at all |

The third is why a boolean is not enough. A gate that treats "could not check" as "clean"
passes exactly the modules most likely to be broken, and a gate that treats it as
"findings" makes an unrelated I/O error look like a non-conformity.

Findings are also available unrendered, so a consumer can filter, count or annotate them
without parsing a table meant for a terminal — the same split `scrumia-extends` already
makes between its table and its `--json`.

## What it refuses

- **It writes nothing** (BR-6). No `--fix`, no formatting pass, no scaffolding of the
  file it found missing. Scaffolding belongs to authoring, which is a different feature
  with a human in front of it.
- **It resolves no composition.** Whether a module *should* be present is
  `scrumia-extends`'s question; whether it is well-formed is this one's. Two tools, two
  questions, neither answering the other's.
- **It ranks nothing.** A finding is a finding. Severity tiers are the open question this
  feature's `index.md` names, and inventing them now would fix an ordering before anyone
  has seen the list it orders.
