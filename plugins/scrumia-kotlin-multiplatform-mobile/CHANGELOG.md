# Changelog — scrumia-kotlin-multiplatform-mobile

All notable changes to this module, on [Keep a Changelog 1.0.0](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]

## [0.2.0] - 2026-08-22
### Added
- Named as the **Kotlin Multiplatform Mobile implementation slot** — the pivot is what a Kotlin Multiplatform Mobile project names in its own `modules` to answer "how is code written for this app", the same role `scrumia-kotlin` plays alone for a pure-JVM/Android project. The pivot still opens no register of its own and still contributes only the six KMP-specific norms below.

## [0.1.0] - 2026-08-22
### Added
- `extends.json` — six KMP-specific norms (`expect-actual-across-source-sets`, `source-set-layout`, `platform-tests-and-dependencies`, `cocoapods-swift-interop`, `kmp-target-declaration`, `kmp-shaped-gradle-wiring`) contributed to the `implement` register, with a single review summary on the `review` register and a `find-spec` entry pointing at the reference. The pivot does not open any register, and contributes to no register named `init` — `scrumia-extends --list` shows the same register set before and after the module lands.
- `rules/` — one file per KMP-specific rule family, citing `https://kotlinlang.org/docs/` for each. No rule duplicates a satellite's territory: Kotlin language rules stay in `scrumia-kotlin`, Gradle the tool stays in `scrumia-gradle`, HTTP in `scrumia-ktor`, UI in `scrumia-material3`, effects in `scrumia-effect`, paradigm in `scrumia-functional-programming`.
- `skills/scrumia-kotlin-multiplatform-mobile/SKILL.md` — the reference that lists the six rule families, their files, and the dissociation from the six satellites. The pivot is compose-only: a single reference skill, no executable, no `bin/`, no `agents/`, no `dependencies.jsonl`.
- The capability the pivot carries: a project that declares `tibs245/scrumia:scrumia-kotlin-multiplatform-mobile` receives the KMP-specific rules alongside the six satellites' rules through one key in `.scrumia/config.yaml`, without re-declaring the satellites.