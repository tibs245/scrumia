# ADR-0020 — The composition is assembled by a tool, not recomposed by the agent

**Status**: accepted — 2026-08-11

## Context

[ADR-0009](0009-documented-composition.md) settled *when* a composition is resolved: once,
at composition time, written into `CLAUDE.md`, read as documentation. That decision stands.
What it never settled is **who does the resolving**, and the answer has always been: the
agent, at read time, out of prose.

An agent about to act reads `CLAUDE.md`'s table, finds the owning module, opens its
`SKILL.md` — and then notices, **in prose**, that another module also has something to say.
`scrumia-rust` carries a section situating whichever practice is plugged in.
`scrumia-ticket` is told to read "the specs contract". The precedence between an
implementation module and a practice was stated in [ADR-0010](0010-cross-cutting-practices.md)'s
body, which nothing sends the agent to. So the agent opens more files, in an order it
infers, and applies a rule it may never have read.

That recomposition is performed by the least reliable actor in the system, once per
session, and nothing checks the result. The audit run during #184's scoping measured the
outcome: **`scrumia-specs-find` has one provider and five prose copies, and it is the
copies that run**; 37 of 37 skills carry a gap between what they promise and what they do.

**[ADR-0018](0018-modules-reach-by-name.md) closed half of this and left the other half
with no good answer.** A module can now *run* another module's script by a published name.
It still cannot tell an agent to *read* another module's document: 0018 offers exactly two
exits — inline it, or cite an absolute URL into this repository. The first is how five
copies of `scrumia-specs-find` came to exist. The second is meaningless in a consuming
project, which has never had this repository's files. Every prose copy the audit found is a
module doing the only thing 0018 left it.

[ADR-0011](0011-rules-hierarchy.md) has a matching unpaid debt. It accepted that "the index
can drift from the files on disk" and promised a `validate.py` check as the mitigation.
That check was never built. The debt and the missing mitigation are the same evidence:
hand-maintained routing does not survive.

## Decision

**A tool assembles, per action and per project, the document that says what to load and in
what order. The rules stay in the module that owns them.**

### The assembly merges routing, not prose

An assembly is a generated index, not a merged corpus. Copying guide bodies into one file
would rebuild the monolith ADR-0011 was written to reject — reloaded whole to read three
lines — and would promote the drifting-copy defect into a build artefact.

This is not only a context-size argument. **Routing-only is what makes the staleness digest
cheap, and a cheap digest is what makes § *Materialisation* below hold.** The two are one
decision: merge the prose, and the digest must cover every guide body, at which point
verifying it is a rebuild.

### A module declares how to enter it, and the module orders its own files

Each module ships `composition.json` at its root, naming — for each action it provides from
the kernel's closed vocabulary — the **entry fragment** an agent opens, the published name
it runs, and the name a person types to reach it:

```json
{
  "module": "scrumia-teams",
  "grain": "cross-cutting",
  "provides": [
    { "action": "sprint/assemble-batch",
      "read": ["skills/scrumia-sprint/SKILL.md"],
      "entry": "scrumia-teams:sprint" },
    { "action": "build/pick-model", "run": "scrumia-pick-model" }
  ],
  "calls": [ { "action": "build/execute-ticket", "from": "skills/scrumia-sprint/SKILL.md" } ]
}
```

**The assembly orders contributors; inside a contributor, its own routing table and
dependency graph govern.** A manifest naming individual guides would restate ADR-0011's
per-guide triggers in a second, hand-maintained place — and would strip the dependency
graph that says `04-testing` presupposes `02` and `03`, instructing an agent to open a
guide whose prerequisites it never mentions.

No fragment carries a hand-written description. Its own frontmatter `description:` is the
one the build reads, and a fragment without one fails the build. The measurement that
settled this: every `when-needed` fragment in the rejected draft was a guide with no
frontmatter at all, so the field was derivable from nothing and maintainable by nobody.

`grain` — `technology` or `cross-cutting` — carries ADR-0010's *specific beats generic* as
a property of the module, now that [ADR-0019](0019-extends-replaces-composition-and-practices.md)
has retired the `practices` key that used to carry it.

### A module publishes its manifest by name

Each module publishes `<module>-manifest` under its own `bin/`, which prints its
`composition.json` with `root` resolved from the executable's own location. The name
already carries ADR-0018's mandatory `scrumia-` prefix, because every module name does.

