# kmp-target-declaration

*Norm.* Targets declare the triples a target family actually ships — `iosArm64` / `iosX64` / `iosSimulatorArm64` for Apple, `androidTarget()` for Android, `jvm("…")` for desktop — and the list is the one source of truth, not the IDE's view.

## What is required

A Kotlin Multiplatform module declares, in the Gradle DSL, every target it compiles for. Targets come in two shapes:

| Family | Declared as | Compiles for |
|---|---|---|
| iOS device | `iosArm64()` | physical iOS devices |
| iOS simulator (Intel) | `iosX64()` | iOS simulators on Intel Macs |
| iOS simulator (Apple Silicon) | `iosSimulatorArm64()` | iOS simulators on Apple Silicon Macs |
| Android | `androidTarget()` | the Android target family |
| Desktop JVM | `jvm("...")` | a JVM desktop target |

```kotlin
// build.gradle.kts
kotlin {
    androidTarget()
    iosArm64()
    iosX64()
    iosSimulatorArm64()
    jvm("desktop")
}
```

A target declared here is a target the build compiles for. The IDE may try to combine `iosX64` and `iosSimulatorArm64` into a single "iOS simulator" target — that is a presentation choice, not the source of truth. The Gradle DSL is.

## Why

A target absent from the Gradle DSL is a target the build does not compile for. The Kotlin documentation states:

> "A target is a build that produces a binary for a specific platform. Targets are declared in the `kotlin {}` block of the build script."

A target declared but never run is dead weight: the build produces an artefact no consumer asked for. A target needed but not declared is the bug this rule catches at the type level — the source set for the target does not compile, the IDE reports a phantom error, and the consumer's import fails because the artefact never existed.

`iosArm64` and `iosSimulatorArm64` are separate because the simulator on Apple Silicon is not the simulator on Intel. Combining them into a single target was the early Kotlin Native mistake that produced silent ABI breaks; the rule that they are separate targets is the response, and a build that compiles one and not the other has a simulator-only artefact the simulator cannot run.

## What is refused

- A target used in a `commonMain`-shared API but not declared in `kotlin { }` — the consumer's build fails with a missing artefact, not with a clear "this target was never compiled" message.
- `iosX64()` declared without `iosSimulatorArm64()` on a CI that runs Apple Silicon runners — the simulator tests have no artefact to run on.
- An Android target without an `androidTarget()` declaration — `android()` is the legacy form, deprecated in Kotlin 1.9, and the new code reads `androidTarget()`.
- A `jvm()` declaration with no JVM target version — the build defaults to a version that may not match the consumer's JDK, and the discrepancy shows up as a runtime class-not-found.

## Sources complémentaires

- Kotlin — [Configure targets](https://kotlinlang.org/docs/multiplatform-configure-targets.html) — the iOS / Android / JVM target families, and the `iosArm64` / `iosX64` / `iosSimulatorArm64` split.
- Kotlin — [Basic project structure](https://kotlinlang.org/docs/multiplatform-discover-project.html) — the targets a freshly-created KMP project declares by default, and the `iosArm64` / `iosSimulatorArm64` pair.
- Kotlin — [Android target](https://kotlinlang.org/docs/multiplatform-android.html) — the `androidTarget()` declaration, and the migration from `android()` to `androidTarget()`.