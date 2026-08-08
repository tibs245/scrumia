# D-01: Refuse destructured props

**Status**: Adopted
**Date**: 2026-08-07
**Impacts**: [guides/01-components-and-props.md](../guides/01-components-and-props.md)

## Context

SolidJS components run **once**. After the initial render, only reactive expressions (things read inside JSX, `createMemo`, `createEffect`, …) re-run. `props` is a reactive object: reading `props.amount` inside a tracked expression keeps it wired to future updates.

```tsx
const { amount } = props   // reads once, at component creation
```

Destructuring reads the value at that single instant and assigns it to a plain variable. Nothing re-runs when the prop changes afterward — the component silently stops tracking it. This is the first bug every developer coming from React writes, because destructuring props is idiomatic there and inert here.

## Arguments For

- **The failure is silent, not loud.** No error, no warning — the UI just stops updating on that one prop. A rule that prevents the mistake beats one that relies on catching it in review or in a non-interactive test.
- **The fix costs nothing.** `props.amount` is exactly as readable as `amount`; there is no ergonomic case for the risk.
- **`mergeProps`/`splitProps` cover the two real reasons to destructure** (defaults, grouping) without breaking reactivity — so the refusal loses no capability.
- **It compounds.** Once a codebase accepts destructured props "for simple cases," every review has to re-litigate which cases are simple enough — an unconditional rule removes the judgment call.

## Arguments Against (trade-offs accepted)

- Destructuring is the familiar idiom for developers arriving from React; banning it outright adds early friction.
- For a prop that is genuinely static for the component's lifetime, the risk is theoretical.
- A linter (`eslint-plugin-solid`) could catch this instead of a written rule — tooling over convention.

## Verdict

Refuse destructuring unconditionally. The failure mode (silent, only visible on the first update after mount) is exactly the kind a static rule should prevent rather than let a linter or a bug report catch later — and linting is a defense-in-depth, not a replacement for the rule itself, since not every project runs the plugin. Use `props.name`, or `splitProps`/`mergeProps` when defaults or grouping are needed.
