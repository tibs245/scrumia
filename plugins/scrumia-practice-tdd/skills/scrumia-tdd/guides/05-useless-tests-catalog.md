# Useless Tests Catalog

> Seven patterns that pass the suite and protect nothing. For each: the pattern, why it protects nothing, what to write instead. Examples are in pseudo-code — the app's implementation module provides the exact idiom.

## Prerequisites

None — usable standalone as a checklist, and referenced from `scrumia-tdd-audit`'s pass 2.

## Rules

### Rule 1: The tautological test

#### Incorrect

```
mock(payment).charge(100)
service.pay(100)
assert mock(payment).received_charge(100)
```

The test repeats the code line by line. It will pass after any regression in the amount calculation, since it calculates nothing — it verifies a conversation with a mock. See also [02-mock-boundary, Rule 2](02-mock-boundary.md).

**Instead**: test the observable effect. The balance went down, the receipt exists, the state changed.

### Rule 2: The implementation mirror

#### Incorrect

```
assert service.internal_cache.size == 3
```

The test knows the internal structure. Every refactor breaks it while the behavior is intact — the suite raises false alarms, and we stop listening to it.

**Instead**: test through the public API. If an internal invariant deserves a test, it may be a module that deserves an API.

### Rule 3: The test that cannot fail

No assertion, an assertion on a constant, `assert true` after a call "to check it doesn't crash". It inflates coverage and the false sense of security.

**Instead**: if the invariant is "raises no error", write it as such, on inputs that could raise one.

### Rule 4: The default snapshot

A 400-line snapshot fails as soon as a comma moves. We regenerate it without reading it — that's structural, nobody re-reads 400 lines on every commit.

**Instead**: targeted assertions on what matters. The snapshot is reserved for outputs where *every* character is contractual (a file format, a short template render). The one deliberate exception is the golden master used to characterize legacy behavior before a refactor — see `scrumia-tdd-refactor`, temporary by construction.

### Rule 5: The timing-fragile test

#### Incorrect

```
sleep(200); assert done
```

Passes on the developer's machine, fails in CI one day out of five. A flaky test costs more than it earns: it teaches the team to re-run without reading.

**Instead**: inject the clock, wait for a signal rather than a duration. The implementation module says how.

### Rule 6: The shared mutable state

Two tests that read the same mutable fixture pass alone, fail together — in one order, not the other.

**Instead**: each test builds its own world. If that's verbose, a fixture *builder*, not shared state.

### Rule 7: The integration test disguised as a unit test

It goes through the database and three modules, but lives in the fast suite. The "unit" suite takes twelve minutes; we stop running it before every commit — and the red-green cycle dies (see [01-the-cycle, Rule 5](01-the-cycle.md)).

**Instead**: put it where the app's integration tests live, with their own cadence. The cycle's suite stays under a minute.
