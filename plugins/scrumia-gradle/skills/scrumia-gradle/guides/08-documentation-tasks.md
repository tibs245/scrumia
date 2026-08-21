# Documentation tasks wired into the lifecycle

> `dokka`, `javadoc`, or a publishing convention plugin hooks into `check` or `build`. The rule is the wiring, not the content of the docs.

## Prerequisites

[01-build-script-format](01-build-script-format.md), [04-task-configuration](04-task-configuration.md) —
the task is declared in a `.gradle.kts` file and registered lazily.

## Rules

### Rule 1: Documentation tasks depend on `check` or `build`

A documentation task that produces a public artefact — `dokkaHtml`, `javadoc`,
`publishToMavenLocal`, a custom `publishDocs` task from a convention plugin — is wired
into the build's lifecycle:

```kotlin
// app/build.gradle.kts — documentation task wired into the lifecycle
tasks.named("check") {
    dependsOn(tasks.named("dokkaHtml"))
}
```

A documentation task that exists but is not a transitive dependency of `check` or
`build` is a finding the audit names. The rule is that the docs are produced as
part of the build, not that they are produced on a developer's machine by a separate
command nobody runs in CI.

### Rule 2: The wiring is in the build script, not in a comment

```kotlin
// Correct: the dependency is expressed in code
tasks.named("check") {
    dependsOn(tasks.named("dokkaHtml"))
}
```

```kotlin
// Finding: a comment that asks the reviewer to remember the wiring
// Run `./gradlew dokkaHtml` before committing
tasks.register("dokkaHtml") { /* … */ }
```

A comment that asks the reviewer to remember a wiring is the comment that the
wiring-in-code rule was written to replace. The audit raises a finding against the
build script, not against the comment.

### Rule 3: The content of the documentation is not this module's concern

A `dokkaHtml` task that produces no useful documentation is a documentation-quality
finding, not a Gradle-rule finding. The rule here is the wiring — the task hooks
into `check` or `build` — and what the task produces is the project's business.
`scrumia-design` may audit the result; `scrumia-teams`'s review may ask whether the
publication runs on `release`. This module asks only whether the task is wired in.

### Rule 4: The publication convention plugin is one form of the rule

A `publishing { publications { … } }` block in a build script that hooks into
`assemble` (via a `publishToMavenLocal` or `publish` task) is the same rule in a
different shape: the publication is a documentation artefact, and the wiring is
through Gradle's standard publishing tasks. The audit treats the publishing
convention plugin's lifecycle hook the same as the documentation task's; both are
conformant when the hook is in `check` or `build`.

## Why

A documentation task that is not part of the build's lifecycle is a task that runs
when a developer remembers to run it. The build's lifecycle is the one thing every
developer and every CI run executes, and what it executes is what the build says it
produces. Wiring the documentation task into `check` or `build` is what makes the
documentation a build artefact rather than a developer's habit, and what makes a CI
failure for a missing-doc a CI failure a reviewer reads rather than a doc the team
notices is stale the next time they look.

## Sources complémentaires

- [Gradle — dokka](https://kotlinlang.org/docs/dokka-introduction.html) — the
  documentation task the Kotlin DSL projects use; cited as the canonical example.
- [Gradle — javadoc](https://docs.gradle.org/current/userguide/javadoc.html) — the
  documentation task for JVM projects; cited as the canonical example for Java.
- [Gradle — Maven Publish Plugin](https://docs.gradle.org/current/userguide/publishing_maven.html) —
  the publication convention plugin and its lifecycle hooks.
