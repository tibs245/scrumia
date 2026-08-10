# Ceremonies — business rules

## Value

For the humans and standing roles deciding whether an occasion beside the ticket path
is worth holding, and for whoever is checking a candidate against this feature before
proposing it. It brings a filter — three admission tests — that keeps such an occasion
from becoming calendar-driven busywork: no ceremony fires on a date alone, reads facts
that do not already exist, or produces nothing that outlives it. It matters because the
founding note dropped BMAD's mandatory ceremonies for exactly that failure — uniform
cost against non-uniform value — and this feature is what stops them creeping back in
under a new name. Not instrumented today: nothing counts how many candidate occasions
were admitted versus refused; the three tests are applied by reading, not by a tool.

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
**recorded** since the previous retrospective read: a deviation record (an override or a
refused split, in `features/business/execution-policy/`'s own two senses), a gate-2
**Blocked** verdict, a label/diff gap flagged in a PR, a ticket reopened after merge.
**No new records, no retrospective.** That is the trigger working, not a degenerate case
of it.

The word *recorded* is doing work there, and the feature it borrows from says why: a
count of zero is evidence of nothing, because nothing forces a deviation to be written
down and an omitted record is indistinguishable from a compliant run
(`features/business/execution-policy/`). This trigger reads that zero anyway, knowingly.
It is safe here and would not be elsewhere: the retrospective's job is to act on what the
project can show, and mobilising a human to confirm that nothing was written down
produces nothing either way. What the zero must never license is the opposite claim —
that the period was clean. A silent period is a period nobody reported on, and if that
silence is itself suspected, the answer is to fix the recording, not to hold a
retrospective that has nothing to read.

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
itself; this feature requires only that it be queryable. The parallel is not yet true in
practice — the deviation record's venue and shape are written down, the mark's are not.
That gap is open, and until it closes BR-6 states an obligation no venue yet accepts.

**Async.** Its whole input is already written down, so nothing in it needs two people
present at the same moment: an agent prepares the reading and proposes the edits, the
human decides when they get to it. Synchronous, it would spend its time re-collecting by
conversation facts that are already queryable — the uniform mobilisation this feature
exists to avoid.

**What it counts, and what it does not settle.** Repetition is counted **on a cell** of
the grid, never on the handle a deviation names: the record carries who decided an
override because a decision has an author, and the retrospective reads it to find a cell
the grid gets wrong, not a person who gets it wrong.

`features/business/execution-policy/` requires the deviation record to be countable and
leaves open *who* counts, *at what threshold*, and whether anything surfaces
the record unprompted. This feature closes none of those three: it names a venue where
the reading happens when it happens, makes nobody accountable for it happening, and sets
no threshold at which a cell should be edited. It does narrow the fourth part of that
question, the *when*: of the three candidates named against that open question — a sprint
boundary, a retrospective, a status pass — this feature specifies the retrospective's own
timing, and leaves the other two as venues it does not speak for.

## Debt audit — admitted

**Trigger.** A human call on a **named area**. That is the whole trigger: nothing today
carries an *area*, so "the same area accumulating findings" is something a human notices
and acts on, not an event a tool can fire. Saying otherwise would fail this feature's own
first test — an event is a *recorded* fact, and a trigger nobody can compute is a trigger
nobody has.

What makes the call worth making is usually that repetition: debt on the path of a ticket
is already filed continuously — `scrumia-ticket` Step 4 turns what an execution notices in
passing into an issue rather than an extra line of diff — so this ceremony is not for
that. It is for what no ticket walks past, and repeated in-passing findings in one area
are the observation that sends someone looking.

**Input.** The specs and the code of that area, the issues already filed against it, and
the gap between a spec and the code that claims to implement it — reported across the
project by the tracker's status pass, and, for one narrow slice of it, by the specs
module's audit of a feature, which catches an interface contract that has drifted from
the code. Nothing shipped checks the general case file by file; the ceremony's reader
does it by hand.

**Its reading is already enacted, per slot; its filing is not.** The composition ships
five audits — `scrumia-tdd-audit`, `scrumia-solid-audit`, `scrumia-rust-audit`,
`scrumia-solidjs-audit`, `scrumia-design-audit` — each in the module that owns the
knowledge its findings need, and each already observing rather than fixing, on an area
asked for up front. This ceremony does not replace them and is not a wrapper over them: it
is the occasion on which one or several are run.

But each of them stops at a **list**, in the session, for a human to turn into tickets.
That is one step short of this ceremony's artefact, and the shortfall is the same one that
disqualifies the sprint's gather below: close the session and the list is gone. So the
filing is the ceremony's own step, not something the audits already did — and it is what
makes the occasion worth naming rather than just running a skill. A project whose
plugged-in modules ship no audit at all still holds the ceremony; it reads the specs, the
code and the filed issues by hand and files the same way.

**A named area is part of the trigger, not a detail.** An audit of "the project" returns
a list nobody triages, which is a document rather than an artefact. The area is named
before the audit starts.

**What it produces that outlives it.** Issues on the tracker, each situated — the file or
the area, what is wrong, how bad. Unlabelled: `scope/*` and `risk/*` are set at
refinement, and an audit that rated its own findings would be doing refinement's job on
a batch it just wrote. Nothing else: **the audit files, it never fixes.** That boundary
is what keeps it from becoming the refactor session dropped below — the moment an audit
starts changing code, it is executing without a ticket, and the acceptance criterion that
makes execution refusable is gone.

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

**This drops the occasion, not the skills.** `scrumia-tdd-refactor` and
`scrumia-solid-refactor` each resolve **one finding**, named before they start — from
their paired audit's list, from an issue, or stated by the person opening them. That
named finding is the scoped intent this section asks for, reached through a skill instead
of by hand, and nothing here refuses it. The intent is what matters, not the venue it was
written in: requiring an issue on the tracker would refuse the shipped skills' own
documented use and would make this feature depend on a tracker slot being filled.

What is dropped is opening one of them on nothing in particular, at no one's request,
because it is Thursday: same skill, no named finding, nothing that could fail, and the
whole objection above applies again.

## The sprint's gather is not a ceremony either

`scrumia-sprint` ends by gathering the batch — per ticket, the PR opened or the reason it
was not, plus what needs human attention. It looks like a ceremony from outside: a named
occasion, at a boundary, reading across several runs. It is not one, and the reason is
this feature's third test.

Its own prose settles it: a deviation reported there is *a second copy for the human in
front of you, not the record* — the record is on the ticket, written when the deviation
was decided. Everything the gather reports already exists somewhere queryable, and the
gather itself survives nothing: close the session and it is gone. No artefact of its own,
so under this feature's BR-3 it is not admitted. The same holds for the sprint's
validation step, where the human approves the batch: that is a decision point **on work in
flight** — a gate's shape, not a ceremony's. The phrase reappears in BR-4 below meaning
something harmless, a human deciding inside an async ceremony; what separates the two is
what is being decided on. Work in flight makes it a gate. Records already written do not.

Naming this matters more than naming the standup. The gather is the one occasion the
composition actually ships that could be mistaken for a ceremony, and it reads across a
sprint's records the way the retrospective does. The two are not redundant: the gather
relays a session's outcome to the human waiting on it, and the retrospective reads what
several sessions left behind in order to change the project. Where a sprint's gather ends
with facts worth acting on, the retrospective is the occasion for acting on them — which
is exactly why a sprint's end is where the call is usually made.

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
2. **A module here would have to assume the slots it reads.**
   `features/business/modular-composition/` BR-3 forbids a module
   assuming another slot is filled. A ceremonies module whose entire input is the
   tracker's record has nothing left to do when the tracker slot is empty — not a
   degraded behaviour it could name, an empty one. A capability that cannot degrade is a
   capability sitting in the wrong place.
3. **Slotless is not the escape hatch.** `scrumia-core` and `scrumia-rules` fill no slot
   because they *describe* the composition — the slot table, the rules format. The
   ceremonies consume it. A slotless module that consumes the composition would be a
   third kind of thing, and nothing found here justifies inventing one.

Those three reasons are the refusal, and they carry no stated cost or reopen condition —
which is what an ADR is for, and what `docs/adr/0013-tracker-stays-one-slot.md` does for
the neighbouring negative decision. Whether this decision belongs in an ADR of its own
instead of here, like that neighbouring one, is an open question. Until it is settled,
this section is the decision's only home, and a spec carries only its current version.

**Where automation lands, if it is ever written.** "One more skill in an existing module"
is [`docs/modules.md`](../../../docs/modules.md)'s own default for a capability that fills
no slot differently, and the composition answers *which* module by placement rather than
by rule: a skill lives where the **knowledge its findings need** lives. That is why five
audits sit in the `practices`, `implementation` and `design` slots and none in the
`tracker`, though every one of them ends in issues. Where the output is filed is not who
knows how to produce it.

Applied here: the debt audit is already enacted per slot by those five, and the part they
cannot see — the spec/code gap — needs the `specs` slot's knowledge, not the tracker's.
The retrospective's knowledge is the execution policy's grid and the roles' judgement,
both the `team` slot's; that is where a skill for it would land, and the edits it proposes
to `settings.team.execution` are that slot's to make.

## Business rules

- **BR-1** — No ceremony triggers on time alone. A calendar may bound when it is
  convenient to look; what fires a ceremony is a recorded fact or a human call.
- **BR-2** — A ceremony reads artefacts that already exist. One whose first job is to
  collect facts by conversation is a recording defect wearing a ceremony's name.
- **BR-3** — A ceremony that produces no artefact of its own is dropped. An artefact the
  ordinary ticket path would have produced anyway is not its own.
- **BR-4** — Synchronous or asynchronous is decided per ceremony and stated with its
  reason. Async is the expected answer, because a ceremony whose input is already written
  needs no simultaneity — and a human's decision inside an async ceremony is a decision
  point, not a reason to make the ceremony synchronous.
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
