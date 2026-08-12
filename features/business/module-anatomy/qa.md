# Acceptance criteria — Module anatomy

One scenario per rule in `business.md`. Each scenario must be able to fail.

## Nominal

### AC-1 — The checker produces a verdict on a module it has never seen

```gherkin
Given any directory that claims to be a ScrumIA module
When the checker is asked for a verdict on it
Then it returns a list of findings — possibly empty — each naming the module, the file
  and the rule that was not met, and it exits distinguishing "checked, nothing found"
  from "could not check", so an unreadable module is never reported as a clean one
```

### AC-2 — Run on this repository's own modules, the checker returns findings

```gherkin
Given the modules this repository ships, none of which was written against this standard
When the checker runs over all of them
Then the finding list is not empty, and every finding names a module and a file that
  exist
```

The point of this criterion is that it can fail in the direction nobody wants: a checker
returning nothing on modules that predate its own standard is a checker that checks
nothing. It stops being useful once the findings are fixed, at which point it is replaced
by AC-1 on a deliberately malformed fixture rather than deleted with the debt.

### AC-3 — The owner is checked like every other module

```gherkin
Given the module that publishes the checker
When the checker runs over every module the marketplace ships
Then that module appears in the run like any other, and a finding against it is reported
  in the same form as a finding against any other — no skip, no exemption, no separate
  tier
```

### AC-4 — The checker writes nothing

```gherkin
Given a module with findings against it, in a clean working tree
When the checker runs over it twice
Then the working tree is unchanged after both runs, no file was created, repaired or
  reformatted, and the second run reports exactly what the first did
```

### AC-5 — The marketplace gate delegates and re-verifies nothing

```gherkin
Given this repository's marketplace gate and the checker
When the gate runs
Then every module-level rule it applies comes from the checker, the gate's own checks are
  only those about the manifest that lists the plugins, their versions and their sources,
  and no rule is verified in both places
```

A rule verified twice is two renderings of it, and the second one is free to drift. This
criterion fails the moment a check is copied rather than delegated.

## Absence and boundary

### AC-6 — A module with no README is a finding

```gherkin
Given a module that ships skills, a contract and a changelog, and no README
When the checker runs over it
Then a finding names the missing README, and the module's `SKILL.md` contract does not
  satisfy it — the two have different readers and one never stands in for the other
```

### AC-7 — A reference that resolves outside the module is a finding

```gherkin
Given a module containing a relative path that leaves the module's own root
When the checker runs over it
Then a finding names the file and the reference, citing the rule as
  `features/business/modular-composition/`'s rather than restating it
```

### AC-8 — A link to a file that does not exist is a finding

```gherkin
Given a module whose skill links to a relative path, and whose skill invokes a script
When either target is absent from what the module ships
Then each is a separate finding naming the referring file and the missing target
```

### AC-9 — A file answering two questions is reported

```gherkin
Given a module file that answers two distinct questions a reader could arrive with
When the checker runs over it
Then a finding names it, and the same finding is not raised against a file that answers
  one question at length — length alone is never the trigger
```

The trigger is stated so it can be argued with. A checker that reports on line count
reports on the wrong thing, and this criterion fails if a long single-concern file is
flagged.

### AC-10 — An index that carries content is reported

```gherkin
Given a module whose entry point lists what the module ships and also states a rule found
  nowhere else
When the checker runs over it
Then a finding names the entry point, because content reachable only through the index is
  content the index carries rather than routes
```

### AC-11 — A directory that is not a module is refused, not judged

```gherkin
Given a directory with no module manifest at all
When the checker is asked for a verdict on it
Then it states that this is not a module and returns no findings, rather than returning
  one finding per rule the directory happens not to meet
```

An unbounded finding list on an arbitrary directory is how a checker teaches people to
ignore it.
