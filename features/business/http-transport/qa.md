# Acceptance criteria — HTTP transport

One scenario per rule in `business.md`. Each scenario must be able to fail.

A scenario runs on a pure-JVM Ktor codebase that activates `scrumia-ktor`
alone — `scrumia-effect`, `scrumia-gradle` and `scrumia-kotlin-multiplatform-mobile`
are not in the project's `modules` map. The rule the scenario tests is the
rule the scenario exercises; the absence of those three modules is what
proves the rule is not theirs.

## Nominal

### AC-1 — The module activates on a pure-JVM Ktor project with no other satellite

```gherkin
Given a project whose `.scrumia/config.yaml` lists
  `tibs245/scrumia:scrumia-ktor` and no entry under `scrumia-effect`,
  `scrumia-gradle` or `scrumia-kotlin-multiplatform-mobile`
When `scrumia-extends --list` is run
Then `scrumia-ktor` appears in the table; none of the other three does;
  and the `implement`, `review` and `find-spec` registers carry the
  module's directives
```

This is the AC-1 promise: the rule is Ktor's, and a project that does not
run the satellites has the rules. AC-8 is the negative form: this scenario
holds when none of the satellites has merged, which is the proof AC-8
demands.

## Server and client, stated separately

### AC-2 — The module's rules state server and client concerns with a stated line for what they share

```gherkin
Given a developer reading the plugin's `rules/` directory
When they read `routing-is-a-tree`, `content-negotiation`,
  `authentication-is-a-named-provider`, `tests-run-on-the-test-application`
  and `server-configuration-outside-the-code`
Then each rule is named in terms of either the server surface
  (`routing {}`, `install(...)`, `authenticate`) or the client surface
  (`HttpClient`, `expectSuccess`, `ResponseException`); and the rules
  that apply to both (content negotiation) say so explicitly and
  distinguish the two installation sites
```

