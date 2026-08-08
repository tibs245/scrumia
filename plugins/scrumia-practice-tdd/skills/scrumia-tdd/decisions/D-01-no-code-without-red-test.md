# D-01: The founding rule — no production code without a red test

**Status**: Adopted
**Date**: 2026-08-07
**Impacts**: [guides/01-the-cycle.md](../guides/01-the-cycle.md)

## Context

The practice needs one rule everything else can be derived from — the cycle's four steps, the mock boundary, the AC mapping — rather than a list of independent rules an agent has to remember and reconcile on its own. The question is what that single rule should be, and specifically whether it must be *red-first* rather than, say, "every line of code has a test" with no ordering constraint.

## Arguments For

- A red test first is proof that the test *can* fail — a test written after the fact proves nothing but its own complacency. Writing the assertion before the code exists is the only way to know the assertion would actually catch the bug it claims to guard against.
- Everything else in this module is a corollary of this one rule, not a parallel rule to keep in sync with it: the cycle operationalizes it step by step, the mock boundary protects what it's allowed to observe, the AC mapping tells it what invariant to write next.
- It gives a binary, checkable gate, for a human reviewer and for an agent alike: was there a failing test for this exact line, yes or no. No interpretation of intent required.

## Arguments Against

- It is a real discipline cost: nothing runs green until a test has failed first, which slows down the first visible progress on a ticket compared to writing the obvious implementation directly.
- It is tempting to bypass under deadline pressure — exactly the moment the safety net matters most, and exactly the moment "no time for a red test" would do the most damage if left as a silent option.
- The rule alone does not guarantee test *quality* — a red test can still be tautological, assertion-free, or otherwise worthless. That residual risk is why the anti-pattern catalog exists as a backstop, not a replacement.

## Verdict

Adopted without exception inside the apps and paths where this practice is plugged in. The legitimate exits are enumerated, not implicit — see [guides/04-where-tdd-stops.md](../guides/04-where-tdd-stops.md) and `exempt_paths` in [guides/03-ac-mapping.md](../guides/03-ac-mapping.md) — so "no time for a red test" is never a silent escape hatch; it is either a declared exemption or a rule violation, never something in between.
