# Acceptance criteria — Module anatomy

One scenario per rule in `business.md`. Each scenario must be able to fail.

Each criterion names the surface it applies to. A criterion naming neither applies to both.

## The procedural check

### AC-1 — A verdict on a module it has never seen

```gherkin
Given any directory carrying a plugin manifest
When the procedural check is asked for a verdict on it
Then it returns findings — possibly none — each naming the module, the file, the
  qualified rule and one line of what was not met
And it exits with the code its state carries, so that a clean module, a malformed one, a
  target that is not a module, a bad invocation and the tool's own failure are five
  distinguishable outcomes rather than "zero or non-zero"
And `--json` names the state in a field, so no consumer infers it from whether the
  finding list is empty
```

A consumer that branches on truthiness reports a clean module as non-conformant the day
`jq` goes missing. That is the failure this criterion exists to fail on.

### AC-2 — Run on this repository's own modules, it returns findings

```gherkin
Given the modules this repository ships, none of which was written against this standard
When the procedural check runs over all of them
Then the finding list is not empty, and every finding names a module and a file that
  exist
```

The point of this criterion is that it can fail in the direction nobody wants: a check
returning nothing on modules that predate its own standard is a check that checks nothing.
It stops being useful once the findings are fixed, at which point it is replaced by AC-1 on
a deliberately malformed fixture rather than deleted with the debt.

### AC-3 — The owner is checked like every other module

```gherkin
Given the module that publishes the procedural check
When it runs over every module the marketplace ships
Then that module appears in the run like any other, and a finding against it is reported
  in the same form — no skip, no exemption, no separate tier
```

### AC-4 — Neither surface writes

```gherkin
Given a module with findings against it, in a clean working tree
When the procedural check runs over it twice, and the audit runs over it twice
Then the working tree is unchanged after all four runs, no file was created, repaired or
  reformatted, and each second run reports what its first did
```

### AC-5 — The marketplace gate delegates what a module's tree can answer

```gherkin
Given this repository's marketplace gate and the two surfaces
When the gate runs
Then every rule it applies that a surface also applies comes from that surface rather
  than from its own code
And what it keeps is what no surface applies: the manifest listing the plugins, their
  versions and their sources; the rules governing the specs tree and the repository's own
  prose; the rules about the relationship between two modules, which no single tree can
  answer; and any module rule a surface could take and has not taken yet, each named
  where it is kept
And no rule is verified in both places
```

The second clause is what stops AC-5 from being read as "keep the manifest checks and
delete the rest". The specs-tree rules are not a module's property and the procedural check
cannot see them; handing them over would not be delegation, it would leave them unenforced.
A rule a surface could decide and does not yet apply is the same failure reached later:
deleting it from the consumer hands it to nobody, which is why it stays, named.

### AC-6 — A module with no README is a finding

```gherkin
Given a module that ships skills, a contract and a changelog, and no README
When the procedural check runs over it
Then a finding names the missing README, and the module's `SKILL.md` contract does not
  satisfy it — the two have different readers and one never stands in for the other
```

### AC-7 — A README missing a required section is a finding; a missing optional one is not

```gherkin
Given a README carrying its name and paragraph, what it answers and what it ships, and
  no "What it refuses"
When the procedural check runs over it
Then a finding names the missing section
Given instead a README carrying the four required sections in order and none of the
  optional ones
When the same check runs
Then no finding is raised — a module that reads no setting, needs nothing else present
  and ships no decision record states all three by omission
Given instead a README whose required sections appear in a different order
When the same check runs
Then a finding names the order, because a reader comparing four modules compares them
  by position
```

The negative half is what keeps the template from producing the defect it exists to
prevent. A check requiring every section would fill four modules with "none", which is
the noise the specs catalog already refuses one level up.

### AC-8 — A reference that resolves outside the module is a finding, and a permitted one is not

