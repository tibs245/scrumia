# Acceptance criteria — session mods

One scenario per rule in `business.md`. Each scenario must be able to fail.

Each criterion of a mod names the test of that plugin's `hooks/register.test.ts` that proves it (`plugins/scrumia-questions/` for the questions inbox, `plugins/scrumia-issues/` for the issues table); the tests that run on two surfaces run on the terminal and the desktop app.

## scrumia-questions

### AC-1 — A question is parked and numbered in order (`BR-q1, BR-q3`)

```gherkin
Given a question carrying every part of its shape
When the model parks it, then parks another
Then each is accepted and numbered one after the other
```

Test: parks a question and numbers them in order.

### AC-2 — A malformed question is refused with its reason and stores nothing (`BR-q1`)

```gherkin
Given a call with no suggested answers, an empty list, more than six, a question that is not text, no blocking mark, or a recommendation outside the suggested answers
When the model parks it
Then the call is refused with a reason naming the fault, and the inbox shows no question
```

Test: a malformed call is refused with its reason (six cases); six options are accepted, seven are refused.

### AC-3 — A blocking question says not to go ahead, one that can wait says to carry on (`BR-q2`)

```gherkin
Given a blocking question and one that can wait
When each is parked
Then the first answers that what depends on it must not go ahead, the second that work carries on
```

Test: a blocking question says not to go ahead, a non-blocking one says to carry on.

### AC-4 — `Other` is always offered and needs a note (`BR-q4`)

```gherkin
Given a question with suggested answers
When `Other` is picked with no note, then a note is typed, and the answers are sent
Then with no note nothing is sent and the next prompt carries nothing; with the note the answer `Other` and the note reach the model
```

Test: Other needs a note, and the note travels with it (terminal, desktop).

### AC-5 — `Additional notes` travel with the answer whichever choice is picked (`BR-q5`)

```gherkin
Given a suggested answer picked and a note typed
When the answers are sent
Then the answer and its note reach the model together; without a note, none is shown
```

Test: an answer with its notes reaches the model by the context, once (terminal, desktop); the recommended answer is sent as is when nothing else is touched (terminal, desktop).

### AC-6 — The recommended answer counts when nothing else is picked (`BR-q6`)

```gherkin
Given a question with a recommendation, and one without
When the person sends without touching either
Then the first is sent with its recommended answer; the second is not ready and is left waiting
```

Test: the recommended answer is sent as is when nothing else is touched (terminal, desktop); one button sends every ready answer and leaves the others (terminal, desktop).

### AC-7 — One action sends every ready answer of the view and leaves the others (`BR-q7`)

```gherkin
Given several questions, some ready, one not
When the person sends from the whole view, then from a view narrowed to the non-blocking ones
Then every ready answer of the view is sent, the answers outside the view and the ones not ready are left waiting, and the filter separates blocking from non-blocking
```

Test: one button sends every ready answer and leaves the others (terminal, desktop); the send button sends only the answers of the filtered view; the filter keeps blocking questions apart (terminal, desktop).

### AC-8 — A question can be removed (`BR-q8`)

```gherkin
Given a waiting question
When the person removes it
Then it no longer shows and its number is not reused
```

Test: Remove takes a question out (terminal, desktop).

### AC-9 — An answer reaches the model once, as context beside the prompt (`BR-q9`)

```gherkin
Given an answer sent
When the person submits two prompts in a row
Then the first carries the answer as context and its text is unchanged; the second carries nothing
```

Test: an answer with its notes reaches the model by the context, once (terminal, desktop); a prompt passes untouched while nothing is answered.

### AC-10 — The question texts reach the model labelled as its own (`BR-q9`)

```gherkin
Given an answer sent
When the next prompt goes through
Then the context says the question texts are the model's and the answers and notes the person's
```

Test: the texts of the questions reach the model labelled as its own.

### AC-11 — A prompt refused further down does not consume the answers (`BR-q10`)

```gherkin
Given an answer sent and a prompt refused below the mod
When the person submits a prompt, then another that is accepted, then a third
Then the answer rides the accepted prompt and is not sent again with the third
```

