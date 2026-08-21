# scrumia-ktor

HTTP server and client rules for a Ktor codebase, covering the eight rule
families Ktor owns — routing, content negotiation, the `HttpClient` lifecycle,
authentication, the in-memory test client, server configuration, WebSockets and
SSE, and call logging — plus a ninth that keeps HTTP status out of the
application's typed-error discipline. The library is the subject; the
paradigm is not.

## What it answers

How does a Ktor codebase look when the rules it follows are written down —
where the route tree lives, what `ContentNegotiation` is for, how an
`HttpClient` is built once and closed once, why a `testApplication` is the
test of a route, and where the line sits between "the network said 4xx" and
"the domain said no". The HTTP shape is the library's; the functional
discipline that informs error handling is a different module's, and this
module's ninth rule is the seam between the two.

## What it refuses

- A route registered outside the application's `routing {}` tree, or a
  handler that carries the work instead of calling into it.
- A `Json.decodeFromString` on `call.receiveText()` in an application that
  installs `ContentNegotiation`. The plugin is the seam; the hand-rolled
  parse is the bypass.
- An `HttpClient` constructed per call, or one whose plugins are
  configured anywhere other than its construction block — and the absence
  of `expectSuccess = true` on a client whose calls are checked by status.
- An `Authorization` header read inside a handler, or a single unnamed
  authentication provider for two audiences that need different validation.
- A test that opens a port, sleeps for a server, or points an `HttpClient`
  at `http://localhost`. `testApplication` exists; the real port does not
  belong to a route test.
- A port, a host, a JWT secret, a database URL, or an external base URL
  written as a literal in Kotlin. `EngineMain` reads `application.conf`;
  the module function reads what it is given.
- A `webSocket {}` whose body never reads a frame, or a
  `respondTextWriter` with `Content-Type: text/event-stream` and an
  infinite loop that never reconnects. The protocol is the route's first
  property.
- A `println` inside a handler, an MDC put that is never cleared, or a
  `CallLogging` without a `filter`. The plugin is the logging seam; the
  application is not.
- A `Result.failure` whose body is `r.status` — the channel is the
  application's, and what the network said is the input, not the output.

## What it ships

| What | Role |
|---|---|
| `rules/routing-is-a-tree.md` | The application's surface is one `routing {}` block, split into nested `route` extension functions. |
| `rules/content-negotiation.md` | `ContentNegotiation` is installed once per application and per client, with one shared serializer configuration. |
| `rules/http-client-lifecycle.md` | One `HttpClient` per remote dependency, built once, closed once, configured at construction. |
| `rules/authentication-is-a-named-provider.md` | Authentication is `install(Authentication) { name -> ... }`; routes wrap in `authenticate("name") {}` and read the principal. |
| `rules/tests-run-on-the-test-application.md` | A route is tested through `testApplication {}`, on the in-memory engine. |
| `rules/server-configuration-outside-the-code.md` | Ports, hosts, secrets and URLs come from `environment.config` and are overridable by environment variables. |
| `rules/websockets-and-sse-each-fit-one-shape.md` | A streaming route states which protocol it uses, and the choice fits the shape of the traffic. |
| `rules/observability-is-the-call-logging-plugin.md` | Request logging is `install(CallLogging)` with a filter and a format; tracing is the `OpenTelemetry` plugin and a stated tracer. |
| `rules/http-status-is-not-effect-semantics.md` | A non-2xx is converted into a domain error in one named place on the client, exhaustive over what `expectSuccess = true` produces. |
| `skills/ktor-audit/SKILL.md` | Nine questions, one per rule family, that find each failure mode in an existing codebase. |
| `rules/ktorspec-finding-keys.md` | The keys this module answers to on the `find-spec` register — what an agent looks up when a question is about Ktor. |

The nine rules reach the `implement` and `review` registers through
`extends.json`, so they apply while a route is written and again while it is
reviewed, without being written twice. The `find-spec` register gains a
mapping from a question to the rule that answers it.

## Sources

| Source | Pinned to |
|---|---|
| [`https://ktor.io/docs/welcome.html`](https://ktor.io/docs/welcome.html) | **Ktor 3.x** |

Every rule cites this source and nothing else — no blog post, no tutorial,
no community pattern. The pin is the contract: the plugin manifest, the
test client shape and the `respondTextWriter` SSE API differ between
Ktor 2.x and 3.x, so a rule written against 2.x raises false positives
on a 3.x codebase. `ktor-audit` checks the target's major version first
and reports the drift instead of the findings.

## What it expects to find

A Kotlin codebase with Ktor as a dependency, on the server or the client
or both. Nothing else — the rules are about a library, not a stack. A
pure-JVM service, a Ktor-on-Android client, a Kotlin/JS browser app: any
of these activates `scrumia-ktor` alone.

The default composition leaves the build wiring of Ktor to
`scrumia-gradle`. Activating `scrumia-ktor` does not pull the dependency,
declare a version, or open a single file in `build.gradle.kts`; the
project's own build module, or its absence, owns that.

A project that adopts the typed-error pattern reaches for `scrumia-effect`
to write the conversion `http-status-is-not-effect-semantics` defers to —
the named place the rule says the conversion lives. `scrumia-ktor` does
not depend on `scrumia-effect`; the two compose by each saying what the
other does not.

`scrumia-kotlin-multiplatform-mobile` is not a dependency either. The
rules are about Ktor, not the platforms it runs on; a Ktor project that
does not target iOS pays no cost, and a Kotlin Multiplatform Mobile
project that does activate `scrumia-ktor` gets the Ktor lane and the
KMM lane from two independent modules.

## Not shipped yet

No `ktor-refactor`. The audit finds each failure mode and a human fixes
each — there is no automated pass that rewrites a `Json.decodeFromString`
into a `call.receive<T>()` or moves a `println` into `CallLogging`. The
detectors are `grep`-based rather than tree-sitter queries: they find the
suspect line and not the value the line returns, which is why the audit
ends in judgment on the line, not in a verdict. A tree-sitter
implementation is the next milestone for this module, not a maybe.
