# ADR-0025 — A sprint is designed once, before its first worktree; tickets carry a footprint the design crosses

**Status**: accepted — 2026-09-10

## Context

`scrumia-sprint` Step 1 has said since its first version that *two tickets touching the
same files get serialized or merged*, and that *the most reliable signal is the scope
declared in the ticket*. The standard work item form asks for that scope — *which apps,
which files* — as free text under *Additional information*, and `scrumia-refine` makes it
the third condition of "ready".

Measured on a consuming project running fifteen batches of five to eleven tickets in
parallel (MyGamesMaster, 2026-09-06 → 2026-09-10), that signal did not do its job:

- **Three merge collisions that no per-ticket review could see** cost three integration
  gates in one batch: a lot removed a column, another read it from a file it had just
  created; a lot sealed a type, another called the old shape. Each branch was green alone.
  The defect existed in no branch — it was born at their meeting.
- **Two parallel branches allocated the same acceptance identifiers** (`AC-276` to
  `AC-278`) in the same `qa.md`. Nothing reads for that; the second to merge renumbered by
  hand, after the fact.
- **A ticket re-asked a decision already written** in a `tech.md` section, because the
  ticket was written after the decision and nothing made it cite it. The executor would
  have re-arbitrated a settled question.
- **The scope written at refinement was eight migrations behind the tree by launch day**
  and gave one wiring file to two lots. It had been written once and re-derived by nobody:
  a free-text field that a tool cannot read is not a signal, it is a note.
- **Every executor of a batch redid its own global analysis** — reading the same twenty
  specs to answer the same questions its neighbours were answering at the same time — and
  reached slightly different answers. The batch paid the analysis N times and got N views.

The rule was right. What it lacked was a form a tool can cross, a moment when someone
decides what the crossing reveals, and a carrier that puts the decision in front of every
executor before they start.

## Decision

**A sprint is designed once, between its batch and its launch. The design is one analysis
of the batch — specs and code together — that reads the tickets' footprints, decides what
their crossing reveals, and commits its durable decisions on the sprint branch before the
first worktree is cut. Executors implement, test and debug along the lines it states; they
do not redo the analysis.**

Four parts, each owned by the feature that already owned the nearest thing.

### 1. A ticket carries a footprint, not a free-text scope (`work-item-format/standard`)

The *anticipated scope* of BR-5 becomes a **footprint** with four entries: what the
ticket **reuses** (a rule, a port, a decision — cited where it is written), what it
**creates** and for whom, what it **retires**, and which **surfaces** it touches. Written
at refinement, it is the same information the form always asked for, in a shape a tool can
cross and a reviewer can refute. A citation under *reuses* is a decidable condition
(`work-item-format` BR-7): it resolves or the ticket is not ready. That is what makes a
written decision findable by the ticket that needs it — the executor cites, it does not
rediscover.

### 2. The crossing is computed, never written (`scrumia-github-project`)

`scrumia-board overlap --milestone "<sprint>"` reads the footprints of a milestone's open
tickets and reports what only their meeting shows: a non-spec surface two tickets share; a
retirement another ticket reuses; two identical creations; a surface that no longer exists
in the tree. It runs at sprint design, against the tree *as it is that day* — which is how
a footprint written a week earlier is found stale before an executor finds it. It computes
and decides nothing: a shared surface is a fact, serializing or merging is a decision.

A global document listing what every ticket touches was weighed and refused: it is the
programme file that lied on the consuming project. ADR-0008 already says why — state that
lives beside the tracker rots. The global view is derived when asked, from the tickets.

### 3. The sprint design: seams first, then one section per app (`dev-flow`)

Between the batch and its validation, the orchestrator convenes the roles the batch's
surfaces draw — tech always, business when a rule moves, design when a screen does — and
writes one page:

- **The seams** — what crosses apps: a shared contract that changes, a migration and its
  order, a port two tickets need, a spec file two tickets write, a retirement another
  ticket reads. This is where lots merge, order is set, and a shared surface gets its name.
- **Per app** — what the sprint does in each app, on which files, consuming the seams.

