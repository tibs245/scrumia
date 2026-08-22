# A route is tested through `testApplication`, on the in-memory engine

*Refusal.* A test that binds a port, sleeps for a server to come up, or points
an `HttpClient` at `http://localhost:8080`.

## What is refused

```kotlin
// ❌ a real port, a real socket, and a race between the two
@Test
fun `users are listed`() = runBlocking {
    val server = embeddedServer(Netty, port = 8080) { module() }.start()
    delay(500)
    val response = HttpClient(CIO).get("http://localhost:8080/users")
    assertEquals(HttpStatusCode.OK, response.status)
    server.stop()
}
```

## What is written instead

```kotlin
@Test
fun `users are listed`() = testApplication {
    application { module() }                       // the same module main() installs

    val client = createClient {
        install(ContentNegotiation) { json() }     // the test client is configured too
    }

    val response = client.get("/users")
    assertEquals(HttpStatusCode.OK, response.status)
    assertEquals(listOf(alice), response.body<List<User>>())
}
```

`testApplication` runs the application on the in-memory engine: no port, no
socket, no wait. `client` — or a `createClient {}` when the test needs plugins —
talks to it directly. An authenticated route is tested by sending the header the
provider expects, not by disabling the provider.

## Why

A port makes a test suite serial, flaky and machine-dependent: two suites
running in parallel collide, CI picks a port that is already taken, and the
`delay` that hides the startup race is either too short on a loaded runner or
wasted time on every run. The in-memory engine removes the network from a test
whose subject was never the network — what is under test is the route tree, the
negotiation and the handler.

Testing across a real socket is a different activity with a different name, and
it belongs to whatever the project uses for end-to-end coverage — not to the
tests that accompany a route.

## Sources complémentaires

- `https://ktor.io/docs/server-testing.html` — `testApplication`, `client`, `createClient`, the in-memory engine. Version pin: **Ktor 3.x**.
