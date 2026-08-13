---
name: scrumia-reactjs-audit
description: Measures the gap between an existing React 19 app and scrumia-impl-reactjs rules — wrong client/server boundaries, useEffect for derived state, imperative DOM, components that fetch directly instead of going through the data boundary. Use it before plugging the module into an existing app, or to check that an app stays on the rails.
---

# Auditing a React 19 app

An audit states findings, it doesn't fix. The output is a list of situated findings the
user turns into tickets. It serves two moments: **before plugging** the module into
existing code (measure the step), and **routinely** (check the step isn't re-forming).

The audited rules are those of the `scrumia-reactjs` skill
(`${CLAUDE_SKILL_DIR}/../scrumia-reactjs/SKILL.md`); the project override
(`.scrumia/impl/scrumia-impl-reactjs.md`) may exempt some — read it first, an exempted
gap is not a finding.

## The passes, mechanical to structural

### 1. Wrong client/server boundaries

Enforces [D-04](${CLAUDE_SKILL_DIR}/../scrumia-reactjs/decisions/D-04-no-unnecessary-client-components.md),
detailed in [01-components-and-props](${CLAUDE_SKILL_DIR}/../scrumia-reactjs/guides/01-components-and-props.md)
and [05-project-layout](${CLAUDE_SKILL_DIR}/../scrumia-reactjs/guides/05-project-layout.md).

```bash
grep -rln "^'use client'\|\"use client\"" src/ --include='*.tsx' --include='*.ts'
```

For every `'use client'` directive, read the file and check whether it actually uses a
Hook the server cannot run, an event handler, or a client-only API. Markings without
one of these reasons are findings — the directive ships the module's transitive imports
to the browser for nothing. Then check the layout files in particular: a layout
carrying `'use client'` is the worst case and is a blocking finding by itself. Remedy:
remove the directive, push interactivity into a leaf Client Component, move data
fetching up to a Server Component.

### 2. `useEffect` for derived state

Enforces [D-01](${CLAUDE_SKILL_DIR}/../scrumia-reactjs/decisions/D-01-no-useeffect-for-derived-state.md),
detailed in [02-state-and-derivations](${CLAUDE_SKILL_DIR}/../scrumia-reactjs/guides/02-state-and-derivations.md).

For every `useEffect` whose body calls a state setter, read the body and ask whether
the value can be calculated during render. Pattern:

```bash
grep -rB2 -A6 'useEffect' src/ --include='*.tsx' --include='*.ts' \
  | grep -E 'set[A-Z][a-zA-Z]+\('
```

Effects whose bodies only mirror props or other state into local state are findings.
Remedy: calculate during render, lift the *id* not the *item*, use `key` to reset a
child whose identity prop changes, or move the work into an event handler (pass 3).

### 3. Effects where event handlers belong

Enforces [D-03](${CLAUDE_SKILL_DIR}/../scrumia-reactjs/decisions/D-03-effects-where-event-handlers-belong.md),
detailed in [02-state-and-derivations](${CLAUDE_SKILL_DIR}/../scrumia-reactjs/guides/02-state-and-derivations.md).

For every `useEffect` whose body fires a side effect (analytics, notification, mutation
of another store) on a prop or state observation, ask: *why does this code run?* If
the answer is "because the user did X", it belongs in X's event handler. The
canonical defect is a notification fired from a `useEffect` that observes
`product.isInCart` — it fires again on every remount where the cart is still populated.
Remedy: move the call into the click handler that initiated the action.

### 4. Imperative DOM

Enforces [D-02](${CLAUDE_SKILL_DIR}/../scrumia-reactjs/decisions/D-02-no-imperative-dom.md),
detailed in [01-components-and-props](${CLAUDE_SKILL_DIR}/../scrumia-reactjs/guides/01-components-and-props.md)
and [03-control-flow](${CLAUDE_SKILL_DIR}/../scrumia-reactjs/guides/03-control-flow.md).

```bash
grep -rn 'document\.\(querySelector\|getElementById\|getElementsBy\)' src/ --include='*.tsx' --include='*.ts'
grep -rn '\.style\.[a-zA-Z]\+\s*=' src/ --include='*.tsx' --include='*.ts'
```

Every hit inside a component file is a finding — React owns the DOM, and an
imperative write is overwritten by the next render. The allowed exceptions are
documented: a third-party imperative widget integration that names what it touches in
a comment, or a `ref` callback on the component itself. The presence of a
`forwardRef` import is also a finding — React 19 passes `ref` as a regular prop.

### 5. Components that fetch directly

Enforces [04-data-boundary](${CLAUDE_SKILL_DIR}/../scrumia-reactjs/guides/04-data-boundary.md),
detailed in [04-data-boundary](${CLAUDE_SKILL_DIR}/../scrumia-reactjs/guides/04-data-boundary.md).

`fetch(`, axios or client SDK imports inside a Client Component file (one with
`'use client'`), used from a `useEffect` to populate state: blocking finding — the
data could have come from a Server Component during render, or from `use(promise)`
against a Promise created at the boundary. The Effect-based fetch is invisible to
Suspense, produces a waterfall, and forces the client to ship whatever transport the
component imports.

```bash
grep -rln 'useEffect' src/ --include='*.tsx' --include='*.ts' \
  | xargs grep -lE 'fetch\(|axios|graphql'
```

Remedy: lift the fetch into a Server Component route, pass the result as a prop, or
create the Promise at the boundary and read it with `use(promise)`.

### 6. Tests, shape and substance

Enforces [06-testing](${CLAUDE_SKILL_DIR}/../scrumia-reactjs/guides/06-testing.md).

- Tests reading state directly (`useState` cell, internal hook value) instead of
  asserting on the rendered result.
- Components with behaviour and no test; primitives without their unit test.
- Importing a Server Component into a client unit test — fails at import time and
  belongs to the framework's RSC test harness.
- If the project writes acceptance criteria: `AC-n` without a citing test.
- If the TDD practice is plugged into this app, its audit (`scrumia-tdd-audit`) owns
  the suite-value passes — offer it instead of duplicating them here.

### 7. Project layout

Enforces [05-project-layout](${CLAUDE_SKILL_DIR}/../scrumia-reactjs/guides/05-project-layout.md).

- Folders by kind (`components/`, `hooks/`, `utils/` as the primary layout) instead of
  by feature — one finding for the layout, not one per file.
- A Server Component placed in `components/` rather than `app/` or the feature
  folder.
- Cross-feature imports that bypass the api contract (feature A importing feature B's
  component internals).

## The output

One table per pass: finding, file:line, severity (`blocking` / `to fix` / `to know`),
one-sentence remedy. Then the summary: the app's state in one sentence, the three most
profitable findings, and — if the audit precedes plugging the module — what must be
resolved before plugging, what can wait.

Rewrite nothing without agreement.
