Referential transparency

*Norm.* An expression is replaceable by its value without changing the program's behaviour. Any expression that fails this substitution is the leak to find. The principle holds with the same wording in every language that supports it; a rule stated in one language's terms belongs to that language's module, not here.

This rule carries a `Verified in:` footer naming the two languages the contributor verified it against. The footer is meta-information about provenance, not the rule itself — and the CI gate (`bin/scrumia-functional-programming-check-vocabulary`) skips it on purpose.

## What is asked of an expression

One condition: the expression's value, computed once and substituted for the expression wherever it appears, produces a program whose behaviour is identical to the program that did not substitute.

An expression that satisfies this is referentially transparent. An expression that fails it is referentially opaque, and opacity is the property referential transparency forbids.

## What opacity looks like

An expression is opaque when its value depends on something its syntactic form does not name. The most common shapes are:

- **An expression that reads a value that changes.** The expression's value depends on the state at the moment of evaluation, and substituting the value for the expression freezes that state into the program's text.
- **An expression whose evaluation changes a value.** The expression's evaluation is itself a side effect on the world, and substituting the value removes the effect.
- **An expression that depends on a non-deterministic source.** The expression's value depends on a source whose next value is not determined by the expression's arguments — a stream, a clock, a random source, the network.

The substitution `expr = value` is the test; the substitution reveals the leak because the program's behaviour changes when the expression is replaced.

## What is written instead

An expression that is referentially transparent can be named by its value. A function call whose result is referentially transparent can be replaced by the result; a binding can be replaced by its right-hand side; an expression whose value is computed once can be inlined at every call site without changing the program's behaviour.

A reader who cannot make the substitution is reading an expression whose value depends on something outside the expression. The substitution is the test a referentially opaque expression fails first, and the failure is the property to look for.

The discipline is not "every expression is a literal" — it is "every expression's value is determined by what the expression names, and the substitution is the proof". A program where every expression is referentially transparent is a program the optimiser can rewrite freely; a program with one opaque expression is a program the optimiser must leave alone.

## Why

The discipline buys three things:

- **Optimisation.** A referentially transparent expression can be moved, duplicated, cached, or inlined by the optimiser without changing the program's behaviour. An opaque expression cannot be moved at all, because moving it changes the order of side effects.
- **Reasoning.** A referentially transparent expression can be reasoned about by substitution: a reader can replace it with its value, simplify, and arrive at a program with the same behaviour. An opaque expression cannot be reasoned about by substitution, because the substitution changes the behaviour.
- **Testing.** A referentially transparent expression can be tested in isolation: the test substitutes arguments and asserts on the result. An opaque expression cannot be tested without setting up the world the expression depends on, and the test's setup is the test's largest source of bugs.

## Sources complémentaires

- The principle is paradigm-wide; the references below name the same rule in each idiom.
  - Kotlin: [`kotlinlang.org` — Pure functions](https://kotlinlang.org/docs/lambdas.html#pure-functions) — version pin: stable; Kotlin 2.0 docs. Licence: Apache 2.0.
  - JavaScript: [`developer.mozilla.org` — Pure functions](https://developer.mozilla.org/en-US/docs/Glossary/Functional_programming) — version pin: MDN web docs current. Licence: CC BY-SA 4.0.
  - Rust: [`doc.rust-lang.org` — Functional language features: Closures](https://doc.rust-lang.org/book/ch13-01-closures.html) — version pin: The Rust Programming Language, current edition. Licence: MIT/Apache 2.0.
  - F#: [`learn.microsoft.com` — Pure Functions](https://learn.microsoft.com/en-us/dotnet/fsharp/tutorials/functional-programming) — version pin: F# docs current. Licence: MIT.

Verified in: F#, Rust