The tool therefore holds no knowledge of install layout, parses no private file, and never
decides *which* module answers anything: it asks a module named by the project's own
`extends` to describe itself. That is not the registry ADR-0009 rejected.

**Absence of a name is never data.** Three outcomes, and the third is what makes this safe:

| State | Verdict |
|---|---|
| On PATH, valid manifest | Contributes |
| On PATH, no `composition.json` | Named degradation — contributes nothing, said by name |
| Named in `extends`, **not on PATH** | **The build fails**, naming the module and the restart rule |

Reading name-absence as "this module contributes nothing" would invert ADR-0018's own
defence. 0018 accepts the PATH risk on the argument that a caller "breaks loudly — the name
is not found". That holds when calling a known name; it collapses when absence *is* the
answer. The concrete case is not hypothetical: a plugin enabled but not yet restarted is
the single most common reason a name is missing, and it would have produced a well-formed
**empty** assembly — committed, CI-green, and read as authoritative evidence that no rules
apply. Failing the build is strictly better than any answer.

### The artefact holds no path this machine resolves

A built assembly names `module + path-inside-module`, never an absolute path.

This is the only remaining form, not merely the nicest. `.scrumia/assemblies/` is neither a
skill nor inside a plugin, so no harness variable is substituted there — `${CLAUDE_SKILL_DIR}`
and `${CLAUDE_PLUGIN_ROOT}` are both already refused elsewhere for the same reason. An
absolute path is machine-specific, which is fatal for a committed, shared artefact. A
relative path climbing out of `.scrumia/` into a versioned plugin cache is unwritable, which
is ADR-0018's opening paragraph.

`scrumia-assemble load` resolves those pairs to real paths when it prints. The committed
artefact stays portable; only the printed answer carries a path.

### Materialisation: built at composition, read at call

`scrumia-assemble build` runs at composition time. `scrumia-assemble load <action>` prints a
built file and **computes nothing**. When its digest no longer matches, it **refuses and
says to rebuild** rather than silently recomputing — a tool that recomputed at call time
would be the registry ADR-0009 rejected, wearing a build step as a disguise.

**The digest covers the project's own cheap inputs only** — `.scrumia/config.yaml` and the
project-local overrides — never the modules' manifests. Were it to cover them, verifying
would mean running every manifest: per-call resolution, and most of `build`'s work. A tool
that has computed the right answer and then refuses to print it is dominated, and the
relaxation would be correct rather than lazy. The line holds only because nothing pulls
against it.

**A plugin version bump does not invalidate a digest, and must not.** Because the artefact
holds routing and not prose, a version that rewrites a guide's body leaves the assembly
correct. Only a version that changes which fragments exist invalidates it, and that is
caught by `scrumia-assemble check` in CI and by a loud missing file — never by wrong prose.
Module versions are recorded in the assemblies index as information for a human reading the
diff, explicitly not as a digest input.

The digest is written once, in the assemblies index. Writing it into every action's file
would turn one config edit into a rewrite of every committed assembly — a merge-conflict
generator across the parallel worktrees a sprint cuts.

### When two contributions meet

Two providers on a **decision** action fails the build, naming both — ADR-0019's BR-8. That
check belongs to `build`, scoped to what `extends` names: two modules that no project plugs
together are not in conflict, and refusing them repo-wide would forbid a second tracker
module, which [ADR-0013](0013-tracker-stays-one-slot.md) deliberately leaves open.

Two **contributions** are both listed, in an order the tool computes and states: project-local
beats app-level beats project-wide; within a tier, `technology` grain beats `cross-cutting`;
then alphabetical, so the artefact is deterministic. That is ADR-0010's precedence rule,
mechanised instead of left in an ADR body.

Two fragments whose **prose** contradicts is **not detected**. A generator cannot read
English. What it delivers is that the two are now visible in one document, in a stated
order, which they never were. Named sub-slots inside an action would make a subset of this
mechanical; **reserved, not adopted** — the posture ADR-0019 took on `x-<module>/<action>`.

### An entry point is reached, not covered

Coverage arithmetic counts **module callers only**. An action provided by a module that no
other module reaches stays a hole, exactly as `features/business/modular-composition/`'s
§ *Coverage is derived, not declared* requires — `scrumia-review` included.

