# ADR-0005 — Validation gates and autonomy levels

**Status**: accepted — 2026-08-07

## Context

Two questions remained open: where exactly does the human step in, and can they fully delegate validation on certain ticket types (a pure refactoring with no behavior change, for instance)?

BMAD's flaw is mobilizing the human uniformly, including when the decision is already made. The symmetrical flaw — automating everything — removes the only guarantee left when agents get things wrong in plausible ways.

## Decision

### Three gates, of increasing cost

**Gate 1 — Automatic.** CI, linter, tests. Blocking, no human. A failure here never escalates higher.

**Gate 2 — Agent.** Routed by the actual scope of the diff, not by the announced label:

| What the PR touches | Reviewers |
|---|---|
| 1 app, no spec | executor's self-review |
| Code, one App spec | `scrumia-tech` |
| `features/business/**`, `legal.md` | `scrumia-tech` + `scrumia-business` |
| ≥2 apps, or an `api-contract.md` | `scrumia-tech`, + `scrumia-business` if business logic is at stake |

**Gate 3 — Human.** The merge to the default branch. **Always**, except for categories explicitly listed in `.scrumia/config.yaml`.

### Autonomy levels

An explicit dial in `.scrumia/config.yaml`:

- **`guided`** — the human validates each ticket's scoping *and* each PR. Starting regime, while calibrating.
- **`assisted`** — agents scope and execute on their own; the human validates PRs. The target cruising regime.
- **`autonomous`** — like `assisted`, plus auto-merge for the categories listed in `auto_merge`.

### On full delegation

**Yes, but through an explicit, versioned whitelist, never through a general rule.**

```yaml
autonomy:
  level: autonomous
  auto_merge:
    - docs-only          # no file outside docs/ and *.md
    - dependency-patch   # patch bump, green CI
```

Three cumulative conditions for an auto-merge to trigger: the category is listed, CI is green, and Gate 2 raised no blocker.

The "refactoring with no behavior change" category is **deliberately excluded** from the default list. It is undecidable automatically: it's precisely when an agent believes it's changing nothing that it changes something. Nothing prevents adding it on a given project — that will be a conscious decision, written in a versioned file.

## Consequences

**What we gain**

- Validation cost tracks risk, instead of being uniform.
- Autonomy is a project datum, not an implicit property: it can be read, discussed in PR, tightened after an incident.
- The whitelist makes every delegation explicit and traceable.

**What we accept**

- *The human remains the bottleneck in `assisted` mode.* Deliberately so: it's the price of a guarantee that holds when agents get things wrong in plausible ways. The remedy is PR throughput, not PR removal — hence batches of 3 to 5 tickets rather than 15.
- *Gate 2 routing runs on the actual diff*, which costs a `gh pr diff` before routing. Negligible, and it prevents a mislabeled ticket from escaping its review.

## Rejected alternative

**A general auto-merge rule based on a confidence score.** An aggregate score gives a false impression of measurement: it produces exactly the same verdict for a trivial change and for a subtly wrong change that ticks the same boxes. A whitelist of named categories can be read and contested; a numeric threshold cannot.
