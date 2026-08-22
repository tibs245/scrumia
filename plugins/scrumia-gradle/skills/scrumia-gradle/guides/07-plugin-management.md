# Plugin versions in `pluginManagement`

> Every plugin version is declared in the `pluginManagement` block of `settings.gradle.kts`. A `plugins { id("...") version "..." }` block in a build script is a finding.

## Prerequisites

[01-build-script-format](01-build-script-format.md) — the settings script is `.kts`.
[02-version-catalog](02-version-catalog.md) — the catalog can also be a source, but the
rule here is the `pluginManagement` block, not the catalog.

## Rules

### Rule 1: Plugin versions are declared in `settings.gradle.kts`

The `settings.gradle.kts` block declares the plugins the build uses, with their
versions, repositories and conflict-resolution rules:

```kotlin
// settings.gradle.kts — the pluginManagement block
pluginManagement {
    plugins {
        kotlin("jvm") version "2.1.20"
    }
    repositories {
        gradlePluginPortal()
        mavenCentral()
    }
}
```

A plugin block in a build script that carries a version literal is the finding this
rule names:

```kotlin
// build.gradle.kts — the finding: a version literal in the plugins block
plugins {
    id("org.jetbrains.kotlin.jvm") version "2.1.20"   // AC-12: this is the finding
}
```

The version belongs in `pluginManagement`, not in the per-project `plugins { … }`
block. The build script applies the plugin; the settings script pins the version.

### Rule 2: A plugin is applied, not versioned, in the build script

A `plugins { id("...") }` block in a build script declares the plugin the project
uses — without a version, because the version lives in `pluginManagement`:

```kotlin
// app/build.gradle.kts — applies, doesn't version
plugins {
    id("scrumia.jvm-conventions")
}
```

The `alias(libs.plugins.kotlin.jvm)` form reads the version from the catalog and
applies the plugin in one step; the same rule applies, with the version declaration
moved to the catalog under the `[plugins]` table rather than to the `pluginManagement`
block. Both are conformant; the one the project chooses is a style choice the audit
does not arbitrate.

### Rule 3: `pluginManagement` is for plugin resolution, not for project resolution

The `pluginManagement` block in `settings.gradle.kts` governs plugin resolution:
which version of a plugin id is resolved, from which repository, in what order. The
`dependencyResolutionManagement` block governs project (library) resolution. The two
blocks answer different questions, and a `pluginManagement` block that lists
`dependencies { … }` or a `dependencyResolutionManagement` block that lists
`plugins { … }` is the wrong block for the entry.

## Why

A plugin's version is a single fact about the build, not a per-project fact. A
`pluginManagement` block is the one place that fact lives; a `plugins { id("...")
version "..." }` block in every build script that uses the plugin is the version
duplicated across every consumer, with the cost that a version bump becomes a
build-script search-and-replace instead of a settings-script edit.

The settings script is also the place that holds the repositories Gradle resolves
plugins from. A `pluginManagement` block that names `gradlePluginPortal()` and
`mavenCentral()` is a declaration that says where the plugin id resolves from, and
what the version conflict resolution is when two plugins ask for different versions
of the same dependency. The build script applies the plugin; the settings script
governs the resolution.

## Sources complémentaires

- [Gradle — Plugin management](https://docs.gradle.org/current/userguide/plugins.html#sec:plugin_management) —
  the reference for `pluginManagement` in `settings.gradle.kts`.
