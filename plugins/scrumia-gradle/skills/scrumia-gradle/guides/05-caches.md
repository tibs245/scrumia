# Caches on by default

> `org.gradle.caching=true` and `org.gradle.configuration-cache=true` are set in `gradle.properties`. Each rule names what it breaks when enabled.

## Prerequisites

None — the caches are properties of `gradle.properties`, not of the build script.

## Rules

### Rule 1: Build cache is enabled

`org.gradle.caching=true` is set in `gradle.properties`. The build cache lets Gradle
reuse task outputs across builds, branches and machines (when a remote cache is
configured).

```properties
# gradle.properties — the build cache flag
org.gradle.caching=true
```

A `gradle.properties` without the flag, or with `org.gradle.caching=false`, is a
finding the audit names.

**What breaks.** Tasks that produce non-deterministic output — anything that depends
on wall-clock time, on a random seed, or on the order inputs are read in — will
return stale outputs from the cache when the inputs are unchanged. The build cache
assumes a task's output is a function of its inputs; a task that violates that
assumption has to opt out with `@DisableCachingByDefault` or be marked with
`@CacheableTask` once the inputs are pinned.

### Rule 2: Configuration cache is enabled

`org.gradle.configuration-cache=true` is set in `gradle.properties`. The
configuration cache lets Gradle reuse the configuration phase across builds.

```properties
# gradle.properties — the configuration cache flag
org.gradle.configuration-cache=true
```

A `gradle.properties` without the flag, or with `org.gradle.configuration-cache=false`,
is a finding the audit names.

**What breaks.** Configuration-time side effects — `tasks.create` for tasks the graph
does not need, direct file reads outside a `TaskInput`, calls to `project.logger`
from a `doFirst { … }` block, anything that touches the build's working directory
during the configuration phase — turn the configuration cache into a non-conformant
configuration the next time it tries to reuse the cached result. Each is a finding
the audit raises separately; this rule names the cache, the guides on tasks and
configuration shape name the behaviours.

### Rule 3: Both caches are on, on the same project

A project that enables one without the other pays the cost of the one without the
benefit of the other. The build cache reuses task outputs; the configuration cache
reuses configuration work. Together they are what makes a second build of the same
project fast, and a CI re-run that follows a `main` rebase cheaper than the first
run was.

### Rule 4: Caches do not absolve the project of input/output hygiene

A task that touches the network, the clock, or the build's working directory at
config time is broken whether or not the cache is on. The cache is a fast path; the
input/output discipline that makes a cache valid is the rule
[04-task-configuration](04-task-configuration.md) governs.

## Why

A Gradle build that runs cold every time is a build whose red-green loop is bounded
by the slowest configuration phase. The two caches push that loop down: the
configuration cache amortises the work the build script does; the build cache
amortises the work the tasks do. Both are off by default in Gradle 8 and earlier
because they require the build script to be configuration-cache-clean and the tasks
to be `@CacheableTask`. The cost of turning them on is what the project pays once;
the benefit compounds with every subsequent build.

## Sources complémentaires

- [Gradle — Build cache](https://docs.gradle.org/current/userguide/build_cache.html) —
  the reference for `org.gradle.caching` and the local + remote cache topology.
- [Gradle — Configuration cache](https://docs.gradle.org/current/userguide/configuration_cache.html) —
  the reference for `org.gradle.configuration-cache` and what breaks the cache.
