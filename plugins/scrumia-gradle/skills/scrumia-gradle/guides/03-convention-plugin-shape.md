# Convention plugin shape

> Shared build logic lives in a `build-logic` composite as a precompiled script plugin, applied through `plugins { id("...") }`. The Kotlin Multiplatform-shaped convention plugin belongs to `scrumia-kotlin-multiplatform-mobile`, not here.

## Prerequisites

[01-build-script-format](01-build-script-format.md), [02-version-catalog](02-version-catalog.md)
— the convention plugin reads the catalog and is written in Kotlin DSL.

## Rules

### Rule 1: Shared build logic lives in `build-logic`

A piece of build logic used by more than one subproject is factored into a composite
build at `build-logic/`, included from the root `settings.gradle.kts`:

```kotlin
// settings.gradle.kts — composite build declaration
includeBuild("build-logic")
```

The composite build is a separate Gradle project: it has its own `settings.gradle.kts`
and its own `build.gradle.kts`, declares its own plugins through `pluginManagement`,
and ships the convention plugins its consumers apply.

### Rule 2: A convention plugin is a precompiled script plugin

The shape is the precompiled script plugin: a `*.gradle.kts` file under
`build-logic/src/main/kotlin/`, declared in the `build-logic` build script and
applied by consumers through `plugins { id("...") }`:

```kotlin
// build-logic/src/main/kotlin/jvm-conventions.gradle.kts
plugins { `kotlin-dsl` }
group = "scrumia.buildlogic"

dependencies {
    implementation(libs.kotlin.stdlib)
}

conventions {
    java {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }
}
```

```kotlin
// app/build.gradle.kts — applies the convention plugin
plugins {
    id("scrumia.jvm-conventions")
}
```

The precompiled script plugin is the modern form Gradle supports natively, with the
typed plugin API the Kotlin DSL compiles against. A `buildSrc/` directory is the older
shape and is a finding the audit names, with a comment naming why it survives when it
does.

### Rule 3: The Kotlin Multiplatform-shaped convention plugin is not here

A convention plugin that declares `kotlin { … }` with `jvm()`, `iosArm64()`,
`iosSimulatorArm64()` or any Kotlin Multiplatform target is
`scrumia-kotlin-multiplatform-mobile`'s concern. The **shape** of a convention plugin
(the precompiled script plugin in a `build-logic` composite) lives in this module; the
**content** that wires Kotlin Multiplatform targets is the satellite's. A reviewer who
finds a Kotlin Multiplatform-shaped convention plugin in this module's guides cites
this rule and points the prose at the satellite.

### Rule 4: A convention plugin is named, not anonymous

A convention plugin in `build-logic/src/main/kotlin/` carries the convention name in
its filename and the `id` it is applied through matches. The directory layout is part
of the contract: `kotlin-conventions.gradle.kts` is applied as `scrumia.kotlin-conventions`,
or with whatever group the `build-logic` build script declares. An anonymous helper
file under `build-logic/` (no `id`, no consumers) is a finding the audit names — the
helper is either a convention plugin the consumers apply or a piece of code that does
not belong under `build-logic`.

## Why

A `build-logic` composite is a separate project, with its own classpath and its own
plugin API. The composite build is what makes a change to a convention plugin
incremental — Gradle recompiles only `build-logic` and only the consumers that depend
on the changed plugin — and what makes a convention plugin a unit a reviewer can
hold in their head. A single-file `buildSrc/` is the same idea in a less composable
shape: every project that reads it loads it whole, and a convention plugin in `buildSrc/`
is a thing the project contains rather than a thing it composes with.

The precompiled script plugin is the form that compiles the convention plugin at
`build-logic`'s own configuration time. The compiled output is what the consumers
apply, and a typo in the convention plugin fails at `build-logic`'s config time
rather than at every consumer's config time. The composite + precompiled shape is
what makes the convention plugin a fast, typed contract between projects.

## Sources complémentaires

- [Gradle — Composite builds](https://docs.gradle.org/current/userguide/composite_builds.html) —
  the reference for `includeBuild(...)` and composite builds in general.
- [Gradle — Precompiled script plugins](https://docs.gradle.org/current/userguide/custom_plugins.html#sec:precompiled_script_plugins) —
  the reference for the `*.gradle.kts` convention plugin form.

For the Kotlin Multiplatform-shaped convention plugin, see `scrumia-kotlin-multiplatform-mobile`.
