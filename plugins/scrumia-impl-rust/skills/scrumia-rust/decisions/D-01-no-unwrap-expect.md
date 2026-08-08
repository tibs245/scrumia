# D-01: No `unwrap()` / `expect()` outside tests and declared prototypes

**Status**: Adopted
**Date**: 2026-08-07
**Impacts**: [guides/05-lints.md](../guides/05-lints.md)

## Context

`unwrap()` and `expect()` turn a `Result`/`Option` into an unconditional panic. Used freely in production code, they let error handling silently degrade into a crash the moment the path they guard is actually exercised.

## Arguments For

- Every `unwrap()` in production is a panic waiting for its triggering input — the type system offered an `Err`/`None` path and the call site chose not to handle it.
- `unwrap_used = "deny"` in the workspace clippy config turns this from a convention into a build failure, catching regressions before review rather than in production.
- Forcing `expect("invariant: <why>")` when impossibility is genuinely proven makes the proof visible at the call site instead of living only in the author's head.

## Arguments Against (trade-offs accepted)

- Prototypes and throwaway exploration code slow down if every early sketch must thread `Result` — accepted by exempting **declared** prototypes explicitly, not by weakening the rule for everything else.
- Tests gain nothing from proper error propagation ceremony — a failed `unwrap()` in a test is already the failure signal — accepted by exempting `#[cfg(test)]` code from the lint.
- `expect("invariant: …")` is more typing than `unwrap()` for genuinely impossible cases — accepted as the cost of the message being the proof, not just an incantation.

## Verdict

`unwrap()` and `expect()` are denied by lint everywhere except tests and code explicitly declared a prototype. Elsewhere, an `Err`/`None` path is either propagated or turned into `panic!`/`expect("invariant: …")` whose message states which invariant makes the branch impossible.
