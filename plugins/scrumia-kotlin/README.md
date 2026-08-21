# scrumia-kotlin

The idiomatic Kotlin language rules a Kotlin codebase writes and reads against — naming
and scope functions, null-safety and platform types, coroutines and Flow, data / sealed /
value classes, object vs companion vs top-level, and visibility modifiers. Plugs in app by
app, alongside whichever modules that app also runs.

## What it answers

How does a Kotlin codebase get written so that the language it uses is the language the
team has agreed to? Kotlin ships a rich standard library, an expressive type system, and
a runtime with structured concurrency — and each of those features is a place where the
wrong default accumulates silently: a `var` where `val` would have stated the invariant,
an `!!` that compiles on the day it is written and breaks on the day the contract moves,
a `GlobalScope.launch` that outlives the screen it was launched from. The module names
six rule families, each grounded on the Kotlin language documentation, and each carrying
at least one falsifiable scenario in `features/business/modular-composition/qa.md`.

## What it refuses

- `var` when `val` carries the invariant; `!!` without a stated local proof; a
  Java-interop platform type (`String!`) read as Kotlin.
- Unstructured concurrency (`GlobalScope.launch` outside the bootstrap); swallowed
  `CancellationException`; `Dispatchers.Main` hard-coded; `Flow` collected without a
  scope.
- A `class` with a single property pretending to be a domain value; a `sealed
  interface` written as a `class` with boolean flags; a `value class` used where a
  single type alias would do.
- A `companion object` whose every member is stateless; an `object` expression used as
  a singleton; a private utility function declared inside a class only to reach a
  sibling private field.
- `public` on a member meant to stay inside the module; `internal` read as
  "package-private" (it is not — it is the module boundary); a member promoted to
  `public` to silence a test that crossed the wrong boundary.

## What it ships

| What | Role |
|---|---|
| `SKILL.md` | The reference — six rule families, the routing table between them, the upstream Kotlin documentation each one cites. |
| `rules/01-data-modelling.md` | `val` / `var`, scope functions, extension functions — what shape a value takes, and how it gets read. |
| `rules/02-null-safety.md` | `?` / `!!`, platform types (`T!`), `require` / `check` / `error` — when the type is nullable, and when the runtime believes it is not. |
| `rules/03-coroutines.md` | Structured concurrency, scopes, dispatchers, cancellation, `Flow` — how concurrency is written. |
| `rules/04-classification.md` | `data class`, `sealed class` / `sealed interface`, `value class` — when to use each. |
| `rules/05-top-level.md` | Object expressions vs companion objects vs top-level functions — what lives where. |
| `rules/06-visibility.md` | `private`, `internal`, `public` — the module boundary, and why a test crossing the wrong one is a finding on the production code. |
| `scrumia-kotlin-audit` (skill) | Measures an existing Kotlin codebase against the six rules, each finding citing the rule it breaks. |

All six rule families reach the `implement` and `review` registers through
`extends.json`. A `find-spec` contribution points a reviewer tracing a rule to its
source. No contribution names a consuming module — the scope is the consuming
project's composition.

## What it expects to find

An app whose `.scrumia/config.yaml` lists `scrumia-kotlin` in its own `extends`. Within
such an app, `.kt` files are what the rules apply to. The module ships no `bin/` and
no `dependencies.jsonl` — it is compose-only, and its only job is contributing rules
to the composition.

A project-local override at `.scrumia/overrides/scrumia-kotlin.md` records a house
convention that does not fit the upstream language guide, without forking the module.

## Sources

| Source | Pinned to |
|---|---|
| [`https://kotlinlang.org/docs/`](https://kotlinlang.org/docs/) | **Kotlin language** |
| [`https://kotlinlang.org/docs/coroutines-guide.html`](https://kotlinlang.org/docs/coroutines-guide.html) | **Coroutines** |
| [`https://kotlinlang.org/docs/java-interop.html`](https://kotlinlang.org/docs/java-interop.html) | **Java interop** — platform types |
| [`https://kotlinlang.org/docs/coding-conventions.html`](https://kotlinlang.org/docs/coding-conventions.html) | **Coding conventions** |

Every rule cites this language documentation and nothing else. The pin is the contract:
the rules are grounded on the Kotlin compiler's documented semantics, so a reading of
the rule and a reading of the docs agree on what `!!` does, what
`coroutineScope { }` guarantees, and what `value class` constrains.

## Dissociation

Each concept lives separately. `scrumia-kotlin` does not assume
`scrumia-functional-programming` is present — its rules are stated in terms of
idiomatic Kotlin, not in terms of a paradigm. A one-line pointer to
`scrumia-functional-programming` may appear under a rule whose Kotlin phrasing touches
the paradigm (val-vs-var, data/sealed classes, require/check/error); it is never a
load-bearing rationale, and the rule reads correctly without it.

`scrumia-kotlin` does not assume `scrumia-kotlin-multiplatform-mobile` or
`scrumia-gradle` either. Source sets, `expect`/`actual`, and build DSL are not its
subject. A pure-JVM project (Spring, Android) activates `scrumia-kotlin` alone and gets
the same rules.
