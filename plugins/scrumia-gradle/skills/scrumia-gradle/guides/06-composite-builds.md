# Composite builds for local siblings

> A locally-built sibling dependency is wired via `includeBuild(...)`. Publishing the same sibling to a Maven snapshot for internal use is a finding.

## Prerequisites

[02-version-catalog](02-version-catalog.md) — the sibling dependency still reads the
catalog; the composite build declaration does not change the catalog.

## Rules

### Rule 1: `includeBuild(...)` for a locally-built sibling

A project that depends on another project its team also works on (a shared library, a
tooling module, a common configuration) declares the dependency as a composite build
in the root `settings.gradle.kts`:

```kotlin
// settings.gradle.kts — composite build declaration
includeBuild("shared/library-x")
```

The consumer then depends on the sibling by the plugin id or Maven coordinates the
sibling exposes; Gradle resolves the dependency against the composite build, not
against the configured repositories.

### Rule 2: Publishing to a Maven snapshot for internal use is a finding

The composite build is the mechanism that makes a local change to the sibling
visible without a publish step. A `mavenLocal()` or `maven { url = uri(".../snapshots") }`
reference to the sibling, with a version like `1.0.0-SNAPSHOT` consumed from the
internal repository, is the same dependency reached through a more expensive path:

```kotlin
// settings.gradle.kts — the finding: Maven-published snapshot of a local sibling
dependencyResolutionManagement {
    repositories {
        maven {
            url = uri("https://internal.example.com/snapshots")
        }
    }
}
```

A snapshot of a sibling that has its own `settings.gradle.kts` in the same workspace
is the snapshot that should have been an `includeBuild(...)`. The Maven repository is
the right shape for a third-party dependency, not for a project the team owns and
edits alongside the consumer.

### Rule 3: The composite build is a separate project

`includeBuild(...)` points at a directory that is itself a Gradle project, with its
own `settings.gradle.kts` and its own `build.gradle.kts`. The composite build does
not share the consumer's build script classpath or plugin classpath. A directory
the consumer points at with `includeBuild(...)` but that does not carry its own
Gradle project is a misconfiguration Gradle reports at sync time, not this module.

### Rule 4: The convention plugin's `build-logic` is also a composite build

The `build-logic` directory from [03-convention-plugin-shape](03-convention-plugin-shape.md)
is itself an `includeBuild(...)` declaration. The rule is the same: a directory
Gradle points at with `includeBuild(...)` is a project, and what makes a project
`build-logic` is that it ships convention plugins rather than application code.

## Why

A locally-built sibling is the dependency a team edits in lock-step with the
consumer. The composite build is the mechanism Gradle ships for that case: the
consumer reads the sibling's outputs from the sibling's own build, and a change to
the sibling is visible in the next consumer build without a publish cycle. A
snapshot publish adds a publish step, a repository step, and a refresh-dependencies
step, each of which is a delay the composite build removes — and each of which is a
place the two projects drift out of sync.

## Sources complémentaires

- [Gradle — Composite builds](https://docs.gradle.org/current/userguide/composite_builds.html) —
  the reference for `includeBuild(...)` and the per-build substitution rule.
