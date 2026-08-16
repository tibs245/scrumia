# Compound components

**Status**: draft

## In brief

The compound component pattern, framework-agnostic. A parent exposes its
parts through a single API, children reach the parent through context (or the
framework's equivalent), and sub-components are co-located rather than
scattered. The plugin that carries it (`scrumia-compound-design`) is written
to apply across React, Vue, Solid and Angular — the principle is the same,
the mechanism differs. Authoritative source:
`https://www.patterns.dev/react/compound-pattern/`.

## Links

- Implemented by: `plugins/scrumia-compound-design/` — `extends.json`
  contributes refusal rules to the `implement` register only, scoped to
  any implementation module whose framework supports context or its
  equivalent.
- Authority: `https://www.patterns.dev/react/compound-pattern/` — the
  plugin's README cites it and the documentation covers React, Vue, Solid
  and Angular side by side rather than translating the React example alone.
- Defers to: `features/business/modular-composition/` for the rules every
  module owes to compose. The framework-agnostic claim is a contribution
  shape, not an exception to those rules.

## Files present

| File | Read it when |
|---|---|
| `business.md` | deciding what the pattern refuses, what it requires, and which framework mechanisms it accepts as context equivalents |
| `qa.md` | writing or running the acceptance scenarios for the pattern rules |
| `tech.md` | tracing how the plugin contributes to the `implement` register |
| `CHANGELOG.md` | history of changes to this spec |

No `ux.md`, `legal.md`, `security.md`: a composition pattern carries no
interface, no personal data, and no privileged surface of its own.
