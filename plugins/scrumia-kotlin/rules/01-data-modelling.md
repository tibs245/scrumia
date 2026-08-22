# Naming, scope functions, extension functions, `val` vs `var`

*Refusal.* A `var` where `val` carries the invariant, a scope function (`let`, `run`,
`with`, `apply`, `also`) chosen by habit rather than by what the call site reads, or an
extension function declared where a private member would have done the same job.

## What is refused

```kotlin
// ❌ the variable is reassigned nowhere — `val` states the invariant
var items: List<Item> = emptyList()
items = items + fetched     // the only assignment; the rest is read

// ❌ `apply` chosen by reflex — `also` reads better when the receiver is not mutated
val name = config.apply { name = it.displayName }
```

The first case compiles today and is the failure mode this rule names. The variable
never moves after its single assignment; the `var` is a permission Kotlin asks the
reader to assume, and the assumption is wrong. Refactor to `val`: the function returns
the new list, and the reader no longer has to track whether `items` may have moved
since the line they were on.

The second case is the same defect with a different symptom. `apply` returns the
receiver, `also` returns the lambda; when the assignment uses the lambda's value and
the receiver is not mutated, `also` reads as "and then compute this", and `apply`
reads as "configure this" — a configuration that does not happen is a false friend.

## What is written instead

`val` by default. A `var` is justified only when the *behaviour* is reassignment — a
counter, a builder, an accumulator that exists across iterations or events. From
[Kotlin's coding conventions](https://kotlinlang.org/docs/coding-conventions.html):

```kotlin
// ✅ reassignment is the behaviour — `var` states it
var attempts = 0
while (attempts < MAX_RETRIES && !succeeded) {
    attempts++
    succeeded = tryOnce()
}

// ✅ the variable never moves — `val` carries the invariant
val items: List<Item> = emptyList() + fetched
```

**Scope functions chosen by what the call site reads.** From the same conventions and
from the [scope functions reference](https://kotlinlang.org/docs/scope-functions.html):

| Reads as | Use |
|---|---|
| "configure this object" — mutates the receiver, returns it | `apply` |
| "and also do this" — takes the receiver as `it`, returns the lambda | `also` |
| "map this value to another" — takes the lambda's parameter, returns it | `let` |
| "execute this block on this receiver" — returns the lambda, often `Unit` | `run` |
| "call a sequence of methods on this receiver" — receiver as `this`, returns the lambda | `with` |

The wrong choice compiles; it does not name what it does. `apply { name = ... }` for a
name that does not configure the receiver is the false friend above.

**Extension functions for a reader benefit, not for namespace pollution.** An
extension function that makes a call site read clearly is welcome; one that exists
only to reach a private field is a private member the wrong class. From the [extension
functions reference](https://kotlinlang.org/docs/extensions.html#extension-functions):

```kotlin
// ✅ the extension reads at the call site; no private field is touched
fun List<Item>.totalCost(): Money = sumOf { it.price }

// ❌ the extension exists only to mutate a sibling private field
class Order {
    private var cachedTotal: Money = Money.ZERO
    fun List<Item>.recompute() { cachedTotal = sumOf { it.price } }
}
```

The second form compiles and tests pass; it is two classes pretending to be one, and
the next reader pays for the indirection.

## Why

`val` and `var` are not synonyms. `var` is a permission the type system grants; the
reader is being told the variable may change. When it does not, the permission is
wrong information — and the reader cannot tell from the call site whether the wrong
information is wrong, because `var` does not declare *when* it moves. A `val` at the
single-assignment site closes the question on the day the line is written.

Scope functions are five names for the same general shape — pass a value, run a block,
return a result — and the differences are what the call site reads. Picking one by
reflex means the call site reads as the reflex, not as what it does. The wrong scope
function is not a bug today; it is a comprehension cost the next reader pays every
time they reach the line.

Extension functions exist so a function can be called on a receiver whose source the
caller does not own. An extension inside a class that reaches a private field of the
class is the same shape with the wrong motive — and the next reader, asked "what class
does this extension belong to", answers the one it is declared inside, and is wrong.

## Sources complémentaires

- Kotlin docs — [Coding conventions](https://kotlinlang.org/docs/coding-conventions.html) — *Immutable val / var*, *Scope functions*. Version pin: **Kotlin language**.
- Kotlin docs — [Scope functions](https://kotlinlang.org/docs/scope-functions.html) — `let`, `run`, `with`, `apply`, `also`. Version pin: **Kotlin language**.
- Kotlin docs — [Extensions](https://kotlinlang.org/docs/extensions.html#extension-functions) — when an extension reads at the call site, and when it does not. Version pin: **Kotlin language**.
