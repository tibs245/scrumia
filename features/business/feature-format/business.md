# Feature format — business rules

## Value

For everyone who writes or reads a spec — the humans steering the project and
the agents executing its tickets. It brings bounded reading: targeted files
with declared boundaries, so a reader loads only what its task needs and an
absence is an assertion rather than an oversight. It matters because the spec
channel is what execution runs on — a format that drifts turns every ticket
into archaeology. Measured: the validation gate's finding count over the
specs tree, which CI holds at zero.

## The two strata

**Business** (`features/business/<feature>/`) — the *what*. Business value,
business rules, domain vocabulary, invariants — and what makes the feature
worth building: the personas, the use cases, the impact on the business, the
user journey as intent. No screen, no API, no tech choice. This is the EPIC:
the reference other strata point back to.

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

### Disposition on disk

Within a stratum, a feature either sits beside its neighbours or **inside**
one of them. One thing licenses nesting: the parent states what any answer to
its question is held to, and the child is one such answer. Dependency, a
shared subject, or a mention are not nesting — they are two features side by
side, linked.

The distinction is not filing preference. Nesting says a reader cannot
understand the child without its parent; juxtaposition says the two are
peers. Getting it wrong wastes one of those two reads, every time.

Three constraints hold:

- A parent is a full feature, carrying every mandatory file with content of
  its own. This format has no grouping directory — a directory that exists
  only to hold children is flattened — at any depth.
- Depth is bounded by **structure**, not by a number. A child of a child is
  legitimate when each node carries its own content, the relationship is
  declared on both sides, and the deeper level expresses a constraint the
  parent itself does not state. The same test applies at every level.
- Both sides declare the relationship. A child's stratum is its parent's.

### The link vocabulary is fixed

An index's links use a closed set of keys. Four are **structural** — they
describe where the feature sits, in which stratum and in which directory —
and are declared on both sides; the rest are **referential**, pointing at an
authority that owes nothing back. **Cited by** is a referential key for
the inverse asymmetry the consumer raises: a feature that names this one
as the home of a finding rather than as something it consumes.

Left open, the vocabulary grows: one key per writer's intuition, several
meaning the same thing, and a link nobody can resolve mechanically is a link
nobody checks. The closed set is what makes a one-sided structural link
detectable rather than a matter of noticing.

## Absolute rule — every file has a three-part boundary

The catalogue does not merely name each file's subject: for every file it
states what the file **holds**, what it **may hold**, and what it **must not
hold** — and every exclusion names the file where that content goes instead.
A scope that only described its subject would leave the boundary to taste,
and taste is how nine indexes grew sections no template defined.

Three boundaries carry most of the collisions; each is settled by one
membership test, stated once and applied by the catalogue's entries:

- **business vs ux, on the journey.** A step stated as actor intent and the
  value delivered, naming no screen, no control, no click path, belongs to
  the business file. The moment it names one, it belongs to the UX file.
  Same journey, two altitudes: business says why the steps exist, UX says
  what the user sees at each one.
- **tech vs archi, on data flow.** Flow that never leaves the app's own
  boundary belongs to the tech file. Flow that crosses apps, scoped to an
  EPIC, belongs to `archi.md`.
- **business vs tech, on mechanisms.** A rule that constrains what the
  product promises — whatever tool enacts it — belongs to the business file.
  How a tool, command or flag achieves it, and what happens when it is
  misused, belongs to the tech file.
- **ux vs qa, on accessibility.** A property the journey must have, stated
  in prose, belongs to the UX file. Anything testable against a named
  technical criterion is an acceptance criterion, tagged as such. A rule the
  design system owns is cited, never restated.

## Absolute rule — the index indexes

The feature's index is the entry point, and nothing else: the brief, the
links with one line of key info each, the file table saying when to read
each file. **A rule, a decision or a rationale in an index is a defect**,
whatever heading it hides under — its home is the file whose subject it is,
and the catalogue's boundary entries name that home. The section set an
index may carry is declared in exactly one place, the specs module's index
template, so a section outside the set is detectable rather than a matter
of taste.

## Absolute rule — a spec cites no ticket

Issues and PRs are the tracker's; a spec that carries a ticket number is
caching tracker state, and it goes stale the day the ticket closes. The
changelog is the one exception — pointing at the tickets that carry the why
is its job. Everywhere else the fact or the open question is stated in
words, and the tracker is searched for whatever tracks it.

## Absolute rule — every feature states its value

`business.md` exists in every feature, and opens with four answers: who the
feature is for, what it brings them, why it matters, and whether that
contribution can be measured — the measure named, or the honest note that it
is not instrumented today. A feature whose value cannot be stated is a
splitting or deletion candidate, not a feature missing a paragraph.

## Findability — the global index

The specs root carries a global index: one line per feature — stratum,
status, one-line brief — so a feature is reachable without a pointer and
without walking the tree. It is generated by a committed tool, never edited
by hand, and validation fails on any drift between the tree and the index —
a stale index is worse than none, because it is believed. The contract key
naming it is `global_index`
([ADR-0016](../../../docs/adr/0016-global-feature-index.md)).

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

`scrumia-specs`, the module currently in the slot, declares two existence
categories, and declares them together where its catalogue lives. **Mandatory
in every feature**: `index.md`, because a feature needs a single entry point
to be found and understood before anything else is opened; `qa.md`, because a
feature nobody can test is not verifiable — and ADR-0004 already makes at
least one independently verifiable scenario constitutive of a feature;
`CHANGELOG.md`, because a feature nobody can follow over time is not
maintainable; `business.md`, because a feature that cannot say who it serves
and why it is worth building is not a unit of value — at the App stratum it
carries the value of this app's share and a reference to the parent, never a
copy of its rules. **Content-tested**: every other file in the catalogue. The
categories are declared explicitly, not inferred from a table cell — a
consumer must be able to read which category a file is in.

### The content test is answered, not felt

"Has content" is a judgement, and a judgement left to prose is applied
differently by every writer — and defaulted to "no" by any reader in a hurry,
which is how a conditional file never gets written while its absence is read
as an assertion nobody made.

So each optional subject carries the closed questions that decide whether it
applies, each with the answer to take when unsure. The writer answers them
rather than deciding by feel, and **reports which subjects were declined and
on which answer**. An absence nobody can see was considered asserts nothing:
the report is what makes "absence is information" true rather than merely
claimed.

A project whose obligations do not vary feature by feature may take the
judgement out of the writer's hands per subject — required always, decided by
context, or off entirely — through its configuration. Requiring one always
means a feature with nothing to state says so explicitly, with a date, rather
than leaving an empty file. The mandatory set ignores the setting: it is not
a preference.

## Absolute rule — no inline history

A spec holds only its current version. No "formerly", no "since v2", no
struck-through section left for context.

The consequence: `CHANGELOG.md` stays short — one entry per notable change,
reverse-chronological, stating the issue that carries the change and the
category of change it is. It never explains *why*; the issue does that. A
changelog entry that explains is a spec that has started growing again — that
is exactly how the monolithic PRD this format replaces re-forms.

An entry names **only what exists when it is written** — the issue does, a PR
number does not, since the entry ships inside the PR. A field nobody can fill
gets a placeholder, and a placeholder reads as complete to anything that does not
squint. And an entry classifies **one** change: a change spanning two categories
is two entries, since a single label would be false about half of it. Which
categories, and why [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)'s set
is narrowed for a document, is the catalogue's to state.

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
