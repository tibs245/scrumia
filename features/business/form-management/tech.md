# Tech — Form management

## How the plugin composes

`scrumia-rhf` ships as a plugin with an `extends.json` that contributes to
two registers, scoped to React only:

| Register | Module that opens it | Where the contribution lives |
|---|---|---|
| `implement` | `scrumia-github-project` (`scrumia-ticket`) | `extends.json#implements` |
| `review` | `scrumia-github-project` (`scrumia-review`) | `extends.json#reviews` |

The scope is `scrumia-impl-reactjs` only. A project running
`scrumia-impl-solidjs` (and no React impl) pays no cost — the
contributions are filtered out by the composition's per-module scope, and
`scrumia-extends`'s table omits the rows.

Each contribution carries:

- a `name` (one of `form-has-resolver`, `inputs-are-registered`,
  `state-through-library`),
- a `type` (`refusal`),
- a `required: false`,
- a `one_liner`,
- a `fragment` pointing at the rule's prose inside the plugin.

## Where the rules live

```
plugins/scrumia-rhf/
├── .claude-plugin/
│   └── plugin.json
├── README.md
├── rules/
│   ├── form-has-resolver.md
│   ├── inputs-are-registered.md
│   └── state-through-library.md
├── skills/
│   └── rhf-audit/
│       └── SKILL.md
├── extends.json
└── CHANGELOG.md
```

## Detecting the registration shape

The `inputs-are-registered` rule needs to distinguish an input that could
have used `register` from one that genuinely needs control. The plugin
ships a detector that classifies an `<input>` or `<select>` JSX element:

- managed by the library: spread of `register()` result (`{...register("name")}`),
  inside a `<Controller>`,
- managed by the developer: paired with `useState` + `onChange` to the same
  field, with no library call,
- genuinely controlled: takes a `value` from a non-form source (a value
  computed elsewhere that the form receives, an editor with rich internal
  state).

The third case is reported by the audit as "review manually" rather than
as a refusal — the rule's principle applies to the second case, and a
false positive on the third is more expensive than a manual review on it.

## Versioning

The plugin's README cites `https://react-hook-form.com` and pins the major
version. React Hook Form's API moves between majors (`useForm` signature,
`Controller` props, `formState` keys). A rule written for v6 against a v7
codebase raises false positives. The pin is the statement the rules are
current as of that version.

## Pairs with

The plugin does not depend on `scrumia-zod`. The resolver pattern works
with any adapter `@hookform/resolvers` ships. The pairing with Zod is
documented in `runtime-validation/business.md` § *Pairs with* and is the
one a project adopting both will reach for first.
