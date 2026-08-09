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

A feature is a **directory of targeted files**, each with a role and a reader. A file is created only if it has content.

This seemingly innocuous rule is the heart of the format. With a fixed template, `legal.md` always exists and contains "N/A" — and you don't know whether that means "not applicable" or "not thought through yet". With the catalog, the absence of `legal.md` is an **assertion**: nothing legal at stake.

Direct consequence: an agent can decide what to read without reading everything. That is what keeps the context cost contained.

The rule gates the **optional** files, not every file a feature holds. `index.md`, `qa.md` and `CHANGELOG.md` are mandatory: a feature must be possible to follow over time and possible to test, and an absent changelog asserts nothing except that nobody wrote one. Which files are mandatory is declared by whichever module fills the `specs` slot — those three are `scrumia-specs`'s declaration, and another module may require a different set. A consumer reads the one in force from `CLAUDE.md`'s `## Specs contract` block, never from this page ([ADR-0012](adr/0012-specs-contract.md)).

## Two strata

**`features/business/<feature>/`** — the *what*. Business value, business rules. No screen, no API, no tech. This is the EPIC.

**`features/app/<app>/<feature>/`** — the *how* of **a single** app. It references its Business parent, and possibly other App features.

The rule that matters: **an App feature never copies a business rule**. It references. A rule duplicated in two files will diverge — it's a matter of time, not of discipline.

An App feature without a Business parent is acceptable if it is purely technical, and its `index.md` must say so. Otherwise, the Business feature is missing.

## The catalog

| File | Business | App Backend | App Frontend |
|---|---|---|---|
| `index.md` | **mandatory** | **mandatory** | **mandatory** |
| `business.md` | the rules themselves | reference to the parent | reference to the parent |
| `qa.md` | **mandatory** | **mandatory** | **mandatory** |
| `CHANGELOG.md` | **mandatory** | **mandatory** | **mandatory** |
| `legal.md` | if personal data, payment, user content, regulated | same | same |
| `archi.md` | if the EPIC touches ≥2 apps | no | no |
| `api-contract.md` | no | often | if it consumes an API |
| `tech.md` | no | often | sometimes |
| `ux.md` | no | no | often |
| `a11y.md` | no | no | often |
| `devx.md` | no | if it exposes a lib | if it exposes components |

**mandatory** marks the files `scrumia-specs` requires of every feature, whatever it is about; every other row is subject to the content test.

The catalog is open. Two rules so it does not sprawl: a new file must have a **distinct reader** (otherwise it is a section, not a file), and its addition must be documented in the catalog — otherwise the next feature will invent another name for the same thing, and the format will lose what makes it useful: its predictability.

## The special role of `index.md`

It is the only file read systematically. It carries the summary, the status, the links, and above all **the list of the files present with one line saying why each one exists**.

That last point is not decorative: it is what lets an agent load `legal.md` only when it is relevant, rather than as a precaution.

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
