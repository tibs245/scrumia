# source-set-layout

*Norm.* Source sets are the layout. `commonMain` holds what every target compiles; `androidMain`, `iosMain`, `jvmMain` hold what only their target compiles; intermediate source sets (`iosArm64Main`, `iosX64Main`, `androidNativeMain`, …) hold what a subset shares.

## What is required

A Kotlin Multiplatform module's code is partitioned into source sets. Each source set compiles to one or more targets, declared in the Gradle DSL. The layout has three tiers:

| Tier | Examples | Compiles for |
|---|---|---|
| common | `commonMain`, `commonTest` | every target the module builds |
| platform | `androidMain`, `iosMain`, `jvmMain` | the target whose name the source set carries |
| intermediate | `iosArm64Main`, `iosX64Main`, `iosSimulatorArm64Main`, `androidNativeMain`, `appleMain` | a named subset of targets |

```kotlin
// commonMain
fun greet(): String = "Hello from commonMain"

// iosMain
actual fun platformName(): String = "iOS"

// iosArm64Main  (intermediate — applies to iosArm64 only)
fun deviceArchitecture(): String = "arm64"

// appleMain   (intermediate — applies to iosArm64 + iosX64 + iosSimulatorArm64 + macos*)
fun appleFamilyOnly() {}
```

The compiler picks up a source file when the target being built includes its source set in its hierarchy. `iosArm64` is built by combining `commonMain` and `iosArm64Main`; `iosX64` is built by combining `commonMain` and `iosX64Main`. The Kotlin documentation is explicit:

> "By default, the source set `iosMain` extends `commonMain`, and every iOS-specific source set, for example, `iosArm64Main`, `iosX64Main`, and `iosSimulatorArm64Main`, extends `iosMain`. So the available source sets in the project structure are hierarchical: `commonMain` → `iosMain` → `iosArm64Main`."

## Why

A piece of code that imports an Android-only API does not compile for iOS. A piece of code that imports a Swift-only bridge does not compile for Android. The source set hierarchy is what makes a multi-target module tractable: every file declares, by where it sits, the targets it can reach, and the compiler enforces it.

Writing iOS-specific code in `commonMain` would either fail to compile (the API isn't on the classpath for other targets) or compile and reach into a platform that doesn't have the runtime at runtime. Writing `commonMain` code in `iosMain` makes it invisible to every other target, and the cost is paid the day a sibling target needs it.

Intermediate source sets are how `iosArm64` and `iosX64` share iOS-only code without lifting it to `iosMain` only to push it back down. They are the granularity the layout already provides.

## What is refused

- Platform code in `commonMain` — Android imports, Swift bridges, JVM-only APIs, native libraries. The compiler accepts only what the targets the source set compiles for can resolve.
- `commonMain`-shaped code in `iosMain`, `androidMain`, or `jvmMain` — sharing by promoting it out of `commonMain` so a sibling target cannot see it.
- A source set for a target that does not exist in the module — the layout that compiles is the layout the Gradle DSL declares.

## Sources complémentaires

- Kotlin — [Multiplatform project structure](https://kotlinlang.org/docs/multiplatform-discover-project.html) — the `commonMain` / `iosMain` / `androidMain` / `jvmMain` hierarchy, the intermediate source sets the build picks up by default.
- Kotlin — [Configure targets](https://kotlinlang.org/docs/multiplatform-configure-targets.html) — the targets each source set compiles for, and how intermediate source sets are named (`iosArm64Main`, `appleMain`, `androidNativeMain`).
- Kotlin — [Source set hierarchy](https://kotlinlang.org/docs/multiplatform-hierarchy.html) — the rule that intermediate source sets extend a parent set, and the parent chain that makes a source set visible to a target.