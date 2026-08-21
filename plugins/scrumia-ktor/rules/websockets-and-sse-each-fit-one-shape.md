# WebSockets and SSE: each fits one shape; a project states which it means

*Refusal.* A request to subscribe to a stream answered by a `while (true) { respondText(...) }`
loop, or a websocket used to push messages one way to a server that only ever
sends.

## What is refused

```kotlin
// ❌ the client never sends; this is SSE pretending to be a websocket
webSocket("/events") {
    while (true) {
        send(pending.poll() ?: continue)
        delay(100)
    }
}

// ❌ a websocket that streams and never accepts a frame
get("/ticker") {
    call.respondTextWriter(contentType = ContentType.Text.EventStream) {
        while (true) { write("data: ${next()}\n\n"); flush(); delay(1000) }
    }
}
```

## What is written instead

The choice is stated where the route lives:

```kotlin
// bidirectional, frames from either side, any media type
webSocket("/chat/{room}") {
    val session = ChatSession(this, call.parameters["room"]!!)
    session.run()
}

// server to client only, text frames, simple reconnect
get("/events") {
    call.respondTextWriter(contentType = ContentType.Text.EventStream) {
        val source = eventSource()
        try { for (e in source) write("data: $e\n\n") } finally { source.close() }
    }
}
```

WebSockets when the client sends frames and the server sends frames back, both
on the same channel; SSE when the stream is one way and the client reconnects
on its own. The route's verb and content type state the choice; the README of
the service states the project-wide convention.

## Why

The two protocols are not interchangeable. A websocket carries framing, binary
support and a backchannel; a server-sent-events stream is a half-duplex text
line that any HTTP client understands. Using `respondTextWriter` with
`Content-Type: text/event-stream` and an infinite loop is the failure mode that
never reconnects, never says "this is a stream", and never sets a header a
proxy can respect. Using a websocket one-way burns the framing, the overhead
and the connection limit the protocol bought, and the browser's auto-reconnect
— the whole reason SSE exists — is gone.

## Sources complémentaires

- `https://ktor.io/docs/server-websockets.html` — `webSocket {}`, frames, sessions. Version pin: **Ktor 3.x**.
- `https://ktor.io/docs/server-sse.html` — server-sent events, `respondTextWriter`, `Content-Type: text/event-stream`. Version pin: **Ktor 3.x**.
