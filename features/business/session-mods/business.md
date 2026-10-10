# Session mods — business rules

## Value

For the person who drives long agent sessions and for the agent working in them. A
session mod brings the person a place where what belongs to them waits at their own pace
instead of interrupting the work or sinking in the scrollback, and brings the agent a
way to carry on without guessing at a decision that is not its own. It matters because
without it every decision of the person's either blocks the session on a question typed
in chat, or is taken silently by the agent. Not instrumented today: nothing counts
parked questions, answers lost or sessions unblocked; the value is read by trying the
mod in a session.

## What a session mod is

A session mod is a Claude Code **mod**: a plugin whose behaviour is function hooks
registered against the session, not skills an agent reads. It acts while the session
runs — it adds a tool the model may call, a band above the prompt, a command, a pane —
and it keeps its own state on the machine, never in the repository.

A session mod is a plugin of its own, without a slot in the composition: nothing in the
composition's six questions is answered by it, and a project that does not install it
loses nothing the other modules owe. Two session mods share a technique, not a need, so
each is specified by its own section below and shipped by its own plugin.

State kept by a session mod is a buffer, not a record. The tracker holds the project's
state; a session mod holds what is in flight between the person and the model.

## scrumia-questions

The questions inbox. The model parks a question that belongs to the person instead of
blocking the session on it; the person reads and answers from a pane when they choose;
the answers return once, together, with their next prompt.

### The shape of a question

A question carries:

- a **context** — the situation it arises from;
- a **linked ticket**, optional — free text naming the ticket the decision belongs to;
- the **question** itself;
- its **impact** — what changes depending on the answer;
- whether it **blocks** — true when part of the work cannot proceed without the answer,
  false when the work can go on;
- **suggested answers**, one to six, and optionally **one recommended**, which is one of
  them.

**BR-q1** — A question missing any of its mandatory parts, or whose parts are malformed,
is refused with the reason, and nothing is stored. Context, question and impact are
non-empty text; the blocking mark is a boolean; the suggested answers are one to six
non-empty texts; a recommendation, when given, is copied from the suggested answers. The
model reads the reason and asks again, so the inbox never holds a question it cannot show.

**BR-q2** — Parking answers the model at once and says what to do next. A question that
blocks tells the model not to go ahead on what depends on it and to carry on with what
does not; a question that can wait tells it to carry on. The answer arrives later, in a
prompt.

**BR-q3** — Questions are numbered in the order they are parked, per project. A question
removed leaves its number unused.

### How a question is answered

**BR-q4** — The person is always offered `Other`, after the suggested answers. `Other`
needs a note: with no note it says nothing, so it is not ready to be sent.

**BR-q5** — `Additional notes` are offered with every question and travel with the answer
whichever choice was picked, suggested answer or `Other`.

**BR-q6** — The recommended answer, when there is one, is preselected, and counts as the
answer if the person picks nothing else. A question with no recommendation and no pick is
not ready.

**BR-q7** — Answers are given in one pass. Picking and noting only prepare a draft; one
action, labelled with the number of answers it sends, sends every ready answer of the
view the person is looking at, and leaves the others waiting. Blocking questions are
shown first, and the person can narrow the view to the blocking or the non-blocking ones.

**BR-q8** — The person may remove a question they no longer want to answer; it is gone,
its answer never sent.

### How an answer returns

**BR-q9** — A sent answer reaches the model as context beside the person's next prompt,
once. Each carries the question's number, its linked ticket when there is one, the
question, the answer and the notes. The text the person typed is never altered; the
question texts are labelled as the model's own and the answers and notes as the person's,
so the model's words never pass for the person's voice.

**BR-q10** — An answer counts as delivered only once the prompt carrying it went through.
A prompt refused further down leaves the answers to the next one.

**BR-q11** — A returned answer carries the linked ticket's number. The inbox is a buffer,
not a record: the decision taken is reported in that ticket, because state lives in the
tracker, and what the buffer held is gone once delivered and purged.

### Where it lives

**BR-q12** — Questions belong to the machine and to the project root they were asked in.
Nothing is written in the repository, and a session in another project never sees them.
Two sessions open on the same project share its inbox.

**BR-q13** — Writes to the inbox go through one queue, so questions parked at the same
moment are all kept. Two processes writing the same project at the same instant are not
protected.

**BR-q14** — A delivered question is dropped thirty days after it was asked. A question
not yet answered or not yet delivered is never dropped by age.

**BR-q15** — A question stored in an older shape, without the blocking mark, still shows,
as one that can wait.

### What it shows without being opened

**BR-q16** — While a question waits, a band above the prompt says how many wait and how
many of them block, and offers to open the inbox. It is absent when nothing waits.

### What it is not

It is not a tracker and not a chat: it holds no decision once delivered, and it asks
nothing of the person on its own. It reads nothing of the other modules; the linked
ticket is free text.

## scrumia-issues

Placeholder. This mod is specified by its own ticket, which adds its section here.

## scrumia-roadmap

Placeholder. This mod is specified by its own ticket, which adds its section here.
