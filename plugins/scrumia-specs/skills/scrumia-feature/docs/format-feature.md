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

A feature is a **directory of targeted files**, each with a role and a reader. An optional file is created only if it has content.

This seemingly innocuous rule is the heart of the format. With a fixed template, `legal.md` always exists and contains "N/A" — and you don't know whether that means "not applicable" or "not thought through yet". With the catalog, the absence of `legal.md` is an **assertion**: nothing legal at stake.

Direct consequence: an agent can decide what to read without reading everything. That is what keeps the context cost contained.

## The boundary

A subject alone does not make a scope: taste is how nine indexes grew sections no
template defined. So the catalog states, for every file, a three-part boundary —
holds, may hold, must not hold, every exclusion naming its destination — and settles
the collision-prone edges with membership tests instead of case-by-case debate. The
tests, the boundaries and the existence categories (which files are mandatory, which
are content-tested) live **once**, in the catalog linked above — this document does
not restate them, because a second copy is how they would drift.

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

The catalog is open. Two rules so it does not sprawl: a new file must have a
**distinct reader** (otherwise it is a section, not a file), and its addition must be
documented in the catalog, boundary included — otherwise the next feature will invent
another name for the same thing, and the format will lose what makes it useful: its
predictability.

## The special role of `index.md`

It is the only file read systematically. Its section set is fixed by the template — `In brief`, `Links`, `Files present`, those three and no others — so a section outside the set is detectable rather than a matter of taste. `Files present` carries **one line per file, stating when to read it**: not why it exists, but the situation that makes an agent open it.

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
