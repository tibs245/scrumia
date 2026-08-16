# Tech — HTML, CSS and accessibility

## How the plugin composes

`scrumia-html-css` ships as a plugin with an `extends.json` that contributes
to two registers:

| Register | Module that opens it | Where the contribution lives |
|---|---|---|
| `implement` | `scrumia-github-project` (`scrumia-ticket`) | `extends.json#implements` |
| `review` | `scrumia-github-project` (`scrumia-review`) | `extends.json#reviews` |

Each contribution carries:

- a `name` (one of `semantic-over-aria`, `element-follows-purpose`,
  `tests-query-by-role`),
- a `type` (`refusal` for `implement` and `review`),
- a `required: false` — the contribution is opt-in through the project's
  composition, not enforced by being on disk,
- a `one_liner` describing what the refusal catches,
- a `fragment` pointing at the rule's prose inside the plugin
  (`rules/<rule-name>.md`).

## Conditional contributions

The vitest advice (`tests-query-by-role`) is a conditional contribution: it
activates only when the plugin's runtime detector finds `vitest` in the
project's `package.json` and at least one `*.test.ts(x)` file in the source
tree. The detector is a shell script the plugin publishes under `bin/`,
which the contribution's metadata names. When the detector returns false,
the contribution contributes nothing — `scrumia-extends`'s table omits the
row.

The other two rules are unconditional.

## Where the rules live

The plugin's refusal rules are short, single-concern Markdown files inside
`plugins/scrumia-html-css/rules/`:

```
plugins/scrumia-html-css/
├── .claude-plugin/
│   └── plugin.json
├── README.md
├── bin/
│   └── detect-vitest.sh   # the conditional detector
├── rules/
│   ├── semantic-over-aria.md
│   ├── element-follows-purpose.md
│   └── tests-query-by-role.md
├── skills/
│   └── html-css-audit/
│       └── SKILL.md
├── extends.json
├── marketplace.json       # if the plugin is published externally
└── CHANGELOG.md
```

Each rule file is one paragraph: the rule, the source URL, the licence line.
The audit skill reads the file and reports the rule's name against a target.

## Sources, version, and freshness

The plugin's README names each source URL and the licence that applies. The
plugin does not pin source content — MDN and W3C pages evolve, and a
snapshot would drift. What is pinned is the **principle** each rule enforces:
"semantic element beats ARIA role when both express the same intent" is a
principle MDN and WAI-ARIA agree on across versions. A rule that depends on
a specific MDN example would be a different rule, written differently.

A rule whose source URL has rotted (a 404, a redirect to unrelated content)
is a finding against the plugin, reported by the audit skill. The fix is to
rewrite the rule's principle in terms of sources that still resolve — not to
remove the rule, which would leave the contribution without a citation.
