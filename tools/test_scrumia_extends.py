#!/usr/bin/env python3
"""Acceptance tests for plugins/scrumia-core/bin/scrumia-extends (#302, #291).

AC-17 and AC-18 of features/business/modular-composition/: a module is declared by
source and a bare name is not a declaration; a setting resolves through three layers
in a stated order.

AC-1..AC-5, AC-9 and AC-10 of features/business/local-extension/: each source resolves
from its own location, resolution states which, and one declaration answered by two
distinct modules is a conflict that binds neither.

Run from the repo root: python3 tools/test_scrumia_extends.py
Exit code 0 when everything passes, 1 otherwise. No dependencies beyond the YAML
reader the tool itself needs.
"""

import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TOOL = ROOT / "plugins" / "scrumia-core" / "bin" / "scrumia-extends"
MODULE_TOOL = ROOT / "plugins" / "scrumia-core" / "bin" / "scrumia-module"
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


def run(args: list[str], config: Path, local: Path | None = None, shared: Path | None = None):
    """No harness runs here, so $SCRUMIA_MODULE_DIR stands in for PATH discovery.

    $SCRUMIA_SHARED_DIR is pinned on every call, empty unless a test names one: a
    developer's own machine may carry it, and a test that inherited it would pass or
    fail on whose machine it ran.
    """
    env = {**os.environ, "SCRUMIA_MODULE_DIR": "plugins", "NO_COLOR": "1",
           "SCRUMIA_CONFIG": str(config), "SCRUMIA_SHARED_DIR": str(shared) if shared else ""}
    env["SCRUMIA_CONFIG_LOCAL"] = str(local) if local else "/nonexistent/config.local.yaml"
    proc = subprocess.run([str(TOOL), *args], cwd=ROOT, env=env,
                          capture_output=True, text=True, timeout=60)
    return proc.returncode, proc.stdout, proc.stderr


def make_module(root: Path, name: str, repo: str | None = None,
                register: str = "implement") -> Path:
    """The smallest tree the tool recognises as a module, contributing one directive."""
    (root / ".claude-plugin").mkdir(parents=True, exist_ok=True)
    manifest: dict = {"name": name, "version": "0.1.0"}
    if repo:
        manifest["repository"] = f"https://github.com/{repo}"
    (root / ".claude-plugin" / "plugin.json").write_text(json.dumps(manifest), encoding="utf-8")
    (root / "extends.json").write_text(json.dumps({register: [{
        "name": f"Directive of {name}", "type": "norm", "when": "required",
        "summary": "what the fragment says", "read": "README.md"}]}), encoding="utf-8")
    (root / "README.md").write_text(f"# {name}\n\nA module.\n", encoding="utf-8")
    return root


def project_with(body: str) -> Path:
    """A throwaway project directory, so `.scrumia/modules/` and `.scrumia/.env.local`
    resolve beside the configuration the way they do in a real one."""
    project = Path(tempfile.mkdtemp(prefix="scrumia-project-"))
    (project / ".scrumia").mkdir()
    (project / ".scrumia" / "config.yaml").write_text(body, encoding="utf-8")
    return project


def modules_in(config: Path, register: str = "implement", app: str = "") -> set[str]:
    args = [register, "--json"] + (["--app", app] if app else [])
    code, out, err = run(args, config)
    if code != 0:
        return {f"(exit {code}) {err.strip()}"}
    return {row["module"] for row in json.loads(out)}


def rows_in(config: Path, register: str = "implement") -> list[dict]:
    _, out, _ = run([register, "--json"], config)
    return json.loads(out)


# Every plugin here claims tibs245/scrumia, which is what a marketplace key is checked
# against; `local:` and `shared:` have directories of their own and are answered by neither.
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
  ":scrumia-specs": {}
  "github:scrumia-teams": {}
  "tibs245/scrumia:scrumia-design": {}
"""

EMPTY_MAPPING = """
project: { name: "Declared nothing" }
modules: {}
"""

APP_ONLY_PARAMS = """
project: { name: "App only" }
modules: {}
apps:
  - name: "web"
    path: "apps/web"
    modules:
      "tibs245/scrumia:scrumia-specs":
        params:
          root: apps/web/features
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
    check("a local: or shared: key is not answered by a marketplace module of that name",
          modules_in(nearby) == set(), modules_in(nearby))
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
    check("a key whose source half is missing is refused too",
          "':scrumia-specs' is not a declaration" in err, err.strip())
    check("a source outside the three BR-13 enumerates is refused",
          "'github:scrumia-teams' is not a declaration" in err, err.strip())
    check("an unresolved declaration is not a failure", code == 0, code)
    os.unlink(bare)


