# Lints and Safety Comments

> The workspace clippy baseline that mechanizes the module's refusals, and the `SAFETY:` comment format for `unsafe`.

## Prerequisites

[04-testing](04-testing.md) — the `unwrap_used` lint below exempts test code; you need to know where tests live to read the exemption correctly.

## Rules

### Rule 1: `unwrap()` and `expect()` are denied outside tests and declared prototypes

Every `unwrap` in production is a panic waiting for its input. In a context where impossibility is proven, `expect("invariant: <why>")` is used instead — the message is the proof. The only exemptions are test code and code explicitly declared a prototype. See [decisions/D-01](../decisions/D-01-no-unwrap-expect.md).

#### Correct

```toml
# Cargo.toml (workspace)
[workspace.lints.rust]
unsafe_op_in_unsafe_fn = "deny"

[workspace.lints.clippy]
unwrap_used = "deny"        # tests are exempt
expect_used = "warn"        # tolerated with an invariant message
dbg_macro = "deny"
todo = "warn"
```

With `clippy: pedantic` in the settings, add `pedantic = { level = "warn", priority = -1 }` and own the dated `allow`s case by case.

---

### Rule 2: `unsafe` isolated, each block preceded by a `SAFETY:` comment

`unsafe` stays in the smallest possible scope. Each block is preceded by a `// SAFETY:` comment stating the invariant guaranteed by the caller. An `unsafe` without a comment is a review rejection — and so is one that states nothing.

#### Correct

```rust
// SAFETY: `indices` comes from `valid_positions()`, which guarantees
// every index < self.data.len(). No mutation between the two calls.
let value = unsafe { self.data.get_unchecked(index) };
```

#### Incorrect

```rust
// SAFETY: it's safe
let value = unsafe { self.data.get_unchecked(index) };
```

The comment states the invariant **and who guarantees it**. "SAFETY: it's safe" is a review rejection just as much as the missing comment.

---

### Rule 3: `#[allow(...)]` is a dated reprieve, not a permanent setting

An `allow` is a dated reprieve with its reason, not a permanent setting. `cargo clippy` with the module's config lists what the `allow`s are masking — each one should be revisited, not accumulated.
