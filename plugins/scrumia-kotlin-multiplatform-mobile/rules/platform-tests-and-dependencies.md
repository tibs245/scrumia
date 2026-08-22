# platform-tests-and-dependencies

*Norm.* Platform-specific tests live in the matching test source set (`androidTest`, `iosTest`, `jvmTest`, `commonTest` for the rest). Dependencies per target declare the dependency for the targets that need it — `commonMainDependencies` is not interchangeable with `iosMainDependencies`.

## What is required

A test that calls a platform API lives in the source set that sees the API. A test that exercises behaviour every target should pass lives in `commonTest`. Dependencies are scoped the same way: the dependency a target compiles against is declared on that target's source set, not on `commonMain`.

```kotlin
// build.gradle.kts
kotlin {
    sourceSets {
        commonMain.dependencies {
            implementation("org.jetbrains.kotlinx:kotlinx-coroutines-core:1.8.0")
        }
        androidMain.dependencies {
            implementation("androidx.core:core-ktx:1.13.0")
        }
        iosMain.dependencies {
            // Nothing here today; the iOS-only API is reached through cinterop, not a JAR.
        }
        commonTest.dependencies {
            implementation(kotlin("test"))
        }
        androidTest.dependencies {
            implementation("androidx.test:core:1.5.0")
            implementation("org.robolectric:robolectric:4.11.1")
        }
        iosTest.dependencies {
            // iOS UI tests live in iosTest; a UIKit call from commonTest would not compile.
        }
    }
}
```

A test in `androidTest` is a JVM test that runs on an Android instrumentation runner or Robolectric, not a "test that happens to compile for Android". The Kotlin documentation states:

> "Test source sets in a multiplatform project are similar to main source sets. The default project hierarchy includes the `commonTest`, `jvmTest`, `androidTest`, and `iosTest` source sets, and the JVM, Android, and iOS source sets extend `commonTest`."

## Why

A dependency declared in `commonMain` is one every target pulls in, including the ones that never use it. A library that only ever runs on Android added to `commonMain` ships the AAR to iOS too, where the linker silently accepts what the runtime has no use for and the app's binary grows. A test that calls a platform API from `commonTest` does not compile for the targets that lack the API, and the moment it does compile the test is no longer testing what it says.

Dependencies per target are also the granularity `expect`/`actual` implementations need: an iOS `actual` is free to depend on a CocoaPods pod through cinterop; an Android `actual` is free to depend on a `androidx.*` library. Neither is reachable from the other.

## What is refused

- A platform-specific dependency declared in `commonMain` — every target pulls it in, even the ones that have no API surface for it.
- A test that calls a platform API from `commonTest` — the test compiles only for the targets that happen to see the API, and a sibling target that does not has the test silently skipped or removed.
- A `commonMainDependencies`/`iosMainDependencies`/`androidMainDependencies` configuration that overlaps — a dependency reachable through both is a dependency whose platform scope is invisible from the configuration that names it.
- An iOS test or an Android instrumentation test placed in `jvmTest` or `commonTest` — the test runner that runs it is the runner the source set declares.

## Sources complémentaires

- Kotlin — [Configure compilations](https://kotlinlang.org/docs/multiplatform-configure-compilations.html) — the dependency configurations per source set (`commonMainDependencies`, `iosMainDependencies`, `androidMainDependencies`, …), and the rule that each is scoped to its source set's targets.
- Kotlin — [Test your multiplatform project](https://kotlinlang.org/docs/multiplatform-run-tests.html) — the `commonTest`, `androidTest`, `iosTest` hierarchy, and the runner each test source set uses by default.
- Kotlin — [Add dependencies](https://kotlinlang.org/docs/multiplatform-add-dependencies.html) — how to add a library dependency to a specific source set rather than the common code.