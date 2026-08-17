# Work item format — business rules

## Value

For whoever writes or picks up an issue — a human or one of the standing roles. It brings
issues that read the same whichever agent wrote them and whichever tracker holds them, so
picking one up costs no re-reading of how this project happens to phrase things. It
matters because the two properties usually traded against each other — every issue looks
alike, and this project's issues look like this project — stop being a trade: the shape is
fixed, the content is composed from the modules the project already runs. Measured: an
issue's conformity is a verdict a module renders, so drift is countable — how many issues
were opened without a criterion that can fail, how many ran under an unresolved alert,
read off the verdicts rather than estimated by reading the backlog.

## BR-1 — The form is declared by a module; the tracker renders it

A project declares the shape of its work items the way it declares its specs and its
design system: by running a module that owns it, which publishes a contract the other
modules read.

The tracker's job is to **render** that form onto its own tool — issue templates, labels,
sub-issues, whatever the tool offers — and to call its judgement. It defines none of it.

The rule bites in both directions, and both are what it is for:

- Changing tracker keeps the form. The issues carry the same sections before and after.
- Changing form keeps the tracker. Nothing in it needs editing to accept a different one.

Before this rule, neither held: the form lived inside the tracker module, so a project
could not have one without the other.

## BR-2 — A form is a set of atomic rules, one responsibility per file

A form is not a template file. It is a set of rules, each stating one thing, each in its
own file, distributed through registers so that a consumer receives exactly the rules that
apply to what it is doing.

This is what lets a form be recomposed rather than forked. A project that wants a lighter
form drops rules; a project with a regulated domain adds them; neither edits a rule that
already exists to make room.

## BR-3 — The form supplies a judgement, not only a template

A form states how an issue is written **and** decides whether a given issue meets it. The
two ship together, in the same module, because a check written apart from the rules it
checks is a second rendering of them — and a second rendering is the one that drifts.

**That judgement is asked at more than one moment, and it is written once.** Deciding that
an issue may be started, and deciding that it may be executed, are the same question posed
at two moments. Writing it twice is what let the two answers diverge: one gate accepting
what the other refuses, with no way to tell which was right.

**The severity belongs to the caller, not to the form.** The form returns what it found;
whether that stops the caller is the caller's to decide. Refinement may refuse to promote
an issue on the same verdict under which execution proceeds with an alert — one is a
decision nobody is waiting on, the other is a run in flight.

## BR-4 — The verdict alerts; the human decides

A verdict never blocks on its own. It reports what the form found missing, and whoever is
running the work decides what to do about it. Stopping a run is a decision a person takes,
not a consequence a form imposes.

**A verdict is recorded where the work item lives, and it outlives the run.** An alert
that exists only in an agent's output is an alert nobody reads on a run that dies, and a
run executed under an unresolved alert must remain visible afterwards — that visibility is
the whole compensation for not blocking.

What this costs is stated rather than discovered: **where nobody is watching, nothing is
enforced.** Work running unattended proceeds under an alert exactly as it would without
one. The record is what makes that countable after the fact; it is not what prevents it.

## BR-5 — A work item is a dated artefact, not a view

What is written into a work item stays as written. It is not recomputed to match the
project's current rules, and it does not silently follow a rule that changed after it was
filed.

This is deliberate and it is the point: a work item carries the history of what was known
and required when it was opened. Re-evaluating one is an explicit act that leaves its own
trace, so the rules an issue was judged under stay recoverable rather than being
overwritten by today's.

The consequence accepted with it: a rule that changes does not propagate to issues already
open. Bringing them into line is work someone decides to do, on the issues they choose.

## BR-6 — Readiness and doneness are composed, never written by the form

The form declares that a work item carries a definition of ready and a definition of done.
It does not write their content.

That content is contributed by the modules the project runs — the practices, the
implementation modules, the compliance ones — each declaring what it requires before work
starts in its territory and what it requires before work is called finished. A project
whose apps run different modules gets different lists per app without anyone maintaining
two forms.

A form that wrote those lists itself would be a form that has to know every practice a
project might adopt. That is the coupling this rule exists to prevent.

## BR-7 — A condition must be decidable without reading the rule it guards

Every contributed rule states when it applies, and rules that do not apply are not read.
That filtering is what allows a project to carry many rules without every reader paying
for all of them.

It puts the whole weight on the condition being answerable from what the reader already
has — the project's composition, the app's own modules, a configuration flag, or what the
work item plainly states. *"When the project runs unit tests"* qualifies. *"When
relevant"* does not: it can only be answered by reading the rule, which is what the
condition was supposed to avoid.

What this costs, stated once: **a condition nobody recognises as applying yields a rule
nobody applies, silently.** There is no error, no gap in the output, and nothing marks the
absence. That is the price of filtering, and it is why the burden sits on the condition's
wording rather than on the reader's diligence.

## BR-8 — What a form may require is bounded by what a tracker can render

A form may require anything that a tracker can express as a title, a body and labels.
Beyond that, portability stops: trackers differ on whether fields are freely declared by
the project or fixed by a schema the tool owns, and a form built on the permissive answer
cannot be rendered on the strict one.

A form is free to be richer than that; it is then a form for the trackers that can carry
it, and it says so rather than being discovered not to fit.

## What this feature does not own

Three boundaries, stated so they are not inferred:

- **What a classification means.** That an issue carries a measure of reach and a measure
  of risk is this feature's; what each level of those axes says is `execution-policy`'s.
- **Where a work item is in its flow.** Columns, transitions, what is a ticket and what is
  a discussion: `github-tracking`'s.
- **How the change reaches the default branch.** Branches, isolation, the reviewable
  proposal: `dev-flow`'s. A form states no branch name — a name a tool derives and a human
  can mistype has one failure mode and no benefit.

## Open questions

- **What a form's contract block declares, and under which keys.** That a form publishes
  one is BR-1's; the vocabulary is not settled.
- **Whether several forms may be composed in one project at once** — a lighter and a
  heavier variant of the same module, chosen per app. Nothing above forbids it and nothing
  above requires it; it is left open rather than answered by omission.
- **Who counts the issues started under an unresolved alert, and at what threshold that
  becomes a signal.** BR-4 makes the count possible and names no reader for it.
