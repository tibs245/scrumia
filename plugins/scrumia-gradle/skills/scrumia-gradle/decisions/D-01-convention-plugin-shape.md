# D-01 — The convention plugin's shape is a precompiled script plugin in `build-logic`

> The shape lives here; the Kotlin Multiplatform-shaped convention plugin belongs to `scrumia-kotlin-multiplatform-mobile`.

## Context

A Gradle project that needs shared build logic factors it out of the per-project
`build.gradle.kts` and into a separate Gradle project the consumers apply through a
plugin id. Two shapes exist for that separate project: the older `buildSrc/`
directory Gradle auto-includes, and the newer `build-logic` composite build Gradle
includes through `includeBuild(...)`.

Inside the convention plugin itself, two shapes exist again: the older
`buildSrc/src/main/kotlin/MyPlugin.kt` Kotlin source file that implements
`Plugin<Project>`, and the newer precompiled script plugin
`build-logic/src/main/kotlin/my-plugin.gradle.kts` that Gradle compiles at
`build-logic`'s own configuration time.

The newer shape is the one Gradle 8 recommends and the one this module requires.

## Decision

A convention plugin in this module is a precompiled script plugin in a `build-logic`
composite:

1. `build-logic/` is a separate Gradle project, declared with
   `includeBuild("build-logic")` in the root `settings.gradle.kts`.
2. The convention plugin is a `*.gradle.kts` file under
   `build-logic/src/main/kotlin/`.
3. The consumers apply the plugin through `plugins { id("...") }`.

The `buildSrc/` directory is the older shape and is a finding the audit names when
present, with a comment naming why it survives when it does.

The Kotlin Multiplatform-shaped convention plugin — a `*.gradle.kts` that declares
`kotlin { jvm() }`, `kotlin { iosArm64() }`, source sets or `expect`/`actual` wiring
— is `scrumia-kotlin-multiplatform-mobile`'s concern. The shape (the precompiled
script plugin in `build-logic`) lives here; the content that wires Kotlin
Multiplatform targets is the satellite's. A reviewer who finds a Kotlin
Multiplatform-shaped convention plugin in `scrumia-gradle`'s guides cites this rule
and points the prose at the satellite.

## Consequences

A `build-logic` composite is a project the team composes with. A change to a
convention plugin is a change that lives in its own tree, with its own test
classpath and its own version control. The composite build is what makes the
convention plugin a unit a reviewer can hold in their head and what makes a change
to it incremental — Gradle recompiles only `build-logic` and only the consumers that
depend on the changed plugin.

The precompiled script plugin is the form that compiles the convention plugin at
`build-logic`'s configuration time. A typo in a convention plugin fails at config
time, with the same Kotlin DSL compile error a typo in a build script would raise
— the same property the project gets from
[01-build-script-format](../guides/01-build-script-format.md), applied to the
convention plugin's own DSL.

## The boundary with `scrumia-kotlin-multiplatform-mobile`

The split is the one the parent EPIC (#447) states: `scrumia-gradle` is the tool,
`scrumia-kotlin-multiplatform-mobile` is the tool *applied to* Kotlin Multiplatform.
A convention plugin's shape is the tool; a convention plugin that wires
`kotlin { jvm() + iosArm64() }` is the tool applied to Kotlin Multiplatform and is
the satellite's concern.

This rule cites the satellite by its module name. A reviewer who finds a Kotlin
Multiplatform-shaped convention plugin in `scrumia-gradle`'s guides names this rule
as the misplaced-rule finding and points at `scrumia-kotlin-multiplatform-mobile` as
where the prose belongs.

## References

- [Gradle — Composite builds](https://docs.gradle.org/current/userguide/composite_builds.html)
- [Gradle — Precompiled script plugins](https://docs.gradle.org/current/userguide/custom_plugins.html#sec:precompiled_script_plugins)
- [scrumia-kotlin-multiplatform-mobile](https://github.com/tibs245/scrumia) — the satellite
  that owns the Kotlin Multiplatform-shaped convention plugin
