#!/usr/bin/env python3
"""Acceptance tests for the config schema scrumia-init writes (#257).

Covers features/business/modular-composition/qa.md AC-1, AC-2 and AC-6 at the one
place this repository can check them: the template in
plugins/scrumia-core/skills/scrumia-init/SKILL.md is the schema every consuming
project's .scrumia/config.yaml is written from, so a drift here is the contract
drifting.

Run from the repo root: python3 tools/test_scrumia_init.py
Exit code 0 when everything passes, 1 otherwise. Needs PyYAML.
"""

import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
SKILL = ROOT / "plugins" / "scrumia-core" / "skills" / "scrumia-init" / "SKILL.md"
RETIRED = ("composition:", "implementation:", "practices:")
# ADR-0019 retired `practices` as a slot, not as a settings namespace.
SETTINGS_NS = re.compile(r"settings[.:]?\s*\w*[.\s]*(implementation|practices)")
# Naming a key as gone is the opposite of instructing an agent to write it.
DISOWNED = re.compile(r"retired|deprecat|stale|no longer|old spelling", re.IGNORECASE)
FAILURES: list[str] = []


def check(name: str, ok: bool, detail: str = "") -> None:
    if ok:
        print(f"  ok    {name}")
    else:
        detail = str(detail)
        FAILURES.append(f"{name}{' — ' + detail if detail else ''}")
        print(f"  FAIL  {name}{' — ' + detail if detail else ''}")


def sections(text: str) -> dict[str, str]:
    """The skill split on its own `## ` headings, so a claim can be located."""
    out, current, buf = {}, "", []
    for line in text.splitlines():
        if line.startswith("## "):
            out[current] = "\n".join(buf)
            current, buf = line[3:].strip(), []
        else:
            buf.append(line)
    out[current] = "\n".join(buf)
    return out


def config_template(step3: str) -> dict:
    """The first YAML fence of Step 3 — the config a project is written from."""
    block = re.search(r"```yaml\n(.*?)\n```", step3, re.DOTALL)
    if not block:
        check("Step 3 carries a YAML config template", False, "no ```yaml fence")
        return {}
    try:
        return yaml.safe_load(block.group(1)) or {}
    except yaml.YAMLError as exc:
        check("the config template is valid YAML", False, str(exc))
        return {}


def main() -> int:
    text = SKILL.read_text(encoding="utf-8")
    secs = sections(text)
    step3 = next((v for k, v in secs.items() if k.startswith("Step 3 —")), "")
    check("Step 3 writes .scrumia/config.yaml", bool(step3))
    cfg = config_template(step3)

    print("AC-6 — a practice reaches an app only through that app's own extends")
    apps = cfg.get("apps") or []
    check("the template carries an apps[] list", bool(apps))
    for app in apps:
        name = app.get("name", "?")
        check(f"{name}: carries its own extends list", isinstance(app.get("extends"), list),
              repr(app.get("extends")))
        check(f"{name}: carries no retired per-app key",
              not ({"implementation", "practices"} & set(app)),
              ", ".join(sorted({"implementation", "practices"} & set(app))))
        check(f"{name}: carries a path", bool(app.get("path")))

    # AC-6's falsifiable half: no project-level entry may apply a practice to an app
    # that did not declare it, so a practice module must never sit in the outer list.
    outer = cfg.get("extends") or []
    strays = [m for m in outer if isinstance(m, str) and "-practice-" in m]
    check("no practice module in the project-level extends", not strays, ", ".join(strays))

    print("The composition is declared by naming modules, not by asserting slots")
    check("the template declares extends at project level", isinstance(outer, list))
    check("no composition: slot map survives", "composition" not in cfg)
    check("every extends entry names a module",
          all(isinstance(m, str) and m for m in outer), repr(outer))

    print("AC-1 — a need nobody covers keeps existing, without a placeholder to carry it")
    lists = [outer] + [a.get("extends") or [] for a in apps]
    check("no null placeholder anywhere in extends",
          all(m is not None for lst in lists for m in lst))
    step8 = next((v for k, v in secs.items() if k.startswith("Step 8")), "")
    check("Step 8 states that an uncovered need is reported, not written back into the config",
          "not** a defect" in step8 or "not a defect" in step8)

    print("Migration — the old spelling is read, converted, and given a window")
    migration = next((v for k, v in secs.items() if k.startswith("Step 3b")), "")
    check("a migration step exists", bool(migration))
    for key in RETIRED:
        check(f"the migration names {key}", key in migration)
    check("both spellings keep working for a stated window",
          "release" in migration and "window" in migration)
    check("the conversion is reported, not silent",
          "report" in migration and "silent" in migration)

    print("The retired keys survive nowhere but the migration")
    elsewhere = {h: b for h, b in secs.items() if not h.startswith("Step 3b")}
    for key in RETIRED:
        hits = [f"{h or '(preamble)'}: {l.strip()}"
                for h, b in elsewhere.items() for l in b.splitlines()
                if key in l and not SETTINGS_NS.search(l) and not DISOWNED.search(l)]
        check(f"no live {key} outside the migration", not hits, "; ".join(hits))

    print()
    if FAILURES:
        print(f"{len(FAILURES)} failure(s):")
        for f in FAILURES:
            print(f"  - {f}")
        return 1
    print("all checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