def test_a_composition_declaring_nothing_does_not_look_correct() -> None:
    print("A composition that declares no module is said to be empty, not merely unextended")

    empty = config_with(EMPTY_MAPPING)
    code, out, err = run(["implement"], empty)
    check("the empty composition is named on stderr",
          "declares no module" in err, err.strip())
    # An empty table means two different things and only one of them is fine; the
    # report has to say which, or the emptiest composition reads as a correct run.
    check("and the report says the project runs no module, not that the register is quiet",
          "runs no module at all" in out, out)
    check("it is still not a failure", code == 0, code)
    os.unlink(empty)

    # The contrast: modules declared, none contributing to this register.
    quiet = config_with(MARKETPLACE)
    _, out, _ = run(["convene"], quiet)
    check("a register nothing extends still answers that it is open",
          "Nothing extends `convene`" in out and "runs no module at all" not in out, out)
    os.unlink(quiet)


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

    # The provenance is the one output whose whole job is to make the cascade
    # checkable, so it must name what answered and never what merely exists.
    _, _, err = run(["--settings", key], config)
    check("a layer that carried nothing is not claimed",
          "config.local" not in err and "nonexistent" not in err, err.strip())

    app_only = config_with(APP_ONLY_PARAMS)
    _, out, err = run(["--settings", key], app_only)
    check("params reachable only through an app are not claimed without --app",
          "params: of" not in err, err.strip())
    check("and they are absent from the answer, matching what was claimed",
          json.loads(out) == {}, out)
    _, out, err = run(["--settings", key, "--app", "web"], app_only)
    check("with the app named, the layer is both applied and reported",
          json.loads(out) == {"root": "apps/web/features"} and "in app web" in err,
          (out, err.strip()))
    os.unlink(app_only)

    # A key several modules read cannot live inside one module's block: settings.team is
    # written by the team module and by scrumia-design (ADR-0014).
    for other in (key, "tibs245/scrumia:scrumia-design"):
        _, out, _ = run(["--settings", other], config)
        check(f"{other.split(':')[-1]} sees the key that is no module's",
              json.loads(out)["team"]["roles"] == ["manager", "tech"], out[:200])
    os.unlink(config)


THREE_LOCATIONS = """
project: { name: "Three" }
modules:
  "tibs245/scrumia:scrumia-practice-tdd": {}
  "shared:acme-conventions": {}
  "local:acme-docs-rules": {}
"""

ABSENT_SHARED = """
project: { name: "Fresh clone" }
modules:
  "shared:acme-conventions": {}
"""

CONFLICTING = """
project: { name: "Conflict" }
extends:
  - acme-conventions
"""

SHADOWED = """
project: { name: "Promoting" }
modules:
  "shared:scrumia-practice-tdd": {}
"""

PROJECT_DIRECTIVE = """
project: { name: "No module at all" }
modules: {}
"""


def test_ac1_ac2_each_source_resolves_from_its_own_location() -> None:
    print("AC-1, AC-2 — a shared checkout and a module inside the project reach the table")

    project = project_with(THREE_LOCATIONS)
    shared = Path(tempfile.mkdtemp(prefix="scrumia-shared-"))
    make_module(shared / "acme-conventions", "acme-conventions")
    make_module(project / ".scrumia" / "modules" / "acme-docs-rules", "acme-docs-rules")

    config = project / ".scrumia" / "config.yaml"
    _, out, _ = run(["implement", "--json"], config, shared=shared)
    rows = json.loads(out)
    by_module = {r["module"]: r for r in rows}
    check("the shared checkout's directive is in the table",
          "acme-conventions" in by_module, sorted(by_module))
    check("the in-project module's directive is in the table",
          "acme-docs-rules" in by_module, sorted(by_module))
    check("a marketplace module beside them still resolves",
          "scrumia-practice-tdd" in by_module, sorted(by_module))
    check("nothing distinguishes the three rows but the location reported alongside them",
          {m: r["location"] for m, r in by_module.items()} ==
          {"acme-conventions": "shared", "acme-docs-rules": "local",
           "scrumia-practice-tdd": "marketplace"},
          {m: r["location"] for m, r in by_module.items()})

    # BR-6: the path is per-machine and reaches the tool through the environment, so the
    # file naming it is interchangeable with the variable and neither is versioned.
    (project / ".scrumia" / ".env.local").write_text(
        f"# this machine\nSCRUMIA_SHARED_DIR={shared}\n", encoding="utf-8")
    _, out, _ = run(["implement", "--json"], config)
    check("the same answer when the path comes from .scrumia/.env.local instead",
          "acme-conventions" in {r["module"] for r in json.loads(out)}, out[:200])

    shutil.rmtree(project)
    shutil.rmtree(shared)


