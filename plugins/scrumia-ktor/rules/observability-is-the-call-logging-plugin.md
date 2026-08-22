# Call logging and observability go through `CallLogging` and a stated tracer

*Refusal.* A `println` of the request, a `System.out` inside a handler, or a
hand-rolled `MDC.put` that nobody clears.

## What is refused

```kotlin
// ❌ a println that no log level turns off, no structure parses, no MDC carries
get("/orders") {
    println("GET /orders from ${call.request.origin.remoteHost}")
    call.respond(orderService.all())
}
```

Equally refused: a `CallLogging` installed without a filter that decides which
paths are logged and at which level, and an MDC started by the application that
is closed nowhere — the next request inherits the previous caller's principal.

## What is written instead

The plugin is installed with a filter, the MDC is filled in a way that clears on
response, and any external tracing has a stated home:

```kotlin
install(CallLogging) {
    level = LogLevel.INFO
    filter { call -> call.request.path().startsWith("/api/") }
    format { call ->
        val status = call.response.status()
        val ms = call.handledDurationMillis()
        "${call.request.httpMethod.value} ${call.request.path()} -> $status in ${ms}ms"
    }
    // MDC populated by the plugin is cleared when the call completes, automatically.
}

install(OpenTelemetry) {
    setTracer(OpenTelemetryTracerAdapter(tracer, TextMapPropagator))
}
```

What the tracer sends on to is a deployment question (collector, sampling, OTLP
versus Jaeger); this module's rule is the boundary — Ktor hands the call to the
adapter it is given and does not invent one.

## Why

A print is unconfigurable, unstructured, and bypasses the project's logging
back-end. A `CallLogging` without a filter logs the health-check probe at INFO,
fills the disk on a load test, and drowns the one line a reader would have
acted on. An MDC left open is the bug where a slow request on thread A sees the
user id of the last request that ran on thread B — and no test fires by default.

## Sources complémentaires

- `https://ktor.io/docs/server-call-logging.html` — `CallLogging`, filters, MDC, format. Version pin: **Ktor 3.x**.
- `https://ktor.io/docs/server-opentelemetry.html` — the OpenTelemetry plugin, tracer adapter. Version pin: **Ktor 3.x**.
