---
name: scrumia-rules
description: The rules-hierarchy format reference — section anatomy (index, guides, decisions, section.json), how an agent navigates it without reading everything, and when a single file is enough instead. Load it before reading or writing any module-shipped or project-local rule section.
---

# The rules-hierarchy format

A single `conventions.md` degrades the moment a topic grows past two or three concerns: an agent either reads all of it for every task, or skims and misses the part that mattered. Worse, the rules it states drift from the reasons they were adopted — nobody can tell a live rule from a stale one, or challenge it with anything but a feeling.

The hierarchy fixes both problems by splitting a topic into three kinds of file, wired by one routing table: an **index** an agent reads first and always, **guides** it loads only on demand, and **decisions** it never loads for code generation — only when a human is challenging a rule.

This module doesn't ship a topic. It ships the format itself, so any module — or any project — can adopt it consistently.

## Anatomy of a section

```
<section>/
├── 00-index.md        # routing table — read first, always
├── guides/
│   └── NN-topic.md    # one concern, correct/incorrect examples
├── decisions/
│   └── D-NN-slug.md   # Status / Date / Impacts / Context / Arguments / Verdict
├── section.json       # { "globs": [...] } — where this section applies
└── CHANGELOG.md        # one entry per evolution, owned by scrumia-rules-update
```

### `00-index.md` — the routing table

Four components, no more:

| Component | Role |
|---|---|
| Guides table | file → "use when you need to..." |
| Quoted-need routing | `"I need to X"` → the guide(s) that answer it |
| Dependency graph | which guides assume which others are already loaded |
| Decisions table | `D-NN` → decision → related guide — for humans challenging a rule, not for code generation |

Quoted-need routing, illustrated:

```
"I need to add a new field to the resource"
  → 02-shape (assumes 01)

"I need to write the validation for it"
  → 03-validation (assumes 01, 02)
```

Dependency graph, illustrated:

```
01-shape        ← foundation, no dependencies
02-fields       ← requires 01
03-validation   ← requires 01, 02
```

### `guides/NN-topic.md` — one concern

One guide answers one question. Numbered rules inside it, each with a **Correct** and an **Incorrect** example — drawn from real usage in the codebase, not invented for the occasion. It closes with a pointer to the decision behind it:

```markdown
> Decision rationale: D-02 — decisions/D-02-slug.md
```

A guide with no such pointer is an opinion wearing a rule's clothes. `scrumia-rules-update` refuses to let one stand unlinked.

### `decisions/D-NN-slug.md` — why

Fixed shape:

```markdown
**Status**: Adopted | Proposed | Superseded by D-NN
**Date**: YYYY-MM-DD
**Impacts**: guides/NN-topic.md

## Context
## Arguments For
## Arguments Against
## Verdict
## History
```

**Arguments Against is not optional.** A decision without a stated cost has not been examined — the same standard this project holds its own ADRs to (`docs/adr/`, format: Context → Decision → Consequences, "what we accept" mandatory).

### `section.json` — where it applies

```json
{ "globs": ["src/data/**"] }
```

The one mechanical link between a section and the code it governs. It lets an agent — or an implementation module — decide which sections are even worth opening for the file it's about to touch, before reading a single index.

## Where sections live

- **Module-shipped** — inside the owning module's skill directory: `plugins/<module>/skills/<skill>/sections/<topic>/`. The module ships the section the way it ships any other reference material.
- **Project-local** — `.scrumia/rules/<section>/`, `00-index.md` as its index. Created and maintained by `scrumia-rules-setup` / `scrumia-rules-update`, registered in the project's `CLAUDE.md` under `## Project rules`.

Nothing structural distinguishes the two — a project-local section is a section like any other. Only its precedence differs (below).

## How an agent navigates

The format's entire value collapses the moment an agent reads everything anyway. The rule:

1. **Read `00-index.md` first, always.** It is kept small on purpose — if it isn't, that's a defect in the section, not a reason to skip it.
2. **Match the task to the quoted-need routing table.** If nothing matches closely, pick the nearest entry and say so — don't fall back to reading every guide "to be safe"; that silently reintroduces the single-file problem this format exists to remove.
3. **Load only the guide(s) selected, then walk their declared dependencies** — a guide that "requires 01, 02" means load exactly those two as well, nothing beyond them.
4. **Decisions are not for code generation.** Open one only when a human is challenging a rule, or when `scrumia-rules-update` sends you there to evolve it.

Same principle already applied to specs navigation (`scrumia-specs-find`, if the `scrumia-specs` module is installed): load the minimum, most general to most specific, stop as soon as you know enough.

## When NOT to use the hierarchy

Below roughly **three distinct concerns**, a section is overhead: an index, a guides directory and a decisions directory, to route between two files that could sit in one. Stay single-file — one `references/conventions.md`, or a section directly in the module's `SKILL.md` — until a genuinely separable third concern shows up.

Signals it's time to split:
- The single file has grown past what an agent should load to answer an unrelated question in the same area.
- Two parts of it stop sharing vocabulary — they're answering different questions that happen to live in the same file.
- A decision inside it needs challenging on its own, independent of the rest.

Splitting early produces a routing table that routes to itself — one index, one guide, no actual routing decision to make. That cost is real; don't pay it pre-emptively.

## Precedence — specific beats generic

One rule, applied at every level a section can appear:

- **Project-local beats module-shipped** on the same concern — `.scrumia/rules/<section>/` overrides a module's `sections/<topic>/` when both exist for the same globs.
- **A more specific module beats a more generic one it situates** — an implementation module's guide wins over a practice module's generic one where they conflict, because the specific module knows the terrain the generic one can't.
- **A project override file beats both**, where a module defines one for itself (each module documents its own override path, e.g. `.scrumia/impl/<module>.md`).

No resolution mechanism decides this automatically — an agent applies the rule by inspection: is there a project-local section covering these globs? If yes, it wins outright; if no, fall through to whichever module-shipped section is more specific to the code being touched.

## The module's two other skills

- `scrumia-rules-setup` — scaffold a project-local section: interview, harvest existing conventions, write the index/guides/decisions/`section.json`, register it in `CLAUDE.md`.
- `scrumia-rules-update` — evolve a rule: locate its decision, challenge it in writing, update decision and guides together, log the change.
