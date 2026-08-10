# Release versioning — business rules

## Value

For a project that has adopted a module and is deciding whether to take an update, and
for whoever ships that module. It brings a number that answers a question on its own —
whether this update asks anything of the project — plus a stated window before a renamed
thing disappears, and a stated moment at which the project is told. It matters because
the alternative is a project reading a diff to find out whether it is about to break, or
worse, finding out at runtime. Not instrumented today: nothing computes a version from
history, nothing checks a commit against this rule, and no measure counts modules that
shipped a change with their number frozen — the gap is read from the changelog and the
manifest, by hand.

## A version is a module's, and speaks about its published surface

The unit that bumps is **the module**, never the repository. A number promises that
*this* module changed; a project pinning one module is not moved by another's release.

What the number speaks about is the module's **published surface**:

- the config keys it reads under `settings.<slot>`
- the contract block it writes into `CLAUDE.md`
- the names of the skills and commands it ships
- the scripts other modules invoke by path
- **what its skills instruct an agent to do, and the artefacts they produce**

The last item is the one a module made of prose cannot leave out: here the deliverable *is*
the instruction, so rewriting what a skill tells an agent changes what a project gets as
surely as renaming a key does. A surface listing only names, keys and paths would let a
module rewrite every instruction it ships under a number promising nothing moved.

Not the content of a project's own specs, which the module never owns, and not the
module's internals, which it may reshape freely.

**A release is a version published to the marketplace** — a manifest whose number moved,
reachable by a project that updates. Not a commit and not a merge; several merges land
between two releases and none of them is one. The window below is counted in these.

| Bump | Promise | What the project owes |
|---|---|---|
| **patch** | nothing on the published surface moved | nothing — take it without reading |
| **minor** | something is available that was not, or something the project sees changed; nothing it already does stops working | nothing — read the changelog to learn what moved |
| **major** | something the project depends on changed shape | act; the changelog names the change and its replacement |

A project that takes a patch or a minor and then breaks has found a **defect in the
module**, not a consequence it should have anticipated. That is the whole content of the
promise, and it is what makes the number worth reading.

### Below `1.0.0`, the mapping shifts by one

Semver promises nothing below `1.0.0`, and every module ships there today. Rather than
pretend otherwise, or let a prose fix ship `1.0.0`:

| The mapping says | Below `1.0.0` the number moves | and the promise a project reads is |
|---|---|---|
| major | minor | major's: **act** |
| minor | patch | minor's: nothing owed, read what you gained |
| patch | patch | patch's: nothing owed |

**The obligation shifts with the number**, one level more severe and not uniformly — which
is why the third column is spelled out. Below `1.0.0`: a **minor** means act; a **patch**
means anything from a fix to a feature, so read the changelog. A project reading the table
unshifted would take a minor "without acting" and break on a rename that shipped inside it,
which is the failure the shift exists to prevent rather than a footnote to it.

The rest of the consequence is honest and worth naming: below `1.0.0` a consumer cannot
tell a feature from a fix by the number, and reads the changelog for anything finer than
"something moved" — at both levels, not only at one. Reaching `1.0.0` lifts the shift, per
module, and is what buys the finer reading.

## Which bump a change earns

The bump is **read off the commit**, not chosen. Two things decide it: the type, and
whether the scope names a module.

- **The type's level** is `docs/adr/0017-version-bump-and-commit-signal.md`'s table,
  which is the vocabulary's one definition. It is cited here and enumerated nowhere:
  a second copy is a second definition, and the ADR is where a type is admitted. The
  changelog category that table carries beside each level is a **proposal**, not a
  determination — the entry is a human's sentence to a consumer.
- **A bump happens only where the scope names a module.** A commit scoped to an app, a
  feature or the repository moves no number, whatever its type — there is no number to
  move. This is why a change to a spec bumps nothing: a feature carries no version.

Which leaves the type itself, which a human does choose — so the choice is constrained by
what the number has to mean:

- **The type is chosen against the published surface, not against the files touched.** A
  change that adds something a project can use is a feature; one that makes existing
  behaviour do what it was already meant to do is a fix; the types that move nothing a
  consumer reads or runs are for changes that do exactly that and no more. In a module made
  of prose, editing what a skill *instructs* is never one of those.
- **A change to the published surface that a project must act on owes the breaking
  signal**, whatever its type. Owed, not offered. Without this clause the level is a
  judgement made after the fact, and the authority the breaking signal carries below is
  authority over a signal nobody was told to send — which is why no commit in this
  repository's history has ever carried one.

**A commit naming several modules bumps every module it names, at the same level, and no
other.** That is the rule the mandatory scope exists to make possible; the alternative —
inferring which modules changed from the paths a commit touched — is what once turned one
fix into a bump across twelve modules, eight of which changed only their own version line.

## What a module owes to be upgradable, and for how long

A module may rename or remove anything it does not publish. What it publishes, it must
keep reading in the old spelling for a window counted **in releases**:

| Release | What the module does |
|---|---|
| **N** | renames. Both spellings work, the new one is preferred, and the changelog carries the old one under `Deprecated` **naming the release that removes it** — the release, not a version number, which at N is unknowable because the number is derived from commits not yet written |
| **N+1** | both spellings still work |
| **N+2** or later | the old spelling may be removed, under `Removed`, in a commit carrying the breaking signal |

Counted in **releases** — versions published to the marketplace — not in commits or merges.

Not "for a while", not "until the next major": two releases, counted. A rename and its
removal in the same release is a breaking change wearing a deprecation notice.

## When a project finds out

Two lags exist independently, and refreshing one does not refresh the other:

| Layer | What is stale | When the project is told |
|---|---|---|
| the marketplace clone behind the repository | the marketplace has not been updated | **at update.** Nothing polls, and nothing should — a project that never updates is never broken by a change it never took. What it reads at that moment is the module's changelog |
| the installed cache behind the clone | the plugin still runs from an older clone | **at install.** Installing replaces the cache, and the same changelog is the notice |

A third moment catches the project that skipped a release: **at first use**, a skill
reading a published name the module has since renamed **fails with a named message** —
the module, the version that removed the name, and its replacement — instead of falling
back to a default. Silent degradation is what makes the second layer invisible, and
`features/business/modular-composition/` already requires a named message for the
analogous absent-module case.

**"Never" is not an admissible answer for a major.** A breaking change a project can take
without ever being told is the failure this feature exists to prevent. Reading the
changelog is a step of taking an update, not a courtesy — which is what makes the
changelog's `Deprecated` and `Removed` entries load-bearing rather than decorative.

## Which assertion of breakage is authoritative

**The commit's breaking signal** — `!` on the type, or a `BREAKING CHANGE:` footer. The
version is derived from history, so the assertion that moves the number has to be the one
*in* history. A line typed into a changelog cannot be it.

A specs changelog's `Breaking:` field is not a competing authority. It describes a
different object — a rule under the specs root, which carries no version — and answers a
different reader. Where one change touches both a module and a spec, both are written and
must agree about the same change: a `Breaking: yes` with no breaking signal behind it, or
a breaking signal with no entry, is a defect to reconcile, not two claims to weigh.

## Nothing computes this yet

The rule is documented and **enforced by nothing**. No validator reads a commit message,
no script derives a number, and no release run exists. That is stated here rather than
discovered: until a gate exists, conformance is a habit, and a module's version is moved
by whoever edits its manifest.

Whether a module ever fills a `release` slot and performs the derivation is not this
feature's to decide, and is open.
