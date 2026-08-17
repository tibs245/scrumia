# Angle: api-contract

**Content-tested, both strata.** The file is `api-contract.md`.

## What this angle answers

The shape of anything that crosses a feature or app boundary, and what a consumer
may rely on.

"API" is the narrow reading. If another feature *parses* it, it is a contract —
whatever the transport: an HTTP endpoint, a file format, a YAML schema, a CLI's
output, an event payload, a log line something greps.

Read by: devs, integration, review agents.

## When it activates

**By context.** One yes is enough.

| Question | Default when unsure |
|---|---|
| Does something outside this feature parse output this feature produces? | yes → write it |
| Does this feature parse something another feature produces? | yes → write it, as a consumer |
| Does it define a file format, a schema, or a command's output shape? | yes → write it |
| Is the structure consumed only inside this feature? | no → `tech.md` |

**By configuration.**

```yaml
modules:
  "<source>:scrumia-specs":
    params:
      angles:
        api-contract: context   # always | context | never
```

`context` is the default.

## The questions to explore it

**If this feature produces the contract**

1. What exactly is exposed? Give the schema — OpenAPI, GraphQL, protobuf, JSON
   Schema — or state the shape precisely enough that a consumer can implement
   against it without reading the code.
2. What are the error cases, and what does a consumer see for each?
3. Is there pagination, ordering, or any implicit limit a consumer will hit?
4. What is **stable** and what may change? A contract with no stability statement
   is one every consumer treats as frozen.
5. What happens to existing consumers when it does change — is there a version, a
   deprecation window, a compatibility guarantee?

**If this feature consumes one**

6. Which contract, owned by which feature? Cite it; do not copy it.
7. What assumptions does this feature make about it that the contract does not
   actually guarantee? Those are the assumptions that break silently on the
   producer's next release, and writing them down is this section's whole value.

## Boundary

**Holds** — the exposed schema, error cases, pagination, stability statement, for
a producer; the reference to the producer's contract and the assumptions made
about it, for a consumer.

**May hold** — an example payload, when the schema alone is hard to read.

**Must not hold**
- an internal structure nobody outside the feature consumes → `tech.md`
- a business rule about what the data means → `business.md`
- a copy of the producer's schema, in a consuming feature → cite it

**Must stay in sync with the code.** A diverged contract is worse than an absent
one: it is believed.

## Files

- Template: [`template.md`](template.md)
- Review guard-rails: [`checklist.md`](checklist.md)
