# The proxy opens the collection route and nothing else

*Refusal.* A reverse proxy that exposes more of the analytics tool than its collection,
that lets the visitor choose the address the tool sees, or that logs the measurement.

## What is refused

- `/audience/*` forwarded whole: the tool's login, API, script and administration reach
  the Internet through the site's domain.
- The tool reading the client address from a header the visitor can send. Tools take
  the first of several address headers they know (a forwarded-for chain, a CDN's
  connecting-address header), and a proxy forwards those it receives unchanged: the
  visitor then picks the address that is hashed and, through a country header, the
  country.
- An access log line for each measurement request, holding the address and the
  address of the page.

## What is written instead

- **One route, with its conditions.** Only the collection route is relayed, and only for
  the method the tool uses (`POST`), the site's own `Origin`, a JSON `Content-Type`,
  and a bounded body (a few kilobytes; an announced length above the bound is
  refused before the body is read). Everything else under the prefix answers `404`,
  the tool's script, API and login included.
- **The proxy writes the client address itself**, into a header of its own naming
  (`X-Client-Ip: {client address}` in the proxy's syntax), replacing whatever the
  visitor sent, and the tool is told to read that header first (Umami:
  `CLIENT_IP_HEADER`). The tool's own geolocation headers are switched off for the
  same reason (Umami: `SKIP_LOCATION_HEADERS`); location comes from the database the
  tool embeds, read on the address the proxy wrote.
- **No access log on that route** (Caddy: `log_skip`), and the tool writes no request
  to its own log. Exemption question 6 is answered from the proxy's configuration.
- **The body is not filtered by the proxy.** A tool may take an address, a user agent
  or a visitor identifier from the body, and an address in the body can win over the
  header. Either the proxy or the tool filters the body, or the specification names
  this as an accepted risk with what would lift it: parasitic data that skews the
  counts, nothing exposed.
- **The tool listens on an address only the proxy reaches** (the host's own loopback or
  a private address), never on a public one.

## Why

The collection route is the only door a stranger needs, so it is the only one open. A
client address the proxy writes is the only one worth hashing.
