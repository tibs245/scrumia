# Ceremonies — business rules

## What a ceremony is here

A **ceremony** is a named occasion that sits beside the ticket path and looks at
several runs at once, mobilising a human or the standing roles.

It is not a gate. A gate ([ADR-0005](../../../docs/adr/0005-validation-gates.md)) sits
inside the execution path and decides whether one change proceeds. A ceremony decides
nothing about a change in flight; it reads what several finished ones left behind.

Convening the roles (`scrumia-standup`) is not a ceremony either: it is a question with
an answer — no trigger of its own, no cadence, nothing it leaves behind.

## Why a calendar is not a trigger

The founding note removes BMAD's mandatory ceremonies deliberately: an occasion that
fires on a date mobilises the human whether or not there is anything to decide. The cost
is uniform, the value is not, and the gap between the two is what makes a method feel
like overhead. Specifying the ceremonies back in without a trigger and an artefact would
reintroduce exactly what was removed.

So: **no ceremony triggers on time alone.** Time may bound *when it is convenient to
look* — a sprint's end, a milestone. What fires the ceremony is a fact already recorded,
or a human deciding to look.

## The three admission tests

A candidate is admitted only if it passes all three.

1. **A trigger that is not a calendar** — an event, meaning a recorded fact, or a human
   call.
2. **An input that already exists** — it reads artefacts written before it starts. A
   ceremony whose first job is to collect facts by conversation is re-collecting what
   the runs should have written down; the fix is the recording, not the ceremony.
3. **An artefact of its own that outlives it** — something queryable once everyone has
   left, and something the ordinary ticket path would not already have produced. *Of its
   own* carries the weight of this test: a candidate whose output is a pull request has
   produced the execution path's artefact, not one of its own.

Failing test 3 is the drop rule: a ceremony that leaves nothing behind is dropped, not
kept for form's sake.

**The tests judge the ceremony, not the run.** A retrospective that reads the facts and
finds nothing worth changing produces no edit, and that is a correct outcome rather than
a failed test — the class is admitted because it produces its artefact whenever the facts
warrant one. What a run may never do is leave no trace of having looked; see the mark
under *Retrospective* below.

## Retrospective — admitted

**Trigger.** A human call at a boundary where facts have accumulated — a sprint's end is
the usual one — and the event that makes the call worth making is at least one fact
recorded since the previous retrospective read: a deviation record, a gate-2 **Blocked**
verdict, a label/diff gap flagged in a PR, a ticket reopened after merge, a refused
split. **No new facts, no retrospective.** That is the trigger working, not a degenerate
case of it.

**Input.** Those records, as the tracker holds them. All of it is written before the
ceremony starts; nothing is reconstructed from anyone's memory of the sprint.

**What it produces that outlives it.** A change to project data or to a spec — a cell
edited in the grid under `settings.team.execution`, a rule changed in a feature, an ADR
opened, an issue filed. And, in every case including the one where it changes nothing,
**a mark of how far it read**.

That mark is not bookkeeping. This ceremony's own trigger is *facts recorded since the
last read*, which is uncomputable if no run says where it stopped: without the mark, the
next retrospective cannot tell a record already read and judged harmless from one nobody
has opened, and the safe reading of that ambiguity is to read everything again, every
time. Which venue holds the mark is the tracker's to say, as with the deviation record
itself; this feature requires only that it be queryable.

**Async.** Its whole input is already written down, so nothing in it needs two people
present at the same moment: an agent prepares the reading and proposes the edits, the
human decides when they get to it. Synchronous, it would spend its time re-collecting by
conversation facts that are already queryable — the uniform mobilisation this feature
exists to avoid.

**What it does not settle.** `features/business/execution-policy/` requires the deviation
record to be countable and leaves open — in #167 — who counts, at what threshold, and
whether anything surfaces the record unprompted. Naming the retrospective as a venue
where that record is read does not close it: this feature says where the reading happens
when it happens, not that anyone is accountable for it happening, and it sets no
threshold at which a cell should be edited.

## Debt audit — admitted

**Trigger.** A human call on a **named area**, or the event repetition makes visible: the
same area accumulating out-of-scope findings across several tickets. Debt on the path of
a ticket is already filed continuously — `scrumia-ticket` Step 4 turns what an execution
notices in passing into an issue rather than an extra line of diff — so this ceremony is
not for that. It is for what no ticket walks past, and repeated in-passing findings in
one area are the signal that the area deserves a look of its own.

**Input.** The specs and the code of that area, the issues already filed against it, and
what the tracker's status pass reports as a gap between spec and code.

**A named area is part of the trigger, not a detail.** An audit of "the project" returns
a list nobody triages, which is a document rather than an artefact. The area is named
before the audit starts.

