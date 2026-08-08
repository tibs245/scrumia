# O — Open/Closed

> At proven variation points, add a case without reopening the code of the existing cases.

## Prerequisites

None — each principle guide stands on its own.

## Rules

### Rule 1: The principle

At proven variation points, you add a case without reopening the code of the existing cases. Open for extension, closed for modification.

### Rule 2: Where it applies

Applies where a third case has already arrived, or arrives at a known cadence — export formats, payment providers, per-country rules.

Outside object orientation: O is done through composition — higher-order functions, strategy parameters — not through inheritance.

### Rule 3: Violation signals

- The cascade of `if`s on a type that grows with each new case, duplicated in several places.
- Adding a case requires modifying N files that asked for nothing.

### Rule 4: Application limits — over-application

A speculative extension point is a debt. When the variants are known and closed, a closed sum (enum + exhaustive handling) that **breaks at compile time** when a case is added beats open extensibility.

Signals that the extension point is speculative:

- An extension point with a single case for two years, complete with its factory and its registry.
- Configuration to vary what no deployment varies.
- Open extensibility where closure would help: when the variants are finite and known, a closed sum (enum, discriminated union) with exhaustive handling turns "I forgot a case" into a compile error. That is a *choice to close*, and it is often the right one.
