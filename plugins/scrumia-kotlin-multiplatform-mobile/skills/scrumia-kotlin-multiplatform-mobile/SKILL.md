---
name: scrumia-kotlin-multiplatform-mobile
description: The Kotlin Multiplatform Mobile reference — six rule families that govern how KMP source sets, targets, Cocoapods integration and Gradle wiring compose into one multiplatform module. Use it before changing an expect/actual declaration, the source-set layout, the targets, a pod, or the KMP-shaped Gradle block.
---

# Kotlin Multiplatform Mobile

The six rule families the module contributes are organised by what they govern, not by which target they touch. The authority for each is its own rule file:

| Family | Rule |
|---|---|
| expect/actual declarations | [`${CLAUDE_SKILL_DIR}/../../rules/expect-actual-across-source-sets.md`](${CLAUDE_SKILL_DIR}/../../rules/expect-actual-across-source-sets.md) |
| source-set layout | [`${CLAUDE_SKILL_DIR}/../../rules/source-set-layout.md`](${CLAUDE_SKILL_DIR}/../../rules/source-set-layout.md) |
| platform tests and dependencies | [`${CLAUDE_SKILL_DIR}/../../rules/platform-tests-and-dependencies.md`](${CLAUDE_SKILL_DIR}/../../rules/platform-tests-and-dependencies.md) |
| Cocoapods and Swift interop | [`${CLAUDE_SKILL_DIR}/../../rules/cocoapods-swift-interop.md`](${CLAUDE_SKILL_DIR}/../../rules/cocoapods-swift-interop.md) |
| KMP target declaration | [`${CLAUDE_SKILL_DIR}/../../rules/kmp-target-declaration.md`](${CLAUDE_SKILL_DIR}/../../rules/kmp-target-declaration.md) |
| KMP-shaped Gradle wiring | [`${CLAUDE_SKILL_DIR}/../../rules/kmp-shaped-gradle-wiring.md`](${CLAUDE_SKILL_DIR}/../../rules/kmp-shaped-gradle-wiring.md) |

The module is the **pivot** for Kotlin Multiplatform Mobile in a composition. It re-exports — by configuration, not by code — six satellites (`scrumia-kotlin`, `scrumia-gradle`, `scrumia-ktor`, `scrumia-material3`, `scrumia-effect`, `scrumia-functional-programming`) so a project that declares `tibs245/scrumia:scrumia-kotlin-multiplatform-mobile` reaches both the KMP-specific rules *and* the satellites' rules through one key in `.scrumia/config.yaml`. A project that does not declare the pivot but does declare the satellites still receives their rules unchanged; the pivot is not a prerequisite for any of them.

## The dissociation

The six satellites own their respective concerns:

| Satellite | Owns |
|---|---|
| `scrumia-kotlin` | Kotlin language — coroutines, null-safety, idiomatic style |
| `scrumia-gradle` | Gradle the tool — Kotlin DSL format, version catalogs, task configuration, build cache, plugin management |
| `scrumia-ktor` | HTTP — Ktor routing, content negotiation, auth |
| `scrumia-material3` | UI — Material 3 tokens, components |
| `scrumia-effect` | Effect handling — typed errors, dependency injection through effects |
| `scrumia-functional-programming` | Paradigm — purity, total functions, referential transparency |

This module owns none of those concerns. The KMP-specific rule set covers what is KMP-shaped and only what is KMP-shaped — `expect`/`actual` declarations, the source-set hierarchy, platform-scoped tests and dependencies, Cocoapods and Swift interop, target declaration, and the KMP-shaped Gradle wiring. A rule about Kotlin coroutine idioms in a KMP module belongs to `scrumia-kotlin`; a rule about how the Gradle build resolves version catalogs belongs to `scrumia-gradle`. The split is visible by file structure alone: this module's `extends.json` lists no fragment under a satellite's root, and no satellite's `extends.json` lists a fragment under this one.

## What this module does not do

- **It does not own Kotlin language rules.** Coroutine idioms, null-safety, language conventions are `scrumia-kotlin`'s.
- **It does not own Gradle the tool.** The Kotlin DSL format, version catalogs, task configuration, the build cache, plugin management — those are `scrumia-gradle`'s. This module reads what `scrumia-gradle` exposes, and applies it to KMP-shaped wiring; it does not re-state the DSL rules.
- **It does not ship an executable.** There is no `bin/` and no `dependencies.jsonl` — the pivot's only published name is what `extends.json` declares.
- **It does not open a register named `init`.** No register at all — the module contributes to `implement`, `review` and `find-spec`, and leaves the register vocabulary to the consumer.

## Reading the rules

Each rule file follows the same shape: a one-line summary of the rule, a "What is required" section with the working code, a "What is refused" section with the regression to report, a "Why" grounded in the Kotlin documentation, and a "Sources complémentaires" pointing at the official Kotlin docs the rule cites. The pinned version is the Kotlin documentation as published; a future Kotlin release that changes the rule is a breaking change for the corresponding module rule.

## Source

The rules cite [`https://kotlinlang.org/docs/`](https://kotlinlang.org/docs/), the Kotlin Multiplatform documentation. A rule not stated in the Kotlin docs is not in the module — the plugin does not draw from blog posts, conference talks, or third-party tutorials. The Kotlin documentation is the single source.

The Kotlin Gradle Plugin Manual and the Gradle documentation cover the Gradle-shaped half of `kmp-shaped-gradle-wiring`; the Kotlin docs cover the KMP-shaped half. The split is the same split the module enforces: Kotlin's `kotlin {}` block and the source-set DSL are KMP-shaped, and the convention plugin mechanism is Gradle-shaped.