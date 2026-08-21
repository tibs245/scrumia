---
name: rhf-audit
description: Audits a React app against the scrumia-rhf rules — a form declares a resolver, its inputs are registered through React Hook Form, and its state is read through the library's API rather than the DOM. Use before adopting the plugin into an existing app, or routinely to catch a mixed-paradigm form.
---

# Auditing React Hook Form usage

The audit states findings, it does not fix. The output is a list of
situated findings the user turns into tickets. It serves two moments:
**before adopting** the plugin into an existing codebase (measure
the step), and **routinely** (check the step is not re-forming).

The audited rules are the three refusals in
[`${CLAUDE_SKILL_DIR}/../../rules/`](${CLAUDE_SKILL_DIR}/../../rules/):

- [form-has-resolver](${CLAUDE_SKILL_DIR}/../../rules/form-has-resolver.md)
- [inputs-are-registered](${CLAUDE_SKILL_DIR}/../../rules/inputs-are-registered.md)
- [state-through-library](${CLAUDE_SKILL_DIR}/../../rules/state-through-library.md)

The authority is `https://react-hook-form.com` — pinned to the
major version the rules were written against (see the README). A
rule whose citation has drifted from the pinned version is rewritten;
a rule the documentation no longer states is removed, not paraphrased.

## The passes

### 1. Resolver coverage

Enforces [form-has-resolver](${CLAUDE_SKILL_DIR}/../../rules/form-has-resolver.md).

Every React component that calls `useForm` must pass a `resolver` as
its second argument. The audit classifies each `useForm` call:

```bash
grep -rn 'useForm(' src/ --include='*.tsx' --include='*.ts'
```

A `useForm()` call with no second argument is a finding. A
`useForm({ defaultValues })` with no resolver is also a finding —
`defaultValues` are not validation. A `useForm({ resolver })` is
clean; `useForm({ resolver, defaultValues, mode })` is clean.

A `Resolver` import from `@hookform/resolvers/<adapter>` in the same
file (or a hoisted one) corroborates the resolver's presence; the
audit does not require it when the resolver is inline.

### 2. Input classification

Enforces [inputs-are-registered](${CLAUDE_SKILL_DIR}/../../rules/inputs-are-registered.md).

Each `<input>`, `<select>` or `<textarea>` JSX element in a file
that calls `useForm` is classified:

- **Library-managed** — `{...register("name")}` on the element, or
  wrapped by `<Controller>`. Clean.
- **Genuinely controlled** — `value` from a non-form source (a
  prop, a value computed outside the form, an editor's internal
  state). Reported as "review manually" with the input's line; a
  reviewer who confirms the case records the exemption, and the
  audit remembers it.
- **Developer-controlled without justification** — `useState` for
  the field's name paired with `onChange` on the element, with no
  library call resolving the field. Finding.

```bash
# Pair the useState declarations with the input JSX, line by line.
grep -rn 'useState\|register(\|<Controller' src/ --include='*.tsx'
```

The audit does not chase a third-party component's internals — a
`<MyRichEditor>` whose library contract is documented is a
genuinely-controlled input regardless of its props. The check
focuses on the call site, not the component tree.

### 3. State channel

Enforces [state-through-library](${CLAUDE_SKILL_DIR}/../../rules/state-through-library.md).

A form's state must be read through the library's API. Each form
file is checked for:

```bash
grep -rn 'document\.querySelector\|formRef\.current\|FormData(' \
  src/ --include='*.tsx' --include='*.ts'
```

A hit inside a file that calls `useForm` is a finding. A hit in a
file that does not is not subject to this rule.

The audit also flags `event.target.elements` reaches inside a
`handleSubmit` handler — the handler receives validated values
already; reaching for the DOM there is the regression the rule
exists to catch.

## The output

One table per pass: finding, file:line, severity (`blocking` /
`to fix` / `to know`), one-sentence remedy. Then the summary: the
app's state in one sentence, the three most profitable findings,
and — if the audit precedes adopting the plugin — what must be
resolved before adopting, what can wait.

## What the audit is not

The audit does not enforce the form library's API choice. A team
that runs its forms through Formik, React Final Form, or a
hand-rolled context is not subject to these rules. The plugin is
scoped to `scrumia-impl-reactjs` only; an app that runs
`scrumia-impl-solidjs` (and not React) pays no cost.

A SolidJS form that follows a different paradigm is a different
problem with its own rules — see the SolidJS implementation module
if that is the stack.

## After the audit

The findings are tickets. Each blocking finding names the rule, the
file, the line, and the remedy. A team that adopts the plugin
records the audit's `genuinely-controlled` exemptions in a project
override (`.scrumia/overrides/scrumia-rhf.md`) — an exempted gap is not
a finding on the next pass.

Rewrite nothing without agreement.
