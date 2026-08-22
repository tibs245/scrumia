Composition over inheritance

*Refusal.* Inheritance is not the default reuse mechanism; typeclasses, extension functions, and function composition are the smaller, more local choice when they fit. The principle holds with the same wording in every language that supports it; a rule stated in one language's terms belongs to that language's module, not here.

This rule carries a `Verified in:` footer naming the two languages the contributor verified it against. The footer is meta-information about provenance, not the rule itself — and the CI gate (`bin/scrumia-functional-programming-check-vocabulary`) skips it on purpose.

## What is refused

A class hierarchy chosen as the primary reuse mechanism when composition would have read as the smaller, more local choice. The test is local: would the program's reuse be the same — same coverage, same extension points, same test surface — if the inheritance relation were replaced by a composition of behaviours the consumer names? If yes, inheritance is the over-application; the composition is what the program should have used.

The rule is not "never inherit" — it is "do not reach for inheritance first". Inheritance has a place: the place where the program's domain genuinely has an "is a" relation, where the substitution principle holds for every operation the type exposes, and where the type's hierarchy is the program's vocabulary for the domain. Outside that place, inheritance is a default the program took because it was the first one offered, not because it was right.

## What composition looks like

Three shapes, and the language chooses which one fits the program's needs:

1. **Typeclasses** (or their language-specific equivalents): a behaviour the type satisfies, declared as a separate thing from the type's own definition. Two unrelated types can satisfy the same behaviour; the behaviour is named by its witness, not by the type's place in a hierarchy.
2. **Extension functions / methods**: a behaviour added to a type without the type's own definition changing. The extension is local to where it is named; the type's author does not need to know the extension exists.
3. **Function composition**: a behaviour built by composing smaller behaviours, each of which does one thing. The composition is read as the chain of behaviours; the type that hosts the chain is the type the composition returns, not a hierarchy the chain descends from.

The three shapes are not exhaustive — they are the shapes the language chooses from, and the language-specific module names the choice.

## What is written instead

A behaviour the program reuses is a behaviour the consumer names. The behaviour's interface is what the consumer depends on; the behaviour's implementation is what the consumer does not need to know. Two types with the same behaviour can be substituted at the interface, and the substitution is local to the consumer's code.

A hierarchy the program draws is a hierarchy whose "is a" relation holds for every operation the type exposes. The relation is what the domain says, not what the program's reuse demands; the reuse reads as the substitution the hierarchy supports, and the substitution is what every consumer of the hierarchy can rely on.

A program whose reuse is composition is a program whose dependencies are local: every consumer names the behaviours it uses, every behaviour is satisfied by the types the consumer depends on, and the hierarchy the types might descend from is irrelevant to the consumer's reasoning.

## Why

The discipline buys three things:

- **Local extension.** A composition can be extended locally — by adding a new behaviour, by adding a new type that satisfies an existing behaviour, by composing existing behaviours in a new order. A hierarchy can be extended by adding a new subclass, and the new subclass is a new thing the hierarchy's consumers must reason about.
- **Local substitution.** A composition can be substituted locally — by replacing one behaviour with another that satisfies the same interface, by replacing one type with another that satisfies the same behaviour, by composing the substitution into the consumer's code without the hierarchy knowing. A hierarchy's substitution is a subclass, and the subclass is a new thing the hierarchy exposes.
- **Local reasoning.** A composition can be read locally: the reader sees the behaviours the consumer names, and the behaviours are what the consumer depends on. A hierarchy must be read across its ancestry: the reader sees a subclass, and the reader must reason about every operation the subclass inherits.

## Sources complémentaires

- The principle is paradigm-wide; the references below name the same rule in each idiom.
  - Kotlin: [`kotlinlang.org` — Higher-order functions and `let`](https://kotlinlang.org/docs/scope-functions.html) and [`kotlinlang.org` — Extensions](https://kotlinlang.org/docs/extensions.html) — version pin: stable; Kotlin 2.0 docs. Licence: Apache 2.0.
  - JavaScript: [`developer.mozilla.org` — Function composition](https://developer.mozilla.org/en-US/docs/Glossary/Functional_programming) — version pin: MDN web docs current. Licence: CC BY-SA 4.0.
  - Rust: [`doc.rust-lang.org` — Traits: Defining Shared Behaviour](https://doc.rust-lang.org/book/ch10-02-traits.html) — version pin: The Rust Programming Language, current edition. Licence: MIT/Apache 2.0.
  - Scala: [`docs.scala-lang.org` — Composition](https://docs.scala-lang.org/tour/mixin-class-composition.html) — version pin: Scala 3 docs current. Licence: Apache 2.0.

Verified in: Scala, Rust