Test: a prompt refused further down does not consume the answers.

### AC-12 — A returned answer carries the linked ticket (`BR-q11`)

```gherkin
Given a question linked to a ticket, answered
When the answer returns
Then the context carries the question's number and the ticket beside the answer
```

Test: an answer with its notes reaches the model by the context, once (terminal, desktop).

### AC-13 — Questions belong to the project they were asked in (`BR-q12`)

```gherkin
Given a question asked in one project and answered
When a prompt is submitted from another project, then back in the first
Then the other project receives nothing and numbers its own questions from one; the first receives the answer
```

Test: questions belong to the project they were asked in.

### AC-14 — Parallel calls keep every question (`BR-q13`)

```gherkin
Given three questions parked at the same moment
When the calls resolve
Then three questions are numbered one to three and all show
```

Test: three parallel calls keep three questions.

### AC-15 — A question is dropped thirty days after its delivery (`BR-q14`)

```gherkin
Given a question asked, answered and delivered twenty days later, a second delivered fifteen days after that, and a third delivered sixteen days after the second
When each is delivered
Then the first is still stored when thirty-five days have passed since it was asked and fifteen since its delivery, and is gone once thirty-one days have passed since its delivery, the recent ones kept
```

Test: a question is dropped thirty days after its delivery, not after it was asked.

### AC-16 — A question stored without its blocking mark still shows as one that can wait (`BR-q15`)

```gherkin
Given a question stored in the older shape
When the pane is opened and narrowed to the blocking ones
Then it shows in the whole view and not in the blocking one
```

Test: a question stored without isBlocking still draws, as one that can wait.

### AC-17 — The band offers to open the inbox while a question waits (`BR-q16`)

```gherkin
Given a blocking question waiting
When the band above the prompt draws
Then it offers to open the inbox and counts one blocking question
```

Test: the band offers to open the inbox when a question waits.

### AC-18 — The inbox is tried by a person on a terminal session and a desktop session

```gherkin
Given the plugin installed in a terminal session and in a desktop-app session
When a person parks, answers and sends a question in each, pane included
Then the result is recorded where the work is tracked, with the surface it was tried on
```

Test: none automated. What a mocked surface cannot prove is whether the pane draws and answers on the real surface; a person tries it and records the result.

### AC-60 — A single-line field refuses a line break or a control character (`BR-q17`)

```gherkin
Given a call whose question, linked ticket, one suggested answer or recommendation holds a line break, or whose question or ticket holds a control character
When the model parks it
Then the call is refused with a reason naming the field, and nothing is stored
```

Test: a single-line field refuses a line break or a control character, naming the field (question, ticket, an options entry, recommended alone, a control character in the question, a unicode line separator in the ticket).

### AC-61 — A context or an impact may span several lines (`BR-q17`)

```gherkin
Given a call whose context and impact hold line breaks
When the model parks it
Then it is accepted and numbered
```

Test: a multi-line context and impact are accepted.

### AC-62 — A prompt the person did not type leaves the answers where they are (`BR-q9`)

```gherkin
Given an answer sent
When a prompt arrives from a task notification, a peer, a coordinator, a scheduled trigger, an unclassified origin, another plugin, or with no origin, then the person types a prompt
Then the first carries nothing and the answer is not marked delivered; the typed one carries it
```

Test: the answers wait for a prompt the person typed (each untyped origin leaves them where they are; a prompt with no origin leaves them where they are).

### AC-63 — A prompt typed by the person, through the prompt box, the bridge, or a plugin submitting as the person, takes the answers (`BR-q9, BR-q12`)

```gherkin
Given an answer sent, in a project that two sessions share
When a prompt typed by the person reaches the session that reads the project first
Then that prompt carries the answer, once
```

Test: the answers wait for a prompt the person typed (composer, bridge and a plugin submitting as the person take them).

### AC-64 — A delivered question stored without its delivery time is purged from the day it was asked (`BR-q14`)

