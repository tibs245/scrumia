# Acceptance criteria — Local extension

One scenario per rule in `business.md`. Each scenario must be able to fail.

## Nominal

### AC-1 — A module outside a marketplace reaches a register's table

```gherkin
Given a well-formed module sitting in a directory of checkouts rather than in a
  marketplace, contributing a directive to a register this project's composition opens
When the directives for that register are asked for
Then its directive appears in the table, and the only thing that had to happen is the
  project declaring the module
```

### AC-2 — A module inside the project reaches the same table

```gherkin
Given the same module placed inside the project instead
When the directives for that register are asked for
Then its directive appears identically, and nothing in the table distinguishes it from a
  published module beyond the location that is reported alongside it
```

### AC-3 — Resolution states where each module came from

```gherkin
Given a composition mixing published modules, a module from a shared checkout directory,
  and a module inside the project
When the composition is reported
Then each module is shown with the location it resolved from, and no module is shown
  without one
```

### AC-4 — A local module is held to the same standard

```gherkin
Given a module inside a project that would produce findings if it were published
When the anatomy checker runs over it
Then it produces the same findings, in the same form, with no allowance made for the
  module being local
```

## Conflict and absence

### AC-5 — Two modules with one name is a conflict, never a silent choice

```gherkin
Given a module name present both in a marketplace the project declares and in the project
  itself
When the composition resolves that name
Then the conflict is reported naming both locations, and neither is used until it is
  resolved — search order decides nothing
```

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

### AC-9 — A directive needs no installation

```gherkin
Given a project adding one directive to a register a module opened
When that register is asked for
Then the directive appears with no module having been created, versioned or installed for
  it
```
