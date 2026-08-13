# Knowledge placement — business rules

## Value

For an agent that has just learned something during a run, and for whoever will need that
thing in three weeks without knowing it was ever learned. It brings one tree from "what
did I just find out" to exactly one destination, and a test that says when the answer is
"nowhere durable". It matters because the default destination costs nothing to write and
everything to retrieve: a fact in one agent's local memory is invisible to every other
agent, to every other machine, and to the human who will hit the same wall. Measurable,
and measured on this repository first: the count of entries currently in agent memory
that would have had a better destination, which is most of them.

## One fact, one destination

A fact is placed once. Two destinations for one fact is the duplication the tree exists
to prevent, and it is worse than no placement at all — a fact written twice is a fact
that will be corrected once.

Where the same fact seems to belong in two places, one of them is the authority and the
other should point at it. That is a pointer, not a second placement.

## The destinations

| What was learned | Where it goes |
|---|---|
| a rule that holds for every project running a given module | that module |
| a rule that holds for this project | the project — one of the shapes `local-extension` names |
| something that changes what the product does or must do | a feature |
| a discussion, a thought, an event, an unresolved disagreement | a ticket |
| something to correct now, small enough to carry its own justification | the change itself |
| everything else, and only after the test below says so | agent memory |

"Fix it now" is a destination in this table, not a question asked before it. Whether to
act or to file is the same decision as where to put the knowledge, taken once, with the
same information.

The three module-or-project destinations are `local-extension`'s to define. This feature
chooses between them; it does not describe them.

## The test that bounds agent memory

**Would this survive being handed to someone else, usefully?**

If a colleague cloning the repository would need it, it does not belong in agent memory —
memory does not travel with the clone. What remains is what is genuinely nobody else's:
how this machine is set up, what this person prefers, which reflexes to reach for first.

Agent memory holds behaviour, procedure, and this machine's prerequisites. It holds no
documentation, no business rule, and no module rule. An entry that fails the test is not a
category of memory: it is a placement that went wrong, and it is reported as one.

This is the rule the feature is most likely to be argued with on, so it is stated in the
form that can be checked rather than in the form that sounds right. A project prerequisite
is exactly the case where the two diverge — it feels like memory and it fails the test,
because whoever clones the project needs it too.

**The test turns on whether the thing travels, not on which directory it sits in.** A
memory directory a project versions travels with the clone, so nothing in it is exempt: it
is project material sitting under a memory-shaped path, and the tree routes it like any
other. Reading the rule as "files under this path are memory" would let the whole question
be settled by a directory name, which is how the failure got here.

## A discussion looks for an issue before it creates one

Most discussions are about something already written down. The tree searches before it
creates, and the search covers issues in every state — an unresolved thought is more often
about something that was closed than about something open. A search restricted to what is
currently on the board will miss exactly the cases the tree was built for.

Where nothing matching exists, a new issue is created, carrying a label that a query can
select on. That is what the label has to earn: an issue holding a discussion is not work
waiting to be refined, and counting it as such is how a backlog becomes unreadable, so
wherever the status and next-step readings meet one they subtract it. Whether they meet
one at all — where such an issue is filed, and which of a tracker's surfaces enumerate it
— is `github-tracking`'s, along with the label's spelling and its declaration.

## The tree reminds, it does not block

The tree runs after the fact. An agent writing to its memory is not intercepted, refused
or redirected mid-action; it is asked afterwards whether that was the right place, and it
answers with the same tree anyone else would use.

This is a deliberate limit and it has a known cost: a reminder can be ignored, and some
will be. The alternative — refusing the write — buys compliance by making a module able to
stop a session, which is a power no ScrumIA module holds today and which fails closed on
every project that installed it. The reminder is chosen on the balance of those two, not
because it works better.

## An empty destination is named, never improvised

Where a destination's capability is not present in the composition — no tracker to hold a
discussion, no specs module to hold a feature — the tree names the gap and the module that
would fill it, and it does not invent a substitute. Writing a discussion into a file
because no tracker exists creates state in the repository, which is the thing the composition
refuses everywhere else.

## Business rules

- **BR-1** — A fact is placed in exactly one destination. A second placement of the same
  fact is a finding, and a pointer is not a placement.
- **BR-2** — The destinations are a module, the project, a feature, a ticket, the change
  itself, and agent memory. The tree chooses between them; it defines none of them.
- **BR-3** — Deciding to act now is a destination in the tree, not a question preceding
  it.
- **BR-4** — Agent memory holds only what would not usefully survive being handed to
  someone else: behaviour, procedure, and this machine's prerequisites. It holds no
  documentation, no business rule and no module rule. The test turns on whether the thing
  travels, never on the directory it sits in — material a project versions is project
  material whatever its path.
- **BR-5** — An entry in agent memory that would have survived the handover is a
  placement failure and is reported as one, with the destination it should have had.
- **BR-6** — A discussion searches issues in every state before creating one, and never
  searches the board — the board carries what is in flight, not what has been settled.
- **BR-7** — A new issue holding a discussion carries a label the status and next-step
  readings exclude wherever they enumerate it. The label's spelling and declaration are
  `github-tracking`'s, as is whether such an issue is enumerated at all.
- **BR-8** — The tree runs after the write, as a reminder. It intercepts nothing and
  refuses nothing.
- **BR-9** — Where the destination's capability is absent from the composition, the tree
  names the gap — the module that would fill it, or the empty slot itself where no module
  can be named — and improvises no substitute. It never writes project state into the
  repository to compensate.

## Vocabulary

- **Placement** — the assignment of one learned fact to one destination. Not storage: the
  writing is done by whatever owns the destination.
- **The handover test** — whether a fact would usefully survive being handed to someone
  else with the repository. The single boundary of agent memory.
- **Discussion** — something unresolved that is not yet a rule and may never become one: a
  disagreement, a thought, an event worth remembering. Its destination is a ticket
  because a ticket is the one place ScrumIA already keeps *why*.
