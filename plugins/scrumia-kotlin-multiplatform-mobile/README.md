# scrumia-kotlin-multiplatform-mobile

The Kotlin Multiplatform Mobile composition preset — the KMP-specific rules for
`expect`/`actual` across source sets, the source-set layout (commonMain, androidMain,
iosMain, the JVM desktop target), the iOS/Android split (platform-specific tests and
dependencies), Cocoapods and Swift interop, target declaration, and KMP-shaped Gradle
wiring. Re-exports six satellites by configuration: `scrumia-kotlin`, `scrumia-gradle`,
`scrumia-ktor`, `scrumia-material3`, `scrumia-effect`, `scrumia-functional-programming`.
Plugs in app by app; a Kotlin Multiplatform Mobile project declares one key and gets
the KMP rules *and* the satellites' rules.

## What it answers

What is KMP-shaped and what is not — which declarations belong in `commonMain` and which
in a platform source set, how a multiplatform module declares its targets, how a Cocoapods
pod is integrated once and only once, how the `kotlin {}` block and the source-set DSL
wire the build. The pivot is for a project that already builds for iOS *and* Android (and
optionally a JVM desktop target) and wants the KMP-specific rules to reach an agent
alongside the language, build, HTTP, UI, effect and paradigm rules it already runs.

## What it refuses

- **No `expect`/`actual` that crosses source sets the wrong way** — an `expect` outside
  `commonMain` is a contract no other target sees; an `actual` in `commonMain` is a copy,
  not an implementation.
- **No source-set layout that mixes platform code with common code** — Android imports in
  `commonMain`, Swift bridges in `commonMain`, JVM-only APIs in `iosMain`. Each is a
  layout that compiles for some targets and silently fails for others.
- **No platform-specific test in `commonTest`, no shared dependency in `commonMain`** —
  a test in `commonTest` that calls a platform API does not compile for the targets
  that lack it; a dependency in `commonMain` ships to every target, including the ones
  that have no API surface for it.
- **No Cocoapods pod declared twice** — once in the KMP module and once in the iOS
  project's `Podfile`. Two declarations of the same dependency is one of which is a
  shadow, and the linker has to pick one.
- **No target the build does not compile for, no target the IDE invents** — the Gradle
  DSL is the one source of truth for which artefacts the module produces.
- **No Gradle wiring that bypasses the Kotlin Multiplatform plugin** — a dependency
  declared in `dependencies { implementation(...) }` instead of `dependencies {
  "commonMainImplementation"(...) }` is a dependency the multiplatform build ignores.

## What it ships

| Skill | Role |
|---|---|
| `scrumia-kotlin-multiplatform-mobile` | The reference — six rule families, each its own file, all citing the Kotlin documentation. Load before changing an `expect`/`actual` declaration, the source-set layout, the targets, a pod, or the KMP-shaped Gradle block. |

## Settings it reads

None. The pivot declares no `params:` of its own; the satellites declare theirs, and the
composition's project-wide settings are read through the cascade, not by this module.

## What it expects to find

A project that declares `tibs245/scrumia:scrumia-kotlin-multiplatform-mobile` in its own
`modules` mapping. The pivot is compose-only: it ships a single reference skill, and the
KMP-specific rules are contributed to the `implement`, `review` and `find-spec` registers
through the standard extension mechanism. A project that declares only the six satellites
(and not the pivot) receives their rules unchanged; the pivot is not a prerequisite for
any of them.

## Decisions

Two: why the pivot is compose-only and not a stack-membership module, and why the
satellites are dissociable — each has always been total on its own, and the pivot is the
way to get the seven together rather than the way any one of them depends on another.
Both are stated in `features/business/modular-composition/`.

## Not shipped yet

An audit skill. The pivot ships a reference, not an audit; a project that wants a
`scrumia-kmp-audit` that measures an existing app against the six families, finding by
finding, each citing its rule, can write one against the `extends.json` data the module
publishes. The pivot does not ship it today because the rule set is the body of work and
no audit is owed before a project adopts it.