# Local tracking

**Status**: draft

## In brief

The address of a tracker store that lives outside the project's
repository, the git plumbing that resolves it from every linked
worktree, and the lock primitive that serialises writes against a
sprint's concurrent executions. The first of six sub-issues of the
`scrumia-tracker-local` design epic; it answers the *no lock*
mechanism of [ADR-0008](../../../docs/adr/0008-state-lives-in-github.md)
and defers nothing.

## Links

- Implemented by: no App — the epic produces no app, the store is the
  implementation. App features follow under their own tickets.
- Defers to: [ADR-0008](../../../docs/adr/0008-state-lives-in-github.md)
  for the rule that nothing in the repo describes a state that moves,
  and for the three-mechanism gate this epic obeys; the local tracker
  holds to the rule by sitting outside the repository, and this
  feature states how.
- Defers to: [ADR-0013](../../../docs/adr/0013-tracker-stays-one-slot.md)
  for the slot the local tracker fills; the epic's closing ADR
  extends it for a composition that decides the tracker slot is
  replaceable.
- Authority: [`docs/adr/0008-state-lives-in-github.md`](../../../docs/adr/0008-state-lives-in-github.md)
  for the prohibition, [`features/business/local-extension/`](../local-extension/)
  for the cascade-of-three-layers the store's address slots into
  (`.scrumia/config.local.yaml` is layer 3).
- Consumed by: the sister sub-issues of the same epic — the store
  address is a parameter the ticket-file record and the index each
  read, and the lock discipline this feature mandates is what lets the
  ticket-file record keep its log in-file. The consumer relationship
  is named at the epic boundary, not by feature-level citations that
  would replicate what the sibling sub-issues declare themselves.

## Files present

| File | Read it when |
|---|---|
| `business.md` | Deciding whether the local tracker is the right shape for a project, and what the separation of repository and state costs the operator |
| `tech.md` | Resolving the store from inside a linked worktree, taking the lock, and arbitrating the rare failure modes |
| `qa.md` | Checking this feature's acceptance criteria |
| `CHANGELOG.md` | History of changes to this spec |

No `ux.md`: nothing a person looks at is produced here — the store has
no interface. No `archi.md`: the EPIC touches no app, the cross-app
coordination that would justify it is absent. No `api-contract.md`:
no consumer outside this feature parses its contents yet; the
sibling sub-issues each carry their own record shape. No `legal.md`:
ticket files contain no personal data. No `security.md`: the lock
and the one-machine precondition are the threat model, and they live
in `tech.md` rather than as a separate angle. No `devx.md`: no
exposed surface for a consuming feature to read today.
