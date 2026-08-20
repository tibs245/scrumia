# Local tracking — technical notes

How the rules stated in `business.md` are carried out. Documents what the
code cannot say for itself: which plumbing, which primitive, which
shape — not why the rule exists.

## Where the path lives

`$CONFIG_LOCAL` is the directory the settings cascade's layer 3 reads
from, set by `--config` or by the project-local default
(`.scrumia/config.local.yaml` beside `.scrumia/config.yaml`). The
store's path is one key in that file:

```yaml
tracker:
  store: /Users/<you>/.local/share/scrumia/tracker
```

`tracker.store` is the **only** key this feature writes; the file
itself is shared with whatever else is per-machine for the project's
own modules, and the cascade already treats it correctly. A path that
does not exist when the tool needs it is reported as the absence
`business.md`'s behaviour axis names — never silently fixed by the
tool.

The key is a single scalar, not a richer structure. A richer one
(index location, lock directory, journal directory) would invite
splitting the store across paths, and the design's whole point is that
there is **one** place to address. Where a follow-on wants more, it
adds a key under `tracker` without moving the store's root.

## Deriving the store key from the main root

The key under `$CONFIG_LOCAL/tracker/` is a function of the project's
**main-root path**, derived through two git calls and one filesystem
operation.

```
store_key = sha256(canonical(main_root)).hex()[:16]
```

| Step | Plumbing | What it returns | Why it is the call that holds |
|---|---|---|---|
| 1 | `git rev-parse --git-common-dir` | the shared `.git`, from any directory in the working tree | this is the call that holds across linked worktrees: every worktree resolves to the same `.git`, so its parent is the same main root |
| 2 | `cd "$(dirname "$git_common_dir")" && pwd -P` | the canonical absolute path of the main checkout's directory | `--show-toplevel` is wrong here — it answers the worktree's root from a linked worktree, and a different answer per worktree is what the derivation explicitly forbids |
| 3 | `sha256 … | head -c16` | a 16-hex-char key under `$CONFIG_LOCAL/tracker/` | shorter than a full hash, long enough that two repositories on one machine are vanishingly unlikely to collide, and short enough to be portable across filesystems with different path-length limits |

The hash is a stable transformation, not a security primitive. A
collision is a re-key event the operator arbitrates, **not** an
attempt to address: a key `9f4a3b…` under two projects on the same
machine is reported as the collision `business.md`'s cost list names,
and the operator renames one rather than the tool guessing which one
wins.

**`$SCRUMIA_TRACKER_KEY` overrides the derivation.** A run that needs
to address a different store — pointing a test at a fixture, addressing
a deliberately shared store from two related projects — sets the
variable and reads that key instead. It is the override the path in
`config.local.yaml` does not provide, because changing the path would
also change the derivation's output, and the override exists to break
that coupling without editing the file. An environment already set
wins over the derivation, the same way a key in
`config.local.yaml` wins over both an absent file and an absent
variable.

## The lock primitive

Every write acquires an exclusive lock before it touches a record.
The lock is **atomic `mkdir`** of a sentinel directory:

```sh
lock_dir="$STORE/locks/$ticket_id.lock"
while ! mkdir "$lock_dir" 2>/dev/null; do
  # back off; bounded retries
done
trap 'rmdir "$lock_dir"' EXIT
```

Three properties of this primitive are load-bearing:

- **It is portable across every filesystem a project is likely to
  find on its home machine**, including NFS-mounted directories where
  POSIX `flock` does not hold, and container filesystems where
  `O_EXCL` semantics vary by host. `mkdir` is the lowest common
  denominator the project can defend.
- **It is self-cleaning under crash.** A process that dies holding
  the lock leaves a directory behind; the next writer whose `mkdir`
  fails after a small retry budget **detects** the stale lock (its
  mtime is older than a budget the next parameter states, and an
  operator-flag `--stale-lock=T` parameterises it). The detection is
  explicit, the failure is named, and the recovery is the operator's
  choice rather than a silent rename.
