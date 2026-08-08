---
name: scrumia-design-system
description: The ScrumIA design-system reference — where identity, tokens and components live, and how to consult them before writing an interface. Load it before creating or modifying a component, a style, or anything a user will look at.
---

# The design system

Load this before writing an interface, not after. The point of a design system is to answer questions you would otherwise answer by inventing: which blue, how much space, does this already exist.

An interface written without consulting it is not wrong on any single line. It drifts — and drift is only visible once it is expensive to undo.

## Composition block

This module's contract with the rest of ScrumIA. `scrumia-init` copies this block verbatim into `CLAUDE.md`'s `## Design contract` section, between the `scrumia:start` markers. Consumers (the implementation modules, `scrumia-ticket`, the team agents) read it from there instead of hard-coding this module's paths; a module replacing this one at the `design` slot must ship its own block in the same shape.

```
design_root: design/
identity_file: identity.md
tokens_file: tokens.css
components_dir: components/
component_preview: preview.html
component_spec: spec.md
card_marker: @dsCard
remote: claude-design
```

`remote: claude-design` tells a consumer that this system has an upstream it can be reviewed in — see [scrumia-design-sync](../scrumia-design-sync/SKILL.md). A project that never syncs sets it to `none`; everything else in this skill still applies, because the local tree is the source of truth either way.

## What lives where

```
design/
├── identity.md              # the intent — what this product should feel like
├── tokens.css               # the vocabulary — custom properties, nothing else
└── components/
    └── <name>/
        ├── preview.html     # every variant, rendered, standalone
        └── spec.md          # when to use it, when not to, what it refuses
```

Three files, three different jobs, and they fail differently. `identity.md` going stale makes the system arbitrary. `tokens.css` going stale makes it a lie. A component without `spec.md` gets used for the wrong thing and grows a fourth variant.

### `identity.md`

Prose, not values. What the product should make someone feel, what it must never look like, and the two or three decisions everything else follows from. It is the file you point at when someone asks "why cyan" — and the file to rewrite when the answer stops being true.

Keep it short enough to read before every design decision. If nobody reads it, it isn't an identity, it's an archive.

### `tokens.css`

Custom properties only — no selectors, no components. A token is a **decision with a name**: `--accent`, `--space-4`, `--radius-card`. A value that appears once is not a token; a value that appears three times and hasn't got one is a bug waiting for a fifth appearance.

Themes are token redefinitions, never separate stylesheets. A component that needs to know which theme is active has been written wrong.

### `components/<name>/`

`preview.html` renders every variant standalone — that is what makes review possible, locally and upstream alike. Its first line carries the card marker so the Design System pane can group it:

```html
<!-- @dsCard group="Actions" -->
```

`spec.md` states when to reach for the component, when not to, and what it refuses to do. The refusal is the useful half: "this button does not carry a destructive action, use `button-danger`" prevents the variant that would otherwise be added next week.

## Before writing a component

Four questions, in this order. Stopping at the first "yes" is the point.

1. **Does it already exist?** Read `components/`. A component under a different name is still the same component.
2. **Is it a variant of something that exists?** Then it belongs in that component's `preview.html` and `spec.md`, not in a new directory.
3. **Do the tokens cover it?** Every color, spacing, radius, duration comes from `tokens.css`. If one doesn't exist, that is a finding — see below.
4. **What does it refuse?** Write that down in `spec.md` while you still know. You will not remember at the fourth variant.

## When a token is missing

Do not inline the value. That is the single rule this module exists to enforce, and inlining is how every design system dies — not by a bad decision, but by a hundred reasonable exceptions.

Two legitimate outcomes:

- **The system must grow.** The need is real and recurring: add the token, name it for its job (`--surface-raised`, not `--blue-800`), and say so in the PR. A token added deliberately is the system working.
- **The component is asking wrong.** Far more common. A need for a color that fits nowhere usually means the component is doing something the identity never planned for. Reconsider the component before growing the vocabulary.

Escalate to `scrumia-designer` when you cannot tell which of the two it is. That ambiguity is exactly the role's job.

## With the implementation modules

The implementation module owns **how the component is written** — its file layout, its props, its tests. This module owns **what it looks like**. They meet at the styling layer and do not overlap: a SolidJS component and a Rust-served template consume the same tokens.

Where they appear to disagree, they are answering different questions — re-read which one. A genuine conflict (the implementation module mandates a styling approach that cannot read `tokens.css`) is a composition problem, not a judgment call: escalate it.

A project override in `.scrumia/design/` wins over this module, as everywhere else in ScrumIA.

## The other skills

| You want to | Skill |
|---|---|
| Install the design tree in a project | [scrumia-design-setup](../scrumia-design-setup/SKILL.md) |
| Push or pull components to `claude.ai/design` | [scrumia-design-sync](../scrumia-design-sync/SKILL.md) |
| Measure an existing interface against the system | [scrumia-design-audit](../scrumia-design-audit/SKILL.md) |
