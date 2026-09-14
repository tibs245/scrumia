# Mock Boundary

> We simulate what we don't own. We do not simulate our own modules.

## Prerequisites

- [01-the-cycle](01-the-cycle.md) — mocking decisions happen inside the cycle's green step.
- [06-test-levels](06-test-levels.md) — this boundary is the unit level's; the other two levels run against the real thing by definition.

## Rules

### Rule 1: Simulate what we don't own

The network, the clock, randomness, the filesystem, third-party services. These are the boundary — outside our code, outside our control, and slow or nondeterministic enough that a real call would break the cycle's speed and repeatability.

### Rule 2: Never simulate our own modules

A test that mocks its neighbor verifies a conversation, not a behavior — it will pass after the regression just as it did before.

**Corollary**: if testing a module requires mocking three neighbors, the problem is in the module's splitting, not in the test tooling.

A mock of your own module that only checks it was called with what you just gave it is the tautological test — see [05-useless-tests-catalog, Rule 1](05-useless-tests-catalog.md) for the concrete pattern and what to write instead.

### Rule 3: A unit-level double stands at a port we own, over functionality we don't

The two rules above are one rule read from both ends, and this is where they meet. A unit test's double stands **at a port this code owns** — a storage port, a clock, a provider client — and what it stands in for is the **external functionality** behind that port. That is what makes the unit level offline and fast, and it is the whole licence the level gets.

"Unit tests use doubles" therefore licenses nothing about our own code: a sibling module is not external functionality, so it is never what a double replaces, at any level. Where a real service must be exercised, the answer is an integration test ([06-test-levels, Rule 3](06-test-levels.md)) — never a unit test with our own module faked out behind it.

It decides the value of the entire suite: get this boundary wrong, and every other rule in this module — the cycle, the AC mapping — protects nothing.
