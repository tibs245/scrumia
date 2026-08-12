# Acceptance criteria — Module anatomy

One scenario per rule in `business.md`. Each scenario must be able to fail.

Each criterion names the surface it applies to. A criterion naming neither applies to both.

## The procedural check

### AC-1 — A verdict on a module it has never seen

```gherkin
Given any directory carrying a plugin manifest
When the procedural check is asked for a verdict on it
Then it returns a list of findings — possibly empty — each naming the module, the file
  and the rule that was not met, and it exits `0`, `1` or `2` so that "checked, nothing
  found" is never confused with "could not check"
```

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
Then every rule it applies that is decidable from one module's tree comes from the
  procedural check rather than from its own code
And the checks it keeps are exactly those neither surface can see: the manifest listing
  the plugins, their versions and their sources, and the rules governing the specs tree
And no rule is verified in both places
```

The second clause is what stops AC-5 from being read as "keep the manifest checks and
delete the rest". The specs-tree rules are not a module's property and the procedural check
cannot see them; handing them over would not be delegation, it would leave them unenforced.

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
Then a finding names the file and the reference, citing the rule as
  `features/business/modular-composition/`'s rather than restating it
Given instead a module reaching another by a bare name published on `PATH`, or citing a
  document by absolute URL
When the same check runs
Then neither raises a finding
```

The second half is not decoration. Both forms are what `modular-composition`'s BR-7
permits and what this repository's own conventions require; a check enforcing only the
first half flags every citation in every module and is unusable here.

### AC-9 — A link or a script that does not exist is a finding

```gherkin
Given a module whose skill links to a relative path, and whose skill invokes a script
When either target is absent from what the module ships
Then each is a separate finding naming the referring file and the missing target
```

### AC-10 — Extension data a module ships is checked; extension data it omits is not

```gherkin
Given a module that opens no register and contributes no directive, shipping none of the
  extension data files
When the procedural check runs over it
Then no finding claims a missing declaration — the absence is a statement
Given instead a module shipping an `extends.json` that does not parse, or a
  `registers.json` naming a register it never opens, or a `dependencies.jsonl` naming a
  source that does not exist
When the same check runs
Then each is a finding
```

This is the case where a module composes cleanly and contributes nothing, and its silence
looks like a decision.

### AC-11 — A directory that is not a module is refused, not judged

```gherkin
Given a directory with no `.claude-plugin/plugin.json`
When the procedural check is asked for a verdict on it
Then it exits `2`, states that this is not a module, and returns no findings — rather than
  returning one finding per rule the directory happens not to meet
```

An unbounded finding list on an arbitrary directory is how a check teaches people to
ignore it.

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

### AC-14 — Every audit question is closed, single-concern and answerable from one file

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

### AC-15 — Both surfaces report in one shape

```gherkin
Given findings produced by the procedural check and findings produced by the audit
When a consumer merges the two lists
Then every row carries module, file, rule and one line of what was not met, and nothing in
  a row's shape reveals which surface produced it
```
