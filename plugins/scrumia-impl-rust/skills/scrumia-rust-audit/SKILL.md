---
name: scrumia-rust-audit
description: Measures the gap between an existing Rust app and the scrumia-impl-rust rules — unwrap in production, untyped errors, traits without polymorphism, unjustified unsafe. Use it before plugging the module into an existing app, or to check that a well-kept app stays that way.
---

# Auditing a Rust app

An audit records findings, it does not fix. The deliverable is a list of situated findings that the user turns into tickets. This skill serves two moments: **before plugging** the module into existing code (measuring the step), and **as routine** (checking that the step does not re-form).

The audited rules are those of the `scrumia-rust` skill (`${CLAUDE_SKILL_DIR}/../scrumia-rust/SKILL.md`); the project override (`.scrumia/overrides/scrumia-impl-rust.md`) may exempt some — read it first, an exempted gap is not a finding.

## The passes, from mechanical to structural

### 1. Panics in waiting

Enforces [D-01](${CLAUDE_SKILL_DIR}/../scrumia-rust/decisions/D-01-no-unwrap-expect.md), mechanized in [05-lints](${CLAUDE_SKILL_DIR}/../scrumia-rust/guides/05-lints.md).

```bash
grep -rn '\.unwrap()\|\.expect(' src/ crates/ --include='*.rs' | grep -v '#\[cfg(test)\]'
```

The grep overestimates (it does not see `mod tests`): check each hit before turning it into a finding. Classify: `unwrap` on the nominal path (blocking), `expect` without an invariant message (to fix), documented `expect("invariant: …")` (compliant, don't report).

### 2. Errors that leak

Enforces [03-errors](${CLAUDE_SKILL_DIR}/../scrumia-rust/guides/03-errors.md).

- Public signatures returning `Box<dyn Error>`, `String`, or a dependency's raw error (`sqlx::Error`, `reqwest::Error`) outside the layer that owns it.
- Layers without their own error enum — the app's error vocabulary tells its structure; so does its absence.

### 3. Indirections without polymorphism

Enforces [D-03](${CLAUDE_SKILL_DIR}/../scrumia-rust/decisions/D-03-no-single-implementer-traits.md), detailed in [02-domain-types](${CLAUDE_SKILL_DIR}/../scrumia-rust/guides/02-domain-types.md).

For each `trait` the app defines: count its `impl`s. A single implementer and no test usage at an infrastructure boundary → over-abstraction finding, recommendation: inline. This finding is of equal gravity to the others — dead indirection costs at every read.

### 4. Ownership fought against

Enforces [D-02](${CLAUDE_SKILL_DIR}/../scrumia-rust/decisions/D-02-no-clone-to-appease-borrowck.md).

`.clone()` density per module — three clones in the same place signal an ownership structure to rethink, not a style to fix line by line. Also look for `Rc<RefCell<…>>` outside the cases where shared mutability is the intended semantics.

### 5. `unsafe` and the reprieves

Enforces [05-lints](${CLAUDE_SKILL_DIR}/../scrumia-rust/guides/05-lints.md).

- Every `unsafe` block without an adjacent `// SAFETY:` comment: blocking.
- Every `#[allow(…)]`: dated and justified, or a finding. `cargo clippy` with the module's config (see [05-lints](${CLAUDE_SKILL_DIR}/../scrumia-rust/guides/05-lints.md)) lists what the `allow`s are masking.

### 6. Types that assert nothing

Enforces [02-domain-types](${CLAUDE_SKILL_DIR}/../scrumia-rust/guides/02-domain-types.md), and [D-04](${CLAUDE_SKILL_DIR}/../scrumia-rust/decisions/D-04-no-deref-inheritance.md) for `Deref`-as-inheritance specifically.

The signs of representable invalid states: two booleans encoding one state, a `String` crossing three layers while carrying an invariant ("necessarily a valid email here"), the same fact re-validated at every floor. For each case: which newtype or which enum would eliminate it.

### 7. Tests, form and substance

Enforces [04-testing](${CLAUDE_SKILL_DIR}/../scrumia-rust/guides/04-testing.md).

- Integration tests importing private items, tests named `test_<function>` rather than by invariant, central invariants without a test.
- If the project writes acceptance criteria: `AC-n`s with no test citing them.
- If `scrumia-tdd` is plugged into the app, its audit (`scrumia-tdd-audit`) is the authority on the suite's value — propose it instead of duplicating its passes here.

## The deliverable

One table per pass: finding, file:line, severity (`blocking` / `to fix` / `worth knowing`), remedy in one sentence. Then the synthesis: the state of the app in one sentence, the three most profitable findings, and — if the audit precedes plugging in the module — what must be resolved before plugging in, what can wait.

Rewrite nothing without agreement.
