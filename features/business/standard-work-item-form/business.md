# Standard work item form — business rules

## Value

For whoever opens an issue on a project running this form. It brings a shape short enough
to fill honestly — three things to write — and complete enough that whoever picks the
issue up needs nothing else. It matters because the two usual failures of an issue
template sit at opposite ends: the long form nobody fills, which produces fields reading
"N/A", and the free-text issue that produces a ticket somebody has to interview its author
about. Measured: the three written sections are each verifiable on their own terms, so an
issue's conformity is countable rather than a matter of taste.

The general rules any form is held to are `work-item-format`'s; this feature states what
this particular form prescribes.

## BR-1 — Five sections, and only three are written by hand

An issue carries a title and five sections, in this order:

| Section | Holds | Filled |
|---|---|---|
| Need | why this exists, from a user's standpoint | by whoever opens the issue |
| Acceptance criteria | what has to be true for it to be finished | by whoever opens the issue |
| Definition of Done | what the project requires of finished work here | composed |
| Definition of Ready | what the project requires before work starts here | composed |
| Additional information | the rattachement: parent feature, anticipated scope | by whoever opens the issue |

Three written, two composed. That count is the form's central claim: it reads as a rich
issue and costs three fields.

No section is optional and none is omitted when it has nothing in it — an absent section
and an unanswered one are told apart by what is under the heading, not by whether the
heading is there.

**No fixed section for a subject the project may not have.** Security, compliance,
performance and their like are not headings here. A project to which one applies
contributes it into the composed sections; a project to which none applies never writes
"N/A". A heading everyone must fill and most must fill with nothing is the noise that
makes a form stop being read.

## BR-2 — The title states the outcome, not the task

A title says what is true once the issue is closed. "Refinement rejects an issue with no
criterion that can fail" is a title; "Add a check to the refine skill" is a task, and it
stops being accurate the moment the work is done differently than anticipated.

This is the only part of the issue most readers ever see — on a board, in a list, in a
search result — so it carries the outcome or it carries nothing useful.

## BR-3 — The need is one user story

```
As a {user}, I want {capability} so that {outcome}.
```

One sentence, one user, one capability. The skeleton is prescribed rather than suggested
because its three slots are what make an unstated user or a missing purpose visible: a
need that cannot be written this way is a need whose beneficiary has not been decided.

Where the user is an agent, a role or another module, it is named as such. The form does
not assume a human beneficiary.

## BR-4 — An acceptance criterion is a sentence that can fail

Each criterion is stated so that it can be shown false. "The user can retrieve their
invoice for a closed month" can fail; "the experience is smooth" cannot, and a criterion
that cannot fail says nothing about whether the work is done.

Criteria live in the issue in the form's own words. Where the project runs a specs module,
the criteria the issue satisfies are cited by that module's identifiers as well — the spec
holds the authority, the issue holds the reference.

## BR-5 — The rattachement names the parent feature and the anticipated scope

Two entries under *Additional information*, and they answer different questions:

- **The parent feature** — where the rules this issue serves are written. It is named
  through the specs module's own vocabulary, never as a path typed in from memory: a
  project with a differently-shaped specs module has a different root, and a hard-coded
  path stops being true there without anything reporting it.
- **The anticipated scope** — which apps and which files this is expected to touch. It is
  what makes the issue sizeable before anyone opens an editor, and what a classification
  is set from.

**Nothing derivable is written here.** A branch name, an identifier, a column: whatever a
tool computes, the issue does not restate. A field a tool can derive and a human can
mistype has one failure mode and no benefit.

## BR-6 — The composed sections are filled at the moment they become decisions

The two composed sections are not filled when the issue is written. They are filled when
the issue is judged ready to start, which is when the project's requirements for it are
actually known.

- **Definition of Ready** is the list the project requires before work starts here,
  resolved at that moment and written into the issue as the decision it records.
- **Definition of Done** is the list the project requires of finished work here, written
  at that same moment because it is followed and ticked during the run.

Both are written into the issue and stay as written — `work-item-format`'s BR-5 governs
that, and it is what makes an issue readable years later against the rules it was actually
judged under.

## BR-7 — What this form does not prescribe

- **What a classification level means.** The issue carries a measure of reach and a
  measure of risk; `execution-policy` says what each level says.
- **Where the issue sits.** Columns, cards, what is a ticket and what is a discussion:
  `github-tracking`.
- **How the change ships.** Branch, isolation, proposal: `dev-flow`.
- **How the issue is rendered.** Templates, label creation, sub-issue linking: whichever
  module fills the tracker slot, per `work-item-format`'s BR-1.

## Open questions

- **Whether lighter and heavier variants of this form ship beside it**, and whether they
  would be separate modules or separate compositions of this one. Only the standard form
  is composed today.
- **What an epic carries under this form.** The sections above describe a ticket; whether
  an epic is the same shape with sections left unanswered, or a form of its own, is not
  settled.
