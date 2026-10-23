# Tech — Web audience measurement

## How the plugin composes

`scrumia-web-audience` ships `extends.json` with two registers, keyed by the register
names themselves; nothing in a contribution names a consumer.

| Register | Module that opens it | Contribution |
|---|---|---|
| `implement` | `scrumia-github-project` (`scrumia-ticket`) | nine refusals, one norm, one optional method |
| `review` | `scrumia-github-project` (`scrumia-review`) | three refusals and one norm |

Each contribution carries `name`, `type`, `when`, `summary` and `read`, the path of the
rule inside the module.

## Where things live

```
plugins/scrumia-web-audience/
├── .claude-plugin/plugin.json
├── README.md
├── CHANGELOG.md
├── extends.json
├── rules/
│   ├── closed-event-catalogue.md
│   ├── one-module-declarative-markup.md
│   ├── cleaned-addresses.md
│   ├── send-to-the-collection-directly.md
│   ├── the-proxy-opens-one-route.md
│   ├── measurement-after-the-page.md
│   ├── production-only-and-browser-signals.md
│   ├── opt-out-that-lasts.md
│   ├── tool-and-database-apart.md
│   └── exemption-conditions.md
├── scripts/detect-direct-tracker-calls.sh
└── skills/web-audience-audit/SKILL.md
```

## The detector

`detect-direct-tracker-calls.sh --module <dir> <root>` lists source files outside the
measurement module that contain the queue's name (`_paq` by default, `--queue` to
change it, or the collection path for a module that sends directly). It reads text, so a queue called through an alias is not found; the audit
says so wherever it reports. Exit codes: `0` clean, `1` tool failure, `2` bad usage,
`3` a file outside the module mentions the queue.

## Versioning

The checklist is a paraphrase dated by the audit: the audit asks when the regulator's
documents were last read, and a project that cannot answer reads them again before the
answers count.
