# D-01: Over-application audited on equal footing with violations

**Status**: Adopted
**Date**: 2026-08-07
**Impacts**: [guides/01-srp.md](../guides/01-srp.md), [guides/02-ocp.md](../guides/02-ocp.md), [guides/03-lsp.md](../guides/03-lsp.md), [guides/04-isp.md](../guides/04-isp.md), [guides/05-dip.md](../guides/05-dip.md)

## Context

A principle without a limit of application becomes a reflex, and a reflex produces useless abstraction. Half the cost of SOLID in the wild comes from its **over-application**, not from its absence: the single-implementer interface created "just in case", the service that delegates to the repository that delegates to the DAO for a behavior that never varies, the extension point with a factory and a registry around a single case.

The question this module asks is never "does this code comply with the principle?" but "**what varies here, and what must stay stable?**". The principles are answers to real variation; without variation, they have nothing to say. This forces a choice in how `scrumia-solid-audit` reports findings: does it look for violations only, or for both violations and over-applications, with equal weight?

## Arguments For (two-column audit)

- **Violations and over-applications are the same mistake in opposite directions.** Missing S on a hot file and splitting a stable module into ten files both come from treating a principle as a reflex instead of an answer to observed variation.
- **Reporting only violations pushes toward over-design.** A one-column audit trains the reader to add abstraction whenever a principle "could" apply, since there is no symmetric finding to catch the opposite mistake. A two-column audit makes removing an abstraction as legitimate a deliverable as adding one.
- **The removal move needs to be as well-known as the addition moves.** `scrumia-solid-refactor` names a concrete move for over-application ("Inline") on equal footing with the moves for the five violations — that only makes sense if the audit that feeds it treats both as first-class findings.
- **L is the control case that proves the method isn't symmetric by default.** L has no known over-application case (see [guides/03-lsp.md](../guides/03-lsp.md)) — an implementer that cannot honor its contract always points back to a badly cut contract, never to "too much substitutability". Auditing for over-application on all five principles, and finding none for L, is itself informative: it confirms the audit is observing the code, not filling a quota.

## Arguments Against (trade-offs accepted)

- **Doubles the audit's cognitive load.** Every finding now needs a direction call (missing vs. excessive), not just a yes/no compliance check. This costs more time per file than a violations-only pass.
- **"Nothing varies" is a judgment call, not a fact.** Unlike a violation signal (an `if` cascade is visible), over-application requires knowing the change history of a zone — a single implementer today may be one deploy away from a second. This risk is mitigated, not eliminated, by scoping the audit to stabilized code and excluding young or exploratory zones (see the "What is not a finding" section of `scrumia-solid-audit`).
- **Lengthens the deliverable.** Two tables plus a synthesis is more to read than a violations list, for a stakeholder who only wants "what's broken".

## Verdict

**Adopted.** `scrumia-solid-audit` reports violations and over-applications in two columns of equal importance, and `scrumia-solid-refactor` names "Inline" as a move on equal footing with the five violation-fixing moves. Delivering one column without the other pushes toward over-design, which costs more in the codebases this module targets than the extra audit effort costs.
