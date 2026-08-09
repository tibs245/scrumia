# Feature format — business rules

## The two strata

**Business** (`features/business/<feature>/`) — the *what*. Business value,
business rules, domain vocabulary, invariants. No screen, no API, no tech
choice. This is the EPIC: the reference other strata point back to.

**App** (`features/app/<app>/<feature>/`) — the *how* of a **single** app.
Per [ADR-0004](../../../docs/adr/0004-feature-splitting.md): an App feature
is the share of a Business feature in exactly one app, never two. An App
feature with no Business parent is acceptable only if it is purely technical,
and its `index.md` must say so explicitly — otherwise the Business feature is
missing and must be written first.

### Reference direction

References flow **App → Business** and **App → App**. Never the reverse: a
Business feature carries no reference to the App features that implement it
by content — `index.md`'s `Links` section may point to one, but the business
rules themselves stay implementation-blind.

- **App → Business**: an App feature's `business.md` references its Business
  parent rather than copying its rules. It records only what is specific to
  this app — a local restriction, an interpretation, a case only this app
  encounters.
- **App → App**: an App feature may reference another App feature — a
  frontend consuming a backend's `api-contract.md`, for instance — but stays
  within a single app's own directory tree; it does not become a second App
  feature covering that other app.

Duplicating a business rule instead of referencing it guarantees the two
copies diverge — it is a matter of time, not of discipline. A rule has one
authoritative location: the Business feature that owns it.

## Absolute rule — absence is information

An optional file is created only when it has content. There is no fixed
template with sections filled with "N/A": that produces a document nobody can
tell apart from one where the author simply hadn't gotten to it yet. With the
catalogue, the absence of such a file is itself the assertion — "nothing to
say on this subject" — and it is what lets an agent decide what to read
without reading everything.

**The rule gates the optional catalogue, not every file a feature holds.** A
feature also carries files it must have whatever it is about, and for those
the content test does not apply — their absence asserts nothing except that
nobody wrote them. What puts a file on that side of the line is a property a
feature cannot lack and still be one: being **findable**, being possible to
**follow over time**, being possible to **test**. A rubric that does not
apply is information; a missing entry point, a missing history or a missing
set of criteria is a gap.

**Which files those are is declared by whichever module fills the `specs`
slot** — it is that module's rule, not a universal one. Another specs module
may require a different set and remain a valid one. A consumer does not
resolve that set for itself: it delegates the writing to the module's own
writing skill, which applies whatever that module requires. Reaching into the
module's files to read the set is the dynamic resolution
[ADR-0012](../../../docs/adr/0012-specs-contract.md) rejected by name, and
`CLAUDE.md`'s `## Specs contract` block is not the answer either — that block
gives a consumer the *names* a module uses, so it can say "the file named by
`acceptance_file`" instead of hard-coding one, and a key there marks nothing
as required. Until the contract carries the set, a consumer treats it as
undeclared rather than inferring one.

`scrumia-specs`, the module currently in the slot, requires three. `index.md`,
because a feature needs a single entry point to be found and understood
before anything else is opened. `qa.md`, because a feature nobody can test is
not verifiable — and ADR-0004 already makes at least one independently
verifiable scenario constitutive of a feature. `CHANGELOG.md`, because a
feature nobody can follow over time is not maintainable. Every other file in
the catalogue is subject to the content test.

## Absolute rule — no inline history

A spec holds only its current version. No "formerly", no "since v2", no
struck-through section left for context.

The consequence: `CHANGELOG.md` stays short — one entry per notable change,
reverse-chronological, pointing to the PR and the issue that carry the
change and its reasoning. It never explains *why*; the issue does that. A
changelog entry that explains is a spec that has started growing again — that
is exactly how the monolithic PRD this format replaces re-forms.

History lives in three places, one per use: `CHANGELOG.md` for *what* changed
and *when*, in one line; the commits for *who* changed it; the issues for
*why*, and which alternatives were rejected.

## Placement rule — `archi.md`

`archi.md` exists only in a Business feature whose EPIC's implementation
touches two or more apps, and it lives nowhere else — not in an App feature,
not outside `features/` (per
[ADR-0003](../../../docs/adr/0003-cross-cutting-architecture.md), which
rejected that third option). It carries how those apps talk to each other
**for this EPIC**: the contracts at stake, the data flow, the deployment
order if it matters, the degraded modes. It dies with the EPIC it was written
for: the file is deleted once the EPIC closes, not merely left unmaintained —
per the lifespan test below, anything in it that would still have value once
the EPIC closes belongs in an ADR instead, so nothing legitimately left in
`archi.md` at that point is worth keeping.

A decision that outlives the EPIC does not belong in `archi.md` — it is a
project ADR under `docs/adr/`. ADR-0003 states the boundary as a test, quoted
here rather than paraphrased so it stays the one place this rule is stated:

> The test to decide: *if the EPIC is shipped and closed, does this document
> still have value?* Yes → ADR. No → `archi.md`.
