# L — Liskov Substitution

> Every implementer of a contract honors the entire contract — including what it never spells out.

## Prerequisites

None — each principle guide stands on its own.

## Rules

### Rule 1: The principle

Every implementer of a contract honors the *entire* contract — types, but also implicit invariants: what is promised not to throw, the accepted bounds, the semantics of edge cases. The one that throws where the contract promises a value, or that demands more than the contract announces, is lying.

### Rule 2: Where it applies

Applies everywhere a contract exists — type hierarchy, trait, interface, callback, endpoint that promises a schema.

Outside object orientation: L holds for any form of contract — trait, interface, callback signature, API schema.

### Rule 3: Violation signals

- An implementer that throws `NotImplemented` on part of the contract.
- Calling code that tests the concrete type before calling ("if it's variant X, don't do Y").
- An override that accepts less or promises more weakly than the contract.
- A test mock that needs to know *which* implementer will be there to predict the result.

### Rule 4: Application limits — over-application

None known. L is the only one of the five with no over-application case: an implementer that cannot honor the contract reveals a badly cut contract, and it is the contract you fix — not a sign the principle was pushed too far.
