---
name: scrumia-kotlin-audit
description: Audit a Kotlin codebase against the six rule families this module ships — val/var and scope functions, null-safety and platform types, coroutines and Flow, data/sealed/value classes, object vs companion vs top-level, and visibility modifiers. Use it before adopting the module on an existing codebase, when a Kotlin bug ships, or to check a contract the language documents is actually being honoured.
---

# Auditing idiomatic Kotlin

Six rule families, each catching a defect the language docs name and the codebase may
silently break. Walk the source tree once per family, name the rule each finding
violates, cite the Kotlin documentation the rule is grounded on. Report findings;
change nothing without being asked.

Every rule this module ships is written against the **Kotlin language** as documented
on `kotlinlang.org/docs/`. Establish the target's Kotlin version first, from its
`build.gradle.kts` / `build.gradle` (or its `libs.versions.toml`):

```bash
grep -m1 'kotlin' build.gradle.kts 2>/dev/null || grep -m1 'kotlin' build.gradle 2>/dev/null
```

On a Kotlin version older than **1.5** (the `value class` introduction), report the
gap rather than the findings: rules 04 and 05 reference `value class` semantics that
did not exist before then. The audit does not say which version the project *should*
use; it says which rules can be applied unchanged.

## 1 — Is `var` carrying the invariant, or could `val`?

Rule: [`01-data-modelling`](../../rules/01-data-modelling.md).

`val` by default. A `var` is justified only when reassignment is the *behaviour*, not
when it is a single assignment that a reader has to assume is the only one.

```bash
grep -rn -E '\bvar\b' --include='*.kt' src | head -50
```

For each `var`, ask: does this declaration reassign itself in the function it lives in?
A `var` that is assigned exactly once is the strongest signal — the `val` form exists
on the line below.

Then the scope functions: `apply`, `also`, `let`, `run`, `with` chosen by reflex rather
than by what the call site reads. The wrong choice compiles; the cost is the next
reader's comprehension, and the only signal is the call site itself. Walk the call
sites where scope functions appear and check the choice against the table the rule
states.

**A finding is a `var` with a single assignment, or a scope function that does not
match the call site.** A `var` inside a loop, inside a builder, or on a counter is
correct. A `var` followed by a single assignment is the finding.

## 2 — Is `!!` carrying a proof, or a hope?

Rule: [`02-null-safety`](../../rules/02-null-safety.md).

`?` on every value that can be absent. `!!` only with a stated local proof (an
early-return, an explicit null check, a sealed-`when` branch that has already
excluded the null case). Platform types (`String!` from Java) handled at the boundary.

```bash
grep -rn '!!' --include='*.kt' src | head -50
grep -rn '!!' --include='*.java' src 2>/dev/null | head -10   # Kotlin calling Java: the platform type is here
```

For each `!!`, look at the line above and the line below. The proof is the early-return
that makes the value non-null before the `!!` consumes it; without the proof, the `!!`
is the same as `!!` in a test, where the test passing is the proof. The proof at the
call site is the only form that survives a refactor.

Then the platform types. A Java method returning `String!` is read by Kotlin as either
`String` or `String?`; the caller's choice is the boundary's contract. A Kotlin
function whose return type is `String` and whose body calls a Java method that returns
`String!` is the failure mode — the boundary is silent.

**A finding is a `!!` without a proof on the line above, or a Kotlin function whose
body crosses a Java boundary and returns `String` instead of `String?`.** A `!!`
inside a test, on a value the test constructed one line up, is correct.

## 3 — Is concurrency structured, and is cancellation cooperative?

Rule: [`03-coroutines`](../../rules/03-coroutines.md).

Structured concurrency by default. `coroutineScope { }` or a scoped lifetime
(`viewModelScope`, `lifecycleScope`, application scope for bootstrap-only work).
`GlobalScope.launch` is the documented escape, and the docs name it for exactly the
cases where cancellation is wrong.

```bash
grep -rn 'GlobalScope' --include='*.kt' src | head -20
grep -rn 'runCatching' --include='*.kt' src | head -30
grep -rn '\.collect' --include='*.kt' src | head -30
grep -rn 'Dispatchers\.' --include='*.kt' src | head -30
```

For each `GlobalScope.launch`, ask: is this the bootstrap? `GlobalScope` is named for
the application lifetime; a ViewModel-scoped job, a request-scoped job, a screen-scoped
job is the wrong default. The next reader has to prove the work survives cancellation
correctly, and the proof costs every reader.

For each `runCatching`, ask: does the block call a `suspend` function? If yes, the
`runCatching` swallows `CancellationException`, which is the channel through which
structured cancellation propagates. The Kotlin coroutines exception handling reference
documents this — the finding cites it.

For each `.collect`, ask: is the call inside a `launch`? A `Flow.collect` is itself a
suspending function; a bare block on a member function of a non-suspending class is
either unreachable (the compiler says so) or in an implicit scope the reader has to
find.

For each `Dispatchers.Main` / `Dispatchers.IO` / `Dispatchers.Default` reference at a
call site, ask: is the dispatcher injected? A hard-coded dispatcher couples the
function to the platform; the test cannot honour the contract; the production code
cannot switch dispatchers for an upstream that demands a different thread pool.