This is the AC-2 promise: server and client are stated separately, with a
clear line. The line is the installation site (the server's module
function versus the client's construction block) and the types each side
sees (`Application` versus `HttpClient`).

## Eight rule families, each falsifiable

The eight ACs below correspond, in order, to the eight rule families the
issue body names. AC-5's wording is satisfied by their union: each of the
eight rule families carries at least one falsifiable scenario in this file,
and every scenario is runnable on a project that activates `scrumia-ktor`
alone.

### AC-3 — Routing: a route outside the declared tree is a finding

```gherkin
Given a pure-JVM Ktor project with `scrumia-ktor` activated and no
  `scrumia-effect`, `scrumia-gradle` or `scrumia-kotlin-multiplatform-mobile`
When an `intercept(ApplicationCallPipeline.Call)` block is added that
  filters on `call.request.path() == "/users"` and responds directly
Then the `ktor-audit` skill reports a finding under
  `routing-is-a-tree`; the finding is reproducible by a single `grep`
  and survives a re-run of the audit
```

### AC-4 — Content negotiation: a hand-rolled parse beside the plugin is a finding

```gherkin
Given the same project, with `install(ContentNegotiation) { json() }`
  installed in the module function
When a handler is added that calls
  `Json.decodeFromString<CreateUser>(call.receiveText())`
Then the audit reports a finding under `content-negotiation`; the
  finding names the file, the line, and the one-line fix the rule
  prescribes (`call.receive<CreateUser>()`)
```

### AC-5 — HTTP client: a per-call `HttpClient` is a finding

```gherkin
Given the same project, with no `scrumia-effect` and no
  `scrumia-gradle`
When a function is added that constructs `HttpClient(CIO)` inside its
  body and uses it to make one request
Then the audit reports a finding under `http-client-lifecycle`; and
  the same audit reports a second finding if a sibling `HttpClient` is
  built without `expectSuccess = true` in its configuration block
```

### AC-6 — Authentication: a check inside the handler is a finding

```gherkin
Given the same project, with `install(Authentication)` absent and a
  handler that reads `Authorization`, verifies a token by hand, and
  responds `401` on failure
When the audit runs
Then it reports a finding under `authentication-is-a-named-provider`;
  the finding names the handler and the absent `install(Authentication)`
  call the rule prescribes
```

### AC-7 — Test client: a real-port test is a finding

```gherkin
Given the same project, with one test class containing
  `embeddedServer(Netty, port = 8080).start(); delay(500); client.get("http://localhost:8080/...")`
When the audit runs
Then it reports a finding under `tests-run-on-the-test-application`; the
  finding names the test class, the `embeddedServer` call, the `delay`,
  and the localhost `HttpClient.get`, and survives a re-run of the audit
```

### AC-8 — Server configuration: a literal port or secret is a finding

```gherkin
Given the same project, with `fun main() = embeddedServer(Netty, port = 8080)`
  and a `val secret = "s3cr3t-dev-key"` in module code
When the audit runs
Then it reports two findings under
  `server-configuration-outside-the-code` — one for the `embeddedServer`
  call and one for the literal secret
```

### AC-9 — WebSockets and SSE: a protocol that does not fit is a finding

```gherkin
Given the same project, with a `webSocket("/events")` whose body never
  reads an incoming frame and only `send`s server-to-client, and a
  `get("/ticker")` that uses `respondTextWriter(contentType =
  ContentType.Text.EventStream)` with an infinite loop and no
  `id:` line
When the audit runs
Then it reports two findings under
  `websockets-and-sse-each-fit-one-shape` — one for the one-way
  websocket and one for the SSE loop that never reconnects
```

### AC-10 — Observability: a `println` in a handler is a finding

```gherkin
Given the same project, with `println("GET /orders ...")` in a handler
  and a sibling handler that does `MDC.put("userId", id)` without
  clearing it
When the audit runs
Then it reports two findings under
  `observability-is-the-call-logging-plugin` — one for the `println`
  and one for the uncleared MDC
```

## The dissociation

### AC-11 — An HTTP-status-to-`Result.failure` is named as misplaced, not as a `scrumia-ktor` rule to follow

```gherkin
Given the same project, with a client function whose return type is
  `Result<User>` and whose body converts on
  `r.status.isSuccess()` to either `Result.success(r.body())` or
  `Result.failure(UserNotFound(id))` for every non-2xx
When the audit runs
Then it reports a finding under `http-status-is-not-effect-semantics`
  stating that the conversion is unnamed, non-exhaustive over
  `expectSuccess = true`'s exception types, and conflates
  HTTP-status with domain semantics; and a second test asserts that the
  finding's `read` field points at
  `plugins/scrumia-ktor/rules/http-status-is-not-effect-semantics.md`
  and nowhere in `scrumia-effect` — the rule is Ktor's to state, the
  paradigm is the next module's
```

This is the AC-7 promise: a rule that conflates the two is named as
misplaced, and the placement of the rule (this module) is the placement of
the dissociation it states.

## Module shape

### AC-12 — The module passes the anatomy check

```gherkin
Given the project with `scrumia-ktor` activated
When `python3 plugins/scrumia-core/bin/scrumia-module check
  plugins/scrumia-ktor --json` is run
Then the verdict's `state` is `clean` and the `findings` list is empty;
  and `python3 tools/validate.py` exits `0`
```

This is the AC-4 promise: the manifest, README, rules, audit skill, and
extension data all pass the shape `scrumia-core` enforces, and
`tools/validate.py` reports no error against the module.

### AC-13 — Every contribution's fragment path lands inside `plugins/scrumia-ktor/`

```gherkin
Given the module's `extends.json` contributing to `implement`, `review`
  and `find-spec`
When each `read` value is resolved relative to the module's root
Then every resolved path is under `plugins/scrumia-ktor/`
```

This is the AC-6 promise: the contribution's fragment is local to the
module, and `scrumia-extends` rendering of the register table shows the
file path the rule is in.

## The independence guarantee

### AC-14 — The module's `qa.md` is the only place these scenarios live

```gherkin
Given the same project, with no `scrumia-effect`, `scrumia-gradle` or
  `scrumia-kotlin-multiplatform-mobile` in `modules`
When `grep -RIn "routing-is-a-tree" --include="*.md" features/` is run
Then the only match is the link in `features/business/http-transport/qa.md`
  to `plugins/scrumia-ktor/rules/routing-is-a-tree.md`; no other
  feature's `business.md` or `qa.md` restates the rule
```

This is the AC-8 promise: `scrumia-ktor` is the only module whose
documents own the Ktor rules, and the other satellites do not pre-empt
them. A satellite that lands later (`scrumia-effect`,
`scrumia-kotlin-multiplatform-mobile`, `scrumia-gradle`) will only add
its own concerns: effect semantics, KMM interop, build wiring. The Ktor
rules are not theirs.