```gherkin
Given a module containing a relative path that leaves the module's own root
When the procedural check runs over it
Then a finding names the file and the reference, and cites the rule by its qualified
  identifier — `modular-composition/BR-7` — with any document it points at given as an
  absolute URL, because the check runs in projects that never had this repository's
  `features/` tree
Given instead a module reaching another by a bare name published on `PATH`, or citing a
  document by absolute URL
When the same check runs
Then neither raises a finding
```

The second half is not decoration. Both forms are what `modular-composition`'s BR-7
permits and what this repository's own conventions require; a check enforcing only the
first half flags every citation in every module and is unusable here.

### AC-9 — A link, a script or a published name that cannot be followed is a finding

```gherkin
Given a module whose skill links to a relative path, and whose skill invokes a script
When either target is absent from what the module ships
Then each is a separate finding naming the referring file and the missing target
Given instead a module shipping a name under `bin/` that is present and not executable
When the same check runs
Then a finding names it, because the name is how every other module reaches this one and
  it fails in the caller, which cannot see why
```

### AC-10 — Extension data a module ships is checked; extension data it omits is not

```gherkin
Given a module that opens no register and contributes no directive, shipping none of the
  extension data files
When the procedural check runs over it
Then no finding claims a missing declaration — the absence is a statement
Given instead a module shipping an `extends.json` that does not parse, or a
  `registers.json` naming a register it never opens, or a `dependencies.jsonl` line that
  is not a record, or one naming a published name with no source
When the same check runs
Then each is a finding
```

This is the case where a module composes cleanly and contributes nothing, and its silence
looks like a decision.

Whether the source a declaration names exists is not on this list. A source names a
marketplace, not a file, so a module's own tree holds no answer — that check belongs to
whatever resolves the composition, and `tech.md`'s boundary is what puts it there.

### AC-11 — A directory that is not a module is refused, not judged

```gherkin
Given a directory with no `.claude-plugin/plugin.json`
When the procedural check is asked for a verdict on it
Then it exits with the code `tech.md` gives the `not a module` state — `4`, distinct from
  the one a bad invocation carries — states that this is not a module, and returns no
  findings, rather than returning one finding per rule the directory happens not to meet
```

An unbounded finding list on an arbitrary directory is how a check teaches people to
ignore it.

### AC-22 — A manifest carries the schema's fields and only those (`module-anatomy/BR-13`)

```gherkin
Given a module's `.claude-plugin/plugin.json`
When the procedural check runs over it
Then the finding is empty if every key the file carries is one the plugin schema
  defines and the three BR-13 marks always-present are all there
And a key the schema does not define raises a finding naming the file and BR-13
  (https://github.com/tibs245/scrumia/blob/main/features/business/module-anatomy/business.md)
Given instead a manifest that omits a conditional field BR-13 marks
  (`repository`, `homepage`, `author`, `license`, `keywords`)
When the same check runs
Then no finding is raised against the omission — the absence is itself the statement
  BR-13 takes as conformant
```

The first scenario fails the day a manifest is allowed to grow a key the platform does
not define, which is the invention the rule exists against. It does not fail on `author`,
`license` or `keywords`: those are fields the plugin schema defines, every module the
marketplace ships carries them, and a standard that called them non-conformant would put
conformity to itself and conformity to the loader in conflict. The second scenario is the
rule that keeps the procedural check from reporting an absence: omitting `repository`
because the module is not yet hosted is conformant, and a check that turned it back in
would be flagging the conformant case as the defect the rule exists against.

A failing scenario — a manifest carrying a key outside the schema — can be triggered with
a single invented string. A passing one is a manifest that names only fields the schema
defines.

## The audit

### AC-12 — A file answering two questions is reported, and a long one is not

```gherkin
Given a module file that answers two distinct questions a reader could arrive with
When the audit runs over the module
Then a finding names it
Given instead a file that answers one question at length
When the same audit runs
Then no finding is raised against it — length is never the trigger, in either direction
```

