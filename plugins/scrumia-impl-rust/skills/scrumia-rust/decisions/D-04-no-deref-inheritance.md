# D-04: No `Deref` to simulate inheritance

**Status**: Adopted
**Date**: 2026-08-07
**Impacts**: [guides/02-domain-types.md](../guides/02-domain-types.md)

## Context

Implementing `Deref`/`DerefMut` on a domain newtype gives it every method of the wrapped type for free, without a line of forwarding code — which is exactly the appeal, and exactly the problem: it is auto-conversion pretending to be an API surface.

## Arguments For

- `Deref` is designed for smart pointers (`Box`, `Rc`, `Vec`'s slice access) — types whose whole point is transparent access to what they wrap.
- Used on a domain newtype, it silently exposes the wrapped type's entire method set, including operations the newtype's constructor was specifically written to prevent from being reached uncontrolled.
- Method resolution through `Deref` is implicit and easy to miss on review — a caller can end up calling a method that was never meant to be part of the type's contract.
- To expose behavior deliberately: a method or a trait, both of which show up explicitly at the call site and in the type's documented surface.

## Arguments Against (trade-offs accepted)

- `Deref` does remove real boilerplate for a newtype that forwards most of its wrapped type's methods — without it, each forwarded method needs its own explicit function.
- Accepted cost: that forwarding boilerplate is written anyway, because the newtype's whole justification (see [02-domain-types](../guides/02-domain-types.md)) is being a distinct type with its own authority — not a transparent alias for the type it wraps.

## Verdict

`Deref`/`DerefMut` stay reserved for actual smart-pointer types. Domain newtypes expose behavior through methods or traits, even when that means writing a bit of forwarding boilerplate by hand.
