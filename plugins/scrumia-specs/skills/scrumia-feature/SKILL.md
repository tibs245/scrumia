---
name: scrumia-feature
description: Creates, updates or audits a ScrumIA feature in features/. Applies the contextual file catalog (index, business, qa, ux, tech, api-contract, legal, a11y, devx) instead of a fixed template. Use it whenever a spec needs to be written, modified or checked.
---

# Writing a ScrumIA feature

A feature is not a document, it's a **directory of targeted files**. Each file has a role and a reader. You only create one if it has something to say.

## Why a catalog rather than a fixed template

This is a preference, not a truth. It comes from a usage finding: a fixed template produces empty sections filled with "N/A", which nobody cleans up and everybody reloads. You then no longer know whether "N/A" means "not applicable" or "not thought through yet".

The catalog moves the problem: **the absence of a file becomes information**. No `legal.md` means "nothing legal at stake", asserted rather than omitted.

In exchange, it demands a bit more judgment at writing time — that's the price to pay, and it doesn't suit every team.

## The TDD angle

This module treats `qa.md` as the central document, not as an appendix. Acceptance criteria are written **before** implementation and directly become the tests.

Concretely:

- A criterion carries a stable identifier (`AC-1`, `AC-2`) that test code references.
- A ticket cites the `AC-n` it satisfies; a PR shows the criterion → test mapping.
- A criterion that cannot fail is not a criterion. "The user must have a good experience" cannot be tested.
- When a behavior changes, `qa.md` changes first — the contradiction then surfaces before being encoded in code, where fixing it costs the least.

This is what makes a spec verifiable rather than declarative. If you prefer a less structured approach, this module is not for you — and that's precisely why it's replaceable.

## The two strata

- **`features/business/<feature>/`** — the *what*. Business value, business rules. No screens, no API, no tech. This is the EPIC.
- **`features/app/<app>/<feature>/`** — the *how* of **a single** app. References its parent Business feature, and possibly other App features (frontend → backend).

An App feature with no Business parent is suspect: either it's purely technical (accepted, say so explicitly in its `index.md`), or the Business feature is missing.

## The catalog

`references/catalog.md` details each file, its content, its reader, and when it is expected. **Read it before creating a feature.** Ready-to-fill templates in `assets/`.

In short:

| File | Business | App Backend | App Frontend |
|---|---|---|---|
| `index.md` | always | always | always |
| `business.md` | always | reference to the parent | reference to the parent |
| `qa.md` | always | always | always |
| `CHANGELOG.md` | always | always | always |
| `legal.md` | if personal data, payment, user content, regulated sector | same | same |
| `archi.md` | if the EPIC touches ≥2 apps | no | no |
| `api-contract.md` | no | often | if it consumes an API |
| `tech.md` | no | often | sometimes |
| `ux.md` | no | no | often |
| `a11y.md` | no | no | often |
| `devx.md` | no | if it exposes a lib or an SDK | if it exposes components |

The catalog is open: `perf.md`, `i18n.md`, `analytics.md` are legitimate if the feature justifies them. When you add one that's not in the catalog, document it in `references/catalog.md` — otherwise the next person will reinvent a different name for the same thing.

## Composition block

This module's contract with the rest of ScrumIA — see `docs/adr/0012-specs-contract.md`. `scrumia-init` copies this block verbatim into `CLAUDE.md`'s `## Specs contract` section, between the `scrumia:start` markers. Consumers (`scrumia-ticket`, `scrumia-split`, the team agents) read it from there instead of hard-coding this module's file names; a module replacing this one at the `specs` slot must ship its own block in the same shape.

```
specs_root: features/
feature_index: index.md
acceptance_file: qa.md
ac_id_format: AC-<n>
changelog: CHANGELOG.md
catalog: business.md, legal.md, archi.md, api-contract.md, tech.md, ux.md, a11y.md, devx.md
```

`catalog` lists the optional per-feature files — the ones a consumer only expects to find sometimes. `index.md`, `qa.md` and `CHANGELOG.md` are named by their own keys because every feature carries them; keep this block in sync with `references/catalog.md` when the catalog changes, or the contract starts lying.

## Splitting: when one feature is really two

A feature is a **unit of value verifiable independently**. The decisive test: can you write at least one Given/When/Then scenario that validates it **without referencing another in-progress feature**? If not, it's not a feature.

Signals that splitting is needed:

- `business.md` exceeds ~200 lines, or `qa.md` ~12 scenarios
- Two groups of rules share no vocabulary
- Two parts can be delivered on different dates without breaking each other

Signals for merging (or for "it's a ticket, not a feature"):

- No business rules of its own, a single acceptance scenario → it's a **ticket** on an existing feature
- It only makes sense delivered together with another → a single feature

These thresholds are guardrails, not laws. Exceeding one calls for checking, not for splitting mechanically.

## Never put history in a spec

A spec contains only **its current version**. No "formerly", no "since v2", no struck-through sections.

History lives in three places, and only one per use:

- The feature's `CHANGELOG.md` — short, one entry per notable change, with pointers
- Commits — who changed what, when
- Issues — **why**, which alternatives, which trade-offs

Changelog entry format:

```markdown
## 2026-09-12 — MFA required at login
- Issue: #45
- PR: #48 (filled at merge)
- Breaking: yes — see the migration described in #45
```

The *why* is in `#45`, not here. A changelog entry that explains its reasoning is a spec starting to grow again.

## Writing a `qa.md` that is useful

Given/When/Then, one scenario per case. An unverifiable criterion is not a criterion: "the user must have a good experience" can neither pass nor fail, so it says nothing.

Systematically cover the nominal case, then: zero, boundary, duplicate, concurrency, cancellation, expiration, insufficient permissions. Those are the cases that produce bug tickets.

## Updating an existing feature

1. Read `index.md` first. It tells you which files exist and why.
2. Modify only the files concerned.
3. If a new topic appears (the feature becomes subject to GDPR), create the file — don't slip it into `business.md`.
4. Add an entry to `CHANGELOG.md` with the linked issue.
5. If a file becomes meaningless, delete it. An empty file is worse than an absent one.

## Auditing a feature

Look for, in this order: inline history (the most frequent defect), files that are empty or full of "N/A", unverifiable acceptance criteria, an `index.md` that no longer matches the files present, an `## Open issues` entry that is closed, an App feature with no Business parent and no justification, an `api-contract.md` that has drifted from the code.

Return one finding per point, with the file path. Rewrite nothing without the user's agreement.
