# API contract — <feature>

<The contract for any data shared across a feature or app boundary — an HTTP
API, but equally a file format, a YAML schema, a CLI's output shape. Must
stay in sync with the code: a diverged contract is believed. Omit any
section with nothing to say.>

## Exposed schema

<Producing feature only: the schema — OpenAPI, GraphQL, protobuf, JSON
Schema, or the shape stated precisely. An internal structure nobody outside
the feature consumes belongs to `tech.md` instead.>

## Error cases

<Producing feature only: the error cases.>

## Pagination

<Producing feature only, if applicable.>

## Stability

<Producing feature only: what is stable and what may change.>

## Consumed contract

<Consuming feature only: the reference to the producer's contract, and the
assumptions made about it.>
