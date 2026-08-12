#!/usr/bin/env python3
"""Acceptance tests for plugins/scrumia-core/bin/scrumia-extends (#302).

AC-17 and AC-18 of features/business/modular-composition/: a module is declared by
source and a bare name is not a declaration; a setting resolves through three layers
in a stated order.

Run from the repo root: python3 tools/test_scrumia_extends.py
Exit code 0 when everything passes, 1 otherwise. No dependencies beyond the YAML
reader the tool itself needs.
"""

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TOOL = ROOT / "plugins" / "scrumia-core" / "bin" / "scrumia-extends"
FAILURES: list[str] = []


def check(name: str, ok: bool, detail: str = "") -> None:
    if ok:
        print(f"  ok    {name}")
    else:
        detail = str(detail)
        FAILURES.append(f"{name}{' — ' + detail if detail else ''}")
        print(f"  FAIL  {name}{' — ' + detail if detail else ''}")


def config_with(body: str) -> Path:
    handle = tempfile.NamedTemporaryFile("w", suffix=".yaml", delete=False, encoding="utf-8")
    handle.write(body)
    handle.close()
    return Path(handle.name)


def run(args: list[str], config: Path, local: Path | None = None):
    """No harness runs here, so $SCRUMIA_MODULE_DIR stands in for PATH discovery."""
    env = {**os.environ, "SCRUMIA_MODULE_DIR": "plugins", "NO_COLOR": "1",
           "SCRUMIA_CONFIG": str(config)}
    env["SCRUMIA_CONFIG_LOCAL"] = str(local) if local else "/nonexistent/config.local.yaml"
    proc = subprocess.run([str(TOOL), *args], cwd=ROOT, env=env,
                          capture_output=True, text=True, timeout=60)
    return proc.returncode, proc.stdout, proc.stderr


def modules_in(config: Path, register: str = "implement", app: str = "") -> set[str]:
    args = [register, "--json"] + (["--app", app] if app else [])
    code, out, err = run(args, config)
    if code != 0:
        return {f"(exit {code}) {err.strip()}"}
    return {row["module"] for row in json.loads(out)}


def rows_in(config: Path, register: str = "implement") -> list[dict]:
    _, out, _ = run([register, "--json"], config)
    return json.loads(out)


# Every plugin in this repository claims tibs245/scrumia in its manifest, which is what
# a marketplace key is checked against. `local:` and `shared:` name a location no
# manifest can know about, so those match on the module's name alone.
MARKETPLACE = """
project: { name: "Keyed" }
modules:
  "tibs245/scrumia:scrumia-practice-tdd": {}
"""

WRONG_SOURCE = """
project: { name: "Elsewhere" }
modules:
  "acme/other:scrumia-practice-tdd": {}
"""

LOCAL_AND_SHARED = """
project: { name: "Nearby" }
modules:
  "local:scrumia-practice-tdd": {}
  "shared:scrumia-design": {}
"""

BARE_NAME = """
project: { name: "Bare" }
modules:
  "scrumia-practice-tdd": {}
  "tibs245/scrumia:scrumia-design": {}
"""

RETIRED_LIST = """
project: { name: "Retired" }
extends:
  - scrumia-practice-tdd
"""

PER_APP = """
project: { name: "Apps" }
modules:
  "tibs245/scrumia:scrumia-design": {}
apps:
  - name: "web"
    path: "apps/web"
    modules:
      "tibs245/scrumia:scrumia-practice-tdd": {}
"""

CASCADE = """
project: { name: "Cascade" }
settings:
  autonomy:
    level: guided
  team:
    roles: [manager, tech]
modules:
  "tibs245/scrumia:scrumia-specs":
    params:
      root: features
      autonomy:
        level: assisted
  "tibs245/scrumia:scrumia-design": {}
apps:
  - name: "web"
    path: "apps/web"
    modules:
      "tibs245/scrumia:scrumia-specs":
        params:
          root: apps/web/features
"""

CASCADE_LOCAL = """
settings:
  autonomy:
    level: autonomous
modules:
  "tibs245/scrumia:scrumia-specs":
    params:
      root: /tmp/specs
"""


