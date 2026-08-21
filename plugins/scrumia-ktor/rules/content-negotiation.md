# Content negotiation is installed once, and nothing parses beside it

*Refusal.* A body serialised or deserialised by hand — `Json.decodeFromString`
on `call.receiveText()`, a manual `Content-Type` header, an object mapper
instantiated in a handler — in an application that installs
`ContentNegotiation`.

## What is refused

```kotlin
// ❌ the plugin is installed, and this route ignores it
post("/users") {
    val body = Json.decodeFromString<CreateUser>(call.receiveText())
    call.respondText(Json.encodeToString(userService.create(body)), ContentType.Application.Json)
}
```

Equally refused: installing `ContentNegotiation` twice with two different
serializers, and installing it on the server while the client that talks to it
parses by hand.

## What is written instead

Install once, per application and per client, with an explicit configuration:

```kotlin
install(ContentNegotiation) {
    json(Json {
        ignoreUnknownKeys = true   // an added field upstream is not an outage here
        explicitNulls = false
    })
}

post("/users") {
    val body = call.receive<CreateUser>()
    call.respond(HttpStatusCode.Created, userService.create(body))
}
```

`call.receive<T>()` and `call.respond(value)` then negotiate on the request's
`Accept` and `Content-Type`. The same rule applies on the client, where
`ContentNegotiation` is a client plugin with the same name and the same
configuration block — that symmetry is why this rule is stated once for both
sides.

## Why

A hand-rolled parse fixes the media type at the call site: the route no longer
answers a client that asks for another one, and it stops honouring the
serializer's configuration — the `ignoreUnknownKeys` set on the plugin is not
applied by a `Json.decodeFromString` using the default instance. The failure is
quiet: it shows up as a deserialisation error on one route while every
neighbouring route tolerates the same payload.

## Sources complémentaires

- `https://ktor.io/docs/server-serialization.html` — installing `ContentNegotiation`, `call.receive`, `call.respond`. Version pin: **Ktor 3.x**.
- `https://ktor.io/docs/client-serialization.html` — the client-side plugin of the same name. Version pin: **Ktor 3.x**.
