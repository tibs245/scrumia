# Local tracking — business rules

```
Stratum:    business
Feature:    features/business/local-tracking/
Parent:     none — bootstrap case: this feature is the parent the epic produces
Angles on:  business, qa, tech, index, changelog
Angles off: ux (no screen, no control), archi (the EPIC touches no app —
            single-app store plus the trackers it replaces are the same
            shape, and the cross-app coordination that would justify
            archi.md is absent), api-contract (no consumer outside
            this feature parses it yet), legal (no personal data;
            ticket contents are the user's own), security (one-machine,
            one-filesystem precondition stated here and in tech.md),
            devx (no exposed surface for a consuming feature to read
            today; the store's contents are this feature's own)
```

## Value

For a project whose tracker slot is empty — no platform account, no remote,
no quota — and for whoever wants the method run end to end without one. It
brings the rules that let a tracker live entirely on disk: where its store
sits, how it is addressed from inside a linked worktree, the locking
primitive that serialises writes, and what the repository and the store
being separate objects costs the people who use them. It matters because
the alternative is that a project without a tracker cannot run the method,
and a project that finds itself needing one has no design to extend — only
the platform's shape, copied across. Measured on the duration a sprint's
five concurrent worktrees all address one store and one another, and on
the absence of any "X saw a stale view of Y" defect across a sprint that
follows these rules.

## Personas

- **The project lead**, running ScrumIA on a project whose tracker slot
  must remain empty — for privacy, for airgapping, for the whole project
  not depending on a network to be alive.
- **The agent**, executing a ticket in a linked worktree, writing into
  the shared store without knowing where the store was set up.
- **The operator**, setting up the store once per machine, then never
  touching it again.

## Use cases

- A sprint of up to five tickets running in parallel from five linked
  worktrees, every transition readable from every other worktree, no
  branch carrying a stale view.
- A clone of the project landing on a machine that has run the method
  before: the store is there, addressed automatically; the clone is
  one worktree among many addressing the same one.
- A clone landing on a machine that has not: the absence is named, the
  error names what was looked for, and the operator chooses how to
  attach — never an implicit initialisation that hides the question.
- A repository moved or renamed: the derivation rules state what an
  operator must do to keep the store reachable, and what they lose if
  they do not.
- A project re-establishing itself after losing its store: the absence
  is named the same way whether the store was deleted by hand, lost in
  a backup, or never followed the project to the new machine.

## The journey, as intent

1. **The operator sets up once per machine.** They pick the directory the
   store will live in and the identity the store answers to. This is the
   step the rest of the journey depends on, and it is taken once.
2. **A clone lands.** The agent running the method addresses the store
   without anyone having told it to. There is no configuration step on
   every clone; there is one store per machine, and the project finds it.
3. **A worktree opens.** The agent resolves the store from inside the
   worktree, using the git plumbing that does not lie to it about which
   root it is in.
4. **A transition is written.** The lock primitive serialises it against
   any other writer — across worktrees, across processes, across five
   simultaneous executions of the same step.
5. **The store is missing.** The error names what was looked for and
   where, and offers to attach an existing store or to fail — it does
   not silently invent a second one.

## The rules

### The store lives outside the project's repository

The store is a directory on the machine that runs the method. Nothing of
the tracker — no ticket file, no index, no log, no counter, no derived
artefact — is written inside the project tree. The rule is
[ADR-0008](../../../docs/adr/0008-state-lives-in-github.md)'s, applied
locally rather than waived for a project without a platform: a state
file in the tree has the same two writers, the same missing lock, the
same missing consistency constraint, whether the rest of the method is
running or not. The store is held outside the repository specifically
to keep one source of truth across the worktrees a sprint opens, and
the rule states that **it is held outside, not gitignored inside**.

Two consequences, both load-bearing:

- **A sprint of N concurrent worktrees addresses one store**, not N.
  Every read sees every write, and `git worktree remove` changes nothing
  about who addresses what.
- **No part of the tracker is restored from a clone**, by construction.
  Backing up the repository does not back up the store; backing up the
  store does not back up the repository. Cloning gives no state.

### Where the store lives

