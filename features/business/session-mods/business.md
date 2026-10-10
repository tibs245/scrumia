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
composition's six questions (specs, tracker, team, discovery, design, implementation) is
answered by it, and a project that does not install it loses nothing the other modules
owe. Two session mods share a technique, not a need, so each is specified by its own
section below and shipped by its own plugin.

A session mod is a plugin like any other for module-anatomy: it passes
`scrumia-module check`. "Mod" names the technique (function hooks), not a category of
module, and there is none (`docs/adr/0024-no-category-of-module.md`).

**The three plugin names and tool names are frozen**, because the plugin name is part of
the tool name the model calls (`mcp__<plugin>__<tool>`) and a project's prompts and
permissions come to name it. A later version keeps a pair, or announces the change in its
changelog. Each section below cites this paragraph and does not restate the pair.

| Plugin | Tool |
|---|---|
| `scrumia-questions` | `mcp__scrumia-questions__ask_later` |
| `scrumia-issues` | `mcp__scrumia-issues__track_issue` |
| `scrumia-roadmap` | `mcp__scrumia-roadmap__plan_sprint` |

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

**BR-q17** — The question, the linked ticket, every suggested answer and the recommendation
are single lines: a line break or any control character in one of them refuses the call,
with a reason naming the field. They are copied as they are into the note the model reads
beside the person's answer, so a line break would let the model write a line that passes for
the person's answer. Context and impact are only drawn in the pane and may span several
lines.

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

**BR-q9** — A sent answer reaches the model as context beside the next prompt the person
typed, once. A prompt the person did not type (an agent's hand-back, a background-task
notification, a peer or coordinator message, a scheduled trigger, a prompt submitted by
another plugin, a prompt whose origin is not known) leaves the answers where they are; only
the person's own gesture (the prompt box, the Remote Control bridge) and a plugin submitting
explicitly as the person count as typed. Each carries the question's number, its linked ticket when there is one, the
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
Two sessions open on the same project share its inbox: an answer given in one session is
delivered at the next typed prompt of whichever session reads the project first.

**BR-q13** — Writes to the inbox go through one queue, so questions parked at the same
moment are all kept. Two processes writing the same project at the same instant are not
protected.

**BR-q14** — A delivered question is dropped thirty days after it was delivered, at the
next delivery that follows. A question stored without its delivery time counts from the day
it was asked. A question not yet answered or not yet delivered is never dropped by age.

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

The tickets of the session. The mod keeps one table of every ticket the session named,
with whether the session took it into account, its status and what exactly remains, so
the person tells where each one stands without rereading the conversation.

### The table

One row per ticket, four columns:

- the **ticket** — its number, as named by the person or by the agent;
- **in session** — `yes` when the session worked on or covered the ticket, `no` when it
  only named it, `?` while nobody has assessed it. A ticket merely named is not taken into
  account;
- the **status** — a column of the tracker, or `Unknown`;
- **remaining** — what exactly is left to do, in a sentence from which the state can be
  read, or `nothing` when nothing is left. A row never carries a status without that
  sentence.

Open tickets are listed before the ones in the done column of the tracker, each in
number order, under a summary line (tickets named, taken into account, open).

**BR-i1** — The agent records a ticket with one tool, `track_issue`: the number, whether
the session took it into account, its status and what remains, and optionally a short
title. Recording a ticket already in the table updates its row in place; a ticket is never
listed twice.

**BR-i2** — The row of a ticket nobody has assessed reads `?`, status `Unknown` and
`Not assessed yet`. It stays in the table until the agent records it: nothing is silently
forgotten.

**BR-i3** — A malformed call is refused with the reason, and nothing is stored. The number
is an integer from 1; the "taken into account" mark is a boolean; the status is one of the
statuses of BR-i5; the remaining text is non-empty; a title, when given, is text. The agent
reads the reason and calls again, so the table never holds a row it cannot draw.

**BR-i4** — Writes to the table go through one queue, so tickets recorded or detected at
the same moment are all kept. Two processes writing the same session at the same instant
are not protected.

### Where the statuses come from

**BR-i5** — The statuses are the columns the tracker module is configured with (the
`columns` of `scrumia-github-project`, read through `scrumia-extends --settings`), plus
`Unknown`, never a list written into the mod. When the tracker declares no `columns`, the
keys of its `board.options` are the columns. A project with other columns gets its own.
They are read when the session starts, before the tool is registered, so the tool's
schema lists them, and kept once a read has succeeded. A status is matched whatever its case and stored as the tracker spells
it. The last column, or the one the tracker's `board.flow.done` names, is the one that
closes a ticket.

