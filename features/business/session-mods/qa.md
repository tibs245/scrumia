# Acceptance criteria — session mods

One scenario per rule in `business.md`. Each scenario must be able to fail.

Each criterion of the questions inbox names the test of `plugins/scrumia-questions/hooks/register.test.ts` that proves it; the tests that run on two surfaces run on the terminal and the desktop app.

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
Given a call with no suggested answers, an empty list, a question that is not text, no blocking mark, or a recommendation outside the suggested answers
When the model parks it
Then the call is refused with a reason naming the fault, and the inbox shows no question
```

Test: a malformed call is refused with its reason (five cases).

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

### AC-15 — A question delivered more than thirty days ago is dropped (`BR-q14`)

```gherkin
Given a question delivered, then another delivered twenty-nine days later, then a third thirty-one days after the first
When each is delivered
Then the first is still stored at twenty-nine days and is gone after thirty-one, the recent ones kept
```

Test: a question delivered more than thirty days ago is dropped, a recent one is kept.

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

## scrumia-issues

Placeholder, completed when the mod is specified.

## scrumia-roadmap

Placeholder, completed when the mod is specified.
