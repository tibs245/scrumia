---
name: scrumia-kotlin
description: The ScrumIA Kotlin reference — naming and scope functions, null-safety and platform types, coroutines and Flow, data/sealed/value classes, object vs companion vs top-level, and visibility modifiers. Load it before writing Kotlin in an app whose language module is scrumia-kotlin, and read the refusal rules the same way on review.
---

# Coding in Kotlin

## The contract

- **What shape a value takes** — `val` by default, `var` only when reassignment is the *behaviour*; `data class` for value-shaped records, `sealed class` / `sealed interface` for closed hierarchies, `value class` for type-safe wrappers around a single underlying value. → [01-data-modelling](rules/01-data-modelling.md), [04-classification](rules/04-classification.md)
- **When the type is nullable, and when the runtime believes it isn't** — `?` on every type that can be absent; `!!` only when the local proof is real (and a comment states what the proof is); platform types (`String!` from Java) treated as a borrowed contract, not as a Kotlin type; `require` for argument preconditions, `check` for state preconditions, `error` for the unconditional "this branch is unreachable". → [02-null-safety](rules/02-null-safety.md)
- **How concurrency is written** — structured concurrency by default (`coroutineScope { ... }`, `viewModelScope`, application-scoped lifetimes); `Flow` for cold streams, `StateFlow` / `SharedFlow` only at the seam that needs hot semantics; `Dispatchers` injected, never hard-coded; cancellation cooperative, never swallowed. → [03-coroutines](rules/03-coroutines.md)
- **What lives where in the type system** — `private` by default, `internal` as the module boundary, `public` only when the surface is meant to cross a published boundary; top-level functions over companion-object statics when no state is shared; `object` expressions for one-off, anonymous SAMs; named `object` declarations for true singletons. → [05-top-level](rules/05-top-level.md), [06-visibility](rules/06-visibility.md)

## Rules

Each rule is one file in `rules/`, read on demand. Refusal rules are also contributed
to the `implement` and `review` registers through `extends.json`, so they apply while
code is written and again while it is reviewed, without being written twice.

| File | Refuses |
|------|---------|
| [rules/01-data-modelling.md](rules/01-data-modelling.md) | `var` when `val` suffices; `class` when `data class` carries the same shape; mutable collections where an immutable one is enough |
| [rules/02-null-safety.md](rules/02-null-safety.md) | `!!` without a stated local proof; platform types (Java-interop `String!`) read as Kotlin; precondition functions (`require` / `check` / `error`) used as the wrong category |
| [rules/03-coroutines.md](rules/03-coroutines.md) | unstructured concurrency (`GlobalScope.launch` outside the bootstrap); cancellation swallowed with `try { ... } catch (e: CancellationException) {}`; `Flow.collect` without a scope; `Dispatchers.Main` hard-coded |
| [rules/04-classification.md](rules/04-classification.md) | a `class` with a single property and no behaviour pretending to be a domain value; an `enum class` or `sealed class` written as `class` with boolean flags |
| [rules/05-top-level.md](rules/05-top-level.md) | a `companion object` whose every member is stateless; an `object` expression used as a singleton; a private utility function declared inside a class only to reach a sibling private field |
| [rules/06-visibility.md](rules/06-visibility.md) | `public` on a member meant to stay inside the module; `internal` treated as "package-private"; a member promoted to `public` to silence a test that crossed the wrong boundary |

## Routing table

```
"I need to write or review a value class"
  → 01-data-modelling + 04-classification

"I need to call Java from Kotlin, or Kotlin from Java"
  → 02-null-safety

"I need to launch a coroutine, expose a Flow, or run work in parallel"
  → 03-coroutines

"I need to decide whether a function is top-level, in a companion object, or an expression"
  → 05-top-level

"I need to choose between private, internal and public on a new declaration"
  → 06-visibility

"I need the full contract before writing Kotlin in a covered app"
  → all six rules, in the order above
```

## Dependencies between rules

```
01-data-modelling   ← foundation, no dependencies
02-null-safety      ← requires 01
03-coroutines       ← requires 01, 02
04-classification   ← requires 01
05-top-level        ← requires 01
06-visibility       ← requires 01
```

## Sources

| Source | Pinned to |
|---|---|
| [`https://kotlinlang.org/docs/`](https://kotlinlang.org/docs/) | **Kotlin language** — naming, scope functions, null-safety, classes and inheritance, coroutines, Flow |
| [`https://kotlinlang.org/docs/coroutines-guide.html`](https://kotlinlang.org/docs/coroutines-guide.html) | **Coroutines** — structured concurrency, scopes, dispatchers, cancellation, Flow |
| [`https://kotlinlang.org/docs/java-interop.html`](https://kotlinlang.org/docs/java-interop.html) | **Java interop** — platform types (`T!`) and nullability annotations |
| [`https://kotlinlang.org/docs/coding-conventions.html`](https://kotlinlang.org/docs/coding-conventions.html) | **Coding conventions** — naming, file layout, idiomatic forms |

Every rule cites this language documentation and nothing else — no blog post, no
tutorial, no community pattern. The pin is the contract: the rules are grounded on
the Kotlin compiler's documented semantics and on the official guide, so a reading
of the rule and a reading of the docs agree on what `!!` does, what
`coroutineScope { }` guarantees, and what `value class` constrains. `scrumia-kotlin-audit`
checks the target's Kotlin version first (from its Gradle or Kotlin file) and reports
the drift instead of the findings.

## What this module does not assume

- **No `scrumia-functional-programming`.** Every rule is stated in pure Kotlin syntax
  and semantics — Kotlin keywords (`val`, `data class`, `sealed interface`), Kotlin
  stdlib names (`require`, `check`, `error`, `Flow`), Kotlin language behaviour
  (structured concurrency, null-safety of `T?`). A one-line pointer to
  `scrumia-functional-programming` may appear under a rule whose Kotlin phrasing
  touches the paradigm (val-vs-var, data/sealed classes, require/check/error); it is
  never a load-bearing rationale, and the rule reads correctly without it.
- **No `scrumia-kotlin-multiplatform-mobile`.** No source-set rules, no
  `expect`/`actual`, no platform-specific type choices. A pure-JVM project (Spring,
  Android) activates `scrumia-kotlin` alone and gets the same rules.
- **No `scrumia-gradle`.** No convention-plugin DSL, no build-script patterns. The
  Kotlin rules are about the language, not the build.

## What it expects to find

An app whose `.scrumia/config.yaml` lists `scrumia-kotlin` in the app's own `extends`.
Within such an app, `.kt` files are what the rules apply to. The module ships no
`bin/` and no `dependencies.jsonl` — it is compose-only.

A project-local override is welcome at `.scrumia/overrides/scrumia-kotlin.md` — a
house convention that doesn't fit the upstream language guide, recorded without forking
the module.

## The module's other skill

`scrumia-kotlin-audit` — measures an existing Kotlin codebase against these rules,
finding by finding, citing the rule each finding violates.
