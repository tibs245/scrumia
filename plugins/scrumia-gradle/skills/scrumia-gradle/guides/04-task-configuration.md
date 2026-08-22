# Tasks are registered, not created

> Tasks use `tasks.register` for lazy evaluation. An eager `tasks.create` is a finding unless the comment beside it states why the eager form is correct.

## Prerequisites

[01-build-script-format](01-build-script-format.md) — the task is declared in a Kotlin
DSL build script.

## Rules

### Rule 1: `tasks.register` for declarative tasks

A task that has no run-time dependency on the configuration phase uses
`tasks.register`, the lazy form:

```kotlin
// app/build.gradle.kts — the lazy form
tasks.register<Jar>("fatJar") {
    archiveClassifier.set("all")
    from(sourceSets.main.get().output)
}
```

`tasks.register` is the form Gradle recommends for any task the configuration phase
need not execute, and the form this module requires. The task is realised only when a
graph references it; configuration-time work that would otherwise run for every
project the build touches is avoided.

### Rule 2: `tasks.create` is a finding without a comment

```kotlin
// app/build.gradle.kts — eager, with a stated reason
// Eager creation is required because the task wires into configuration-cache
// incompatible reflection that registers an Input during the configuration phase.
tasks.create("generateProtos") {
    dependsOn(generateProtoTaskProvider)
}
```

An eager `tasks.create` without a comment naming why the eager form is correct is a
finding the audit raises against the file. The comment is the audit's signal that the
deviation is deliberate; without it, the eager task is a defect to fix, not a
deviation to keep.

### Rule 3: `register` over `create` for tasks declared through a typed plugin

When a typed plugin exposes a task through a `TaskProvider`, the project applies the
plugin and then configures the task through the provider. `tasks.register` with the
typed form is the Kotlin DSL way; the `tasks.create` form is the legacy fallback for
the case where the plugin does not expose a provider, and that case is the only one
this module exempts.

```kotlin
// app/build.gradle.kts — typed task configuration
plugins {
    id("scrumia.jvm-conventions")
}

tasks.named<JavaCompile>("compileJava") {
    options.compilerArgs.add("-Xlint:all")
}
```

A typed configuration through `tasks.named` reads as the contract the convention plugin
declared; an untyped lookup by name is the configuration the typed form replaced.

## Why

A build script runs at configuration time, before any task runs. A `tasks.create` form
eagerly instantiates the task at config time, which means a task the build graph
never reaches still costs the configuration phase its setup work. The
`tasks.register` form is lazy: the task is realised when something references it, and
the configuration phase is faster and the build graph is what decides what gets built.

The configuration cache goes one step further: it caches the configuration phase
itself, so a build that survives a configuration-cache round-trip cannot have any
configuration-time side effects. A `tasks.create` form is configuration-time work and
is one of the things the configuration cache breaks when it is enabled
([05-caches](05-caches.md)).

## Sources complémentaires

- [Gradle — Lazy task creation](https://docs.gradle.org/current/userguide/task_configuration_avoidance.html) —
  the reference for `tasks.register` over `tasks.create`.
- [Gradle — Configuration cache](https://docs.gradle.org/current/userguide/configuration_cache.html) —
  the cache `register` plays well with; `create` does not.
