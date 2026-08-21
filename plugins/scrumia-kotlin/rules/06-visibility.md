# Visibility modifiers

*Refusal.* `public` on a member meant to stay inside the module; `internal` treated as
"package-private" (it is not — it is the module boundary); a member promoted to `public`
to silence a test that crossed the wrong boundary. Each one is the wrong default at the
wrong granularity, and the wrong default is the one that compiles today and reads
cleanly tomorrow.

## What is refused

```kotlin
// ❌ `public` (the default) on a member meant to stay inside the module
class OrderRepository internal constructor(...) {
    val cache: MutableMap<OrderId, Order> = mutableMapOf()   // public — read-only outside the module
    fun resetCache() { cache.clear() }                       // public — mutates from anywhere
}

// ❌ `internal` treated as "package-private"
package com.example.orders
internal class OrderMapper { ... }        // "only this package" — wrong; internal is the module, not the package

// ❌ a member promoted to `public` to silence a test that crossed the boundary
class OrderService {
    public fun currentState(): OrderState = ...   // public so the test can read it from another module
}
```

The first case compiles today and is the failure mode this rule names. `public` is the
default visibility, and the default is the one the type system does not state
explicitly. A field the next consumer is meant to read but not mutate is not the
contract `public` carries; the consumer reads, then mutates through the function, and
the invariant the cache was meant to enforce is silently broken. The Kotlin visibility
reference is explicit: visibility is a property of the *module*, not the *type*, and
the wrong default at the wrong boundary is the one that compiles today and rots
tomorrow.

The second case is the wrong mental model. The Kotlin visibility reference says
`internal` means "visible inside the same module" — a module being the unit of
compilation, not the Java package. A consumer thinking `internal` is package-private
will write a Kotlin file in the same package and expect the visibility to hold across
modules; it does not. The Kotlin docs say so explicitly, and the wrong mental model is
the wrong default at the wrong scale.

The third case is the wrong fix at the wrong seam. The test crossed the boundary; the
right fix is to move the test, or to expose a narrower surface the test can hold.
Promoting a member to `public` to make the test pass widens the surface a consumer
sees; the next consumer relies on the wider surface; the next change has to keep the
wider surface working. The test was right that the contract is observable; the fix
was wrong about *who* should observe it.

## What is written instead

**`private` by default; `internal` as the module boundary; `public` only on a surface
meant to cross a published boundary.** From the [Kotlin visibility modifiers
reference](https://kotlinlang.org/docs/visibility-modifiers.html):

```kotlin
// ✅ the cache is private; the surface that crosses the module is intentional
class OrderRepository internal constructor(
    private val config: RepositoryConfig,
) {
    private val cache: MutableMap<OrderId, Order> = mutableMapOf()

    internal fun snapshot(): Map<OrderId, Order> = cache.toMap()   // module sees a read-only view

    fun findById(id: OrderId): Order? = cache[id]
}

// ✅ `internal` is the module, not the package
// file: src/com/example/orders/OrderMapper.kt
internal class OrderMapper {
    fun toDomain(record: OrderRecord): Order = ...
}
// visible inside the Gradle module that compiles this file; not visible to other Gradle modules in the same package
```

**Tests stay inside the boundary they test.** The third "what is refused" case is its
own fix:

```kotlin
// ✅ the test observes through the published surface, not through a member promoted for the test
class OrderServiceTest {
    @Test
    fun `given an order, when service is queried, then state matches`() {
        val service = OrderService(...)
        assertEquals(OrderState.New, service.state)   // state is the published surface
    }
}
```

A test that needs to read a private member is a finding on the design, not on the
test: either the design needs to expose the state through a contract the test can
hold, or the test needs to live in the same module and observe through `internal`.

## Why

`public` is the *absence* of a visibility annotation. The Kotlin language reference
states this in the first paragraph of the visibility section: a declaration without a
modifier is public. The absence of a modifier is the absence of a stated boundary;
the reader has to assume the boundary is "anywhere the type is reachable", and the
assumption is wrong the day the type is reachable somewhere the author did not
intend.

`internal` is the Kotlin boundary. It is named for the unit the compiler sees —
the Gradle module, the Maven module, the compilation unit — and it is precisely that
unit because the language was designed for the case where a multi-module project
needs a finer-grained boundary than `public` without the ceremony of `private` at
every site. The Kotlin docs say so explicitly. A reader who thinks `internal` is
package-private has imported a Java idiom and missed the Kotlin-specific boundary the
language added.

`public` is for surfaces meant to cross a published boundary — a library API, a
module's outward-facing types, a function declared to be the entry point a consumer
calls. It is not for surfaces meant to stay inside the module, and it is not for
fields the consumer should read but not mutate. A `val` declared `public` is a field
the consumer reads and a function the consumer calls — the same declaration carries
both, and the consumer has no signal from the type which contract they have.

The fix for a test that crossed the wrong boundary is to expose the surface the test
needs through a contract, not to promote the field the test reaches. Promoting the
field makes the test pass; it also makes every consumer see the field. The two
outcomes cannot be un-promoted separately: widening the surface to fix the test
widens the surface for everyone.

## Sources complémentaires

- Kotlin docs — [Visibility modifiers](https://kotlinlang.org/docs/visibility-modifiers.html) — `private`, `protected`, `internal`, `public`, the module boundary. Version pin: **Kotlin language**.
- Kotlin docs — [Coding conventions / Visibility of declarations](https://kotlinlang.org/docs/coding-conventions.html) — the recommended defaults. Version pin: **Kotlin language**.
