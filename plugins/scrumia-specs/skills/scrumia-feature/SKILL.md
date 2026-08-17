---
name: scrumia-feature
description: Creates, updates or audits a ScrumIA feature in features/. Applies the contextual angle catalog (index, business, qa, changelog, ux, tech, api-contract, archi, legal, security, devx) instead of a fixed template. Use it whenever a spec needs to be written, modified or checked.
---

# Writing a ScrumIA feature

A feature is not a document, it's a **directory of targeted files**. Each file is the
output of one **angle** — one way of interrogating the feature — and each angle ships
its own questions, template and review guard-rails in
[`references/angles/<angle>/`](references/angles/). Beyond the four files this module
mandates, you write a file only if its angle activates.

Four mandatory angles: `index`, `business`, `qa`, `changelog`. Seven content-tested:
`ux`, `tech`, `api-contract`, `archi`, `legal`, `security`, `devx`. The table of all
eleven, with what activates each, is in
[`references/catalog.md`](references/catalog.md).

## Creating a feature — the procedure

Follow the order. It is not a style preference: each step produces what the next one
needs, and the most common defect in this format — an `index.md` that does not match
the directory — is only possible when the order is broken.

**1. Find out whether it already exists.** Load `scrumia-specs-find` and use it.
Writing a rule into the wrong feature is the defect that costs the most later,
because two features then define the same rule differently. If an existing feature
owns the subject, you are updating, not creating — jump to *Updating* below.

**2. Establish the scope, and state it before writing anything.** Five lines:

```
Stratum:   business | app/<app>
Feature:   <path it will live at>
Parent:    <Business parent, or parent feature, or none — and why none>
Angles on: <the ones the questions turned up>
Angles off: <the ones considered and declined, with the answer that declined them>
```

The last two lines come from step 3. The scope block is what makes the rest
reviewable — without it, nobody can tell an assertion from an omission.

**3. Run the activation questions.** For each content-tested angle, open its
`context.md` § *When it activates* and answer its closed questions. Each one names
the default answer when you are unsure — use it rather than deciding by feel. A
project may have forced an angle on or off in `.scrumia/config.yaml`; read the
effective setting through `scrumia-extends --settings`, never out of the file.

**4. Write `business.md` first.** Its `## Value` section — who, what it brings, why
it matters, whether it is measured — before anything else. A feature whose value
cannot be stated is a splitting or deletion candidate, not a feature missing a
paragraph. Read [`angles/business/context.md`](references/angles/business/context.md)
for the questions.

**5. Write `qa.md`.** The criteria are downstream of the rules, and they come before
the code that satisfies them. Nominal case first, then the edge cases that apply.

**6. Write each activated angle's file**, one at a time, reading its `context.md`
before and its `checklist.md` after.

**7. Write `index.md` last.** It lists the files present; it cannot be correct before
they exist. Declare every link on both sides — the other feature's `index.md` gets
its half in the same change.

**8. Write `CHANGELOG.md`** — the entry that creates the feature, with the issue that
carries the why.

**9. Regenerate the global index** — `python3 tools/build_features_index.py`.
Validation fails on drift.

**10. Run the guard-rails.** Every angle you wrote, its `checklist.md`. Then
`python3 tools/validate.py`. A checklist finds what a validator cannot read; the
validator finds what a reader skims past. Neither replaces the other.

**11. Report.** See *What to hand back*, below.

## What to hand back

The format's central claim is that **the absence of a file is an assertion**. That
claim is only true if the assertion is visible, so the report is not a courtesy — it
is what makes the absences auditable:

- the files written, one line each;
- the angles **declined**, each with the question that declined it — "no `legal.md`:
  processes no personal data";
- the angles that were forced by configuration rather than by context;
- what you could not answer and left as an open question in the spec;
- anything the checklists flagged that you did not fix, and why.

An angle absent from this list is an angle nobody can tell was considered.

## Updating an existing feature

1. Read `index.md` first. It tells you which files exist and when to read each.
2. Modify only the files concerned — and re-read the angle's `context.md` if the
   change touches its boundary.
3. If a new subject appears, run that angle's activation questions and create the
   file — don't slip it into `business.md`.
4. Run the changed angles' `checklist.md`.
5. Add an entry to `CHANGELOG.md` with the linked issue, one category.
6. If an optional file becomes meaningless, delete it — an empty file is worse than
   an absent one. Never a mandatory file: one that has gone thin is one to fill, not
   one to remove.
7. If you created, renamed or removed a feature, regenerate the global index
   (`python3 tools/build_features_index.py`).
8. Report, per *What to hand back*.

## Auditing a feature

Run every present angle's `checklist.md` against its file, then look for what no
single checklist can see:

- an `index.md` that no longer matches the files present;
- a link declared on one side only;
- a content-tested file that is absent while its activation questions clearly answer
  yes, with nothing in the index asserting the absence;
- an App feature with no Business parent and no justification;
- a nested feature that should be a sibling, or the reverse — the test is in
  `catalog.md` § *Disposition on disk*;
- an `api-contract.md` that has drifted from the code.

Return one finding per point, with the file path. Rewrite nothing without the user's
agreement.

## Why a catalog rather than a fixed template

This is a preference, not a truth. It comes from a usage finding: a fixed template
produces empty sections filled with "N/A", which nobody cleans up and everybody
reloads. You then no longer know whether "N/A" means "not applicable" or "not thought
through yet".

The catalog moves the problem: **the absence of an optional file becomes
information**. No `legal.md` means "nothing legal at stake", asserted rather than
omitted. It works because it is bounded: `index.md`, `qa.md`, `CHANGELOG.md` and
`business.md` are mandatory, so their absence stays a gap rather than a claim — a
feature nobody can find, follow over time, or test is not a feature. That mandatory
set is this module's own, declared in `references/catalog.md`; another module at the
`specs` slot may require a different one.

