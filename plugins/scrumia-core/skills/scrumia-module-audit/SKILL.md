---
name: scrumia-module-audit
description: Audits one ScrumIA module against the anatomy rules a program cannot decide from its tree alone — one concern per file, an index that routes rather than carries, and the README sections that depend on what a module actually does. Use it after `scrumia-module check`, or wherever a module's shape needs a verdict a reader would otherwise have to produce by hand.
---

# Auditing a module's anatomy

`features/business/module-anatomy/` is one authority applied through two surfaces. The
procedural check — `scrumia-module check` — takes what a program can decide from a
module's tree alone. This skill takes the half that has to be read to be judged: whether a
file answers one concern, whether an index still carries content, and whether the README's
optional sections match what the module actually needs.

It is a checklist, not a review. Every question below is closed, names exactly one rule,
and is answered from one file — never by holding the rest of the module in context. That
is what lets it run on the cheapest model available, which is the condition of it running
at all: an audit that costs as much as a review is one that gets run once and never again.

It writes nothing. Like the procedural check, it reports; it does not repair, reformat, or
scaffold what it found missing.

## Step 1 — Read the README once

Before walking any other file, read the module's `README.md`. This is the one file every
later question is allowed to hold alongside the file in front of it — not "the rest of the
module," just this one anchor, read once and carried forward. Note which of the four
optional sections it carries: **Settings it reads**, **What it expects to find**,
**Decisions**, **Not shipped yet**.

If the module carries no README, stop: that is already `scrumia-module check`'s finding
(`module-anatomy/BR-4`), and this audit has nothing to add until one exists.

## Step 2 — Walk the module's prose, one file at a time

For every file the module ships that carries prose for a reader — each skill's `SKILL.md`,
its `references/` or guide files, the README itself — ask the two questions below. Each is
answered from that one file.

### Q1 — Does this file answer more than one distinct question a reader could arrive with? (`module-anatomy/BR-2`)

A reader comes to a file wanting one thing. If reaching the answer means reading past a
different question's answer first, the file is two files and an index.

**Length is never the signal, in either direction.** A short file that jumps between two
unrelated procedures is a finding; a long file that answers one question at length is not.
Judge what the file is *for*, not how much of it there is.

- Finding: `{ module, file, rule: "module-anatomy/BR-2", message: "answers <question A> and <question B> in one file" }`
- No finding: the file is long, or short, and answers one question throughout.

### Q2 — If this file is an index, does it also carry content found nowhere else? (`module-anatomy/BR-3`)

Applies only where the file's own job is to route — a module's top-level entry point, or a
skill's own file once its guides were split out. Everything else answers "not applicable"
and moves on.

Where it applies: does the file, past what exists and when to open each, also state a
rule, a fact or a procedure that is not written in the file it points to? An index that
still asserts something on its own account was never split — only prefixed.

- Finding: `{ module, file, rule: "module-anatomy/BR-3", message: "carries <the content>, found nowhere else the index points to" }`
- No finding: the file only lists what exists and says when to open each.

## Step 3 — Walk the module's skills and scripts for what they read and need (`module-anatomy/BR-4`)

For every file the module ships that could act — a skill's instructions, a script, a
command — ask, of that file alone, four closed questions, each naming `module-anatomy/BR-4`
and each answered from that one file:

- Does it read a project setting: a key under `settings.` in `.scrumia/config.yaml`, an
  environment variable, or a config file of its own?
- Does it depend on something already being present that the module did not create —
  another directory, another module's output, a piece of state?
- Does it record a decision — a choice made and the alternative it rejected — rather than
  only the behaviour that follows from it?
- Does it describe something the module does not yet do — named, not built?

Record which files answered yes to which, and to what.

## Step 4 — Compare the record against the README

This step is bookkeeping, not a new question: it combines yes/no answers already produced
one file at a time in Steps 1 and 3, and asks nothing that needed two files open at once.
Four comparisons, one per optional section:

| Step 3 found | README section | Result |
|---|---|---|
| a file reads a setting | no **Settings it reads** | finding — the absence asserts the module reads none, and it doesn't |
| a file depends on something present | no **What it expects to find** | finding — same reason |
| a file records a decision | no **Decisions** | finding — same reason |
| a file names something not yet built | no **Not shipped yet** | finding — same reason |
| nothing found | section absent | no finding — the absence is true |

**The reverse direction is not this audit's.** A README section present where Step 3 found
nothing is not flagged here — `module-anatomy/BR-4` requires an absent section to be true,
not a present one to be necessary, and AC-14 tests only the omission.

- Finding: `{ module, file: "README.md", rule: "module-anatomy/BR-4", message: "reads a setting <name> but carries no 'Settings it reads' section" }` (and the equivalent for the other three rows)

## Step 5 — The README length guardrail (`module-anatomy/BR-4`)

Read the README once more, on its own. Past roughly eighty lines it has likely become
documentation, which belongs in the module's skills or in `docs/`. This is a guardrail, not
a threshold: judge what the extra lines are *doing*, never the count alone. A README this
long because it lists real sections earned by a module that reads settings, needs something
present and ships decisions is not a finding; one padded with restated `SKILL.md` content
or narration is.

- Finding: `{ module, file: "README.md", rule: "module-anatomy/BR-4", message: "past the guardrail, and the extra lines are <what they restate or narrate>" }`
- No finding: the length is earned by the sections it states.

## Report

Report every finding from Steps 2, 4 and 5 in one list, each row carrying `module`, `file`,
`rule`, and one line of what was not met — the same four fields `scrumia-module check
--json`'s `findings` array carries, so a consumer merges this list with the procedural
check's without knowing which surface produced which row. A clean module gets one line:
`<module> — no findings`.

No exit code: this is a skill, read by whoever asked for it, not a process another tool
branches on.
