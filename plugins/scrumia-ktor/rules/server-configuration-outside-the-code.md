# What the server binds and connects to comes from configuration

*Refusal.* A port, a host, a database URL, a JWT secret or an external base URL
written as a literal in Kotlin.

## What is refused

```kotlin
// ❌ every environment is a recompile, and the secret is in version control
fun main() {
    embeddedServer(Netty, port = 8080, host = "0.0.0.0") {
        val secret = "s3cr3t-dev-key"
        module(secret)
    }.start(wait = true)
}
```

## What is written instead

`EngineMain` reads `application.conf` (or `application.yaml`), and the module
reads its own values from the environment it is given:

```hocon
ktor {
    deployment { port = 8080, port = ${?PORT} }
    application { modules = [ com.example.ApplicationKt.module ] }
}
jwt {
    issuer = "https://example.com/"
    secret = ${JWT_SECRET}          # no default: absent is a startup failure, not a fallback
}
```

```kotlin
fun main(args: Array<String>) = EngineMain.main(args)

fun Application.module() {
    val issuer = environment.config.property("jwt.issuer").getString()
    val secret = environment.config.property("jwt.secret").getString()
    configureSecurity(issuer, secret)
    configureRouting()
}
```

A value that differs between environments is overridden by an environment
variable through `${?VAR}`; a secret carries no default at all.

## Why

A literal makes the deployment target a property of the binary: staging and
production need two builds, and the difference between them is invisible in a
diff of the configuration. A secret written in Kotlin is a secret in git history,
and rotating it is a release. `environment.config.property` fails at startup when
a required key is missing — the loud failure, on boot, rather than a
`NullPointerException` on the first authenticated request.

`EngineMain` also keeps the module function free of engine choice, which is what
makes the same module runnable under `testApplication` without a second entry
point.

## Sources complémentaires

- `https://ktor.io/docs/server-configuration-file.html` — `EngineMain`, `application.conf`, environment-variable substitution. Version pin: **Ktor 3.x**.
- `https://ktor.io/docs/server-create-and-configure.html` — `embeddedServer` versus `EngineMain`, and the module function. Version pin: **Ktor 3.x**.