- **Its scope is per-record.** A ticket's lock is its own; the
  index's lock is its own; they do not contend for one global
  semaphore. The store's writes parallelise exactly to the degree the
  records they target allow, and the only contention a reader pays is
  for the record they are looking at.

**Rejected:** `flock(2)` on a single fd — does not hold across NFS,
adds a dependency on POSIX locks being honoured by the target
filesystem. **Rejected:** an `O_EXCL` lockfile — same NFS caveat,
plus a window between the file's creation and the first byte being
written where the lock says "held" but the file holds nothing.
`mkdir` collapses both: the sentinel **is** the lock, atomically.

## What the lock decides for the ticket-file record

The lock's presence is what makes the log inside the ticket file
(the sibling sub-issue's "log: one place, one kind of entry")
legitimate. The chain is exact:

1. The writer holds `locks/<ticket_id>.lock` for the duration of the
   read-modify-write.
2. Inside the hold, the writer reads the ticket file, appends one
   event, writes the file back atomically.
3. No second writer can interleave; the second writer's `mkdir`
   fails until the first releases.
4. The result is **atomic append** as a property of the lock, not as
   a property of the filesystem.

Without the lock, the same chain is **read-modify-write with a
window** in which a concurrent writer renames their copy back on top
of the first's, and the first's appended lines vanish. That is the
lost update `business.md` names as the defect the store refuses.

## The id allocator's seat-belt

The sibling sub-issue on the ticket-file record will mint ticket ids
via `open(O_CREAT|O_EXCL)` of `$STORE/id.highwater`. The file holds
a single 64-bit integer; every mint reads, increments, writes.
**The high-water mark is the one scalar nothing can derive from the
files** — and it is the one place the lock this feature mandates is
taken for the whole allocator, not per-ticket. That is the store's
full answer to ADR-0008's *no consistency constraint*: every other
datum in the store is reconstructible from the ticket files; this
one is the seed nothing else carries.

The lock that protects the high-water mark is a **store-wide lock**,
distinct from the per-ticket locks the rest of the store takes. A
mint holds `locks/id.lock` for the duration of the
read-increment-write. The window is small (microseconds on a local
filesystem) and the contention it pays is the cost of "the one
scalar nothing can derive" — the only place the store serialises
work that otherwise runs in parallel.

## Reading the lock's hold for the discipline it enforces

A reader does **not** take the write lock to read. It opens the
ticket file, reads what is there, releases. The store's discipline is
that a write is atomic against another write; a read that races a
write either reads the old version or the new one, with the kernel's
own per-file consistency — never an interleaving. The index
(sibling sub-issue) is the cache that absorbs the read latency, and
its own rebuild (its "direction of truth") is what restores
consistency if it ever drifts, not a reader taking a lock it does not
need.

## One-machine, one-filesystem as a precondition, not a constraint

The lock, the high-water mark allocator, and the atomic append all
require:

- a single host kernel;
- a single filesystem, with the system's atomic-`mkdir` semantics
  honoured (POSIX-compliant local filesystems qualify; NFSv3 with
  no `mkdir` semantics does not);
- a single user identity, since the lock directory's permissions are
  per-user.

A multi-host or multi-filesystem store would require a distributed
lock and a consensus algorithm; this feature does not provide them,
and the cost list in `business.md` is what a reader who needs them
hits. The store is a single-object-on-a-single-machine, by
construction, and an extension that needed otherwise would be a
different feature.

## What the operator's setup step looks like

The first time a project runs on a new machine, the operator
establishes the store once:

```sh
mkdir -p "$(scrumia-extends --print-tracker-key)"
```

`scrumia-extends --print-tracker-key` prints the key without reading
it, so the operator's first run produces the path on stdout, the
`mkdir` creates it, and the project's record points at it without
further ceremony. The tool never creates the path itself — the
creation is an explicit operator action, naming what it does.

A machine that already holds a store from a previous run prints the
same key, and the operator decides whether to attach, share, or
start clean. The decision is theirs because the tool's role is to
**name the absence**, not to **resolve it**.
