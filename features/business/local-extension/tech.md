# Local extension — how resolution finds the three locations

`business.md` states which locations exist and what a conflict is.
`features/business/modular-composition/`'s `tech.md` states the pipeline this sits inside —
discover, keep what the project runs, collect, order. This file states the one step that
pipeline delegates here: **turning a declaration into a directory**, and what the tool says
when it cannot.

## Where each source is looked for

One pass, three tiers, every root tagged with the tier it came from. No tier replaces
another, and no tier is searched only when another came up empty — a fallback would make
the answer depend on what is missing.

| Source in the key | Looked for at | When the tier is empty |
|---|---|---|
| `<owner>/<repo>` | every `…/bin` entry of `$PATH` whose parent holds `.claude-plugin/plugin.json` | no harness is running |
| `shared` | `$SCRUMIA_SHARED_DIR/<module>/` | the variable is unset — the ordinary state of a fresh clone |
| `local` | `<the configuration's own directory>/modules/<module>/`, i.e. `.scrumia/modules/` | the project ships no module of its own |

Each tier takes one `<module>/` directory per entry and looks no deeper. A tree walked to
find modules would adopt one by having it copied somewhere, which is the opposite of a
composition that declares what it runs.

**`$SCRUMIA_MODULE_DIR` overrides the first tier only**, replacing the PATH scan with a
directory of checkouts. It exists because CI and this repository run with no harness, and
it keeps the meaning it already had: what it yields is credited to the marketplace tier,
because that is what it stands in for. It says nothing about `shared` or `local`, which
have directories of their own.

**The local tier is derived from the configuration's directory, not from the working
directory.** Pointing `$SCRUMIA_CONFIG` at another project's configuration moves the local
modules with it, which is the only reading under which the two cannot disagree.

## `.scrumia/.env.local`

`KEY=value` per line; blank lines and anything without a `=` are skipped, which is what
makes a `#` comment a comment. Surrounding quotes are dropped because people write them
out of habit; nothing else about the value is interpreted, and nothing is expanded —
anything more is a shell, and reading a machine's file as a shell is how a configuration
executes. One variable is read today, `SCRUMIA_SHARED_DIR`.

A variable already set in the environment wins over the file. That ordering is what lets a
single run be pointed at another checkout without editing machine state, and it is why
tests and CI need no fixture file.

The file is loaded by whatever resolves a declaration to a location. A reader that only
repeats the declarations as written resolves nothing, so it needs nothing — which is why
`compose-status.sh` does not load it, and why that is not the asymmetry BR-6 warns about.

## Binding a declaration to a root

A declaration matches a discovered root when the names agree **and** the tier is the one
its source names:

| Key | Matches |
|---|---|
| `<owner>/<repo>:<name>` | a marketplace root named `<name>` whose manifest claims that repository |
| `shared:<name>` | a root named `<name>` in the shared tier |
| `local:<name>` | a root named `<name>` in the local tier |
| a bare name from the retired `extends:` list | a root named `<name>` in **any** tier — the name predates the grammar and carries no location |

The marketplace row is unchanged; the two below it are what this feature adds. Before it, a
`local:` key bound whichever marketplace module carried the name and the composition then
reported it as local — a location it did not come from, and the exact misreading BR-5
exists to prevent.

**Identity is the physical path.** Every root is resolved through its links before being
compared, so a checkout reached twice — linked into the project as well as sitting in the
shared directory — is one root and one module, reported at one location. That test is what
keeps the conflict rule off the ordinary promotion case, alongside the declaration itself:
a project running a checkout of a published module says `shared:`, and the published copy
is then a module it does not run rather than a rival for the same key.

**Where more than one tier still answers, the narrowest wins**, `local` before `shared`
before `marketplace`. Only a bare name from the retired list can reach that, since every
other key binds inside one tier. It is BR-5's shadow, written as a rank in the code rather
than inherited from the order the tiers happen to be discovered in: a label that nobody
stated moves the day someone reorders the discovery, and this one is reported to a human as
the reason a particular copy is running.

Four outcomes, one per declaration:

| Roots bound | State | Effect |
|---|---|---|
| exactly one | `resolved` | its directives render, its location is reported |
| none | `absent` | a declared absence — named, its location stated, nothing fails |
| several, each in a different tier, from a key naming none | `shadow` | the narrowest renders and is reported; the others are named beside it |
| several, otherwise | `conflict` | named on stderr with every root, binds nothing |

## What each surface reports, and what it exits

