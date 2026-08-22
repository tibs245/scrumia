---
name: scrumia-functional-programming
description: The ScrumIA Functional Programming paradigm — purity, total functions, referential transparency, immutability, composition over inheritance, and effect discipline, all in language-neutral terms so the same wording holds in Kotlin, JavaScript, Rust and any language that supports them. Load it before writing code in an app that extends this module.
---

# Coding in Functional Programming

**A paradigm stated in language-neutral terms so the same rule holds across languages.**

This module is paradigm-level, not technology-level: the principles hold with the same wording in Kotlin, JavaScript, Rust, Scala, F#, Haskell, Swift — and any language that supports them. The cited languages are not exhaustive; the principle is paradigm-wide. Each rule carries a `Verified in:` footer naming at least two of those languages — the smallest count that catches both directions of failure (wrote this thinking of one language only; copied verbatim from a foreign ecosystem without translating).

A rule that can only be stated in one language's terms is misplaced: the language-specific rule belongs to that language's module, not here. The CI gate (`bin/scrumia-functional-programming-check-vocabulary`) greps each rule fragment for syntax tokens of one language, skips `README.md` and `Verified in:` lines, and exits non-zero when a token slips in. The drift is caught before review spends the time to notice it.

## The contract

- **Purity** — a function's result depends only on its arguments; what happens at the impure boundary is named where it is. → [rules/purity.md](rules/purity.md)
- **Total functions** — every input maps to an output; failure is a value the signature carries, not a throw the runtime raises. → [rules/total-functions.md](rules/total-functions.md)
- **Referential transparency** — an expression is replaceable by its value without changing the program's behaviour; any expression that fails this is the leak to find. → [rules/referential-transparency.md](rules/referential-transparency.md)
- **Immutability by default** — a value mutates only when an equivalent immutable value would have written more; the line where mutation becomes acceptable is drawn before the code is. → [rules/immutability.md](rules/immutability.md)
- **Composition over inheritance** — inheritance is not the default reuse mechanism; typeclasses, extension functions and function composition are the smaller, more local choice when they fit. → [rules/composition-over-inheritance.md](rules/composition-over-inheritance.md)
- **Effect discipline** — an effect is described as a value the program composes, executed at the boundary; collapsing description and execution is the over-application this rule catches. → [rules/effect-discipline.md](rules/effect-discipline.md)

## Rules

| File | Use when you need to... |
|------|--------------------------|
| [purity](rules/purity.md) | Decide whether a function is pure, and what the impure boundary looks like in this program |
| [total-functions](rules/total-functions.md) | Model a function whose inputs may not all admit an output, and choose the failure value the signature carries |
| [referential-transparency](rules/referential-transparency.md) | Find the expression whose substitution would change the program's behaviour |
| [immutability](rules/immutability.md) | Decide whether a value should be mutable, and where the boundary to mutation lives |
| [composition-over-inheritance](rules/composition-over-inheritance.md) | Choose between an inheritance relation and a composition — typeclass, extension function, function composition |
| [effect-discipline](rules/effect-discipline.md) | Separate the description of an effect from its execution, even when the language has no first-class effect type |
| [misplaced-rule](rules/misplaced-rule.md) | Recognise a rule that has drifted into one language's terms and propose its move |

## Routing table

```
"I need to decide whether a function is pure"
  → purity

"I need to handle a function whose input may not admit an output"
  → total-functions

"I need to find a non-replaceable expression"
  → referential-transparency

"I need to decide whether a value should be mutable"
  → immutability

"I need to choose between inheritance and composition"
  → composition-over-inheritance

"I need to separate description from execution"
  → effect-discipline

"A rule feels like it belongs to one language's syntax, not to the paradigm"
  → misplaced-rule
```

## Dependencies between rules

```
purity                       ← foundation, no dependencies
total-functions              ← requires purity (a total function is pure; partiality is what totality forbids)
referential-transparency     ← requires purity (a non-pure expression is not referentially transparent)
immutability                 ← independent — also used by referential-transparency's reasoning
composition-over-inheritance ← independent — names a default, not a sequence
effect-discipline            ← requires purity (an effect described is still a value; collapsing it is the impurity this rule catches)
misplaced-rule               ← independent — the meta-rule that names a drift into one language
```

## Project override

If `.scrumia/overrides/scrumia-functional-programming.md` exists, its content takes precedence over this skill. A project records its house exceptions there without forking the module.

## Scoping

This module applies to the apps that list `scrumia-functional-programming` in their own `extends` in `.scrumia/config.yaml` — paradigm scoping is by app, not by file pattern. The module activates alone: a project declaring it and no other Functional-Programming-adjacent module receives the full paradigm rule set on `implement`, `review` and `find-spec`. A language-specific module extends, never replaces: its rules are the language-specific reading of the same paradigm principles.
