# Authentication is a named provider, never a check inside a handler

*Refusal.* A handler reading `Authorization` itself, verifying a token, or
deciding whether the caller may proceed. Authentication is declared as a named
provider and applied by wrapping routes in `authenticate("<name>")`.

## What is refused

```kotlin
// ❌ the check is one route's private business; the next route forgets it
get("/me") {
    val header = call.request.headers["Authorization"]
    if (header == null || !verify(header.removePrefix("Bearer "))) {
        return@get call.respond(HttpStatusCode.Unauthorized)
    }
    call.respond(profileOf(header))
}
```

Also refused: a single unnamed provider used for two audiences that need
different validation, and a `validate {}` block that throws to signal a refusal
instead of returning `null`.

## What is written instead

Providers are installed once, each with a name, and routes state which one they
sit behind:

```kotlin
install(Authentication) {
    jwt("api-user") {
        realm = jwtRealm
        verifier(jwtVerifier)                 // issuer, audience and key come from config
        validate { credential ->
            credential.payload.getClaim("sub").asString()
                ?.let { JWTPrincipal(credential.payload) }   // null means "not this caller"
        }
        challenge { _, _ -> call.respond(HttpStatusCode.Unauthorized) }
    }
    basic("ops") { validate { creds -> opsUsers.check(creds) } }
}

routing {
    authenticate("api-user") {
        get("/me") {
            val principal = call.principal<JWTPrincipal>()!!  // the provider guarantees it
            call.respond(profileOf(principal))
        }
    }
}
```

Which scheme — JWT, OAuth, basic, or a custom one — is a deployment question.
The rule is the same for all four: named, installed once, applied by wrapping.

## Why

A check written in a handler protects exactly that handler. The route added next
week is unprotected and nothing says so: no compiler error, no failing test,
no line in the route tree that looks wrong. `authenticate("api-user") { }` makes
the protected surface visible at the tree level, gives every route inside a
principal that is already validated, and lets a second audience be a second
named provider rather than a branch inside a shared one.

Returning `null` rather than throwing is what lets the provider run its
`challenge` block: a thrown exception escapes the authentication pipeline and
becomes a 500 where a 401 was meant.

## Sources complémentaires

- `https://ktor.io/docs/server-auth.html` — the `Authentication` plugin, named providers, `authenticate {}`, principals. Version pin: **Ktor 3.x**.
- `https://ktor.io/docs/server-jwt.html` — the JWT provider, verifier and `validate`. Version pin: **Ktor 3.x**.
