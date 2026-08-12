# scrumia-practice-tdd

The practices slot for test-driven development, operationalized for an agent rather than
assumed as a habit: the red-green-refactor cycle, the mock boundary, and the link from an
acceptance criterion to the test that proves it. Applies app by app, with or without an
implementation module.

## What it answers

Whether a change actually has a test that could have failed, and where TDD legitimately
stops — exploratory spikes, trivial glue code, visual styling — versus where skipping the
red test is the defect this module exists to catch.

## What it refuses

- No production code without a red test written first. This is the founding refusal, not
  a guideline — an agent's bias is toward writing implementation and tests together and
  narrating the order afterward, which is exactly what the cycle is spelled out to
  prevent.
- No test that cannot fail. `scrumia-tdd-audit`'s catalog of useless tests names the
  pattern; a PR reviewer checks against the same catalog.
- No exemption claimed after the fact. A path excluded from TDD is declared at the moment
  it is taken, not argued for once the audit finds it.

## What it ships

| Skill | Role |
|---|---|
| `scrumia-tdd` | The reference — the cycle, the mock boundary, the AC → test mapping, where TDD stops. Load before writing code in an app that extends this module. |
| `scrumia-tdd-audit` | Measures an app's test safety net: holes, useless tests, a mutation probe, AC coverage, the mock boundary, mechanical health. Observes only. |
| `scrumia-tdd-refactor` | Puts an existing area under characterization tests before touching it, then refactors in small green steps. |

## Settings it reads

Under `settings.practices.scrumia-practice-tdd` in `.scrumia/config.yaml`: `ac_mapping`
(`strict`, enforced at commit, or `loose`, checked at PR) and `exempt_paths`.

## What it expects to find

An app that lists `scrumia-practice-tdd` in its own `extends`. A specs module writing
`AC-n` criteria sharpens the AC-mapping guide; without one, it draws invariants from the
raw request instead. An optional `.scrumia/practices/scrumia-practice-tdd.md` records
house exceptions without forking the module.

## Decisions

Two: why red comes before green rather than "every line has a test," and why the cycle is
spelled out as an explicit checkable sequence instead of a general instruction to use TDD.
