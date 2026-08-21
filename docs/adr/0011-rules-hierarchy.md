# ADR-0011 — A rules hierarchy for knowledge skills

**Status**: accepted — 2026-08-07

## Context

Implementation and practice modules ship their standing rules as a **knowledge skill**: one `SKILL.md`, loaded whole the moment it triggers, plus a `references/` folder for anything too long to inline.

`scrumia-rust` (`plugins/scrumia-impl-rust/skills/scrumia-rust/SKILL.md`) is representative: one file carries "how we test", "which design principles", "how the code is structured", "what we refuse", a "practices situated" section for whichever of `scrumia-tdd` / `scrumia-solid-principles` is plugged in, the settings block and the override pointer — plus a single flat `references/conventions.md` for the file tree, code samples and lints. `scrumia-tdd` (`plugins/scrumia-tdd/skills/scrumia-tdd/SKILL.md`) follows the same shape: the cycle, the AC-to-test mapping, the mock boundary, the scope boundary, the refusals, one flat `references/anti-patterns.md`. Loading either skill for "add one test" pulls in the refusals section and the settings block just the same as loading it for "review the whole test suite" would — there is no partial load.

This holds today because each module answers a handful of named points. It stops holding on three axes already visible in `docs/modules.md`: practice-situating sections multiply (Rust already situates two practices, a third — `scrumia-hexagonal` — is under consideration); implementation modules multiply per stack; and a monorepo plugs several implementation and practice modules across apps that share nothing. A root `SKILL.md` then answers for apps it does not cover, reloaded whole regardless. It is the same growth curve, and the same failure mode, that `docs/format-feature.md` names for the monolithic PRD and that ADR-0003 rejected for a single cross-cutting architecture file: a document that only grows, gets reloaded in full to read three lines, accumulates sections nobody prunes, and past a point nobody verifies.

Separately, `.scrumia/config.yaml`'s `apps[]` already carries an app → implementation/practices mapping, and `scrumia-init` already tabulates it into `CLAUDE.md` — but nothing scopes a module's rules to the files inside a given app's path, and a project's own conventions have only one outlet: a single override file (`.scrumia/overrides/<module>.md`). That file is exactly the flat-file shape this ADR moves modules away from — a project with real house rules to record hits the same growth curve one file down.

