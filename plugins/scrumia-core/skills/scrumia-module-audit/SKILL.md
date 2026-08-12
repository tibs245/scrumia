---
name: scrumia-module-audit
description: Audits one ScrumIA module against the anatomy rules a program cannot decide from its tree alone — one concern per file, an index that routes rather than carries, and the README sections that depend on what a module actually does. Use it after `scrumia-module check`, or wherever a module's shape needs a verdict a reader would otherwise have to produce by hand.
---

# Auditing a module's anatomy

The anatomy standard —
[`features/business/module-anatomy/`](https://github.com/tibs245/scrumia/blob/main/features/business/module-anatomy/business.md)
— is one authority applied through two surfaces. The procedural check —
`scrumia-module check` — takes what a program can decide from a module's tree alone. This
skill takes the half that has to be read to be judged: whether a file answers one concern,
whether an index still carries content, and whether the README's optional sections match
what the module actually needs.

It is a checklist, not a review. Every question below is closed, names exactly one rule,
and is answered from one file — never by holding the rest of the module in context. That
is what lets it run on the cheapest model available, which is the condition of it running
at all: an audit that costs as much as a review is one that gets run once and never again.

It writes nothing. Like the procedural check, it reports; it does not repair, reformat, or
scaffold what it found missing.

## Step 1 — Read the README once

If the target carries no `.claude-plugin/plugin.json`, stop: it is not a module, and this
audit — like `scrumia-module check` — has nothing to judge on a directory that happens not
to be one.

Otherwise, read the module's `README.md` once and record, as four booleans and nothing
more, which of the optional sections it carries: **Settings it reads**, **What it expects
to find**, **Decisions**, **Not shipped yet**. That record — not the file itself — is what
Step 3 compares against; no later question holds the README alongside another file.

If the module carries no README, stop: that is already `scrumia-module check`'s finding
(`module-anatomy/BR-4`), and this audit has nothing to add until one exists.

## Step 2 — Walk every file the module ships, one at a time

For every file the module ships — each skill's `SKILL.md`, its `references/` or guide
files, scripts, commands, the README itself — ask the six questions below, of that one
file. Nothing here classifies a file first ("is this prose, or does it act, or is it a
decision record?") before deciding which questions apply to it: every file gets every
question, and most answer no to most of them.

### Q1 — Does this file answer more than one distinct question a reader could arrive with? (`module-anatomy/BR-2`)

A reader comes to a file wanting one thing. If reaching the answer means reading past a
different question's answer first, the file is two files and an index.

**Length is never the signal, in either direction.** A short file that jumps between two
unrelated procedures is a finding; a long file that answers one question at length is not.
Judge what the file is *for*, not how much of it there is.

- Finding: `{ module, file, rule: "module-anatomy/BR-2", message: "answers <question A> and <question B> in one file" }`
- No finding: the file is long, or short, and answers one question throughout.

### Q2 — If this file is an index, does it also state content of its own? (`module-anatomy/BR-3`)

Applies only where the file's own job is to route — a module's top-level entry point, or a
skill's own file once its guides were split out. Everything else answers "not applicable"
and moves on.

Where it applies: does the file, past what exists and when to open each, also state a
rule, a fact or a procedure of its own? An index that still asserts something on its own
account was never split — only prefixed. Answered from the index alone: this is never a
question of whether the same content also appears elsewhere, which would mean opening
every file the index points to just to ask it.

- Finding: `{ module, file, rule: "module-anatomy/BR-3", message: "carries <the content> rather than routing to it" }`
- No finding: the file only lists what exists and says when to open each.

### Q3–Q6 — What this file reads, needs, records or admits (`module-anatomy/BR-4`)

Four closed questions, each answered from this one file:

- Does it read a project setting: any key in `.scrumia/config.yaml`, an environment
  variable, or a config file of its own?
- Does it depend on something already being present that the module did not create —
  another directory, another module's output, a piece of state?
- Is this file itself a decision record — its whole subject one choice and the alternative
  it rejected, the way `scrumia-design` ships
  `skills/scrumia-design-system/decisions/D-01-two-columns.md`? Rationale prose inside an
  ordinary skill file does not count — only a file whose entire job is recording the
  decision does.
- Does it describe something the module does not yet do — named, not built?

Record which files answered yes to which, and to what.

## Step 3 — Compare the record against the README

This step is bookkeeping, not a new question: it combines yes/no answers already produced
one file at a time in Steps 1 and 2, and asks nothing that needed two files open at once.
Four comparisons, one per optional section:

| Step 2 found | README section | Result |
|---|---|---|
| a file reads a setting | no **Settings it reads** | finding — the absence asserts the module reads none, and it doesn't |
| a file depends on something present | no **What it expects to find** | finding — same reason |
| a file is a decision record | no **Decisions** | finding — same reason |
| a file names something not yet built | no **Not shipped yet** | finding — same reason |
| nothing found | section absent | no finding — the absence is true |

**The reverse direction is not this audit's.** A README section present where Step 2 found
nothing is not flagged here — `module-anatomy/BR-4` requires an absent section to be true,
not a present one to be necessary, and AC-14 tests only the omission.

- Finding: `{ module, file: "README.md", rule: "module-anatomy/BR-4", message: "reads a setting <name> but carries no 'Settings it reads' section" }` (and the equivalent for the other three rows)

## Step 4 — The README length guardrail (`module-anatomy/BR-4`)

Read the README once more, on its own. Past roughly eighty lines: **are the extra lines
restating `SKILL.md` content or narrating, rather than stating sections this module has
earned by reading settings, needing something present or shipping decisions?** This is a
guardrail, not a threshold — judge what the extra lines are doing, never the count alone.

- Finding: `{ module, file: "README.md", rule: "module-anatomy/BR-4", message: "past the guardrail, and the extra lines are <what they restate or narrate>" }`
- No finding: the length is earned by the sections it states.

## Report

Report every finding from Steps 2, 3 and 4 in one list, each row carrying `module`, `file`,
`rule`, and one line of what was not met — the same four fields `scrumia-module check
--json`'s `findings` array carries, so a consumer merges this list with the procedural
check's without knowing which surface produced which row. Match its conventions exactly:
`module` is the name `plugin.json` declares, never the directory; `file` is the path
relative to the module's own root (`skills/scrumia-init/SKILL.md`, not an absolute path
and not one prefixed with `plugins/<module>/`). A clean module gets one line: `<module> —
no findings`.

No exit code: this is a skill, read by whoever asked for it, not a process another tool
branches on.
