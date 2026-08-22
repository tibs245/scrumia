# Spec keys this module answers to

The `scrumia-specs` register `find-spec` is asked for when an agent is
locating the feature a rule belongs to. The keys below name what
`scrumia-ktor` answers for. A question that does not match is not this
module's: a question about an HTTP-style typed error returns nothing from
this register and is the next module's to answer.

## Routing and surface

- `routing-tree` — the application's surface is one `routing {}` block, split
  into nested `route` calls, each an extension function or a call into one.
  Refusal: `routing-is-a-tree`.
- `route-prefix` — a path segment shared by sibling routes (`/api/v1`) is
  declared once, on the parent route, not repeated on every leaf.
  Refusal: `routing-is-a-tree`.

## Content and serialization

- `content-negotiation` — the application installs `ContentNegotiation` once;
  handlers do not call `Json.decodeFromString` on `call.receiveText()`.
  Refusal: `content-negotiation`.
- `serializer-config` — the configuration of the chosen serializer
  (`ignoreUnknownKeys`, `explicitNulls`, naming) is set where the plugin is
  installed, not at the call site. Refusal: `content-negotiation`.

## The HTTP client

- `httpclient-lifecycle` — one `HttpClient` per remote dependency, held for
  the application's lifetime, closed with it.
  Refusal: `http-client-lifecycle`.
- `client-configuration` — client plugins (`ContentNegotiation`, `Logging`,
  `HttpRequestRetry`) are installed in the client's configuration block at
  construction; `expectSuccess` is stated there too.
  Refusal: `http-client-lifecycle`.
- `response-validation` — `expectSuccess = true` is set, and non-2xx becomes
  a `ResponseException`; the application's typed-error discipline decides
  what to do with it. Refusal: `http-client-lifecycle`,
  `http-status-is-not-effect-semantics`.

## Authentication

- `authentication-providers` — authentication is a named provider installed
  in `install(Authentication) { ... }`, applied by `authenticate("name") {}`.
  Refusal: `authentication-is-a-named-provider`.
- `principal-extraction` — once `authenticate {}` has run, the principal
  comes from `call.principal<T>()`; the route does not re-validate the
  token. Refusal: `authentication-is-a-named-provider`.

## Testing

- `test-application` — a route is tested through `testApplication`, on the
  in-memory engine; no port, no `embeddedServer.start()`, no `delay`.
  Refusal: `tests-run-on-the-test-application`.
- `test-client` — the test's `createClient {}` is configured the same way
  the application's client is. Refusal: `tests-run-on-the-test-application`.

## Server configuration

- `engine-main` — the entry point is `EngineMain.main(args)`, reading
  `application.conf`; the module function is engine-agnostic.
  Refusal: `server-configuration-outside-the-code`.
- `config-external` — a port, a host, a database URL, a JWT secret, an
  external base URL is read from `environment.config` and overridable by
  an environment variable; no default for a secret.
  Refusal: `server-configuration-outside-the-code`.

## WebSockets and SSE

- `streaming-protocol` — a streaming route declares the protocol it uses
  (`webSocket` or `Content-Type: text/event-stream`) and the choice fits
  the shape of the traffic (bidirectional vs server-to-client only).
  Refusal: `websockets-and-sse-each-fit-one-shape`.

## Observability

- `call-logging` — request logging is `install(CallLogging) { ... }` with a
  filter, a level and a format; no `println` inside a handler.
  Refusal: `observability-is-the-call-logging-plugin`.
- `tracing-bridge` — an external tracer is plugged in through the
  `OpenTelemetry` plugin and the tracer adapter; the application does not
  invent a tracer. Refusal: `observability-is-the-call-logging-plugin`.

## Where the line sits

- `status-to-typed-error` — a non-2xx is converted into a domain error in
  one named place, on the client side, exhaustive over what
  `expectSuccess = true` produces; the conversion does not live in a
  handler and does not live in `HttpClient`'s configuration block.
  Refusal: `http-status-is-not-effect-semantics`.

The keys whose refusal is `http-status-is-not-effect-semantics` are the
ones `scrumia-effect` (or whatever the project uses for typed errors)
extends with. A question about how a domain error is *modelled* is not
in this register — it is the next module's, and answering it from here
would conflate library and paradigm, the dissociation this module exists
to defend.
