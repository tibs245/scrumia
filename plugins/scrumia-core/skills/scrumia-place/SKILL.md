---
name: scrumia-place
description: Routes something learned during a run to exactly one destination — a module, this project, a feature, a ticket, the change itself, or agent memory. Use it when a run turns up something worth keeping, when an agent has just written to its own memory, or to re-place entries already sitting in a memory directory.
---

# Place what was learned

A run turns up something nobody had written down: a call that truncates silently, a
convention this repository follows, a decision taken in passing. This skill takes that
thing and returns **one** destination for it.

One fact goes to one place. Two copies is worse than none — a fact written twice is a fact
that will be corrected once. Where it seems to belong in two, one of them is the authority
and the other points at it; a pointer is not a second placement.

The rules are
[`features/business/knowledge-placement/`](https://github.com/tibs245/scrumia/blob/main/features/business/knowledge-placement/business.md)'s.
This skill applies them and defines none of them.

## What you can hand it

| Input | What it does |
|---|---|
| a fact, in prose | routes it |
| a path to a memory entry | reads the entry itself and routes it — you do not re-explain it |
| a memory directory | routes every entry in it, one at a time |

It runs **after** the fact. An agent writing to its own memory is not intercepted, refused
or redirected mid-action; the question arrives next, and one of its answers is that the
write was right.

## Step 1 — Say the fact in one sentence

Write what was learned as a rule someone who was not there could act on. "Reads of the
board without a filter truncate at thirty" is a fact; "I ran the board and got thirty rows"
is a run.

**State what must be true, not who does it** — and then check the sentence against the one
question that separates questions 2 and 3: *would anything in the product have to change
for this to hold?* "We open pull requests against the specs branch here" and "the ticket
skill opens a pull request against the specs branch" are one fact in two costumes, and only
the second admits that a tool must change. Answer that question about the fact and write the
answer into the sentence before Step 3 reads it.

This step is where one fact becomes one destination. Skip it and the tree still returns one
answer per sentence — which is not the same thing, and is the duplication it exists to
prevent arriving by a side door.

If the sentence needs an *and*, or carries two claims of different reach, or states a rule
*and* objects to something still in flight, it is two facts. Split them and route each
separately — one memory entry routinely holds a general lesson, a detail true only of this
repository, and a live disagreement, and those have three different destinations.

## Step 2 — Ask whether it is already placed

Look for the fact where it could already be, before choosing anywhere to put it. Five
places, and for the first four the composition says where they sit — never assume a layout:

- the modules this project runs, skills and references included;
- the project's own rules — its `CLAUDE.md` and its configuration;
- the specs root, as the specs contract in `CLAUDE.md` names it;
- the tracker, for anything that reads like a debate;
- the agent memory directories themselves. A fact already sitting in one is placed, rightly
  or wrongly, and re-placing it is Step 3's job — writing a second copy of it is not.
  **The composition declares none of these.** A project has at least two scopes — the one it
  commits, and the harness's own outside the repository — so this is the one place you cover
  what you were given rather than what a layout says, and the answer names which directories
  those were. A sweep that quietly covered half of them reports success either way.

Grep the tokens that survive someone else's phrasing — a command name, a flag, a number —
rather than your own sentence, which is the one wording certain not to be there:

```bash
grep -rni "<token>" <those paths>
```

If it is there, **it is placed**: report where, and stop. What may still be added is a
pointer from wherever you were about to write it — one line naming the authority, never a
second statement of the rule. "I will restate it somewhere closer to hand" is exactly the
duplication this step exists to catch.

Where what you are routing is itself the second copy — an entry that already exists
somewhere with more authority — stopping is not the whole answer. The authority stands and
the entry is the duplicate: **drop it** where a reader standing at the duplicate would
reach the authority anyway, and leave **a pointer** only where they would not. Leaving both
statements is the two-copies state this step exists to end, and a sweep meets it constantly.

There is a third outcome besides *placed* and *not placed*, and it is the one worth saying
out loud: **the fact is not true here** — a file that was never renamed, a flag that does
not exist, a rule the thing it describes has since dropped. Say so and stop; a wrong fact
has no destination, and every branch below will happily give it one. Where it is true only
in a narrower form, that narrower form is the fact: state it and route that.

**This step runs on one fact, not on one file.** A file Step 1 split into three gets three
searches, and can come back placed, untrue and routable at once. Stopping on the file
because its first claim is stale is how a live lesson gets thrown away with a dead one.

## Step 3 — The tree

Ask these in order. The first *yes* is the destination, and nothing after it is asked.

| # | Ask | Yes → |
|---|---|---|
| 1 | Does it hold for every project running one of the modules this composition runs? | that module |
| 2 | Does it change what the product does or must do? | a feature |
| 3 | Does it govern how work is done here, for anyone working on this repository? | the project |
| 4 | Is it unresolved — a disagreement, a thought, an event — something still open that someone will have to settle? | a ticket |
| 5 | Once it is corrected, would nobody need to be told? | the change itself |
| 6 | none of the above | Step 4 decides |

Questions 1 to 3 ask **what the fact is a rule about** — a module's behaviour, the
product's, or the way work is done here — and only in that order. Questions 4 and 5 catch
what is not a rule at all.

**The product is asked about before the repository, and that ordering is load-bearing.**
Almost everything true of the product is also true of the repository holding it, so a
project question asked first swallows every product behaviour there is. It bites hardest on
a repository that ships its own tooling — where a rule about the tool and a convention of
the house are the same sentence — and that is the case the order is built for, not an edge
of it.

Questions 1 and 2 both fit more often than they look, and one word separates them:
**observed, or decided.**

- Question 1 takes what a module **already does** — a behaviour you found out about. It is
  reported where it is read, and the module is the destination because the behaviour is
  already true for every project running it.
- Question 2 takes what the product **should do** — a behaviour somebody chose. A decision
  is specified before it is built, so it goes to a feature even when the thing that will
  eventually carry it is a module.

Sending a decision straight into a module's prose skips the specification and writes it
where a project would find the rule but not the reason. That is the specs-before-code order
inverted, and a repository whose product *is* its modules meets this collision on nearly
every fact rather than at its edges — which is exactly why the test is *observed or
decided* and not *which artefact will hold it*.

**1 — that module.** Name it: the module that publishes the thing the fact is about. A rule
about how a published name behaves belongs to whoever publishes it, not to the project that
tripped over it.

Where the cause sits in one module and the rule has to be acted on in another, the
destination is **the module whose skill would carry the sentence** — where it is read at
the moment it applies. A rule filed against its cause and never read where it bites is
placed wrong, however accurately it names the cause. Where two modules both read it when it
applies, it goes to whichever reads it **first**; the later one takes a pointer if it needs
one.

Where no module owns it at all, do not create one for it —
[`module-authoring`](https://github.com/tibs245/scrumia/blob/main/features/business/module-authoring/business.md)
refuses a module for a single rule. It still has to live where a reader will find it, so it
takes question 3's branch, and the answer says plainly that its reach is wider than the
place now holding it. That is the honest form of the refusal, and it is not a reason to
widen a module until one is warranted.

**2 — a feature.** Name the feature that owns the behaviour, or state that none exists yet.
That statement is an answer, not a failure.

**Which feature owns a rule is the specs module's question, not this one's.** Ask it the way
the composition exposes it rather than picking by subject matter — two features whose names
both sound right is the normal case, and the module that holds the specs is the only thing
that knows which of them the rule is read from. Where the composition offers no such answer,
name the closest feature **and say you are choosing rather than reading** — a guess reported
as a guess is usable; a guess reported as a placement is not.

Do not pick the file inside it: which file receives what is the specs module's
([`feature-format`](https://github.com/tibs245/scrumia/blob/main/features/business/feature-format/business.md)),
and this skill stops at the feature.

**3 — the project.** This branch is how work is done here, not what the product does — a
convention, a house rule, a prerequisite. Name which of the shapes
[`local-extension`](https://github.com/tibs245/scrumia/blob/main/features/business/local-extension/business.md)
lists it should take, and why that one, in a line. That list is stated there and nowhere
else, this one included — read it rather than a copy of it. Naming the shape is the answer;
which register a directive joins is settled where it is written, not here. Where none of
them fits — a module in the composition may own project-level material of its own shape —
say which is closest **and that none fits**. That is a finding for `local-extension`, whose
list it is; it is not a shape to force the fact into. **A prerequisite
lands in this branch, not in memory**: "you need X to work on this" is framed as a note
about a machine and is needed by whoever clones the repository. What is on *your* machine
and absent from the project's prerequisites is question 6's.

**4 — a ticket.** A ticket is the one place this composition already keeps *why*, which is
what an unresolved thing needs. Look for the issue that already covers it before creating
one — something settled is more often a closed issue than a new one. What a new issue
carries, and how it is labelled, is
[`github-tracking`](https://github.com/tibs245/scrumia/blob/main/features/business/github-tracking/business.md)'s
and the tracker module's.

A fact that is simply **not a rule** is not unresolved. Nothing about it is open, and nobody
has to settle it — it takes questions 5 and 6 like anything else. Reading "not a rule yet"
as this branch's admission test would send every machine-local fact to the tracker, which is
the one destination that turns a private note into project state.

**5 — the change itself.** The question is whether anything survives the fix. A broken
link, a stale sentence, a wrong default: correct it, with the reason in the change, and
nothing is left to state anywhere. Where someone would still need to be told once the fix
is in, the fix is not the placement — one of the branches above is, and the correction
travels with it.

Nothing above this branch asked "act now, or file it?". Acting is a destination like the
others, reached by the same tree on the same information, and it is not a question put
before them.

## Step 4 — The handover test

**Would this survive being handed to someone else, usefully?**

If whoever clones this repository would need it, agent memory is the wrong place — memory
does not travel with the clone, and a fact in it is invisible to every other agent, every
other machine, and the person who will hit the same wall. Reject that placement and state
this test as the reason. Then name the destination, and where it comes from depends on how
you got here:

- **Step 3 answered** — a question fired, and you are here because the fact was offered to
  memory and you ran the tree over it anyway. Name what Step 3 gave.
- **Step 3 gave nothing**, so the fact reached here through question 6. A fact that falls
  through every question and still survives the handover means questions 1 to 3 were read
  too narrowly, not that it has no home: ask them again with its reach in hand. Where none
  of them fires even then, it is the project's, and the answer says plainly that its reach
  is wider than the place now holding it — the same move an unowned module rule gets.

Neither path ends without a destination. "Nowhere" is not one of this skill's answers.

What the test sends to memory is genuinely nobody else's: how this machine is set up, what
this person prefers, which reflex to reach for first. **That is a real answer.** When the test
says memory, say memory and stop — offering a module or the project *as well*, for a fact
nobody else can use, is the same failure pointing the other way, and a tree that never
chooses memory has replaced one wrong default with another.

Memory holds behaviour, procedure, and this machine's prerequisites. It holds no
documentation, no business rule, and no module rule.

### The path decides nothing

The test turns on whether the thing travels, never on the directory it sits in. A project
that commits its agent-memory directory has a directory whose contents reach every clone,
so nothing in it is exempt: it is project material sitting under a memory-shaped path.

- An entry whose content a colleague would need is routed out of it like any other,
  whatever it sits under.
- An entry nobody else could use is memory on its content. That its directory is versioned
  is then a fact about the directory, worth raising on its own; it is not a reason to
  re-place the entry.

A rule that could be satisfied by moving a file into a directory with the right name is not
this rule.

## What an answer says

- the destination, named — which module, which of the project's shapes, which feature,
  which issue — or the statement that it does not exist yet;
- the question that decided it, in one line;
- for a placement rejected out of memory, the handover test as the reason;
- nothing else. One destination, and no runner-up.

Routing is the whole job: whatever owns the destination does the writing, by its own rules.
Naming a destination that does not exist yet, and creating nothing, is a complete answer.

## Sweeping a memory directory

Route each entry on its own — Step 1 first, since an entry is where two facts are most
likely to be wearing one filename. A file that only lists the others is an index: it is
navigation, not an entry, and it is routed nowhere — what it is owed is a check that its
lines still point at something. Report a list: entry, destination, deciding question, and
**whether the entry was a placement failure** — an entry that should never have been in
memory is a defect, and a sweep that only lists new addresses reads as a reshuffle.
Expect most of an untouched directory to leave. The default destination costs nothing to
write and everything to retrieve, which is the whole reason this tree exists.

Report the sweep to whoever asked for it. It describes what that directory held on the day
it ran, so writing it into a file leaves behind something that will still be claiming it
next month; what is durable is the procedure, and the procedure is this file.