**A finding is a `GlobalScope.launch` outside the bootstrap, a `runCatching` around
suspension, a `.collect` outside a `launch`, or a hard-coded `Dispatchers`.** Each
finding cites the rule and the Kotlin coroutines documentation.

## 4 — Is the type the right shape?

Rule: [`04-classification`](../../rules/04-classification.md).

`data class` for value-shaped records. `sealed class` / `sealed interface` for closed
hierarchies. `value class` for type-safe wrappers around a single underlying value.

```bash
grep -rn -E '^\s*(override\s+)?fun\s+(equals|hashCode|toString)\b' --include='*.kt' src | head -30
grep -rn 'class\s\+\s*[A-Z][A-Za-z0-9]*\s*{' --include='*.kt' src | head -50
grep -rn -E 'value\s+class\s' --include='*.kt' src 2>/dev/null
```

For each hand-written `equals`/`hashCode`/`toString` inside a class, ask: would
`data class` have generated the same form? If yes, the hand-written form is the
finding. A hand-written form that disagrees with what `data class` would have
generated is also a finding — it disagrees.

For each `class` declaration with a string field that names a kind ("type", "kind",
"category") and one or more payload fields that are only set for some kinds, ask:
is this a closed hierarchy written as a flat record? A `sealed interface` with two
data-class implementations makes the type system enforce what the string was supposed
to enforce.

For each `data class` with one field, ask: is this a `value class` instead? The
wrapper's identity is the value's identity; the `data class` ceremony buys an
allocation on every wrap and unwrap, and the `equals`/`hashCode`/`toString` are not
even the right contracts.

**A finding is a hand-written `equals`/`hashCode`/`toString` where `data class`
would do, a flat record with a kind-string that should be a sealed hierarchy, or a
single-field `data class` that should be a `value class`.**

## 5 — Is the function where it should be?

Rule: [`05-top-level`](../../rules/05-top-level.md).

Top-level functions when no state is shared. `companion object` only when state or a
stateful factory belongs on the class. `object` *expressions* for one-off SAMs;
`object` *declarations* for true singletons.

```bash
grep -rn 'companion object' --include='*.kt' src | head -30
grep -rn -E '^\s*object\s+\w+\s*[{(]' --include='*.kt' src | head -30
```

For each `companion object`, ask: does it carry state, or a factory that needs to be
on the class for clarity? A `companion object` whose every member is a stateless
helper or a `const val` is the wrong default — the call site walks through
`Order.Companion.create(...)` to reach a function that could have been top-level.

For each `object` *expression* (`object : Interface { ... }`), ask: is this a one-off
listener that closes over local state? Then the expression is correct. For each `object`
*declaration* (`object Foo { ... }`), ask: is this a true singleton with its own file?
Then the declaration is correct. Mixing the two — declaring an `object` expression
where a singleton was meant, or declaring an `object` declaration where a one-off
listener was meant — is the finding.

**A finding is a stateless `companion object`, an `object` expression used as a
singleton, or an `object` declaration used as a one-off listener.**

## 6 — Is the visibility the right granularity?

Rule: [`06-visibility`](../../rules/06-visibility.md).

`private` by default. `internal` as the module boundary. `public` only on a surface
meant to cross a published boundary. A member promoted to `public` to silence a test
that crossed the wrong boundary is a finding on the production code, not the test.

```bash
grep -rn -E '^\s*(public\s+)?val\s+\w+\s*=' --include='*.kt' src | head -50
grep -rn -E '^\s*(public\s+)?fun\s+' --include='*.kt' src | head -50
```

For each `val` and `fun` without an explicit visibility modifier, ask: is this surface
meant to cross a published boundary? The default is `public`, the absence of a
modifier is the absence of a stated boundary, and the reader has to assume the
boundary is "anywhere the type is reachable". The Kotlin visibility reference says
so explicitly.

For each `internal` declaration, ask: is the module the boundary the author intended?
`internal` is the *module* — the Gradle / Maven compilation unit — not the package.
A reader who thinks `internal` is package-private has imported a Java idiom; the
wrong mental model is the wrong default at the wrong scale.

**A finding is a `val` or `fun` whose surface is meant to stay inside the module but
carries no visibility modifier, or an `internal` declaration whose author appears to
have meant package-private.**

## Reporting

One finding per line: the file, the line, the rule's identifier
(`kotlin-language/BR-1` through `kotlin-language/BR-6`), and one line of what was not
met. The six rule families each carry their own BR-number — the ACs in
`features/business/modular-composition/qa.md` pin the identifiers, so a finding's
identifier is greppable against the spec.

Each finding cites the source the rule is derived from — the Kotlin language
documentation, the coroutines guide, the Java interop reference. A finding without a
source citation is a finding against the audit, not against the project.

Close with the count of refusers per family. That is the number the six questions
do not cover individually, and the one worth acting on first: a project that fails
rule 1 across most of its `var` declarations has a different shape of fix than one
that fails rule 6 on a single `internal` declaration.
