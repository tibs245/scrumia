# D-02: Why the cycle is stated this hard for an agent

**Status**: Adopted
**Date**: 2026-08-07
**Impacts**: [guides/01-the-cycle.md](../guides/01-the-cycle.md)

## Context

An agent has a known bias: generating the implementation and the tests in one block, then making everything pass. That is test-after in disguise, even though a test suite exists at the end of it — and the cycle in [guides/01-the-cycle.md](../guides/01-the-cycle.md) exists precisely to prevent it. The question this decision resolves: why spell out the cycle as an explicit, checkable sequence (write one test, run it, verify *why* it fails, only then write code) instead of trusting a general instruction like "use TDD"?

## Arguments For

- Left to a general instruction, an agent's default is to produce the implementation and its tests together in the same generation pass, then iterate until everything is green. The artifact looks identical to real TDD — test file plus passing suite — so a reviewer scanning the diff cannot tell the difference from the result alone.
- That failure mode is invisible from the outside; only enforcing the *sequence* — a test observed red before the corresponding code exists — catches it, which is why the rule is a step-by-step cycle and not a one-line reminder.
- The explicit checkpoint "check that it fails for the right reason" closes a further, agent-specific gap: a test that merely fails on an import error or a compilation error would still look "red" to a pass that is only chasing the shortcut, without ever exercising the invariant it claims to test.

## Arguments Against

- The step-by-step framing adds ceremony an experienced human developer doesn't need — it is written for the weaker default (the agent's), and can read as pedantic when applied to human-authored changes.
- The rule is easier to state than to verify mechanically: nothing today stops an agent from generating implementation and tests together and simply narrating the steps in the right order afterward. The rule depends on the agent actually running the red before writing the code, not on reporting that it did.

## Verdict

The cycle in [guides/01-the-cycle.md](../guides/01-the-cycle.md) is written as an explicit, checkable sequence — red, run it, verify why it fails; green, minimum; refactor — specifically because "do TDD" as a general instruction regresses to test-after under an agent's default behavior. The cost (ceremony, imperfect enforceability) is accepted because the alternative is a rule that looks followed and isn't.
