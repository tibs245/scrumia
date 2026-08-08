# Catalog of feature files

Complete reference. Each file has a defined content, a reader, and a condition of existence.

> **The rule that governs everything else**: a file is only created if it has content.
> The absence of a file is an assertion ("nothing to say here"), not an oversight.

---

## `index.md` — mandatory, everywhere

The entry point. It's the only file an agent or a human systematically reads before deciding what to read next. It must fit in one reading.

Contains:
- The summary of the feature in 10 lines maximum
- Its status: `draft`, `active`, `deprecated`
- Its links: parent Business feature (for an App), App features that implement it (for a Business), consumed App features
- The list of files present **with one line saying why**
- The open GitHub issues that concern it

Read by: everyone, first.

The "why this file exists" field is not decorative: it's what lets an agent load `legal.md` only when it's relevant, instead of reading everything as a precaution.

---

## `business.md` — business rules

**Business feature**: the business rules, the domain vocabulary, the invariants. This is the reference.

**App feature**: *does not copy* the rules. References the parent Business feature and records only what's specific to this app — a local restriction, an interpretation, a case this app alone encounters.

Duplicating a business rule in two files guarantees they will diverge. A single reference, a single place that has authority.

Read by: business, QA, devs.

---

## `qa.md` — acceptance criteria

Mandatory everywhere. Given/When/Then, one scenario per case.

**Business feature**: the business criteria, independent of any interface.
**App feature**: the criteria of this implementation, including technical cases (timeout, network error, concurrent state).

A criterion must be able to fail. If it cannot fail, it tests nothing.

Expected coverage: nominal, zero, boundary, duplicate, concurrency, cancellation, expiration, insufficient permissions.

Read by: QA, devs, execution and review agents.

---

## `CHANGELOG.md` — mandatory, everywhere

Short. One entry per notable change, reverse-chronological.

```markdown
## YYYY-MM-DD — one-line title of the change
- Issue: #NN
- PR: #NN (filled at merge)
- Breaking: yes | no
```

**Never** contains the reasoning. The why is in the issue. An entry that explains turns into a parallel spec.

Read by: everyone, to know what moved and where to dig.

---

## `legal.md` — compliance

Present if the feature touches: personal data, payment, user content, minors, health, or a regulated sector.

Contains: the applicable obligations, named; the data processed and its legal basis; the retention period; the rights of the individuals; the required notices and consents.

Contains no made-up legal advice. When an obligation is uncertain, write it as an open question — that's more useful than a wrong answer that reassures.

Read by: legal, business, devs.

---

## `archi.md` — cross-cutting architecture of an EPIC

**Only in a Business feature whose implementation touches ≥2 apps.**

Contains: how the apps talk to each other **for this EPIC**, which contracts are at stake, the data flow, the deployment order if it matters, the degraded modes.

Does not contain the project's durable decisions — those go in `docs/adr/`. The distinction: `archi.md` dies with the EPIC, an ADR outlives the project.

Read by: Technical Lead, devs of the apps concerned.

---

## `api-contract.md` — interface contract

**App Backend**: the exposed schema (OpenAPI, GraphQL, protobuf), the error codes, pagination, compatibility.

**App Frontend**: the reference to the contract of the consumed backend app, and the assumptions made about it.

Must stay in sync with the code. A diverged contract is worse than an absent one: it is believed.

Read by: devs, integration, review agents.

---

## `tech.md` — internal technical choices

The choices specific to this feature in this app: dependencies added and their reason, structure chosen and alternative rejected, debt assumed with its date and its exit condition.

Doesn't document what the code already says. Documents what the code cannot say: why this choice rather than another.

Read by: devs, Technical Lead.

---

## `ux.md` — user experience

App Frontend, generally. The user journey, the screen states (empty, loading, error, success), the exact copy, the interface constraints.

The error and empty states are the useful part: the nominal path can be guessed, the others can't.

Read by: UX, frontend devs.

---

## `a11y.md` — accessibility

App Frontend, when there is an interface. The targeted WCAG criteria, keyboard navigation, text alternatives, screen reader announcements, contrasts, automated tests.

Separate from `ux.md` because it has a different reader and a different verification cycle.

Read by: UX, frontend devs, QA.

---

## `devx.md` — developer experience

When the feature exposes something consumable by others: lib, SDK, hooks, reusable components.

Contains: how to use it, minimal examples, the pitfalls, what is stable and what is not.

Read by: devs of the other apps.

---

## Extending the catalog

The catalog is open. `perf.md`, `i18n.md`, `analytics.md`, `security.md` are legitimate additions.

Two rules to keep it from sprawling:

1. **A new file must have a distinct reader.** If the same people already read another file of the feature, it's a section, not a file.
2. **Document the addition right here**, with its content and its condition of existence. Otherwise the next feature will invent another name for the same thing, and the catalog will lose the only thing that makes it useful: its predictability.