```gherkin
Given a delivered question stored without a delivery time, asked forty days ago, and another asked five days ago
When the next delivery happens
Then the first is dropped and the second kept
```

Test: a delivered question stored without deliveredAt is purged from the day it was asked.

## scrumia-issues

### AC-19 — A ticket is recorded with its status and what remains (`BR-i1`)

```gherkin
Given a ticket not yet in the table
When the agent records it with its status and what remains
Then it is accepted and counted as open
```

Test: recording > records a ticket with its status and what remains.

### AC-20 — Recording a ticket again updates its row in place (`BR-i1`)

```gherkin
Given a ticket recorded as `Backlog`
When the agent records it again as `Done` with nothing remaining
Then the table still holds one row for it and no ticket is open
```

Test: recording > updates a ticket in place instead of listing it twice.

### AC-21 — A malformed call is refused with its reason and stores nothing (`BR-i3`)

```gherkin
Given a call whose number is text, fractional, below one or missing, whose taken-into-account mark is missing or not a boolean, whose status is outside the columns or missing, whose remaining text is empty or missing, or whose title is not text
When the agent records it
Then the call is refused with a reason naming the fault, and the pane lists no such ticket
```

Test: recording > a malformed call is refused with its reason and stores nothing (eleven cases).

### AC-22 — The status is matched whatever its case, and `Unknown` is always accepted (`BR-i3, BR-i5`)

```gherkin
Given the default columns
When the agent records a ticket as `in review`, then another as `Unknown`
Then the first is stored as `In review`, the second as `Unknown`
```

Test: recording > the status is matched whatever its case, and kept as the board spells it; recording > Unknown is always accepted.

### AC-23 — Parallel writes lose nothing (`BR-i4`)

```gherkin
Given three tickets recorded at the same moment, and a prompt naming two more at the same moment as two other records
When the calls resolve
Then every ticket is in the table, numbered in the answers one after another
```

Test: recording > three parallel calls keep three tickets; recording > parallel calls and a prompt naming tickets lose nothing.

### AC-24 — The statuses are the tracker's columns, and others are refused with the list (`BR-i5`)

```gherkin
Given a tracker configured with the columns `Todo`, `Doing`, `Shipped`
When the session starts, then the agent records a ticket as `Doing`, then as `In progress`
Then the first is accepted, the second is refused with `Todo, Doing, Shipped, Unknown`; the tool's schema lists the same
```

Test: the status vocabulary comes from the tracker > the columns of the tracker are read at session start and others are refused with the list; the status vocabulary comes from the tracker > the tool description tells the agent to read the board and the schema lists the columns.

### AC-25 — The last column closes a ticket (`BR-i5`)

```gherkin
Given a tracker whose columns end with `Shipped`
When the agent records a ticket as `Shipped` with nothing remaining
Then no ticket is counted open
```

Test: the status vocabulary comes from the tracker > the last column counts as done.

### AC-26 — The columns are read on the first call when no session start came first (`BR-i5`)

```gherkin
Given a session in which the start hook did not run before the tool is called
When the agent records a ticket with a column of the tracker
Then it is accepted
```

Test: the status vocabulary comes from the tracker > the status is read lazily when no session start came first.

### AC-27 — With no readable tracker, the defaults serve and the pane says so (`BR-i6`)

```gherkin
Given a tracker command that fails
When the session starts, the agent records a ticket as `Ready for dev`, then as `Elsewhere`, and the pane is opened
Then the first is accepted, the second is refused with the six default columns and `Unknown`, and the pane says the defaults are used and why
```

Test: the status vocabulary comes from the tracker > the six default columns serve when the tracker cannot be read, and the pane says so; the status vocabulary comes from the tracker > the pane says when it uses the tracker columns; the status vocabulary comes from the tracker > every way the tracker cannot be read serves the defaults and the pane says why (no tracker module, an absent one, no columns, columns that are not text, settings that are not JSON, a command missing).

### AC-28 — The agent is told to report the status it read on the board, and the mod reads none (`BR-i7`)

