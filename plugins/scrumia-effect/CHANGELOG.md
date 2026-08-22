# Changelog — scrumia-effect

All notable changes to this module, on [Keep a Changelog 1.0.0](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]

## [0.1.0] - 2026-08-22
### Added
- `plugins/scrumia-effect/SKILL.md` — the reference skill, one entry point with the discipline section first and the four approach sections (`Result`, `Either`, `IO`/suspend, effect.website) layered on top, then error semantics and retry as data. Every rule's first line names the approach.
- `plugins/scrumia-effect/extends.json` contributing to the `implement`, `review`, and `find-spec` registers — a `Result`-only project receives only the `Result` and discipline rules as load-bearing; the `Either` and effect.website rules are listed but not consulted unless the project also runs those approaches.
- `plugins/scrumia-effect/skills/scrumia-effect/guides/` — ten guides, one per rule. Discipline first (01-04), then the four approaches (05-08), then error semantics (09-10). Each guide opens with the approach name so a reader can tell in one line whether it applies.
- `plugins/scrumia-effect/skills/scrumia-effect/decisions/` — D-01 explains why the discipline is split from the four approaches rather than absorbed into them; D-02 explains why retry is composed as a function on the effect rather than as a try/catch loop at the call site.
- `plugins/scrumia-effect/README.md` — names what the module owns, what it refuses, the dissociation (`scrumia-functional-programming` owns the paradigm, `scrumia-kotlin` owns `suspend`/`Flow`, `scrumia-ktor` owns HTTP-status-as-effect, the library's own module owns the rest of its API).
- Marketplace entry in `.claude-plugin/marketplace.json`. The module is library-agnostic on the pattern; `effect.website` is cited by URL and never imported.
