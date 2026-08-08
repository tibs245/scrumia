---
name: scrumia-solidjs-audit
description: Measures the gap between an existing SolidJS app and scrumia-impl-solidjs rules — destructured props, effects used as derivations, components that fetch, structure by kind. Use it before plugging the module into an existing app, or to check that an app stays on the rails.
---

# Auditing a SolidJS app

An audit states findings, it doesn't fix. The output is a list of situated findings the user turns into tickets. It serves two moments: **before plugging** the module into existing code (measure the step), and **routinely** (check the step isn't re-forming).

The audited rules are those of the `scrumia-solidjs` skill (`${CLAUDE_SKILL_DIR}/../scrumia-solidjs/SKILL.md`); the project override (`.scrumia/impl/scrumia-impl-solidjs.md`) may exempt some — read it first, an exempted gap is not a finding.

## The passes, mechanical to structural

### 1. Broken reactivity

Enforces [D-01](${CLAUDE_SKILL_DIR}/../scrumia-solidjs/decisions/D-01-no-destructured-props.md), mechanized in [01-components-and-props](${CLAUDE_SKILL_DIR}/../scrumia-solidjs/guides/01-components-and-props.md).

```bash
grep -rn 'const {.*} = props\|const {.*} = mergeProps' src/ --include='*.tsx'
```

Every destructured props is a finding (blocking — it fails silently). Then look for early returns before JSX in components (`if (...) return <` outside JSX) — same class of bug, enforced by [D-03](${CLAUDE_SKILL_DIR}/../scrumia-solidjs/decisions/D-03-no-early-returns-before-jsx.md), [03-control-flow](${CLAUDE_SKILL_DIR}/../scrumia-solidjs/guides/03-control-flow.md).

### 2. Effects that derive

Enforces [D-02](${CLAUDE_SKILL_DIR}/../scrumia-solidjs/decisions/D-02-no-createeffect-as-derivation.md), detailed in [02-derivations](${CLAUDE_SKILL_DIR}/../scrumia-solidjs/guides/02-derivations.md).

Every `createEffect` whose body calls a signal setter is a derivation in disguise: finding, remedy `createMemo`. Count the remaining `createEffect`s — each should name an outside-world target (DOM, storage, analytics). One that doesn't is suspect.

### 3. React reflexes

Enforces [02-derivations](${CLAUDE_SKILL_DIR}/../scrumia-solidjs/guides/02-derivations.md), Rule 1.

Imported memoisation habits: `createMemo` wrapping trivial property reads, dependency-array patterns rebuilt by hand, state lifted "to force a refresh", `untrack` used to silence a loop instead of fixing the flow. Each finding names the Solid idiom that replaces it.

### 4. Components that fetch

Enforces [04-data-boundary](${CLAUDE_SKILL_DIR}/../scrumia-solidjs/guides/04-data-boundary.md), Rule 1.

`fetch(`, axios or client SDK imports inside `.tsx` component files: blocking finding — the component can't be tested without a server. Remedy: move to the feature's `api.ts`, reach it through `createResource`.

### 5. Structure

Enforces [05-project-layout](${CLAUDE_SKILL_DIR}/../scrumia-solidjs/guides/05-project-layout.md).

- Folders by kind (`components/`, `hooks/`, `utils/` as the primary layout) instead of by feature — one finding for the layout, not one per file.
- Route components carrying business logic (guide's Rule 2, shared with [04-data-boundary](${CLAUDE_SKILL_DIR}/../scrumia-solidjs/guides/04-data-boundary.md)).
- Cross-feature imports that bypass the api contract (feature A importing feature B's component internals).

### 6. State ownership

Enforces [01-components-and-props](${CLAUDE_SKILL_DIR}/../scrumia-solidjs/guides/01-components-and-props.md), Rule 3 (duplicated state) and [05-project-layout](${CLAUDE_SKILL_DIR}/../scrumia-solidjs/guides/05-project-layout.md), Rule 4 (default global state).

- Props copied into local signals (two sources of truth).
- Stores or context used as default global state — for each, name the two unrelated consumers that would justify it, or the finding stands.

### 7. Lists and keys

Enforces [D-04](${CLAUDE_SKILL_DIR}/../scrumia-solidjs/decisions/D-04-for-vs-index.md), [03-control-flow](${CLAUDE_SKILL_DIR}/../scrumia-solidjs/guides/03-control-flow.md).

`<For>` over primitives, `<Index>` over objects — check the hot lists first (the ones that update on user input).

### 8. Tests, shape and substance

Enforces [06-testing](${CLAUDE_SKILL_DIR}/../scrumia-solidjs/guides/06-testing.md).

- Tests reading signals directly instead of asserting rendered output.
- Components with behaviour and no test; primitives without their unit test.
- If the project writes acceptance criteria: `AC-n` without a citing test.
- If the TDD practice is plugged into this app, its audit (`scrumia-tdd-audit`) owns the suite-value passes — offer it instead of duplicating them here.

## The output

One table per pass: finding, file:line, severity (`blocking` / `to fix` / `to know`), one-sentence remedy. Then the summary: the app's state in one sentence, the three most profitable findings, and — if the audit precedes plugging the module — what must be resolved before plugging, what can wait.

Rewrite nothing without agreement.
