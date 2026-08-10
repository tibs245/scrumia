# Catalog of feature files

Complete reference. Each file has a boundary stated three ways — what it **holds**, what
it **may hold**, what it **must not hold** — and every exclusion names the file where
that content goes instead. An entry that only described its subject would leave the
boundary to taste; these entries do not.

## The two existence categories

**Mandatory in every feature** — `index.md`, `qa.md`, `CHANGELOG.md`, `business.md`.
A feature has to be findable, has to be possible to follow over time, has to be
possible to test — and has to be worth building: every feature states its value, so
`business.md` exists at both strata. Their absence asserts nothing; it is a gap.

**Content-tested** — everything else. A file is created only when it has content; its
absence is the assertion "nothing to say on this subject", not an oversight and not a
placeholder. This is what lets an agent decide what to read without reading everything.

## No ticket in a spec

A spec cites no issue and no PR. Tracker state lives in the tracker; a spec that
carries a ticket number is caching state that goes stale the day the ticket closes —
fourteen stale references were measured across twelve indexes before this rule.
**`CHANGELOG.md` is the one exception**: history's job is to point at the tickets
that carry the why. Everywhere else, state the fact or the open question in words —
"not automated today", "who counts, and at what threshold, is open" — and let the
tracker be searched for the ticket that tracks it. `tools/validate.py` enforces this.

These categories are **this module's** declaration, not a property of the format as
such: whichever module fills the `specs` slot declares its own set, and this file is
where `scrumia-specs` declares its own. Do not read the set out of `CLAUDE.md`'s
`## Specs contract` block instead — that block names the files a module uses so
consumers need not hard-code them, and marks none of them required
(`docs/adr/0012-specs-contract.md`).

## The membership tests

Three boundaries carry most of the collisions; each has one test, stated here and
applied by the entries below rather than restated.

- **business vs ux, on the journey.** A step stated as actor intent and the value
  delivered, naming no screen, no control, no click path → `business.md`. The moment
  it names one → `ux.md`. Same journey, two altitudes: `business.md` says why the steps
  exist, `ux.md` says what the user sees at each one.
- **tech vs archi, on data flow.** Flow that never leaves the app's own boundary →
  `tech.md`. Flow that crosses apps, scoped to an EPIC → `archi.md`.
- **business vs tech, on mechanisms.** A rule that constrains what the product
  promises — whatever tool enacts it — → `business.md`. How a tool, command or flag
  achieves it, and what happens when it is misused → `tech.md`. "Reads are filtered
  or they lie" is business; the flag that does the filtering is tech.
- **ux vs qa, on accessibility.** A property the journey must have, stated in prose
  ("this control is reachable by keyboard") → `ux.md`. Anything testable against a
  named technical criterion (a contrast ratio, a keyboard-trap check, an announcement)
  → a tagged `qa.md` criterion. Identity-level rules (contrast minimums, the accent
  hue-distance rule) live in `design/` and are cited, never restated.

---

## `index.md` — mandatory in every feature

The entry point, and nothing else. It is the only file an agent or a human
systematically reads before deciding what to read next; it must fit in one reading,
and everything in it must serve that one decision.

Holds:
- The summary of the feature in 10 lines maximum — what it does and for whom
- Its status: `draft`, `active`, `deprecated`
- Its links: parent Business feature (for an App), App features that implement it
  (for a Business), consumed App features, and the authority pointers — the `design/`
  or `docs/` file that answers a question this feature defers, one line of key info each
- The list of files present, one line per file saying **when to read it** — the agent
  deciding what to load is this table's reader

