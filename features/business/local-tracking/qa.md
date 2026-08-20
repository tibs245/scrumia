# Acceptance criteria — Local tracking

One scenario per rule in `business.md`. Each scenario must be able to fail.

## Nominal

### AC-1 — The store lives outside the project, addressed from `.scrumia/config.local.yaml`

```gherkin
Given a project whose `.scrumia/config.yaml` carries the composition and `.scrumia/config.local.yaml` is gitignored
When the spec is read end-to-end
Then it states that no part of the tracker — ticket files, indexes, logs, locks, the high-water mark — is written inside the project's repository
And the resolution is named as `.scrumia/config.local.yaml`, layer 3 of the settings cascade already read by `scrumia-extends`
And no environment variable, no derivation from `$HOME`, and no derivation from the project's name is named as the resolution path
```

### AC-2 — One store addresses every linked worktree, anchored on the common git root

```gherkin
Given a repository opened as the main checkout and four linked worktrees pointing at it (`git worktree add …`)
When the store's address is derived from inside any of those five locations
Then all five derive the same path: `git rev-parse --git-common-dir` resolves to the shared `.git`, the parent of that is normalised to one main-root path, and the key under `$CONFIG_LOCAL/tracker/` is the same for all five
And the spec names `git rev-parse --git-common-dir` as the plumbing it anchors on, and names `--show-toplevel` as the one it must not
And given any one of those five worktrees writing a transition, when any other of the five reads, it sees the transition
And after `git worktree remove` on one of them, the remaining four still derive the same key and still see the same store
```

### AC-3 — An absent store is named, with an attach option; a second store is never silently initialised

```gherkin
Given a fresh machine where the project has never run, and no store exists under the key the derivation would produce
When the tool resolves the store's path
Then it reports the expected path and the operator step required, and the method does not proceed — it does not create an empty store at a default location
Given instead an existing store at a different path on the same machine, reachable from this user
When the tool resolves the store's path
Then it offers to attach the existing one — naming both paths, requiring the operator's affirmation — and on affirmation, the project's record points at the attached store
And in neither case is a second store initialised without the operator's knowledge
```

### AC-4 — The locking primitive is stated, the in-file log's permissibility rides on it, and the lost update is described as prevented

```gherkin
Given the spec stating the writing discipline
When it is read end-to-end
Then the lock primitive is named as atomic `mkdir` (an `O_EXCL` sentinel), `flock` and lockfile alternatives are listed only as rejected
And the rule says clearly: with the exclusive lock held, an in-file event log is permitted — the sibling sub-issue on the ticket-file record reads off this directly; without it, the in-file log is forbidden because read-modify-write forfeits atomic append
And the lost update — one writer reads, both rename atomically, the second wins the whole file including the first's appended lines — is described as **prevented**, never left unaddressed
And a write performed without the lock is named as a defect the store does not tolerate, with the consequence stated
```

### AC-5 — The one-machine, one-filesystem precondition is stated where the reader meets it, and the costs of the split are listed

```gherkin
Given a reader arriving at the spec's rules section
When it reads the locking and append rules
Then the one-machine, one-filesystem precondition is stated explicitly — the lock primitive, the atomic append, and `O_EXCL` creation all require it, and `flock` and lockfile alternatives are rejected on those grounds rather than on style
And the precondition is stated as a design precondition rather than as a discovered apology
And the spec's "Costs the design owns" section lists — in plain prose, not as a discovery: cloning gives no state, backing up the repo does not back up the store, moving or renaming the project orphans the store, deleting the repo does not delete the store, two projects of the same name on one machine collide and the resolution does not break the tie silently
```

### AC-6 — The ADR-0008 gate: this sub-issue answered `no lock`

```gherkin
Given the epic's three-mechanism gate on ADR-0008 — two writers, no lock, no consistency constraint
When the spec is read for which of the three it answered
Then it states that this sub-issue answered **no lock**: the lock primitive is named, mandatory on the write path, and the lost update is prevented
And the spec states explicitly that this sub-issue did **not** answer `two writers` — that mechanism is the next sub-issue's (the ticket-file record's "two populations, and the distinction the card gave for free") to defend — and did **not** answer `no consistency constraint` — that mechanism is the index sub-issue's to defend, plus the high-water mark in the ticket-file record sub-issue
And an unanswered mechanism at this sub-issue stops the epic here; the spec states the gating principle, not merely its own completion
```

## Boundary

### Out of scope

- The shapes of the records the store holds. The sibling sub-issues on
  the ticket-file record and on the index own the fields, the log
  format, and the index; the store's address is one parameter they
  read, not their subject.
- The behaviour of a write against the lock's timeout, contention,
  and crash recovery. The ticket-file record sub-issue's lock-holding
  window and the operator's experience when a writer dies holding
  the lock are its responsibility.
- Cross-machine state. The store is one machine, one filesystem, and
  any replication story is out of scope for this feature.
- The identity of an individual ticket, the allocator that mints it,
  and the high-water mark that makes an id never reused. The
  ticket-file record sub-issue owns them; the spec states here only
  that they live under the lock this feature mandates.
