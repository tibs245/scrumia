# D-02: Retry composes as a function on the effect, not as a try/catch loop at the call site

**Status**: Adopted
**Date**: 2026-08-22
**Impacts**: [guides/10-retry-as-data.md](../guides/10-retry-as-data.md), [guides/08-effect-website.md](../guides/08-effect-website.md), [guides/07-io-suspend.md](../guides/07-io-suspend.md)

## Context

Retry is one of the recurring patterns that almost every effectful system has to implement, and almost every implementation gets wrong: a try/catch loop at the call site, with a fixed backoff, a fixed attempt count, and no knowledge of whether the failure is even retryable. The cost is that the retry policy is scattered across every call site that retries, the failure does not carry the metadata the next attempt needs, and the program has no way to know — from the return type alone — whether the call succeeded, retried, or failed.

The decision this module has to make is whether retry is **control flow** (a `while` loop, an `if` retry, a try/catch with a backoff) or **data on the effect** (the failure carries `Retry-After`, attempt count, backoff hint; the retry is a function on the effect; the call site does not loop). The control-flow form has the cost named above; the data form has the cost that the failure type must include the metadata, and the retry function must be written.

## Arguments For (retry as data, composed as a function on the effect)

- **The failure's metadata (`Retry-After`, attempt count, backoff hint) is part of what the next attempt needs; carrying it on the failure is what lets the retry function use it.** A server returning `Retry-After: 30s` is telling the client when to try again, and a retry loop ignoring the header is guessing a backoff the server already said is wrong. The discipline treats the server's hint as authoritative — and authoritative means read off the failure, not guessed at the call site.
- **The retry policy lives in one place.** A retry function (`op.retryWith { failure -> … }`, `Effect.retry(schedule)`, the equivalent in each approach) is the only place the program decides when to retry. Changing the policy — switching from fixed backoff to exponential, adding jitter, capping attempts — is one edit, not N edits across N call sites.
- **The call site does not loop, does not catch exceptions, does not guess a backoff, and does not lose the typed effect.** The function returns the same typed effect it would have returned without retry, and the caller observes the failure the same way. A reviewer finding a try/catch loop at the call site knows immediately: the typed effect has been discarded.
- **The retry composes.** Two retried operations compose as descriptions: `opA.retryWith(schedule).flatMap { a -> opB(a).retryWith(otherSchedule) }`. The composition is a description of the combined retry; the run is at the seam; the schedule is part of the description.

## Arguments Against (control flow at the call site)

- **The control-flow form is shorter to write for a single call site.** `for (i in 0 until 3) { try { return op() } catch (e: Exception) { Thread.sleep(1000) } }` is one line of business logic; the data form is a `Retryable` failure type, a retry function, and a schedule. The cost is real for a single call site, and the mitigation is that the data form is one-time — the retry function is written once and reused across every call site that retries.
- **The data form requires the failure to be a typed effect.** A function that throws on failure cannot carry the metadata on the failure, because the failure is an exception, not a value. The mitigation is [09-when-to-throw](../guides/09-when-to-throw.md)'s rule: a recoverable failure returns a value. The retry-as-data rule assumes the recoverable-failure rule is in force, and a program where the failure is an exception has lost both.
- **The data form does not compose with an exception-based retry loop.** A program that retries on exception cannot read `Retry-After` off the exception's headers without a per-exception parser, and the schedule is a guess. The discipline refuses the loop on the same ground as the typed-effect rule: the type system cannot see what the loop is doing, and the reviewer cannot either.

## Verdict

**Adopted.** Retry composes as a function on the effect, with the failure carrying the metadata the next attempt needs. The call site does not loop. The reference implementation is effect.website's `Effect.retry(schedule)`, where `Schedule<R, E, A>` is the typed decision; the discipline applies the same shape to `Result`, `Either`, and `IO`/suspend, with `Retryable(retryAfter, attempt, op)` as the metadata carrier.

The data form is the one place the retry policy lives; the call site is a function call. A reviewer finding a try/catch loop with a backoff at the call site names it as the failure this rule catches, and the fix is to type the failure, carry the metadata, and compose the retry as a function.
