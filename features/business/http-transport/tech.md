# HTTP transport — tech

The plugin at `plugins/scrumia-ktor/` contributes nine refusal rules to
the `implement` register, nine refusal rules to the `review` register,
and one mapping to the `find-spec` register. The mapping covers
eleven keys; the refusal rules cover the eight rule families the issue
names plus the dissociation between HTTP status and effect semantics.

## The register contributions

`plugins/scrumia-ktor/extends.json` is a single JSON object with three
top-level keys: `implement`, `review`, `find-spec`.

- `implement` carries nine refusal rules and one method (`ktor-audit`).
  Every refusal rule has a `type: "refusal"`, a `when: "required"`, a
  one-line `summary`, and a `read` path relative to the module's root
  pointing at the rule file in `rules/`.
- `review` carries nine refusal rules. Each is the review-side form of
  the implement-side rule of the same name — same `read` path, same
  rule family, different wording suited to a reviewer reading a diff.
- `find-spec` carries one entry: the mapping the `ktorspec-finding-keys`
  file declares, with eleven keys. The `read` path points at
  `rules/ktorspec-finding-keys.md`.

A contribution names no consumer. The same `read` path is reached by
`scrumia-extends implement`, `scrumia-extends review` and the
`find-spec` lookup, with no edit to the file at the other end of the
link. The contract is the one `features/business/modular-composition/`
states.

## What the rule files look like

Each `rules/*.md` is a refusal rule with the same shape:

1. **What is refused** — a small code fragment showing the failure mode.
2. **What is written instead** — the code that satisfies the rule.
3. **Why** — the paragraph that names the failure mode the rule
   prevents and the reader who would notice the absence of the rule.
4. **Sources complémentaires** — the URLs the rule cites, with the
   Ktor major version pinned.

The eight rule-family files cover routing, content negotiation, HTTP
client, authentication, test client, server configuration, WebSockets
and SSE, and observability. The ninth file
(`http-status-is-not-effect-semantics.md`) is the dissociation: it
states where the conversion lives and names the conversion's
non-ownership of the typed-error paradigm. The tenth file
(`ktorspec-finding-keys.md`) is the `find-spec` mapping.

## What the audit skill looks like

`skills/ktor-audit/SKILL.md` is a `name: ktor-audit` skill that asks
nine questions, one per rule family, in order, and reports findings
without changing code. Each question is read from the rule file
(`read` field in the corresponding `extends.json` entry) and ends in
a `grep` command the audit can re-run.

The skill's frontmatter `description` is the input the `Agent` tool
sees when matching an invocation: it names the audit's subject
("a Ktor codebase against the nine rule families this module
ships"), its trigger ("before adopting the module on an existing
codebase, when a Ktor-shaped bug ships, or to check a new route
against the rules before review"), and the version pin
("Ktor 3.x"). On a 2.x codebase the audit stops on the version
check and reports the drift — the failure mode the description
is written to prevent.

## How the module is added to a project

`plugins/scrumia-ktor/.claude-plugin/plugin.json` declares the module
name, version, description and keywords. The marketplace
enumerator (`.claude-plugin/marketplace.json`) registers the same
name and version. `site/modules.json` declares the module's emoji
and slot. `site/i18n/{en,fr}/modules/scrumia-ktor.json` carries the
i18n strings the module's page on the site reads.

A project that adopts `scrumia-ktor` lists the module in
`.scrumia/config.yaml` under `modules:` and the rules take effect
on the next `scrumia-extends` call. The module's
`plugins/scrumia-ktor/extends.json` is the single source; a
project that enables the module in its harness and omits the
entry from `extends` (project-wide and per app) gains no rules
— that is the `modular-composition/BR-2` rule.

## The independence

`scrumia-ktor` is the only module whose documents own the Ktor
rules. The eight rule families and the dissociation are stated
once, in `plugins/scrumia-ktor/rules/`, and no other feature's
`business.md` or `qa.md` restates them. A satellite that lands
later (`scrumia-effect`, `scrumia-gradle`,
`scrumia-kotlin-multiplatform-mobile`) will add its own
concerns: effect semantics, build wiring, KMM interop. The
Ktor rules are not theirs, and the audit finds their
violations because the audit reads this module's rules.

The same independence holds in the other direction: this
module's `extends.json` does not reach into any other module's
tree. The `ktorspec-finding-keys.md` mapping names rules by
short name; the rules they name resolve to files under
`plugins/scrumia-ktor/`. The dissociation's `read` field
points at the same module's own rule. The independence is
the contract, and `BR-7` is the gate.
