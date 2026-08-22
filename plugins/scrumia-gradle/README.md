# scrumia-gradle

Gradle the build tool — the Kotlin DSL over Groovy, the version catalog as the one place
versions live, the shape of a convention plugin, lazy task configuration, the build and
configuration caches, composite builds, and `pluginManagement`. Stated in terms of
Gradle, not Kotlin Multiplatform, so a pure-JVM project (Spring, Android, a CLI) gets
the same rules as one that activates the Kotlin Multiplatform Mobile satellite.

## What it answers

How a Gradle project is shaped so the tool stays fast and the build script stays
readable. Eight rules, each one of them a finding an audit can name: where the version
goes, how a task is declared, what the convention plugin looks like, where the local
sibling dependency hooks in, and where the documentation tasks attach. The audit names
the file and the rule; the reference skill states what the rule *is* and why.

## What it refuses

- **Groovy DSL in a project this module owns.** Build scripts are `.gradle.kts`, not
  `.gradle`. The dynamic typing and the `apply plugin:` form reach Gradle today only by
  accident — Kotlin DSL is the form that catches the typos at compile time and is the
  one this module requires.
- **A version literal in a build script.** Every plugin and library version sits in
  `gradle/libs.versions.toml`; the build script reads it. A literal in `build.gradle.kts`
  is a finding, not a style choice.
- **A `plugins { id("...") version "..." }` block in a build script.** Plugin versions
  are declared in `settings.gradle.kts`'s `pluginManagement` block. The build script
  applies the plugin, the settings script pins the version.
- **`tasks.create` without a stated reason.** Tasks are declared with `tasks.register`
  for lazy evaluation; an eager `tasks.create` is a finding unless the comment beside it
  names why the eager form is correct.
- **A local sibling dependency published to a Maven snapshot.** A locally-built sibling
  is wired through `includeBuild(...)` — a composite build — and nothing more. Publishing
  it for internal use is a finding, because the composite build is the mechanism that
  makes the local change visible without going through a publish cycle.
- **A Kotlin Multiplatform-shaped convention plugin in this module.** That shape belongs
  to `scrumia-kotlin-multiplatform-mobile`. The shape of a convention plugin (the
  precompiled script plugin, applied through `plugins { id("...") }`) lives here; what
  the plugin *does* for Kotlin Multiplatform is the satellite's concern.

## What it ships

| Skill | Role |
|---|---|
| `scrumia-gradle` | The reference — eight guides (build script format, version catalog, convention plugin shape, task configuration, caches, composite builds, pluginManagement, documentation tasks) and one decision record. Read before writing a Gradle build. |
| `scrumia-gradle-audit` | Audits an existing Gradle project against the eight rules. Reports findings with file, line and rule identifier; rewrites nothing without agreement. |

## Settings it reads

None — the module is configuration-free. Every rule is a refusal or a norm in the
build script, and the audit reads the project's tree directly. A future setting
(e.g. a Gradle version floor) would land here with the deprecation window
[ADR-0017](https://github.com/tibs245/scrumia/blob/main/docs/adr/0017-version-bump-and-commit-signal.md)
states.

## What it expects to find

A Gradle project: a `settings.gradle.kts` at the root, a `gradle/libs.versions.toml`,
and at least one subproject's `build.gradle.kts`. None of the rules require the
project to be a Kotlin project — the DSL is the same for Java, Groovy, Kotlin, Android
or any other Gradle-supported language. The Kotlin Multiplatform-specific application
of these rules lives in `scrumia-kotlin-multiplatform-mobile`, which this module
neither requires nor assumes.

## Decisions

One so far — `D-01`, the convention plugin shape: precompiled script plugins in a
`build-logic` composite, applied through `plugins { id("...") }`, with the
Kotlin Multiplatform-shaped convention plugin cited as belonging to
`scrumia-kotlin-multiplatform-mobile` rather than restated here.

## Not shipped yet

No `scrumia-gradle-wrapper-helper` under `bin/`. The module's eight rules are
shape-level — what the build script and the settings script look like — and a Gradle
wrapper helper would reach for runtime state (the wrapper version, the daemon
status) that no rule in this module currently checks. The audit reads the project's
tree as text and the `bin/` directory is intentionally absent: adding one before a
rule that needs it is the placeholder this section exists to forbid.

No `scrumia-gradle-refactor` skill. An audit that finds a `.gradle` Groovy file or a
version literal names it; the rewrite to `.gradle.kts` or to a catalog entry is a
mechanical pass the human in front of the screen runs, and writing the skill first
would be writing the answer before the question.