May hold: a one-line pointer to the file that elaborates a claim ("the persona is in
`business.md`").

Must not hold: a rule → the file its subject names below; a decision or its rationale →
the ADR or the tracker; a ticket number → the tracker (see *No ticket in a spec*); a
fact a `design/` file or a component spec already states → cite it, one line; history →
`CHANGELOG.md`. **A rule, a decision or a rationale in an index is a defect**, whatever
heading it hides under.

The section set is declared by the template (`assets/index.template.md`): `In brief`,
`Links`, `Files present` — those three, no others. `tools/validate.py` enforces the
set; what it cannot read — a rule smuggled under a conformant heading — review owns.

Read by: everyone, first.

---

## `business.md` — mandatory in every feature

Every feature states its value, in four answers a reader gets before anything else:
**who** the feature is for, **what it brings** them, **why it matters** — and whether
that contribution **can be measured**, with the measure named, or the honest note that
it is not instrumented today. A feature whose value cannot be stated is a splitting or
deletion candidate, not a feature missing a paragraph.

**Business feature**: the reference. The value statement above, then the business
rules, the domain vocabulary, the invariants, the personas, the use cases, and the
user journey **as intent** (per the membership test above). A reader understands
immediately what is expected and what it brings, before any screen or line of code
exists.

**App feature**: the value statement for *this app's* share of the work, a reference
to the parent Business feature — *never* a copy of its rules — and only what is
specific to this app: a local restriction, an interpretation, a case this app alone
encounters.

May hold: an open business question, clearly marked as open rather than resolved by
assertion.

Must not hold: a screen, a control, a navigation path → `ux.md`; a technology choice
or a constraint of the implementation → `tech.md`; a test scenario → `qa.md`; a schema
another feature consumes → `api-contract.md`; the history of how a rule came to be →
the issue.

Duplicating a business rule in two files guarantees they will diverge. A single
reference, a single place that has authority.

Read by: business, QA, devs.

---

## `qa.md` — mandatory in every feature

The acceptance criteria. Given/When/Then, one scenario per case, each carrying a
stable identifier (`AC-<n>`) that tickets and tests reference.

**Business feature**: the business criteria, independent of any interface.
**App feature**: the criteria of this implementation, including technical cases
(timeout, network error, concurrent state) and the accessibility targets that can
fail — a contrast ratio, a keyboard path, an announcement — tagged as such.

A criterion must be able to fail. If it cannot fail, it tests nothing.

Expected coverage: nominal, zero, boundary, duplicate, concurrency, cancellation,
expiration, insufficient permissions. An "out of scope" section prevents bug tickets
on behaviour never promised.

Must not hold: the persona or the value the criteria protect → `business.md`; why a
rule exists → the issue; how the implementation satisfies a criterion → `tech.md`.

Read by: QA, devs, execution and review agents.

---

## `CHANGELOG.md` — mandatory in every feature

Short. One entry per notable change, reverse-chronological.

```markdown
## YYYY-MM-DD — one-line title of the change
- Issue: #NN
- PR: #NN (filled at merge)
- Breaking: yes | no
```

**Never** contains the reasoning. The why is in the issue. An entry that explains
turns into a parallel spec.

Read by: everyone, to know what moved and where to dig.

---

## `ux.md` — user experience

App Frontend, content-tested. The interface half of the journey: what the user sees,
in what order, and what the screen refuses to do.

Holds:
- The screen or flow — entry point, exit point
- The composition — the components this screen uses, each a pointer to its
  `design/components/<name>/spec.md`, with its role on this screen; never a copy
- The screen states — empty, loading, error, success — with the exact copy per state
- The navigation — reading order, focus flow, what changes announce themselves
- The text alternatives, and the accessibility properties of the journey stated in
  prose (the testable half goes to `qa.md`, per the membership test)
- The interface constraints — what this screen must never do, when it is not already
  a component-level refusal

May hold: a markdown or ASCII mockup, **only as a seed** for a layout that has no
`design/` counterpart yet — it converts into an exploration or a component spec, it
does not stay a permanent second drawing. A link to an external design tool serves
the same purpose.

Must not hold: a literal colour, spacing or duration → `design/tokens.css`; a
component's anatomy or behaviour → its `design/components/` spec, cited; a business
rule or the intent behind the journey → `business.md`; a WCAG target that can pass or
fail → a tagged `qa.md` criterion. When prose here touches something a criterion
tests, it cites the criterion and names the constraint — it does not restate the
criterion's mechanism. A value this screen needs that no token or component supplies
is a finding for `design/`, not a number written here.

Read by: UX, frontend devs.

---

## `tech.md` — internal technical choices

The choices specific to this feature in this app: dependencies added and their reason,
structure chosen and alternative rejected, debt assumed with its date and its exit
condition, the constraints the implementation lives under, and the flow of information
and data **within this app**.

Doesn't document what the code already says. Documents what the code cannot say: why
this choice rather than another.

Must not hold: flow that crosses an app boundary → `archi.md` (membership test above);
a rule the business owns → `business.md`; a schema another feature consumes →
`api-contract.md`.

Read by: devs, Technical Lead.

---

## `api-contract.md` — shared interfaces between features

The contract for any data shared across a feature or app boundary — an HTTP API, but
equally a file format, a YAML schema, a CLI's output shape. If another feature parses
it, it is a contract, whatever the transport.

**Producing feature**: the exposed schema (OpenAPI, GraphQL, protobuf, JSON Schema, or
the shape stated precisely), the error cases, pagination if any, what is stable and
what may change.
**Consuming feature**: the reference to the producer's contract, and the assumptions
made about it.

Must not hold: an internal structure nobody outside the feature consumes → `tech.md`.

Must stay in sync with the code. A diverged contract is worse than an absent one: it
is believed.

Read by: devs, integration, review agents.

---

## `archi.md` — cross-cutting architecture of an EPIC

**Only in a Business feature whose implementation touches ≥2 apps.**

Holds: how the apps talk to each other **for this EPIC**, which contracts are at
stake, the cross-app data flow, the deployment order if it matters, the degraded
modes.

Must not hold: a decision meant to outlive the EPIC → `docs/adr/`. The test: *if the
EPIC is shipped and closed, does this document still have value?* Yes → ADR. No →
`archi.md`.

It dies with the EPIC: when the EPIC closes — shipped **or abandoned** — the file is
deleted, not left unmaintained. Anything still worth keeping at that point was an ADR
all along.

Read by: Technical Lead, devs of the apps concerned.

---

## `legal.md` — compliance

Present if the feature touches: personal data, payment, user content, minors, health,
a regulated sector — or carries a named legal risk of its own (a trademark question,
a licence obligation).

Holds: the applicable obligations, named; the data processed and its legal basis; the
retention period; the rights of the individuals; the required notices and consents.
A residual legal risk the project accepts is recorded with the acceptance record
defined in `security.md`'s entry — stated once there, referenced from here, so the
two files cannot drift.

Must not hold: made-up legal advice — an uncertain obligation is written as an open
question, not resolved by assertion; an engineering risk with no legal trigger →
`security.md`.

Read by: legal, business, devs.

---

## `security.md` — risk analysis

Content-tested, both strata. Present when the feature has a meaningful risk surface
on any axis below — which is a judgment the absence of the file asserts was made.

Holds: a risk table, one row per identified risk — the risk, its axis, its rating,
and its mitigation or its acceptance. Four axes, each answering one question:

| Axis | The question it answers |
|---|---|
| Availability | If this fails, who is blocked, and for how long? |
| Integrity | If this is silently wrong, what breaks downstream, and is the error detectable? |
| Confidentiality (access) | Who must not see this, and what happens if they do? |
| Traceability | If this is disputed later, can the who/when/why be reconstructed? |

One ordinal scale, so ratings compare across features:

- **low** — failure is cosmetic or self-healing; nobody is blocked
- **medium** — degraded for some, a workaround exists
- **high** — a core flow is blocked or silently wrong; recovery is manual
- **critical** — irreversible loss (data, money, trust) or no recovery path

**The acceptance record** — for every risk assumed rather than mitigated, and reused
by `legal.md` for residual legal risks: the axis and rating, why it is accepted, who
accepted it (named — a merge by the project owner counts as the acceptance it
records), and the revisit condition — the event or date that invalidates the
acceptance.

Must not hold: an accessibility concern → `ux.md` and `qa.md` (it is not an "access"
risk in this table's sense); a legal obligation → `legal.md`; a threat catalogue with
no rated conclusion — a row that rates nothing decides nothing.

Read by: business (signs the acceptances), Technical Lead, devs.

---

## `devx.md` — developer experience

When the feature exposes something consumable by others: lib, SDK, hooks, reusable
components.

Holds: how to use it, minimal examples, the pitfalls, what is stable and what is not.

Must not hold: the internal why of the implementation → `tech.md`.

Read by: devs of the other apps.

---

## The worked examples

Two real features, kept conformant with this catalog and its templates, serve as the
copy source: `features/business/github-tracking/` for the Business stratum,
`features/app/site/hero/` for the App stratum. When this catalog and an example
disagree, the catalog is right and the example has drifted — file it as a finding.

## Extending the catalog

The catalog is open. `perf.md`, `i18n.md`, `analytics.md` are legitimate additions.

Two rules to keep it from sprawling:

1. **A new file must have a distinct reader.** If the same people already read another
   file of the feature, it's a section, not a file.
2. **Document the addition right here**, with its boundary in the same three-part
   shape. Otherwise the next feature will invent another name for the same thing, and
   the catalog will lose the only thing that makes it useful: its predictability.
