# scrumia-impl-rust

The implementation slot for Rust: invalid states made unrepresentable, typed errors per
layer, one test per invariant. Plugs in app by app, alongside whichever practice modules
that app also runs.

## What it answers

How Rust gets written in an app that plugs this module in — project layout, domain types,
error handling, testing, lints — as five guides read on demand, plus the refusals a
reviewer checks a PR against.

## What it refuses

- No `unwrap`/`expect` in production code.
- No defensive `.clone()` to route around the borrow checker.
- No trait with a single implementer — that is a struct with an interface in the way.
- No `Deref` used to fake inheritance.

Each is a decision record (`D-01` through `D-04`), not a lint config, because a
reviewer's judgement is what enforces it.

## What it ships

| Skill | Role |
|---|---|
| `scrumia-rust` | The reference — five guides and the four refusals above. Load before writing Rust in an app that extends this module. |
| `scrumia-rust-audit` | Measures the gap between an existing Rust app and these rules: `unwrap` in production, untyped errors, single-implementer traits, unjustified `unsafe`. Reports; rewrites nothing without agreement. |

## Settings it reads

Under `settings.implementation.scrumia-impl-rust` in `.scrumia/config.yaml`:
`test_runner`, `clippy` profile, `coverage_threshold`, `msrv`.

## What it expects to find

An app that lists `scrumia-impl-rust` in its own `extends`; within it, `.rs` files and
`Cargo.toml` are what the guides apply to. An optional
`.scrumia/impl/scrumia-impl-rust.md` records a project's house exceptions without forking
the module.

## Decisions

Four, `D-01` through `D-04` — one per refusal above, for a reviewer who wants the
reasoning rather than just the rule.
