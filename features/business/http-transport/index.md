# HTTP transport

**Status**: draft

## In brief

HTTP server and client rules for a Ktor codebase, applicable to a pure-JVM
service, a Ktor-on-Android client, or a Kotlin/JS browser app. The eight rule
families Ktor owns — routing, content negotiation, the `HttpClient` lifecycle,
authentication, the in-memory test client, server configuration, WebSockets and
SSE, and call logging — are stated once, in one plugin, and a ninth rule keeps
HTTP status out of the application's typed-error discipline. The plugin that
carries it (`scrumia-ktor`) targets Ktor alone — the build wiring of the
dependency lives in `scrumia-gradle`, and the typed-error paradigm lives in
`scrumia-effect`. Authoritative source: `https://ktor.io/docs/welcome.html`.

## Links

- Implemented by: `plugins/scrumia-ktor/` — `extends.json` contributes
  refusal rules to the `implement` and `review` registers, plus a `find-spec`
  mapping for the keys the module answers to.
- Authority: `https://ktor.io/docs/welcome.html` — the plugin's README cites
  it and pins the version the rules were written against (**Ktor 3.x**).
- Defers to: `features/business/modular-composition/` for the contract every
  ScrumIA module owes — the manifest's fields, the `extends.json` shape, the
  README sections. This feature is what the module owns; the shape is
  modular-composition's.
- Defers to: `features/business/feature-format/` for the angle catalogue and
  the rule that the feature files follow. This feature is not a PRD.
- Boundary: `features/business/runtime-validation/` for the parallel a Ktor
  project composes with when it adds Zod to the wire format. The two
  plugins compose independently; the pair is documented but neither requires
  the other.
- Boundary: `scrumia-gradle` (a module of this project's own composition) for
  the build wiring of Ktor as a dependency. `scrumia-ktor` does not open a
  single file in `build.gradle.kts`, declare a version, or activate
  `expectedBy`; the project's build module owns that. A Ktor project that
  runs no `scrumia-gradle` activates `scrumia-ktor` alone.

## Files present

| File | Read it when |
|---|---|
| `business.md` | Deciding what the plugin refuses, what it requires, and why HTTP-status dissociation matters |
| `qa.md` | Writing or running the acceptance scenarios for the Ktor rules |
| `tech.md` | Tracing how the plugin contributes to the `implement`, `review` and `find-spec` registers |
| `CHANGELOG.md` | History of changes to this spec |

No `ux.md`: a server/client library carries no interface. No `legal.md`,
`security.md`: the rules do not encode a regulatory requirement or a security
control beyond what the library's own documentation states, and what they state
is `ktor.io`'s, not a project's.
