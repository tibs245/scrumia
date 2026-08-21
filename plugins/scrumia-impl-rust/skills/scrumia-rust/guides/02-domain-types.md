# Domain Types

> Make invalid states unrepresentable — the type is the authority once its constructor has validated it. The module's organizing principle; everything else follows from it.

## Prerequisites

[01-project-layout](01-project-layout.md) — these types live inside the crate/module structure it defines (a domain's newtypes and entities sit in that domain's crate, never in a shared `models.rs`).

## Rules

### Rule 1: The newtype — validation in the constructor

An amount is an `Amount(u64)`, not a `u64`; an email is an `Email(String)`, not a `String`. The only way to build one goes through a constructor that validates. After that, any function receiving the type knows it is valid — no re-validation anywhere.

#### Correct

```rust
pub struct Email(String);
impl Email {
    pub fn parse(raw: &str) -> Result<Self, EmailError> { /* the only way in */ }
}
// Any function that receives an Email knows it is valid. No re-validation anywhere.
```

---

### Rule 2: The state enum — not booleans

Two booleans make four states, and one of them is usually absurd (paid but not shipped and no payment date, say). An `enum` expresses only the states that actually exist.

#### Correct

```rust
pub enum OrderState {
    Cart { items: Vec<Item> },                    // no payment date here:
    Paid { items: Vec<Item>, at: DateTime },      // it only exists once paid
    Shipped { tracking: TrackingNumber },
}
```

---

### Rule 3: The typestate — when order of operations is the invariant

```rust
pub struct Connection<State>(/* … */, PhantomData<State>);
impl Connection<Unauthenticated> {
    pub fn authenticate(self, token: Token) -> Result<Connection<Authenticated>, AuthError> { /* … */ }
}
impl Connection<Authenticated> {
    pub fn request(&self, /* … */) { /* unreachable before authenticate(): compile error */ }
}
```

To be dosed: the typestate pays off when the order is a safety invariant, not for a form's three states.

---

### Rule 4: Traits for real polymorphism, not for decoupling on principle

A trait earns its place with two living implementers, or a genuine test double need at an infrastructure boundary — not on the promise that a second implementer might show up. When the variants are finite and known, an `enum` and an exhaustive `match` do the job: adding a variant breaks at compile time, which is a help, not a hindrance. See [decisions/D-03](../decisions/D-03-no-single-implementer-traits.md) for the full reasoning against single-implementer traits.

---

### Rule 5: `Deref` is for smart pointers, not for inheritance

`Deref` is for smart pointers. To expose behavior on a domain type: a method or a trait, never `Deref` standing in for an OOP-style "is-a". See [decisions/D-04](../decisions/D-04-no-deref-inheritance.md).

---

### Rule 6: Ownership over defensive `clone()`

A `clone()` is justified by semantics — two legitimate owners — not by a lost fight against the borrow checker. Three clones in the same place signal an ownership structure to rethink, not a style issue to fix line by line. See [decisions/D-02](../decisions/D-02-no-clone-to-appease-borrowck.md).

## Alongside other modules

**`scrumia-solid-principles`** — situated here:
- **O**: prefer closure — `enum` + exhaustive `match` (Rule 4 above) — as long as the variants are known. An assumed restriction of the principle.
- **L**: every `impl` of a trait honors the trait's documented invariants, backed by shared contract tests.
- **I**: thin traits, cut to the consumer's measure.
