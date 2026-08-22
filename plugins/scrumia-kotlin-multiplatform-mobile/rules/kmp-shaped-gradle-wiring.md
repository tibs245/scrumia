# kmp-shaped-gradle-wiring

*Norm.* KMP-shaped Gradle wiring: the `kotlin {}` block applies the Kotlin Multiplatform plugin, source-set dependencies go through `dependencies { "commonMainImplementation"(...) }`, convention plugins expose `kotlin("...")` targets without re-declaring them. Gradle *applied to* Kotlin Multiplatform, not Gradle the tool — the source-set DSL and the `kotlin {}` block are what makes the wiring multiplatform-shaped.

## What is required

A Kotlin Multiplatform build is wired in three layers:

1. **The `kotlin {}` block declares the targets.** Targets come from `iosArm64()`, `androidTarget()`, `jvm("desktop")`, and the block is the one source of truth for which artefacts the module produces.
2. **The `sourceSets {}` block inside `kotlin {}` declares source-set dependencies.** Each source set has a dependencies block, and the dependencies declared there are scoped to the targets that source set compiles for. `commonMain.dependencies { ... }` is the shared set; `iosMain.dependencies { ... }` is iOS-only.
3. **Convention plugins externalise the wiring.** A `kmp-conventions` plugin applied by every KMP module applies `kotlin("multiplatform")`, declares the targets, configures the source sets, and registers the project's common dependencies. A module that consumes the convention plugin does not redeclare any of it.

```kotlin
// build-logic/conventions/src/main/kotlin/KotlinMultiplatformConventionPlugin.kt
class KotlinMultiplatformConventionPlugin : Plugin<Project> {
    override fun apply(target: Project) = with(target) {
        with(pluginManager) {
            apply("org.jetbrains.kotlin.multiplatform")
        }
        extensions.configure<KotlinMultiplatformExtension> {
            androidTarget()
            iosArm64()
            iosSimulatorArm64()
            jvm("desktop")
            sourceSets {
                commonMain.dependencies {
                    implementation("org.jetbrains.kotlinx:kotlinx-coroutines-core:1.8.0")
                }
            }
        }
    }
}
```

A consumer module then declares:

```kotlin
// app/build.gradle.kts
plugins {
    id("acme.kmp-conventions")
    kotlin("native.cocoapods") version "2.0.0"
}

kotlin {
    cocoapods {
        ios.deploymentTarget = "14.0"
    }
}
```

The Kotlin documentation is explicit about the source-set DSL:

> "To add a dependency to a specific source set, use the source set's name in the dependency configuration, like `commonMainImplementation`, `iosMainImplementation`, or `androidMainImplementation`."

## Why

The source-set DSL is what makes a Gradle build KMP-shaped: a target's dependency on a library is declared *for that source set*, and the build wires the artefact into the artefact for that target. A library added to `dependencies { implementation(...) }` instead of `dependencies { "commonMainImplementation"(...) }` is a library the build ignores — the JVM/JS/Native compile classpaths do not include it.

A convention plugin that declares `kotlin("multiplatform")` and the targets is the answer to the rule "every module that compiles the same set of targets repeats the same boilerplate": one plugin, one declaration, one place to change the target list when iOS gains a new architecture or the JVM target version moves.

The split is Gradle the tool owning the *mechanism* (Kotlin DSL format, version catalogs, task configuration, build cache, plugin management) — that is a separate module's territory — and this module owning the *KMP-shaped wiring* (the `kotlin {}` block, the source-set DSL, convention plugins). The two meet at the build script's `plugins {}` block and never inside it.

## What is refused

- A dependency declared in `dependencies { implementation(...) }` for a source set the build ignores — the `kotlin {}` source-set DSL is what makes the dependency reach the right classpath.
- The `kotlin {}` block applied without the Kotlin Multiplatform plugin — the block is a type the plugin contributes; without the plugin, the script does not compile.
- A target declared in `kotlin {}` that the convention plugin also declares — two declarations of the same target, one of which is a shadow, and the linker has to choose.
- A `commonMain.dependencies { implementation(...) }` that names a library only one target can resolve — every target compiles the dependency in, the targets that cannot resolve it fail at link time.

## Sources complémentaires

- Kotlin — [Configure compilations](https://kotlinlang.org/docs/multiplatform-configure-compilations.html) — the source-set DSL, the `commonMainImplementation` / `iosMainImplementation` / `androidMainImplementation` dependency configurations.
- Kotlin — [Set up targets manually](https://kotlinlang.org/docs/multiplatform-set-up-targets.html) — the `kotlin {}` block, the targets it accepts, and how convention plugins externalise the declaration.
- Gradle — [Sharing project structure with convention plugins](https://docs.gradle.org/current/userguide/sharing_projects.html) — the convention plugin mechanism, applied at the `plugins {}` block, with the convention plugin owning the wiring the consuming module would otherwise redeclare.