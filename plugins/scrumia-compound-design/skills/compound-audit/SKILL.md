---
name: compound-audit
description: Audit a component library against the compound component pattern — does the parent own its parts? Are the parts co-located? Is the public API one symbol? Catches prop-drilling, scattered sub-components, and a compound consumed as a constellation.
---

# Compound component audit

Take stock of an existing component library against the three refusals the plugin carries. The audit reads the parent, the parts, and the public surface; what it returns is the same shape the implementation module's own audit returns, one finding per rule broken.

## When to load

When a component library exists and the question is "is this composed correctly?" — not "is this code correct?" The audit answers the first; the second is the implementation module's job.

## What to read

1. The library's entry point — what it exports, what is `index.ts` re-exporting, what is reachable from `import { … } from 'lib'`. One file, the shape of the public surface.
2. One parent and its parts. The smallest compound in the library is enough; the question is the same shape.
3. The library's `package.json` if the framework is React, Vue, Solid or Angular. The audit's per-framework checks are gated on which one it is — a Vue component is not subject to the React-shaped rules.

## What to refuse

For each rule, one finding or zero. Findings name the file, the rule (`compound-components/BR-N`), and one line of what was not met.

### Rule 1 — children-reach-parent-through-context

A child whose parent state passes through three or more prop levels. Two is fine; the threshold is the third. The first two levels are usually a parent's own composition — `<Tabs>` passing `value` to `<Tabs.List>` is internal. The third is the consumer-implied shape: `<Tabs.List>` passing `value` to `<Tabs.Trigger>`. Context (or `provide`/`inject`, or signals, or a service) is the medium for that reach.

The detector traces the value's path: if it crosses a `<Context.Provider>` (React), a `provide()` call (Vue), a Solid `<Context.Provider>`, or an Angular injection token, the chain is justified. Otherwise, three or more levels is a finding.

### Rule 2 — sub-components-co-located

A part exported from a separate file, a separate directory, or a separate `index.ts` from the parent. The audit checks the library's public surface: `import { Tabs, Tab } from 'lib'` is a finding; `import { Tabs } from 'lib'; <Tabs.Tab />` is not. Two exports where one should be reachable is the failure the rule catches.

### Rule 3 — compound-consumed-as-unit

A part the consumer reaches for by name, with the parent passed in as a prop. `<Tab items={…} value={…} onSelect={…} parent={Tabs} />` reads the part as a standalone — the parent is no longer the unit. The audit catches the case where the part's API mirrors the parent's: `<Tab>` taking `value`, `onSelect`, and `activeId` is the parent leaking through a back door.

## What to report

A finding carries the file, the rule, and one line of what was not met. The shape mirrors `scrumia-module check --json`: same envelope, same state values. The audit does not write — fix what it finds, then re-run.

```json
{
  "ok": true,
  "state": "clean" | "findings",
  "module": "scrumia-compound-design",
  "findings": [
    { "module": "scrumia-compound-design",
      "file": "components/Tabs.tsx",
      "rule": "compound-components/BR-2",
      "message": "Tab exported alongside Tabs — the parts should travel with the parent" }
  ]
}
```

## Source

The single authority for this pattern is [patterns.dev — Compound Pattern](https://www.patterns.dev/react/compound-pattern/). The three rules this audit enforces are statements of that page's principle; a 404 on the URL is a finding, and a reworded principle is the fix.