**BR-i6** — When the tracker's columns cannot be read — the command is missing, fails,
declares no tracker module or no columns — the mod falls back to the six default columns
(`Backlog`, `Ready for dev`, `To dev`, `In progress`, `In review`, `Done`) plus `Unknown`,
and says so in the pane with the reason. It never stops working for want of a tracker.
Only a successful read is kept for the process: after a failure the defaults serve that
one call and the next call reads again, so a tracker that was briefly unreachable is
picked up as soon as it answers.

**BR-i7** — The agent reports the status; the mod does not read the board and makes no
network call. The tool's description tells the agent to read the ticket's status from the
board first (for example with `scrumia-board` when it is available, that command belonging to the
tracker module and possibly absent) and to report that. The mod therefore cannot tell a
status that is stale or wrong from one that is right: the table is what the agent said,
which is why `remaining` is written as a sentence the person can check. Reading the board
from the mod, and what it would do when the board is unreachable, is a refusal here, not a
gap.

### How a ticket reaches the table without the agent

**BR-i8** — Every ticket number written with a leading hash in a prompt the person typed is added to the table at once as
not assessed, and the next prompt carries a reminder, labelled with the mod's name, asking
the agent to read each ticket's status on the board and record it. The reminder rides a
ticket once: it is marked reminded only when the prompt carrying it went through, so a
prompt refused further down leaves it for the next one.

**BR-i9** — A prompt the person did not type is never read for ticket numbers: an agent's
hand-back, a background-task notification, a peer or coordinator message, a scheduled
trigger, a prompt submitted by another plugin, and a prompt whose origin is not known. Only
the person's own gesture (the prompt box, the Remote Control bridge) and a plugin submitting
explicitly as the person count as typed.

**BR-i10** — The mod never reads what it wrote itself, nor what is not a ticket. Lines
carrying the mod's own label are left out, so its reminder pasted back or quoted by the
agent names nothing; code spans and fenced code are left out; a number preceded by a word
character, `&` or `/` (an entity, a link fragment) is not a ticket; a hash followed by a
number with a leading zero (`0012`, `000`) is not a ticket, since a ticket number starts with 1 to 9. A three-digit colour made of other digits, outside code,
remains read as a ticket: it is a known limit.

**BR-i11** — A ticket the agent names alone reaches the table without depending on the
agent remembering to call the tool: the final text of each turn the agent completed is read
as the person's prompt is (BR-i10), the tickets it names are added as not assessed, and the
next prompt the person types carries the reminder of BR-i8. A turn that was interrupted,
refused or failed is not read. The gap that remains is a ticket named only in text the agent
wrote before a tool call within the turn: only the final text is seen, and that is stated
rather than hidden.

### What "this session" means

**BR-i12** — The table belongs to the session, identified by the id the session answers
to. The same id back — a session resumed under its own id — shows the same table. A
`/clear` starts the conversation under a new id, so the table starts empty, and the
previous one stays stored under its id. A resume that goes on under a new id (a fork)
starts empty too. Nothing in the table reaches another session.

**BR-i13** — Tables are kept on the machine for the thirty most recently touched sessions; the
oldest beyond that are dropped. Nothing is written in the repository: the table is a
buffer, and the state of a ticket lives in the tracker.

### What it shows

**BR-i14** — `/issues` opens a pane showing the table, drawn on the terminal and on the
desktop app. With no ticket named, the pane says so. It always says where its statuses come
from: the tracker's columns, or the defaults and why.

### Where it lives

**BR-i15** — A plugin of its own, without a slot in the composition, as decided in
`docs/adr/0026-session-mods-are-plugins-of-their-own.md`. Its plugin name and tool name are
frozen, as the introduction states.

### Known limits

- A three-digit colour made of digits other than zeros (`111`), outside code, is read as a
  ticket.
- The `scrumia-questions` mod writes its own numbers with a hash too: an agent that
  cites a question by its number and hash adds a ticket that does not exist to the table, as not assessed. The
  mod cannot tell a question from a ticket; the agent records it as `Unknown` with
  `remaining` saying so, or the person ignores the row.
- The final text of a turn is the only agent text read (BR-i11).

### What it is not

It is not the tracker and does not move a ticket on the board. It reads nothing of the
board; the only thing it reads of the other modules is the list of columns.

## scrumia-roadmap

The roadmap. The person asks the session to take some lots of tickets into account; the
agent plans them as sprints and records each one; the person reads, from a pane, what each
sprint holds and what they will really be able to try at its end. Placement: a plugin of
its own, per `docs/adr/0026-session-mods-are-plugins-of-their-own.md`; no new decision. Its
names are the frozen pair of the introduction.