The store's path is recorded in `.scrumia/config.local.yaml`, the layer
3 of the settings cascade already read by `scrumia-extends` and already
gitignored in every project that uses it. The path is version-free in
the sense the cascade already requires: `.scrumia/config.yaml` carries
no path that names one machine; `.scrumia/config.local.yaml` carries a
path, is read on this machine, and is never committed.

The path is recorded there — and not derived from the project's name,
not derived from `HOME`, not derived from an environment variable — for
three reasons:

- **Portability.** A new machine takes the project and the store is set
  up on that machine, in one step, without restating the project's
  name or sharing a filesystem with anyone.
- **Visibility.** A reader looking at the project for the first time
  sees a file whose entire job is to be the per-machine configuration,
  and finds the store's path there. The same file already holds
  whatever else is per-machine for the project's own modules; the
  store joins it without widening the contract.
- **Override.** A specific store wins over a derived one, and the
  override is file-form, not environment-form — what one run did,
  the next run reads the same way, and CI does not need a fixture
  variable to point at the same path a developer would.

Where the file carries nothing, or carries a path the machine cannot
reach, the absence is reported as an absence: the store is **not**
silently initialised at a default location, because two stores at two
locations is the defect the file exists to prevent.

### What the store answers to

The store is keyed by the **normalised main-root path** of the
repository. From any directory — the main checkout, any linked
worktree, any directory inside either — `git rev-parse --git-common-dir`
resolves to the same `.git`, and the path that lives next to it (or
above it, for a bare checkout) is the project's main root. **It is the
main root, never `--show-toplevel`** — `--show-toplevel` answers the
worktree's root from a linked worktree, which is a different directory
and a different store every time.

| Caller's location | `git rev-parse --show-toplevel` | `git rev-parse --git-common-dir` (resolved) |
|---|---|---|
| main checkout | the main root | `…/.git` |
| a linked worktree | the worktree's root | `…/.git` (the same one) |
| a deep directory in either | that tree's root | `…/.git` (the same one) |

A project name is **not** the key, even though two projects with the
same name on one machine would collide if they were. A name that
derives identity from `<owner>/<repo>` carries the `<owner>` forward;
the resolution the store uses does not, by construction, and the cost
of that — two repos called `scrumia` on the same machine — is paid
where it is paid: by the second one choosing a distinct path under
`<id>`, not by the resolution inventing a tie-breaker it cannot
document.

The key is a directory on disk under `$CONFIG_LOCAL/tracker/`; its name
is the hash, or the stable transformation, of that normalised main-root
path. The exact transformation is `tech.md`'s — what the spec states
here is that the key **is a function of the main-root path alone**,
that the function is deterministic, and that any other input would
break the "one store, every worktree sees it" rule the next axis
exists to deliver.

### A worktree addresses the same store as the main checkout

Given the rule above, the resolution is implied: take `git-common-dir`,
normalise to its parent, derive the key, look under
`$CONFIG_LOCAL/tracker/<key>/`. A worktree addressing it is the **same
key** the main checkout derived. There is no second configuration the
worktree reads, no per-worktree branch of the rule, and no path the
worktree carries that the main checkout does not.

The failure this prevents is the one BMAD hits: a state file in the
working tree is present in the main checkout, absent from every linked
worktree (`git worktree add` copies tracked files only), and a module
that resolves the store next to the config finds a plausible, wrong
path and never fails. The combination — store outside the repo, key
derived from the common `.git` — is what removes both halves of that
trap.

### The lock, and what the lock decides for the ticket-file record

The store's exclusive write primitive is **atomic `mkdir`**. A writer
acquires the lock by `mkdir` of a sentinel directory under
`$STORE/locks/<name>` with `O_EXCL` (or its `mkdir` equivalent on every
target), holds the lock for the duration of its write, and releases by
removal. **No `flock`, no `O_EXCL` lockfile** — both hold locally and
neither holds on the filesystems a project is most likely to use, and
`mkdir` is portable across every filesystem the project's home is
likely to find, with no dependency added.

The lock is **mandatory for any writer**, mandatory on the write path,
and never optional. A transition written without the lock is a lost
update — a second writer reads the file, both rename atomically, the
second wins **the whole file** including the first's appended lines —
and the discipline the store holds to is the one that makes the
in-file event log the sibling sub-issue on the ticket-file record
opts into legitimate. **With** an exclusive lock, an in-file event
log is permitted; **without**, it is forbidden, because
read-modify-write forfeits atomic append.

