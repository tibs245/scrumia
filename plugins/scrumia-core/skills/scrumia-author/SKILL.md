---
name: scrumia-author
description: Brings a need to a ScrumIA module the anatomy check accepts on its first run — deciding whether a module is warranted at all, where it lives, and writing only what the module actually has. Use it to create a module, to change one, or to move one between locations, and before proposing one: two of its answers are that no module should exist.
---

# Author a module

A need arrives — a procedure, a set of rules, a capability worth running in more than one
place — and the cheapest thing an agent can do with it is create a module. This pass exists
to stop that from being the default, and to make the module correct on the occasion it is
warranted.

Three things it is not. It is not a template expansion: it asks, and what it writes depends
on the answers. It is not a scaffolder: a tree of headings with nothing under them is a
module that already has findings against it. And it is not obliged to produce anything —
**a pass concluding that no module is warranted has run to completion**, and reporting that
is an answer rather than a failure to reach one.

The rules are
[`module-authoring`](https://github.com/tibs245/scrumia/blob/main/features/business/module-authoring/business.md)'s.
This skill applies them and defines none of them.

## A change is not a lighter path

Creating a module and changing one run the same refusals and the same check. An edit that
skips the check is how a module that passed once stops passing without anyone noticing —
which is the failure the check exists to catch, arriving through the one door left open.

What a change owes on top of that — the module's own findings read before anything is
touched, and the type and scope its commit will carry — is `module-authoring`'s BR-4 and
BR-5, and it is Step 0's. A move owes the same reading and the same commit line: it is a
change to a module that already exists, and the only thing distinguishing it is that it
must leave every file byte-identical.

## This file carries the pass, not the standard

What a well-formed module contains is
[`module-anatomy`](https://github.com/tibs245/scrumia/blob/main/features/business/module-anatomy/business.md)'s,
and none of it is restated here — a second copy of a standard is the copy that drifts, and
this one has a tool. Read the standard, and let the check name what is not met yet:

```bash
scrumia-module check <path-to-the-module>
```

It reads that module's own tree and nothing else, which is what lets it answer on a module
still being written and declared nowhere. Each finding names the file and the rule it
missed. Read `scrumia-module --help` before branching on its exit status: it separates five
states, and a non-zero exit is not a finding.

The name is published by the module this skill ships in, so it is on `PATH` whenever this
skill is loaded. Nothing here composes a path into another module
([ADR-0018](https://github.com/tibs245/scrumia/blob/main/docs/adr/0018-modules-reach-by-name.md)).

## Step 0 — The module already exists

Runs only when there is a module to change or to move, and runs **before** anything is
touched. Everything after it runs unchanged either way: a change is not a lighter path, and
neither is a move.

### Read its findings before you touch it

```bash
scrumia-module check <path-to-the-module>
```

Whatever it returns now belongs to the module, not to this pass. Report those findings
first, and keep them apart from what Step 5's run returns: **the difference between the two
runs is the only thing that says which findings this change introduced.** A pass that runs
the check once, at the end, hands back a single list in which its own work and the module's
existing state are indistinguishable — and the module's history gets quietly reattributed
to whoever touched it last.

Fixing a pre-existing finding is welcome and is a change like any other. Inheriting one in
silence is what this reading forbids.

### Moving it between locations rewrites nothing

A module moves when the reach of its need turns out to be wider or narrower than where it
sits — Step 3's table, read again on a module that already exists. The move changes two
things, and both of them are outside the module:

- **where its directory sits**, one of the three places
  [`local-extension`](https://github.com/tibs245/scrumia/blob/main/features/business/local-extension/business.md)
  states;
- **what declares it** — the `<source>:<module>` key in the configuration of every project
  that runs it and, where a marketplace is the destination, that marketplace's own
  manifest. That entry is written *from* the module's manifest; the manifest is never
  edited to agree with it.

Everything the module ships comes out byte-identical, **its own manifest included**. A
version, a homepage or a repository filled in on the way out is a rewrite however
reasonable the moment looks: a field naming a publication the module does not have is
absent rather than invented, and adding it later is an edit that runs this pass on its own
terms.

**Show that, rather than intending it.** Take the tree before, take it after, and compare:

```bash
diff -r <before> <after> && scrumia-module check <after>
```

An empty diff and a verdict identical to Step 0's first run are the evidence. "The move
rewrote nothing" is not evidence, and it is what a move that rewrote something also says.

Once it has moved, the declaration is the other half: `scrumia-extends --modules` reports
where each declared module resolved from on this machine, so a rekeyed declaration that
still resolves — to the new location, not the old — is what says the move landed. A module
answered in its old location *and* its new one is `local-extension`'s to name, not this
pass's to tidy away.

The reverse direction is the same move and carries no extra ceremony. What it owes is owed
to the projects that had adopted the module, and it is
[`release-versioning`](https://github.com/tibs245/scrumia/blob/main/features/business/release-versioning/business.md)'s
rather than invented here: a final release of the module carrying the breaking signal,
whose changelog entry names where the module went. That release is the notice. Do not open
an issue on an adopting project, message anyone, or add a field to the manifest saying
where it moved.

### Name the commit, and derive nothing from it

Report the **type** and the **scope** the change's commit will carry, and stop there.

What follows from them is
[`release-versioning`](https://github.com/tibs245/scrumia/blob/main/features/business/release-versioning/business.md)'s,
and the level is read off the commit rather than chosen here. **Do not announce one** — not
"this is a minor", not "this is a major": it asserts a conclusion from inputs that are not
written yet, and below `1.0.0`, where every module still sits, the word names two different
things at once.

## Step 1 — Say what the need is, and count what it holds

Write the need as what a project would gain, in one or two sentences, in the words of
someone who does not already have it. "Every ticket here is estimated against a house scale
before it is picked up" is a need; "we want a module for estimation" is a conclusion with
the need still inside it.

Then count its **distinct concerns**: the separate questions someone would arrive with.
Not files, not rules, not features — questions. Three concerns means a reader arriving with
one of them has to read past the answers to the other two.

Count before wanting a module. The count is what Step 2 refuses on, and a count taken after
the decision agrees with it every time.

## Step 2 — The two refusals

Both run before anything is created, and either one can end the pass.

### A module is not created for a need below the threshold

Below roughly three distinct concerns, the structure costs more than it carries: a module
built below it is a wrapper whose only content is the ceremony of being a module, and it
will be installed, versioned and maintained for that.

One standing rule is the clearest case and it is not the only one. Everything between one
rule and the threshold lands here too — two concerns, or a single procedure no register
asks for. That band is the commonest input this pass gets, and it has the same outcome:
**create nothing, and name the destination that fits.**

Which destination is not this skill's to choose. Hand the need to the tree that already
chooses, stated as the rule it would be:

- [`scrumia-place`](../scrumia-place/SKILL.md) — the tree that chooses. It states the
  destinations it chooses between; this file does not.
- The shapes a project's own answer can take are
  [`local-extension`](https://github.com/tibs245/scrumia/blob/main/features/business/local-extension/business.md)'s.
  They are stated there and nowhere else, this file included.

Then stop. Report the need, the count that decided it, and the destination the tree named
— and write nothing. That is a completed pass.

### A new slot is not invented to hold a new module

A slot is justified on one test, and it is answered with a name rather than with a
principle: **can you name a real project that would fill this slot with a different
module?** Not one that could exist — one that does, or one whose need is stated.

Where you cannot, the slot is refused, and two answers are accepted in its place:

- one more capability in a module the composition already runs;
- a module that fills no slot at all, which is a complete module — the kernel this skill
  ships in is one.

Creating the slot and noting the doubt is not among them. A slot nothing would fill
differently is a question the composition already answers; what a slot is, and when one is
justified, is
[`modular-composition`](https://github.com/tibs245/scrumia/blob/main/features/business/modular-composition/business.md)'s.

## Step 3 — The reach decides the location

A module lives where the need it answers lives:

| The need is | The module lives |
|---|---|
| this project's alone | inside the project |
| this person's, across their projects | in the directory of checkouts shared between them |
| anyone's who runs ScrumIA | in a marketplace |

**State the reach you inferred, out loud, before creating anything.** It is an inference
from a sentence someone else wrote, and the human is the one who can contradict it. The
default is the narrowest reach that covers the need.

Where each place actually sits, and how a declaration there resolves, is
[`local-extension`](https://github.com/tibs245/scrumia/blob/main/features/business/local-extension/business.md)'s
— read it rather than assuming a path. A shared checkout in particular is resolved per
machine, so its location is **never something to write into a file**: `scrumia-extends
--help` names the variable it resolves through, and `--modules` reports where each module
the project already declares resolved from on this machine.

Starting at the marketplace is the expensive mistake: a module published before its second
use has adopters before it has evidence. Before creating anything there, state the two
obligations publishing carries and have them accepted:

- **a version**, whose bumps
  [`release-versioning`](https://github.com/tibs245/scrumia/blob/main/features/business/release-versioning/business.md)
  governs and which is read off the commit rather than chosen;
- **a deprecation window** before a renamed thing disappears, on the terms stated there.

Neither obligation applies inside a project, which is what makes the narrow default cheap.
And moving later is free: promotion changes a module's location and what declares it, and
rewrites no file it contains.

## Step 4 — Write what the module has, and nothing else

Where the pass has nothing to write, it writes nothing, and the absence is the statement.
A register the module opens nothing on gets no declaration; a setting it reads none of
gets no section; a name it publishes none of gets no `bin/`. Writing "none" under a
heading says the same thing more expensively, and leaves the next reader something to
prune.

**No marker to be filled in later.** No `TODO`, no "describe here", no section left for
whoever comes after. A pass that emits placeholders produced findings and called them a
starting point.

In order:

1. **The manifest**, at `.claude-plugin/plugin.json`. Write it first: the check refuses a
   target carrying no manifest rather than judging it, so until it exists nothing below is
   verifiable.
2. **The README**, whose reader and whose sections are both the standard's. The check names
   each section that is missing or empty, so write what the module is for and let it name
   the rest.
3. **What the module actually does** — its skills, its commands, its agents, the names it
   publishes. A knowledge skill that outgrew one file takes the rules hierarchy
   [ADR-0011](https://github.com/tibs245/scrumia/blob/main/docs/adr/0011-rules-hierarchy.md)
   describes, its routing table included: neither surface asks for that table, so a skill
   that grew without one composes, checks clean, and applies to nothing.
4. **The extension data, for what the module actually opens, contributes and runs** — and
   for nothing else. Write a declaration and the call that reads it together, or write
   neither: the check reports a register declared and never consulted, on
   `modular-composition`'s BR-11. What each of the three files declares is
   [`scrumia-extend`](../scrumia-extend/SKILL.md)'s.

Run the check as you go rather than at the end. A name under `bin/` never made executable,
a path built from a variable nothing substitutes, a reference climbing out of the module —
each is a finding a first draft routinely carries, none is visible to a reader, and the
check names the file and the fix for all three.

## Step 5 — The check decides when the pass is finished

Run it on what you produced, with nothing edited between the writing ending and the check
running:

```bash
scrumia-module check <path-to-the-module>
```

Findings are fixed and the check is run again. **The pass has not finished while the module
it produced has a finding against it** — that is the measure this feature is judged on, and
a pass reporting success alongside a list of findings has moved its own work to whoever
reads the report.

A clean check is not the whole standard: what has to be read to be judged is outside what
a program decides. Re-read the module against the standard once the check is clean, and
where the composition ships a surface that asks those questions, run it too.

The check is also not the whole gate. A project that ships modules usually has one of its
own on top — a manifest listing what it publishes, a changelog shape, rules about the
relationship between two modules, none of which one module's tree can answer. Run it
before calling the pass finished, or the module is clean and the branch is red.

## What the pass reports

Five lines, whether or not a module exists at the end of it:

- the need, in a sentence, and the count of concerns it holds;
- the reach inferred and the location chosen — named as an inference, so it can be
  contradicted;
- which refusal fired, if one did, and what the tree named instead;
- what was created, or that nothing was;
- the check's verdict, run last.

A pass that created nothing reports the same five lines and is a completed pass. An
authoring pass that can only succeed by creating a module will always create one.

Where the module already existed, three more, and they are the difference between a change
reported and a change asserted:

- the findings the module carried **before** Step 0 opened it, told apart from the verdict
  above — without them the two arrive as one list, and this pass's work reads as the
  module's history;
- where it moved, the location it left and the one it went to, with the empty diff that
  says nothing inside it changed;
- the type and the scope its commit will carry — and no level, which is read off that
  commit elsewhere.
