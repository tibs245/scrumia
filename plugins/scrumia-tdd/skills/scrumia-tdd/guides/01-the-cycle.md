# The Cycle

> Not one line of production code without a red test that justifies it.

## Prerequisites

None — this is the foundation of the whole module. Every other guide in this module assumes the cycle described here.

## Rules

### Rule 1: Red before green, always

Everything else in this module follows from this one rule. A red test first is proof that the test *can* fail — a test written after the fact proves nothing but its own complacency. Full reasoning: [D-01](../decisions/D-01-no-code-without-red-test.md).

### Rule 2: Red — one test, run it, verify why it fails

Write *one* test that expresses the next invariant. Run it. Check that it fails **for the right reason**: a failing assertion, not an accidental import or compilation error.

An agent has a known bias: generating the implementation and the tests in one block, then making everything pass. That is test-after in disguise, and this checkpoint exists precisely to catch it. Why the rule is stated this hard for an agent: [D-02](../decisions/D-02-agent-bias.md).

### Rule 3: Green — the minimum, truly

Write the minimum that makes the test pass. The minimum, truly: generalization will wait for the test that demands it.

### Rule 4: Refactor — under green, clean up

Naming, duplication, structure. Re-run the suite. Then start again with the next invariant.

### Rule 5: Never skip running the red

It is the only step that cannot be faked. A test you didn't watch fail is a test you're only assuming works.

### Rule 6: Never disable a red test to ship

A red test is information; neutralizing it destroys that information. If the test is wrong, fix the test; if it's right, fix the code.

### Rule 7: The unit is the invariant, not the function, not a coverage number

Coverage is a consequence of testing invariants, not a goal in itself — aiming for a percentage produces tests with no real assertion that reach it. Three invariants on one function means three tests; a trivial function with no invariant means zero tests.
