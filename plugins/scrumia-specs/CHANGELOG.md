# Changelog — scrumia-specs

All notable changes to this module, on [Keep a Changelog 1.0.0](https://keepachangelog.com/en/1.0.0/).

## [0.5.0] - 2026-08-17
### Added
- The catalog splits into **angles**: one directory per angle under
  `scrumia-feature/references/angles/<angle>/`, each shipping `context.md` (what it
  answers, what activates it, the questions that explore it, its boundary),
  `template.md` and `checklist.md` — the review guard-rails naming the defects that
  angle actually produces. `references/catalog.md` becomes the index of the eleven.
- Activation is answered rather than felt: each content-tested angle carries a table of
  closed questions with the answer to take when unsure. A project overrides any of them
  through `params.angles` — `always`, `context` (default) or `never`.
- `scrumia-feature` gains a numbered creation procedure whose order is what prevents the
  format's most common defect, and a mandatory report of which angles were declined and
  on which answer — an absence nobody can see was considered asserts nothing.
- The disposition on disk is stated: when a feature sits inside another, the test that
  decides it, and the three constraints that come with nesting.
- `index.md`'s `Links` vocabulary is a closed set of nine keys — four structural,
  declared on both sides; five referential.
- `tools/validate.py` gains `check_angle_directories`, `check_feature_links` and
  `check_feature_nesting`.
- `registers.json`, `extends.json` and `dependencies.jsonl` — this module opens the
  `write-spec` and `find-spec` registers, contributes the spec-before-code rule to
  `implement` and the spec/code gap to `review`, and declares the names it runs.
- `scrumia-specs-find` asks the `find-spec` register what else this project loads with a
  spec — the register it opens was, until now, promised and never consulted.
- The catalog states where a feature-format rule is restated — the six sites a sweep
  has to reach, ordered by damage — and distinguishes a criterion's own falsifiability
  (`qa.md`, "must be able to fail") from ADR-0004's feature-splitting *verifiable*, which
  is a different property under a shared word.
- `format-feature.md`, the format's rationale, moves from this repository's own `docs/`
  to ship inside `scrumia-feature` itself, alongside the catalog it explains: a project
  reads the version of the rationale that matches its installed skill, not whatever this
  repository's `main` branch carries.
### Changed
- The changelog entry drops its `PR:` field and gains a `Category:` — an entry names
  only what exists when it is written. The catalog and the template state the new shape.
- `scrumia-feature/SKILL.md`'s history rule is now an explicit must/must-not checklist
  instead of prose alone, and states `business.md`'s sourcing boundary against ADRs and
  acceptance criteria explicitly — an executor following only `scrumia-ticket` had no
  reason to open this file's rule before writing.
- `README.md` — addressed to whoever is deciding whether to run this module, not to the
  agent that already does: what it answers, what it refuses, what it ships.

## [0.4.0] - 2026-08-10
### Added
- The `specs` slot: per-feature specs as a contextual file catalogue under `features/`, not a monolithic PRD.
- `scrumia-feature` — creates, updates and audits a feature, applying the catalogue rather than a fixed template; `/feature` invokes it.
- `scrumia-specs-find` — finds the feature that owns a rule, so a ticket loads its context instead of the whole tree.
- `scrumia-specs-setup` — installs the tree.

Earlier versions shipped without a changelog; `0.4.0` is the first version this file
describes, and it states what the module carries rather than reconstructing how it got
there. That history is in the repository's git log and its issues.
