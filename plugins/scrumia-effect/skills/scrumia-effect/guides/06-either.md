# 06 — `Either<L, R>` (approach: Either)

> *Approach: `Either` — applies when the project uses `Arrow`'s `Either`, `Rust::Result` (which is structurally similar but with reversed polarity), Haskell's `Either`, or another `Either`-shaped type. A project that does not use `Either` reads no rule in this section as load-bearing.*

`Either<L, R>` is the typed effect for the case where the failure is a value the next operation has to read. The convention is **left for failure, right for success**, and the convention is the rule — reversing it, or treating the type as a generic two-value carrier, is a finding against the rule.

## Prerequisites

- [01-typed-effects](01-typed-effects.md) — `Either` is one typed effect.
- [05-result](05-result.md) — when to migrate from `Result` to `Either`.

## Rules

### Rule 1: Left is failure, right is success — never the other way

`Either<Failure, Success>` (or its equivalent with the left type named for what can fail and the right type named for what can succeed) is the convention. A `Either<Success, Failure>` with the polarity reversed is the failure mode this rule exists to catch: the caller pattern-matches on the wrong side, the failure path runs on success, and the bug is invisible at the type level because both types are valid.

The discipline's test: does the function's signature say `Either<FailureType, SuccessType>`? If the answer is "yes, but I had to flip it because the library's `map` operates on the right," the function has flipped it for the library, not for the discipline.

### Rule 2: The left type names the failure, the right type names the success

`Either<String, User>` is an `Either` whose failure channel carries prose. `Either<NotFound | ValidationError | Conflict, User>` is an `Either` whose failure channel carries the typed cases the next operation will branch on. The discipline prefers the typed cases: the next operation can pattern-match on `when (result) { is Left(NotFound) -> …; is Left(ValidationError) -> …; is Right(user) -> … }` and dispatch on the failure kind, not parse the prose.

### Rule 3: Compose with `flatMap`, short-circuit on left

Two `Either`-returning operations compose on the right channel and short-circuit on the left. The discipline's rule is the same as `Result`'s: `flatMap` is the composition, the first left becomes the result, no further work runs, and the typed left is what the second operation would have needed had the first one succeeded.

### Rule 4: A function that takes an `Either` reads the left

A function that takes `Either<L, R>` as an argument and does not branch on the left has been handed a typed effect and ignored half of it. The discipline refuses the shape on the ground that the function's signature promised to handle both cases, and the implementation handled one.

The test: does the function call `when (it) { is Left -> …; is Right -> … }` or equivalent? If only one branch is implemented, the other is the failure mode this rule catches.

### Rule 5: An `Either` that wraps `Result` is not the migration, it is the confusion

A function that returns `Either<Result<T, E>, T>` has wrapped a typed effect inside the left channel of another typed effect, and the right channel duplicates the success type. The discipline refuses the shape: the inner `Result` is either the failure channel (in which case the `Either` is redundant) or the success channel (in which case the `Either` is broken). The migration from `Result` to `Either` is the left channel taking over the typed-failure role, not the `Either` carrying the `Result` as cargo.

### Rule 6: Pattern-match on the left explicitly

`Either.getOrElse { default }` discards the left. A function whose caller reads only `getOrElse` has been handed a typed effect and treated the left as if it were an `Option.None`. The discipline refuses the silent discard when the caller had reason to branch on the left — the `getOrElse` form is for the case where the failure is genuinely a default-value case, and a caller using it on a typed failure has lost the type.
