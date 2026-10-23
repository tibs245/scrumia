# The tool and its database are apart from the application

*Refusal.* An analytics tool that shares a database, a role or a network path with the
application, reaches out of the host, or has its administration on the Internet.

## What is refused

- The tool's schema in the application's database. A role of the application that reads
  everything (a pooled "read all data" membership, a superuser) then reads the
  measurement too, and an application exposed to the Internet can join measured visits
  to accounts. That join is the cross-referencing the exemption forbids.
- A tool that calls out: version checks, telemetry, remote lists, a geolocation service.
- An administration interface published beside the collection.
- Retention left to the tool's good will.

## What is written instead

- **Its own database**, owned by an administrative role, `CONNECT` withdrawn from
  everyone, granted to the tool's role only; the tool's role is a plain login with no
  membership and no right on the application's database, and the application's roles
  have no line allowing them to join the tool's. If the same database server is
  backed up as a whole, say it: separation does not keep the rows out of the backups.
- **No outgoing call.** The tool's switches for telemetry, update checks and private
  mode are on (Umami: `DISABLE_TELEMETRY`, `DISABLE_UPDATES`, `PRIVATE_MODE`), and a
  measured check in the environment where it runs proves nothing leaves.
- **The administration is published on a private network only** (a VPN interface),
  every account has two-factor authentication, and the default account's password is
  replaced at provisioning. The public route is the collection alone
  (`the-proxy-opens-one-route.md`).
- **A reading role for dashboards**, read-only by default, with `SELECT` on the single
  table it needs and nothing else; the specification says that such a source still
  reads rows, the computed identifier included, and states who may open it.
- **Retention is a job the project owns.** Where the tool has no retention setting
  (Umami has none), a scheduled purge deletes events past the stated duration, then
  the sessions with no event left, and empties the tables the project does not use
  (identified-visitor data and links); it is tested against a copy.
- **The secret that enters the identifier's calculation never rotates.** Changing it
  cuts the counts in two; the monthly change of the identifier comes from the tool's
  salt rotation, not from the secret.
- **The image is pinned by digest**, pulled by the deployment and never by the running
  unit, and a new version means reading the tool's schema and environment again.

## Why

Separation is the guarantee that the measurement stays a count. Where one role can read
both, the guarantee is a promise, and the next feature will keep it only by luck.
