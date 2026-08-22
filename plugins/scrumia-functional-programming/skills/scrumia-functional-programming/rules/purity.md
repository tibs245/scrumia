Purity

*Norm.* A function whose result depends only on its arguments, and whose evaluation changes nothing outside its return value. The principle holds with the same wording in every language that supports it; a rule stated in one language's terms belongs to that language's module, not here.

This rule carries a `Verified in:` footer naming the two languages the contributor verified it against. The footer is meta-information about provenance, not the rule itself — and the CI gate (`bin/scrumia-functional-programming-check-vocabulary`) skips it on purpose.

## What is asked of a function

Two conditions, both of them:

1. The result depends only on the arguments the signature names. The same arguments produce the same result, every time, on every machine, in any order.
2. The evaluation changes nothing outside the function's own return value. No state outside the function reads differently after the call than before it.

A function that satisfies both is pure. A function that fails either is impure; the question is what the impure boundary looks like.

## What the impure boundary looks like

A program that never reads the world, never writes to it, never waits on it — never does anything useful. Impurity is the program's interface to the world, and the rule is that the interface lives in one place the reader can find.

The boundary is whatever the program's architecture calls the place where impurity must live: an I/O layer, an adapter, a handler at the edge of the system. Inside that boundary, purity holds; outside it, impurity is named. The discipline is not "no impurity anywhere" — it is "impurity is named where it lives, and every other place is pure by default".

A reader who cannot tell where the boundary is — because the program mixes purity and impurity in the same function, or scatters impure calls across a layer that should be pure — is reading a program whose structure does not name the rule it is enforcing. That is what the rule catches.

## What is written instead

When a function needs an impure operation, the impure operation is the function's argument or its return — not its body. A function that reads the current time takes a clock as an argument; a function that writes to a database takes the writer as an argument; a function that depends on configuration takes the configuration as an argument. The function's body stays pure, and the boundary is named by the signature.

The same function with the impurity inlined is a function whose result depends on something outside its arguments — and a reader who substitutes the call with its return value gets a different program. That is the substitution a referential transparency violation is, and it is what the purity rule catches first.

## Why

The discipline buys three things a program without it cannot have:

- **Local reasoning.** A pure function can be read and tested in isolation; the test substitutes arguments for inputs and asserts on the result, with no setup of global state.
- **Safe substitution.** A pure expression can be replaced by its value anywhere it appears, and the program's behaviour is unchanged. The compiler and the optimiser rely on this; so does every reader who refactors by renaming a binding to its value.
- **Composable parallelism.** A pure function can be run more than once, in any order, on more than one thread, with the same result every time. Impurity in the body is what makes parallel execution unsafe, and removing the impurity is what makes it safe.

The discipline is not free: a program with a strict impure boundary is a program with more signatures, more arguments, more indirection at the edge. The cost is the price of local reasoning, safe substitution, and composable parallelism — and the price is lower than the cost of debugging the program without them.

## Sources complémentaires

- Hughes, J. (1989). *Why Functional Programming Matters.* — the original argument, on local reasoning and composition as the gains purity buys.
- The principle is paradigm-wide; the references below name the same rule in each idiom.
  - Kotlin: [`kotlinlang.org` — Functional programming](https://kotlinlang.org/docs/lambdas.html) — version pin: stable; Kotlin 2.0 docs. Licence: Apache 2.0.
  - JavaScript: [`developer.mozilla.org` — Functional programming](https://developer.mozilla.org/en-US/docs/Glossary/Functional_programming) — version pin: MDN web docs current. Licence: CC BY-SA 4.0.
  - Rust: [`doc.rust-lang.org` — Functional language features](https://doc.rust-lang.org/book/ch13-00-functional-features.html) — version pin: The Rust Programming Language, current edition. Licence: MIT/Apache 2.0.

Verified in: Kotlin, JavaScript, Rust