**What it produces that outlives it.** Issues on the tracker, each carrying the scope and
risk labels that let the execution policy route it. Nothing else: **the audit files, it
never fixes.** That boundary is what keeps it from becoming the refactor session dropped
below — the moment an audit starts changing code, it is executing without a ticket, and
the acceptance criterion that makes execution refusable is gone.

**Async.** It reads artefacts and writes issues; the roles judge in writing and the human
triages a list. Nothing in it requires simultaneity, and a synchronous audit would end in
a spoken list that still has to be written down afterwards — its artefact would be
produced *after* the ceremony rather than *by* it.

## Refactor session — dropped

**It fails test 3.** A refactor session's output is a change to the code, proposed as a
pull request — precisely what the execution path already produces from a scoped ticket.
The session contributes no artefact of its own. What it adds is a second route to
someone else's.

And that second route is worse than redundant. A ticket carries a verifiable acceptance
criterion, and execution is refused without one (`features/business/dev-flow/` AC-1). A
"session" has no such gate: it is execution on an intent nobody wrote down. Keeping it
would reintroduce, under a ceremony's name, the single thing the execution path refuses.

So refactoring is not a ceremony here. It is work, and work is a ticket. Where
refactoring is warranted and nobody has filed it, that is the debt audit's output — and
the audit files an issue, like anything else.

## Where the ceremonies live: no module, no new slot

**`scrumia-ceremonies` is not built.** The two admitted ceremonies are specified here and
enacted through the modules a project already has plugged in. Three reasons, heaviest
first:

1. **Neither end of either ceremony is a new question.** A slot is a question
   (`features/business/modular-composition/` BR-1). Both ceremonies read artefacts the
   `tracker` slot holds, and write into things existing slots already own: the tracker's
   issues, the `team` slot's grid in `.scrumia/config.yaml`, the `specs` slot's features.
   A project wanting "a different retrospective" wants different facts or a different
   grid — it changes the module in one of *those* slots, and the ceremony follows. There
   is no third answer left for a module to give, and a slot nobody can answer differently
   is not a slot.
2. **A module here would have to assume the slots it reads.** BR-3 forbids a module
   assuming another slot is filled. A ceremonies module whose entire input is the
   tracker's record has nothing left to do when the tracker slot is empty — not a
   degraded behaviour it could name, an empty one. A capability that cannot degrade is a
   capability sitting in the wrong place.
3. **Slotless is not the escape hatch.** `scrumia-core` and `scrumia-rules` fill no slot
   because they *describe* the composition — the slot table, the rules format. The
   ceremonies consume it. A slotless module that consumes the composition would be a
   third kind of thing, and nothing found here justifies inventing one.

**Where automation lands, if it is ever written.** Neither ceremony is automated by this
spec; both are practices a human runs with the roles. When one earns a skill, it belongs
to the module that already owns its output — the `team` slot for the retrospective, whose
edits land in `settings.team.execution` and whose judgement is the roles', and the
`tracker` slot for the debt audit, whose output is issues. "One more skill in an existing
module" is [`docs/modules.md`](../../../docs/modules.md)'s own default for a capability
that fills no slot differently, and nothing here beats it.

## Business rules

- **BR-1** — No ceremony triggers on time alone. A calendar may bound when it is
  convenient to look; what fires a ceremony is a recorded fact or a human call.
- **BR-2** — A ceremony reads artefacts that already exist. One whose first job is to
  collect facts by conversation is a recording defect wearing a ceremony's name.
- **BR-3** — A ceremony that produces no artefact of its own is dropped. An artefact the
  ordinary ticket path would have produced anyway is not its own.
- **BR-4** — Synchronous or asynchronous is decided per ceremony and stated with its
  reason. Async is the expected answer, because a ceremony whose input is already written
  needs no simultaneity — and a human's decision inside an async ceremony is a gate, not
  a reason to make the ceremony synchronous.
- **BR-5** — The debt audit files issues and never changes code. Changing code is a
  ticket, gated by an acceptance criterion.
- **BR-6** — A retrospective leaves a queryable mark of how far it read, whether or not it
  changed anything, because its own trigger reads that mark.
- **BR-7** — Ceremonies are specified here and enacted through the plugged-in modules. No
  `ceremonies` slot exists and no module claims one; a candidate ceremony is admitted or
  dropped by the three tests, never by a module wanting content.

## Vocabulary

- **Ceremony** — an occasion beside the ticket path, looking at several runs at once.
  Reserved for what passes the three tests; a candidate that fails one is not "a light
  ceremony", it is dropped.
- **Gate** — a decision point inside the execution path, on one change (ADR-0005). Never
  called a ceremony, and never counted as one: a project with three gates and two
  ceremonies has five things, not five ceremonies.
- **Session** — deliberately unused as a name for work. What "refactor session" named is
  a ticket; calling it a session is what let it skip the acceptance criterion.
