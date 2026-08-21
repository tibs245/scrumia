---
name: ktor-audit
description: Audit a Ktor codebase against the nine rule families this module ships — routing declared as a tree, content negotiation installed once, a long-lived HttpClient, named authentication providers, tests on the in-memory engine, configuration outside the code, WebSockets vs SSE stated, observability through CallLogging, and HTTP status kept out of effect semantics. Use it before adopting the module on an existing codebase, when a Ktor-shaped bug ships, or to check a new route against the rules before review.
---

# Auditing a Ktor codebase

Nine questions, one per rule family. Answer them in order, file by file — the
first eight are read from the code, the ninth starts from the code and ends in
judgment. Report findings; change nothing without being asked.

Every rule this module ships is written against **Ktor 3.x**. Establish the
target's major version first, from the project's build file:

```bash
grep -E "io\.ktor:|ktor-version" build.gradle.kts gradle/libs.versions.toml
```

On **Ktor 2.x**, stop and say so. The plugin manifest is different
(`Auth` versus `Authentication`, `CallLogging` configuration, the
`respondTextWriter` SSE shape), and the test client moved to
`createClient {}`. Report the version gap as the finding, and ask whether the
project intends to migrate or wants the rules refreshed for 2.x.

## 1 — Is the surface a declared tree?

Rule: [`routing-is-a-tree`](../../rules/routing-is-a-tree.md).

Find the application's `routing {}` block — the call from the module
function, in the file `EngineMain` points at. The tree under it should be the
only place a path is registered.

Then check every file the project ships for other registrations:

```bash
grep -RInE "routing \{|intercept\(|route\(" --include="*.kt" src
```

A registration outside the tree — `routing {}` in a different file, an
`intercept(ApplicationCallPipeline.Call)` that filters on path, a nested
prefix spelled out on every leaf — is a finding.

## 2 — Is content negotiation installed once?

Rule: [`content-negotiation`](../../rules/content-negotiation.md).

Find the `install(ContentNegotiation)` call — there should be one on the
server and one on each `HttpClient` that deserialises. Then:

```bash
grep -RInE "Json\.decodeFromString|Json\.encodeToString|ObjectMapper" --include="*.kt" src
```

A `Json.decodeFromString` on `call.receiveText()` (or `receiveStream()`), or a
Jackson mapper built inside a handler, is a finding.

## 3 — Is the HttpClient built once and configured at construction?

Rule: [`http-client-lifecycle`](../../rules/http-client-lifecycle.md).

Find every `HttpClient(`:

```bash
grep -RIn "HttpClient(" --include="*.kt" src
```

Each occurrence should be inside a top-level `val` (or a single
`createClient {}` for tests). A `HttpClient(` inside a function body, a
`runBlocking`, or an `init {}` of a class that is constructed per call, is a
finding. So is a `client` with no `expectSuccess` property set anywhere in
its construction block.

## 4 — Is authentication a named provider?

Rule: [`authentication-is-a-named-provider`](../../rules/authentication-is-a-named-provider.md).

Find the `install(Authentication)` call and every `authenticate(`:

```bash
grep -RInE "install\(Authentication\)|authenticate\(" --include="*.kt" src
```

A `validate { }` block should return a principal (or `null` to refuse); a
handler that reads `Authorization` and verifies a token by hand, a single
unnamed provider used for two audiences that need different validation, and
a `validate { }` that throws, are all findings.

## 5 — Are tests on the in-memory engine?

Rule: [`tests-run-on-the-test-application`](../../rules/tests-run-on-the-test-application.md).

Find the tests:

```bash
grep -RInE "testApplication|embeddedServer\(" --include="*.kt" src test
```

A test with `embeddedServer(` followed by `.start()` (or `.start(wait =`),
a `@BeforeAll` that opens a port, or an `HttpClient` pointed at
`http://localhost`, is a finding. So is a `testApplication` block whose
`createClient` is the default client rather than a configured one.

## 6 — Is configuration outside the code?

Rule: [`server-configuration-outside-the-code`](../../rules/server-configuration-outside-the-code.md).

Find the entry point and the module function:

```bash
grep -RInE "fun main\(|EngineMain\.main|embeddedServer\(" --include="*.kt" src
```

An `embeddedServer(Netty, port = <literal>` is a finding. A module function
that reads `environment.config.property("...")` is the right shape. Then:

```bash
grep -RInE "(secret|password|token|api[_-]?key)\s*=\s*\"" --include="*.kt" src
```

A literal secret or token (in any form) in Kotlin source is a finding.

## 7 — Are WebSockets and SSE each used where they fit?

Rule: [`websockets-and-sse-each-fit-one-shape`](../../rules/websockets-and-sse-each-fit-one-shape.md).

Find streaming routes:

```bash
grep -RInE "webSocket|respondTextWriter|ContentType\.Text\.EventStream" --include="*.kt" src
```

A `webSocket` whose body never reads a frame is an SSE use case; a
`respondTextWriter` with `Content-Type: text/event-stream` and an infinite
loop, with no reconnect hint and no event id, is a websocket use case. Each
is a finding.

## 8 — Is observability through `CallLogging`?

Rule: [`observability-is-the-call-logging-plugin`](../../rules/observability-is-the-call-logging-plugin.md).

Find logging:

```bash
grep -RInE "println\(|System\.out|CallLogging|OpenTelemetry" --include="*.kt" src
```

A `println` or `System.out` inside a handler is a finding. So is a
`CallLogging` without a `filter { call -> ... }` (the probe at INFO is
load-bearing), and an MDC put in a handler that is never cleared.

## 9 — Is the HTTP status kept out of effect semantics?

Rule: [`http-status-is-not-effect-semantics`](../../rules/http-status-is-not-effect-semantics.md).

Find the client calls and their results:

```bash
grep -RInB1 -A6 "Result\.(success|failure)" --include="*.kt" src
```

A client function whose return type is `Result<T>` and whose body only
converts on `r.status.isSuccess()` (or any other status check) is a finding —
the conversion does not distinguish which 4xx means which domain error, and
a 5xx collapses into the same channel. A catch-all `catch (e: Exception) {
Result.failure(e) }` beside it is the same finding: the channel claims domain
and carries network.

## Report

For each finding, name the file, the line, the rule, and the one-line fix
the rule prescribes. Group findings by rule so the report reads as a list of
decisions the agent is asking the human to make, not a flat list of
violations.
