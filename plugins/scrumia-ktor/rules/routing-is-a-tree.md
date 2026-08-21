# Routing is a declared tree, not a scattered registration

*Refusal.* A route registered anywhere other than the application's `routing {}`
tree, or a handler that carries the work instead of calling into it.

## What is refused

```kotlin
// ❌ each file reaches for the Application and staples a path onto it
fun Application.userStuff() {
    intercept(ApplicationCallPipeline.Call) {
        if (call.request.path() == "/users") call.respond(repository.all())
    }
}
```

Also refused: a nested path spelled out in full on every sibling route
(`/api/v1/users`, `/api/v1/users/{id}`, `/api/v1/orders`) when `route("/api/v1")`
carries it once; and a handler holding transaction, mapping and business branches
inline, which makes the route tree unreadable and the logic untestable without a
server.

## What is written instead

One `routing {}` per application, split into extension functions that are still
route builders, and nested prefixes declared once:

```kotlin
fun Application.configureRouting() {
    routing {
        route("/api/v1") {
            userRoutes()
            orderRoutes()
        }
    }
}

fun Route.userRoutes() = route("/users") {
    get { call.respond(userService.all()) }
    get("/{id}") {
        val id = call.parameters["id"] ?: return@get call.respond(HttpStatusCode.BadRequest)
        call.respond(userService.byId(id))
    }
}
```

A handler reads the call, delegates, and responds. Whatever it delegates to is
not Ktor's business — and is testable without one.

## Why

The route tree is the only place a reader can see the application's surface.
Registered through an interceptor or hidden behind a pipeline phase, a path
exists but appears nowhere; two of them can claim the same URL and the winner is
decided by installation order. A declared tree makes that collision a visible one
and makes a prefix change a single edit.

## Sources complémentaires

- `https://ktor.io/docs/server-routing.html` — routing tree, nested routes, route extension functions. Version pin: **Ktor 3.x**.
