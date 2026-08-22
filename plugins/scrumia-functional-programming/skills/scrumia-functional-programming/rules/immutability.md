Immutability by default

*Refusal.* A value that mutates when an equivalent immutable value would have written less, and the line where mutation becomes acceptable. The principle holds with the same wording in every language that supports it; a rule stated in one language's terms belongs to that language's module, not here.

This rule carries a `Verified in:` footer naming the two languages the contributor verified it against. The footer is meta-information about provenance, not the rule itself — and the CI gate (`bin/scrumia-functional-programming-check-vocabulary`) skips it on purpose.

## What is refused

A value whose type permits in-place mutation, when the program's behaviour would be identical with an immutable value that produces a new value for each update. Mutation is the over-application this rule catches, not the virtue.

The test is local: would the value's interface be the same — same read, same iteration, same query — if every update returned a new value rather than mutating in place? If yes, mutation is the over-application; the immutable value is what the program should have used.

## What mutation is acceptable for

Three places, and only three, where mutation earns its keep:

1. **Performance-critical inner loops** where allocation cost dominates the runtime. The mutation is local, the loop body is the only reader, and the immutable alternative has been measured to be too slow.
2. **I/O buffers** that the operating system or the language runtime hands the program as a mutable region. The mutation is forced by the interface the program is given; the alternative is to copy, and the copy is the cost.
3. **Concurrent shared state** where a coordination protocol — a lock, a queue, an actor — mediates the access and the protocol is the program's contract. The mutation is the protocol's hand-off; the alternative is a queue with the same semantics and more allocation.

Outside these three, mutation is a default the program took because it was easier, not because it was right. The rule is to draw the line before the code is, and to name the place where mutation crosses it.

## What is written instead

A value that the program updates returns a new value. The interface is read-only; the update is a function from the old value to the new value, and every reader sees the value at the moment of the read.

A collection the program iterates without mutating is a collection whose interface does not include an update operation; the update is a new collection, and the old one is what the iteration sees.

A counter the program increments is a function from the current count to the next count, and the next count is the function's return. The function is pure, the count is referentially transparent, and the iteration over the counter's history is a list of the values the function returned.

The discipline is not "no mutation anywhere" — it is "mutation is named where it is, and every other place is immutable by default". A program whose mutation is named is a program whose readers can find the mutation; a program whose mutation is the default is a program whose readers cannot reason about it without running it.

## Why

The discipline buys three things:

- **Safe sharing.** An immutable value can be shared between threads, between callbacks, between iterations of a loop, without coordination. A mutable value cannot be shared without the protocol that mediates the access, and the protocol is what the value's readers must know.
- **Safe substitution.** An immutable value can be substituted for its definition without changing the program's behaviour; a mutable value cannot be substituted, because the substitution would freeze the mutation at the substitution site.
- **History as a value.** An immutable value's history is the sequence of values the program produced. A mutable value's history is the sequence of states the program went through, and the sequence is harder to reason about than the value.

## Sources complémentaires

- The principle is paradigm-wide; the references below name the same rule in each idiom.
  - Kotlin: [`kotlinlang.org` — Immutability](https://kotlinlang.org/docs/data-classes.html) — version pin: stable; Kotlin 2.0 docs. Licence: Apache 2.0.
  - JavaScript: [`developer.mozilla.org` — Immutable data](https://developer.mozilla.org/en-US/docs/Glossary/Immutable) — version pin: MDN web docs current. Licence: CC BY-SA 4.0.
  - Rust: [`doc.rust-lang.org` — Variables and Mutability](https://doc.rust-lang.org/book/ch03-01-variables-and-mutability.html) — version pin: The Rust Programming Language, current edition. Licence: MIT/Apache 2.0.

Verified in: Kotlin, JavaScript, Rust