def test_ac17_a_module_is_declared_by_source() -> None:
    print("AC-17 — a module is declared by source, and resolves from what its key names")

    market = config_with(MARKETPLACE)
    check("a marketplace key resolves the module that claims that source",
          "scrumia-practice-tdd" in modules_in(market), modules_in(market))
    rows = rows_in(market)
    check("every row carries the key it was declared by",
          all(r["declared_as"] == "tibs245/scrumia:scrumia-practice-tdd" for r in rows),
          {r["declared_as"] for r in rows})
    check("and the location reported is the one in the key",
          all(r["source"] == "tibs245/scrumia" for r in rows), {r["source"] for r in rows})
    os.unlink(market)

    wrong = config_with(WRONG_SOURCE)
    check("the same name under another marketplace resolves nothing",
          modules_in(wrong) == set(), modules_in(wrong))
    os.unlink(wrong)

    nearby = config_with(LOCAL_AND_SHARED)
    found = modules_in(nearby)
    check("a local: key resolves by name", "scrumia-practice-tdd" in found, found)
    check("a shared: key resolves by name", "scrumia-design" in found, found)
    rows = rows_in(nearby)
    check("each is credited with the location its own key states",
          {r["module"]: r["source"] for r in rows} ==
          {"scrumia-practice-tdd": "local", "scrumia-design": "shared"},
          {r["module"]: r["source"] for r in rows})
    os.unlink(nearby)

    apps = config_with(PER_APP)
    check("an app's own mapping is keyed the same way and reaches only that app",
          modules_in(apps, app="web") == {"scrumia-design", "scrumia-practice-tdd"}
          and modules_in(apps) == {"scrumia-design"},
          (modules_in(apps, app="web"), modules_in(apps)))
    os.unlink(apps)


def test_ac17_a_bare_name_is_not_a_declaration() -> None:
    print("AC-17 — a bare name is reported as such, never resolved against what is installed")

    bare = config_with(BARE_NAME)
    code, out, err = run(["implement", "--json"], bare)
    resolved = {row["module"] for row in json.loads(out)}
    check("the bare name resolves nothing",
          "scrumia-practice-tdd" not in resolved, resolved)
    check("the sourced key beside it still resolves",
          "scrumia-design" in resolved, resolved)
    check("the key is named in the report", "'scrumia-practice-tdd'" in err, err.strip())
    check("and it is called what it is",
          "is not a declaration" in err and "<source>:<module>" in err, err.strip())
    check("an unresolved declaration is not a failure", code == 0, code)
    os.unlink(bare)


def test_ac17_the_retired_list_is_still_read() -> None:
    print("AC-17 — the retired extends: list is read for one more minor, with a warning")

    retired = config_with(RETIRED_LIST)
    code, out, err = run(["implement", "--json"], retired)
    check("its bare names still resolve, since they predate the grammar",
          "scrumia-practice-tdd" in {r["module"] for r in json.loads(out)}, out[:200])
    check("the reader is told to migrate", "migrate to 'modules:'" in err, err.strip())
    check("and is not told its names are malformed",
          "is not a declaration" not in err, err.strip())
    check("reading a retired shape is not a failure", code == 0, code)
    os.unlink(retired)


def test_ac18_a_setting_resolves_through_three_layers() -> None:
    print("AC-18 — settings:, then the module's params:, then the local layer")

    config = config_with(CASCADE)
    key = "tibs245/scrumia:scrumia-specs"

    _, out, _ = run(["--settings"], config)
    base = json.loads(out)
    check("with no module named, the answer is the base layer",
          base == {"autonomy": {"level": "guided"}, "team": {"roles": ["manager", "tech"]}},
          base)

    _, out, _ = run(["--settings", key], config)
    resolved = json.loads(out)
    check("layer 2 overrides layer 1", resolved["autonomy"]["level"] == "assisted", resolved)
    check("what layer 2 does not carry survives from layer 1",
          resolved["team"]["roles"] == ["manager", "tech"], resolved)
    check("and the module's own key is there", resolved["root"] == "features", resolved)

    _, out, _ = run(["--settings", key, "--app", "web"], config)
    scoped = json.loads(out)
    check("an app's params beat the project-wide ones, specific over generic",
          scoped["root"] == "apps/web/features", scoped)

    local = config_with(CASCADE_LOCAL)
    _, out, _ = run(["--settings", key], config, local=local)
    machine = json.loads(out)
    check("layer 3 overrides layer 2", machine["root"] == "/tmp/specs", machine)
    check("layer 3 overrides layer 1 too",
          machine["autonomy"]["level"] == "autonomous", machine)
    check("and it still leaves alone what no layer above it names",
          machine["team"]["roles"] == ["manager", "tech"], machine)

    _, _, err = run(["--settings", key], config, local=local)
    check("the layers that answered are named, not only applied",
          "settings:" in err and key in err and str(local) in err, err.strip())
    os.unlink(local)

    # A key several modules read cannot live inside one module's block: settings.team is
    # written by the team module and by scrumia-design (ADR-0014).
    for other in (key, "tibs245/scrumia:scrumia-design"):
        _, out, _ = run(["--settings", other], config)
        check(f"{other.split(':')[-1]} sees the key that is no module's",
              json.loads(out)["team"]["roles"] == ["manager", "tech"], out[:200])
    os.unlink(config)


def main() -> int:
    if not os.access(TOOL, os.X_OK):
        print(f"error: {TOOL.relative_to(ROOT)} is not executable")
        return 1
    test_ac17_a_module_is_declared_by_source()
    test_ac17_a_bare_name_is_not_a_declaration()
    test_ac17_the_retired_list_is_still_read()
    test_ac18_a_setting_resolves_through_three_layers()
    print(f"\n{len(FAILURES)} failure(s)")
    return 1 if FAILURES else 0


if __name__ == "__main__":
    sys.exit(main())
