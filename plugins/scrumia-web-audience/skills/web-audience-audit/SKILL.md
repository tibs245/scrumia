---
name: web-audience-audit
description: Audit a web app's audience measurement against the six rules this module ships — closed event catalogue, one owning module, cleaned addresses, production-only with browser signals, a lasting opt-out, and the exemption conditions. Use it before adopting the module on an app that already measures, when a measurement change ships, or before the privacy policy is revised.
---

# Auditing audience measurement

Six questions, one per rule. Read what each asks from the files, then report. Change
nothing without being asked.

First establish what measures: the tracker product, the module that loads it, and
where the specification lists its events. An app with no measurement has nothing to
audit; say so and stop.

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
Add `--queue NAME` for a tracker whose queue is not `_paq`. Then check that a test
makes the same rule fail, and that the pages declare events by attribute.

## 3 — Is the address that leaves a template?

Rule: [`cleaned-addresses`](../../rules/cleaned-addresses.md).

Find the function that builds the sent address. Check path template, no query, no
fragment, referrer reduced to its origin, title free of the variable part, and a
test with the awkward inputs. Check which routes carry a variable part, and that
each is templated or not measured.

## 4 — Production only, and browser signals honoured?

Rule: [`production-only-and-browser-signals`](../../rules/production-only-and-browser-signals.md).

Find where the site identifier is read. A literal identifier in source is a finding.
Check that empty renders nothing, that an invalid value stops the build, that
Global Privacy Control and Do Not Track prevent loading the tracker, and that no
banner exists unless the specification says the app left the exemption.

## 5 — Can the person object, and does it last?

Rule: [`opt-out-that-lasts`](../../rules/opt-out-that-lasts.md).

Check the control is in the privacy policy with its three states, that the opt-out
cookie lasts longer than the measurement cookie, that the status is announced, and
that the policy's cookie table matches the module's constant.

## 6 — Do the exemption conditions hold?

Rule: [`exemption-conditions`](../../rules/exemption-conditions.md).

Answer the fifteen questions one by one, each with the file or setting that proves
it. Questions about the server (log lines, retention, IP truncation, disabled
features) are answered from its configuration, not from the application's code;
say which source answered. Check the date the regulator's documents were last read.

## Reporting

One finding per line: the file, the rule's name, one line of what was not met.
Separate what the script decided from what you read. Close with the list of the
fifteen questions answered no or not verifiable; that list is what the owner decides
on, between fixing and leaving the exemption.
