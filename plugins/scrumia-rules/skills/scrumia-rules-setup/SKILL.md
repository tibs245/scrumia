---
name: scrumia-rules-setup
description: Scaffolds a project-local rule section under .scrumia/rules/<section>/ — short interview, then harvests existing conventions from the codebase instead of inventing them, writes the index/guides/decisions, and registers the section in CLAUDE.md. Use it when a project's own conventions on a topic are worth writing down as rules.
---

# Scaffolding a project-local rule section

Requires `scrumia-rules` — read it first if you haven't: it defines the format this skill produces. Idempotent: run again on an existing section, it checks and reports drift instead of overwriting.

## What this skill refuses

**Inventing rules.** A project-local section documents what the codebase already does, not what an agent thinks it should do. If a convention can't be sourced — in code, in tooling config, or in the user's own words during the interview — it doesn't get written as a rule. It gets asked about instead.

## Step 1 — Short interview

Ask, briefly:

1. **Which concern?** One topic, not a grab-bag — "how we fetch data", not "frontend stuff". If the answer covers more than one topic, that's two sections, or a signal the request is premature (see `scrumia-rules`, "When NOT to use the hierarchy" — fewer than ~3 distinct rules, stay single-file).
2. **Why now?** A repeated correction in review, a new contributor asking the same question twice, an existing convention nobody wrote down. "Because rules are good practice" is not a reason — it produces a section nobody consults.
3. **Which paths does it govern?** The globs for `section.json`. If the answer is "the whole repo", push back: a section that broad usually hides several concerns.

Stop here if fewer than three distinct rules are in view once harvesting (next step) is done — a single guide, or a paragraph in `CLAUDE.md`, serves better than a routing table with one destination.

## Step 2 — Harvest, don't invent

Gather evidence before writing a single rule, in this order:

1. **Neighboring code.** Read the files the declared globs match. A pattern repeated across most of them, with no contradicting instance, is a candidate rule. A pattern present once is an example, not a convention.
2. **Lint and format configs.** ESLint/Biome rules, `rustfmt.toml`, `clippy.toml`, `.editorconfig`, `tsconfig` strict flags — anything already enforced mechanically is a rule the team has already decided, just not narrated. These are the strongest candidates for `Status: Adopted`.
3. **Existing docs.** `README.md`, `CONTRIBUTING.md`, wiki pages, comments at the top of a shared module — informal rules waiting to be formalized.
4. **The interview answers themselves**, where the user states a convention directly.

For each candidate rule, note where it came from. That provenance is what decides its decision's `Status` in Step 4 — and it is what you show the user before writing anything, so they can correct a pattern you mistook for a convention.

**A pattern found in code that contradicts a lint rule or a stated convention is a finding, not a rule** — surface the contradiction, don't silently pick a side.

## Step 3 — Write `00-index.md`

Follow the anatomy from `scrumia-rules`: guides table, quoted-need routing, dependency graph, decisions table. Route only to guides you are about to create in this run — an index promising a guide that doesn't exist is worse than no index.

## Step 4 — Write the first guides and decisions, together

One guide per harvested concern, in `guides/NN-topic.md`: numbered rules, each with a **Correct** example taken from the actual codebase (not rewritten to look cleaner) and an **Incorrect** one — either a real instance you found contradicting the rule, or, failing that, a plausible mistake stated as such.

Each guide ships with its decision in `decisions/D-NN-slug.md`, same change, never after the fact:

- **`Status: Adopted`** — only when the evidence is strong: enforced by tooling, or confirmed with no exception found, or the user explicitly confirmed it during the interview.
- **`Status: Proposed`** — everything weaker: a pattern observed but not confirmed, a single strong example generalized. Say so plainly in the report (Step 7); a `Proposed` decision is a draft the team still needs to ratify, not a rule an agent should enforce yet.

Arguments For and Arguments Against are mandatory in every decision, `Proposed` included — the harvesting step already surfaced the trade-off (why the codebase does it this way, what it costs). Write it down now, while it's still visible; it's the whole reason the decision exists as its own file instead of a bare assertion in the guide.

## Step 5 — Write `section.json`

```json
{ "globs": ["<pattern>", "..."] }
```

The globs agreed on in Step 1, possibly refined once harvesting showed the pattern's real boundaries.

## Step 6 — Register the section in `CLAUDE.md`

Under a dedicated, idempotent block:

```markdown
<!-- scrumia-rules:start -->
## Project rules

Project-local rule sections. Before touching a path listed here, read that section's
index first — its rules override any module-shipped section covering the same code
(specific beats generic; see `scrumia-rules`).

| Path globs | Section index |
|---|---|
| `src/data/**` | `.scrumia/rules/data-fetching/00-index.md` |
<!-- scrumia-rules:end -->
```

Re-running: **add a row, never remove or reorder existing ones** without asking. Before adding, check `.scrumia/rules/` on disk against the table — a section directory with no row is drift to report; a row pointing at a directory that no longer exists is drift to report. Fix neither silently.

If the `<!-- scrumia-rules:start -->` block doesn't exist yet, create it; don't touch the `<!-- scrumia:start -->` block `scrumia-init` owns — different markers, same file.

## Step 7 — Report back

What was created, the globs it now governs, and — the one thing not to bury — **which decisions are `Adopted` and which are `Proposed`**. A `Proposed` decision left unconfirmed for long enough is worth flagging back to the user rather than silently treated as settled.

## What you don't do

- No rule with no traceable source — code, tooling config, docs, or the user's own words.
- No `Status: Adopted` without one of the three qualifying conditions in Step 4.
- No guide without its decision, even in a first draft.
- No commit — the user reviews.

## The module's two other skills

- `scrumia-rules` — the format this skill produces; read it first.
- `scrumia-rules-update` — evolve a rule once the section exists.
