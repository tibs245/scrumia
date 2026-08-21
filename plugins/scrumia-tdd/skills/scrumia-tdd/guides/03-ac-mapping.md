# From Acceptance Criteria to Tests

> Every acceptance criterion in scope becomes at least one test, and the link stays visible.

## Prerequisites

- [01-the-cycle](01-the-cycle.md) — this guide feeds the "next invariant" of the cycle's red step.

## Rules

### Rule 1: Every `AC-n` in scope becomes at least one test

If the project writes acceptance criteria — whatever specs module carries them — each `AC-n` in scope becomes at least one test, and the link stays visible: the identifier in the test name or in an adjacent comment.

### Rule 2: Without formal criteria, draw invariants from the request itself

Write them at the top of the suite. A ticket with no verifiable invariant does not get coded in TDD — it gets sent back to scoping.

### Rule 3: Cover the nominal case, then the systematic edge cases

Zero, boundary, duplicate, concurrency, cancellation, expiration, insufficient permissions. These are the cases that produce bug tickets.

## Settings

Under this module's own `params:` in `.scrumia/config.yaml`, beside the key of the app
that lists it:

```yaml
apps:
  - name: api
    modules:
      "tibs245/scrumia:scrumia-tdd":
        params:
          ac_mapping: strict    # strict: every AC-n cited by a test; loose: correspondence checked at PR
          exempt_paths: []      # paths declared outside TDD (prototypes, generated/)
```

Read the effective value through `scrumia-extends --settings`, never out of the file — historically this sat under `settings.practices`, which the resolver still reconciles for the deprecation window.

`ac_mapping: strict` enforces Rule 1 at commit time — no `AC-n` without a citing test. `ac_mapping: loose` defers the check to PR review, for projects that iterate faster than they can keep the citation current. `exempt_paths` names the paths carved out of this guide and of [04-where-tdd-stops](04-where-tdd-stops.md) — prefer a declared exemption there over a silent one here.