```gherkin
Given the tool registered at session start
When the registration is read
Then its description tells the agent to read the board first (naming `scrumia-board` only as an example, when it is available) and says the tool does not check it; the mod runs no command but the two reading the columns
```

Test: the status vocabulary comes from the tracker > the tool description tells the agent to read the board and the schema lists the columns; the status vocabulary comes from the tracker > the columns of the tracker are read at session start and others are refused with the list (the two commands it ran).

### AC-29 — A typed prompt that names new tickets asks the agent to record them, once (`BR-i2, BR-i8`)

```gherkin
Given a prompt typed by the person naming tickets 3528 and 12, then another naming 3528 and 99
When each goes through
Then the first carries a reminder naming the first two, the second names only 99
```

Test: what is detected, and from where > a prompt the person typed that names new tickets asks the agent to record them, once.

### AC-30 — A prompt without a ticket number passes untouched (`BR-i8`)

```gherkin
Given a typed prompt naming no ticket
When it goes through
Then its context is unchanged
```

Test: what is detected, and from where > a prompt without a ticket number passes untouched.

### AC-31 — A reminder in a prompt refused below is carried again (`BR-i8`)

```gherkin
Given a typed prompt naming a ticket and refused further down, then another
When each goes through
Then the second carries the reminder
```

Test: what is detected, and from where > a reminder carried by a prompt refused below is carried again.

### AC-32 — A ticket the agent already recorded is not reminded (`BR-i8`)

```gherkin
Given a ticket recorded by the agent
When the person types a prompt naming it
Then no reminder is added
```

Test: what is detected, and from where > a ticket recorded by the agent is not reminded.

### AC-33 — A prompt the person did not type is not read (`BR-i9`)

```gherkin
Given a prompt naming a ticket and arriving as a task notification, a peer message, a coordinator hand-off, a scheduled trigger, an unclassified prompt, a prompt submitted by another plugin, or with no origin
When it goes through
Then the ticket is not in the table and no reminder is added
```

Test: what is detected, and from where > a prompt the person did not type is not read (seven cases).

### AC-34 — The person typing through the bridge, or a plugin submitting as the person, is read (`BR-i9`)

```gherkin
Given a prompt naming a ticket, arriving from the Remote Control bridge, and another submitted by a plugin as the person
When each goes through
Then both tickets are in the table
```

Test: what is detected, and from where > the Remote Control bridge is the person typing; what is detected, and from where > a prompt the person did not type is not read > a plugin that submits as the person is read.

### AC-35 — The mod's own note is not read, pasted or quoted (`BR-i10, BR-i11`)

```gherkin
Given the mod's reminder naming ticket 77 pasted into a typed prompt beside ticket 78, and the same reminder quoted by the agent beside ticket 78
When the prompt goes through and the turn completes
Then ticket 78 is in the table, ticket 77 is not
```

Test: what is detected, and from where > the note the mod injected is not read, even pasted into a prompt; what is detected, and from where > what the agent says > the mod's own note quoted by the agent is not read.

### AC-36 — Code, a colour of zeros, a link fragment and an entity are not tickets (`BR-i10`)

```gherkin
Given a typed prompt carrying a colour of zeros, an inline code span with a number, a link fragment, an entity, a fenced block with a number, and one real ticket
When it goes through
Then only the real ticket is in the table
```

Test: what is detected, and from where > numbers in code, a colour of zeros, a url fragment and an entity are not tickets.

### AC-37 — A ticket the agent names alone reaches the table (`BR-i11`)

```gherkin
Given a turn that completed with a final text naming ticket 321
When the turn completes
Then ticket 321 is in the table as not assessed
```

Test: what is detected, and from where > what the agent says > a ticket the agent names alone reaches the table, as not assessed.

### AC-38 — The next typed prompt carries the reminder for it, once (`BR-i8, BR-i11`)

```gherkin
Given a ticket named only by the agent
When the person types two prompts in a row
Then the first carries the reminder, the second nothing
```

Test: what is detected, and from where > what the agent says > the next prompt the person types asks the agent to record it, once.

### AC-39 — An interrupted or failed turn is not read (`BR-i11`)