def test_ac3_resolution_states_where_each_module_came_from() -> None:
    print("AC-3 — every declared module is shown with the location it resolved from")

    project = project_with(THREE_LOCATIONS)
    shared = Path(tempfile.mkdtemp(prefix="scrumia-shared-"))
    make_module(shared / "acme-conventions", "acme-conventions")
    make_module(project / ".scrumia" / "modules" / "acme-docs-rules", "acme-docs-rules")
    config = project / ".scrumia" / "config.yaml"

    _, out, _ = run(["--modules", "--json"], config, shared=shared)
    reported = {row["key"]: row for row in json.loads(out)}
    check("every declaration is reported", len(reported) == 3, sorted(reported))
    check("each carries the location it resolved from",
          {k: r["location"] for k, r in reported.items()} ==
          {"tibs245/scrumia:scrumia-practice-tdd": "marketplace",
           "shared:acme-conventions": "shared", "local:acme-docs-rules": "local"},
          {k: r["location"] for k, r in reported.items()})
    check("and the directory it resolved to",
          all(len(r["roots"]) == 1 and r["state"] == "resolved" for r in reported.values()),
          reported)
    shutil.rmtree(project)
    shutil.rmtree(shared)

    # AC-6's half of the same rule: no location a clone can reach, so no root — and the
    # report must still say which location it would have come from.
    fresh = project_with(ABSENT_SHARED)
    code, out, _ = run(["--modules", "--json"], fresh / ".scrumia" / "config.yaml")
    absent = json.loads(out)[0]
    check("a module the machine cannot reach is a declared absence, not a blank",
          absent["state"] == "absent" and absent["location"] == "shared"
          and absent["roots"] == [], absent)
    check("and reading a composition with one is not a failure", code == 0, code)
    shutil.rmtree(fresh)


def test_ac4_a_local_module_is_held_to_the_same_standard() -> None:
    print("AC-4 — the anatomy checker returns the same verdict wherever the module sits")

    published = Path(tempfile.mkdtemp(prefix="scrumia-published-"))
    make_module(published / "acme-conventions", "acme-conventions")
    # A finding every module can produce: the README carries none of the three sections.
    project = project_with(THREE_LOCATIONS)
    inside = project / ".scrumia" / "modules" / "acme-conventions"
    inside.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(published / "acme-conventions", inside)

    verdicts = []
    for where in (published / "acme-conventions", inside):
        proc = subprocess.run([str(MODULE_TOOL), "check", str(where), "--json"],
                              capture_output=True, text=True, timeout=60)
        verdicts.append((proc.returncode, json.loads(proc.stdout)["findings"]))
    check("the same tree produces findings at all", verdicts[0][1] != [], verdicts[0])
    check("and the identical verdict from both locations, with no local allowance",
          verdicts[0] == verdicts[1], verdicts)
    shutil.rmtree(project)
    shutil.rmtree(published)


def test_ac5_one_declaration_two_modules_is_a_conflict() -> None:
    print("AC-5 — two distinct modules answering one declaration bind neither")

    project = project_with(CONFLICTING)
    shared = Path(tempfile.mkdtemp(prefix="scrumia-shared-"))
    make_module(shared / "acme-conventions", "acme-conventions")
    make_module(project / ".scrumia" / "modules" / "acme-conventions", "acme-conventions")
    config = project / ".scrumia" / "config.yaml"

    code, out, err = run(["implement", "--json"], config, shared=shared)
    check("neither is used — no directive of that module reaches the register",
          json.loads(out) == [], out[:200])
    check("the conflict is named, with both locations",
          "acme-conventions" in err and "shared" in err and "local" in err, err.strip())
    check("the shortened table is not the only signal",
          "binds neither" in err, err.strip())
    check("and it does not stop the composition being read", code == 0, code)

    _, out, _ = run(["--modules", "--json"], config, shared=shared)
    row = json.loads(out)[0]
    check("--modules reports it as a conflict naming every root",
          row["state"] == "conflict" and len(row["roots"]) == 2, row)

    code, _, err = run(["--check"], config, shared=shared)
    check("the dependency check exits non-zero on it", code != 0, code)
    check("and says what is unmet", "unmet dependency" in err, err.strip())
    shutil.rmtree(project)
    shutil.rmtree(shared)


