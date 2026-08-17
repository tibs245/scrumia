# Feature format

The operational reference is the catalog: [`../references/catalog.md`](../references/catalog.md)

This document explains **why** the format is the way it is. It ships alongside the
catalog, inside `scrumia-specs` itself, so what a project reads matches the version of
the skill it actually has installed — not whatever this repository's `main` branch
carries at the moment someone opens a link.

**This repository additionally restates the format rule at two sites of its own,
neither shipped to a consumer project** — `docs/architecture.md` restates it in prose;
`site/i18n/{en,fr}/modules/scrumia-specs.json` (`refusals`, `philosophy`) restates it for
`site/**/modules/*.html`, which is **generated** from that JSON by
`tools/build_site.py` — edit the JSON and rebuild, both languages. Sweep these two in
addition to the catalog's own list, but only when working in this repository itself.

## What we replace

A monolithic PRD has four defects, and they make each other worse:

1. It grows indefinitely — every feature adds, none removes.
2. It gets reloaded in full to read three lines — the context explodes, every time.
3. It accumulates obsolete sections nobody cleans up — nothing is authoritative anymore.
4. It becomes unreadable for the human and the agent alike — so nobody verifies it anymore.

The fourth defect is the worst: from the moment nobody verifies anymore, the document keeps being cited while it is wrong.

## The principle: absence is information

A feature is a **directory of targeted files**, each the output of one **angle** — one
way of interrogating the feature, with its own reader. An optional file is created only
if it has content.

This seemingly innocuous rule is the heart of the format. With a fixed template, `legal.md` always exists and contains "N/A" — and you don't know whether that means "not applicable" or "not thought through yet". With the catalog, the absence of `legal.md` is an **assertion**: nothing legal at stake.

Direct consequence: an agent can decide what to read without reading everything. That is what keeps the context cost contained.

## The boundary

A subject alone does not make a scope: taste is how nine indexes grew sections no
template defined. So each angle states a three-part boundary — holds, may hold, must
not hold, every exclusion naming its destination — and the collision-prone edges are
settled by membership tests instead of case-by-case debate.

An angle ships three files, and the split is deliberate. `context.md` says what the
angle answers, **when it activates**, and the questions that explore it; `template.md`
is what gets copied; `checklist.md` is the guard-rails a reviewer runs against the
result. Judgment that stays in someone's head is applied differently every time — the
questions make it repeatable, and the checklist makes it checkable by someone who did
not write the file.

The tests and the existence categories (which files are mandatory, which are
content-tested) live **once**, in the catalog linked above; each angle's own boundary
lives once, in its `context.md`. This document restates neither, because a second copy
is how they drift.

## Activation, and why it is written as closed questions

The catalog's conditional column — "if personal data", "if it touches ≥2 apps" — is a
reminder, not the rule. The rule is a table of closed questions in each angle's
`context.md`, each with the answer to take when unsure.

That shape is chosen for a specific failure: open-ended judgment, applied by a reader
in a hurry or by a model with little room to reason, defaults to "no" on every
question — so the conditional file never gets written, and its absence is read as an
assertion nobody made. A closed question with a stated default fails the other way,
which is the cheaper direction.

A project can take the judgment out of the writer's hands entirely, per angle, through
`params.angles` in `.scrumia/config.yaml`: `always`, `context` (the default), `never`.
That is for projects whose obligations do not vary feature by feature — an audited
codebase where an absent `security.md` is never an acceptable assertion. The mandatory
four ignore the setting.

