# ADR-0004 — Feature splitting criterion

**Status**: accepted — 2026-08-07

## Context

The file catalog solves the size of **one** feature, not the number of features. Without a criterion, two symmetrical drifts appear: features too big, reproducing the monolithic PRD at directory scale; or features too small, where the overhead of `index.md` and `CHANGELOG.md` exceeds the content.

A usable criterion must be verifiable by an agent without subjective judgment.

## Decision

**A feature is a unit of value that can be verified independently.**

The decisive test: *can you write at least one Given/When/Then scenario that validates it, without depending on another feature under construction?*

If not, it's not a feature — it's a piece of another one.

### Layer rules

- A **Business** feature carries its own business rules and its own acceptance criteria.
- An **App** feature is the share of a Business feature in **a single** app. Never two.
- An App feature without a Business parent is acceptable if it is purely technical, and its `index.md` must say so explicitly. Otherwise, the Business feature is missing.

### Operational thresholds

Guardrails, not laws. Exceeding one calls for checking, not for splitting mechanically.

**Splitting signals**
- `business.md` exceeds ~200 lines
- `qa.md` exceeds ~12 scenarios
- Two groups of rules share no vocabulary
- Two parts can ship on different dates without breaking each other

**Merge signals, or "it's a ticket"**
- No business rule of its own and a single acceptance scenario → it's a **ticket** on an existing feature
- It only makes sense shipped with another one → a single feature

## Consequences

**What we gain**

- The main criterion is binary and verifiable: the independent scenario exists, or it doesn't.
- The feature / ticket distinction becomes sharp, which prevents the proliferation of micro-features.
- The "one App feature, one app" rule guarantees no feature becomes a coupling point between apps.

**What we accept**

- *The thresholds are arbitrary.* 200 lines and 12 scenarios come from experience, not from measurement. They're there to trigger a check, not to decide. To be revised after a few real projects.
- *A feature can legitimately exceed the thresholds* when its domain is intrinsically dense. The independent-scenario test always takes precedence over the thresholds.

## Rejected alternatives

**Splitting by estimated implementation size.** Makes the spec structure depend on technical choices, when the Business layer must be independent of them. And an estimate before splitting is a fabrication.

**Splitting by team or by app, including on the Business side.** Reproduces the org chart in the specs. A business rule doesn't change because two teams share it — the App layer carries that projection.

## To revisit

After three real projects, with the sizes actually observed.