```gherkin
Given a turn ended by interruption naming ticket 400, and one that failed naming ticket 401
When they complete
Then neither ticket is in the table
```

Test: what is detected, and from where > what the agent says > a turn that was interrupted or failed is not read.

### AC-40 — A ticket already known is not listed twice (`BR-i1, BR-i11`)

```gherkin
Given a ticket recorded by the agent, then named again in a final text
When the turn completes and the agent records it again
Then the table holds one row
```

Test: what is detected, and from where > what the agent says > a ticket already known is not listed twice.

### AC-41 — The same session id brings the same table back, as after a resume (`BR-i12`)

```gherkin
Given a ticket recorded in a session, the session answering to another id in which another ticket is recorded, then to the first id again
When the pane is opened and a ticket is recorded
Then the first ticket is there and not the other one, and the new one makes two
```

Test: the scope of the session > the table of a session is back when the same session id returns, as after a resume.

### AC-42 — After a `/clear` the table starts empty and the old one is kept under its id (`BR-i12`)

```gherkin
Given a ticket recorded, then the session answering to a new id as after a `/clear`
When the pane is opened, a ticket is recorded, then the first id returns
Then the new table holds only the new ticket; the first holds only the first
```

Test: the scope of the session > after a /clear the id changes and the table starts empty, the old one kept under its id.

### AC-43 — One session never sees the tickets of another (`BR-i12`)

```gherkin
Given a ticket named by a typed prompt in one session
When another session opens its pane, then its person names the same ticket
Then the other pane lists nothing, and the other session is reminded of the ticket as a new one
```

Test: the scope of the session > a different session never sees the tickets of another.

### AC-44 — Only the thirty most recent sessions are kept (`BR-i13`)

```gherkin
Given thirty sessions each having recorded a ticket at a later moment than the one before, the first of them recording again after all the others, then two more sessions
When each of the first four and the last two is opened again
Then the second and the third, the least recently touched, are gone; the first, whose last touch is recent, the fourth and the last two are there
```

Test: the scope of the session > only the thirty most recent sessions are kept, the least recently touched going first.

### AC-45 — The pane lists what was named and what was recorded, on both surfaces (`BR-i14`)

```gherkin
Given a ticket named by a prompt and another recorded by the agent with its remaining text
When the pane is drawn on the terminal and on the desktop app
Then both rows show, the recorded one with its remaining text
```

Test: the pane > lists a mentioned ticket and a recorded one (terminal, desktop).

### AC-46 — The pane says so when nothing was named (`BR-i14`)

```gherkin
Given a session where no ticket was named
When the pane is drawn
Then it says no ticket was mentioned
```

Test: the pane > says so when no ticket was mentioned.

### AC-47 — The issues table is tried by a person on a terminal session and a desktop session

```gherkin
Given the plugin installed in a terminal session and in a desktop-app session
When a person names tickets, lets the agent record some, runs `/issues`, then resumes and `/clear`s the session
Then the result is recorded where the work is tracked, with the surface it was tried on and what the table held after the resume and after the `/clear`
```

Test: none automated. What a mocked session cannot prove is whether the pane draws on the real surface, whether the engine really hands a resumed session its own id back, and whether the final text of a real turn reaches the detector; a person tries it and records the result.

### AC-65 — A number with a leading zero is not a ticket (`BR-i10`)

```gherkin
Given a typed prompt naming a hash followed by `0012`, `007` and `000`, beside a hash followed by `12`
When it goes through
Then only ticket 12 is in the table
```

Test: what is detected, and from where > a number with a leading zero is not a ticket.

### AC-66 — A failed read of the tracker is not kept for the process (`BR-i5, BR-i6`)

```gherkin
Given a tracker whose first read fails and whose second read gives the columns `Todo` and `Shipped`
When the session starts, then the agent records a ticket as `Todo`, then another as `Backlog`, and the pane is opened
Then the tool registered at start lists the default columns, the first record is accepted, the second is refused with `Todo, Shipped, Unknown`, the pane names the tracker's columns, and no further read follows
```

