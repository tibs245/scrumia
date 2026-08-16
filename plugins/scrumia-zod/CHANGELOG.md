# Changelog — scrumia-zod

All notable changes to this module, on [Keep a Changelog 1.0.0](https://keepachangelog.com/en/1.0.0/).

## [0.1.0] - 2026-08-14
### Added
- The module, carrying the `runtime-validation` capability: three refusal rules
  contributed to the `implement` and `review` registers.
- `schema-as-source-of-truth` — the TypeScript type is derived with `z.infer`,
  never hand-written beside the schema it restates, with `z.input`/`z.output`
  for the transform case.
- `validation-at-boundary` — the four seams that count as a trust boundary, why
  an internal parse costs a deep clone without buying a guarantee, and when
  `.parse` or `.safeParse` is the right one.
- `errors-carry-a-message` — the Zod v4 `error` param, its precedence chain, and
  `z.flattenError` / `z.treeifyError` for getting messages back out per field.
- `zod-audit` — a skill auditing an existing codebase against the three rules,
  which establishes the target's Zod major version before reporting anything.
- `scripts/detect-boundaries.sh` — classifies each `.parse` / `.safeParse` as
  boundary-crossing or internal, exiting `3` on a suspect call. The verdict is
  heuristic and every finding says so.
- Rules are written against **Zod v4** and cite `https://zod.dev/llms.txt`. On a
  v3 codebase the audit reports the version gap rather than the findings: v4
  replaced `errorMap`, `invalid_type_error`, `required_error` and the bare
  `message` param with a single `error` param.
