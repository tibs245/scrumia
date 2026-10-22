# The address that leaves is the template, not the visit

*Refusal.* Sending the page's real address, with its query string, its fragment or
the identifier carried in its path, to the measurement.

## What is refused

```ts
// ❌ the tracker reads location.href by itself and sends whatever it holds
//    /join/8F3K-22QA?utm_source=mail&email=a@b.example#step2
```

An address carrying a token, an invitation code, an e-mail or a campaign tag turns a
page count into a record about a person. The tracker's default is to send it all.

## What is written instead

The module computes the address it sends, with a pure function, and hands it to the
tracker explicitly (`setCustomUrl` in Matomo) instead of letting the tracker read it.

- **The path is reduced to its template.** `/join/8F3K-22QA` becomes `/join/:code`,
  `/fr/join/8F3K-22QA` becomes `/fr/join/:code`. The list of routes that carry a
  variable part is the application's own, kept next to the routes.
- **No query string, no fragment.** None is sent, whatever its name.
- **The referrer is reduced to its origin**, and is empty for a navigation inside
  the site (`setReferrerUrl`).
- **The title is the page's own title** and never contains the variable part. A page
  whose title would carry it is given a fixed one for measurement.
- **A page that reads a token does not load the tracker at all** when even the
  template is more than the purpose needs. Say which in the specification.
- **Campaign tags are not kept.** Attribution by campaign name or tag is marketing
  measurement and lies outside the exemption (see `exemption-conditions.md`); the
  query string is dropped before anything can read it.

The function is tested with the awkward inputs: a path with a trailing slash, an
encoded character, a referrer from the same origin, a referrer that does not parse.

## Why

What is not sent cannot be stored, leaked or recombined. Cleaning at the source is
the only place where the guarantee does not depend on the server configuration.
