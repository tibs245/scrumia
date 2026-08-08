---
name: scrumia-tdd-refactor
description: Puts an existing code area under test before modifying it — characterization tests, golden master, then refactoring in small green steps. Use it to resolve a finding from scrumia-tdd-audit or before touching code with no safety net.
---

# Put under test, then refactor

We do not refactor code without a safety net. This skill builds the safety net first, on **observed** behavior — not desired behavior.

## The two-hats rule

At any moment, you wear only one of the two:

- **Tests hat** — you add tests, you don't touch production code.
- **Refactor hat** — you move structure under a green suite, you change no behavior.

Changing a behavior (fixing a bug, adding a case) is neither: it is ordinary TDD, in a separate change, **after** the refactor — the cycle in [`scrumia-tdd`, guides/01-the-cycle.md](${CLAUDE_SKILL_DIR}/../scrumia-tdd/guides/01-the-cycle.md).

## Step 1 — Characterize

Write tests that pin down what the code **does**, including its quirks:

1. Identify the significant inputs: nominal, edges, error cases — read the existing call sites to know what really flows through.
2. For each input, write a test whose assertion is the *current* output. If you can't predict it, run and freeze what you observe.
3. **An observed behavior that looks like a bug gets noted, not fixed**: a `CHARACTERIZATION: probable bug, see <issue>` comment on the test, and an issue if the tracker module is plugged in — otherwise a list at the end of the output.

When the output is large (a generated file, a complete response), a *golden master* is acceptable **here** — it is the exception to the anti-snapshot rule ([`scrumia-tdd`, guides/05-useless-tests-catalog.md, Rule 4](${CLAUDE_SKILL_DIR}/../scrumia-tdd/guides/05-useless-tests-catalog.md)), temporary by nature: it will be replaced by targeted assertions as the refactor clarifies what matters.

## Step 2 — Cut dependencies to the strict minimum

If the area can't be tested without network, clock or database: introduce the **minimal seam** — one extra parameter, an injected value. Nothing else. No general interface, no restructuring: it's the refactor that's coming, not its preparation swelling up.

Each seam is itself a micro-refactor: green suite before, green suite after.

## Step 3 — Refactor in small steps

Under the green safety net:

- One move at a time — extract, rename, relocate, never two at once.
- Suite re-run at every step. A step that goes red gets **undone** (`git checkout`), it does not get fixed forward.
- Frequent commits if the user wants them; otherwise, announced checkpoints.

The refactor stops when the original finding is resolved. What you notice along the way becomes an issue, not one more step — a refactor that overflows is exactly as dangerous as a PR that overflows.

## Step 4 — Settle up

1. Replace the golden master with targeted assertions where the refactor clarified the structure.
2. The bugs noted in step 1: list them with their issue. Fixing them is ordinary TDD, one per change ([`scrumia-tdd`, guides/01-the-cycle.md](${CLAUDE_SKILL_DIR}/../scrumia-tdd/guides/01-the-cycle.md)).
3. Report back: what is now under the safety net, what still isn't, and why.

## What you don't do

- No refactor and fix in the same change — the suite cannot tell which of the two it is validating.
- No "while I'm at it".
- No deleting a characterization test that goes red: it just paid you back.