Test: the status vocabulary comes from the tracker > a failed read is not remembered: the next call reads again and the columns change.

### AC-67 — The done column is the one the tracker names, else the last (`BR-i5`)

```gherkin
Given a tracker with the columns `Todo`, `Shipped`, `Archived` whose `board.flow.done` names `Shipped`, and another that declares only `board.options` keys `Todo`, `Doing`, `Shipped`
When a ticket is recorded in `Shipped`, then one in `Archived` on the first tracker, and an unknown status is refused on the second
Then the first ticket is not open and the second is; the second tracker's columns are its option keys, with `Unknown`, and its last one closes a ticket
```

Test: the status vocabulary comes from the tracker > board.flow.done names the done column, whatever its place; the status vocabulary comes from the tracker > without columns, the keys of board.options are the columns and the last one is done.

### AC-68 — Open tickets are listed first, each group by number, under the summary line (`BR-i14`)

```gherkin
Given tickets 30 and 1 recorded as `Done`, 5 as `In progress` and 20 as `Backlog`, in that order
When the pane is drawn
Then the rows read 5, 20, 1, 30 and the summary line says four mentioned, four taken into account, two open
```

Test: the pane > open tickets come first, each group by number, under the summary line.

## scrumia-roadmap

Each criterion names the test of `plugins/scrumia-roadmap/hooks/register.test.ts` that proves it; the tests that run on two surfaces run on the terminal and the desktop app.

### AC-48 — A sprint is recorded, then updated in place by its name (`BR-r3`)

```gherkin
Given a sprint recorded, then recorded again under the same name with another objective and state, and a second sprint under another name
When the roadmap is read
Then the first sprint shows its latest objective only, and both sprints show
```

Test: records a sprint, then updates it in place by name.

### AC-49 — A malformed sprint is refused with its reason and stores nothing (`BR-r1`)

```gherkin
Given a call with no name, an order that is not an integer, a source of unknown kind or empty reference, an empty objective, no testable list, an unknown state, no tickets, a ticket without description, or a ticket number twice
When the agent records it
Then the call is refused with a reason naming the fault, and the roadmap shows no sprint
```

Test: a malformed call is refused with its reason and stores nothing (fourteen cases, including those of AC-50 and a ticket number of zero or below).

### AC-50 — The testable list is never silently empty (`BR-r2`)

```gherkin
Given an empty testable list without the statement that nothing is testable, then that statement beside a non-empty list, then the statement beside an empty list
When each is recorded
Then the first two are refused, and the third is recorded and the pane says in words that nothing is testable
```

Test: a malformed call is refused with its reason and stores nothing (empty testable list, nothingTestable with a list); a sprint with nothing testable says so in words.

### AC-51 — Each sprint is a card with its objective, what is testable, its tickets and its progress, on both surfaces (`BR-r4, BR-r5`)

```gherkin
Given a sprint of two tickets, one done, with a testable item
When the pane is opened on a terminal surface and on a desktop surface
Then the card shows its source, its objective, the testable item, each ticket with its title, its description and its status drawn, and the progress one over two
```

Test: the pane draws sprints as cards with tickets and progress (terminal, desktop).

### AC-52 — The sprints are drawn in their order (`BR-r4`)

```gherkin
Given two sprints recorded in the reverse of their order
When the pane is opened
Then the one of lower order comes first
```

Test: the sprints are drawn in their order, not in the order they were recorded.

### AC-53 — The view can be narrowed to one state (`BR-r4`)

```gherkin
Given a planned sprint and a running one
When the person narrows the view to running, then to planned, then back to all
Then each view shows only the sprints of that state, and all shows both
```

Test: the state filter narrows the view (terminal, desktop).

### AC-54 — A sprint shows when it was resolved and is marked possibly stale if not recorded in this session (`BR-r3, BR-r6`)

```gherkin
Given a sprint stored by an earlier session and a sprint recorded now
When the pane is opened
Then both show a resolved time, the first carries the mark possibly stale and the second does not, and recording the first again removes its mark; a sprint recorded under one session id carries the mark once the session id is another
```

