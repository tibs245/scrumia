---
name: scrumia-specs-find
description: Navigates a project's specs — finds the feature that owns a rule, traces dependencies between features, or loads the minimal context useful to a ticket. Use it before implementing or reviewing, rather than reading all of features/.
---

# Navigating the specs

The targeted-files format is only worth anything if you read little. This skill finds the useful minimum and stops there.

## The rule that governs everything

**Load as little as possible, in order from most general to most specific, and stop as soon as you know enough.**

Reading all of `features/` cancels the entire benefit of the splitting. If you catch yourself doing it, the question asked is too vague: rephrase it before reading.

## Finding the feature that owns a rule

1. Read the global index first — the file named by the contract's `global_index` key, at the root of `specs_root` (`features/index.md` in this project). One line per feature: stratum, status, brief. It narrows the search before any per-feature file is opened.
2. `grep` on the `index.md` files of the candidates it surfaces — they carry the summary, so most searches resolve there.
3. If nothing comes up, widen to `business.md`.
4. Only as a last resort, search all files.

If the global index is missing, fall back to walking the tree from step 2 and report the gap — it is generated state, and its absence is worth flagging rather than silently working around.

When several features seem to own the same rule, that's a signal to report back: a business rule should have only one authority. Report it rather than picking the most plausible one.

## Loading a ticket's context

In this order, stopping as soon as possible:

1. The `index.md` of the feature it's attached to — it says which files exist and why
2. Its `qa.md` — the criteria to satisfy
3. Its `business.md` if the ticket touches a rule
4. Its `api-contract.md` and `tech.md` if the ticket touches an interface or a technical choice
5. The parent Business feature, if the ticket concerns an App feature and the rule is at stake

The other files are only read if the `index.md` indicates they are relevant. That is exactly the role of its "why this file exists" column.

## Tracing dependencies

The links are declared in the `index.md` files. For a given feature:

- **Upward** — its parent Business feature
- **Downward** — the App features that implement it
- **Lateral** — the App features it consumes (frontend → backend)

A declared link to a nonexistent feature is a defect to report; a real link that isn't declared is one too, and it's harder to spot. When you find that a feature consumes another without declaring it, say so.

## What deserves reporting along the way

Without launching an audit — just what you come across while searching:

- An App feature with no Business parent and no explicit justification
- Two features that define the same rule differently
- An `index.md` that lists absent files, or omits some
- A `draft` feature referenced by an active ticket

Report, don't fix. An unrequested correction in a spec is a behavior change in disguise.
