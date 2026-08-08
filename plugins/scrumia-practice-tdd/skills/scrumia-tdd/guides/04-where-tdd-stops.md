# Where TDD Does Not Apply

> A practice without limits becomes a reflex. This one stops at three legitimate exits.

## Prerequisites

- [01-the-cycle](01-the-cycle.md) — an exemption is a deliberate exit from the cycle, not a substitute for it.

## Rules

### Rule 1: The spike is exempt, but only until it survives

Exploratory code, declared throwaway in the ticket, does not need a red test first. If it survives — it ships, or the next change builds on it — it becomes code to cover *before* any further change.

### Rule 2: Declarative configuration and trivial glue code are exempt

No logic to constrain means no invariant to protect, and no test to write.

### Rule 3: Visual styling is exempt

A color threshold can't be made into an invariant; the interface's *behavior* can. Test that the error state shows, not the exact shade it shows in.

### Rule 4: Declare the exception the moment you take it, not afterwards

An exemption claimed retroactively — after the code exists, to justify why it wasn't tested — is not an exemption, it's a rationalization. State it in the ticket or the commit at the moment you decide to skip the red test, exactly like the paths listed in `exempt_paths` (see [03-ac-mapping, Settings](03-ac-mapping.md#settings)) are declared in the config, not discovered after the fact.