What changes is that the hole names its **entry point**, resolved by CI to a real skill or
command file, so the remedy printed is the right one instead of "plug a module that provides
it". The asymmetry that makes this evidence sufficient here and insufficient in the caller
graph: **for a human entry point, existence is the whole claim** — a command file that
exists is invocable, there is no further edge — **while for a module-to-module edge,
existence refutes nothing.**

## Consequences

**What we gain**

- The recomposition an agent used to perform from prose is performed by a tool, at
  composition time, into an artefact a human can read and a diff can show.
- A module can finally point at another module's document, which ADR-0018 left it no way to
  do — closing the hole the five copies of `scrumia-specs-find` were filling.
- ADR-0011's never-built drift mitigation is paid: a fragment that stops existing fails the
  build instead of dangling in an index nobody rechecks.
- ADR-0009's own stated worst flaw — *"`CLAUDE.md` can diverge from the configuration. This
  is the most likely flaw of this design"* — is closed mechanically rather than by asking an
  agent to copy blocks by hand.

**What we accept**

- **The PATH behaviour is now load-bearing for the whole mechanism, not for two call sites.**
  ADR-0018 accepted it as *observed on Claude Code 2.1.227, not contracted*, on the argument
  that its two callers fail loudly. This makes every assembly depend on it. Verified again
  here, on Claude Code 2.1.227: every enabled plugin's `<root>/bin` is on the session PATH,
  including directories absent from disk when the session started. If the harness changes,
  no assembly can be built — which is loud, and is why the third outcome above is a build
  failure rather than an empty file.
- **CI exercises the repo-path resolution, never the PATH one.** The validation workflow is
  a checkout and a Python run: no harness, no installed plugins, no PATH entries. The
  mechanism therefore has two resolution paths and the product's own is exercised by no
  automated run at all, only by the manual verification recorded above.
- **Callers are declared, not measured.** A module now declares what it calls, with a file
  inside itself as evidence — which is a provenance fix, since the party that knows writes
  the line, and the reason nobody caught `build/move-card` naming three callers that did not
  call it. It is not a measurement: a file existing, and even containing a name, refutes
  nothing about whether that call runs. Deriving callers by grepping for published names is
  filed, not claimed here.
- **A manifest is a new obligation on module authors**, and it is deliberately not a fourth
  entry in `modular-composition`'s *three things a module owes*. That list admits an item
  only when skipping it breaks **silently**; a missing manifest is a loud, named degradation.
  It lives in its own section, and a module without one is still composable — it simply
  contributes to no assembly.
- **The contract blocks are not inlined into assemblies.** Doing so would put one payload in
  three places behind two generators with no gate between them. `build` emits them once, in
  the assemblies index; making `scrumia-init` read them from the manifest rather than copying
  a markdown section by hand is filed.

## Rejected alternatives

**Merging the rules themselves into one generated skill** — the shape first proposed.
Rejected on ADR-0011's own reasoning: a document that only grows and is reloaded whole to
read three lines. It would also make the staleness digest cover every guide body, which
collapses § *Materialisation* into a rebuild-on-every-call.

**A directed `A extends B` edge between modules.** Rejected: it would make one module name
another's internals, weakening the decoupling ADR-0009 exists to protect, and would require
a third-party author to know the extendee rather than only the kernel's action vocabulary.
What reads as "A extends B" is two modules contributing to the same action, which ADR-0019
already expresses. `extends` therefore keeps exactly one sense — ESLint's, a flat unordered
list of participants — and the config schema is unchanged by this ADR.

**Reading `~/.claude/plugins/installed_plugins.json` to find a module's root.** Rejected
again, on ADR-0018's grounds: it is the capability registry rebuilt by hand, and it breaks
when a private file changes shape. Asking a module to describe itself through a published
name needs neither.

**Recomputing on `load` instead of refusing.** Rejected: it is resolution at call time, and
it is what ADR-0009 refused. The design is arranged so that refusing is also the *cheaper*
option, because a decision that costs its holder nothing is the only kind that survives.

## To revisit

- If the entry-point wording still leaves a hole count readers learn to ignore, the next
  step is a third **reported** bucket — an action outside both counters — which requires
  `modular-composition/business.md` amended, and is a business decision rather than a
  mechanism one.
- If prose contradictions between two contributions turn out to be frequent rather than
  theoretical, revisit the named sub-slots reserved above.
- If the harness publishes a contract for plugin PATH, or withdraws the behaviour, this ADR
  and 0018 move together.
