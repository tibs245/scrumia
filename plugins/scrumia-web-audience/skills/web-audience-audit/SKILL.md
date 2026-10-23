---
name: web-audience-audit
description: Audit a web app's audience measurement against the ten questions this module ships — closed event catalogue, one owning module, cleaned addresses, a direct send, the proxy's one route, a measurement that never touches the page, production-only with browser signals, a lasting opt-out, the tool and its database kept apart, and the exemption conditions. Use it before adopting the module on an app that already measures, when a measurement change ships, or before the privacy policy is revised.
---

# Auditing audience measurement

Ten questions, one per rule. Read what each asks from the files, then report. Change
nothing without being asked.

First establish what measures: the tool, the module that sends to it, the proxy in front
of it and where the specification lists its events. An app with no measurement has
nothing to audit; say so and stop.

## 1 — Is every event in the catalogue?

Rule: [`closed-event-catalogue`](../../rules/closed-event-catalogue.md).

List the event names the code can send. Compare with the specification's table.
A name in the code and not in the table is a finding; so is a value taken from the
page rather than from a closed list.

## 2 — Does one module own the tracker?

Rule: [`one-module-declarative-markup`](../../rules/one-module-declarative-markup.md).

```bash
${CLAUDE_SKILL_DIR}/../../scripts/detect-direct-tracker-calls.sh --module <module-dir> <source-root>
```

Exit `3` lists files outside the module that mention the queue; each is a finding.
Add `--queue NAME` for a tracker whose queue is not `_paq`, or `--queue <collection
path>` for a module that sends directly. Then check that a test makes the same rule
fail, and that the pages declare events by attribute.

## 3 — Is the address that leaves a template?

Rule: [`cleaned-addresses`](../../rules/cleaned-addresses.md).

Find the function that builds the sent address. Check path template, no query, no
fragment, referrer reduced to its origin, title free of the variable part, and a
test with the awkward inputs. Check which routes carry a variable part, and that
each is templated or not measured.

## 4 — Does the module send directly, with the listed keys only?

Rule: [`send-to-the-collection-directly`](../../rules/send-to-the-collection-directly.md).

Check that no vendor script is loaded, that the send goes to a path on the site's own
domain, that the content security policy and any cross-origin setting are unchanged,
and that a test compares the keys of each payload with the specification's list. A key
the tool would take to override what it infers (address, user agent, timestamp,
visitor identifier) is a finding.

## 5 — Does the proxy open one route, and write the client address?

Rule: [`the-proxy-opens-one-route`](../../rules/the-proxy-opens-one-route.md).

Answered from the proxy's configuration and the tool's environment, not from the
application's code; say which file answered. Check the method, origin, content type and
size conditions, a `404` for every other path under the prefix, the header the proxy
writes over the visitor's, the tool configured to read it first, the geolocation headers
switched off, no access log on the route, and what the specification says about a body
that is not filtered. Where no configuration is in the repository, report "not
verifiable" rather than yes.

## 6 — Does the measurement leave the page alone?

Rule: [`measurement-after-the-page`](../../rules/measurement-after-the-page.md).

Check that the module starts after load, when the browser is idle, and that nothing in
rendering depends on it. Find the tests that make the send throw, reject, and the
collection unreachable; if none exists, that is a finding, whatever the code looks like.

## 7 — Production only, and browser signals honoured?

Rule: [`production-only-and-browser-signals`](../../rules/production-only-and-browser-signals.md).

Find where the site identifier is read. A literal identifier in source is a finding.
Check that empty renders nothing, that an invalid value stops the build, that
Global Privacy Control and Do Not Track are read by the module before each send, and
that no banner exists unless the specification says the app left the exemption.

## 8 — Can the person object, and does it last?

Rule: [`opt-out-that-lasts`](../../rules/opt-out-that-lasts.md).

Check the control is in the privacy policy with its states, that the marker is the one
the tool respects, that it outlasts the measurement, that an unreadable marker means
nothing is sent, that a failed write is told, that the status is announced, and that the
policy's list of what the browser keeps matches the module's constant.

## 9 — Are the tool and its database apart?

Rule: [`tool-and-database-apart`](../../rules/tool-and-database-apart.md).

Answered from the deployment's configuration. Check the database, the roles that can
connect to it and the roles of the application that cannot, the tool's outgoing calls
switched off, the administration's network, two-factor authentication, the purge and its
test, and the digest of the image. Check what the policy says: no cookie but not "no
tracker", pseudonymous for stored lines, anonymous for totals only.

## 10 — Do the exemption conditions hold?

Rule: [`exemption-conditions`](../../rules/exemption-conditions.md).

Answer the fifteen questions one by one, each with the file or setting that proves
it. Questions about the server (log lines, retention, IP handling, disabled
features) are answered from its configuration, not from the application's code;
say which source answered. Check the date the regulator's documents were last read.

## Reporting

One finding per line: the file, the rule's name, one line of what was not met.
Separate what the script decided from what you read. Close with the list of the
fifteen questions answered no or not verifiable; that list is what the owner decides
on, between fixing and leaving the exemption.