A **lot** is whatever the person asks the session to take into account: a milestone, a
list of ticket numbers, a board column, or something else. The agent resolves it and
records it with its **source**; the mod reads no ticket state, only the tracker's list of
columns (the module `scrumia-github-project` is optional: defaults apply without it), so it
holds only what the agent recorded and says when it did.

A **sprint** here is one such lot, as the roadmap names it. It is not dev-flow's sprint, a
batch of tickets executed in parallel on a branch of its own
([dev-flow](../dev-flow/business.md), "The sprint branch"): a roadmap sprint may never be
executed that way, and a batch executed that way need not be on the roadmap.

### The shape of a sprint

A sprint carries:

- a **name**, which identifies it, and an **order**, an integer, its place in the roadmap;
- a **source** — a kind (milestone, tickets, column, other) and a reference in free text;
- an **objective** — what the sprint is for;
- **testable at the end** — what a person can really try once the sprint is over, not what
  is merely implemented; a sprint with nothing to try says so explicitly instead of
  leaving the list empty;
- its **tickets**, each with a number, a title, a description and its board status;
- a **state**: planned, running or done;
- the time it was last **resolved** from its source, stamped by the mod, not given by the agent.

**BR-r1** — A sprint missing any of its mandatory parts, or whose parts are malformed, is
refused with the reason, and nothing is stored. Name and objective are non-empty text; the
order is an integer; the source has a known kind and a non-empty reference; the state is
one of the three; the tickets are a non-empty list, each with a positive number, a title,
a description and a status, no number twice in one sprint. A ticket's status is one of the
columns of the tracker module, read as the issues table reads them (**BR-i5**, **BR-i6**:
`scrumia-extends --settings`, the six default columns when they cannot be read), plus
`Unknown`; any other status is refused with the list of columns, and is stored as the
tracker spells it. The order is unique in a project: a sprint recorded under a new name
with the order of another is refused, naming that sprint; recorded under its own name it
keeps its order. The agent reads the reason and records again, so the roadmap never holds
a sprint it cannot show.

**BR-r2** — The testable list is never silently empty. Either it names what a person can
try, or it is empty together with an explicit statement that nothing is testable, which
the pane shows in words. An empty list without that statement is refused, and so is that
statement beside a non-empty list.

**BR-r3** — Recording is an upsert by name: a sprint recorded under a name that exists
replaces it whole, under a new name it is added. Each recording restamps the time.

### What the person sees

**BR-r4** — The pane lists the sprints in order, each as a bordered card: its state, its
objective, what is testable at its end, and its tickets, each with number, title,
description and a colour for its status. The person can narrow the view to one state.

**BR-r5** — A sprint shows its progress, the number of its tickets whose status is done
over the number of its tickets. A ticket is done when its status is the tracker's done
column: the one `board.flow.done` names, else the last column; no status name is written
into the mod. Progress is counted from the statuses the agent recorded, nothing else. The
colour of a status follows the columns too: the done column in the success colour,
`Unknown` in the error colour, the columns after the first and before the done column in
the warning colour, the others dim.

**BR-r6** — A sprint shows when it was last resolved from its source. A sprint the agent
has not recorded in the current session is marked as possibly stale, since the board may
have moved since. "This session" is the session id of the host, so a sprint recorded
under another session id is possibly stale, also after a reload of the same process.

**BR-r7** — The person may remove a sprint they no longer want on the roadmap, from the
pane; it is gone, its number of order free for another.

### Where it lives

**BR-r8** — The roadmap belongs to the machine and to the project root it was recorded
in; nothing is written in the repository, and a session in another project never sees it.
Writes go through one queue, so sprints recorded at the same moment are all kept. Two
processes writing the same project at the same instant are not protected.

**BR-r9** — A sprint stored in an older shape, with parts missing, still shows what it
has and says what it lacks, rather than failing to draw.

**BR-r10** — A sprint whose state disagrees with its tickets is not refused; it carries a
visible mark. A done sprint with tickets not done reads "state done, N ticket(s) not
done"; a planned sprint whose tickets are all done reads "state planned, all N ticket(s)
done". The state is the agent's word, the tickets are its record; the person sees the
gap rather than the mod choosing between them.

**BR-r11** — The mod checks the form of the testable list (BR-r2), not its truth. It cannot
judge whether a line is really something a person can try; that stays with the agent and
the person who reads the card.

### What it is not

It is not the board and not a planner: it computes no plan, reads no ticket state (only the tracker's list of columns), and a
ticket status shown is the one the agent last recorded. The tracker holds the project's
state; the roadmap is a buffer of the agent's reading of it.
