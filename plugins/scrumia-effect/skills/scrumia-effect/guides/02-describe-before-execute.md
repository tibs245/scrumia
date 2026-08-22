# 02 — Describe before execute (discipline)

> *Approach: discipline — applies regardless of whether the project uses `Result`, `Either`, `IO`/suspend, or effect.website.*

A function returns a description; execution happens at the seam, not at the call site. The call site is pure, the seam is impure, and the seam is the only place the impure lives.

## Prerequisites

- [01-typed-effects](01-typed-effects.md) — the description is a typed effect.

## Rules

### Rule 1: The call site is pure

The function the caller invokes returns a value. Whatever impure work the caller is asking for is represented by that value and will be performed elsewhere — at the seam, by the runtime, by a function whose job is to run the description. The call site does not read the clock, does not write to disk, does not block on IO; it composes values.

### Rule 2: The seam is impure, by definition

There is one place where the description becomes execution: the seam. In a `Result`-only program, the seam is wherever the result is unwrapped and the failure is observed; in an `IO` program, it is `unsafeRunSync` / `unsafeRunAsync` / the equivalent; in effect.website, it is the runtime's `runPromise` / `runSyncExit` and the entry point that calls it. The seam is not optional — every typed effect has to be run somewhere, and "somewhere" is the seam.

The discipline's test: can a reader name the function whose job is to run the description? If the answer is "the entry point, eventually, somewhere," the seam is not named, and the discipline is not in force.

### Rule 3: The seam is named, not anonymous

A program whose effect is run by the call site — `val user = api.get("/users/$id")` inside a function the caller invokes — has no seam; the call site is impure, and the discipline refuses the shape. The seam is named so the discipline is enforceable: a reviewer can find the function whose return type is `T` and whose body runs the description, and the program has exactly one of them per process.

### Rule 4: Description composes; execution does not

Two effects combine as values: `effectA.flatMap { a -> effectB(a) }`, `resultA.flatMap { a -> resultB(a) }`, `eitherA.flatMap { a -> eitherB(a) }`, or their `for`-comprehension equivalents. The composition is a description of the combined effect, not the running of it. Running is a separate step, performed once, at the seam.

The discipline's test: can the two effects be combined without running either one? If the answer is "no, the first one runs when it's constructed," neither one is a description, and the discipline is not in force.

### Rule 5: A description that runs at construction is not a description

A function that returns `IO { … }` and the `IO { … }` block performs the effect when the `IO` is constructed — rather than when the `IO` is run — has performed the effect at construction time. The discipline refuses the shape: the type says description, the runtime says execution, and the two have to agree.

The fix is structural: build the description with values (`IO.defer { … }`, `Effect.suspend { … }`, the equivalent in each approach), so the block runs at the seam, not at construction.
