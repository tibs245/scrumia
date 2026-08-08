# D — Dependency Inversion

> The domain does not depend on the infrastructure; both depend on a contract the domain owns — and only at the boundaries.

## Prerequisites

None — each principle guide stands on its own.

## Rules

### Rule 1: The principle

The domain does not depend on the infrastructure; both depend on a contract the domain owns.

### Rule 2: Where it applies

Applies at infrastructure boundaries — database, HTTP, file system, clock, randomness, third-party services — plus those the project declares in `settings.practices.scrumia-practice-solid.boundaries` (see [SKILL.md](../SKILL.md)).

Outside object orientation: D is done by injecting a function or a value, not necessarily an object.

### Rule 3: Violation signals

- A business-rule module that imports the HTTP client or the ORM.
- Impossible to test a rule without starting a container.
- The clock read directly (`now()`) in the middle of a rule computation — the test will have to wait for midnight.

### Rule 4: Application limits — over-application

Between two modules of the same domain, the direct call is the right choice — indirection there costs more in readability than it earns in decoupling, since there is nothing to decouple.

Signals that the inversion has gone too far:

- Indirection between two modules of the same domain, which never vary independently.
- A contract owned by the infrastructure (the interface copies the third-party client's API word for word): the dependency is not inverted, it is decorated.
- Dependency injection for pure functions.