Prior art: [`fictional-guacamole`](https://github.com/tibs245/fictional-guacamole), same author, built for the `ovh/manager` monorepo. It structures sections as an index (`00-index.md`) acting as a routing table, numbered guides with a stated dependency graph, per-section decision records, and an interactive installer emitting per-IDE output (`.cursor/rules/*.mdc`, `.github/instructions/*.md`).

## Decision

**A rules hierarchy** for the knowledge skills of implementation and practice modules. `SKILL.md` stops carrying content directly and becomes a **routing index**: a one-paragraph contract summary, a guides table, a routing table (task phrasing → guide numbers), a dependency graph between guides, and a decisions table. Content moves into `guides/NN-topic.md` (one concern per file, correct/incorrect examples) and `decisions/D-NN-*.md` (the why, written to be challenged — matching this repo's own ADR discipline, applied one level down). A `section.json` declares the file globs the section applies to by default.

Scope: this restructures **knowledge skills only** — `scrumia-rust`, `scrumia-solidjs`, `scrumia-tdd`, `scrumia-solid-principles`. The procedural skills of the same modules (`scrumia-rust-audit`, `scrumia-tdd-refactor`, setup skills) are unaffected: they are already a checklist or a procedure, not a corpus of standing rules, and gain nothing from the split.

Concretely, for `scrumia-rust`:

```
plugins/scrumia-impl-rust/skills/scrumia-rust/
├── SKILL.md                        # contract summary, guides table, routing table, dependency graph, decisions table
├── section.json                    # { "globs": ["**/*.rs", "Cargo.toml"] }
├── guides/
│   ├── 01-project-layout.md          # workspace tree, crate organization
│   ├── 02-domain-types.md            # newtype, state enums, typestate
│   ├── 03-errors.md                  # thiserror per layer, #[source] translation
│   ├── 04-testing.md                 # one test per invariant, proptest
│   └── 05-lints.md                   # workspace clippy lints, SAFETY comment format
└── decisions/
    ├── D-01-no-unwrap-expect.md
    ├── D-02-no-clone-to-appease-borrowck.md
    ├── D-03-no-single-implementer-traits.md
    └── D-04-no-deref-inheritance.md
```

The routing table is what an agent actually consults: `"writing a new test"` → `04-testing`; `"defining a new domain type"` → `02-domain-types`; `"adding an error to a layer"` → `03-errors`. The dependency graph states what `02-domain-types` presupposes before `04-testing` makes sense — so an agent following a link loads in the right order instead of guessing.

Adopted from `fictional-guacamole`: the index-as-routing-table, numbered guides with an explicit dependency graph, per-section decision records, globs for file scoping. Dropped: the per-IDE installers and npm packaging. ScrumIA is deliberately Claude-Code-only (ADR-0001), and skills already do progressive disclosure natively — `SKILL.md` loads on trigger, `guides/` and `decisions/` load on demand — so there is no format to emit *to*.

### Per-app activation in monorepos

`apps[].path` in `.scrumia/config.yaml` — already present in every example, never enforced — becomes **required**. It is what the rest of this mechanism anchors on:

```yaml
apps:
  - name: api
    path: apps/api          # required — anchors this app's globs and its CLAUDE.md stub
    implementation: scrumia-impl-rust
    practices: [scrumia-tdd]
```

`scrumia-init` keeps writing the app → modules mapping, now including each path, into the root `CLAUDE.md` (the "Implementation and practices, per app" table already does this; this ADR makes the path column load-bearing rather than decorative). It additionally **offers** a per-app stub at `<path>/CLAUDE.md`:

```markdown
<!-- scrumia:start -->
## This app's modules

Implementation: `scrumia-impl-rust` — load `scrumia-rust` before writing code here.
Practices: `scrumia-tdd`.
Full composition: see the repository root `CLAUDE.md`.
<!-- scrumia:end -->
```

This rides Claude Code's native nested-`CLAUDE.md` loading — no new mechanism, the same trick ADR-0009 already relies on, applied at a second directory level. An agent working inside `apps/api` gets exactly that app's modules without scanning a root table sized for every app in the monorepo. Within an app, a section's `section.json` globs (resolved relative to `path`) decide whether that section's guides apply to the file being touched at all — a `scrumia-solidjs` section with `globs: ["**/*.tsx", "**/*.ts"]` says nothing about `apps/api`.

### Project-local rules

A project can maintain its own sections, in the same shape, under `.scrumia/rules/<section>/`:

```
.scrumia/rules/legacy-billing/
├── SKILL.md
├── section.json          # { "globs": ["apps/api/src/billing/**"] }
├── guides/
└── decisions/
```

This does not replace the single-file overrides (`.scrumia/overrides/<module>.md`) — those stay the right tool for a short exception to an existing module. It is the outlet for house rules that either outgrow a single file or answer to no plugged module at all (a legacy subsystem's quirks, a security rule specific to this codebase). The tooling — scaffolding a new section, checking it against the same shape a module uses — is the new `scrumia-rules` module: optional, since the format needs no module to be written by hand, the same way `.scrumia/overrides/<module>.md` needs none today.

Precedence is unchanged from ADR-0010: **specific beats generic**. A project-local section beats an implementation module, which beats a practice module, for any file its glob covers. What changes is scope, not order — a project can now out-argue a module with a rules hierarchy of its own instead of a single overflowing file.

## Consequences

**What we gain**

- Loading a knowledge skill for one task loads one or two guides, not the whole corpus — the same win `docs/format-feature.md` describes for specs, one layer down.
- The *why* separates from the *rule*: a guide is written to be followed while coding, a decision record is written to be challenged. Neither has to carry the other's weight.
- A monorepo agent working in `apps/api` reads a stub sized for `apps/api`, not a root table listing every app.
- A project with real local conventions gets the same tool a module author gets, instead of a single file it will eventually outgrow.

**What we accept**

- **More files per module.** A four-section `SKILL.md` becomes eight-plus files. A single rule change now touches a guide and, if the reasoning moved, a decision record — two files instead of one paragraph. Accepted because the alternative is the reload-everything cost paid on every trigger, forever, and that cost compounds while this one does not.
- **The index can drift from the files on disk.** A guide added without a routing-table entry is invisible to an agent that would have needed it; a decision record deleted without updating its guide's reference leaves a dangling claim. Mitigation: `tools/validate.py` gains a check for this class of drift (broken guide/decision references, files on disk absent from any table) the same way it already checks broken doc links and missing skill frontmatter. This is a mitigation, not a guarantee — the index can still drift between two `validate.py` runs.
- **Small modules pay pure overhead.** A module with fewer than roughly three distinct concerns has nothing to route between — `SKILL.md` as an index over one guide is indirection with no payoff. The floor is explicit: a module under that size stays single-file, full stop. `scrumia-solid-principles` (five principles, already multi-concern) crosses it; a hypothetical module answering one narrow question would not, and should not be forced into this shape.

## Rejected alternatives

**Keep the single fat file.** The status quo. It works exactly until it doesn't, and the failure mode is not hypothetical — it is the one `docs/format-feature.md` documents for the monolithic PRD and ADR-0003 rejected for a single architecture file: a document that grows, gets reloaded whole for three relevant lines, and accumulates sections nobody removes because removing requires proving nothing depends on them. Applying that same reasoning to knowledge skills and then not acting on it would be inconsistent with why ScrumIA rejected it everywhere else.

**A separate rules repository**, sharing sections across projects independently of the modules that use them. Rejected on the same grounds as ADR-0007: ScrumIA has a single author and a single repo precisely to avoid coordinating releases across repos; a rules repo reintroduces that coordination for exactly the content this ADR is trying to make cheaper to maintain, and contradicts the golden rule that everything lives in one repo.

**Per-IDE output formats**, following `fictional-guacamole`'s installer for Cursor and Copilot. Out of scope by constraint, not by oversight: ScrumIA targets Claude Code only (ADR-0001). An installer emitting `.mdc` and `.instructions.md` variants would be built, tested and maintained for tools ScrumIA has no other reason to support — pure cost, no user it serves today.

## To revisit

If the guide count inside one section grows past roughly a dozen, the index itself risks becoming what this ADR was written to avoid — at that point, consider whether the section should split into two. If the three-concern floor turns out wrong in practice once real modules have gone through this migration, revise the number rather than the principle.
