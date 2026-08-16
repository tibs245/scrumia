# Tech — Compound components

## How the plugin composes

`scrumia-compound-design` ships as a plugin with an `extends.json` that
contributes to one register:

| Register | Module that opens it | Where the contribution lives |
|---|---|---|
| `implement` | `scrumia-github-project` (`scrumia-ticket`) | `extends.json#implements` |

The plugin does **not** contribute to `review`. A compound component's
review is the same review any component passes — props shape, accessibility,
performance — and adding it to `review` would duplicate what an
implementation module's own rules already cover. The choice is documented
in `business.md` § *What the plugin contributes*.

The scope is broad: any implementation module whose framework supports
context or its equivalent. A project running `scrumia-impl-reactjs` and
`scrumia-impl-solidjs` together gets the same contribution shape twice,
with the framework's idiom in each.

Each contribution carries:

- a `name` (one of `children-reach-parent-through-context`,
  `sub-components-co-located`, `compound-consumed-as-unit`),
- a `type` (`refusal`),
- a `required: false`,
- a `one_liner`,
- a `fragment` pointing at the rule's prose inside the plugin.

## Where the rules and docs live

```
plugins/scrumia-compound-design/
├── .claude-plugin/
│   └── plugin.json
├── README.md
├── docs/
│   ├── react.md
│   ├── vue.md
│   ├── solid.md
│   ├── angular.md
│   └── principle.md
├── rules/
│   ├── children-reach-parent-through-context.md
│   ├── sub-components-co-located.md
│   └── compound-consumed-as-unit.md
├── skills/
│   └── compound-audit/
│       └── SKILL.md
├── extends.json
└── CHANGELOG.md
```

The four framework docs state the same principle in each framework's
idiom — React's `createContext`, Vue's `provide`/`inject`, Solid's
context, Angular's service or `inject()`. The audit skill reads the
framework of the file under review and applies the matching rule phrasing.

## Detecting context use

The `children-reach-parent-through-context` rule needs to know whether a
prop chain of three or more is justified. The plugin ships a detector that
traces the value's path from its definition to its use:

- crosses a `Provider` boundary (React), a `provide()` call (Vue), or
  equivalent → the chain is justified, no finding,
- otherwise, three or more levels → finding.

The detector is heuristic and the audit reports it as such. A compound
component that legitimately crosses three prop levels for reasons the
heuristic misses is reviewed manually.

## Sources, no version

The plugin's README cites `https://www.patterns.dev/react/compound-pattern/`
without a version pin — the principle has been stable since the pattern's
first documentation, and the source URL is the only thing that needs to
resolve. A 404 on the source URL is a finding; a reworded principle is
the fix.
