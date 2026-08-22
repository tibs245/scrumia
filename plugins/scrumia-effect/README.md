# scrumia-effect

The typed-effect discipline for any app that produces, transforms, or consumes a side effect — describe before execute, failure as a value, the effect boundary, and which approach to reach for when a single one will not do. Library-agnostic on the pattern: a project using only `Result` reads no rule that requires knowing what an `Either` is, and a project on `effect.website` reads the discipline the same way. `effect.website` is cited as the reference implementation, not wrapped.

## What it answers

When does a function return a value rather than throw one, and where does the seam between "description" and "execution" sit in a codebase that uses more than one of `Result`, `Either`, `IO`/suspend, or `effect.website`? The discipline answers for any choice of approach; the four approach sections are layered on top, not substitutes — a rule on `Either` migration is not a rule that applies to a `Result`-only project, and "service-locator avoided" applies at discipline level only, never as a reason to know what a `Layer` is.

## What it refuses

- No effect discipline without a named approach. Every rule's first line names which one it informs — `Result`, `Either`, `IO`/suspend, effect.website, or discipline-level — so a reader can tell in one line whether the rule applies to what they use.
- No substitution of approaches. A `Result` is not "an `Either` that throws away the left"; an `IO` is not "a `suspend` that wraps a value"; the four are layered, and the discipline is the layer they sit on top of.
- No wrapping of effect.website. The reference is cited by URL; this module ships no client of that library, and a project that adopts `effect.website` directly receives the discipline from this module and the API from that one.
- No throwing for recoverable failures. A function that catches a not-found, a validation failure, a conflict, or a timeout and continues does not know what is true if the function threw — the value path is the only path that carries enough information to continue.
- No retry as a try/catch loop at the call site. Retry is data on the failure — `Retry-After`, attempt count, backoff hint — composed as a function on the effect, not as control flow around the call.
- No service-locator at the effect boundary. Environments and layers (where they apply) replace constructor-injected dependencies; discipline-level, this is "the call site does not reach for the dependency it needs."

## What it ships

| Skill | Role |
|---|---|
| `scrumia-effect` | The reference — the discipline section (typed effects, describe-before-execute, effect boundary, service-locator avoided), then the four approach sections (`Result`, `Either`, `IO`/suspend, effect.website) layered on top, plus error semantics and retry as data. Load before writing or reviewing code that produces, transforms, or consumes a side effect in an app where this module is plugged in. |

| Guide | Read it when |
|---|---|
| `guides/01-typed-effects.md` | Deciding whether a value is an effect or a description of one |
| `guides/02-describe-before-execute.md` | Splitting what an effect is from when it runs |
| `guides/03-effect-boundary.md` | Locating the seam where the description hands off to execution |
| `guides/04-service-locator-avoided.md` | Justifying the discipline's "no reach for the dependency" stance |
| `guides/05-result.md` | Choosing `Result` and knowing when to migrate to `Either` |
| `guides/06-either.md` | The `Either<L, R>` convention — left for failure, right for success |
| `guides/07-io-suspend.md` | The description/execution split as a discipline; `suspend` is named, not defined |
| `guides/08-effect-website.md` | When to reach for the reference implementation, and what it adds over the discipline |
| `guides/09-when-to-throw.md` | The recoverable / unrecoverable test for whether a function returns or throws |
| `guides/10-retry-as-data.md` | Carrying retry metadata on the failure and composing retry as a function on the effect |

## Settings it reads

None. The module ships a discipline; the libraries that implement each approach (`Arrow`, `kotlin.Result`, `kotlinx.coroutines`, effect.website) carry their own configuration.

## What it expects to find

An app that produces, transforms, or consumes a side effect — which is most of them. The discipline applies regardless of which of the four approaches the app uses, and is silent on apps that do not produce one. A project adopting `scrumia-kotlin` alongside this module finds `suspend` named, not defined, in the IO/suspend guide; rules on `suspend`'s behaviour belong to `scrumia-kotlin`. A project adopting `scrumia-ktor` finds HTTP-status-as-effect ruled there, not here.

## Decisions

Two: why the discipline is split from the four approaches rather than absorbed into them, and why retry is composed as a function on the effect rather than as a try/catch loop at the call site.

## Not shipped yet

No `scrumia-effect-audit`. The discipline is read by an agent when it implements or reviews, not measured against a codebase — there is no static shape that distinguishes a function that returns a `Result` from one that throws, and the audit a static check could perform is the false positive the module refuses to ship. A human reading the rules against an existing codebase is the audit this module owes.