Both halves are required. A surface that flags long single-concern files has replaced the
rule with a proxy, which is what moving this criterion to the audit was meant to avoid.

### AC-13 — An index that carries content is reported

```gherkin
Given a module whose entry point lists what the module ships and also states a rule found
  nowhere else
When the audit runs over it
Then a finding names the entry point, because content reachable only through the index is
  content the index carries rather than routes
```

### AC-14 — An optional section a module needs, and omits, is a finding

```gherkin
Given a module that reads three settings and whose README carries no "Settings it reads"
When the audit runs over it
Then a finding names the omission, because the absence asserts something the module
  contradicts
Given instead a module that reads none and omits the same section
When the same audit runs
Then no finding is raised — the absence is true, which is what makes it information
```

Also the audit's: a README past the ~80-line guardrail, judged on what the extra lines are
doing rather than on the count, which is the proxy BR-2 refuses.

### AC-15 — Every audit question is closed, single-concern and answerable from one file

```gherkin
Given the audit's checklist
When each question is read
Then it admits a yes or no answer, names exactly one of this feature's rules, and can be
  answered from a single file without the rest of the module in context
And no question states a rule that appears nowhere in `business.md`
```

This is the criterion that keeps the audit affordable. A question needing the whole module
in context is one that cannot run on a cheap model, and an audit that cannot run cheaply is
one that runs once.

### AC-16 — Both surfaces report in one shape

```gherkin
Given findings produced by the procedural check and findings produced by the audit
When a consumer merges the two lists
Then every row carries module, file, rule and one line of what was not met, and nothing in
  a row's shape reveals which surface produced it
```

### AC-17 — A doc a skill needs, cited instead of carried, is a finding

```gherkin
Given a module whose skill applies a rule it does not state, and points at a document
  outside the module for it
When the audit runs over it
Then a finding names the reference, because what the skill applies is not in the module
Given instead a module whose skill states the rule and points outward only for the reason
  behind it
When the same audit runs
Then no finding is raised — provenance is a legitimate reason to point outward
Given a module citing an external source nobody can vendor, with its licence
When the same audit runs
Then no finding is raised
```

Split across both surfaces, per BR-5. *That* a reference leaves the module is decidable
from the tree and is the procedural check's — and is enforced by neither surface today,
which is debt this criterion makes visible rather than hides. *Whether* what it reaches is
operative or provenance has to be read, so it is the audit's, and it is the half stated in
the Gherkin above. The two are one rule reported in one shape (AC-16), not two rules.

A form-shaped question is not accepted in place of this one: a bare path in prose and a
markdown link are the same act, and asking only about links would pass a module that writes
every one of them the other way.

### AC-23 — A publication field, when present, names a publication that exists (`module-anatomy/BR-13`)

```gherkin
Given a module whose manifest carries `repository` or `homepage`
When the audit runs over the module
Then the URL resolves on the day the audit runs, and a finding names the file and the
  unresolvable field — alongside BR-13
  (https://github.com/tibs245/scrumia/blob/main/features/business/module-anatomy/business.md)
Given instead a manifest carrying neither
When the same audit runs
Then no finding is raised — the absence is the statement BR-13 takes as conformant
```

This is the half BR-5 sends to the audit. A URL is read, not parsed: which of the
publication fields a manifest carries is the procedural check's, and a manifest carrying
the wrong one is BR-13's, not this criterion's. A link the audit cannot open on the day
it runs names the file and the unresolvable field — never the surrounding manifest — so
a finding the reviewer has to walk back through `plugin.json` to read.

"Resolves on the day the audit runs" snapshots the URL: a publication that moves later is
not re-found here. The audit reads no cache, makes no second attempt, and refuses to
guess at a redirect. A blank `homepage` is an empty string the audit will not try to open;
that is BR-13's case (a conditional field that should have been absent) and the procedural
check owns it.
