# Business rules — Composer

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
