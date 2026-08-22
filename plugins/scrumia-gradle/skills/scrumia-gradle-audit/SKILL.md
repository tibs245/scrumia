---
name: scrumia-gradle-audit
description: Audits an existing Gradle project against the eight rules this module ships — Kotlin DSL over Groovy, version catalog usage, convention plugin shape, lazy task configuration, the build and configuration caches, composite builds for local siblings, pluginManagement, and documentation tasks wired into the lifecycle. Use it before adopting the module on an existing codebase, when a build shape change ships, or to verify a project held to the rules really is.
---

# Auditing a Gradle project

An audit observes, it does not fix. The output is a list of situated findings —
file, line, rule identifier — that the user turns into tickets or applies by hand.
The eight rules are read from the project's tree; nothing in this skill invokes
`gradlew`.

## Scope

Ask which app or which directory to audit if it isn't obvious. The module applies to
apps that list `scrumia-gradle` in their own `modules` in `.scrumia/config.yaml`.
Within the app, the files in scope are `settings.gradle.kts`, `settings.gradle`,
`build.gradle.kts`, `build.gradle`, every `*.gradle.kts` and `*.gradle` under any
subdirectory, `gradle/libs.versions.toml`, `gradle.properties`, and every file under
`build-logic/`.

If no Gradle project is present (`settings.gradle.kts` and `build.gradle.kts` both
absent), stop and say so — the audit has nothing to find.

## The eight passes, in order

### 1 — Build script format

Rule: [`01-build-script-format`](../scrumia-gradle/guides/01-build-script-format.md).

```bash
find <root> -name "*.gradle" -not -path "*/node_modules/*" -not -path "*/.gradle/*" -not -path "*/build/*"
find <root> -name "settings.gradle"
```

A `.gradle` file in the project tree is a finding the audit names; the audit reports
the path and the rule. A `settings.gradle` file is the same finding against the
settings script.

### 2 — Version literals outside the catalog

Rule: [`02-version-catalog`](../scrumia-gradle/guides/02-version-catalog.md).

```bash
grep -rn --include="*.kts" -E '"[0-9]+\.[0-9]+(\.[0-9]+)?"' <root>/build.gradle.kts <root>/app/build.gradle.kts
```

A version literal in a `.kts` file is a finding; the audit checks whether the literal
also appears in `gradle/libs.versions.toml`. A literal that is in the catalog and
read via `libs.<accessor>` is conformant; a literal that is in the build script
without a catalog entry is the finding.

### 3 — Convention plugin shape

Rule: [`03-convention-plugin-shape`](../scrumia-gradle/guides/03-convention-plugin-shape.md).

A `buildSrc/` directory is a finding unless a comment in the project's README names
why the older shape survives. A `build-logic/` directory is conformant; an
`includeBuild("build-logic")` declaration in the root `settings.gradle.kts` is the
shape the audit confirms.

A convention plugin under `build-logic/src/main/kotlin/` that declares Kotlin
Multiplatform targets (`jvm()`, `iosArm64()`, `expect`/`actual` wiring) is a Kotlin
Multiplatform-shaped convention plugin and is the satellite's concern, not this
module's. The audit reports it as a misplaced-rule finding, naming the satellite.

### 4 — Tasks declared with `tasks.register`

Rule: [`04-task-configuration`](../scrumia-gradle/guides/04-task-configuration.md).

```bash
grep -rn --include="*.kts" -E 'tasks\.create\s*\(' <root>
```

A `tasks.create` form without a sibling comment naming why the eager form is correct
is a finding. The audit reads the comment in the same file at the same line; an
absent comment is the finding's signal.

### 5 — Caches enabled

Rule: [`05-caches`](../scrumia-gradle/guides/05-caches.md).

```bash
grep -E '^org\.gradle\.caching\s*=' <root>/gradle.properties
grep -E '^org\.gradle\.configuration-cache\s*=' <root>/gradle.properties
```

A flag missing from `gradle.properties`, or set to `false`, is a finding. The audit
reads both flags in one pass; a project that enables one without the other is the
half-on finding.

### 6 — Local siblings as composite builds

Rule: [`06-composite-builds`](../scrumia-gradle/guides/06-composite-builds.md).

The audit reads the `settings.gradle.kts` for `includeBuild(...)` declarations and
the `dependencyResolutionManagement` block for repositories. A Maven repository that
serves snapshots of a sibling project the team also edits in the same workspace is
the snapshot-published-as-internal finding.

### 7 — Plugin versions in `pluginManagement`

Rule: [`07-plugin-management`](../scrumia-gradle/guides/07-plugin-management.md).

```bash
grep -rn --include="*.kts" -E 'version\s+"[0-9]' <root>
```

A version literal in a `plugins { … }` block in a build script is the
`pluginManagement` finding. A `pluginManagement { plugins { … version "…" } }`
declaration in the settings script is conformant.

### 8 — Documentation tasks wired into the lifecycle

Rule: [`08-documentation-tasks`](../scrumia-gradle/guides/08-documentation-tasks.md).

The audit checks the lifecycle wiring: `tasks.named("check") { dependsOn(...) }` or
`tasks.named("build") { dependsOn(...) }` for `dokkaHtml`, `javadoc`,
`publishToMavenLocal`, or a project's custom documentation task. A documentation
task with no lifecycle hook is the finding.

A `publishing { publications { … } }` block with a `publishToMavenLocal` or
`publish` task is the publication form of the rule; the audit treats the publishing
task's lifecycle hook the same as the documentation task's.

## Reporting

One finding per line: the file, the line (when known), the rule identifier
(`scrumia-gradle/BR-N` where N matches the guide), and one line of what was not met.

Close with the count of files that pass every rule, the count of files that fail at
least one, and the rule the audit found most often. The two counts let a reader see
whether the failure is concentrated in a few files or scattered across the project,
and the mode rule lets them decide where to start.

A finding against a Kotlin Multiplatform-shaped convention plugin is reported as a
misplaced-rule finding, naming `scrumia-kotlin-multiplatform-mobile` as the
satellite that owns the prose. The finding is reported so the audit is honest about
what it found; the fix is a ticket on the satellite, not on this one.

Rewrite nothing without agreement. If the user wants to fix the findings, work rule
by rule and produce one PR per rule.
