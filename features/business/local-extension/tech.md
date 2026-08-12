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
shared directory — is one root and one module, reported at one location. Where two tiers
reach one directory, the tier reported is the first of `marketplace`, `shared`, `local` to
reach it; the choice decides a label and never which module runs, which is the only thing
BR-7 refuses to let a search order decide.

That test is what keeps the conflict rule off the ordinary promotion case, alongside the
declaration itself: a project running a checkout of a published module says `shared:`, and
the published copy is then a module it does not run rather than a rival for the same key.

Three outcomes, one per declaration:

| Roots bound | State | Effect |
|---|---|---|
| exactly one | `resolved` | its directives render, its location is reported |
| none | `absent` | a declared absence — named, its location stated, nothing fails |
| two or more distinct | `conflict` | named on stderr with every root, binds nothing |

## What each surface reports, and what it exits

| Surface | Resolved | Absent | Conflict |
|---|---|---|---|
| a register's table | its rows, in scope order | absent from the table | absent from the table, named on stderr |
| `--modules` | key, module, location, root | the row, state `absent`, the location it would come from | the row, state `conflict`, every root |
| `--check` | — | — | an unmet dependency; exit non-zero |

Exit status still carries meaning only for `--check`. A register table is an answer whether
it is long or short, and a conflict must not stop a skill that never needed that module —
which is why the conflict is loud everywhere and fatal in exactly one place.

`--modules` exists because "the composition is reported" had two candidate readers and only
one of them resolves anything. `compose-status.sh` prints the declarations as written; its
stdout is a versioned fixture, and giving it a resolved location would make a gated artefact
depend on which machine ran it.

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

## Constraints and debt

- **`bash` + `jq`, and the two YAML readers the machine may already have.** Inherited from
  the tool this lives in; the tiers add no dependency, because a directory listing and
  `pwd -P` are all resolution needs.
- **CI can only ever exercise `$SCRUMIA_MODULE_DIR`**, never the harness's PATH. That
  blind spot is `modular-composition`'s and unchanged: what this feature adds is that the
  other two tiers *are* exercisable in CI, since both are plain directories.
- **A conflict is detected between roots, never between two keys naming one root.** A
  project declaring both `shared:x` and `local:x` where the two are the same directory
  gets that module's directives twice in one table. Nothing reports it. *Exit condition*:
  a declaration-level duplicate check, worth writing when a composition is seen doing it —
  it takes a deliberate link plus two deliberate keys to reach.
