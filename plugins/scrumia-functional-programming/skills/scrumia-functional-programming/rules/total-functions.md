Total functions

*Norm.* A function whose signature names every input the function can be called with, and produces an output for each. Failure is a value the signature carries, not a throw the runtime raises. The principle holds with the same wording in every language that supports it; a rule stated in one language's terms belongs to that language's module, not here.

This rule carries a `Verified in:` footer naming the two languages the contributor verified it against. The footer is meta-information about provenance, not the rule itself — and the CI gate (`bin/scrumia-functional-programming-check-vocabulary`) skips it on purpose.

## What is asked of a function

One condition: every input the function accepts has an output the function produces. There is no input the function can be called with for which the function has no answer.

A function that satisfies this is total. A function that fails it is partial, and partiality is the property totality forbids.

## What failure looks like

A function that fails to produce an output for some input has to communicate that fact somewhere. The two places are the signature and the runtime:

- **Failure as a value the signature carries.** The signature names a type that holds both the success and the failure; the function returns that type, and the caller pattern-matches or unwraps it. The caller decides what to do with the failure; the type system tells them it can happen.
- **Failure as a runtime event.** The function declares a partial signature, takes an input for which it has no answer, and the runtime is what tells the caller — by terminating the program, by logging a message, by writing to a stream nobody reads.

The first is the rule. The second is what the rule catches. A partial function is a function whose signature lies about what the function can do, and a runtime event is what the lie becomes when it is exercised.

## What is written instead

A function whose input may not admit an output returns a value the caller can pattern-match: a tagged union of the success shape and the failure shape, with the failure shape carrying the information the caller needs to recover. The signature is honest; the caller is told at the type level; the runtime is not.

A function that calls another function inherits the callee's partiality: if the callee can fail, the caller can fail, and the caller is partial too. The signature names what the caller can fail with, and the type system follows the failure through every layer of the call graph. A function whose callees are total is itself total; a function whose callees are partial is partial, and the signature says so.

The discipline is not "no function ever fails" — it is "no function fails without the signature saying so". A program where every failure is named at the type level is a program where the compiler tells the caller what can go wrong, and the caller decides what to do about it before the runtime does.

## Why

The discipline buys three things:

- **The compiler as the failure checker.** A signature that names its failure is a signature the type checker reads. The caller is told at compile time, not at runtime; the question "what can fail here" has an answer in the type, not in the test suite.
- **No unhandled failure paths.** A function whose signature names its failure is a function the caller cannot ignore — the caller must pattern-match, must unwrap, must decide. A function whose failure is a runtime event is a function the caller can forget, and forgetting is the bug.
- **The error budget is visible.** A program whose failures are all in the type is a program whose total number of failure paths is countable from the signatures alone. A program whose failures are runtime events is a program whose failure paths are enumerable only by running it.

## Sources complémentaires

- The principle is paradigm-wide; the references below name the same rule in each idiom.
  - Kotlin: [`kotlinlang.org` — Exceptions](https://kotlinlang.org/docs/exceptions.html) and the [`Result`](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin/-result/) idiom — version pin: stable; Kotlin 2.0 docs. Licence: Apache 2.0.
  - JavaScript: [`developer.mozilla.org` — Error](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Error) and the [`Promise`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise) idiom — version pin: MDN web docs current. Licence: CC BY-SA 4.0.
  - Rust: [`doc.rust-lang.org` — Recoverable Errors with `Result`](https://doc.rust-lang.org/book/ch09-02-recoverable-errors-with-result.html) and [`?`](https://doc.rust-lang.org/book/ch09-02-recoverable-errors-with-result.html#propagating-errors-with-the--operator) — version pin: The Rust Programming Language, current edition. Licence: MIT/Apache 2.0.
  - Haskell: [`haskell.org` — A gentle introduction to Haskell: Error Handling](https://www.haskell.org/tutorial/) — version pin: tutorial current. Licence: haskell.org site terms.

Verified in: Haskell, Rust
