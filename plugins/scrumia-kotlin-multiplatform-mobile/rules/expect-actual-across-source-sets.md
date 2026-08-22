# expect-actual-across-source-sets

*Norm.* An `expect` declaration lives in `commonMain`; each `actual` lives in the platform source set that can resolve it. The contract is one source of truth, the implementations are by target.

## What is required

A multiplatform declaration — a function, a property, a class, a typealias — is introduced once, in `commonMain`, with the `expect` keyword. Each `actual` declaration that resolves it lives in the platform source set that compiles for the target it answers.

```kotlin
// commonMain
expect fun platformName(): String

// androidMain
actual fun platformName(): String = "Android"

// iosMain
actual fun platformName(): String = "iOS"

// jvmMain (when a JVM target is configured)
actual fun platformName(): String = "JVM"
```

Each `actual` carries the same fully-qualified signature as the `expect`, modulo the body. An `actual` is not free to narrow the type — the compiler enforces it. An `actual` is not free to move the contract's source-of-truth into a platform source set, because no other source set sees it.

## Why

The contract is the thing every target compiles against. A declaration moved out of `commonMain` is a declaration that two targets can disagree about, silently, because neither has the other's view. The Kotlin documentation is explicit:

> "The `expect` keyword marks a declaration as *expected*. Expected declarations are the API of a module, but not its implementation. Expected declarations can have implementations only in actual declarations, which are marked with the `actual` keyword. All actual declarations that implement an expected declaration must be placed in the same package and marked with the `actual` keyword."

`commonMain` is the source set every target inherits from. An `expect` written anywhere else does not compile for targets that do not see it; an `actual` written in `commonMain` does not compile at all, because there is no other source set for it to resolve. The shape the compiler accepts and the shape the contract needs are the same shape.

## What is refused

- An `expect` declared in `androidMain`, `iosMain`, or any other non-`commonMain` source set — the contract no longer reaches the targets that need it.
- An `actual` declared in `commonMain` — the compiler refuses it, and any "actual" written in the same source set as its `expect` is a copy, not an implementation.
- A signature mismatch between `expect` and `actual` — the compiler rejects it; a near-match that compiles against one target and not another is the regression this rule exists to catch at the type level rather than at runtime.

## Sources complémentaires

- Kotlin — [Expected and actual declarations](https://kotlinlang.org/docs/multiplatform-expect-actual.html) — the `expect`/`actual` contract, the rule that `expect` lives in common code, and that `actual` matches the expected signature exactly.
- Kotlin — [Multiplatform project structure](https://kotlinlang.org/docs/multiplatform-discover-project.html) — the source-set hierarchy `commonMain` → `androidMain`/`iosMain`/`jvmMain`, and the rule that each platform implementation lives in its own source set.