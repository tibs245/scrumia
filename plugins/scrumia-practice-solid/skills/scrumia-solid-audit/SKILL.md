---
name: scrumia-solid-audit
description: Audits an app's design against SOLID — the violations and, on equal footing, the over-applications (abstractions without variation, dead indirections). Use it to take stock of the design before a refactor or after a phase of rapid growth.
---

# Auditing the design

This audit has two columns, of equal importance: **the violations** (the principle is missing where it would help) and **the over-applications** (the principle is applied where nothing varies). Delivering one without the other pushes toward over-design — this is a deliberate choice, not an oversight: see [D-01](${CLAUDE_SKILL_DIR}/../scrumia-solid-principles/decisions/D-01-over-application-audited-equally.md).

The per-principle signals — violation *and* over-application — are in the five guides:

| Principle | Guide |
|---|---|
| S | [${CLAUDE_SKILL_DIR}/../scrumia-solid-principles/guides/01-srp.md](${CLAUDE_SKILL_DIR}/../scrumia-solid-principles/guides/01-srp.md) |
| O | [${CLAUDE_SKILL_DIR}/../scrumia-solid-principles/guides/02-ocp.md](${CLAUDE_SKILL_DIR}/../scrumia-solid-principles/guides/02-ocp.md) |
| L | [${CLAUDE_SKILL_DIR}/../scrumia-solid-principles/guides/03-lsp.md](${CLAUDE_SKILL_DIR}/../scrumia-solid-principles/guides/03-lsp.md) |
| I | [${CLAUDE_SKILL_DIR}/../scrumia-solid-principles/guides/04-isp.md](${CLAUDE_SKILL_DIR}/../scrumia-solid-principles/guides/04-isp.md) |
| D | [${CLAUDE_SKILL_DIR}/../scrumia-solid-principles/guides/05-dip.md](${CLAUDE_SKILL_DIR}/../scrumia-solid-principles/guides/05-dip.md) |

This skill says where to look and how to deliver the finding.

## Scope

Ask which app if it isn't obvious. Read its implementation module if one is plugged in (mapping in `CLAUDE.md`) — it may restrict some principles, and **its restrictions take precedence**: don't report as a violation what the implementation module refuses to apply.

## Where to look first

Don't read the whole app. Three entry points give the essentials:

1. **The hot files** — `git log --format= --name-only -100 | sort | uniq -c | sort -rn | head -20`. The file every PR touches is either an S violation or the legitimate core of the domain; the audit says which (signals: [guides/01-srp.md](${CLAUDE_SKILL_DIR}/../scrumia-solid-principles/guides/01-srp.md)).
2. **The infrastructure boundaries** — look for imports of HTTP clients, ORMs, third-party SDKs, the clock. Note *who* imports them: the infrastructure (normal) or the domain (D violation) (signals: [guides/05-dip.md](${CLAUDE_SKILL_DIR}/../scrumia-solid-principles/guides/05-dip.md)).
3. **The contracts** — interfaces, traits, abstract classes. For each: how many real implementers? A single one since forever → over-application column. An implementer that cheats (throws, restricts, lies) → L violation (signals: [guides/03-lsp.md](${CLAUDE_SKILL_DIR}/../scrumia-solid-principles/guides/03-lsp.md), also relevant for I: [guides/04-isp.md](${CLAUDE_SKILL_DIR}/../scrumia-solid-principles/guides/04-isp.md)).

Then a targeted pass over what these three entry points have designated.

## What is not a finding

- A pattern the app's implementation module explicitly imposes or refuses — its rule takes precedence.
- A young abstraction in a zone declared as exploration — over-design is judged on stabilized code.
- Code nobody touches and that works. The audit serves upcoming work; a frozen, bug-free corner costs nothing.

## The deliverable

Two tables — violations, over-applications — with, for each finding: the principle, the file, the observed fact (not the opinion: "1 implementer for 14 months", not "useless abstraction"), and the effect on the work ("testing a rule requires a container").

Then a three-line synthesis: the state of the design in one sentence, the two most profitable findings to address, what can wait.

Rewrite nothing without agreement. To address a finding, propose `scrumia-solid-refactor`, one finding at a time.
