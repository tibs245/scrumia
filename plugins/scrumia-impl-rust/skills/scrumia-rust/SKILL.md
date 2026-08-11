---
name: scrumia-rust
description: The Rust practices of ScrumIA — tests per invariant, unrepresentable invalid states, typed errors per layer, structure by domain, and what we refuse. Load it before writing code in an app whose implementation module is scrumia-impl-rust.
---

# Coding in Rust

This module contributes to `build/apply-implementation` for every app that lists it in its own `extends` in `.scrumia/config.yaml`. It is the authority on the "how" in those apps — including against your preferences. It is one choice among other possible ones; it is worth what its reasons are worth, given with each rule.

## The contract

- **How we test** — one test per invariant, not per function; the compiler is the first test suite. → [04-testing](guides/04-testing.md)
- **Which design principles** — invalid states unrepresentable is the organizing principle; `Result` at the boundaries, typed errors per layer. → [02-domain-types](guides/02-domain-types.md), [03-errors](guides/03-errors.md)
- **How the code is structured** — modules by domain, thin `lib.rs`, workspace from the second deployable unit on, `unsafe` isolated behind a `SAFETY:` comment. → [01-project-layout](guides/01-project-layout.md), [05-lints](guides/05-lints.md)
- **What we refuse** — `unwrap`/`expect` in production, defensive `clone`, single-implementer traits, `Deref`-as-inheritance, `allow` that settles in, leaky public error types. → [D-01](decisions/D-01-no-unwrap-expect.md), [D-02](decisions/D-02-no-clone-to-appease-borrowck.md), [D-03](decisions/D-03-no-single-implementer-traits.md), [D-04](decisions/D-04-no-deref-inheritance.md)

## Guides

| File | Use when you need to... |
|------|------------------------|
| [01-project-layout](guides/01-project-layout.md) | Lay out a new workspace, place a crate, decide what a crate may depend on |
| [02-domain-types](guides/02-domain-types.md) | Model a domain value or state so invalid states can't compile |
| [03-errors](guides/03-errors.md) | Define a layer's error enum, translate an error from the layer below |
| [04-testing](guides/04-testing.md) | Write a test for an invariant, decide unit vs. integration vs. proptest |
| [05-lints](guides/05-lints.md) | Set the workspace clippy baseline, write an `unsafe` block |

## Routing table

```
"I need to lay out a new workspace or place a crate"
  → 01-project-layout

"I need to model a domain value or state"
  → 01-project-layout + 02-domain-types

"I need to define an error type or translate one from another layer"
  → 01-project-layout + 03-errors

"I need to write a test for an invariant"
  → 02-domain-types + 03-errors + 04-testing

"I need to set the clippy baseline or write an unsafe block"
  → 02-domain-types + 04-testing + 05-lints

"I need the full contract before writing code in a covered app"
  → 01-project-layout + 02-domain-types + 03-errors + 04-testing + 05-lints
```

## Dependencies between guides

```
01-project-layout ← foundation, no dependencies
02-domain-types   ← requires 01
03-errors         ← requires 01
04-testing        ← requires 02, 03
05-lints          ← requires 02, 04
```

## Decisions

The `decisions/` folder explains **why** each refusal was adopted — not needed to write code, useful to challenge or evolve the rule via PR.

| ADR | Decision | Related guide |
|-----|----------|---------------|
| [D-01](decisions/D-01-no-unwrap-expect.md) | No `unwrap()`/`expect()` outside tests and declared prototypes | 05-lints |
| [D-02](decisions/D-02-no-clone-to-appease-borrowck.md) | No `clone()` to silence the borrow checker | 02-domain-types |
| [D-03](decisions/D-03-no-single-implementer-traits.md) | No generic traits with a single implementer | 02-domain-types |
| [D-04](decisions/D-04-no-deref-inheritance.md) | No `Deref` to simulate inheritance | 02-domain-types |

## Settings

Under `settings.implementation.scrumia-impl-rust` in `.scrumia/config.yaml`:

```yaml
settings:
  implementation:
    scrumia-impl-rust:
      test_runner: cargo        # cargo | nextest
      clippy: default           # default | pedantic
      coverage_threshold: null  # a number, or null: no imposed threshold
      msrv: null                # "1.79" to pin a minimum version
```

## Project override

If `.scrumia/impl/scrumia-impl-rust.md` exists, its content takes precedence over this skill and its guides. A project records its house conventions there — a legacy crate, an error exception, a runtime choice — without forking the module.

## The module's other skill

`scrumia-rust-audit` — measures the gap between an existing app and these rules, finding by finding, citing the guide or decision each finding violates.

## Scope

This module applies to apps whose `.scrumia/config.yaml` lists `scrumia-impl-rust` in the app's own `extends`. Within such an app, `section.json`'s globs (`**/*.rs`, `Cargo.toml`) pick which files trigger the guides above.
