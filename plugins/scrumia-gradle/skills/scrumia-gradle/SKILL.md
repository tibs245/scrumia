---
name: scrumia-gradle
description: The ScrumIA Gradle reference — Kotlin DSL over Groovy, the version catalog as the one place versions live, the shape of a convention plugin (build-logic composite, precompiled script plugin), lazy task configuration, the build and configuration caches, composite builds for local siblings, pluginManagement, and documentation tasks wired into the lifecycle. Stated in terms of Gradle, not Kotlin Multiplatform. Load it before writing or reviewing a Gradle build script.
---

# Coding in Gradle

**Eight rules, eight refusals or norms, stated in terms of the tool.**

This module refines one point of the implementation contract: **how a Gradle project is
shaped**. It applies to apps that list it in their own `modules` in
`.scrumia/config.yaml`, with or without an implementation module. When the project is a
Kotlin Multiplatform Mobile project, the Kotlin Multiplatform-specific application of
these rules lives in `scrumia-kotlin-multiplatform-mobile` — this module remains the
shape of the tool, applied to that project's build scripts the same way it would be to a
plain JVM project's.

## The contract

- **Build script format** — `.gradle.kts`, never `.gradle`; Kotlin DSL is the form Gradle
  compiles at config time. → [01-build-script-format](guides/01-build-script-format.md)
- **Versions live in the catalog** — every plugin and library version in
  `gradle/libs.versions.toml`, the build script reads it. →
  [02-version-catalog](guides/02-version-catalog.md)
- **Convention plugin shape** — shared build logic in a `build-logic` composite as a
  precompiled script plugin, applied via `plugins { id("...") }`. →
  [03-convention-plugin-shape](guides/03-convention-plugin-shape.md) and
  [D-01](decisions/D-01-convention-plugin-shape.md)
- **Tasks are registered, not created** — `tasks.register` for lazy evaluation;
  `tasks.create` is a finding unless a comment states why. →
  [04-task-configuration](guides/04-task-configuration.md)
- **Caches on by default** — `org.gradle.caching=true` and
  `org.gradle.configuration-cache=true` in `gradle.properties`; each rule names what it
  breaks when enabled. → [05-caches](guides/05-caches.md)
- **Composite builds for local siblings** — a locally-built sibling dependency is wired
  via `includeBuild(...)`; a Maven snapshot of the same sibling is a finding. →
  [06-composite-builds](guides/06-composite-builds.md)
- **Plugin versions in `pluginManagement`** — plugin versions belong in the
  `settings.gradle.kts` block; a `plugins { id("...") version "..." }` in a build
  script is a finding. → [07-plugin-management](guides/07-plugin-management.md)
- **Documentation tasks wired into the lifecycle** — `dokka`, `javadoc` or a publishing
  convention plugin hooks into `check` or `build`; the rule is the wiring, not the
  content of the docs. → [08-documentation-tasks](guides/08-documentation-tasks.md)

## Guides

| File | Use when you need to... |
|------|--------------------------|
| [01-build-script-format](guides/01-build-script-format.md) | Decide the file extension of a build script; understand why `.gradle.kts` over `.gradle` |
| [02-version-catalog](guides/02-version-catalog.md) | Add a dependency or update a version; find the version catalog; migrate a literal to a catalog entry |
| [03-convention-plugin-shape](guides/03-convention-plugin-shape.md) | Factor shared build logic out of a project; decide whether a piece of logic is a convention plugin or an in-build-script function |
| [04-task-configuration](guides/04-task-configuration.md) | Declare a new task; understand `tasks.register` vs `tasks.create` |
| [05-caches](guides/05-caches.md) | Enable or troubleshoot the build cache or the configuration cache; understand what each cache breaks when enabled |
| [06-composite-builds](guides/06-composite-builds.md) | Wire a sibling project you also work on; avoid publishing it to a Maven snapshot for internal use |
| [07-plugin-management](guides/07-plugin-management.md) | Add a plugin; understand why plugin versions live in `settings.gradle.kts` |
| [08-documentation-tasks](guides/08-documentation-tasks.md) | Wire `dokka`, `javadoc` or a publishing convention plugin into `check` or `build` |

## Routing table

```
"I need to write a new build script"
  → 01-build-script-format + 02-version-catalog

"I need to add a dependency"
  → 02-version-catalog (catalog first; build script reads it)

"I need to update a version"
  → 02-version-catalog (libs.versions.toml; never a literal in the build script)

"I need to factor shared logic across modules"
  → 03-convention-plugin-shape (build-logic composite, precompiled script plugin)

"I need to declare a new task"
  → 04-task-configuration (tasks.register, lazy)

"I need to make the build faster"
  → 05-caches (enable both caches in gradle.properties)

"I need to depend on a sibling project I also work on"
  → 06-composite-builds (includeBuild, never snapshot)

"I need to apply a plugin"
  → 07-plugin-management (version in pluginManagement, not in the plugins block)

"I need to publish documentation"
  → 08-documentation-tasks (wire into check or build)
```

## Dependencies between guides

```
01-build-script-format   ← foundation, no dependencies — read first
02-version-catalog       ← requires 01 (the catalog reads from a .kts file)
03-convention-plugin-shape ← requires 01, 02 (the plugin declares a dependency in the catalog)
04-task-configuration    ← requires 01 (lazy evaluation is a Kotlin DSL property)
05-caches                ← independent — a property of gradle.properties, not the build script
06-composite-builds      ← requires 02 (the sibling still uses the catalog)
07-plugin-management     ← independent — a property of settings.gradle.kts
08-documentation-tasks   ← requires 01, 04 (the task hooks into check or build)
```

## Decisions

| D-NN | Decision | Related guide |
|------|----------|---------------|
| [D-01](decisions/D-01-convention-plugin-shape.md) | The convention plugin is a precompiled script plugin in a `build-logic` composite; the Kotlin Multiplatform-shaped convention plugin belongs to `scrumia-kotlin-multiplatform-mobile`, not here | [03-convention-plugin-shape](guides/03-convention-plugin-shape.md) |

## Settings

None — the module is configuration-free. A future setting (e.g. a Gradle version floor,
or a cache-troubleshooting profile) would land here with the deprecation window
[ADR-0017](https://github.com/tibs245/scrumia/blob/main/docs/adr/0017-version-bump-and-commit-signal.md)
states. Today, every rule is a refusal or a norm the audit reads from the project's
tree.

## Project override

If `.scrumia/overrides/scrumia-gradle.md` exists, its content takes precedence over this
skill and its guides. A project records its house exceptions there — a legacy Groovy
build script that cannot migrate in one PR, a custom composite-build topology that the
audit would otherwise flag — without forking the module.

## The module's other skill

- `scrumia-gradle-audit` — measure an existing Gradle project against the eight rules,
  finding by finding, citing the guide each finding violates.

## Scope

This module applies to apps whose `.scrumia/config.yaml` lists `scrumia-gradle` in the
app's own `modules` (or in the project-wide `modules`, when the project has one Gradle
project and no per-app split). Within such a project, `section.json`'s globs
(`settings.gradle.kts`, `settings.gradle`, `build.gradle.kts`, `build.gradle`,
`**/*.gradle.kts`, `**/*.gradle`, `gradle/libs.versions.toml`, `gradle.properties`,
`build-logic/**/*.kt`, `build-logic/**/*.kts`) pick which files trigger the guides
above. An app with multiple Gradle projects (Android modules, multi-module JVM) is in
scope for every one of them.
