# ADR-0012 — The specs contract: documented, not hard-coded

**Status**: accepted — 2026-08-07

## Context

`scrumia-github-project`'s `scrumia-ticket` (its spec-reading step and its "update the spec first" step) and `scrumia-discovery`'s `scrumia-split` both write `features/`, `index.md`, `qa.md`, `business.md`, `api-contract.md`, `CHANGELOG.md` and `AC-n` directly into their prose, as if these names were universal. They are not: they are `scrumia-specs`'s own choices, documented in that module's `references/catalog.md` and nowhere else. `scrumia-teams`'s `scrumia-business` and `scrumia-tech` agents do the same in their "what to read" sections.

This is the exact failure ADR-0009 exists to prevent, reappeared one level down. ADR-0009 documents **which module fills which slot** — a tracker module knows it's talking to "the specs module" without knowing its name. It never documented **what vocabulary that module uses internally**. A consumer skill that needs to say "read the acceptance criteria file" had no documented name to reach for, so it reached for `scrumia-specs`'s own file name instead. `docs/composition.md` states the prohibition this violates in one line: *"a module never assumes another is present."* Naming `qa.md` in `scrumia-ticket`'s own steps is a stronger assumption than that — it assumes not just that a specs module is present, but that it is *this* one.

The consequence is concrete: swap `scrumia-specs` for a different specs module — a different root, a different per-file split, a different criterion identifier — and `scrumia-ticket`, `scrumia-split`, and the team agents keep reading and writing `qa.md`, `business.md`, `features/`, `AC-n`. Nothing errors. The ticket either silently misses the real spec files or silently writes into a directory the replacement module doesn't read. This is worse than a crash: a crash gets noticed.

## Decision

**The specs module declares a "specs contract" block. `scrumia-init` copies it into `CLAUDE.md`. Every consumer reads it from there.**

`scrumia-specs` documents, in its main `SKILL.md`, a "Composition block" section — a fixed set of `key: value` lines, this exact vocabulary and no other:

```
specs_root: features/
feature_index: index.md
acceptance_file: qa.md
ac_id_format: AC-<n>
changelog: CHANGELOG.md
catalog: business.md, legal.md, archi.md, api-contract.md, tech.md, ux.md, a11y.md, devx.md
```

`scrumia-init` copies this block verbatim — no rewriting, no summarizing — into `CLAUDE.md`, between the `scrumia:start` markers, under a new `## Specs contract` heading, the same step that already writes the "which module fills which slot" table. This is not a new mechanism: it is ADR-0009's copy-into-`CLAUDE.md` trick, applied to a module's internal vocabulary instead of only its name — the same move ADR-0011 already made for per-app stubs.

Every consumer — `scrumia-ticket`, `scrumia-split`, the `scrumia-business` and `scrumia-tech` agents, and any future consumer — reads these six keys from `CLAUDE.md` and refers to specs by them: "the directory in `specs_root`", "the file named by `acceptance_file`", "identifiers in `ac_id_format`". Hard-coding another module's own file names, anywhere outside that module itself, is forbidden.

**Degraded mode.** If `CLAUDE.md` carries no `## Specs contract` block — no specs module plugged in, or `scrumia-init` not yet run — a consumer says so plainly: *"no specs module documented — ask the human or proceed without spec updates"*, and continues with whatever part of its job doesn't need specs. Degraded, not broken — the same standard ADR-0009 and ADR-0010 already hold every other slot to.

## Consequences

**What we gain**

- Replacing `scrumia-specs` no longer silently breaks `scrumia-ticket`, `scrumia-split`, or the team agents. A replacement that ships its own Composition block keeps them working unchanged; one that doesn't makes them degrade with a named message instead of reading or writing the wrong files.
- One designated place to fix the vocabulary. A consumer skill that drifts back to hard-coding `qa.md` is a diff against a documented contract, not a guess about intent.
- No new machinery: the same `scrumia-init` step, the same markers, the same "agent reads a plain sentence at context load" trade-off ADR-0009 already argued for and already accepted.

**What we accept**

- **One more block to keep true.** A swapped specs module must ship its own Composition block, or every consumer degrades. This is the specs-slot instance of the cost ADR-0009 already named for the whole composition table — paid on a slot change, which happens rarely.
- **A small readability tax.** Consumer skills now say "the file named by `acceptance_file`" instead of "`qa.md`" — more words, less concrete, on every skill that touches specs. Accepted because the alternative is a name that stops being true the moment the module underneath it changes.
- **The same drift risk ADR-0009 already owns**, one level down: `CLAUDE.md`'s `## Specs contract` block can lag behind the specs module actually installed if `scrumia-init` isn't re-run after a swap. Mitigated the same way — re-run checks, not overwrites; a future `scrumia-compose` diagnostic would check this block first, next to the composition table it already owns.

## Rejected alternatives

**Dynamic runtime resolution.** A consumer skill reads `scrumia-specs`'s own `SKILL.md` at execution time to learn its vocabulary, instead of reading a copy from `CLAUDE.md`. This is the capability registry ADR-0009 already rejected, replayed for a module's internal names instead of its identity: the agent now holds "go find out what this module calls its acceptance file" in mind on every ticket, paying a resolution cost on every call for a vocabulary that changes a handful of times in a project's life. ADR-0009's argument transfers without modification: documented, not resolved.

**A shared vocabulary module all modules depend on** — a `scrumia-spec-vocabulary` plugin that `scrumia-github-project`, `scrumia-discovery` and `scrumia-teams` would each declare a hard dependency on. Rejected on two grounds. First, Claude Code plugins have no dependency mechanism to declare this with — ADR-0010 already hit this wall for practice modules and had to emulate composition through configuration instead. Second, and more fundamental: a hard dependency is exactly the coupling the founding prohibition exists to forbid — *a module never assumes another is present* (`docs/composition.md`). A tracker module built to require a vocabulary module could no longer be installed on its own, which is precisely the freedom this project sells.

**Status quo — leave the names hard-coded.** This is the flagship instance of ScrumIA breaking its own founding argument. Replaceability is not a claim this project gets to make selectively: a specs module swap silently breaking the tracker and the discovery module, while `docs/composition.md` states that no module assumes another is present, is a documented promise contradicted by the project's own code. Leaving it standing costs the project its central argument, not just three files.

## To revisit

If a project swaps specs modules often enough that re-running `scrumia-init` after every swap becomes the friction point — the same trigger ADR-0009 already names for the composition table as a whole. If a differently-shaped specs module (no per-feature catalog at all, a single flat spec file) shows the six-key vocabulary is too narrow — widen the vocabulary itself rather than letting consumers special-case around it.
