# Module anatomy — business rules

## Value

For whoever writes a ScrumIA module, audits one before adopting it, or has to change a
single line inside one. It brings a stated internal shape and a verdict on any module, so
that conformity is something reported rather than something a careful reader notices. It
matters because a module made of prose has no compiler: nothing today fails when a skill
grows to answer four questions at once, when a link points at a file that was renamed, or
when a module ships with no way for a human to tell what it is for without opening its
skills. Measurable, and the first measure is uncomfortable: the count of findings returned
on this repository's own modules, and the count of checks `tools/validate.py` performs
that are already covered elsewhere.

## The test this standard is judged on

`modular-composition` closes its pluggability list at three items and states the test
that admits an item: **silent breakage when a project composes the module with a
different set than the one it was written against**. Nothing here belongs on that list,
and this feature proposes no fourth entry.

The failure this standard answers is a different one, and it is not silent — it is slow:

- an agent loads a whole skill to change one paragraph, and pays for the rest every time
- a defect ships because nothing but a reader was ever going to catch it
- a human choosing between two modules has to read both to find out what they do

A module can fail every rule below and still compose perfectly. That is precisely why
the rules need something checking them: nothing else will ever notice.

## One concern per file

A file answers one question. A file that answers two is two files, and an index that
lists them.

This is the same growth curve [ADR-0011](../../../docs/adr/0011-rules-hierarchy.md) names
for knowledge skills and [ADR-0003](../../../docs/adr/0003-cross-cutting-architecture.md)
rejected for a single cross-cutting architecture file: a document that only grows, is
reloaded in full to read three lines, accumulates sections nobody prunes, and past a
point nobody verifies. It applies to a module as a whole, not only to the skills inside
it.

The threshold is not a line count. It is whether a reader arriving with one question has
to read past an answer to a different one. Below roughly three distinct concerns on a
topic, splitting produces ceremony rather than clarity — a rule `scrumia-rules` already
states for rule sections, and the same judgment applies here.

**An index routes, it does not carry.** Once a module's entry point has been split, what
remains at the top is a routing table: what exists, and when to open each. An index that
still carries content is a file that was never split, only prefixed.

## A README is addressed to a human who has not adopted the module

Every module carries a README, and its reader is not the agent running the module. It is
whoever is deciding whether to run it at all: what the module is for, what it refuses,
what it ships, and what it expects to find. A module without one can only be evaluated by
reading its skills, which is a cost paid by every person who ever considers it.

This is not the `SKILL.md` contract, which `modular-composition` already requires and
which addresses the agent. The two have different readers and say different things; a
README that restates the contract has the wrong audience, and a contract that explains
what the module is for has the wrong one too.

### The sections it carries

Four are required of every module, and the rest are content-tested — the same two
categories the specs catalog uses, and for the same reason: an absent section that means
something specific is information, while a section filled with "none" is noise nobody
prunes.

| Section | Present when |
|---|---|
| `# <module name>`, then one paragraph | always — the name is the published one, the paragraph says what the module is for in a reader's terms, not the composition's |
| **What it answers** | always — the question a project has that makes this module the answer. Not a feature list |
| **What it refuses** | always — the boundary. This is the section that lets a reader conclude the module is *not* for them, which is the most valuable thing a README does |
| **What it ships** | always — skills, commands and names published on `PATH`, as a table |
| **Settings it reads** | the module reads any. Absent means it reads none |
| **What it expects to find** | the module needs something else present to be useful. Absent means it stands alone |
| **Decisions** | the module ships decision records. Absent means it ships none |
| **Not shipped yet** | something described is not built. Absent asserts the module is complete as described |

The order above is the reading order, and it is not negotiable section by section: a
reader scanning four modules compares them by position. What varies between modules is
which optional sections appear, never where the required ones sit.

Two refusals travel with the template. **No section with nothing under it** — an empty
heading is worse than an absent one. And **no restatement of the `SKILL.md` contract**:
the settings section names what the module reads and points at the contract for the
schema, rather than reproducing it.

A guardrail rather than a rule: past roughly eighty lines a README has become
documentation, and documentation belongs in the module's skills or in `docs/`. The two
READMEs this repository already ships sit at forty-five and forty-eight lines. Exceeding
it calls for checking, not for cutting.

## One authority, two surfaces, split on what a machine can decide

This standard is one authority on what a module must contain and what it must not. It is
applied through two surfaces, and which surface takes a rule is decided by one question:
**can a program decide it without reading for meaning?**

| Surface | Takes | Examples |
|---|---|---|
| the **procedural check** | what is decidable from the tree alone | a README exists; the extension data files are present and parse; a link resolves; a script a skill invokes ships; nothing resolves outside the module |
| the **audit** | what has to be read to be judged | this file answers two questions; this index carries what it should route to; this paragraph restates another module's rule instead of pointing at it |

The audit is a checklist an agent answers, question by question, and the questions are
written so that the cheapest model available can answer them — closed, one concern each,
answerable from one file at a time. It is not a second standard and it holds no rule of
its own: every question it asks is one of this feature's rules, phrased as a question.

Splitting this way is what keeps the judged half from being either abandoned or faked. A
regular expression standing in for "one concern per file" would flag long files and miss
short muddled ones, and its findings would be argued with until nobody ran it. A rule
nobody can check is a rule nobody follows.