| Surface | Resolved | Absent | Shadow | Conflict |
|---|---|---|---|---|
| a register's table | its rows, in scope order | absent from the table | the narrowest module's rows, named on stderr | absent from the table, named on stderr |
| `--modules` | key, module, location, root | state `absent`, the location it would come from — none, where the key states no source the grammar admits | state `shadow`, the winning location, every root | state `conflict`, **no location**, every root |
| `--check` | — | — | named, not counted | an unmet dependency; exit non-zero |
| `--claims` | honoured where the file names it | the verdict below | as resolved — it binds | the verdict below |
| `compose-status.sh` | the declaration as written, under a heading saying so | the same — it resolves nothing, so it distinguishes none of these | | |

A conflict is credited with no location, where a resolved or shadowed declaration is
credited with the one it bound. Naming the narrowest of the roots it refused to pick
between would read as the one it picked, in the one column a reader scans first.

`--check` reports a shadow without counting it. That buys the person running it by hand,
not CI: `tools/validate.py` reads that stderr only on a non-zero exit, so a green run
discards it. It is still the right surface, because it is the one someone runs when asking
what is wrong.

Exit status carries meaning at two surfaces, and they fail on different things. A register
table is an answer whether it is long or short, and a conflict must not stop a skill that
never needed that module — which is why the conflict is loud everywhere and fatal only at
`--check`. `--claims` fails on nothing about the composition at all: what it can refuse is
a sentence written about it.

## Reconciling what `CLAUDE.md` claims

`--claims` takes a file — `CLAUDE.md` beside the configuration's own directory unless one
is named — and reconciles it against the states above. **One file per run**: an app's own
`CLAUDE.md` is a second claim in a second file, and the root run says nothing about it. One
row per declaration, and one verdict each:

| The declaration | The file | Verdict |
|---|---|---|
| `resolved` or `shadow` | names it, or does not | `honoured` / `unclaimed` — the capability is here either way |
| `absent` or `conflict` | does not name it | `not claimed` — the file says nothing it cannot back |
| `absent` or `conflict`, stating no source the grammar admits | names only the module | `unsourced` — the declaration states no origin for the file to repeat |
| `absent` or `conflict` | names its declaration key | `named as absent` — the file states the source, so the reader can see what is missing |
| `absent` or `conflict`, from a marketplace or from inside the project, or bound under another key | names only the module | `reachable` — what is missing is the module, not the sentence |
| `absent` or `conflict`, from a shared checkout | names only the module | `claimed` — a capability asserted to a reader who cannot reach it. Exit non-zero |

**Only the shared tier can produce the last row**, because it is the only source whose
absence belongs to the reader alone (BR-8). A marketplace declaration nothing answers means
the plugin is not installed or the session was not restarted, and one inside the project
means a directory missing from the repository — both are missing for the author too,
neither is corrected by editing a sentence, and `--modules` already names both.

**A module another declaration bound is present whatever this one did**, so it is
`reachable` too. That is the promotion arrangement seen from one key behind: a module moved
into the project while a `shared:` key still names it resolves under `local:`, the file's
claim is true, and a tool failing there would be demanding the author write `shared:` over
a module that ships in the repository — talking a project into the defect it exists to
catch. The stale key is `--modules`' finding, where both rows are visible at once.

**The match is on strings, never on the file's shape.** What shape the composition section
takes is `modular-composition`'s and changes without this tool being told; a reconciliation
that parsed a table would pass by accident the day the table moved. The declaration key is
what separates the middle rows because it is the one string carrying the module *and* its
source (BR-6) — so a file that names it has said where the capability would come from, in
the words the configuration uses, and a file that names only the bare module has not. A key
present anywhere in the file counts: which sentence it sits in is a human's judgement, and
a tool grading English is a tool inventing findings.

A declaration stating no source the grammar admits — one from the retired list, one with no
source at all, one whose source is a fourth thing — gets `unsourced`, and neither `named as
absent` nor `claimed` would be true of it. The configuration states no origin, so no wording
of the file could have repeated one, and keying the declaration by source is what makes it
answerable at all. That is the fix the shadow report and the grammar's own notice already
name. The test is the source rather than the key's shape: a key that is its own module name
is one way to state no origin, and `foo:x` is another.

A name matches at its edges, not as a substring, and the boundary alphabet treats a path as
one token: without that, a module named `tools` is found inside `tools/validate.py` and a
module named `acme` inside `acme-lint`, and the tool accuses a correct file of a claim it
never made. The remedy it prints then reads *add this to the file* — which would be a tool
talking a project into the exact defect it exists to catch.

It is vacuous on the machine that wrote the file, by construction — everything resolves
there — and it is the clone that gets the answer. That asymmetry is the point rather than a
weakness: AC-7 is a claim about a reader who is not the author.

