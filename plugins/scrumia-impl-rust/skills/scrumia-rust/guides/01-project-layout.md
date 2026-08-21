# Project Layout

> The workspace tree, how crates are organized by domain, and who may depend on what.

## Prerequisites

None — this is the foundation. Every other guide assumes the crate/module structure defined here.

## Rules

### Rule 1: Workspace from the second deployable unit on

A single crate is the default. Move to a Cargo workspace only once a second deployable unit exists (a second binary, a second service sharing code) — one crate per domain once that domain has become autonomous, not before. Splitting early buys structure nobody needs yet and pays for it in cross-crate ceremony.

#### Correct

A service with two domains, once it has earned the split:

```
api/
├── Cargo.toml                 # [workspace] from the 2nd deployable unit on
├── crates/
│   ├── billing/                # one crate per domain that has become autonomous
│   │   ├── src/
│   │   │   ├── lib.rs          # declarations + chosen re-exports, nothing else
│   │   │   ├── amount.rs       # the domain's newtypes
│   │   │   ├── invoice.rs      # entities + invariants + `mod tests` at the bottom
│   │   │   └── error.rs        # THIS crate's error enum (thiserror)
│   │   └── tests/               # integration: public API only
│   │       └── invoice_lifecycle.rs
│   └── infra/
│       └── src/
│           ├── persistence/    # implements the domain's contracts
│           └── http/
└── src/
    └── main.rs                 # the binary: wiring, config, anyhow tolerated here
```

---

### Rule 2: Modules by domain, not by technical kind

Modules are named after what the code is about (`billing/`, `catalog/`), never after what kind of code it is. A catch-all `models.rs`, `helpers.rs`, or `utils.rs` at the top of the tree is a module with no reason to change on its own — everything changes it.

#### Correct

```
src/
  billing/
  catalog/
```

#### Incorrect

```
src/
  models.rs
  helpers.rs
  utils.rs
```

---

### Rule 3: Thin `lib.rs`

`lib.rs` holds module declarations and chosen re-exports — nothing else. Logic lives in the modules it declares, never in the crate root.

---

### Rule 4: Dependency direction between layers

Who is not allowed to depend on what: `billing` never depends on `infra`. `infra` depends on `billing` (it implements its contracts). The binary depends on both and does the wiring. This direction is what makes the domain testable without a database, a network, or a filesystem.

## Alongside other modules

**`scrumia-solid-principles`** — situated here:
- **S** applies to the module and the crate.
- **D**: at infrastructure boundaries only — the layering in Rule 4 above. Between modules of the same crate, the direct call is the rule and indirection a refusal (see [decisions/D-03](../decisions/D-03-no-single-implementer-traits.md)).
