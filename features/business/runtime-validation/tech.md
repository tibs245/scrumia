# Tech — Runtime validation

## How the plugin composes

`scrumia-zod` ships as a plugin with an `extends.json` that contributes to
two registers:

| Register | Module that opens it | Where the contribution lives |
|---|---|---|
| `implement` | `scrumia-github-project` (`scrumia-ticket`) | `extends.json#implements` |
| `review` | `scrumia-github-project` (`scrumia-review`) | `extends.json#reviews` |

Each contribution carries:

- a `name` (one of `schema-as-source-of-truth`, `errors-carry-a-message`,
  `validation-at-boundary`),
- a `type` (`refusal`),
- a `required: false`,
- a `one_liner`,
- a `fragment` pointing at the rule's prose inside the plugin.

## Where the rules live

```
plugins/scrumia-zod/
├── .claude-plugin/
│   └── plugin.json
├── README.md
├── rules/
│   ├── schema-as-source-of-truth.md
│   ├── errors-carry-a-message.md
│   └── validation-at-boundary.md
├── skills/
│   └── zod-audit/
│       └── SKILL.md
├── extends.json
└── CHANGELOG.md
```

## Boundary detection

The `validation-at-boundary` rule needs to know what counts as a trust
boundary. The plugin ships a small detector (a shell script or a tree-sitter
query, depending on the project's language mix) that classifies a function
call as boundary-crossing or internal:

- boundary: HTTP client call (`fetch`, `axios`, `http.get`), file read
  (`fs.readFile`, `readFileSync`), message queue subscriber, user-input
  parser (`JSON.parse` on a request body),
- internal: any function whose argument was constructed in the same file
  or module without crossing a boundary on the way.

The detector's verdict is heuristic — it is a starting point, not a proof —
and the audit skill reports it as such: "this function appears to be
internal; verify before suppressing". A project's review accepts or rejects
the heuristic finding by hand, which is the level at which the rule
operates.

## Versioning

The plugin's README cites `https://zod.dev/llms.txt` and pins the major
version the rules were written against. A rule written for Zod v3 against
a v4 codebase raises false positives — v4's API moves in places the rules
assume. The pin is a statement the rules are current as of that version;
a project on a newer major sees the audit report the version drift and
asks the plugin to refresh.

## Pairs with

The plugin does not depend on `scrumia-rhf` and does not require it. A
project that adopts Zod without forms pays the cost of Zod alone. A
project that adopts both gets the resolver pattern documented in
`form-management/business.md` § *Pairs with*.
