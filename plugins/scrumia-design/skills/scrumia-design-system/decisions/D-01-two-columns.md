# D-01 — The audit reports drift and mutedness on equal footing

## Context

`scrumia-design-audit` measures an existing interface against the design system. The obvious audit reports one thing: where the interface departs from the system. Invented colors, inlined spacings, duplicated components — all cheaply detected, all unambiguous.

## Considered

- **Drift only.** Every finding is mechanical, greppable, and impossible to argue with. It is also the audit that a linter could produce, and it optimizes for a single outcome: an interface that obeys.
- **Reporting only violations pushes toward mutedness.** A one-column audit trains the reader to remove anything the system does not already answer, since nothing symmetric ever rewards distinctiveness. Taken to its end it produces a grid of grey cards where every value is a valid token — an interface that passes the audit completely and looks like no one's product.
- **Mutedness is not mechanically detectable.** It requires a stated identity to measure against, and it costs judgment where the drift column costs a grep. That is a real cost, and it is why the audit stops and says so when `identity.md` is empty rather than guessing.

## Decision

**Adopted.** `scrumia-design-audit` reports drift and mutedness in two columns of equal importance, and refuses to produce the mutedness column without a written identity to anchor it — an unanchored one would be taste wearing an audit's clothes.

`scrumia-designer` carries the same pair as its two failure modes. A module that only guards consistency ends up guarding a product nobody recognizes, which costs more in the projects this module targets than the extra judgment costs.
