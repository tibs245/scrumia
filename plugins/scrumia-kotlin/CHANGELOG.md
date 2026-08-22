# Changelog — scrumia-kotlin

All notable changes to this module, on [Keep a Changelog 1.0.0](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]

## [0.1.0] - 2026-08-22
### Added
- The module, carrying the **idiomatic Kotlin language rules** capability: six refusal rule families contributed to the `implement`, `review` and `find-spec` registers.
- `01-data-modelling` — `val` / `var`, scope functions (`let`, `run`, `with`, `apply`, `also`), extension functions — what shape a value takes, and how it gets read.
- `02-null-safety` — `?` / `!!`, platform types (`T!` from Java interop), `require` / `check` / `error` — when the type is nullable, and when the runtime believes it is not.
- `03-coroutines` — structured concurrency, scopes, dispatchers, cancellation, `Flow` — how concurrency is written.
- `04-classification` — `data class`, `sealed class` / `sealed interface`, `value class` — when to use each.
- `05-top-level` — object expressions vs companion objects vs top-level functions — what lives where.
- `06-visibility` — `private`, `internal`, `public` — the module boundary, and why a test crossing the wrong one is a finding on the production code.
- `scrumia-kotlin-audit` — a skill auditing an existing Kotlin codebase against the six rules, which establishes the target's Kotlin version first and reports the drift instead of the findings when the version is below 1.5.
- Rules are written against **the Kotlin language** as documented on `kotlinlang.org/docs/` and cite `https://kotlinlang.org/docs/`, the coroutines guide, the Java interop reference, and the coding conventions. The pin is the contract: the rules are grounded on the Kotlin compiler's documented semantics and on the official guide, so a reading of the rule and a reading of the docs agree on what `!!` does, what `coroutineScope { }` guarantees, and what `value class` constrains.
- The module is **compose-only**: no `bin/`, no `dependencies.jsonl`. It contributes to the composition through `extends.json` and nothing else. A pure-JVM project (Spring, Android) activates `scrumia-kotlin` alone and gets the same rules; `scrumia-functional-programming`, `scrumia-kotlin-multiplatform-mobile` and `scrumia-gradle` are not assumed.
