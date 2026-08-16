# scrumia-compound-design

The compound component pattern, framework-agnostic. A parent exposes its parts through a single API, children reach the parent through context (or the framework's equivalent), and sub-components are co-located rather than scattered — across React, Vue, Solid and Angular, in each framework's idiom.

## What it answers

How a component library exposes a parent with parts — `<Tabs>` with `<Tabs.Tab>`, not `<Tabs>` with `<Tab items={…}>` — without leaking its internal state into every consumer's prop list. The pattern is the same in every framework; the mechanism differs. The plugin documents both.

## What it refuses

- A prop chain of three or more levels for parent state. Two is fine; three is a finding — context (or `provide`/`inject`, or signals, or a service) is the medium for parent-child state in a compound.
- Sub-components exported from a separate module path. A compound's parts travel with the parent; a `<Tab>` imported separately is a finding.
- A compound consumed as a constellation. The public API is the parent; everything else is an internal.

## What it ships

| Skill | Role |
|---|---|
| `compound-audit` | Take stock of an existing component — does it read like a compound? Are the parts co-located? Is the public API one symbol? |

| Doc | Read it when |
|---|---|
| `docs/principle.md` | Reading the principle for the first time, or explaining it in code review |
| `docs/react.md` | Translating the principle into React's `createContext` and `<Context.Provider>` |
| `docs/vue.md` | Translating the principle into Vue's `provide` / `inject` |
| `docs/solid.md` | Translating the principle into Solid's `createContext` |
| `docs/angular.md` | Translating the principle into Angular's service or `inject()` |

## Settings it reads

None. The plugin documents a pattern; the implementation modules (`scrumia-impl-reactjs`, `scrumia-impl-vue`, `scrumia-impl-solidjs`, `scrumia-impl-angular`) carry the framework-specific conventions it relies on.

## What it expects to find

A project running at least one framework module the pattern transfers to, or no framework module at all — the principle reads without a consumer, and the audit reads against the library being checked. A project running, say, `scrumia-impl-reactjs` plus a `<Tabs>` whose `<Tab>` is three prop levels deep gets the same finding shape in both rule sets: an implementation refusal and a compound refusal, side by side.

## Decisions

- The plugin contributes only to the `implement` register — never to `review`. A compound's review is the same review any component passes: props shape, accessibility, performance. Duplicating that coverage under another name would be a rule no module owes. Documented in [`features/business/compound-components/business.md`](https://github.com/tibs245/scrumia/blob/main/features/business/compound-components/business.md) § *What the plugin contributes*.
- The framework docs state the same principle in each idiom rather than translating the React example alone. A reader who already works in Vue should not have to read React to understand Vue; the four are written to be read in any order.