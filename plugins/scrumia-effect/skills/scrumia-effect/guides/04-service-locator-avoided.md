# 04 — Service-locator avoided (discipline)

> *Approach: discipline — applies regardless of whether the project uses `Result`, `Either`, `IO`/suspend, or effect.website. "Service-locator avoided" applies at discipline level only; the environments/layers mechanism lives in the effect.website section ([08-effect-website](08-effect-website.md)).*

The call site does not reach for the dependency it needs. Environments and layers, where they apply, replace the constructor-injected service locator; discipline-level, this is the statement that nothing the function depends on is fetched globally, threaded through a parameter object, or imported as a singleton.

## Prerequisites

- [01-typed-effects](01-typed-effects.md) — a typed effect is what the dependency is wired into.
- [03-effect-boundary](03-effect-boundary.md) — the boundary is where dependencies cross once.

## Rules

### Rule 1: A function does not reach for the dependency it needs

A function that calls `Clock.System.now()`, instantiates an HTTP client, reads a global config object, or looks up a service in a registry has reached for the dependency it needs. The discipline refuses the shape on the ground that the call site is the service-locator pattern: the function's behaviour depends on something fetched globally, and the function does not say so.

The fix is to pass the dependency in — as a parameter, as part of an environment (in effect.website), as a constructor argument (in object-oriented code). What the function depends on is then named at the function's boundary, and the function is testable without standing up the dependency.

### Rule 2: No global singleton behind the scenes

A module that exposes a function and silently uses a globally-registered dependency to do its work is the service-locator pattern in disguise: the function looks pure, the test runs against the global, and the dependency is invisible to the reader. The discipline refuses the shape: a singleton behind the function is the same singleton the function would reach for directly, with one extra layer of indirection that hides it.

### Rule 3: No parameter object that is a service locator in disguise

A function that takes a `Dependencies` or `Services` or `Context` parameter and reaches through it for `deps.clock`, `deps.httpClient`, `deps.database` has been handed the service-locator as a parameter. The discipline refuses the shape on the same ground as Rule 1 — the call site reaches for the dependency it needs, just through an extra dot.

The fix is structural: take the dependency itself, not the object that carries it. The function's signature names what it depends on.

### Rule 4: Where environments and layers apply, they replace the locator

In effect.website, the discipline's mechanism is `Layer<R, E, A>` and `Effect.gen { … }` with `Clock` / `HttpClient` / etc. imported from the environment rather than constructed at the call site. The service-locator pattern's absence in effect.website is not because effect.website forbids globals — it is because the type system replaces the global with an environment the program declares.

The discipline-level rule is what carries across all four approaches: the call site does not reach for the dependency. The mechanism by which this is enforced is the approach's own — environments and layers in effect.website, constructor parameters in OO code, function parameters in pure code, and the test is the same: a reviewer can name, from the function's signature, everything the function depends on.

### Rule 5: A test that stands up the dependency to test the function is the wrong test

A function that reaches for a global needs the global in the test, and the test becomes a test of the global as much as of the function. The discipline names this the test the wrong test: a function that takes its dependency as a parameter can be tested with a test-double of the dependency, and the test is a test of the function.

The right test instantiates the dependency, passes it in, and asserts on what the function did with it. The test that needs the singleton to be live is the test that says the function was not separable from its dependency.
