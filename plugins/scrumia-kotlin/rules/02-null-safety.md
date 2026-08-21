# Null-safety, platform types, and precondition functions

*Refusal.* A `!!` without a stated local proof; a Java-interop platform type (`T!`)
read as a Kotlin type; a precondition function used as the wrong category — `require`
for state, `check` for arguments, `error` for the unconditional branch that should not
be reachable.

## What is refused

```kotlin
// ❌ `!!` papers over a nullable the surrounding code already proved — but the comment says so, not the type
fun describe(name: String?): String =
    "Hello, ${name!!}"                     // the caller passes a non-null name "most of the time"

// ❌ a Java method returning `String!` is read as `String` here
val length: Int = javaRegistry.get("key").length   // get(...) returns String!

// ❌ `require` on a state condition; `check` on an argument condition
class Order {
    fun pay(amount: Money) {
        require(isOpen) { "Order must be open" }     // this is a state precondition, not an argument precondition
        check(amount > Money.ZERO) { "amount must be positive" }  // this is an argument precondition, not a state one
    }
}
```

The first case compiles today and is the failure mode this rule names. `!!` says "I
know this is not null" — but the surrounding function did not prove it, the comment
did, and the comment rots the day the caller changes. The exception throws `NullPointerException`
without a stack trace that names the contract that was assumed.

The second case is the same defect through Java interop. The Kotlin language reference
calls the type `String!` — a "platform type" that the compiler permits to be used as
either `String` or `String?`, with no check at the boundary. The Kotlin docs say so
explicitly: the choice is the caller's, and the choice is wrong information when the
caller treats `String!` as `String`.

The third case is two mistakes in one block. `require` checks an argument
precondition; `check` checks a state precondition. The two throw the same exception
type but name different contracts, and a stack trace pointing at the wrong one sends the
reader to the wrong layer.

## What is written instead

**`?` on every type that can be absent; `!!` only with a stated local proof.** From
[Kotlin's null-safety reference](https://kotlinlang.org/docs/null-safety.html):

```kotlin
// ✅ the type states the contract; the function handles the absence
fun describe(name: String?): String =
    "Hello, ${name ?: "stranger"}"

// ✅ `!!` carries the proof in the same expression
val length = name ?: return@describe 0
val upper = name!!.uppercase()        // preceded by the early-return above; the proof is the line before
```

The early-return is the proof. The `!!` is the act of consumption. Both are on the
page; the reader can follow them; a refactor that breaks the early return breaks the
proof and the compile catches it.

**Platform types handled at the boundary.** From the [Java interop — Nullable
annotations reference](https://kotlinlang.org/docs/java-interop.html#null-safety-and-platform-types):

```kotlin
// ✅ the boundary names the type; the rest of the codebase uses `String?`
fun lookupName(key: String): String? =
    javaRegistry.get(key)               // String! — narrowed to String? at the boundary

// ❌ the platform type leaks past the boundary
fun lookupName(key: String): String =
    javaRegistry.get(key)               // String! — narrowed to String, no check at the seam
```

When the upstream Java code carries `@NotNull` / `@Nullable` annotations, Kotlin
respects them and the narrowing is automatic. When it does not, the boundary picks a
side: the function returns `String?`, the caller handles the absence, and the platform
type stops at the function.

**`require` for arguments, `check` for state, `error` for the unreachable branch.**
From the [preconditions reference](https://kotlinlang.org/docs/exceptions.html#preconditions):

| Function | Use when | Throws |
|---|---|---|
| `require(value) { "..." }` | the *caller* has broken the contract on the value passed in | `IllegalArgumentException` |
| `check(value) { "..." }` | the *internal state* is wrong, the caller did nothing wrong | `IllegalStateException` |
| `error("...")` or `throw IllegalStateException("...")` | this branch is unreachable — a sealed `when` over an enum that has no `else` | `IllegalStateException` |

The three are not interchangeable. A `require` on internal state sends the reader to
the wrong layer; a `check` on an argument sends them there too. `error` is for the
branch a `sealed when` proves unreachable — it is the assertion the compiler cannot
state, and it is the only one of the three that has no recovery path.

## Why

`?` is the type system telling the reader the value may be absent. `!!` is the reader
overriding it. The override is correct on the day it is written — the line above
proves the value is non-null — and wrong on the day the proof moves. A comment that
names the proof survives a rename and dies on a refactor; the early-return that *is*
the proof survives both, because the compiler is following it.

Platform types are Kotlin's compromise with the Java ecosystem, and the compromise is
explicit: the Kotlin docs say the choice is the caller's. The choice that "just works"
is the one that turns the boundary into a lie — every call downstream trusts the type
the boundary did not enforce, and the `NullPointerException` lands in the function
that called the function that called the boundary, with no evidence at the seam.

`require` and `check` throw the same exception, and the exception is the wrong lens
to read them through. A stack trace names the function and the message; the message
names the contract; the contract is what `require` or `check` *says*. Reading
"amount must be positive" against a state precondition sends the operator to the
state, not to the call, and the bug stays.

## Sources complémentaires

- Kotlin docs — [Null-safety](https://kotlinlang.org/docs/null-safety.html) — `?`, `!!`, safe call, elvis. Version pin: **Kotlin language**.
- Kotlin docs — [Java interop / Null-safety and platform types](https://kotlinlang.org/docs/java-interop.html#null-safety-and-platform-types) — the `T!` notation and the boundary's responsibility. Version pin: **Kotlin language**.
- Kotlin docs — [Exceptions / Preconditions](https://kotlinlang.org/docs/exceptions.html#preconditions) — `require`, `check`, `error`. Version pin: **Kotlin language**.
