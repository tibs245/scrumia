# Changelog — scrumia-gradle

All notable changes to this module, on [Keep a Changelog 1.0.0](https://keepachangelog.com/en/1.0.0/).

## [0.1.0] - 2026-08-22
### Added
- The Gradle-the-tool capability: eight rules contributed to the `implement` and `review` registers — Kotlin DSL over Groovy, version catalog as the one place versions live, the shape of a convention plugin (precompiled script plugin in a `build-logic` composite), lazy task configuration, the build and configuration caches, composite builds for local siblings, `pluginManagement`, and documentation tasks wired into the lifecycle.
- `scrumia-gradle` — the reference skill carrying eight guides and one decision record. Read before writing or reviewing a Gradle build script.
- `scrumia-gradle-audit` — the audit skill measuring an existing Gradle project against the eight rules, finding by finding, citing the guide each finding violates.
- One entry to the `find-spec` register: the Gradle rules are documented under `plugins/scrumia-gradle/skills/scrumia-gradle/guides/`; `scrumia-specs-find` reaches them through that entry when a ticket touches a Gradle build script.

Satellite of the Kotlin / Kotlin Multiplatform Mobile lane; lands independently of every other satellite. The Kotlin Multiplatform-specific application of Gradle lives in `scrumia-kotlin-multiplatform-mobile`, not here.
