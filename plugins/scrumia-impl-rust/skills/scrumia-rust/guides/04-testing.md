# Testing

> One test per invariant, not per function. The compiler is the first test suite — don't test what a type already guarantees.

## Prerequisites

[02-domain-types](02-domain-types.md) — an invariant encoded in a type needs no runtime test. [03-errors](03-errors.md) — error paths are invariants like any other, and get named tests.

## Rules

### Rule 1: One test per invariant, not per function

The test name states the invariant: `rejects_an_expired_token`, not `test_verify_token`. If the project writes acceptance criteria, the `AC-n` appears in the name or in an adjacent comment.

#### Correct

```rust
// In the module: the named invariant, the AC cited if the project writes them
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn rejects_an_expired_token() { // AC-3
        let token = Token::expired_for(Duration::from_secs(1));
        assert!(matches!(verify(&token), Err(AuthError::Expired)));
    }
}
```

---

### Rule 2: Unit tests live in the module

`#[cfg(test)] mod tests` — they are allowed to see private items, that is their advantage over everything else.

---

### Rule 3: Integration tests live in `tests/`, public API only

If an integration scenario needs private access, it is the API that is incomplete — not a reason to reach into the crate's internals from `tests/`.

---

### Rule 4: `proptest` where the input space is large

Parsing, serialization, domain arithmetic. A hand-written nominal case proves nothing about an input space; a property does.

#### Correct

```rust
// Property: where the input space is large
proptest! {
    #[test]
    fn parse_then_display_is_identity(raw in "[a-z]{1,20}@[a-z]{1,10}\\.[a-z]{2,4}") {
        let email = Email::parse(&raw).unwrap(); // unwrap OK: we are in a test
        prop_assert_eq!(email.to_string(), raw);
    }
}
```

---

### Rule 5: The compiler is the first test suite

An invariant encoded in a type (see [02-domain-types](02-domain-types.md)) needs no runtime test — don't test what the type system already guarantees. A test that only re-checks a constructor's own validation is redundant with the constructor.

---

### Rule 6: Inject the clock and randomness

The clock and randomness are injected (a `now: DateTime` parameter or a `Clock` trait at the boundary) — a test that depends on the system time will fail on a February 29th.

## With the practices

**`scrumia-practice-tdd`** — the cycle is tooled with `cargo test` (or `cargo nextest run`, depending on `test_runner`). Rust particularity: red has **two legitimate forms** — the test that fails, and the test that **does not compile yet** because the type or the signature does not exist. Writing the signature to make the test compile is already the green step beginning. `proptest` properties enter the cycle like any other test: the property first, red, then the implementation.
