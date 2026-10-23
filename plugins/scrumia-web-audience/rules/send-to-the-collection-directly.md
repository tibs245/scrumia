# The module sends to the tool's collection, on the site's own domain

*Refusal.* Loading the analytics tool's own script into the pages, or sending the
measurement to another domain than the site's.

## What is refused

```html
<!-- ❌ the tool's script decides what is read, kept and sent -->
<script defer src="https://analytics.example.net/script.js" data-website-id="…"></script>
```

A vendor script reads the page's address, title, screen and language by itself, keeps
its own state, and is another piece of code the content security policy must allow.
Some do not read the browser's Global Privacy Control signal at all, and some keep the
visit token in memory, so a multi-page site loses it at every navigation. A call to a
different domain needs the policy widened and a cross-origin permission, and puts a
third host in the privacy policy's list of recipients.

## What is written instead

- **The measurement module posts to the tool's collection endpoint itself**, a
  `fetch` with `keepalive: true` and a JSON body, to a path on the site's own domain
  (`/audience/collect`). The path is a constant of the module and the contract with the
  reverse proxy (`the-proxy-opens-one-route.md`).
- **The body holds only the keys the specification lists.** For Umami that is
  `{"type":"event","payload":{…}}`, the payload carrying the site identifier, the
  host name, the cleaned address (`cleaned-addresses.md`), the cleaned referrer and,
  for a named event, its name and closed data. No title, no screen, no language, and
  none of the keys the tool would accept to override what it infers (client address,
  user agent, timestamp, visitor identifier). A test builds each payload and compares
  its keys with the list.
- **The content security policy does not change**: the module is a script the build
  produces, never inline, and `connect-src 'self'` covers the send. If the build ends
  up inlining it, its fingerprint joins `script-src` like any built script.
- **No CORS.** The send is same-origin; a rule that opens a cross-origin permission for
  the measurement is a finding.
- **The collection path is written by the module only.** A test lists the source files
  outside the module and fails if one contains the path in quotes. The bundled
  detector does the same with `--queue /audience/collect` for a codebase with no such
  test yet.
- **Every page that sends goes through the module's single guard**: signals, opt-out
  marker and unreadable storage are read before each send, not once at load
  (`production-only-and-browser-signals.md`, `opt-out-that-lasts.md`).

## Why

What the module sends is exactly what the specification says, and nothing the tool
would add on its own. The privacy policy can then state the payload in full, and a
change of tool changes the module's body and the proxy, not every page.
