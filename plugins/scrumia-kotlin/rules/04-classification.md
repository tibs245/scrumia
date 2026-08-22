# `data class`, `sealed class` / `sealed interface`, `value class`

*Refusal.* A `class` with a single property and no behaviour pretending to be a domain
value; a closed hierarchy written as a `class` with boolean flags or string fields; a
single-property wrapper built as a `class` instead of a `value class` (or, where it is
even simpler, an inline `value class`).

## What is refused

```kotlin
// ❌ a `class` with one property and no behaviour — the equality and toString are about to be hand-written
class EmailAddress(private val value: String) {
    override fun equals(other: Any?) = other is EmailAddress && other.value == value
    override fun hashCode() = value.hashCode()
    override fun toString() = "EmailAddress($value)"
}

// ❌ a closed hierarchy written as a `class` with a discriminator string and a payload field
class Shape {
    var kind: String = ""       // "circle" | "square"
    var radius: Double = 0.0
    var side: Double = 0.0
}

// ❌ a wrapper that is `data class` when the value semantics are about a single underlying value, not a record
data class UserId(val raw: String)              // five fields would be data class; one field is value class
```

The first case compiles today and is the failure mode this rule names. The class
*looks* like a domain value but is not — there is no `copy`, no `componentN`, and the
hand-written `equals`/`hashCode`/`toString` is exactly what `data class` would have
generated. The cost is paid by the next reader, who has to prove to themselves the
hand-written forms agree with `data class`'s.

The second case is the same defect on a closed hierarchy. The kind field is a string,
the radius and side fields coexist on every instance, and the type system cannot tell
which one is set. A `sealed interface` with two data-class implementations tells the
type system, the compiler, and the reader the same thing: this is a closed set of
shapes, each carries its own data, and the `when` is exhaustive without an `else`.

The third case is the wrong shape at the wrong size. `data class` is right when the
type is a record of several fields — five fields with `equals` and `copy` and
`componentN` are exactly the contract. When the type is a single underlying value, the
record is ceremony; `value class` (formerly `inline class`) gives the type safety at
runtime cost near zero.

## What is written instead

**`data class` for value-shaped records.** From the [Kotlin classes reference —
data classes](https://kotlinlang.org/docs/data-classes.html):

```kotlin
// ✅ the record has the equality, the toString, the componentN, and the copy — for free
data class Point(val x: Int, val y: Int)

// ✅ a closed hierarchy that the type system enforces
sealed interface Shape
data class Circle(val radius: Double) : Shape
data class Square(val side: Double) : Shape

fun area(shape: Shape): Double = when (shape) {
    is Circle -> Math.PI * shape.radius * shape.radius
    is Square -> shape.side * shape.side
    // no `else`: the `when` is exhaustive over the sealed hierarchy
}
```

**`value class` for type-safe wrappers around a single underlying value.** From the
[inline classes / value classes reference](https://kotlinlang.org/docs/inline-classes.html):

```kotlin
// ✅ the wrapper has the type safety at zero runtime cost
@JvmInline
value class UserId(val raw: String)

@JvmInline
value class EmailAddress(val value: String)

fun sendInvite(to: UserId, body: EmailAddress) { ... }

val id = UserId("u-42")
sendInvite(id, EmailAddress("hi@example.com"))    // compiles
sendInvite(EmailAddress("hi@example.com"), id)    // does not compile — types catch it
```

The wrapper compiles down to the underlying `String` at the bytecode level. The type
system keeps the names apart at the source level. Both wins, neither cost.

**`sealed class` and `sealed interface` for closed hierarchies.** From the [sealed
classes reference](https://kotlinlang.org/docs/sealed-classes.html):

```kotlin
// ✅ `sealed class` when the hierarchy carries shared state
sealed class Result<out T> {
    data class Success<T>(val value: T) : Result<T>()
    data class Failure(val cause: Throwable) : Result<Nothing>()
    object Loading : Result<Nothing>()
}

// ✅ `sealed interface` when the hierarchy is a pure sum type, no shared state
sealed interface Event
data class Click(val x: Int, val y: Int) : Event
data class KeyPress(val code: Char) : Event
```

`sealed class` and `sealed interface` differ only in what they can extend — a class
can carry shared state and constructor parameters, an interface cannot — and both make
the `when` exhaustive.

## Why

`data class` is the Kotlin standard library saying "this is a record of values, and
the type system will generate the contracts a record owes". Hand-writing those
contracts is the wrong default: the contracts are mechanical, the reader has to prove
the hand-written form agrees with the generated one, and the proof costs every reader
who has to make it. The hand-written form is also the form that rots — adding a field
to the constructor without adding it to `equals` is the silent bug the compiler would
have caught.

A `class` with a string discriminator is the same defect on a closed hierarchy. The
string is data the type system cannot read; the field that is irrelevant to the kind
has to be checked at runtime; the `when` over the discriminator has to carry a default
that should not exist. `sealed interface` makes the discriminator a type, the field
that does not belong is on the implementation that does, and the `when` is exhaustive
because the compiler knows the set is closed.

`value class` is for the case where the type is *one* underlying value, and the
record of fields is ceremony the runtime does not need. The wrapper compiles away to
the underlying value; the type system keeps the names apart. Without `value class`,
the wrapper is a `data class` with one field and the runtime pays for an allocation
on every wrap and unwrap, and the `equals`/`hashCode`/`toString` are not even the
right contracts — the wrapper's identity is the value's identity, and the wrapper
itself has no business existing at runtime.

## Sources complémentaires

- Kotlin docs — [Data classes](https://kotlinlang.org/docs/data-classes.html) — generated `equals`/`hashCode`/`toString`/`componentN`/`copy`. Version pin: **Kotlin language**.
- Kotlin docs — [Sealed classes and interfaces](https://kotlinlang.org/docs/sealed-classes.html) — closed hierarchies and exhaustive `when`. Version pin: **Kotlin language**.
- Kotlin docs — [Inline value classes](https://kotlinlang.org/docs/inline-classes.html) — type-safe wrappers at zero runtime cost. Version pin: **Kotlin language**.