A project with no such file claims nothing, which is reported and is not a failure. A file
the caller names is different: the caller asserted it is there, so one that is not, or one
that cannot be read, is an error. Read as empty it would clear every claim and exit clean,
which is the one answer a surface whose job is to fail must never give.

## Two sets, and why they are not one

Discovery yields every root; binding yields the roots the declarations chose. Most of the
tool reads the second. Three checks read a third — one root per module **name** — because
they ask about identity rather than about directives: which module opens a register, which
publishes a name, whether two modules opened the same one.

Read off the raw discovery, those three break the moment a checkout sits beside its
published copy — the promotion case — by reporting a register as opened twice, by the same
module, and failing `--check` on it. Read off the bound set alone, they would stop covering
every installed module, which is what makes `--check` a repository-wide gate here rather
than a per-project one. So the third set is discovery collapsed by name, preferring the
root a declaration bound.

`--modules` exists because "the composition is reported" had two candidate readers and only
one of them resolves anything. `compose-status.sh` prints the declarations as written; its
stdout is a versioned fixture, and giving it a resolved location would make a gated artefact
depend on which machine ran it. What it owes instead is BR-6's other half — its heading says
what it did, *the modules this project declares*, because a heading claiming they run
claims exactly what it did not check.

## The row shape a consumer may depend on

`--json` rows gain one field, `location`, alongside the `source` they already carry:
`source` is what the **key** says, `location` is what **resolution found**. They agree on
every resolved row today and are still two facts — a row that could carry a source with no
location is the declared absence, and one that could disagree is the defect the pair exists
to expose.

`--modules --json` emits one object per declaration: `key`, `module`, `source`, `scope`
(`project-wide` or an app's name), `state`, `location`, and `roots` — an array, because a
conflict has more than one and a consumer that read a single path would silently take the
first.

Neither shape is an `api-contract.md`, and that is a judgement rather than an oversight:
that file in this catalog is a contract **between apps**, and `plugins/` is not an app.
Today nothing outside `scrumia-core` parses either — `tools/validate.py` reads `--check`'s
exit status and its stderr, and every skill reads the rendered table. *Exit condition*: the
first consumer outside this module that parses `--json`, at which point the shape has a
holder and belongs in a file that says so.

## Constraints and debt

- **`bash` + `jq`, and the two YAML readers the machine may already have.** Inherited from
  the tool this lives in; the tiers add no dependency, because a directory listing and
  `pwd -P` are all resolution needs.
- **CI can only ever exercise `$SCRUMIA_MODULE_DIR`**, never the harness's PATH. That
  blind spot is `modular-composition`'s and unchanged: what this feature adds is that the
  other two tiers *are* exercisable in CI, since both are plain directories.
- **A conflict is detected between roots, never between two keys naming one root.** A
  project declaring both `shared:x` and `local:x` where the two are the same directory
  gets that module's directives twice in one table, and nothing reports it. The setup is a
  link plus two keys — which is close to the promotion arrangement this feature encourages,
  so it is reachable by accident and not only by construction. *Exit condition*: a
  duplicate check across declarations, before a composition is seen doing it.
- **A file that quotes its own configuration disarms `--claims` wholesale.** A key counts
  anywhere in the file, so a project documenting its composition by pasting the `modules:`
  block under the prose puts every declaration key in reach and every unbacked claim
  becomes `named as absent`. It is the one input shape that retires the check silently, and
  it is the price of refusing to read the file's structure — a rule about which region of
  the file a key must sit in is a rule about the file's shape, which is
  `modular-composition`'s and not this tool's to assume. *Exit condition*: a composition
  section the writer marks off, at which point the region is declared rather than guessed.
- **`--claims` reconciles the declarations, so a claim about a module the composition no
  longer declares is invisible to it.** That is the ordinary stale-`CLAUDE.md` failure, and
  it is `modular-composition`'s — the composing skill compares the file against the config,
  where this compares the file against what resolved. Both are needed and neither covers
  the other. *Exit condition*: a project found carrying a claim neither surface caught.
- **A module resolved `local` or `shared` cannot publish a command.** The harness puts
  only an enabled marketplace plugin's `bin/` on PATH, so a name published by a checkout is
  not runnable — while `--check` reports the dependency met, because it accepts a name
  published by any discovered module. That leniency was written for `$SCRUMIA_MODULE_DIR`,
  where no harness runs and PATH proves nothing; it now covers two tiers where a harness
  does run and PATH does prove something. Nothing in this repository publishes from either
  tier, so nothing regresses today — but it bounds a claim stated flatly above and in
  `module-authoring`'s BR-3: moving between locations is free for a module that ships data,
  and not yet for one that ships a command. *Exit condition*: `--check` distinguishing the
  tiers, and the promotion pass saying so.
