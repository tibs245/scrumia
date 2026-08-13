# Acceptance criteria — Knowledge placement

One scenario per rule in `business.md`. Each scenario must be able to fail.

## Nominal

### AC-1 — A rule about a module's own behaviour lands in that module

```gherkin
Given something learned about how one of the composition's tools behaves — a call that
  silently truncates, an argument that must always be passed — that holds for every
  project running that module
When the tree is asked where it belongs
Then the destination is that module, not this project's configuration and not agent
  memory, and the tree names the module
```

This is the case the feature was built on: it fails today, and it fails in the direction
of agent memory every time.

### AC-2 — A rule that holds for this project alone lands in the project

```gherkin
Given a convention that applies to this repository and would not apply to another project
  running the same modules
When the tree is asked where it belongs
Then the destination is the project, the tree names which of the shapes
  `features/business/local-extension/` lists it should take, and says why that one
```

### AC-3 — Something that changes what the product does lands in a feature

```gherkin
Given a behaviour that was decided during a run and is not written in any specification
When the tree is asked where it belongs
Then the destination is a feature, and the tree names the feature or states that one does
  not exist yet, without deciding which file inside it receives the rule
```

### AC-4 — Acting now is chosen by the same tree

```gherkin
Given something small enough to correct immediately and whose justification fits in the
  change
When the tree runs
Then "make the change" is the destination it returns, arrived at through the same
  decision as every other destination, with no separate question having been asked first
```

## The boundary of agent memory

### AC-5 — Something that survives the handover is rejected for memory

```gherkin
Given a fact that whoever clones this repository would need in order to work on it
When it is offered to agent memory
Then the tree rejects that placement, names the destination that fits, and states the
  handover test as the reason
```

### AC-6 — Something nobody else can use is accepted in memory

```gherkin
Given a fact about how this machine is configured, useless to anyone cloning the
  repository
When the tree runs
Then agent memory is the destination, and no other is proposed — a run that returns the
  project or a module for this fact fails the criterion
```

A tree that never chooses memory has replaced one wrong default with another.

### AC-7 — A project prerequisite is not memory

```gherkin
Given a prerequisite stated as belonging to the project rather than to the machine
When the tree runs
Then the destination is the project, because a clone needs it too, and the tree says so
  rather than accepting the framing it was given
```

### AC-8 — A versioned memory directory is not exempt

```gherkin
Given a project that commits an agent-memory directory, so its contents reach every clone
When an entry in it is submitted to the tree
Then the handover test is applied to the entry's content and not to its path, and an entry
  a colleague would need is routed out of it like any other
```

A rule that could be satisfied by moving a file into a directory with the right name is
not the rule this feature states.

### AC-9 — An existing memory entry is re-placed on demand

```gherkin
Given an entry already sitting in agent memory
When it is submitted to the tree
Then the tree returns either the destination it should have had, with the handover test
  cited, or the statement that memory is correct for it — and it does not require the
  entry to be re-explained to do so
```

## Discussions

### AC-10 — An existing issue is found before a new one is created

```gherkin
Given a discussion about something an issue already covers, and that issue is closed
When the tree routes it
Then the closed issue is found and proposed, because the search covers every state, and
  no new issue is created
```

### AC-11 — A new discussion issue is excluded from what is counted as work

```gherkin
Given no existing issue matching a discussion
When a new one is created for it
Then it carries the label `features/business/github-tracking/` declares for that purpose
Given that issue placed where the readings would otherwise count it
When the status and next-step readings run
Then neither counts it as a ticket awaiting refinement
```

This criterion fails in the way that matters if the label is created and nothing subtracts
it: a label nothing queries is documentation, not a filter.

The second half needs its own Given because the first does not reach it. Where the tracker
files a discussion outside what the readings enumerate, the exclusion passes by absence
whatever the label says, and the criterion would be satisfied by a filter that does not
exist. `features/business/github-tracking/`'s AC-13 is the one that puts a labelled issue in
front of the readings and fails if nothing subtracts it; this criterion covers the label
being carried, and the exclusion holding once the issue is there to be counted. Where the
tracker files such an issue is that feature's to state, and this one does not restate it.

### AC-12 — The board is never the search surface

```gherkin
Given a discussion whose subject was settled and whose issue has left the board
When the tree searches
Then the search runs over issues in every state and not over the board, and the settled
  issue is reachable
```

## Refusals and degradation

### AC-13 — One fact, one destination

```gherkin
Given a fact already placed in a module
When the same fact is submitted again
Then the tree reports it as already placed, names where, and proposes a pointer rather
  than a second copy
```

### AC-14 — The reminder does not block

```gherkin
Given an agent writing something to its own memory mid-run
When the write happens
Then it completes, the run is not interrupted, and the question about placement arrives
  afterwards
```

### AC-15 — An absent destination is named, not improvised

```gherkin
Given a composition with no module in the tracker slot
When the tree routes a discussion
Then it names the gap and the module that would fill it, creates nothing, and does not
  write the discussion into a file in the repository
```