Test: a sprint stored by an earlier session is marked possibly stale, one recorded now is not; a sprint recorded under another session id is possibly stale; the stamp is the clock at recording.

### AC-55 — Two project roots do not see each other's sprints (`BR-r8`)

```gherkin
Given a sprint recorded in one project and another in a second project
When the pane is opened in the second
Then it shows only its own sprint
```

Test: two project roots do not see each other.

### AC-56 — Parallel recordings keep every sprint (`BR-r8`)

```gherkin
Given three sprints recorded at the same moment
When the calls resolve
Then all three show
```

Test: three parallel calls keep three sprints.

### AC-57 — A sprint stored in an older shape still draws (`BR-r9`)

```gherkin
Given a sprint stored with only a name, an order and an objective
When the pane is opened
Then it draws, saying its source and its testable list are not recorded
```

Test: a sprint stored in an older shape still draws.

### AC-58 — A sprint can be removed from the pane (`BR-r7`)

```gherkin
Given a recorded sprint
When the person presses Remove on its card
Then it no longer shows
```

Test: Remove takes a sprint out (terminal, desktop).

### AC-69 — A ticket's status is a column of the tracker, and the done column closes it (`BR-r1, BR-r5`)

```gherkin
Given a tracker with the columns `Todo`, `Doing`, `Shipped`, and another whose `board.flow.done` names `Shipped` among `Todo`, `Shipped`, `Archived`
When a sprint with one ticket in `Shipped` is recorded and the pane opened, then one with a ticket in `Done` is recorded on the first tracker, and one with the tickets `Shipped` and `Archived` on the second
Then the first shows one over one done, the `Done` status is refused with `Todo, Doing, Shipped, Unknown`, `Unknown` in any case is accepted, and the second shows one over two done; the tool registered at start lists the columns
```

Test: the statuses are the columns of the tracker > a tracker whose last column is Shipped counts it as done; the done column named by board.flow.done wins over the last; a status outside the columns is refused with the list; Unknown is allowed; the tool registered at start lists the columns.

### AC-70 — An unreadable tracker gives the default columns, said in the pane, and is read again (`BR-r1, BR-r5`)

```gherkin
Given a tracker that cannot be read, then one whose first read fails and whose second gives the columns `Todo`, `Doing`, `Shipped`
When tickets are recorded as `Done` and as `Shipped`, and the pane is opened
Then on the first the six default columns serve, `Shipped` is refused with them and `Unknown`, the pane says default columns are in use, and one over two is done; on the second a status of the default columns is accepted at first and refused with the tracker's columns once it can be read
```

Test: the statuses are the columns of the tracker > an unreadable tracker falls back to the default columns, says so, and reads again next time; a failed first read is not kept.

### AC-71 — The order is unique in a project (`BR-r1`)

```gherkin
Given a sprint recorded at order 1
When another name is recorded at order 1, then the first name again at order 1
Then the second call is refused with a reason naming the first sprint and nothing is stored, and the third replaces the first
```

Test: two sprints with the same order: the second is refused and the first stays.

### AC-72 — A state that disagrees with the tickets is marked, not refused, on both surfaces (`BR-r10`)

```gherkin
Given a done sprint with three tickets of which one is done, a planned sprint whose two tickets are done, and a running sprint
When they are recorded and the pane is opened on a terminal surface and on a desktop surface
Then every call is accepted, the first card reads "state done, 2 ticket(s) not done", the second "state planned, all 2 ticket(s) done", and the running sprint carries no such mark
```

Test: a state that disagrees with the tickets is marked, not refused (terminal, desktop).

### AC-59 — The roadmap is tried by a person on a terminal session and a desktop session

```gherkin
Given the plugin installed in a terminal session and in a desktop-app session
When the agent records a sprint in each and the person opens the pane
Then the result is recorded where the work is tracked, with the surface it was tried on
```

Test: none automated. What a mocked surface cannot prove is whether the pane draws and stays readable on the real surface; a person tries it and records the result.
