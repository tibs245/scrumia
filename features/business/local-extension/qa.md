# Acceptance criteria — Local extension

One scenario per rule in `business.md`. Each scenario must be able to fail.

## Nominal

### AC-1 — A module outside a marketplace reaches a register's table

```gherkin
Given a well-formed module sitting in a directory of checkouts rather than in a
  marketplace, contributing a directive to a register this project's composition opens
When the directives for that register are asked for
Then its directive appears in the table, and the steps taken were exactly two: the
  checkout placed in the directory this machine names, and one `shared:` key added to
  `modules` — no path written into any versioned file, no per-module configuration
  beyond that key
And a published module of the same name that the composition does not declare changes
  nothing about that answer
```

### AC-2 — A module inside the project reaches the same table

```gherkin
Given the same module placed at `.scrumia/modules/<module>/` instead, declared `local:`
When the directives for that register are asked for
Then its directive appears identically, and nothing in the table distinguishes it from a
  published module beyond the location that is reported alongside it
```

### AC-3 — Resolution states where each module came from

```gherkin
Given a composition mixing published modules, a module from a shared checkout directory,
  and a module inside the project
When the modules the composition resolves are reported
Then each is shown with the location it resolved from and the directory it resolved to,
  and no module is shown without one — a module the machine cannot reach appearing as a
  declared absence naming the location it would come from, never as a blank
```

The surface is `scrumia-extends --modules`, named here because "the composition is
reported" had two candidate readers and only one of them resolves anything. The other
prints the declarations as written, which is a different claim and needs no location.

### AC-4 — A local module is held to the same standard

```gherkin
Given a module inside a project that would produce findings if it were published
When the anatomy checker runs over it
Then it produces the same findings, in the same form, with no allowance made for the
  module being local
```

The checker takes a path and reads that tree alone, so what satisfies this criterion is
that it has no notion of location at all, rather than that it treats three of them alike.
The test is one tree checked from two locations returning the identical verdict.

## Conflict and absence

### AC-5 — Two modules answering one declaration is a conflict, never a silent choice

```gherkin
Given one declaration that two distinct modules, in two locations, both answer to
When the composition resolves that declaration
Then the conflict is reported naming both locations, neither is used, no directive of
  that module reaches any register, and every other declaration still resolves — search
  order decides nothing
And the dependency check exits non-zero on it, so the shortened table is not the only
  signal
Given instead a module reachable at two paths that are the same directory — a checkout
  reached through a link as well as directly
When the composition resolves it
Then it is one module: it resolves, it is used, and its location is reported once
Given instead a published module installed and a checkout of it declared `shared:`
When the composition resolves that declaration
Then the checkout resolves and is used, the published copy is a module this project does
  not run, and nothing is reported as a conflict
```

The last two scenarios are the ones that make the first safe to enforce. Promotion
produces both copies by construction — `module-authoring`'s BR-3 is only affordable if
holding them at once is not a fault — and each is settled by identity or by the
declaration rather than by the search, which is what BR-7's test buys.

### AC-6 — A clone that cannot reach the module is told, and still works

```gherkin
Given a project whose composition names a module living only in a shared checkout
  directory on another machine
When the composition is read on a fresh clone
Then the capability is reported as a declared absence, naming the module and the kind of
  location it would come from, every register that module contributed to renders without
  it, and nothing fails
```

### AC-7 — What `CLAUDE.md` claims survives a clone without the local material

```gherkin
Given a project whose `CLAUDE.md` describes its composition
When it is read on a clone that has none of the machine-local material
Then every capability it claims is either present or reported as absent, and none is
  claimed as present while being unreachable
```

This is the criterion the shared-checkout location is most likely to fail. It is stated
so that choosing that location is a decision with a known cost rather than a convenience.

## Boundary

### AC-8 — Local material without a module is not a malformed module

```gherkin
Given a project whose only local extension is a set of directives and a rules section,
  with no module of its own anywhere
When the composition is checked and the anatomy checker runs
Then the project is reported as correctly extended, the directives appear in their
  registers, and no finding claims a module is missing or malformed
```

### AC-9 — No versioned file names a path outside the project

```gherkin
Given a project running a module from a shared checkout
When every file the repository versions is read
Then the module is keyed `shared:<module>`, so its location is stated by its declaration
  and by nothing beside it, no filesystem path outside the project appears in any
  versioned file, and the path `shared` resolves to comes from `.scrumia/.env.local`
And `.scrumia/.env.local` is excluded from version control
```

The exclusion is part of the rule, not an operational detail: a repository that commits
that file has put one machine's layout back into the composition, which is the thing this
criterion exists to prevent.

### AC-10 — A directive needs no installation

```gherkin
Given a project adding one directive to a register a module opened
When that register is asked for
Then the directive appears with no module having been created, versioned or installed for
  it
```
