# The HttpClient is built once and configured at construction

*Refusal.* An `HttpClient` created inside a function that runs per request or
per call, and a client whose plugins are configured anywhere other than its
construction block.

## What is refused

```kotlin
// ❌ a new engine, a new connection pool and a new thread pool, per call
suspend fun fetchUser(id: String): User {
    val client = HttpClient(CIO)
    return client.get("https://api.example.com/users/$id").body()
}
```

Also refused: a client built once and never closed on shutdown, and
`expectSuccess` left unstated — the default is `false`, so a 500 comes back as a
response object and the failure only surfaces when the body fails to
deserialise.

## What is written instead

One client per remote dependency, held for the application's lifetime, closed
with it, and configured where it is built:

```kotlin
val client = HttpClient(CIO) {
    expectSuccess = true            // stated, not inherited from a default nobody read
    install(ContentNegotiation) { json() }
    install(Logging) { level = LogLevel.INFO }
    install(HttpRequestRetry) {
        retryOnServerErrors(maxRetries = 3)
        exponentialDelay()
    }
    defaultRequest { url("https://api.example.com/") }
}

// and, wherever the application's lifetime ends:
monitor.subscribe(ApplicationStopped) { client.close() }
```

`expectSuccess = true` turns a non-2xx into a `ResponseException`. Whether that
exception is then caught and mapped is not this module's question — see
[`http-status-is-not-effect-semantics`](http-status-is-not-effect-semantics.md).

## Why

An `HttpClient` owns an engine, a connection pool and a coroutine scope.
Constructing one per call throws away keep-alive, re-resolves DNS, and leaks
threads under load — the symptom is a service that is fine in tests and exhausts
file descriptors in production. Configuring plugins at construction is what makes
the client's behaviour readable in one place: retry policy, logging level and
serializer are properties of the dependency, not of the call site.

## Sources complémentaires

- `https://ktor.io/docs/client-create-and-configure.html` — creating a client, engines, closing it. Version pin: **Ktor 3.x**.
- `https://ktor.io/docs/client-response-validation.html` — `expectSuccess` and `ResponseException`. Version pin: **Ktor 3.x**.
- `https://ktor.io/docs/client-retry.html` — `HttpRequestRetry`. Version pin: **Ktor 3.x**.
