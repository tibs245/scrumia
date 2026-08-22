# 07 — IO / suspend (approach: IO/suspend)

> *Approach: `IO`/suspend — applies when the project uses Kotlin's `suspend`, Arrow's `IO`, Haskell's `IO`, Rust's `async`, or any other "description/execution split" type. `suspend` is named here as the discipline's marker; rules on its **behaviour** — cancellation, structured concurrency, dispatchers, `Flow` — live in `scrumia-kotlin`.*

The description/execution split as a discipline: an effect is a value the program holds, and execution happens at the seam. `suspend` is Kotlin's name for the marker; `IO<A>` is the Scala/Arrow/Haskell name for the type; `Future<T>` (in some languages) is the closest structural equivalent but with a different discipline — what the rest of this module says applies only to true description/execution types, not to eagerly-running `Future`s.

## Prerequisites

- [01-typed-effects](01-typed-effects.md) — `IO` and `suspend` are typed effects.
- [02-describe-before-execute](02-describe-before-execute.md) — the split is the discipline.

## Rules

### Rule 1: A `suspend` function returns a value, not runs the effect

A `suspend fun loadUser(id: UserId): User` returns a `User`. The function does not perform the effect — it suspends, and the coroutine machinery performs the effect at the appropriate point. The discipline refuses the shape on the same ground as the typed-effect rule: the function's type says it produces a value, and the function's body must do what the type says.

This is the discipline's marker in Kotlin: `suspend` names the description/execution split, and a `suspend` function that does not suspend (because it does no effect work) is a candidate for being non-`suspend`, and a non-`suspend` function that does effect work is the failure the rule catches.

### Rule 2: An `IO` value is a description, executed at the seam

`IO { … }` builds a description. `unsafeRunSync()` (or `unsafeRunAsync()`, or the equivalent in each approach) runs it. The discipline treats the run function as the seam — the one place where the description becomes execution — and refuses a program that runs effects at construction time, that runs effects inside another `IO`'s block, or that has no named seam at all.

The test: can a reader name the function whose body calls `unsafeRunSync` / `unsafeRunAsync` / the equivalent? If the answer is "the entry point, somewhere, eventually," the seam is not named.

### Rule 3: Compose with `flatMap` (or `>>=`), not with nested `run`

Two `IO`s combine with `flatMap` (or `>>=` / `andThen`) as descriptions. The composition is a description; the run is at the seam. The discipline refuses the nested `ioA.unsafeRunSync().let { ioB.unsafeRunSync() }` shape: the seam has been crossed twice, the boundary has been lost, and the second `IO` is being run inside a program that was supposed to be pure.

### Rule 4: The failure channel is typed, not a thrown exception

`suspend fun loadUser(id: UserId): User` returning a `User` after throwing an exception on failure has performed the effect and discarded the typed failure. The discipline refuses the shape: a `suspend` function that can fail should either return a `Result<User, Failure>` (typed effect) or throw an exception the caller can catch with the typed information — `suspend fun loadUser(id: UserId): User` performing a `throw NotFoundException(id)` is the second form, and the rule is that the exception type is named in the signature (`@Throws(NotFoundException::class)`, the equivalent), not buried in the body.

In `IO`, the equivalent rule is `IO<E, A>` — the failure type is named, the `IO` returns a description of it, and the program dispatches on `ExitCase.Failure` (in effect.website) or the equivalent rather than catching a thrown exception.

### Rule 5: `suspend` is named here; its behaviour lives in `scrumia-kotlin`

This module names `suspend` as the discipline's marker in Kotlin and does not own the rules on its behaviour. Cancellation, structured concurrency, dispatchers, `Flow`, `CoroutineContext`, the `viewModelScope.launch { … }` pattern — every one of those is `scrumia-kotlin`'s to state. A reviewer finding a rule about one of them in this module names it as misplaced and proposes the move.

The split is by what the rule is **about**: this module's rules are about the description/execution split; `scrumia-kotlin`'s rules are about the coroutine machinery that runs descriptions. The two cite each other in prose where the rule needs to.

### Rule 6: An `async`/`Future` is not an `IO`

A `Future<T>` (in Scala, Java) that runs when constructed is not an `IO` — it is an eagerly-running effect with a value type. The discipline refuses the conflation: a project adopting `IO` does not adopt `Future` as the same thing, and a project whose only effect type is `Future` is not running this section's rules at all (it is running whatever its `Future` library says).

The test: does the type run at construction or at run? If at construction, it is not an `IO`, and the rules in this section do not apply to it.
