---
name: scrumia-tdd
description: The ScrumIA TDD reference — the red-green-refactor cycle operationalized for an agent, the mock boundary, the acceptance criterion → test link. Load it before writing code in an app where the TDD practice is plugged in.
---

# Coding in TDD

**Not one line of production code without a red test that justifies it.**

This practice refines one point of the implementation contract: **how we test**. It applies to apps that declare it in `.scrumia/config.yaml` (`apps[].practices`), with or without an implementation module. When an implementation module is plugged in, it situates this practice for its stack — its tooling takes precedence over the generic examples here.

## The contract

- Red, green, refactor, repeat — never skip running the red, it is the only step that cannot be faked → [guides/01-the-cycle.md](guides/01-the-cycle.md), founding rule in [D-01](decisions/D-01-no-code-without-red-test.md), agent-specific rationale in [D-02](decisions/D-02-agent-bias.md)
- We simulate what we don't own; we never simulate our own modules → [guides/02-mock-boundary.md](guides/02-mock-boundary.md)
- Every acceptance criterion in scope becomes at least one test, link kept visible → [guides/03-ac-mapping.md](guides/03-ac-mapping.md)
- The practice stops at the spike, at declarative configuration, at visual styling — declared the moment the exception is taken, never after → [guides/04-where-tdd-stops.md](guides/04-where-tdd-stops.md)
- Seven test patterns that pass the suite and protect nothing → [guides/05-useless-tests-catalog.md](guides/05-useless-tests-catalog.md)

## Guides

| File | Use when you need to... |
|------|--------------------------|
| [01-the-cycle](guides/01-the-cycle.md) | Run red-green-refactor on a ticket, as an agent |
| [02-mock-boundary](guides/02-mock-boundary.md) | Decide what a test may simulate and what it must not |
| [03-ac-mapping](guides/03-ac-mapping.md) | Turn acceptance criteria (or a raw request) into a test list; configure `ac_mapping` / `exempt_paths` |
| [04-where-tdd-stops](guides/04-where-tdd-stops.md) | Recognize a legitimate exemption before writing untested code |
| [05-useless-tests-catalog](guides/05-useless-tests-catalog.md) | Recognize a test that will never protect anything |

## Routing table

```
"I need to implement a ticket in TDD"
  → 01-the-cycle + 03-ac-mapping

"I need to decide whether to mock a dependency"
  → 02-mock-boundary (assumes 01)

"I have no formal acceptance criteria to test against"
  → 03-ac-mapping

"I'm about to skip a test for a spike / config / styling change"
  → 04-where-tdd-stops (assumes 01)

"I want to check whether an existing test is worth keeping"
  → 05-useless-tests-catalog
```

## Dependencies between guides

```
01-the-cycle             ← foundation, no dependencies
02-mock-boundary         ← requires 01 (mocking decisions happen inside the cycle's green step)
03-ac-mapping            ← requires 01 (feeds the "next invariant" of the cycle's red step)
04-where-tdd-stops       ← requires 01 (an exemption is a deliberate exit from the cycle)
05-useless-tests-catalog ← independent — a checklist usable standalone, also used by scrumia-tdd-audit
```

## Decisions

| ADR | Decision | Related guide |
|-----|----------|---------------|
| [D-01](decisions/D-01-no-code-without-red-test.md) | The founding rule: no production code without a preceding red test | 01-the-cycle |
| [D-02](decisions/D-02-agent-bias.md) | Why the cycle is stated this hard for an agent | 01-the-cycle |

## Project override

If `.scrumia/practices/scrumia-practice-tdd.md` exists, its content takes precedence over this skill. A project records its house exceptions there without forking the module.

## The module's two other skills

- `scrumia-tdd-audit` — assess the real state of an app's test safety net.
- `scrumia-tdd-refactor` — put an area under test before modifying it.

## Scoping

This module applies to the apps that declare `scrumia-practice-tdd` in `.scrumia/config.yaml` (`apps[].practices`) — TDD scoping is by app, not by file pattern. Within an app, [`section.json`](section.json) globs (`**/*` by default) pick which files the guides apply to; the only per-path carve-out is `exempt_paths` under `settings.practices.scrumia-practice-tdd` (see [guides/03-ac-mapping.md](guides/03-ac-mapping.md)), honored before any guide in this module applies.
