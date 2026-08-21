# An HTTP status is not a `Result.failure`

*Refusal.* A Ktor handler that, on receiving a non-2xx, wraps the body in
`Result.failure` — or a caller that, on receiving a non-2xx, treats it as a
typed error of the application's domain. The HTTP status is the network's
verdict on the request; the application's domain errors are something else.

## What is refused

```kotlin
// ❌ a status code smuggled into a typed error channel
suspend fun fetchUser(id: String): Result<User> = try {
    val r = client.get("/users/$id")
    if (r.status.isSuccess()) Result.success(r.body()) else Result.failure(UserNotFound(id))
    // any 4xx becomes UserNotFound; a 500 from the upstream also becomes UserNotFound
} catch (e: Exception) { Result.failure(e) }
```

The reverse is also refused: a `try { ... } catch (e: UserNotFound) { call.respond(HttpStatusCode.NotFound) }`
inside a handler, which is fine — what is refused is doing the conversion in the
*client* without naming which status maps to which domain error, which
non-status case the conversion also has to cover, and what the consumer does
when both the network and the domain refuse the call.

## What is written instead

The client states, in one place, the conversion it actually intends:

```kotlin
sealed class FetchError {
    data class NotFound(val resource: String) : FetchError()
    data class ServerError(val upstream: HttpStatusCode) : FetchError()
    data class Network(val cause: Throwable) : FetchError()
}

suspend fun fetchUser(id: String): Either<FetchError, User> = try {
    val r = client.get("/users/$id")                       // expectSuccess = true
    r.body<User>().right()
} catch (e: ClientRequestException) {                      // 4xx after expectSuccess
    if (e.response.status == HttpStatusCode.NotFound)
        FetchError.NotFound("user/$id").left()
    else FetchError.ServerError(e.response.status).left()
} catch (e: ServerResponseException) {                      // 5xx
    FetchError.ServerError(e.response.status).left()
} catch (e: Exception) { FetchError.Network(e).left() }    // network, parse, anything else
```

The conversion is named, exhaustive over what `expectSuccess = true` produces,
and sits where the application's typed-error discipline lives — not inside the
HTTP layer.

## Why

`scrumia-ktor` owns the wiring: it installs `expectSuccess = true`, it gives the
client the converter, and it stops. The decision of "which 4xx is which domain
error" is a domain decision and lives where the domain does — in
`scrumia-effect` or in the typed-error pattern a project has chosen. Conflating
the two produces a function whose return type says "domain error" and whose
contents are "whatever the network said"; one of them is always a lie, and the
lie is silent until a 5xx comes back as a domain-level "not found".

This rule is the dissociation `scrumia-ktor` is named for: it owns the
library's shape, not the paradigm the application uses to talk about failure.

## Sources complémentaires

- `https://ktor.io/docs/client-response-validation.html` — `expectSuccess`, `ClientRequestException`, `ServerResponseException`, `ResponseException`. Version pin: **Ktor 3.x**.
