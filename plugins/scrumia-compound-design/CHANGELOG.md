# Changelog — scrumia-compound-design

All notable changes to this module, on [Keep a Changelog 1.0.0](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]

## [0.1.0] - 2026-08-14
### Added
- `extends.json` contributing three refusals to the `implement` register only — children-reach-parent-through-context, sub-components-co-located, compound-consumed-as-unit. The plugin deliberately does not contribute to `review`; a compound's review is the same review any component passes.
- `rules/` — one markdown file per refusal, each citing the patterns.dev reference as its single source.
- `docs/principle.md` — the pattern in one page, framework-agnostic.
- `docs/react.md`, `docs/vue.md`, `docs/solid.md`, `docs/angular.md` — the same principle in each framework's idiom. The four read in any order; none translates another.
- `skills/compound-audit/` — answers "is this compound composed correctly?" by reading the parent, the parts, and the public surface against the three refusals.
- README citing `https://www.patterns.dev/react/compound-pattern/` as the single authority for the pattern.