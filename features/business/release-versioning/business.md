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

Not the content of a project's own specs, which the module never owns, and not the
module's internals, which it may reshape freely.

| Bump | Promise | What the project owes |
|---|---|---|
| **patch** | nothing on the published surface moved | nothing — take it without reading |
| **minor** | something is available that was not; nothing the project already does stops working | nothing — read the changelog to learn what you gained |
| **major** | something the project depends on changed shape | act; the changelog names the change and its replacement |

A project that takes a patch or a minor and then breaks has found a **defect in the
module**, not a consequence it should have anticipated. That is the whole content of the
promise, and it is what makes the number worth reading.

### Below `1.0.0`, the mapping shifts by one

Semver promises nothing below `1.0.0`, and every module ships there today. Rather than
pretend otherwise, or let a prose fix ship `1.0.0`:

| The mapping says | Below `1.0.0` it is |
|---|---|
| major | minor |
| minor | patch |
| patch | patch |

The consequence is honest and worth naming: below `1.0.0` a consumer cannot tell a
feature from a fix by the number, and reads the changelog for anything finer than
"something moved". Reaching `1.0.0` lifts the shift, per module, and is what buys the
finer reading.

## Which bump a change earns

The bump is **derived from the commit**, not chosen. Two things decide it: the type,
and whether the scope names a module.

- **The type's level** is `docs/adr/0017-version-bump-and-commit-signal.md`'s table,
  which is the vocabulary's one definition. It is cited here and enumerated nowhere:
  a second copy is a second definition, and the ADR is where a type is admitted.
- **`!` on the type, or a `BREAKING CHANGE:` footer, overrides the level and bumps a
  major.** Available on every type, not only the two the standard bumps from.
- **A bump happens only where the scope names a module.** A commit scoped to an app, a
  feature or the repository moves no number, whatever its type — there is no number to
  move. This is why a change to a spec bumps nothing: a feature carries no version.

**A commit naming several modules bumps every module it names, at the same level, and no
other.** That is the rule the mandatory scope exists to make possible; the alternative —
inferring which modules changed from the paths a commit touched — is what once turned one
fix into a bump across twelve modules, eight of which changed only their own version line.

## What a module owes to be upgradable, and for how long

A module may rename or remove anything it does not publish. What it publishes, it must
keep reading in the old spelling for a window counted **in releases**:

| Release | What the module does |
|---|---|
| **N** | renames. Both spellings work, the new one is preferred, and the changelog carries the old one under `Deprecated` **naming the version that removes it** |
| **N+1** | both spellings still work |
| **N+2** or later | the old spelling may be removed, under `Removed`, in a commit carrying the breaking signal |

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