That sibling sub-issue reads off this rule: the log lives inside the
ticket file, append-only under the lock, and the lock's presence is
what guarantees the append is atomic. The lost update it names is
**prevented** — accepted never, because accepting it makes the
ticket file the artefact that can be silently destroyed by a
concurrent writer, and the ticket file is the source of truth the
rest of the store reconstructs from.

### The one-machine, one-filesystem precondition

The lock primitive, the atomic append, and the `O_EXCL` creation the
id allocator (the high-water mark is the one scalar the sibling
sub-issue on the ticket-file record owns) relies on all hold on a
single machine,
single filesystem, and **none holds across NFS**, a network share, or
a container filesystem that mounts remote storage. This is not a
property the design degrades on — it is a precondition the design
states. The store is outside the repository; the store is already on
the machine that runs the method; the precondition is met by
construction, and stating it here means a reader designing on top of
this feature makes the assumption explicit rather than discovering it
under a failure they cannot debug.

### Behaviour when the store is absent

The store is expected at a specific path, and either it is there or it
is not. **The tool never silently initialises a second one.**

- **If the project is being executed for the first time on a machine**
  the tool finds the path it would have used, finds it empty, and
  says so — naming the path and the operator step required to create
  the store.
- **If an existing store is reachable somewhere on the machine but
  not at the path the derivation chose** the tool offers to attach it
  — once, interactively, with the existing path stated and the
  derivation's path stated. Guessing is excluded: the operator's
  affirmation is required, not assumed.
- **If the path is recorded but the directory at it does not exist**
  the tool reports the path, the expectation, and the empty directory,
  and waits. A second store at the default location is **not** what
  "the path is empty" means — what it means is that whatever lived
  there is no longer there, and the decision that follows belongs to
  the operator, not to the tool.

### Costs the design owns

The repository and the store are two separate objects, and that
carries a known list of costs — stated plainly, the way [ADR-0008](../../../docs/adr/0008-state-lives-in-github.md)
stated its own, so a reader who chose this feature has already read
the cost list before the design sold them on the value:

- **Cloning the project gives no state.** Intentional, and the reason
  the design exists; a clone that needs state is a clone that needs
  to attach an existing store, not a clone that ships one.
- **Backing up the project does not back up the store.** A repository's
  backup that has not been told the store exists is a backup of
  durable material — specs, ADRs, code — and a loss of state that
  cannot be rebuilt from the repo alone. The store has its own backup
  story, which is the operator's; this feature does not own it.
- **Moving or renaming the project orphans the store.** The key is
  derived from the project root; a project at a new path derives a
  different key, and the store at the old key is what the project
  used to address. The operator re-derives or re-attaches; the tool
  names the absence it now finds, the same way it would on a fresh
  machine.
- **Deleting the repository does not delete the store.** A directory
  that has been written to on this machine continues to live there.
  This is the cost of refusing to write any of it to the repository:
  a project that never had a remote had no remote to delete from, and
  the store the method ran on is left where the method put it.
- **Two projects of the same `<owner>/<repo>` on one machine share a
  key.** They collide at the derivation; the operator distinguishes
  them by installing them under distinct paths or by attaching an
  existing store to the second rather than letting the derivation
  pick. The collision is reported, not resolved silently.

## Vocabulary

- **Store** — the directory outside the repository that holds the
  tracker's records, its indexes, its locks, and its high-water mark.
  Not the tracker; the place the tracker writes to.
- **Key** — the deterministic function of the project's main-root
  path that names the store's directory under `$CONFIG_LOCAL/tracker/`.
  One per project, derived, never user-chosen, never carried in a
  versioned file.
- **Lock** — the atomic `mkdir` sentinel a writer holds for the
  duration of a write. It is the primitive that makes a concurrent
  append to the ticket file legitimate, and its absence is the
  primitive that makes the same append a lost update.
- **Attach** — the operator action of pointing the project at a store
  the derivation did not find. Interactive, one-shot, recorded; never
  inferred.
- **Common root** — what `git rev-parse --git-common-dir` resolves to
  from any directory in the working tree: the shared `.git`, the
  one store every linked worktree therefore derives the same key from.
