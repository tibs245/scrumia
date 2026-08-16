---
name: zod-audit
description: Audit a codebase's runtime validation against the three Zod rules this module ships — schemas duplicated as hand-written types, user-facing boundaries with no field-targeted errors, and parses on internal values. Use it before adopting the module on an existing codebase, when a validation bug ships, or to check a trust boundary is actually validated.
---

# Auditing runtime validation

Three questions, one per rule. Answer them in order — the first two are read from
the files, the third starts from a script and ends in judgment. Report findings;
change nothing without being asked.

Every rule this module ships is written against **Zod v4**. Establish the target's
major version first, from its `package.json`:

```bash
grep -m1 '"zod"' package.json
```

On **v3**, stop and say so. The error API is different — `errorMap`,
`invalid_type_error`, `required_error` and a bare `message` param are v3 names
that v4 replaced with `error` — so question 2 would report the whole codebase as
non-conformant. Report the version gap as the finding, and ask whether the
project intends to migrate or wants the rules refreshed for v3.

## 1 — Is any inferred type declared twice?

Rule: [`schema-as-source-of-truth`](../../rules/schema-as-source-of-truth.md).

Find schemas and the types beside them:

```bash
grep -rn "z\.object(" --include=*.ts --include=*.tsx src | head -50
```

For each, look in the same file for an `interface` or `type` enumerating the same
keys. A file with a `z.object` and no `z.infer` anywhere is the strongest signal —
the shape is being consumed as some other type.

**A finding is a twin, not a coincidence.** Before reporting, check the three
cases the rule exempts: a narrowing derived from the inferred type, a type with no
schema at all, and a third-party interface the schema is written to satisfy. The
third is the one that reads exactly like the bug — if the file imports the type
from a dependency, it is not a finding.

## 2 — Do user-facing boundaries carry field-targeted errors?

Rule: [`errors-carry-a-message`](../../rules/errors-carry-a-message.md).

This question is only asked of schemas a **human reads the failure of**: form
submissions, query strings a page renders from, API responses a UI turns into a
message. A schema on an internal path is out of scope, and reporting it is the
false positive that makes an audit ignorable.

Establish the global fallback first, because it answers the question for the
whole codebase at once:

```bash
grep -rn "z\.config(" --include=*.ts src
```

A `customError` or a configured locale is a legitimate way to satisfy the rule.
Where there is none, check each user-facing schema for an `error` param on the
schema or its checks. Then check the read side: a handler iterating
`error.issues` by hand to build a per-field map is re-implementing
`z.flattenError()` / `z.treeifyError()`, and that is a finding of its own.

## 3 — Is validation at the boundary, or everywhere?

Rule: [`validation-at-boundary`](../../rules/validation-at-boundary.md).

Start from the detector:

```bash
${CLAUDE_SKILL_DIR}/../../scripts/detect-boundaries.sh --json src
```

It reports every `.parse` / `.safeParse` with a verdict of `boundary` or
`internal-suspect`, and exits `3` when at least one looks internal (`0` clean,
`1` tool failure, `2` bad usage).

**The verdict is a heuristic and every finding carries `"heuristic": true`.** The
script reads text, not data flow: a parse whose value crossed a boundary through
a helper in another file reads as `internal-suspect` and is not a finding. So
`internal-suspect` is where the audit starts reading, not what it reports.

For each one, answer from the code: **where did this value come from?** Trace the
argument back. If it was constructed in this module by typed code, it is a
finding. If it arrived from network, file, user input, a queue, `process.env`, or
across a published surface this codebase does not control, it is correct and the
detector was wrong.

Report each surviving finding in the script's own words — *this call appears to
be internal; verify before removing it* — never as a certainty.

Then run the question the detector cannot ask: **is there a boundary with no
parse at all?** Grep the boundary markers and look for the ones no schema
follows. A missing parse is a worse defect than a redundant one, and it is
invisible to a tool that starts from parse calls.

## Reporting

One finding per line: the file, the line, the rule's name, and one line of what
was not met. Separate what the tool decided from what you read — a reader has to
be able to tell a heuristic from a judgment, because they act on them
differently.

Close with the count of boundaries carrying no validation at all. That number is
the one the other three questions do not cover, and usually the one worth acting
on first.
