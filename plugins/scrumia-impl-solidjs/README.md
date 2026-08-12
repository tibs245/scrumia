# scrumia-impl-solidjs

The implementation slot for SolidJS: fine-grained reactivity without the reflexes that
defeat it, behaviour-first component tests, feature-based structure. Plugs in app by app.

## What it answers

How SolidJS gets written in an app that plugs this module in — components and props,
derivations, control flow, the data boundary, project layout, testing — as six guides read
on demand, plus the refusals a reviewer checks a PR against.

## What it refuses

- No destructured props — it breaks the reactivity a signal depends on.
- No `createEffect` used as a derivation where `createMemo` already says what it means.
- No early return placed before the JSX it guards.
- No `<For>` where `<Index>` is what the list actually needs, or the reverse.

Each is a decision record (`D-01` through `D-04`), because the difference from a
component model like React's is exactly where a habit brought over from it breaks.

## What it ships

| Skill | Role |
|---|---|
| `scrumia-solidjs` | The reference — six guides and the four refusals above. Load before writing code in an app that extends this module. |
| `scrumia-solidjs-audit` | Measures the gap between an existing SolidJS app and these rules, eight passes from broken reactivity through test coverage. Reports; fixes nothing itself. |

## Settings it reads

Under `settings.implementation.scrumia-impl-solidjs` in `.scrumia/config.yaml`:
`test_runner`, `e2e`, `coverage_threshold`, `strict_mode`.

## What it expects to find

An app that lists `scrumia-impl-solidjs` in its own `extends`; within it, `src/**/*.ts`
and `src/**/*.tsx` are what the guides apply to. An optional
`.scrumia/impl/scrumia-impl-solidjs.md` records a project's house exceptions without
forking the module.

## Decisions

Four, `D-01` through `D-04` — one per refusal above, for a reviewer who wants the
reasoning rather than just the rule.
