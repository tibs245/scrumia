---
name: scrumia-effect
description: The typed-effect discipline for an agent — describe before execute, failure as a value, the effect boundary, and which approach to reach for (Result, Either, IO/suspend, or effect.website). Library-agnostic on the pattern; cites effect.website as the reference implementation rather than wrapping it. Load before writing or reviewing code that produces, transforms, or consumes a side effect in an app where this module is plugged in.
---

# The typed-effect discipline

This module owns **the discipline of typed effects** — what every approach has to satisfy to be one. It applies to apps that list `scrumia-effect` in their own `extends` in `.scrumia/config.yaml`. The four canonical approaches (`Result`, `Either`, `IO`/suspend, effect.website) are layered on top of the discipline; the discipline is not absorbed into them. A project on `Result` alone reads no rule that requires knowing what `Either` is.

The module cites [https://effect.website](https://effect.website) as the reference implementation of the typed-effect discipline — the canonical articulation of describe-before-execute, environments, layers, and effect polymorphism. It does not wrap that library; a project adopting effect.website directly receives the discipline from this module and the API from that one. ([D-01](decisions/D-01-discipline-split-from-approaches.md)).

## The discipline

The four things every approach has to satisfy to be one. They apply regardless of which approach a project uses; the four approach sections layer on top of them.

- **Typed effects** — an effect is a description of a value-producing action, not the action itself. The type carries that distinction, so the compiler can tell whether a function performed the effect or returned one. → [guides/01-typed-effects.md](guides/01-typed-effects.md)
- **Describe before execute** — a function returns a description; execution happens at the seam, not at the call site. The call site is pure, the seam is impure, and the seam is the only place the impure lives. → [guides/02-describe-before-execute.md](guides/02-describe-before-execute.md)
- **The effect boundary** — the seam between description and execution is where the impure lives; nothing crosses it twice. Whatever enters the impure seam (clock, randomness, IO, third-party) does so once, and what exits is a value the rest of the program can hold. → [guides/03-effect-boundary.md](guides/03-effect-boundary.md)
- **Service-locator avoided** — the call site does not reach for the dependency it needs. Environments and layers, where they apply, replace the constructor-injected service locator; discipline-level, this is the statement that nothing the function depends on is fetched globally, threaded through a parameter object, or imported as a singleton. → [guides/04-service-locator-avoided.md](guides/04-service-locator-avoided.md)

## The four approaches

Layered on top of the discipline. A rule on `Result` is not a rule that applies to an `Either`-only project; an `IO` rule is not a `Result` rule; an effect.website rule is not an `IO` rule. Every guide below names its approach in its first line, so a reader can tell in one line whether the rule applies.

- **Result** — when to use it, when to migrate to `Either`. → [guides/05-result.md](guides/05-result.md)
- **Either<L, R>** — left for failure, right for success; the convention. → [guides/06-either.md](guides/06-either.md)
- **IO / suspend** — the description/execution split as a discipline; `suspend` is named here, not defined (rules on its behaviour live in `scrumia-kotlin`). → [guides/07-io-suspend.md](guides/07-io-suspend.md)
- **effect.website** — when to reach for the reference implementation, and what environments and layers add over the discipline. → [guides/08-effect-website.md](guides/08-effect-website.md)

## Error semantics

Owned here, separated from HTTP. `scrumia-ktor` owns HTTP-status-as-effect; this module owns the recoverable/unrecoverable split, the throw-or-return test, and retry as data.

- **When to throw** — recoverable failures (validation, not-found, conflict, timeout) return a value; unrecoverable failures (invariant violation, exhausted resources, programmer error) throw. The test: "if I catch this and continue, do I know what's true?" → [guides/09-when-to-throw.md](guides/09-when-to-throw.md)
- **Retry as data, not marketing** — a failure that may be retried carries `Retry-After`, attempt count, backoff hint; retry composes as a function on the effect, not as a try/catch loop at the call site. → [guides/10-retry-as-data.md](guides/10-retry-as-data.md)

## Guides

| File | Use when you need to... |
|---|---|
| [01-typed-effects](guides/01-typed-effects.md) | Decide whether a value is an effect or a description of one |
| [02-describe-before-execute](guides/02-describe-before-execute.md) | Split what an effect is from when it runs |
| [03-effect-boundary](guides/03-effect-boundary.md) | Locate the seam where the description hands off to execution |
| [04-service-locator-avoided](guides/04-service-locator-avoided.md) | Justify "the call site does not reach for the dependency it needs" |
| [05-result](guides/05-result.md) | Choose `Result` and know when to migrate to `Either` |
| [06-either](guides/06-either.md) | Apply the `Either<L, R>` convention — left for failure, right for success |
| [07-io-suspend](guides/07-io-suspend.md) | Treat the description/execution split as a discipline; name `suspend`, do not define it |
| [08-effect-website](guides/08-effect-website.md) | Decide whether to reach for the reference implementation |
| [09-when-to-throw](guides/09-when-to-throw.md) | Apply the recoverable / unrecoverable test for whether a function returns or throws |
| [10-retry-as-data](guides/10-retry-as-data.md) | Compose retry as a function on the effect, with the failure carrying what the next attempt needs |

## Routing table

```
"I'm writing or reviewing a function that produces, transforms, or consumes a side effect"
  → 01 + 02 + 03 + 04 (the discipline)

"I'm picking between Result, Either, IO/suspend, and effect.website"
  → 05 + 06 + 07 + 08 (the four approaches)

"I'm deciding whether a function returns a value or throws"
  → 09 (error semantics)

"I'm implementing retry — same call, several attempts"
  → 10 (retry as data)

"I'm wiring dependencies into an effect"
  → 04 (service-locator avoided), or 08 (environments and layers) if effect.website

"I'm reading a project that uses only Result"
  → 01 + 02 + 03 + 04 + 05 + 09 + 10
    (the discipline, the Result section, and the error-semantics sections that apply to any approach)
```

## Dependencies between guides

```
01-typed-effects                     ← foundation, no dependencies
02-describe-before-execute           ← requires 01 (the description is the typed effect)
03-effect-boundary                   ← requires 02 (the boundary is where description hands off to execution)
04-service-locator-avoided           ← requires 01 (a typed effect is what the dependency is wired into)
05-result                            ← requires 01 (Result is one typed effect)
06-either                            ← requires 01 (Either is one typed effect)
07-io-suspend                        ← requires 01 + 02 (IO/suspend is the description/execution split made explicit)
08-effect-website                    ← requires 01 + 02 + 03 + 04 (the reference implements the whole discipline)
09-when-to-throw                     ← independent — the throw-or-return test applies regardless of approach
10-retry-as-data                     ← requires 01 + 09 (retry is data on the failure the test already named)
```

The discipline and the four approaches are not parallel: the four are layered on top of the discipline. A reader can start with the discipline alone and reach the approach that matches what their project uses; the approach guides assume the discipline has been read.

## Decisions

| ADR | Decision | Related guides |
|-----|----------|----------------|
| [D-01](decisions/D-01-discipline-split-from-approaches.md) | The discipline is split from the four approaches, not absorbed into them — a `Result`-only project reads no `Either` rule as load-bearing | 01-10 |
| [D-02](decisions/D-02-retry-as-a-function-on-the-effect.md) | Retry composes as a function on the effect, not as a try/catch loop at the call site | 10 |

## Dissociation

The discipline is broad on purpose; what this module does NOT own is named so a project reading it knows where the rule actually lives.

- **The paradigm (purity, total functions, immutability, typeclasses)** → `scrumia-functional-programming`. The discipline here is about effects; the paradigm-level rules about why effects exist are stated there.
- **HTTP-specific error handling (Ktor's `StatusCode`, `expectSuccess`, response-shape failures)** → `scrumia-ktor`. A rule that names `StatusCode` belongs there, not here.
- **Kotlin language constructs (`suspend`, `Flow`, `CoroutineContext`)** → `scrumia-kotlin`. The IO/suspend guide names `suspend` as the discipline's marker; its behaviour — cancellation, structured concurrency, dispatchers — is owned there.
- **Kotlin Multiplatform source-set wiring of an effect library** → `scrumia-kotlin-multiplatform-mobile`. The discipline is library-agnostic on the pattern; the wiring of a library across source sets is not this module's question.
- **A specific library's API beyond its effect model** — the library's own documentation carries it. This module teaches the discipline; the rest of the API belongs to the library.

A project using any of the four approaches can activate `scrumia-effect`; the module does not encode a choice between them.

## Per-app scoping

This module applies to the apps that list `scrumia-effect` in their own `extends` in `.scrumia/config.yaml`. Within an app, [`section.json`](section.json)'s globs pick which files the guides apply to. The default scope is every source file; a project that wants to scope narrower sets `params.globs` under the module's own key.

## Source

The single authority for the typed-effect discipline is the effect.website documentation:

- [`https://effect.website/docs`](https://effect.website/docs) — the discipline articulated: describe before execute, environments, layers, effect polymorphism, error model, concurrency.
- [`https://effect.website/docs/error-management/retry`](https://effect.website/docs/error-management/retry) — retry as data on the failure.

This module cites this source and nothing else — no blog post, no tutorial, no community pattern. The pin is the reference: the discipline is read off that documentation, not off a wrapper this module ships.