The order matters and is the whole point of the split: the collisions were never inside an
app, always between two. Three per-app designs written independently would each be
coherent and wrong at the join. Per app is the right grain for the modules, the reviewers
and `scrumia-extends review --app`; it is the wrong grain to *start* from.

The design names surfaces, an order and shared decisions. It does not design the inside
of a ticket — that stays the ticket's. A line that changes neither a file, nor an order,
nor a lot has no place in it.

### 4. Durable decisions ride the sprint branch; the ephemeral part is the draft sprint PR

The sprint branch exists before the first worktree (`dev-flow` § *The sprint branch*).
The design's durable decisions — the named port, the changed contract, the reserved
migration — are **spec edits committed on that branch** before Step 4b cuts anything.
Every ticket branch inherits them: two executors find the same name in the same file
instead of inventing two. The ephemeral part — the order, the merged lots, a condition
such as "this ticket leaves the batch if that PR is not merged" — is the **body of the
sprint's own PR, opened as a draft on the design commit**. That PR already exists in the
flow (it carries the closes); opening it first makes the design the first thing the
sprint shows and the thing gate 3 reads last. `scrumia-ticket` reads it before the ticket;
the global review of `sprint-fast` reads the aggregate against it.

## Consequences

- **A batch pays the analysis once.** The roles read the specs one time, together, and
  what they decide reaches N executors as the same text. The per-ticket analysis shrinks to
  the ticket.
- **Refinement gets one more condition.** A ticket whose footprint does not resolve is not
  ready. The footprint is filled by whoever refines, which is where the information is
  known — the form's BR-6 logic applied to the scope.
- **The sprint gets one more step and one more artefact.** Bounded: a page, the roles the
  surfaces draw, one convening. `sprint-fast` inherits it by citing Steps 1–3, and its
  global review gains a question it could not ask before — *is the aggregate what the
  design announced?*
- **What it does not prevent, named.** A lot that removes a symbol another lot uses in a
  file it *creates during the sprint* is invisible to any footprint written before it.
  The grep of every retired symbol over the merged tree stays the last net, and the
  design's *retires* list is what tells the reviewer which symbols to grep.
- **A footprint is a dated artefact** (`work-item-format` BR-5): it stays as written. The
  crossing compares it to today's tree; the mismatch is reported, not corrected in place.

## Rejected alternatives

- **One design per app, independently.** Each coherent, the join wrong — the measured
  failure. Kept as the second half of the design, after the seams.
- **A global intent document in the repository.** It is the file that drifted. Refused by
  ADR-0008 already; refused here again with the measurement.
- **Stubs that reserve a place** — an empty port, an empty `AC-<n>` heading — so that two
  tickets cannot collide on it. A reserved hole carries a name and no rule; it reads as
  delivered and is not. The consuming project names this *a hole with a label* and has
  paid for it. Reservation is done by committing the **spec** of the thing, not a stub of
  its code.
- **A mandatory design phase before every ticket.** A mini waterfall; the ticket already
  writes its spec before its code. The design is per *sprint*, about *seams*, and bounded
  to what changes a file, an order or a lot.
- **Uniqueness and renumbering of acceptance identifiers.** Real, and the specs module's:
  `ac_id_format` is its vocabulary. Filed separately rather than folded in here.

## Relates to

- [ADR-0008](0008-state-lives-in-github.md) — the crossing is computed from the tracker;
  no global file.
- [ADR-0020](0020-skill-extension-protocol.md) — the `sprint` register carries a
  project's own surface vocabulary (what must run alone, what blocks its consumers); the
  crossing is generic, the severity is project data.
- [ADR-0005](0005-validation-gates.md) — the design is validated with the batch at the
  human's launch decision; it adds no gate.

## To revisit

- After three sprints designed this way on a consuming project: does the crossing find
  what a reviewer finds, and does the per-app section get read, or only the seams?
- If a tracker other than GitHub fills the slot and has no draft pull request: where the
  ephemeral part lives is that module's to answer under `github-tracking`'s rule.
