# D-03: No generic traits with a single implementer

**Status**: Adopted
**Date**: 2026-08-07
**Impacts**: [guides/02-domain-types.md](../guides/02-domain-types.md)

## Context

A trait defined ahead of any second implementation is indirection without polymorphism: one concrete type behind an interface nobody else implements, paid for at every call site and every read.

## Arguments For

- Generic traits with a single implementer add indirection without polymorphism — there is nothing to be polymorphic over yet.
- Traits are for real polymorphism: two living implementers, or a genuine test-double need at an infrastructure boundary — not decoupling on principle.
- When the variants are finite and known, an `enum` and an exhaustive `match` do the same job better: adding a variant breaks at compile time everywhere it isn't handled, which is a help, not a hindrance.

## Arguments Against (trade-offs accepted)

- A trait drawn early can look forward-thinking, ready for a second implementation that seems inevitable — accepted cost: it usually isn't inevitable, and the trait sits unused.
- Extracting a trait later, once a second implementer genuinely arrives, does cost a refactor — accepted explicitly: **the day the second implementer arrives, the extraction costs ten minutes.** That ten minutes is cheaper than the indirection tax paid on every read until then.
- Test doubles at infrastructure boundaries are a legitimate second implementer from day one — this is the carve-out, not an exception to argue around case by case.

## Verdict

No trait until two living implementers exist, or a genuine test double is needed at an infrastructure boundary. Closed, known variants get an `enum` + exhaustive `match` instead — the compiler enforces exhaustiveness the moment a variant is added.
