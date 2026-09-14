# Test Levels

> Three levels, named so a cadence can name them. What a test *needs to run* decides which level it lives in; what it *asserts* decides which level should hold the invariant.

## Prerequisites

- [01-the-cycle](01-the-cycle.md) — the cycle's suite is the unit level, and its time budget is Rule 5's.
- [02-mock-boundary](02-mock-boundary.md) — the unit level's doubles stand exactly where that guide puts them, and nowhere else.

## Rules

### Rule 1: Three levels, each defined by what it needs and what it asserts

| Level | Needs to run | Asserts | Speed expectation |
|---|---|---|---|
| **Unit** | Test doubles only. No external functionality: no network, no database, no broker, no real clock. | **As much as possible** — every condition and every behaviour of every function, class and component. Very technical tests. | The whole suite of an app in minutes, so it runs all the time. |
| **Integration** | Minimal real services — a real database, a real broker — on a reduced scope. | **States and correct integration**: an adapter against its real service (SQL, constraints, row-level security, migrations, messaging), a route or a screen against the layers under it. | Minutes, often behind a shared lock. Run by impact. |
| **End-to-end** | A complete infrastructure, temporary or permanent: server, workers, storage, broker, and a driven client. | **Global journeys**, from the user's point of view, playing the scenarios the product was designed around. | Tens of minutes or more. May be non-deterministic when a third-party model or provider sits in the path. |

A level is a place with a cadence, not a folder name. Two tests asserting the same thing at different cost belong to different levels.

### Rule 2: What a test needs decides its level, because cadence follows cost

The two axes disagree more often than they agree, and the tie-break is always the same: **the level is decided by what the test needs to run.**

The case that makes this concrete: a screen rendered in an in-process simulator against fake state, a route exercised on an in-memory HTTP engine against fake ports. By purpose both test the integration of a page or of a route. By what they need, both are unit tests — offline, deterministic, fast. **They stay in the unit suite**, because they keep the cycle fast and the per-ticket cadence already covers them, and they are **counted apart in the audit as *in-process integration*** so nobody reads them as proof that a real route or a real screen was exercised.

The reverse case is the same rule run backwards: a test that needs a real database is an integration test even when all it asserts is a calculation. Move the calculation out of the reach of the database rather than move the test.

### Rule 3: Route the invariant before writing the test

At the cycle's red step, the invariant about to be tested names its own level:

- A calculation, a branch, a state transition, an error case, a validation rule → **unit**. If it can only be reached through a real service, the split of the code is the problem, per [02-mock-boundary](02-mock-boundary.md)'s corollary.
- What a query returns, what a constraint refuses, what a migration leaves behind, what a transaction isolates, what a message carries across a real broker → **integration**. A unit test cannot fail on these, whatever it asserts, so it may not hold them.
- A screen's states against a real view model, a route against its real handlers and its real storage → **integration by purpose**; Rule 2 decides where it lives, and the choice is stated rather than left to the reader.
- A journey a user or a scenario walks across several screens, services and turns → **end-to-end**.
- An acceptance criterion is covered **at the lowest level where it can fail** — the rule and its consequence for the AC → test link are in [03-ac-mapping, Rule 4](03-ac-mapping.md).

### Rule 4: Writing a unit test

One behaviour per test, and every branch of a condition. Doubles stand at the owned ports and nowhere else. A test that would still pass with the condition inverted is a hole, whatever it covers. The suite stays inside the cycle's time budget ([01-the-cycle, Rule 5](01-the-cycle.md)) — that budget is what makes the level worth having.

### Rule 5: Writing an integration test

Real service, minimal scope.

- **Isolate the resource that is actually shared, not the one that is easy to copy.** Name which resource is isolated and which is not, in the log line as much as in the test's setup: a working copy per worker isolates *files*, and leaves a database server's connection budget shared server-wide. A message claiming isolation is a guard that guards nothing.
- **Clean up in an order that does not depend on test execution order.** A suite that is green in one order and red in another is red — the order that passes is the accident.
- **Prove the test by mutating the data, not the code under test.** Remove the row, violate the constraint, drop the message: an integration test that stays green through that asserts nothing about the service it pays for.

### Rule 6: Writing an end-to-end test

Scenarios come from the product's scenario documents, not from the implementation — a journey derived from the code tests that the code does what it does. Non-deterministic or paid dependencies, a model provider among them, are either recorded or run on demand, outside any blocking gate.

**A project may declare end-to-end automation deferred** — until the product's interactions stabilise, for instance — and keep a manual walk in the meantime. The declaration is made **up front and dated**, exactly like [04-where-tdd-stops, Rule 4](04-where-tdd-stops.md)'s exemptions: it is written before the journeys it excuses exist, it names what would lift it, and it is never discovered by an audit. A deferral whose declaration is younger than the code it covers is a rationalisation, not a deferral, and the audit reports it as a finding.

### Rule 7: The cadence is not this guide's

Which level runs at which moment — inside the cycle, at a gate, at the end of a batch — is the project's development-flow rule. This guide defines the levels so that a cadence can name them; it states no moment of its own, and a project's flow states no definition of its own. Neither restates the other.

## Settings

Under this module's own `params:` in `.scrumia/config.yaml`, beside the key of the app
that lists it:

```yaml
apps:
  - name: server
    modules:
      "tibs245/scrumia:scrumia-tdd":
        params:
          levels:
            unit:        { command: "<the app's own command>" }
            integration: { command: "<…>", lock: "<shared resource this suite takes>" }
            e2e:         { command: "<…>", deferred_since: "", deferred_until: "" }
          impact:                      # which integration tests a changed path reaches
            - paths: ["server/storage/**", "server/migrations/**"]
              integration: "<selector for that suite's subset>"
            - paths: ["server/http/**"]
              integration: "<…>"
```

Read the effective value through `scrumia-extends --settings`, never out of the file.

Every command here is **the project's**, never this module's: no skill and no guide of this
module carries a stack's test command, and an app that declares none has no level this
module can run for it — which is a finding to report, not a command to guess.

`levels.*.command` names how each level is run. `levels.integration.lock` names the
resource that suite takes server-wide, so a caller can serialise on the right thing
(Rule 5). `levels.e2e.deferred_since` carries the date of Rule 6's declaration, empty when
none was made; a deferral with no date is not one.

`impact` maps changed paths to the integration tests they reach. It is project data
because only the project knows its own test filters. **A path matched by no row means the
whole integration suite**, not none: a mapping that is silent about a path has not
answered for it. What a gate does with this answer — which moment runs which level, and
what a skipped level owes the report — belongs to the project's development flow, per
Rule 7.