In exchange, it demands judgment at writing time. The angles' activation questions
are how that judgment is made repeatable rather than left to taste.

## The TDD angle

This module treats `qa.md` as the central document, not as an appendix. Acceptance
criteria are written **before** implementation and directly become the tests.

- A criterion carries a stable identifier (`AC-1`, `AC-2`) that test code references.
- A ticket cites the `AC-n` it satisfies; a PR shows the criterion → test mapping.
- A criterion that cannot fail is not a criterion.
- When a behavior changes, `qa.md` changes first — the contradiction then surfaces
  before being encoded in code, where fixing it costs the least.

This is what makes a spec verifiable rather than declarative. If you prefer a less
structured approach, this module is not for you — and that's precisely why it's
replaceable.

## The two strata

- **`features/business/<feature>/`** — the *what*. Business value, business rules. No
  screens, no API, no tech. This is the EPIC.
- **`features/app/<app>/<feature>/`** — the *how* of **a single** app. References its
  parent Business feature, and possibly other App features (frontend → backend).

An App feature with no Business parent is suspect: either it's purely technical
(accepted, say so explicitly in its `index.md`), or the Business feature is missing.

A feature may also sit **inside** another, when the parent states what any answer to
its question is held to and the child is one such answer. That is the only reason to
nest; everything else is two features side by side, linked. The test, and the three
constraints that come with nesting, are in `catalog.md` § *Disposition on disk*.

## What else this project asks of a spec

```bash
scrumia-extends write-spec
```

A module the project runs may require something of a feature that this catalog does
not name — a legal note, a security section, a performance budget. It arrives here,
from the module that owns the rule, rather than being restated in this skill or
guessed at. An empty table means the catalog is the whole obligation.

## Splitting: when one feature is really two

A feature is a **unit of value verifiable independently**. The decisive test: can you
write at least one Given/When/Then scenario that validates it **without referencing
another in-progress feature**? If not, it's not a feature.

Signals that splitting is needed:

- `business.md` exceeds ~200 lines, or `qa.md` ~12 scenarios
- Two groups of rules share no vocabulary
- Two parts can be delivered on different dates without breaking each other

Signals for merging (or for "it's a ticket, not a feature"):

- No business rules of its own, a single acceptance scenario → it's a **ticket** on
  an existing feature
- It only makes sense delivered together with another → a single feature

These thresholds are guardrails, not laws. Exceeding one calls for checking, not for
splitting mechanically.

## Never put history in a spec

A spec contains only **its current version**.

**A feature file must contain:**
- The current rule or behavior, stated in the present tense
- A live ownership pointer to another spec or ADR that is the current authority on
  something the file states (e.g. "the type vocabulary is ADR-0017's") — that's
  ownership, not history
- In `qa.md` specifically: testable criteria identified by `AC-n` — the other files
  carry no obligation to

**A feature file must not contain:**
- Quoted or paraphrased former wording — no "formerly", no "since v2", no
  struck-through sections
- Past-tense narration of how or why a change happened — a sentence that describes
  the change instead of the current rule. "By human ruling", "retired", "absorbed",
  "folded into" are the usual tell, not an exhaustive list to pattern-match on: the
  same words read fine describing current behavior ("not folded into `Backlog`"), so
  judge the sentence, not the token
- A ticket, issue or PR number anywhere outside `CHANGELOG.md`
- A specific commit, sprint or other past event cited as evidence for why a rule now
  reads the way it does

Run this checklist on the file you're about to write, not only on review — a spec
that narrates how it got here is the most frequent defect this module's audits find.

History lives in three places, and only one per use: the feature's `CHANGELOG.md`,
short, one entry per notable change; the commits — who changed what, when; the
issues — **why**, which alternatives, which trade-offs. The entry's format is the
[`changelog` angle](references/angles/changelog/context.md)'s to state, once.

## Composition block

This module's contract with the rest of ScrumIA — see
`docs/adr/0016-global-feature-index.md`, which supersedes
`docs/adr/0012-specs-contract.md`. `scrumia-init` copies this block verbatim into
`CLAUDE.md`'s `## Specs contract` section, between the `scrumia:start` markers.
Consumers (`scrumia-ticket`, `scrumia-split`, the team agents) read it from there
instead of hard-coding this module's file names; a module replacing this one at the
`specs` slot must ship its own block in the same shape.

```
specs_root: features/
feature_index: index.md
global_index: index.md
acceptance_file: qa.md
ac_id_format: AC-<n>
changelog: CHANGELOG.md
catalog: business.md, legal.md, archi.md, api-contract.md, tech.md, ux.md, security.md, devx.md
```

`catalog` lists the per-feature files a consumer only expects to find sometimes.
`index.md`, `qa.md` and `CHANGELOG.md` get keys of their own because consumers need a
stable name for each; `global_index` names the file at the root of `specs_root` that
lists every feature, generated by `tools/build_features_index.py` and gated against
drift (see `docs/adr/0016-global-feature-index.md`). Keep this block in sync with
`references/catalog.md` when the catalog changes, or the contract starts lying.

**This block does not declare the mandatory set, and a consumer must not infer one
from it.** A key names a file, it does not require it — a module that carries a
changelog without mandating it still needs a `changelog:` key, or consumers have no
name to use. Of the four files this module mandates in every feature, three are named
outside `catalog` (`index.md`, `qa.md`, `CHANGELOG.md`) and the fourth, `business.md`,
sits inside it — a key's position says nothing about status. Which files are mandatory
is `references/catalog.md`'s to declare — not the contract's.
