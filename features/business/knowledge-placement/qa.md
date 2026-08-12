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
Then the destination is the project — its configuration, a directive, or a rules section
  — and the tree names which of the three and why
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

### AC-5 — Something that survives the handover is refused for memory

```gherkin
Given a fact that whoever clones this repository would need in order to work on it
When it is offered to agent memory
Then the tree refuses that destination, names the one that fits, and states the handover
  test as the reason
```

### AC-6 — Something nobody else can use is accepted in memory

```gherkin
Given a fact about how this machine is configured, useless to anyone cloning the
  repository
When the tree runs
Then agent memory is the destination, and the tree does not route it to the project or to
  a module in order to avoid using memory at all
```

A tree that never chooses memory has replaced one wrong default with another.

### AC-7 — A project prerequisite is not memory

```gherkin
Given a prerequisite stated as belonging to the project rather than to the machine
When the tree runs
Then the destination is the project, because a clone needs it too, and the tree says so
  rather than accepting the framing it was given
```

### AC-8 — An existing memory entry is re-placed on demand

```gherkin
Given an entry already sitting in agent memory
When it is submitted to the tree
Then the tree returns either the destination it should have had, with the handover test
  cited, or the statement that memory is correct for it — and it does not require the
  entry to be re-explained to do so
```

## Debates

### AC-9 — An existing issue is found before a new one is created

```gherkin
Given a debate about something an issue already covers, and that issue is closed
When the tree routes it
Then the closed issue is found and proposed, because the search covers every state, and
  no new issue is created
```

### AC-10 — A new debate issue is excluded from what is counted as work

```gherkin
Given no existing issue matching a debate
When a new one is created for it
Then it carries the label `features/business/github-tracking/` declares for that purpose,
  and the status and next-step readings do not count it as a ticket awaiting refinement
```

This criterion fails in the way that matters if the label is created and nothing subtracts
it: a label nothing queries is documentation, not a filter.

### AC-11 — The board is never the search surface

```gherkin
Given a debate whose subject was settled and whose issue has left the board
When the tree searches
Then the search runs over issues in every state and not over the board, and the settled
  issue is reachable
```

## Refusals and degradation

### AC-12 — One fact, one destination

```gherkin
Given a fact already placed in a module
When the same fact is submitted again
Then the tree reports it as already placed, names where, and proposes a pointer rather
  than a second copy
```

### AC-13 — The reminder does not block

```gherkin
Given an agent writing something to its own memory mid-run
When the write happens
Then it completes, the run is not interrupted, and the question about placement arrives
  afterwards
```

### AC-14 — An absent destination is named, not improvised

```gherkin
Given a composition with no module in the tracker slot
When the tree routes a debate
Then it names the gap and the module that would fill it, creates nothing, and does not
  write the debate into a file in the repository
```
