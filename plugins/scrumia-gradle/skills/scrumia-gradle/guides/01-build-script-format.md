# Build script format

> Build scripts are `.gradle.kts`, never `.gradle`. Kotlin DSL is the form Gradle compiles at config time, and is the form this module requires.

## Prerequisites

None — this is the foundation of the whole module. Every other guide in this module
assumes a Kotlin DSL build script.

## Rules

### Rule 1: Kotlin DSL over Groovy DSL

Build scripts use the `.gradle.kts` extension. A `.gradle` Groovy file is a finding
the audit names:

```
plugins/scrumia-gradle/guides/01-build-script-format.md, Rule 1 — Groovy DSL file present
```

The `.kts` extension is the signal that the script is a Kotlin source file compiled by
the Gradle Kotlin DSL. The compiled class is then re-used across builds and the file
itself is type-checked against the Gradle API — two properties the Groovy script never
has, and that a reviewer otherwise has to compile in their head.

### Rule 2: `settings.gradle.kts`, not `settings.gradle`

The settings script carries the same rule. A `settings.gradle` file is the same
finding the audit raises against a `build.gradle` file:

```kotlin
// settings.gradle.kts — only the .kts form
rootProject.name = "scrumia-reference"
include(":app")
```

### Rule 3: Prefer `plugins {}` over `apply plugin: ""`

The `plugins { id("...") }` form in a `.gradle.kts` script is the Kotlin DSL's typed
entry. The legacy `apply(plugin = "...")` form, including `apply plugin: "..."` in
Groovy, is a finding the audit names against a build script that bypasses the typed
plugin API.

### Rule 4: Files that aren't build scripts are out of scope

A `.gradle` extension on a non-build file (e.g. a Gradle init script in
`~/.gradle/init.d/`, a Gradle script sourced by name through `--init-script`) is not
this module's concern. The rule applies to `settings.gradle[.kts]` and to every
`build.gradle[.kts]`. An init script the project writes for itself is a build logic
artefact and follows this module's rules the same way.

## Why

The Kotlin DSL compiles the build script at configuration time. A typo in a Groovy
DSL script fails at the first build attempt, with a stack trace pointing inside Gradle
rather than at the line that introduced the bug; a typo in a Kotlin DSL script fails at
config time, with a Kotlin error pointing at the file and line. The second is what
keeps a build script something a reviewer can read and an IDE can navigate. The first
is the bug this rule exists to fail fast on.

## Sources complémentaires

- [Gradle — Kotlin DSL build scripts](https://docs.gradle.org/current/kotlin_dsl.html) —
  the reference for the `.gradle.kts` form; cited as the authority.
