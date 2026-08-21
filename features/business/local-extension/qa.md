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
Given one declaration that two distinct modules both answer to — a module and a fork of
  it, checked out side by side in the location its key names
When the composition resolves that declaration
Then the conflict is reported naming both directories, neither is used, no directive of
  that module reaches any register, and every other declaration still resolves — search
  order decides nothing
And the dependency check exits non-zero on it, so the shortened table is not the only
  signal, and it does so once rather than once per register that module opens
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

### AC-11 — A declaration naming no location is shadowed, not disabled

```gherkin
Given a declaration in the retired list shape, which names no location, and two locations
  answering it — a published module and a checkout of it
When the composition resolves that declaration
Then the narrowest location is used, the module contributes its directives normally, the
  report names every location that answered and which one won, and it names the fix:
  keying the declaration by source
And the dependency check does not fail on it — a shadow is used, so it is only ever said
```

This is the case a rule fired on the name alone would have broken: it is what promotion
looks like from a project still on the retired shape, and disabling the module there would
punish a project for a grammar it is being migrated off.

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
Given a project whose `CLAUDE.md` names a module by its bare name, resolving only from a
  shared checkout on the machine that wrote the file
When the claims that file makes are reconciled against resolution on a clone holding
  none of that material
Then that module is named with the state it resolved to and the origin its key states,
  and the reconciliation exits non-zero — the file claims a capability this reader has
  no way to reach
Given instead a `CLAUDE.md` naming the same module by its declaration key, so the file
  itself states where the module would come from
When the same reconciliation runs on the same clone
Then the claim is reported as an absence the file already states, and it exits zero
Given a project every declared module of which resolves for the reader
When the same reconciliation runs
Then every claim is honoured and it exits zero, on any machine
Given instead a module named by its bare name that nothing answers either, declared from a
  marketplace or from inside the project — a location whose absence is every reader's, the
  author's included
When the same reconciliation runs
Then it is reported without failing, because what is missing there is the module and not
  the sentence
And in none of the four does any register fail to render, nor any other surface fail
```

The surface is `scrumia-extends --claims`, named here for the same reason AC-3 names its
own: *"`CLAUDE.md` is read"* has no actor, and a criterion whose subject is a file nobody
runs can neither pass nor fail. What it compares is the file's text against the state each
declaration resolved to — not the prose around it, which is the human's.

This is the criterion the shared-checkout location is most likely to fail. It is stated
so that choosing that location is a decision with a known cost rather than a convenience.

### AC-14 — A per-app `CLAUDE.md` stub is reconciled against its own scope

```gherkin
Given a project whose root `CLAUDE.md` declares nothing about a module, but whose
  `apps[].path/CLAUDE.md` for one app declares `shared:acme-web` and lists the
  app's `modules:` mapping under that key
When `scrumia-extends --claims` runs at the project root
Then it reconciles the app's stub against the app's own scope, the app's declaration
  is reported `claimed` against the app's file, and the exit code is 0 for that
  module
And a module declared at the root file is reconciled against the root file
And a module declared in neither file is reported `not claimed` and exits non-zero
```

The surface is the same `scrumia-extends --claims` as AC-7. With no file named, it walks
the root `CLAUDE.md` and every `apps[].path/CLAUDE.md` that exists, reconciling each
declaration against the file of its own scope — the root file for project-wide
declarations, the app's stub for that app's. A file a caller names is still read on its
own, the way it was: backward compatibility with the surface AC-7 stated, and a way to
audit one file in isolation. The stub is a claim `scrumia-init` wrote, so the
reconciliation covers it the same way it covers the root file: the tool that wrote the
claim is the one that reconciles it.

## Boundary

### AC-8 — Local material without a module is not a malformed module

```gherkin
Given a project whose only local extension is a set of directives and a rules section
  those directives name, with no module of its own anywhere
When the composition is checked and the anatomy checker runs
Then the project is reported as correctly extended, the directives appear in their
  registers, and no finding claims a module is missing or malformed
```

Constructible because both shapes have a stated home: the directives are the project's own
`extends.json` beside its configuration, and the rules section is whatever document a
directive's `read:` names. The anatomy checker is handed no tree here, because there is no
module to hand it — and the directory the configuration sits in is not one, which is the
answer it gives when asked.

### AC-9 — No versioned file names a path outside the project

```gherkin
Given a project running a module from a shared checkout
When every file the repository versions is read
Then the module is keyed `shared:<module>`, so its location is stated by its declaration
  and by nothing beside it, no filesystem path outside the project appears in any
  versioned file, and the path `shared` resolves to comes from `.scrumia/.env.local`
And `.scrumia/.env.local` is excluded from version control
Given that file written the way people write such files — an `export` prefix, spaces
  around the `=`, a quoted value, a trailing space, a comment above it
When resolution reads it
Then the shared location resolves in every one of those cases; and where the file names
  nothing, or names a directory that is not on this machine, that is reported rather than
  read as a location holding no modules
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

### AC-12 — A contract-defined project root is not local material

```gherkin
Given a project holding only contract-defined project roots — a `specs_root` named by
  `scrumia-specs`'s contract and a `design_root` named by `scrumia-design`'s — and no
  directive, no rules section and no skill of its own
When the composition is checked and the anatomy checker runs
Then the project is reported as correctly extended, the contract roots are reported as
  read by the contracts that declare them rather than by this feature's enumeration, and
  no finding names a contract root a malformed module, a malformed directive, or a
  malformed rules section — local material has not been widened to cover it
Given instead the same project holding one directive alongside the contract roots
When the composition is checked
Then the directive is reported under BR-3 as it would be without the contract roots, and
  the contract roots are still reported by their contracts, and the two reports do not
  conflate
```

### AC-13 — The closing vocabulary sentence states the exclusion

```gherkin
Given the closing sentence of `local-extension/business.md`'s Vocabulary
When the file is read end-to-end
Then the sentence names the bounded shapes and states that project-owned material
  declared by another module's contract is not local material, and a reader who knows
  the three shapes alone has the full claim and the full exclusion
```

AC-13 pins the load-bearing closing sentence at line 275 — `scrumia-place` cites it via
the list, not the section title, and any tool that grep-matches the bounding phrase reads
it there.
