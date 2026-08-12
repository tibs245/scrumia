---
name: scrumia-author
description: Brings a need from nothing to a ScrumIA module the anatomy check accepts on its first run — deciding whether a module is warranted at all, where it lives, and writing only what the module actually has. Use it to create a module, and before proposing one: two of its answers are that no module should exist.
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

## One pass, not three

Creating a module, changing one, and moving one between locations are the same pass. The
refusals apply to what is being added as much as to what is being created, and the check
below decides when any of the three is finished. There is no lighter path for a change: an
edit that skips the check is how a module that passed once stops passing without anyone
noticing.

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

### A module is not created for what is smaller than one

Below roughly three distinct concerns, the structure costs more than it carries: a module
built around one rule is a wrapper whose only content is the ceremony of being a module,
and it will be installed, versioned and maintained for that.

One standing rule is the clearest case and it is not the only one. Everything between one
rule and the threshold lands here too — two concerns, or a single procedure no register
asks for. That band is the commonest input this pass gets, and it has the same outcome:
**create nothing, and name the destination that fits.**

Which destination is not this skill's to choose. Hand the need to the tree that already
chooses, stated as the rule it would be:

- [`scrumia-place`](../scrumia-place/SKILL.md) — the tree, which routes to a module, this
  project, a feature, a ticket, the change itself, or agent memory.
- The shapes a project's own answer can take are
  [`local-extension`](https://github.com/tibs245/scrumia/blob/main/features/business/local-extension/business.md)'s,
  and they are stated there and nowhere else, this file included. None of them is a
  degraded module: a project whose entire local extension is four directives has extended
  ScrumIA correctly.

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
differently is a register vocabulary that grew by one and answers nothing new; what a slot
is, and when the vocabulary admits one, is
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
`local-extension`'s — read it rather than assuming a path, and `scrumia-extends --modules`
reports where each declared module resolved from on this machine. A shared checkout in
particular is resolved per machine and named by nothing versioned, so a path to it is
something to ask for or read, never something to write into a file.

Starting at the marketplace is the expensive mistake: a module published before its second
use has adopters before it has evidence. Before creating anything there, state the two
obligations publishing carries and have them accepted:

- **a version**, whose bumps
  [`release-versioning`](https://github.com/tibs245/scrumia/blob/main/features/business/release-versioning/business.md)
  governs and which is read off the commit rather than chosen;
- **a deprecation window** before a renamed thing disappears, counted in releases and
  stated there.

Neither obligation applies inside a project, which is what makes the narrow default cheap.
And moving later is free: promotion changes a module's location and what declares it, and
rewrites no file it contains.

## Step 4 — Write what the module has, and nothing else

Where the pass has nothing to write, it writes nothing, and the absence is the statement.
A register the module opens nothing on gets no declaration; a setting it reads none of
gets no section; a name it publishes none of gets no `bin/`. The standard reads an absence
that way, so a heading with "none" under it is noise the next reader has to prune and an
empty heading is a finding outright.

**No marker to be filled in later.** No `TODO`, no "describe here", no section left for
whoever comes after. A pass that emits placeholders produced findings and called them a
starting point.

In order:

1. **The manifest**, at `.claude-plugin/plugin.json`. That file, and only that file, is
   what makes the directory a module — without it the check refuses the target rather than
   judging it, and everything below is unverifiable.
2. **The README**, addressed to whoever has not adopted the module and is deciding whether
   to. Its sections and their order are the standard's; the check names each one that is
   missing or empty, so write what the module is for and let it name the rest.
3. **What the module actually does** — its skills, its commands, the names it publishes.
   One file answers one question, and a name under `bin/` is executable or it fails in
   whoever calls it.
4. **The extension data, for what the module actually opens, contributes and runs** — and
   for nothing else. Opening a register is itself the promise to consult it, so a
   `registers.json` naming a register no skill it ships asks for is a finding: write the
   declaration and the call that reads it together, or write neither. What each of the
   three files declares is [`scrumia-extend`](../scrumia-extend/SKILL.md)'s.

Everything a file inside the module points at resolves inside the module. A path climbing
out of it is the finding this check exists for; another module is reached by the name it
publishes on `PATH`, and a document belonging to no module is cited by absolute URL —
`modular-composition`'s BR-7, which the check enforces.

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

A clean check is not the whole standard. What has to be read to be judged — whether a file
answers two questions, whether an index routes or carries, whether the README addresses
someone who has not adopted the module — is outside what a program decides. Re-read the
module against the standard once the check is clean, and where the composition ships a
surface that asks those questions, run it too.

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
