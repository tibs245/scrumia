# Changelog — scrumia-ktor

All notable changes to this module, on [Keep a Changelog 1.0.0](https://keepachangelog.com/en/1.0.0/).

## [0.1.0] - 2026-08-22
### Added
- The module, carrying the `http-transport` capability: nine refusal rules
  covering the eight rule families Ktor owns plus the dissociation that
  keeps HTTP status out of the application's typed-error discipline.
- `routing-is-a-tree` — the application's surface is one `routing {}` block,
  split into nested extension functions, never scattered as interceptors
  or pipeline phases.
- `content-negotiation` — `ContentNegotiation` is installed once per
  application and per client, with one shared serializer configuration;
  `Json.decodeFromString` on `call.receiveText()` is refused.
- `http-client-lifecycle` — one `HttpClient` per remote dependency, held
  for the application's lifetime, closed with it; `expectSuccess` and
  plugins are stated where the client is built.
- `authentication-is-a-named-provider` — authentication is
  `install(Authentication) { name -> ... }`; routes wrap in
  `authenticate("name") {}` and read the principal, the check never lives
  in the handler.
- `tests-run-on-the-test-application` — a route is tested through
  `testApplication {}`, on the in-memory engine; no port, no
  `embeddedServer.start`, no `delay`, no localhost `HttpClient`.
- `server-configuration-outside-the-code` — ports, hosts, secrets and
  URLs come from `environment.config` and are overridable by environment
  variables; `EngineMain` is the entry point.
- `websockets-and-sse-each-fit-one-shape` — a streaming route states
  which protocol it uses, and the choice fits the shape of the traffic
  (bidirectional vs server-to-client only).
- `observability-is-the-call-logging-plugin` — request logging is
  `install(CallLogging) { ... }` with a filter, a level and a format;
  tracing is the `OpenTelemetry` plugin and a stated tracer.
- `http-status-is-not-effect-semantics` — a non-2xx is converted into a
  domain error in one named place on the client, exhaustive over what
  `expectSuccess = true` produces; the channel is the application's, not
  the network's. This is the dissociation `scrumia-ktor` is named for.
- `ktor-audit` — a skill auditing an existing Ktor codebase against the
  nine rules, which establishes the target's Ktor major version before
  reporting anything.
- `ktorspec-finding-keys` — the `find-spec` mapping for the keys this
  module answers to.
- Rules are written against **Ktor 3.x** and cite
  `https://ktor.io/docs/welcome.html`. On a 2.x codebase the audit
  reports the version gap rather than the findings: the plugin manifest,
  the test client shape and the SSE API differ.
