# Feature format

The operational reference is the catalog:
[`plugins/scrumia-specs/skills/scrumia-feature/references/catalog.md`](../plugins/scrumia-specs/skills/scrumia-feature/references/catalog.md)

This document explains **why** the format is the way it is.

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

## The three-part boundary

The catalog doesn't just name each file's subject — for every file it states what the file **holds**, what it **may hold**, and what it **must not hold**, and every exclusion names the file where that content goes instead. A scope that only described its subject would leave the boundary to taste; taste is how nine indexes grew sections no template defined.

Three boundaries carry most of the collisions, and each is settled by one membership test rather than restated case by case:

- **business vs ux, on the journey.** A step stated as actor intent and the value delivered, naming no screen, no control, no click path, belongs to `business.md`. The moment it names one, it belongs to `ux.md`.
- **tech vs archi, on data flow.** Flow that never leaves the app's own boundary belongs to `tech.md`. Flow that crosses apps, scoped to an EPIC, belongs to `archi.md`.
- **ux vs qa, on accessibility.** A property the journey must have, stated in prose, belongs to `ux.md`. Anything testable against a named technical criterion — a contrast ratio, a keyboard-trap check, an announcement — is a tagged `qa.md` criterion.

This document explains why the boundary exists; the operational reference — the full three-part entry for every file — is the catalog linked above.

## The two existence categories

**Mandatory in every feature**: `index.md`, `qa.md`, `CHANGELOG.md`, `business.md`. A feature has to be findable, has to be possible to follow over time, has to be possible to test — and has to be worth building: every feature states its value, at both strata, so `business.md` is mandatory everywhere too. Their absence asserts nothing, it is a gap.

**Content-tested**: everything else. A file is created only when it has content; its absence is the assertion "nothing to say on this subject", not an oversight and not a placeholder.

Which files fall in which category is declared by whichever module fills the `specs` slot — this three-way split is `scrumia-specs`'s own declaration, made in its own catalog, and another module may declare a different set. A consumer does not resolve that set for itself — it delegates the writing to the specs module's own writing skill. Note what does *not* declare it: `CLAUDE.md`'s `## Specs contract` block names a module's files so consumers need not hard-code them, and marks none of them required ([ADR-0012](adr/0012-specs-contract.md)).

## Two strata

**`features/business/<feature>/`** — the *what*. Business value, business rules. No screen, no API, no tech. This is the EPIC.

**`features/app/<app>/<feature>/`** — the *how* of **a single** app. It references its Business parent, and possibly other App features.

The rule that matters: **an App feature never copies a business rule**. It references. A rule duplicated in two files will diverge — it's a matter of time, not of discipline.

An App feature without a Business parent is acceptable if it is purely technical, and its `index.md` must say so. Otherwise, the Business feature is missing.

## The catalog

| File | Business | App Backend | App Frontend |
|---|---|---|---|
| `index.md` | **mandatory** | **mandatory** | **mandatory** |
| `business.md` | **mandatory** — value, rules, personas, journey-as-intent | **mandatory** — value + reference to the parent | **mandatory** — value + reference to the parent |
| `qa.md` | **mandatory** | **mandatory** | **mandatory** |
| `CHANGELOG.md` | **mandatory** | **mandatory** | **mandatory** |
| `legal.md` | if personal data, payment, user content, regulated | same | same |
| `security.md` | if the feature has a meaningful risk on availability, integrity, confidentiality or traceability | same | same |
| `archi.md` | if the EPIC touches ≥2 apps | no | no |
| `api-contract.md` | no | if another feature or app parses what it exposes | if it consumes another feature's contract |
| `tech.md` | no | often | sometimes |
| `ux.md` | no | no | often |
| `devx.md` | no | if it exposes a lib | if it exposes components |

**mandatory** marks the files `scrumia-specs` requires of every feature, at every stratum: `index.md`, `business.md`, `qa.md`, `CHANGELOG.md`; every other row is subject to the content test. `api-contract.md` covers any shared interface between features, not only an HTTP API — a file format or a CLI's output shape counts the moment another feature parses it.

The catalog is open. Two rules so it does not sprawl: a new file must have a **distinct reader** (otherwise it is a section, not a file), and its addition must be documented in the catalog — otherwise the next feature will invent another name for the same thing, and the format will lose what makes it useful: its predictability.

## The special role of `index.md`

It is the only file read systematically. Its section set is fixed by the template — `In brief`, `Links`, `Files present`, those three and no others — so a section outside the set is detectable rather than a matter of taste. `Files present` carries **one line per file, stating when to read it**: not why it exists, but the situation that makes an agent open it.

That last point is not decorative: it is what lets an agent load `legal.md` only when the situation calls for it, rather than as a precaution.

Two more rules keep the index from re-growing what it just shed: a spec cites no ticket anywhere — `CHANGELOG.md` excepted — the fact or the open question is stated in words instead; and every feature opens `business.md` with its value stated in four answers — who it is for, what it brings, why it matters, and whether that can be measured.

## The global index

`features/` also carries one index at its root — the file named by the specs contract's `global_index` key, `features/index.md` in this project — listing every feature in one line each: stratum, status, one-line brief. It makes a feature reachable without a pointer and without walking the tree.

It is generated, never hand-written: `python3 tools/build_features_index.py` builds it from the tree, and `tools/validate.py` fails the build on any drift between the two. A stale index is worse than none, because it is believed. See [ADR-0016](adr/0016-global-feature-index.md) for the contract change that named it.

## Never any history in a spec

A spec contains only its current version. No "formerly", no "since v2", no struck-through section.

History lives in three places, one per use:

- **The feature's `CHANGELOG.md`** — short, one entry per change, with pointers
- **The commits** — who changed what, when
- **The issues** — *why*, which alternatives, which trade-offs

```markdown
## 2026-09-12 — MFA required at login
- Issue: #45
- PR: #48 (filled at merge)
- Breaking: yes — see the migration described in #45
```

The reasoning is in `#45`. A changelog entry that explains is a spec that starts growing again — this is exactly how monolithic PRDs re-form.

## Splitting

A feature is a **unit of value verifiable independently**. The test: can you write a Given/When/Then scenario that validates it without depending on another feature in progress?

Thresholds, as guardrails and not as laws: ~200 lines of `business.md`, ~12 scenarios in `qa.md`. In the other direction: no rule of its own and a single scenario means it is a **ticket**, not a feature.

Details and justification in [ADR-0004](adr/0004-feature-splitting.md).

## Writing a `qa.md` that serves its purpose

Given/When/Then, one scenario per case. **A criterion must be able to fail**: "the user must have a good experience" can neither pass nor fail, so it says nothing.

Systematically cover the nominal case, then zero, limit, duplicate, concurrency, cancellation, expiration, insufficient rights. Those are the cases that produce bug tickets.

The "out of scope" section is worth the detour: it prevents bug tickets on behaviors that were never promised.
