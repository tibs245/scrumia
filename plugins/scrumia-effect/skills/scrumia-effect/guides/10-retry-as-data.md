# 10 — Retry as data, not marketing (error semantics)

> *Approach: error semantics — applies regardless of whether the project uses `Result`, `Either`, `IO`/suspend, or effect.website. A failure that may be retried carries `Retry-After`, attempt count, backoff hint; retry composes as a function on the effect, not as a try/catch loop at the call site.*

Retry is data on the failure, not control flow around the call. A failure that may be retried carries the metadata the next attempt needs — when the server says it is OK to try again (`Retry-After`), how many attempts have already happened, what backoff the program should apply — and the program composes retry as a function on the effect, with the metadata read off the failure and the schedule deciding when the next attempt runs.

## Prerequisites

- [01-typed-effects](01-typed-effects.md) — the effect is a description.
- [09-when-to-throw](09-when-to-throw.md) — the failure is a typed effect, not a thrown exception.

## Rules

### Rule 1: The failure carries the retry metadata

A `Retryable` failure carries `Retry-After: Duration` (or the equivalent — a timestamp, a delay, a backoff hint), `attempt: Int` (how many attempts have happened), and the operation that was attempted. The metadata is part of the failure type, not a comment on it, and the failure is a value the program holds.

A `Result<T, Error>` whose `Error` is a sealed hierarchy including `Retryable` (or an equivalent) is the shape: the caller pattern-matches, sees `Retryable(retryAfter, attempt)`, and decides whether to retry, with the metadata read off the value.

### Rule 2: Retry composes as a function on the effect

```kotlin
// Either-style, retry as a function on the effect:
val result = op(input)
    .flatMap { firstResult ->
        when (firstResult) {
            is Retryable -> firstResult.retryWith(op)
            is Success -> Success(firstResult.value)
            is Fatal -> Fatal(firstResult.error)
        }
    }
```

The retry is a function on the effect (`retryWith`), the function reads the metadata off the failure (`Retryable.retryAfter`, `Retryable.attempt`), and the composition produces a new effect that may succeed, fail retryably, or fail fatally. The call site does not loop.

The reference implementation: effect.website's `Effect.retry(schedule)`, where `Schedule<R, E, A>` decides when the next attempt runs based on the failure. The discipline's rule is the same: a schedule (or a `Retryable` value) decides, and the call site does not.

### Rule 3: A try/catch loop retrying at the call site is the failure this rule catches

```kotlin
// ❌ The retry is at the call site — it does not know what it is retrying.
var attempt = 0
var lastError: Throwable? = null
while (attempt < 3) {
    try {
        return op(input)
    } catch (e: Exception) {
        lastError = e
        attempt++
        Thread.sleep(1000L * attempt)
    }
}
throw lastError!!
```

This shape is what the discipline refuses:

- The loop does not know whether the failure is retryable. It catches `Exception` and assumes yes.
- The loop does not know when to retry. It sleeps a fixed backoff that ignores the server's `Retry-After`.
- The loop does not know when to stop. It stops at `attempt < 3`, which is a number chosen by the caller, not a property of the operation.
- The loop does not return a typed effect. It returns the success value or throws, and the caller has no way to know which it got without reading the body's exceptions.

The fix is structural: the operation returns a typed effect (`Result<T, Error>`), the failure carries the metadata, and the retry is a function on the effect.

### Rule 4: `Retry-After` from the server beats the client's guess

A failure carrying `Retry-After: 30s` (HTTP, or its equivalent in other protocols) is a server-asserted hint that the operation may succeed after that delay. The discipline treats the server's hint as authoritative: a program that retries with a fixed backoff ignoring `Retry-After` is the failure mode the rule catches, because the server's hint exists precisely to say "do not retry me on your schedule, retry me on mine."

### Rule 5: A non-retryable failure is not retried

A `Fatal` failure (the program cannot make progress; the invariant is violated; the resource is exhausted) is not retried. The discipline refuses a retry function that retries everything: the failure's type says whether it can be retried, and the retry function reads the type. A `Retryable` is retried; a `Fatal` is not; a `Success` is returned.

### Rule 6: Retry metadata is logged, not lost

A retry that happens silently is a retry the next reader cannot diagnose. The discipline requires the metadata to be visible: `Retryable(retryAfter=30s, attempt=1, op="fetchUser")` carries what the next attempt needs and what the log needs. A retry function that logs only "retried" without the metadata has discarded what the discipline requires to be held.

## Worked example

A function that fetches a user, may fail retryably on 429 (rate-limited) or 503 (service unavailable), and may fail fatally on 404 (not-found) or any other 4xx:

```kotlin
sealed interface FetchUserError {
    data class Retryable(
        val retryAfter: Duration,
        val attempt: Int,
        val op: String
    ) : FetchUserError
    data class Fatal(val statusCode: Int, val message: String) : FetchUserError
}

fun fetchUser(id: UserId): Result<User, FetchUserError> = …

// Retry composed as a function on the effect.
fun fetchUserWithRetry(id: UserId, maxAttempts: Int = 3): Result<User, FetchUserError> {
    fun go(attempt: Int): Result<User, FetchUserError> =
        fetchUser(id).flatMap { result ->
            when (result) {
                is FetchUserError.Retryable ->
                    if (attempt >= maxAttempts) Result.failure(result)
                    else go(attempt + 1)  // in practice, with delay from result.retryAfter
                is FetchUserError.Fatal -> Result.failure(result)
            }
        }
    return go(1)
}
```

The retry reads the metadata (`result.retryAfter`, the attempt count), decides whether to retry based on the failure's type (`Retryable` vs `Fatal`), and stops at the configured `maxAttempts` — which is a property of the caller, not a property of the operation. The call site does not loop, does not catch exceptions, does not guess a backoff. The failure carries what the next attempt needs.
