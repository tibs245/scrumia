# Module anatomy — business rules

## Value

For whoever writes a ScrumIA module, audits one before adopting it, or has to change a
single line inside one. It brings a stated internal shape and a checker that produces a
verdict on any module, so that conformity is something a machine reports rather than
something a careful reader notices. It matters because a module made of prose has no
compiler: nothing today fails when a skill grows to answer four questions at once, when
a link points at a file that was renamed, or when a module ships with no way for a human
to tell what it is for without opening its skills. Measurable, and the first measure is
uncomfortable: the count of findings the checker returns on this repository's own
modules, and the count of checks `tools/validate.py` performs that the checker already
performs.

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
the rules need a checker: nothing else will ever notice.

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

## One checker, and it owns nothing

Conformity is verified by exactly one checker, published on `PATH` by the module that
owns this standard. It states what a module must contain and what it must not, and it is
the single authority on both.

A consumer of the checker adds only what is its own. This repository's marketplace gate
has something of its own — the manifest that lists the plugins, their versions and their
sources, which exists nowhere but here — and it delegates everything else. A check
performed in two places is two renderings of one rule, and two renderings of one rule
diverge; the duplication is itself a defect this feature counts.

**The checker writes nothing, anywhere.** It reports; it never repairs, never reformats,
never creates the file it found missing. A tool that fixes what it finds cannot be
trusted to report what it did not fix, and a verdict that changed the thing it judged
cannot be reproduced.

## What must be absent is a rule like any other

A standard that only lists what must be present cannot catch the defect that matters
most here: a module reaching outside itself. That rule is
`modular-composition`'s BR-7, and this feature does not restate it — it makes it
checkable, which is the part that was missing.

The same holds for what a module must not carry internally: a file that duplicates
another module's rule rather than pointing at it, a link to a path that does not exist,
a script a skill invokes and that was never shipped. Each is an absence rule, each fails
only at the moment an agent follows it, and none of them is visible to review.

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
- **BR-4** — Every module carries a README addressed to whoever has not adopted it yet —
  what it is for, what it refuses, what it ships, what it expects. It is not the
  `SKILL.md` contract and does not restate it.
- **BR-5** — Conformity is verified by exactly one checker, owned and published by the
  module that owns this standard. A consumer of the checker verifies only what is its
  own and re-verifies nothing the checker already covers.
- **BR-6** — The checker writes nothing. It reports a finding; it never repairs,
  reformats or creates what it found missing.
- **BR-7** — The standard states what must be absent as well as what must be present, and
  an absence rule is checked like any other. Where the rule belongs to another feature,
  the checker enforces it and this one does not restate it.
- **BR-8** — Every module ships against this standard, the module owning the checker
  included. There is no exemption, and a finding on the owner is reported like any other.

## Vocabulary

- **Checker** — the single tool that produces a conformity verdict on a module. Not a
  linter for a language, not the marketplace gate: those are consumers.
- **Finding** — one stated non-conformity, naming the module, the file and the rule. A
  finding is not a failure of the run: a checker that found things ran correctly.
- **Consumer** — anything that invokes the checker and adds its own checks on top. This
  repository's marketplace gate is one; a module's own CI would be another.
