# Changelog — scrumia-rhf

All notable changes to this module, on [Keep a Changelog 1.0.0](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]
### Changed
- **Breaking — the project override moves to `.scrumia/overrides/scrumia-rhf.md`,
  from `.scrumia/impl/scrumia-rhf.md`.** `.scrumia/impl/` and
  `.scrumia/practices/` only ever differed by a category of module that no longer
  exists, so they collapse into one directory
  ([ADR-0024](https://github.com/tibs245/scrumia/blob/main/docs/adr/0024-no-category-of-module.md)).
  A project with an override file must move it; left where it is, it is not read.

### Added
- `extends.json` — the three refusals (`form-has-resolver`,
  `inputs-are-registered`, `state-through-library`) are contributed to
  the `implement` and `review` registers, so a skill applies them
  without naming this module.
- `rules/` — one file per refusal, citing `https://react-hook-form.com`
  pinned to v7.
- `skills/rhf-audit/SKILL.md` — the audit against the three refusals.
- The capability the plugin carries: declarative form management for
  React implementations, paired with schema-driven validation through
  a resolver.
