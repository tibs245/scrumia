# Project Layout

> The `features/` tree: what goes where, what may depend on what, and where shared state lives.

## Prerequisites

None — structural, read anytime; not sequenced with the other guides.

## Rules

### Rule 1: By feature, not by kind

`features/checkout/` holds its components, its primitives, its tests — not `components/`, `hooks/`, `utils/` bins sorted by file type.

#### Correct (reference tree)

```
web/
├── src/
│   ├── app.tsx                  # shell: providers, router — no logic
│   ├── routes/                  # thin route components: layout + composition
│   │   └── checkout.tsx
│   ├── features/                # by feature, not by kind
│   │   └── checkout/
│   │       ├── CartSummary.tsx
│   │       ├── CartSummary.test.tsx   # test next to the component
│   │       ├── usePricing.ts          # feature-local primitive
│   │       └── api.ts                 # the feature's data access — the only fetch site
│   ├── primitives/              # cross-feature primitives, one per file
│   │   └── createDebounced.ts
│   ├── components/              # cross-feature dumb UI (Button, Dialog) — no data access
│   └── lib/                     # framework-free helpers (pure functions)
└── e2e/                         # Playwright journeys — outside the fast loop
```

---

### Rule 2: Dependencies flow one way

`components/` and `lib/` import nothing from `features/`. A feature may import another feature's **api contract**, never its components' internals. `routes/` composes features and owns no state.

---

### Rule 3: Reusable primitives live in `primitives/`, one per file, documented by their test

Cross-feature primitives belong here; a primitive used by a single feature stays feature-local (see the tree above, `usePricing.ts`).

---

### Rule 4: Stores for shared nested state, signals for the rest — global state is a decision, not a default

Global state must be justified by two unrelated consumers, and it lives in a named module — not scattered across files. Context used as a global variable rather than as scoped injection is the same mistake with an extra layer of indirection.

---

> These rules are structural defaults; `.scrumia/impl/scrumia-impl-solidjs.md`, if present, may record a project's exceptions (see the skill's [Project override](../SKILL.md#project-override) section).
