# Object expressions vs companion objects vs top-level functions

*Refusal.* A `companion object` whose every member is stateless; an `object` expression
used as a singleton; a private utility function declared inside a class only to reach a
sibling private field; a top-level `fun` that should have been a member because it does
reach private state.

## What is refused

```kotlin
// ❌ the `companion object` has no state, no constant — every member could be top-level
class Order {
    companion object {
        fun create(items: List<Item>): Order = Order(items, Money.ZERO)
        const val MAX_ITEMS = 100
    }
}

// ❌ an `object` expression used as a singleton — it is one, but only inside the enclosing scope
fun runOnce() {
    val counter = object {
        var n = 0
    }
    counter.n++
    // next call gets a new counter — not a singleton, an anonymous class on each call
}

// ❌ a top-level function that exists to reach a private field of another class
class OrderRepository {
    private val cache = mutableMapOf<OrderId, Order>()

    // this is a private member; declaring it top-level breaks the encapsulation
    fun Order.id() = cache.keys.firstOrNull { it == this.id }
}
```

The first case compiles today and is the failure mode this rule names. `companion
object` is for state shared across instances, or for a factory that does work the
caller should not see. When the only members are stateless helpers and constants,
the `companion object` is ceremony the call site pays for twice — once to find the
factory, once to realise the factory is not stateful — and the next reader pays for
the indirection forever.

The second case is the wrong shape at the wrong level. `object` *expressions* are
anonymous singletons within the enclosing scope. The counter above is not a singleton
— it is an instance of an anonymous class that exists only inside `runOnce`, and
every call creates a new one. The Kotlin language reference is explicit about this:
an `object` *expression* is local to its declaration; an `object` *declaration* is a
singleton.

The third case is the same defect from the other side. A function declared at the top
level of a file is reachable from anywhere in the package; declaring it inside a class
is not the only reason to scope it. The shape "this function exists only to reach a
sibling private field" is the shape that *should* be a private member — anything else
leaks the abstraction.

## What is written instead

**Top-level functions when no state is shared.** From the [Kotlin coding
conventions](https://kotlinlang.org/docs/coding-conventions.html) and from the
[functions reference](https://kotlinlang.org/docs/functions.html):

```kotlin
// ✅ the factory is a top-level function; the constant is a top-level `const val`
const val MAX_ITEMS = 100

fun createOrder(items: List<Item>): Order =
    require(items.size <= MAX_ITEMS) { "Order too large" }
        .let { Order(items, Money.ZERO) }
```

The call site reads `createOrder(items)`, not `Order.Companion.createOrder(items)`. The
companion-object ceremony is gone; the contract is one line; the next reader has
nothing to learn about a `Companion` to make sense of the call.

**`companion object` only when state or a stateful factory belongs on the class.**
From the [object expressions and declarations reference](https://kotlinlang.org/docs/object-declarations.html):

```kotlin
// ✅ the companion holds state the class owns — a default registry, an instance counter
class ConnectionPool private constructor(private val config: Config) {
    companion object {
        private val instances = mutableListOf<ConnectionPool>()

        fun create(config: Config): ConnectionPool {
            require(instances.size < MAX_POOLS) { "pool limit reached" }
            return ConnectionPool(config).also(instances::add)
        }
    }
}

// ✅ the companion holds a factory that needs to be on the class for clarity, not because of state
class Money private constructor(val amountMinor: Long, val currency: Currency) {
    companion object {
        fun of(amountMinor: Long, currency: Currency): Money =
            Money(amountMinor, currency)
    }
}
```

The first case holds state the class owns (`instances`). The second case is a
named-factory idiom that reads naturally as `Money.of(...)` — and the convention
*calls for* a `companion object` so the factory has a name. The state and the
clarity are the reasons; "every member is stateless" is not.

**`object` *declaration* for a true singleton; `object` *expression* for a one-off
SAM or local anonymous class.** From the same reference:

```kotlin
// ✅ object declaration — the singleton lives in its own file
object Json {
    private val mapper = ObjectMapper()
    fun encode(value: Any): String = mapper.writeValueAsString(value)
    fun <T> decode(json: String, type: Class<T>): T = mapper.readValue(json, type)
}

// ✅ object expression — a one-off listener that closes over local state
button.addActionListener(object : ActionListener {
    override fun actionPerformed(e: ActionEvent) {
        show(count)
        count++
    }
})
```

**Private utility functions stay private — declared inside the class that owns the
state they reach.** The third "what is refused" case is its own fix:

```kotlin
// ✅ the utility is a private member of the class that owns the cache
class OrderRepository {
    private val cache = mutableMapOf<OrderId, Order>()

    private fun Order.idInCache(): OrderId? = cache.keys.firstOrNull { it == this }
}
```

## Why

`companion object` is a named slot on the class for state and behaviour that
belong with the class. When the slot is empty — when every member is stateless and
the factory could be a top-level function — the slot is ceremony the call site
pays for. The Kotlin coding conventions call top-level functions the default for
pure functions, and the call site that says so reads better than the one that
walks through `Order.Companion.`.

`object` *expressions* and `object` *declarations* are two different things in the
language, and the difference is what the call site reads. An expression is local and
anonymous; a declaration is global and named. The Kotlin reference says so in the
first paragraph of the section. The wrong choice compiles; it does not name what it
does; the next reader has to look up which one was meant.

A function declared at the top level of a file is reachable from anywhere in the
package. That reach is a property of the language, not a comment the author left
behind. A function that exists only to reach a private field is a private member the
wrong class; declaring it top-level leaks the abstraction, and the next reader has to
discover by reading the implementation that the function is not part of the public
API.

## Sources complémentaires

- Kotlin docs — [Object expressions and declarations](https://kotlinlang.org/docs/object-declarations.html) — `object Foo` vs `object : Interface { ... }`. Version pin: **Kotlin language**.
- Kotlin docs — [Coding conventions / Functions](https://kotlinlang.org/docs/coding-conventions.html) — top-level functions preferred over companion-object statics when no state is shared. Version pin: **Kotlin language**.
- Kotlin docs — [Functions](https://kotlinlang.org/docs/functions.html) — function scope, member functions, extension functions. Version pin: **Kotlin language**.
