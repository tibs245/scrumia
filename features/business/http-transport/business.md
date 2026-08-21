# HTTP transport — business rules

## Value

For whoever builds a Ktor codebase — a server, a client, a service that does
both — the shape the library asks for, stated as refusal rules a reviewer
can read: routes declared as a tree, content negotiation installed once, an
`HttpClient` built once and closed once, named authentication providers,
tests on the in-memory engine, configuration outside the code, WebSockets and
SSE each used where they fit, and observability through `CallLogging`. It
matters because Ktor's defaults are permissive: a missing `expectSuccess` is
a silent failure, a hand-rolled `Json.decodeFromString` bypasses the
serializer's configuration, a `println` inside a handler is a logging seam
that nothing else can read. Not instrumented today: nothing counts how many
Ktor codebases ship with the per-call `HttpClient` or the real-port test,
because the failure is silent until load.

## Sources

This module's authority is the library's own documentation, not community
advice. Every rule the plugin ships cites the source below; a rule without a
citation is not shipped, and a citation that drifts is rewritten against the
version the rules were pinned against.

| Source | URL | What it provides |
|---|---|---|
| Ktor documentation | `https://ktor.io/docs/welcome.html` | The complete server and client reference: routing, serialization, the `HttpClient` and its plugins, authentication providers, the in-memory test engine, `EngineMain` and `application.conf`, WebSockets, SSE, `CallLogging`, OpenTelemetry. The plugin pins to the major version the rules were written against; the citation is the link, the pin is the contract. |

The plugin does not draw from blog posts, conference talks, or third-party
tutorials. The library's own documentation is the single source — a rule
not stated there is not in the plugin.

## The module's role

The module's business rules are statements about *what this module is and
what it does for the project that adopts it*. They are not a list of good
practices — those live in the plugin's `rules/` directory, one file per
behavioural rule, each citing the source above.

- **BR-1** — The module can be taken directly by a project that does not
  run `scrumia-impl-reactjs` or `scrumia-impl-solidjs`. A pure-JVM service,
  a Ktor-on-Android client, a Kotlin/JS browser app, a CLI that talks to a
  Ktor server: any of these activates `scrumia-ktor` alone. The rules are
  about a library, not a stack.

- **BR-2** — The module extends the `implement`, `review` and `find-spec`
  registers. A project running `scrumia-ktor` gains the rules while writing
  Ktor code, again while reviewing it, and the `find-spec` mapping when an
  agent is looking up a Ktor question. A project running neither extension
  point pays no cost.

- **BR-3** — Every rule the module ships cites the Ktor documentation —
  never a blog post, never a tutorial, never a community pattern. A rule
  whose citation has drifted from the pinned version is rewritten; a rule
  the documentation no longer states is removed, not paraphrased.

- **BR-4** — The module helps a Ktor codebase carry solid notions of HTTP
  wiring. "Solid" means grounded in the library's documented API, applied
  to the library's surface rather than the application's domain, and
  reasoned about in terms of the library's own abstractions
  (`Application`, `HttpClient`, `Route`, `Principal`, `ApplicationConfig`)
  — not fashionable, not "defensive", not framework-specific.

- **BR-5** — The module anchors HTTP wiring in the library's own seams,
  not in ad-hoc defensive layers. Authentication is `install(Authentication)`
  with a named provider, not a header check inside a handler. Logging is
  `install(CallLogging)` with a filter, not a `println` inside a handler.
  Serialization is `install(ContentNegotiation)`, not a
  `Json.decodeFromString` on `call.receiveText()`. The seam is the plugin;
  the bypass is the failure mode.

- **BR-6** — The module states the eight rule families Ktor owns —
  routing, content negotiation, HTTP client, authentication, test client,
  server configuration, WebSockets and SSE, observability — and a ninth
  rule for the dissociation that keeps HTTP status out of the
  application's typed-error discipline. Each rule family carries at
  least one falsifiable scenario in `qa.md` (AC-5), and the dissociation
  is named as the line this module defends (AC-7).

- **BR-7** — The module does not own the build wiring of Ktor. The
  dependency declaration, the version pin, the engine choice and any
  `expectedBy` configuration live in `scrumia-gradle` (or in the
  project's own build file, when no ScrumIA build module is active).
  `scrumia-ktor` opens no file under `build.gradle.kts`; the project that
  activates both modules reaches the build wiring through
  `scrumia-extends --settings build`.

- **BR-8** — The module does not own the typed-error paradigm. A non-2xx
  is a non-2xx, and the application decides how to model that. The
  ninth rule states the conversion is named, exhaustive and on the
  client side; the conversion itself is the next module's
  (`scrumia-effect`, or whatever the project uses). `scrumia-ktor` says
  where the conversion lives, not how to write it.

- **BR-9** — The module does not own the Kotlin language constructs used
  inside Ktor handlers. A handler that uses a coroutine, a sealed class,
  an extension function on `Route` follows Kotlin rules from
  `scrumia-kotlin`. The Ktor rules state what the *handler* does to
  *Ktor*, not what the code inside it does to Kotlin.

- **BR-10** — The module does not own Kotlin Multiplatform-specific
  interop. A Ktor client on iOS or a Ktor server on watchOS follows
  Ktor's KMM documentation; `scrumia-ktor` does not restate it. The
  dissociation is what makes `scrumia-ktor` landable and mergeable
  independently of `scrumia-kotlin-multiplatform-mobile` (AC-8).

## Settings

This module reads no settings. The Ktor configuration block
(`install(ContentNegotiation)`, `install(Authentication)`, `defaultRequest`)
is project code, not ScrumIA settings; `application.conf` is the project's
file, not the module's. A `scrumia-ktor` rule that requires a
configuration value is a rule that names the configuration key, not a rule
that reads ScrumIA's own settings register.

## The dissociation, stated once

A rule that conflates HTTP-status with effect semantics (a `Result.failure`
whose body is `r.status`, a handler that catches a domain error and responds
`404` without naming which domain error) is named as misplaced. This module
owns HTTP wiring; the typed-error pattern is `scrumia-effect`'s. The
defence is the ninth rule, `http-status-is-not-effect-semantics`, and it is
the line the module exists to hold.
