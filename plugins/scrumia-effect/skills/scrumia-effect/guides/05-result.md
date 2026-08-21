# 05 — `Result<T, E>` (approach: Result)

> *Approach: `Result` — applies when the project uses `kotlin.Result`, `Rust::Result`, or another `Result`-shaped type. A `Result`-only project reads no rule in the `Either` or effect.website sections as load-bearing.*

`Result` carries the success/failure pair through one operation. It is the smallest typed effect most languages ship in their standard library, and the one to reach for when the failure mode is a single kind of error and the operation does not need to compose with another on its failure channel.

## Prerequisites

- [01-typed-effects](01-typed-effects.md) — `Result` is one typed effect.

## Rules

### Rule 1: A function that can fail returns `Result`, not a thrown exception

A function whose failure mode is recoverable (validation, not-found, conflict, timeout) and that the caller is expected to handle returns `Result<T, E>`. The caller observes the failure as a value (`result.isFailure`, `result.exceptionOrNull()`, the `onFailure { … }` branch) and decides what to do — not by catching a `Throwable` that may or may not be the kind the function documented.

The discipline's test: does the function's signature say what can fail it, or does it require the caller to know from the comment? If the answer is the comment, the function has not been typed as an effect.

### Rule 2: The failure type carries the error, not a string

A `Result<T, String>` is a `Result` whose failure channel carries prose. A `Result<T, ValidationError>` (or its equivalent) is a `Result` whose failure channel carries a typed error the caller can branch on. The discipline prefers the typed error: a caller matching on `ValidationError.Missing(field)` does not pattern-match on the string "missing field", and a typed failure is the shape that composes with the next operation.

### Rule 3: Compose with `flatMap`, not with nested `if`

Two operations each returning `Result` compose on their success channel with `flatMap` (or `.andThen` / `.map` on the success branch) and compose on their failure channel by short-circuiting: the first failure becomes the result, no further work runs. The discipline refuses the nested `if (a.isSuccess) { val b = opB(a.getOrThrow()); if (b.isSuccess) { … } }` shape: the composition is what `Result` is for, and not composing is the same as not using `Result`.

### Rule 4: Migrate to `Either` when two operations must compose on their failure

`Result`'s failure channel is `Throwable` in the standard library, and a typed error channel is bolted on per-language. Two operations composing on their typed failure channel — where the second operation's input depends on the first operation's typed failure — is the case `Either<L, R>` exists for. The discipline names the migration: when the failure channel becomes a value the second operation needs to read, `Result` no longer fits.

The test: does the second operation branch on the first operation's failure type, or does it just need to know whether the first one failed? If it branches, `Either`. If it just needs to know, `Result` is still right.

### Rule 5: `Result.runCatching` is a bridge, not a destination

`Result.runCatching { … }` wraps a block that may throw into a `Result` whose failure is the exception. The discipline treats it as a bridge — the seam where a function that throws is converted into a function that returns — and refuses it as a destination: a function whose whole body is `runCatching { … }` has not been written to return a `Result`, it has been wrapped to return one. The bridge belongs at the seam between an un-typed caller and a typed callee, not inside the typed callee itself.

### Rule 6: Do not re-throw from inside `Result`'s success path

A `Result`-returning function that calls another `Result`-returning function and re-throws on failure has unwrapped the typed failure and discarded its type. The discipline refuses the shape on the same ground as the typed failure rule: the caller, who needed to branch on the failure type, now has to catch the exception and inspect it, and the typed effect has been undone.
