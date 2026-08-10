---
name: sweep-surface-format-rules
description: Where a scrumia-specs format rule is restated — the eight places a consistency sweep has to reach, two of them agent-executed and two generated
metadata:
  type: project
---

A rule about the feature format is restated far from `references/catalog.md`. A sweep
that stops at the obvious three leaves the retired rule live somewhere an agent runs it.
Ordered by damage:

1. `scrumia-specs-setup/SKILL.md` Step 3 — the composition line handed to `scrumia-init`
   for a **consumer project's** `CLAUDE.md`. Always loaded, and the only statement of the
   rule a project gets without opening `catalog.md`.
2. `scrumia-specs/commands/feature.md` — restates the rule as an instruction; front door
   for `/feature`.
3. `scrumia-feature/SKILL.md` — three separate statements: the opening framing sentence,
   the catalogue table, and "Updating an existing feature" step 5 (*delete a file that
   became meaningless*), which a mandatory-file rule must carve out of.
4. `assets/index.template.md` — the note under the "Files present" sample table.
5. `docs/format-feature.md` and `docs/architecture.md`.
6. `site/i18n/{en,fr}/modules/scrumia-specs.json` (`refusals`, `philosophy`), whose
   `site/**/modules/*.html` are **generated** — edit the JSON and rebuild with
   `tools/build_site.py`, both languages.
7. `scrumia-discovery/skills/scrumia-split/SKILL.md` Step 2 — enumerates which files to
   create for a new feature, in contract-key terms. A consumer in another module, easy to
   miss, and the place a rule about mandatory files gets silently re-derived.

**Why:** #25 (2026-08-09) existed because three texts disagreed; the fixing diff swept
five places and left four, two of which instruct an agent.

**How to apply:** grep the rule's phrasing, not the file list — the wordings differ by
site. See [[contract-block-carries-names-not-status]] for the neighbouring trap.
