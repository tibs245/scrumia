# 01 — Typed effects (discipline)

> *Approach: discipline — applies regardless of whether the project uses `Result`, `Either`, `IO`/suspend, or effect.website.*

An effect is a description of a value-producing action, not the action itself. The type carries that distinction, so the compiler can tell whether a function performed the effect or returned one.

## Prerequisites

None — this is the foundation of the whole module. Every other guide assumes an effect is typed.

## Rules

### Rule 1: An effect is a value, not an event

A function whose return type is `Result<T, E>`, `Either<E, T>`, `IO<E, A>` (or its equivalent) returns a **description** of the effect, not the effect itself. The function does not throw, does not read the clock, does not write to disk, does not call the network — it builds the description. Execution is a separate step, performed at the seam, by a function whose return type is the bare value (or the impure terminal the runtime provides).

The test is at the type level: a function that returns `IO<Int>` has the type of a description; a function that returns `Int` has the type of a value. The compiler sees the difference; the program depends on the compiler seeing it.

### Rule 2: The type carries the discipline, not the comment

A `suspend` function is the discipline's marker in Kotlin; an `IO<A>` is the discipline's marker in Scala/Arrow/Haskell-style code; an `Effect<R, E, A>` is the discipline's marker in effect.website. The marker is not optional: a function that reads the clock and returns `Int` is not typed as an effect — the type system says it is pure, and the type system is right until the comment says otherwise. Comments are not a substitute for types.

### Rule 3: The description names what it produces and what can fail it

`Result<T, E>` names the success type `T` and the failure type `E`. `Either<E, T>` names the failure type `E` (left) and the success type `T` (right). `IO<E, A>` names the failure channel `E` and the success channel `A`. A description that omits the failure channel — `IO<A>` with no error model, `suspend (): T` with no `Throwable` — has not described what can fail it; the discipline refuses the omission.

The discipline's test: can a reader name, from the type alone, the shape of what comes back when the function does not perform its effect? If the answer is "no, that's in the implementation," the function has not been typed as an effect.

### Rule 4: An effect that is not described is not an effect

A function that performs IO at the call site — `fun loadUser(): User = api.get("/users/$id")` — performs the effect when it is called, not when its result is consumed. The discipline refuses the shape on the ground that the call site cannot defer the effect, cannot compose it with another effect, and cannot substitute a test for it without a mocking boundary that exists only because the type did not.

The fix is structural, not stylistic: return the description (`suspend () -> User`, `IO<User>`, `Effect<User>`), and let the caller decide when to run it.

### Rule 5: A description whose type is not an effect type is not typed as one

Returning `Either<String, User>` for a function that reads a file is a typed effect. Returning `User` with the file read inside the function is not — even if the comment says "this might fail." The discipline is read off the type, not off the comment, and a discipline read off the comment is not the discipline this module owns.