A rule may be taken by both surfaces where each reaches part of it — the procedural check
confirming a README exists, the audit judging whether it addresses the right reader. What
is forbidden is the same *question* asked twice, in two wordings that will drift.

## A consumer adds only what is its own

Whatever a consumer of either surface checks on top must be something neither surface
covers. This repository's marketplace gate has two such things — the manifest that lists
the plugins, their versions and their sources, and the rules governing the specs tree,
neither of which is a property of any single module — and it delegates everything that is.
A check performed in two places is two renderings of one rule, and two renderings of one
rule diverge; the duplication is itself a defect this feature counts.

The boundary is what a surface can see. The procedural check reads one module's tree, so
it can never adopt a rule about the specs tree or about the relationship between modules;
handing it one would not be delegation, it would be a rule left unenforced.

## Neither surface writes anything

Both report; neither repairs, reformats, or creates the file it found missing. A tool that
fixes what it finds cannot be trusted to report what it did not fix, and a verdict that
changed the thing it judged cannot be reproduced.

The audit is held to this the more strictly, because it is the one that could plausibly
offer to rewrite the file it just criticised.

## What must be absent is a rule like any other

A standard that only lists what must be present cannot catch the defect that matters
most here: a module reaching outside itself. That rule is
`modular-composition`'s BR-7, and this feature does not restate it — it makes it
checkable, which is the part that was missing.

The same holds for what a module must not carry internally: a file that duplicates
another module's rule rather than pointing at it, a link to a path that does not exist,
a script a skill invokes and that was never shipped. Each is an absence rule, each fails
only at the moment an agent follows it, and none of them is visible to review.

## Extension data is optional, and optional is not unchecked

A module that opens no register and contributes no directive ships none of the extension
data files, and that is a complete module — `modular-composition` states it and refuses to
make their presence a condition of being pluggable. This standard does not reverse that.

What it adds is the half that was missing: **a file a module does ship is checked**. An
`extends.json` that does not parse, a `registers.json` naming a register the module never
opens, a `dependencies.jsonl` naming a source that does not exist — each is a finding.
The failure they produce is the one that costs most to trace, because the module composes
and contributes nothing, and its silence looks like a decision.

That the file may be absent and the absence means something specific is exactly why it
needs checking when present: nothing else distinguishes "contributes nothing on purpose"
from "contributes nothing because its declaration is malformed".

## The standard has no exemption for its owner

Every module the marketplace ships is checked, including the one that publishes the
checker. A standard its author does not meet is a recommendation, and a recommendation
is what this feature exists to replace.

## Business rules

- **BR-1** — A module's internal shape is judged on one test: an agent finds and changes
  the right line without loading what it does not need, and a defect does not ship
  because only a reader could have caught it. Nothing on `modular-composition`'s
  pluggability list is restated here, and nothing here is added to it.
- **BR-2** — One file answers one question. A file a reader must read past to reach the
  answer they came for is two files and an index.
- **BR-3** — An index routes and carries no content of its own beyond what it takes to
  route: what exists, and when to open each.
- **BR-4** — Every module carries a README addressed to whoever has not adopted it yet.
  Four sections are required — the name and its paragraph, what it answers, what it
  refuses, what it ships — in that order; the others are present when they have something
  to say and their absence states it. It is not the `SKILL.md` contract and does not
  restate it.
- **BR-5** — This standard is one authority, applied through two surfaces. A rule goes to
  the procedural check when a program can decide it from the module's tree alone, and to
  the audit when it has to be read to be judged. A consumer of either verifies only what
  neither covers, and re-verifies nothing they already cover.
- **BR-6** — Neither surface writes anything. Each reports a finding; neither repairs,
  reformats or creates what it found missing.
- **BR-7** — The standard states what must be absent as well as what must be present, and
  an absence rule is checked like any other. Where the rule belongs to another feature,
  the procedural check enforces it and this one does not restate it.
- **BR-8** — An extension data file is optional and its absence is a statement. A file a
  module does ship parses, and declares only things that exist.
- **BR-9** — A module declaring a standing role ships the agent that role names. A role a
  project enables whose agent the module does not ship is a finding, reported with the
  restart that usually explains it.
- **BR-10** — Every module ships against this standard, the module owning the two surfaces
  included. There is no exemption, and a finding on the owner is reported like any other.
- **BR-11** — Every question the audit asks is one of this feature's rules, phrased as a
  question, closed, and answerable from one file at a time. The audit holds no rule of its
  own, and a question it cannot answer that way belongs to the procedural check or to
  neither.

## Vocabulary

- **The procedural check** — the tool that decides, from a module's tree alone, the rules
  a program can decide. Not a linter for a language, not the marketplace gate: those are
  consumers.
- **The audit** — the checklist an agent answers for the rules that must be read to be
  judged. Cheap by design: closed questions, one concern each, one file at a time.
- **Finding** — one stated non-conformity, naming the module, the file and the rule.
  A finding is not a failure of the run: a surface that found things ran correctly.
- **Consumer** — anything that invokes either surface and adds its own checks on top. This
  repository's marketplace gate is one; a module's own CI would be another.
