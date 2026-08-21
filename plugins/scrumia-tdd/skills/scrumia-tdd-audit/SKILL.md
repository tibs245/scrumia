---
name: scrumia-tdd-audit
description: Audits an app's test safety net — unprotected areas, tests that cannot fail, uncovered acceptance criteria, real value of the suite. Use it before adopting TDD on existing code, or to verify that an app held to TDD really is.
---

# Auditing the test safety net

An audit observes, it does not fix. The output is a list of situated findings — file, pattern, severity — that the user turns into tickets or hands to `scrumia-tdd-refactor`.

## Scope

Ask which app to audit if it isn't obvious. Read its implementation module if one is plugged in (mapping in `CLAUDE.md`): it tells you where the tests live and how they are named. Without a module, deduce it from the code.

## The six passes, in order

### 1. Holes in the safety net

Production code that no test constrains. Don't trust line-by-line coverage: look for **invariants** without a test — the calculation rule, the state transition, the error case. A function covered at 100% where no test would fail if you inverted its central condition is a hole in the safety net. The invariant, not the function or the coverage number, is the unit to check for: [`scrumia-tdd`, guides/01-the-cycle.md, Rule 7](${CLAUDE_SKILL_DIR}/../scrumia-tdd/guides/01-the-cycle.md).

### 2. Tests that cannot fail

The catalog is in the module's [`guides/05-useless-tests-catalog.md`](${CLAUDE_SKILL_DIR}/../scrumia-tdd/guides/05-useless-tests-catalog.md): tautological, assertion-free, implementation mirrors, massive snapshots, timing-fragile, shared mutable state, integration disguised as unit. Count them — their proportion measures the suite's complacency.

### 3. The mutation probe

The most honest measure, in small doses. On two or three critical areas:

1. Check that the working tree is clean (`git status`) — otherwise stop right there.
2. Invert a central condition, or replace a return value.
3. Run the suite.
4. **Restore immediately** (`git checkout -- <file>`), before any other action.

If nothing goes red, the safety net has a hole at that exact spot — a finding more telling than any percentage. Never run this probe on a tree carrying uncommitted changes. It is the same check the cycle asks for on every new test — that red is real and for the right reason — run backward on existing code: [`scrumia-tdd`, guides/01-the-cycle.md, Rule 2](${CLAUDE_SKILL_DIR}/../scrumia-tdd/guides/01-the-cycle.md).

### 4. Mapping to acceptance criteria

If the project writes `AC-n`: does every criterion of shipped features have a test that cites it? List the orphans in both directions — criterion without a test, and test citing a criterion that no longer exists. Rule and settings (`ac_mapping: strict|loose`): [`scrumia-tdd`, guides/03-ac-mapping.md](${CLAUDE_SKILL_DIR}/../scrumia-tdd/guides/03-ac-mapping.md).

### 5. The mock boundary

Look for mocks of the project's own internal modules. Each one is a finding: the test verifies a conversation, and the splitting may deserve a question. Boundary rule: [`scrumia-tdd`, guides/02-mock-boundary.md](${CLAUDE_SKILL_DIR}/../scrumia-tdd/guides/02-mock-boundary.md).

### 6. Mechanical health

- Duration of the fast suite — beyond a minute, the red-green cycle no longer holds in practice.
- Disabled tests (`skip`, `ignore`, commented out): each with its age (`git log`). A disabled test that was once red and never fixed is a violation, not a finding to soften: [`scrumia-tdd`, guides/01-the-cycle.md, Rule 6](${CLAUDE_SKILL_DIR}/../scrumia-tdd/guides/01-the-cycle.md).
- Known flaky tests — look for CI re-runs if you have access.

## The output

One table per pass: finding, file, severity (`blocking` / `to fix` / `good to know`). Then three lines of synthesis: the state of the safety net in one sentence, the two riskiest areas, the first recommended action.

Rewrite nothing without agreement. If the user wants to fix things, offer `scrumia-tdd-refactor` area by area.
