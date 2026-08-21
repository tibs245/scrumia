# 03 — The effect boundary (discipline)

> *Approach: discipline — applies regardless of whether the project uses `Result`, `Either`, `IO`/suspend, or effect.website.*

The seam between description and execution is where the impure lives; nothing crosses it twice. Whatever enters the impure seam (clock, randomness, IO, third-party) does so once, and what exits is a value the rest of the program can hold.

## Prerequisites

- [01-typed-effects](01-typed-effects.md) — the boundary is between description and execution.
- [02-describe-before-execute](02-describe-before-execute.md) — execution is at the seam.

## Rules

### Rule 1: The boundary is the only place the impure lives

Inside the boundary, everything is a description — pure values, typed effects, composed effects. Outside the boundary (at the seam), the description is run, and the impure work happens. The boundary is a line a reviewer can draw on the codebase: everything above it returns values, everything below it (the seam) runs them.

### Rule 2: An impure dependency crosses the boundary once

A clock, a random source, a database connection, an HTTP client, a file handle: each one crosses the boundary once. A function that takes the clock as a parameter and uses it has crossed it once; a function that calls `Clock.System.now()` inside a "pure" path has crossed it again, and the discipline refuses the shape on the ground that the boundary is no longer a boundary.

The test: does the function reach for the dependency it needs, or is the dependency passed in (or wired through an environment / layer, where they apply)? Reaching for the dependency is the service-locator pattern [04-service-locator-avoided](04-service-locator-avoided.md) names; passing it in is the boundary in force.

### Rule 3: What exits the boundary is a value the rest of the program can hold

A function whose return type is `User` and whose body performs an effect and returns a value has produced a value the rest of the program can hold. A function whose return type is `IO<User>` has produced a description; the boundary is where that description becomes a `User`. What exits the boundary is what the rest of the program holds — never a partially-run description, never a half-applied effect.

### Rule 4: A second crossing is a finding

A program whose effect is run, the result is held, and then the result is re-wrapped in another effect (`IO { existingIO.unsafeRunSync() }`) has crossed the boundary twice. The discipline refuses the shape: the boundary is a line, not a region, and a second crossing is the failure the boundary exists to catch.

The fix is structural: compose the descriptions before they cross the boundary, and cross once.

### Rule 5: A test that needs the seam to be impure is not testing the boundary

A test that reaches for `Clock.System.now()`, instantiates an HTTP client, or reads a file to verify a function is testing the impure work, not the function. The discipline names the test the wrong test: a function that returns a description can be tested with a description-shaped input, without the seam, and the test that needs the seam is the test that says the function was not separable from the effect to begin with.

The right test asserts on the description: given this input, the function produces this description. The runtime the test runs against may run the description, but the assertion is on the description itself.
