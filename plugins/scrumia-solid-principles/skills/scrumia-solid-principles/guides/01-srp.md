# S — Single Responsibility

> A module groups what changes together, for the same requester — not "does one literal thing".

## Prerequisites

None — each principle guide stands on its own.

## Rules

### Rule 1: The principle

A module groups what changes together, for the same requester. "Requester" in the broad sense: the business rule, the export format, and the retry policy change neither at the same pace nor at the request of the same people. Group what shares a pace and a requester; separate what doesn't.

### Rule 2: Where it applies

Applies to any named unit — module, class, function, component.

Outside object orientation: S holds for a module, a function, a component — no class required.

### Rule 3: Violation signals

- The file every PR touches, whatever the subject.
- A module whose name contains "and", "manager", "utils", "common".
- A function whose parameters split into two groups that never cross.
- Imports in two airtight families (half talk to the database, the other half to rendering).

### Rule 4: Application limits — over-application

A responsibility is not a function — ten functions that change together are *one* responsibility. Splitting beyond that scatters what is always read together.

Signals that the split has gone too far:

- Ten fifteen-line files always opened together to understand a single behavior.
- A simple change that crosses five files by ricochet of delegations.
- Increasingly abstract names to justify the splitting (`Processor`, `Handler`, `Orchestrator` in the same chain).
