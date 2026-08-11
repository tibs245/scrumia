# Business rules — Composer

## Value

For a visitor deciding whether ScrumIA fits their project. It brings the one
place on the site where that visitor acts rather than reads: assembling
their own composition, slot by slot, and leaving with the install commands
and the `.scrumia/config.yaml` their choices produce. It matters because the
modularity claim stated everywhere else on the site is abstract until
someone builds with it — the composer is where "swap a module" stops being a
sentence and becomes something the visitor just did. Measured: not
instrumented today — no analytics track how far a visitor gets through the
six rows or whether they copy an artifact.

Business parent: none beyond the site epic.

App stratum. This feature has no Business parent of its own — it does not
copy `modular-composition`'s rules, it applies them to one screen. Only what
is specific to that application sits here.

## The rules

**Empty is an offered option, never an unasked one.** Every slot carries a
`leave it empty` choice whose description states what the absence costs, in
the voice of `features/business/modular-composition/business.md`'s AC-4:
named degradation, work continuing. No sentence may imply the agents break. A
slot the visitor was never asked must not be emitted as a decided `null` —
which is why `design` is a question here and not a silent default.

**The install claim is the real one.** No one-liner consumes a generated
config; claiming one would be the promise `modular-composition`'s BR-3
forbids modules from making, and the site gets no exemption. What the
composer claims is what is true: commit the file, install the modules, run
`scrumia-init` — which finds an existing `.scrumia/config.yaml` and verifies
it instead of proposing one.
