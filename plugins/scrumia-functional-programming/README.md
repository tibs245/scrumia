# scrumia-functional-programming

The Functional Programming paradigm, stated in language-neutral terms so the same wording holds in Kotlin, JavaScript, Rust, Scala, F#, Haskell and Swift — and any language that supports them. The cited languages are not exhaustive; the principle is paradigm-wide. A project on any of them can activate this module alone, and the rules below apply without naming a type or a syntax keyword from any one of them.

## What it answers

Whether a piece of code is shaped by the discipline Functional Programming holds itself to — what purity, totality, referential transparency, immutability, composition over inheritance, and effect discipline look like at the rule level — across stacks, not for one of them. A reviewer asks the same question on a Kotlin module, a TypeScript module, and a Rust crate, and the answer comes from the same table.

## What it refuses

- **Impurity smuggled past the boundary** — a function whose result depends on something outside its arguments, or whose evaluation changes something outside its return value, where the boundary is not named. The rule is language-neutral; the boundary is whatever the program's architecture calls the place where impurity must live.
- **Partial functions** — a function whose signature accepts an input for which it cannot produce an output, and signals that fact by terminating the program. Failure is a value, not an exception, and a partial function is what an absent failure value looks like.
- **Non-replaceable expressions** — an expression whose value depends on something its syntactic form does not name, so the substitution `expr = value` would change the program's behaviour. That is a referential-transparency violation, and it is the property a program loses first.
- **Default mutation** — a value that mutates when an equivalent immutable value would have read the same and written less. Mutation has a place; defaulting to it is the over-application this module audits for.
- **Inheritance as the primary reuse mechanism** — reaching for an inheritance relation where composition — typeclasses, extension functions, function composition, algebraic structure — would have read as the smaller, more local choice. The rule is not "never inherit"; it is "do not reach for inheritance first".
- **Effect description and execution collapsed** — a program whose effects are described at the moment they run rather than as values the program composes before execution. Languages without first-class effects still describe and execute at different moments; collapsing the two is what effect discipline forbids.

A rule that can only be stated in one language's terms is misplaced: the language-specific rule belongs to that language's module. The CI gate (`bin/scrumia-functional-programming-check-vocabulary`) greps each rule fragment for syntax tokens and exits non-zero when one slips in, so the drift is caught before review spends the time to notice it. Every rule carries a `Verified in:` footer naming at least two cited languages — the two smallest count that catches both directions of failure (wrote this thinking of one language; copied verbatim from a foreign ecosystem).

## What it ships

| Skill | Role |
|---|---|
| `scrumia-functional-programming` | The reference — six principles, one file per principle, each stated in language-neutral terms with a `Verified in:` footer. Load before writing code in an app that extends this module. |

The vocabulary gate is a shell script the plugin publishes under `bin/`; the CI calls it through `tools/validate.py`, which scans `plugins/*/bin/*` to discover it. The script greps the plugin's own rule fragments for syntax tokens of a single language, skips `README.md` and `Verified in:` lines, and exits non-zero with a one-line message naming each occurrence. A passing CI run is the textual enforcement of BR-17.

## Settings it reads

None. The module is paradigm-level and reads no configuration: the rules are the rules, and a project that needs a house exception records it under `.scrumia/overrides/scrumia-functional-programming.md`.

## What it expects to find

An app that lists `scrumia-functional-programming` in its own `extends`. The module activates alone: no companion module is required for the rules to land. A project on Kotlin, JavaScript, Rust, Scala, F#, Haskell or Swift — or any other language the rules apply to — receives the full paradigm rule set on `implement`, `review` and `find-spec` from this module alone. A language-specific module (`scrumia-kotlin`, `scrumia-impl-reactjs`, `scrumia-impl-rust`, …) extends, never replaces: its rules are the language-specific reading of the same paradigm principles, and a rule that belongs there does not belong here.

## Decisions

- The module contributes to `implement`, `review` and `find-spec` — never to `audit`. An audit is the same review against the same rules, and contributing to both would be the same contribution under two names. Recorded in BR-9: a contribution names no consumer.
- The `Verified in:` footer is named (not only applied) in each rule's preamble. A footer the reader does not see is a footer the contributor can forget, and a forgotten footer is the language-only drift the gate exists to catch.
