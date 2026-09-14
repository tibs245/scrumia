# scrumia-tdd

Test-driven development, operationalized for an agent rather than
assumed as a habit: the red-green-refactor cycle, the mock boundary, and the link from an
acceptance criterion to the test that proves it. Applies app by app, with or without an
implementation module.

## What it answers

Whether a change actually has a test that could have failed, at which of the three levels
it belongs — unit, integration, end-to-end, decided by what a test needs to run rather
than by what it is about — and where TDD legitimately stops: exploratory spikes, trivial
glue code, visual styling, versus where skipping the red test is the defect this module
exists to catch.

## What it refuses

- No production code without a red test written first. This is the founding refusal, not
  a guideline — an agent's bias is toward writing implementation and tests together and
  narrating the order afterward, which is exactly what the cycle is spelled out to
  prevent.
- No test that cannot fail. `scrumia-tdd-audit`'s catalog of useless tests names the
  pattern; a PR reviewer checks against the same catalog.
- No exemption claimed after the fact. A path excluded from TDD is declared at the moment
  it is taken, not argued for once the audit finds it — and end-to-end automation a
  project defers is declared up front and dated, on the same terms.
- No coverage threshold. The audit reports coverage per level and as a union because that
  is the cheapest map of what no level reaches; nothing in this module blocks on the
  number.

## What it ships

| Skill | Role |
|---|---|
| `scrumia-tdd` | The reference — the cycle, the mock boundary, the three test levels, the AC → test mapping, where TDD stops. Load before writing code in an app that extends this module. |
| `scrumia-tdd-audit` | Measures an app's test safety net: holes, useless and misclassified tests, a mutation probe, AC coverage, the mock boundary, mechanical health, coverage per level and as a union. Observes only. |
| `scrumia-tdd-refactor` | Puts an existing area under characterization tests before touching it, then refactors in small green steps. |

## Settings it reads

Under this module's own `params:` in `.scrumia/config.yaml`: `ac_mapping`
(`strict`, enforced at commit, or `loose`, checked at PR), `exempt_paths`, `levels`
(the project's own command for each of the three levels, and the shared resource the
integration suite takes) and `impact` (which integration tests a changed path reaches).
The commands are the project's: this module ships none, so a stack's test command is
never hard-coded here.

## What it expects to find

An app that lists `scrumia-tdd` in its own `extends`. A specs module writing
`AC-n` criteria sharpens the AC-mapping guide; without one, it draws invariants from the
raw request instead. An optional `.scrumia/overrides/scrumia-tdd.md` records
house exceptions without forking the module.

## Decisions

Two: why red comes before green rather than "every line has a test," and why the cycle is
spelled out as an explicit checkable sequence instead of a general instruction to use TDD.
