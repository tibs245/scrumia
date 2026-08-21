# 09 — When to throw (error semantics)

> *Approach: error semantics — applies regardless of whether the project uses `Result`, `Either`, `IO`/suspend, or effect.website. HTTP-status-as-effect lives in `scrumia-ktor`, not here.*

Recoverable failures (validation, not-found, conflict, timeout) return a value. Unrecoverable failures (invariant violation, exhausted resources, programmer error) throw. The test: **if I catch this and continue, do I know what's true?**

## Prerequisites

None — the throw-or-return test applies to any function in any approach.

## Rules

### Rule 1: Recoverable failures return a value

A function whose failure mode is recoverable — the caller can continue, the program can make progress, the operation can be retried or backed off — returns a typed effect (`Result<T, E>`, `Either<E, T>`, `IO<E, A>`, the equivalent). The caller pattern-matches on the failure case and dispatches; the function does not throw.

The cases the rule covers:

- **Validation** — the input did not meet the rule. The caller fixes the input (or asks the user to). The function returns `ValidationError` (or the typed equivalent).
- **Not-found** — the resource was not there. The caller decides whether to create it, fetch it elsewhere, or report its absence. The function returns `NotFound` (or the typed equivalent).
- **Conflict** — the operation could not proceed because of the resource's state. The caller reads the state and retries or surfaces it. The function returns `Conflict` (or the typed equivalent).
- **Timeout** — the operation took too long. The caller retries with backoff, falls back to a cached value, or surfaces the timeout to the user. The function returns `Timeout` (or the typed equivalent).

The test: if I catch this and continue, do I know what's true? Yes — the program is in a state where the failure was handled and the rest of the operation can proceed. The function should have returned a value.

### Rule 2: Unrecoverable failures throw

A function whose failure mode is unrecoverable — the program cannot make progress, the invariant the function relies on has been violated, the resource the function needed has been exhausted — throws an exception. The exception carries the diagnostic information a programmer or an out-of-band process needs; the caller is not expected to catch it.

The cases the rule covers:

- **Invariant violation** — a precondition the function depends on has been broken. The function cannot proceed without violating the program's invariants. The function throws an `IllegalStateException` (or the equivalent).
- **Exhausted resources** — the memory, the file handles, the threads, the connections the function needed are gone. The function cannot proceed at all, and retrying is the wrong move (the resource is still exhausted). The function throws.
- **Programmer error** — `null` where the type said non-null, an out-of-range index, a malformed input that the type system did not catch. The function throws, because the type system said "this cannot happen" and the type system was wrong, and the bug is the diagnostic.

The test: if I catch this and continue, do I know what's true? No — the program is in a state where the invariant that lets the rest of the program run has been violated. Catching and continuing would be lying. The function should throw.

### Rule 3: HTTP-status-as-effect is `scrumia-ktor`, not here

The Ktor client's `StatusCode`, the `expectSuccess` flag, the response-shape failures, and the request-time exceptions are owned by `scrumia-ktor`. A rule that names `StatusCode` or `expectSuccess` belongs there; this module's recoverable/unrecoverable test is what the ktor module applies to those cases. A reviewer finding a rule about HTTP-status-as-effect in this module names it as misplaced and proposes the move.

### Rule 4: The test is one line; the discipline is the willingness to apply it

"if I catch this and continue, do I know what's true?" is the test. A reviewer asking it of a `try { … } catch (e: Exception) { … }` block — and finding that the catch knows what's true — names the throw as misplaced; the function should have returned a value, and the catch is the evidence. A reviewer asking it of a function returning a `Result<User, Error>` whose `Error` includes a programmer-error kind — naming that kind as something the caller cannot recover from — proposes the move: the programmer-error kind belongs as an exception, not as a value.

### Rule 5: An exception type is named in the signature

A function that throws names the exception types in its signature (`@Throws(NotFoundException::class)`, `throws NotFoundException`, the equivalent). The discipline treats the un-named exception as the same shape as the un-typed failure: the caller cannot know what to catch without reading the body. The exception is named so the caller can know what to catch, what to propagate, and what to handle.

### Rule 6: A function that catches and re-throws is not handling the failure

A `try { … } catch (e: Exception) { throw RuntimeException("wrapped", e) }` block has handled nothing — the original exception is still thrown, and the wrapper adds nothing the caller needs. The discipline refuses the shape on the same ground as the discipline-level "an effect that runs at construction is not a description": the wrapping looks like handling and isn't, and the caller cannot tell the two apart without reading the body.
