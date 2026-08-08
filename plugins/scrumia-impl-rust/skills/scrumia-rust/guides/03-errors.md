# Errors

> `Result` at the boundaries, panic on a violated internal invariant — never the other way around. Each layer speaks its own error vocabulary and translates the one from below.

## Prerequisites

[01-project-layout](01-project-layout.md) — "layer" here means a crate or module boundary as defined there (domain vs. infra vs. binary).

## Rules

### Rule 1: `Result` at the boundaries, panic on a violated internal invariant

An invalid input is a normal case (`Err`); a broken internal invariant is a bug (`panic!` with an invariant message). Confusing the two produces either panics in production or `Result`s nobody knows how to handle. This is the same discipline the lints mechanize for `unwrap`/`expect` — see [05-lints](05-lints.md).

---

### Rule 2: Typed errors per layer

Each layer defines its own error enum (`thiserror`) and translates the errors from below — the domain does not leak `sqlx::Error`. `anyhow` is tolerated in the binary (`main`, CLI), never in a library.

#### Correct

```rust
// crates/billing/src/error.rs — the domain layer
#[derive(Debug, thiserror::Error)]
pub enum BillingError {
    #[error("invoice {0} not found")]
    NotFound(InvoiceId),
    #[error("invalid amount: {0}")]
    InvalidAmount(#[from] AmountError),
    #[error("the invoice store failed")]
    Store(#[source] Box<dyn std::error::Error + Send + Sync>), // the cause, opaque
}
```

```rust
// crates/infra/src/persistence/invoices.rs — the infra layer translates
impl InvoiceStore for PostgresStore {
    async fn load(&self, id: InvoiceId) -> Result<Invoice, BillingError> {
        sqlx::query_as(/* … */)
            .fetch_optional(&self.pool).await
            .map_err(|e| BillingError::Store(Box::new(e)))?   // sqlx does not leak
            .ok_or(BillingError::NotFound(id))
    }
}
```

The rule in one sentence: **a layer exposes its own error vocabulary, and translates the one from below**. `#[from]` for errors of the same vocabulary, `#[source]` + translation for those of another.

---

### Rule 3: Never `Box<dyn Error>` or `String` as a public API's error type

The caller can do nothing with either but display it — no `match`, no recovery decision. A public function returns its layer's typed error enum, always.

## With the practices

No cross-cutting practice restricts this guide directly; the "how we test" and "which design principles" contracts each layer's errors follow live in [04-testing](04-testing.md) and [02-domain-types](02-domain-types.md).
