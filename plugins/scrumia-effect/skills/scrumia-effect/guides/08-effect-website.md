# 08 — effect.website (approach: effect.website)

> *Approach: effect.website — applies when the project reaches for the reference implementation of the typed-effect discipline, articulated at [`https://effect.website`](https://effect.website). The environments and layers pattern lives here; "service-locator avoided" applies at discipline level only ([04-service-locator-avoided](04-service-locator-avoided.md)).*

effect.website is the reference implementation this module cites for the typed-effect discipline: describe-before-execute, typed errors, environments, layers, effect polymorphism, structured concurrency, retry as data. A project that adopts effect.website directly receives the discipline from `scrumia-effect` and the API from that library. This module does not wrap it — it does not vendor a client, re-export the API, or substitute its own types.

## Prerequisites

- [01-typed-effects](01-typed-effects.md) — `Effect<R, E, A>` is a typed effect.
- [02-describe-before-execute](02-describe-before-execute.md) — execution is at the seam.
- [03-effect-boundary](03-effect-boundary.md) — the boundary is where the impure lives.
- [04-service-locator-avoided](04-service-locator-avoided.md) — the call site does not reach for the dependency.

## When to reach for effect.website

The discipline alone (sections 01-04) covers most codebases. effect.website is the reference for projects where one or more of the following are true:

- The codebase has several effect-producing operations (clock, randomness, IO, third-party services) that compose into larger programs, and the composition needs to be type-checked.
- The codebase needs **environments** — typed contexts (e.g. `Clock`, `HttpClient`, `Logger`, `Database`) that the program declares and the implementation provides, with the type system enforcing that every effect that needs an environment has it.
- The codebase needs **layers** — composable descriptions of how environments are built, so that test layers, production layers, and per-environment layers are the same shape.
- The codebase needs **effect polymorphism** — the ability to write a function whose effect type is generic over `Effect<R, E, A>` so the same function works against `Clock`, `TestClock`, and a custom test environment without code change.
- The codebase needs **structured concurrency** — fibers, interruption, scoped resources, the kind of runtime management that goes beyond "run this and wait."

A project that does not need any of the above reaches for `Result`, `Either`, or `IO`/suspend and stops there. The discipline applies; the reference implementation is not justified by the use case.

## Rules

### Rule 1: Environments replace the service-locator pattern, with the type system enforcing it

A `Clock` in effect.website is not a global. It is a context the program declares (`type Clock = Clock.Service`) and provides via a `Layer`. A function that uses the clock imports it from the environment (`yield* Clock.currentTimeMillis`), and the type system says "this effect needs a `Clock`." The discipline's "service-locator avoided" rule is enforced here not by convention but by the type: a function whose environment does not declare `Clock` cannot call `Clock.currentTimeMillis`.

The test: does the function declare its environment requirements (`Effect<Clock | HttpClient, Error, User>`)? If the answer is "no, it just uses them," the program has lost the discipline effect.website exists to enforce.

### Rule 2: Layers are the shape of "how an environment is built"

A `Layer<R, E, A>` is a description of how to construct `A` from `R` (or from nothing). The discipline treats `Layer` as the answer to "how is this dependency wired in production, in tests, in a CLI, in a server" — and the test layer, the production layer, and the per-environment layers are the same shape, composed with `Layer.merge` / `Layer.provide` / the equivalent.

A `main` function that wires the layers is the seam: it provides the production layer to the program and runs the program. The program itself is a description that takes the environment as a parameter, and the seam is the function that gives it one.

### Rule 3: An environment hand-wired at the call site has lost the layers mechanism

A function that imports `HttpClient` directly (constructing it or fetching it from a registry) has lost what effect.website ships the layers mechanism to enforce. The discipline refuses the shape on the same ground as the discipline-level service-locator rule, with the addition that the type system was the enforcement and the type system has been bypassed.

The fix is structural: declare the dependency as part of the environment, provide it through a layer, and let the type system check the wiring.

### Rule 4: Retry is composed as a function on the `Effect`

effect.website's `Effect.retry` (and the schedule-based variants) takes a `Schedule<R, E, A>` and composes retry as a function on the effect, not as a try/catch loop at the call site. The discipline treats this as the reference implementation of [10-retry-as-data](10-retry-as-data.md): the failure carries what the next attempt needs, the schedule decides when the next attempt runs, and the composition is a description the program holds.

### Rule 5: The runtime is the seam

effect.website programs run at the seam: `runPromise`, `runSyncExit`, `runFork`, the entry point that calls one of them. The discipline's rule is the same as the IO rule: the seam is named, the description is held until the seam, and a program that runs effects inside the description has lost the discipline.

### Rule 6: A project that adopts effect.website does not adopt this module as a substitute

effect.website ships its own opinionated guidance, and a project that runs both this module and effect.website receives the discipline from here and the API guidance from there. The two cite each other in prose where the rule needs to (this guide cites effect.website for the API; effect.website's own docs cite this module's discipline for the rationale). What this module does not do is re-export effect.website's API as its own — a project adopting effect.website is adopting effect.website, not a ScrumIA wrapper of it.

## Source

- [`https://effect.website/docs`](https://effect.website/docs) — the discipline: describe before execute, environments, layers, effect polymorphism, error model, concurrency.
- [`https://effect.website/docs/error-management/retry`](https://effect.website/docs/error-management/retry) — retry as a function on the effect, with `Schedule`.
- [`https://effect.website/docs/requirements-management/layers`](https://effect.website/docs/requirements-management/layers) — the layers mechanism that replaces the service-locator pattern with a type-system-enforced environment.

A rule without a citation to effect.website is not in this section; this module cites the reference and nothing else.
