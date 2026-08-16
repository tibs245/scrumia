# scrumia-zod

Runtime validation for a TypeScript codebase that touches untrusted data, built
on [Zod](https://zod.dev). The schema is the source of truth: the type is
derived from it, the error messages are part of it, and it runs where data
enters the application rather than on every call along the way.

## What it answers

Where does validation actually belong, and what does a schema owe the person who
trips it? TypeScript's guarantees stop at the trust boundary — an API response
typed `User` is `User` only because someone trusted the server. Three refusal
rules mark that seam, keep the type derived rather than duplicated, and require
that a failure a user reads names the field and what to do about it.

## What it refuses

- No TypeScript type hand-written beside the schema it restates. `z.infer` derives
  it, so a schema change reaches every consumer through the compiler.
- No `.parse()` on a value the type system already proved. Validation is the seam
  between trusted and untrusted code, not a layer applied everywhere.
- No user-facing boundary failing with `Invalid input: expected string`. At that
  boundary the message is part of the schema, and it is field-targeted.

## What it ships

| What | Role |
|---|---|
| `rules/schema-as-source-of-truth.md` | The type is derived with `z.infer`, never declared twice. |
| `rules/validation-at-boundary.md` | What a trust boundary is, and why an internal parse costs without buying. |
| `rules/errors-carry-a-message.md` | The v4 `error` param, and getting messages back out per field. |
| `zod-audit` (skill) | Three questions that find a duplicated type, an unmessaged boundary, and a redundant parse on an existing codebase. |
| `scripts/detect-boundaries.sh` | Classifies each `.parse` / `.safeParse` as boundary-crossing or internal. Heuristic, and says so. |

All three rules reach the `implement` and `review` registers through
`extends.json`, so they apply while code is written and again while it is
reviewed, without being written twice.

## Sources

| Source | Pinned to |
|---|---|
| [`https://zod.dev/llms.txt`](https://zod.dev/llms.txt) | **Zod v4** |

Every rule cites this source and nothing else — no blog post, no tutorial, no
community pattern. The pin is the contract: v4 replaced v3's `errorMap`,
`invalid_type_error`, `required_error` and bare `message` with a single `error`
param, so the rules raise false positives on a v3 codebase. `zod-audit` checks
the target's major version first and reports the drift instead of the findings.

## What it expects to find

A TypeScript codebase with Zod as a dependency. Nothing else — the rules are
about where a schema sits, not about which framework surrounds it.

The default composition is an app that also runs `scrumia-impl-reactjs` or
`scrumia-impl-solidjs`, and that scope is the consuming project's to declare in
its own app module list. Nothing in this module encodes it: a Node service, a
CLI or a server-rendered app takes the module directly, and no file here has to
change for that.

`scrumia-rhf` is not a dependency. A project that adopts both reaches the
resolver pattern; a project that adopts Zod without forms pays for Zod alone.

## Not shipped yet

No `zod-refactor`. The audit finds a duplicated type, an unmessaged boundary and
a redundant parse, and a human fixes each — there is no automated pass that
rewrites an interface into a `z.infer` or moves a parse to its boundary. The
detector is also text-based rather than a tree-sitter query: it cannot follow a
value across files, which is why its verdict is labelled heuristic everywhere it
appears. A tree-sitter implementation is the next milestone for this module, not
a maybe.