def test_ac5_identity_and_declaration_settle_the_other_two_cases() -> None:
    print("AC-5 — one module reached twice, and an undeclared copy, are not conflicts")

    project = project_with(CONFLICTING)
    shared = Path(tempfile.mkdtemp(prefix="scrumia-shared-"))
    make_module(shared / "acme-conventions", "acme-conventions")
    (project / ".scrumia" / "modules").mkdir(parents=True)
    (project / ".scrumia" / "modules" / "acme-conventions").symlink_to(
        shared / "acme-conventions", target_is_directory=True)
    config = project / ".scrumia" / "config.yaml"

    _, out, err = run(["--modules", "--json"], config, shared=shared)
    row = json.loads(out)[0]
    check("two routes to one directory are one module, resolved and used",
          row["state"] == "resolved" and len(row["roots"]) == 1, row)
    check("and nothing is called a conflict", "binds neither" not in err, err.strip())
    shutil.rmtree(project)
    shutil.rmtree(shared)

    # The promotion case: the published module is installed and a checkout of it is
    # declared. module-authoring BR-3 is only affordable if that is not a fault.
    promoting = project_with(SHADOWED)
    checkout = Path(tempfile.mkdtemp(prefix="scrumia-shared-"))
    make_module(checkout / "scrumia-practice-tdd", "scrumia-practice-tdd")
    _, out, err = run(["--modules", "--json"], promoting / ".scrumia" / "config.yaml",
                      shared=checkout)
    row = json.loads(out)[0]
    check("the declared checkout resolves while the published copy is simply not run",
          row["state"] == "resolved" and row["location"] == "shared"
          and row["roots"][0]["root"].startswith(str(checkout.resolve())), row)
    check("and no conflict is reported", "binds neither" not in err, err.strip())
    shutil.rmtree(promoting)
    shutil.rmtree(checkout)


def test_ac9_ac10_no_versioned_path_and_no_installation() -> None:
    print("AC-9, AC-10 — the machine's path is not versioned, and a directive needs no module")

    gitignore = (ROOT / ".gitignore").read_text(encoding="utf-8").splitlines()
    check("the file naming the shared directory is excluded from version control",
          ".scrumia/.env.local" in [line.strip() for line in gitignore], gitignore)

    project = project_with(PROJECT_DIRECTIVE)
    (project / ".scrumia" / "extends.json").write_text(json.dumps({"implement": [{
        "name": "A house rule", "type": "norm", "when": "required",
        "summary": "this project's own", "read": "CLAUDE.md"}]}), encoding="utf-8")
    code, out, _ = run(["implement", "--json"], project / ".scrumia" / "config.yaml")
    rows = json.loads(out)
    check("the project's own directive appears with no module created or installed",
          [r["name"] for r in rows] == ["A house rule"], rows)
    check("and it outranks every module, at scope 0",
          rows and rows[0]["scope"] == 0, rows)
    check("reading it is not a failure", code == 0, code)
    shutil.rmtree(project)


def main() -> int:
    if not os.access(TOOL, os.X_OK):
        print(f"error: {TOOL.relative_to(ROOT)} is not executable")
        return 1
    test_ac17_a_module_is_declared_by_source()
    test_ac17_a_bare_name_is_not_a_declaration()
    test_ac17_the_retired_list_is_still_read()
    test_a_composition_declaring_nothing_does_not_look_correct()
    test_ac18_a_setting_resolves_through_three_layers()
    test_ac1_ac2_each_source_resolves_from_its_own_location()
    test_ac3_resolution_states_where_each_module_came_from()
    test_ac4_a_local_module_is_held_to_the_same_standard()
    test_ac5_one_declaration_two_modules_is_a_conflict()
    test_ac5_identity_and_declaration_settle_the_other_two_cases()
    test_ac9_ac10_no_versioned_path_and_no_installation()
    print(f"\n{len(FAILURES)} failure(s)")
    return 1 if FAILURES else 0


if __name__ == "__main__":
    sys.exit(main())