Which files are mandatory is the plugged specs module's own declaration, made where
its catalog lives; another module may declare a different set. A consumer delegates
the writing to that module's writing skill, and does not infer the set from
`CLAUDE.md`'s `## Specs contract` block, which names files without marking any of
them required ([ADR-0016](https://github.com/tibs245/scrumia/blob/main/docs/adr/0016-global-feature-index.md)).

## Two strata

**`features/business/<feature>/`** — the *what*. Business value, business rules. No screen, no API, no tech. This is the EPIC.

**`features/app/<app>/<feature>/`** — the *how* of **a single** app. It references its Business parent, and possibly other App features.

The rule that matters: **an App feature never copies a business rule**. It references. A rule duplicated in two files will diverge — it's a matter of time, not of discipline.

An App feature without a Business parent is acceptable if it is purely technical, and its `index.md` must say so. Otherwise, the Business feature is missing.

## One feature inside another

A feature may sit inside another, in the parent's own directory. One thing licenses
that: the parent states what any answer to its question is held to, and the child is
one such answer. Everything else — dependency, a shared subject, a mention — is two
features side by side, linked but not nested.

The distinction is not filing preference. Nesting says "you cannot understand this
without its parent"; juxtaposition says "these two are peers". A reader who lands on a
nested feature reads its parent first, and a reader who lands on a sibling does not
need to. Getting it wrong makes one of those two reads wasted, every time.

Two constraints keep it from becoming a folder tree: a parent is a full feature with
content of its own — this format has no grouping directory — and nesting stops at one
level. A child of a child means the middle level was really the feature. The test and
its rules are the catalog's.

The catalog is open. Three rules so it does not sprawl: a new angle must have a
**distinct reader** (otherwise it is a section, not an angle); it ships the full
directory — questions, template, checklist; and it is listed in the catalog's table.
Otherwise the next feature will invent another name for the same thing, and the format
will lose what makes it useful: its predictability.

## The special role of `index.md`

It is the only file read systematically. Its section set is fixed by the template — `In brief`, `Links`, `Files present`, those three and no others — so a section outside the set is detectable rather than a matter of taste. `Files present` carries **one line per file, stating when to read it**: not why it exists, but the situation that makes an agent open it.

Its `Links` vocabulary is fixed for the same reason. Left open, it grew fifteen keys
across twenty indexes — two of them meaning the same thing, several invented once and
never reused — and a link nobody can resolve mechanically is one nobody checks. Nine
keys now: four structural, declared on both sides because they describe where the
feature sits; five referential, one-sided because the authority owes nothing back.

That last point is not decorative: it is what lets an agent load `legal.md` only when the situation calls for it, rather than as a precaution.

Two more rules keep the index from re-growing what it just shed: a spec cites no ticket anywhere — `CHANGELOG.md` excepted — the fact or the open question is stated in words instead; and every feature opens `business.md` with its value stated in four answers — who it is for, what it brings, why it matters, and whether that can be measured.

## The global index

`features/` also carries one index at its root — the file named by the specs contract's `global_index` key, `features/index.md` in this project — listing every feature in one line each: stratum, status, one-line brief. It makes a feature reachable without a pointer and without walking the tree.

It is generated, never hand-written: `python3 tools/build_features_index.py` builds it from the tree, and `tools/validate.py` fails the build on any drift between the two. A stale index is worse than none, because it is believed. See [ADR-0016](https://github.com/tibs245/scrumia/blob/main/docs/adr/0016-global-feature-index.md) for the contract change that named it.

## Never any history in a spec

A spec contains only its current version. No "formerly", no "since v2", no struck-through section.

History lives in three places, one per use: the feature's `CHANGELOG.md` — short, one
entry per change, and the **only** spec file allowed to cite an issue — and only an
issue, since the entry ships inside the PR that would number it; the commits — who
changed what, when; the issues — *why*, which
alternatives, which trade-offs. A changelog entry that explains its reasoning is a
spec that starts growing again — this is exactly how monolithic PRDs re-form. The
entry's exact shape is the catalog's and the template's to state, once.

## Splitting

A feature is a **unit of value verifiable independently**. The test: can you write a
Given/When/Then scenario that validates it without depending on another feature in
progress? In the other direction: no rule of its own and a single scenario means it
is a **ticket**, not a feature. The numeric guardrails and their justification are
[ADR-0004](https://github.com/tibs245/scrumia/blob/main/docs/adr/0004-feature-splitting.md)'s; validation surfaces a breach as a
warning so the fourth one is not silent.
