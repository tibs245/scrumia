# scrumia-impl-reactjs

The implementation slot for React 19: Server Components by default, Actions and
`useActionState` for mutations and forms, derived state calculated during render,
behaviour-first component tests, feature-based structure. Plugs in app by app.

## What it answers

How React 19 gets written in an app that plugs this module in — components and props,
state and derivations, control flow, the data boundary, project layout, testing — as six
guides read on demand, plus the refusals a reviewer checks a PR against.

## What it refuses

- No `useEffect` for state that can be calculated during render — effects belong to the
  *because the component is displayed* case, not to derivation.
- No imperative DOM escape hatch (`element.style = …`, `document.querySelector` for what
  React already renders) — React owns the DOM, the component owns its render.
- No effect where an event handler answers the same question — effects synchronise with
  display, handlers respond to interactions.
- No unnecessary `"use client"` — every added one ships its dependency tree to the
  browser, which is a cost paid on every request, not a free annotation.

Each is a decision record (`D-01` through `D-04`), because React 19's whole point is the
exact opposite of the reflex a habit would bring.

## What it ships

| Skill | Role |
|---|---|
| `scrumia-reactjs` | The reference — six guides and the four refusals above. Load before writing code in an app that extends this module. |
| `scrumia-reactjs-audit` | Measures the gap between an existing React 19 app and these rules, seven passes from wrong client/server boundaries through project layout. Reports; fixes nothing itself. |

## Settings it reads

Under `settings.implementation.scrumia-impl-reactjs` in `.scrumia/config.yaml`:
`test_runner`, `e2e`, `coverage_threshold`, `react_compiler`.

## What it expects to find

An app that lists `scrumia-impl-reactjs` in its own `extends`; within it, `src/**/*.tsx`
and `src/**/*.ts` are what the guides apply to. An optional
`.scrumia/impl/scrumia-impl-reactjs.md` records a project's house exceptions without
forking the module.

## Decisions

Four, `D-01` through `D-04` — one per refusal above, for a reviewer who wants the
reasoning rather than just the rule. Each cites the React 19 docs passage it rests on.
