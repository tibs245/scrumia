Effect discipline

*Norm.* An effect is described as a value the program composes, then executed at the boundary; collapsing description and execution is the over-application this rule catches. The principle holds with the same wording in every language that supports it; a rule stated in one language's terms belongs to that language's module, not here.

This rule carries a `Verified in:` footer naming the two languages the contributor verified it against. The footer is meta-information about provenance, not the rule itself — and the CI gate (`bin/scrumia-functional-programming-check-vocabulary`) skips it on purpose.

## What is asked of an effect

An effect in a program — a read, a write, a wait, a network call, a clock read, a random source — has two moments: the moment it is described, and the moment it is executed. The discipline is that the two moments are separated, and the program composes descriptions before any execution happens.

A language with first-class effects in its type system makes the separation visible: the signature names the effect, the body's type tracks which effects are described, and the runtime is what executes them. A language without first-class effects still has the two moments — every program has a "what would happen" and a "what happens" — and the rule applies to both: collapsing the two is the over-application this rule catches.

## What collapsing looks like

An effect described at the moment it executes:

- A function that calls a database in its body. The database call is the effect; the function's return value depends on the database's response. The effect is described by the call itself, and the program cannot compose the description before execution — the call is the description.
- A function that writes to a log in its body. The log write is the effect; the function's body performs the write at the moment the function is called. The program cannot inspect the description, cannot defer the write, cannot compose the write with other writes before any of them runs.
- A function that waits on a clock in its body. The wait is the effect; the function's body performs the wait at the moment the function is called. The program cannot describe the wait without performing it.

A program whose effects are described at the call site is a program whose effects are entangled with the call graph: a reader who follows the call graph follows the effects, and the effects are what the program is doing at every step.

## What is written instead

An effect described as a value:

- A function whose body returns a description of the database call. The description is a value the program composes; the execution is a function the program calls with the description, at the boundary the program draws.
- A function whose body returns a description of the log write. The description is a value the program composes with other log descriptions; the program executes the composed description at the boundary, in the order the composition determines.
- A function whose body returns a description of the wait. The description is a value the program composes with other wait descriptions; the program executes the composed description at the boundary, in the order the composition determines.

A language without first-class effects can still separate the two moments by returning a closure or a builder that captures the effect's description and defers the execution to a single interpreter at the boundary. The discipline is the same: description is a value the program composes, execution is the program's last step, and the boundary is what the program's architecture names.

The rule is not "no effect type system" — that is a writing choice, not a principle. The rule is "description and execution are separate moments, and the program's structure names the boundary between them".

## Why

The discipline buys three things:

- **Composition.** A description can be composed with other descriptions: two database reads can be sequenced, two log writes can be batched, two waits can be parallelised. An execution is already happening, and the program cannot compose it.
- **Inspection.** A description can be inspected by the program: the program can log it, test it, route it, transform it. An execution is what the program does, and the program cannot inspect what it is doing.
- **Deferral.** A description can be deferred: the program can hold the description, decide later whether to execute it, and pass it to a different interpreter. An execution has happened, and the program cannot undo it.

## Sources complémentaires

- The principle is paradigm-wide; the references below name the same rule in each idiom.
  - Kotlin: [`kotlinlang.org` — Coroutines: Composing suspending functions](https://kotlinlang.org/docs/composing-suspending-functions.html) — version pin: stable; Kotlin 2.0 docs. Licence: Apache 2.0.
  - JavaScript: [`developer.mozilla.org` — Using promises](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Using_promises) — version pin: MDN web docs current. Licence: CC BY-SA 4.0.
  - Rust: [`doc.rust-lang.org` — Fearless Concurrency](https://doc.rust-lang.org/book/ch16-00-concurrency.html) — version pin: The Rust Programming Language, current edition. Licence: MIT/Apache 2.0.
  - Scala: [`docs.scala-lang.org` — Futures](https://docs.scala-lang.org/overviews/core/futures.html) — version pin: Scala 3 docs current. Licence: Apache 2.0.

Verified in: Kotlin, Scala
