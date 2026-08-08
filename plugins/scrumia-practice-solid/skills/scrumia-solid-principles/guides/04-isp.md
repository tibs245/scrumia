# I — Interface Segregation

> An interface is cut to the measure of its consumer, not its implementer.

## Prerequisites

None — each principle guide stands on its own.

## Rules

### Rule 1: The principle

An interface is cut to the measure of its *consumer*, not its implementer. Nobody depends on methods they don't call.

### Rule 2: Where it applies

Applies to interfaces, traits, component props, the surface of SDKs and exported modules.

Outside object orientation: I holds for a component's props as much as for a trait.

### Rule 3: Violation signals

- The test implementation that must provide fifteen methods to exercise one.
- A component with twenty props of which each usage fills four.
- The single "repository interface" that all services traverse in full.

### Rule 4: Application limits — over-application

Thin does not mean atomized — twenty one-method interfaces for a single consumer is the catch-all turned inside out.

Signals that the segregation has gone too far:

- One interface per method, systematically, with no distinct consumer to justify it.
- More interface files than behavior files.
