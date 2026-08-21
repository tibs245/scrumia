#!/usr/bin/env python3
"""Acceptance tests for plugins/scrumia-core/bin/scrumia-extends (#302, #291).

AC-17 and AC-18 of features/business/modular-composition/: a module is declared by
source and a bare name is not a declaration; a setting resolves through three layers
in a stated order.

AC-1..AC-11 of features/business/local-extension/: each source resolves from its own
location, resolution states which, one declaration answered by two distinct modules is a
conflict that binds neither, and one naming no location is a shadow. A declaration no
location answers is an absence every surface survives (AC-6), what `CLAUDE.md` claims is
reconciled against those states (AC-7), and a project extending itself without a module
of its own is correctly extended rather than broken (AC-8).

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
STATUS_TOOL = ROOT / "plugins" / "scrumia-core" / "scripts" / "compose-status.sh"
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
  "tibs245/scrumia:scrumia-tdd": {}
"""

WRONG_SOURCE = """
project: { name: "Elsewhere" }
modules:
  "acme/other:scrumia-tdd": {}
"""

LOCAL_AND_SHARED = """
project: { name: "Nearby" }
modules:
  "local:scrumia-tdd": {}
  "shared:scrumia-design": {}
"""

BARE_NAME = """
project: { name: "Bare" }
modules:
  "scrumia-tdd": {}
  ":scrumia-specs": {}
  "github:scrumia-teams": {}
  "a/b/c:scrumia-discovery": {}
  "tibs245/scrumia:scrumia-design": {}
"""

# The four keys BARE_NAME's grammar refuses. Named once: the pattern is written in three
# places, and a copy loosened on its own contradicts the notice printed beside it.
REFUSED = ["scrumia-tdd", ":scrumia-specs", "github:scrumia-teams",
           "a/b/c:scrumia-discovery"]

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
  - scrumia-tdd
"""

PER_APP = """
project: { name: "Apps" }
modules:
  "tibs245/scrumia:scrumia-design": {}
apps:
  - name: "web"
    path: "apps/web"
    modules:
      "tibs245/scrumia:scrumia-tdd": {}
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
          "scrumia-tdd" in modules_in(market), modules_in(market))
    rows = rows_in(market)
    check("every row carries the key it was declared by",
          all(r["declared_as"] == "tibs245/scrumia:scrumia-tdd" for r in rows),
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
          modules_in(apps, app="web") == {"scrumia-design", "scrumia-tdd"}
          and modules_in(apps) == {"scrumia-design"},
          (modules_in(apps, app="web"), modules_in(apps)))
    os.unlink(apps)


def test_ac17_a_bare_name_is_not_a_declaration() -> None:
    print("AC-17 — a bare name is reported as such, never resolved against what is installed")

    bare = config_with(BARE_NAME)
    code, out, err = run(["implement", "--json"], bare)
    resolved = {row["module"] for row in json.loads(out)}
    check("the bare name resolves nothing",
          "scrumia-tdd" not in resolved, resolved)
    check("the sourced key beside it still resolves",
          "scrumia-design" in resolved, resolved)
    check("the key is named in the report", "'scrumia-tdd'" in err, err.strip())
    check("and it is called what it is",
          "is not a declaration" in err and "<source>:<module>" in err, err.strip())
    check("a key whose source half is missing is refused too",
          "':scrumia-specs' is not a declaration" in err, err.strip())
    _, out, _ = run(["--modules", "--json"], bare)
    located = {r["key"]: r["location"] for r in json.loads(out)}
    check("and it is credited with no location, not with the marketplace",
          all(located.get(k) == "(none)" for k in REFUSED), located)
    (Path(bare).parent / "CLAUDE.md").write_text(
        "".join(f"| `{k.split(':')[-1]}` | x |\n" for k in REFUSED), encoding="utf-8")
    code, out, _ = run(["--claims", str(Path(bare).parent / "CLAUDE.md")], bare)
    check("and the reconciliation calls every one of them unsourced, as the notice does",
          code == 0 and out.count("| unsourced |") == len(REFUSED), out[:500])
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
          "scrumia-tdd" in {r["module"] for r in json.loads(out)}, out[:200])
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
  "tibs245/scrumia:scrumia-tdd": {}
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
modules:
  "shared:acme-conventions": {}
"""

SHADOWING = """
project: { name: "Shadow" }
extends:
  - acme-conventions
"""

SHADOWED = """
project: { name: "Promoting" }
modules:
  "shared:scrumia-tdd": {}
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
          "scrumia-tdd" in by_module, sorted(by_module))
    check("nothing distinguishes the three rows but the location reported alongside them",
          {m: r["location"] for m, r in by_module.items()} ==
          {"acme-conventions": "shared", "acme-docs-rules": "local",
           "scrumia-tdd": "marketplace"},
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
          {"tibs245/scrumia:scrumia-tdd": "marketplace",
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

    # Two directories in one tier both publishing the name — a fork checked out beside the
    # module it forked. A `shared:` key names that tier and cannot say which of the two.
    project = project_with(CONFLICTING)
    shared = Path(tempfile.mkdtemp(prefix="scrumia-shared-"))
    make_module(shared / "acme-conventions", "acme-conventions")
    make_module(shared / "acme-conventions-fork", "acme-conventions")
    config = project / ".scrumia" / "config.yaml"

    code, out, err = run(["implement", "--json"], config, shared=shared)
    check("neither is used — no directive of that module reaches the register",
          json.loads(out) == [], out[:200])
    check("the conflict is named, with both directories",
          "acme-conventions-fork" in err and "shared:acme-conventions" in err, err.strip())
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
    # BR-9: it blocks its own declaration and nothing else. One conflict is one finding —
    # not a second one about a module colliding with itself in a register.
    check("and reports the conflict once, not once per register the module opens",
          err.count("binds neither") == 1 and "nothing decides which main skill" not in err,
          err.strip())
    shutil.rmtree(project)
    shutil.rmtree(shared)


def test_ac11_a_bare_name_answered_twice_is_a_shadow_not_a_conflict() -> None:
    print("AC-11 — a declaration naming no location is shadowed, reported and used")

    project = project_with(SHADOWING)
    shared = Path(tempfile.mkdtemp(prefix="scrumia-shared-"))
    make_module(shared / "acme-conventions", "acme-conventions")
    make_module(project / ".scrumia" / "modules" / "acme-conventions", "acme-conventions")
    config = project / ".scrumia" / "config.yaml"

    code, out, err = run(["implement", "--json"], config, shared=shared)
    check("the module is used, not disabled — promotion must stay cheap",
          [r["module"] for r in json.loads(out)] == ["acme-conventions"], out[:200])
    check("and the one used is the narrowest location",
          json.loads(out)[0]["location"] == "local", out[:200])
    check("the shadow is reported, naming every location that answered",
          "shared" in err and "local" in err and "narrowest" in err, err.strip())
    check("with the fix named: key it by source", "<source>:<module>" in err, err.strip())

    code, _, err = run(["--check"], config, shared=shared)
    check("a shadow is not an unmet dependency", code == 0, code)
    shutil.rmtree(project)
    shutil.rmtree(shared)


def test_ac5_identity_and_declaration_settle_the_other_two_cases() -> None:
    print("AC-5 — one module reached twice, and an undeclared copy, are not conflicts")

    project = project_with(SHADOWING)
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
    check("and nothing is called a conflict or a shadow",
          "binds neither" not in err and "narrowest" not in err, err.strip())
    shutil.rmtree(project)
    shutil.rmtree(shared)

    # The promotion case: the published module is installed and a checkout of it is
    # declared. module-authoring BR-3 is only affordable if that is not a fault.
    promoting = project_with(SHADOWED)
    checkout = Path(tempfile.mkdtemp(prefix="scrumia-shared-"))
    make_module(checkout / "scrumia-tdd", "scrumia-tdd")
    _, out, err = run(["--modules", "--json"], promoting / ".scrumia" / "config.yaml",
                      shared=checkout)
    row = json.loads(out)[0]
    check("the declared checkout resolves while the published copy is simply not run",
          row["state"] == "resolved" and row["location"] == "shared"
          and row["roots"][0]["root"].startswith(str(checkout.resolve())), row)
    check("and no conflict is reported", "binds neither" not in err, err.strip())
    shutil.rmtree(promoting)
    shutil.rmtree(checkout)


def test_env_local_is_read_or_reported_never_silently_empty() -> None:
    print("BR-6 — the machine's file is read through its habits, or its silence is named")

    shared = Path(tempfile.mkdtemp(prefix="scrumia-shared-"))
    make_module(shared / "acme-conventions", "acme-conventions")

    for label, body in [
        ("an export prefix", f"export SCRUMIA_SHARED_DIR={shared}\n"),
        ("spaces around the =", f"SCRUMIA_SHARED_DIR = {shared}\n"),
        ("a quoted value", f'SCRUMIA_SHARED_DIR="{shared}"\n'),
        ("a trailing space", f"SCRUMIA_SHARED_DIR={shared} \n"),
        ("a comment above it", f"# where my checkouts live\nSCRUMIA_SHARED_DIR={shared}\n"),
    ]:
        project = project_with(ABSENT_SHARED)
        (project / ".scrumia" / ".env.local").write_text(body, encoding="utf-8")
        _, out, _ = run(["--modules", "--json"], project / ".scrumia" / "config.yaml")
        check(f"{label} still resolves the shared tier",
              json.loads(out)[0]["state"] == "resolved", json.loads(out))
        shutil.rmtree(project)

    # The failure this exists for: a file that yields nothing takes the whole tier with it,
    # and every table just renders shorter.
    project = project_with(ABSENT_SHARED)
    (project / ".scrumia" / ".env.local").write_text("SCRUMIA_SHRED_DIR=/x\n", encoding="utf-8")
    _, out, err = run(["--modules", "--json"], project / ".scrumia" / "config.yaml")
    check("a file that sets nothing is named, not read as an empty tier",
          "sets no SCRUMIA_SHARED_DIR" in err, err.strip())
    shutil.rmtree(project)

    project = project_with(ABSENT_SHARED)
    (project / ".scrumia" / ".env.local").write_text(
        "SCRUMIA_SHARED_DIR=/nowhere/at/all\n", encoding="utf-8")
    _, _, err = run(["--modules", "--json"], project / ".scrumia" / "config.yaml")
    check("and a path that is not a directory here is named too",
          "not a directory on this machine" in err, err.strip())
    shutil.rmtree(project)
    shutil.rmtree(shared)


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


CLAIMED = """
project: { name: "Claiming" }
modules:
  "tibs245/scrumia:scrumia-tdd": {}
  "shared:acme-conventions": {}
"""


def compose_status(config: Path):
    env = {**os.environ, "NO_COLOR": "1", "SCRUMIA_CONFIG": str(config),
           "SCRUMIA_CONFIG_LOCAL": "/nonexistent/config.local.yaml"}
    proc = subprocess.run([str(STATUS_TOOL)], cwd=ROOT, env=env,
                          capture_output=True, text=True, timeout=60)
    return proc.returncode, proc.stdout, proc.stderr


def test_ac6_a_clone_that_cannot_reach_the_module_is_told_and_still_works() -> None:
    print("AC-6 — the capability is a declared absence, every register renders, nothing fails")

    project = project_with(CLAIMED)
    config = project / ".scrumia" / "config.yaml"
    shared = Path(tempfile.mkdtemp(prefix="scrumia-shared-"))
    make_module(shared / "acme-conventions", "acme-conventions")

    # The machine that has the checkout — the state the absence below has to be told apart
    # from, or the test proves only that a name nothing ever answered stays unanswered.
    _, out, _ = run(["implement", "--json"], config, shared=shared)
    check("with the shared directory reachable, the module's directive is in the table",
          "acme-conventions" in {r["module"] for r in json.loads(out)}, out[:200])

    # Nothing else changes: no key removed, no file edited. Only the environment that
    # resolved it is gone, which is what a clone arrives in.
    code, out, err = run(["--modules", "--json"], config)
    absent = [r for r in json.loads(out) if r["key"] == "shared:acme-conventions"][0]
    check("without it, the declaration is an absence naming the kind of location",
          absent["state"] == "absent" and absent["location"] == "shared", absent)
    check("and it is credited with no root rather than with a wrong one",
          absent["roots"] == [], absent)
    check("reading the composition is not a failure", code == 0, code)
    check("and nothing calls the project malformed",
          "malformed" not in err and "not a module" not in err, err.strip())

    code, out, _ = run(["implement", "--json"], config)
    rows = json.loads(out)
    check("the register renders without it", code == 0 and rows, code)
    check("carrying the modules that did resolve, and not the one that did not",
          {r["module"] for r in rows} == {"scrumia-tdd"}, rows)

    for args in (["--list"], ["--check"]):
        code, _, err = run(args, config)
        check(f"{' '.join(args)} still answers, and does not fail on the absence",
              code == 0, f"exit {code}: {err.strip()}")

    code, out, _ = compose_status(config)
    check("the reader that resolves nothing still runs", code == 0, code)
    check("and says it declares rather than that it runs",
          "Modules this project declares" in out, out[:200])

    shutil.rmtree(project)
    shutil.rmtree(shared)


def test_ac7_what_claude_md_claims_survives_a_clone() -> None:
    print("AC-7 — a claim the reader cannot reach is named, and one that states its source is not")

    project = project_with(CLAIMED)
    config = project / ".scrumia" / "config.yaml"
    shared = Path(tempfile.mkdtemp(prefix="scrumia-shared-"))
    make_module(shared / "acme-conventions", "acme-conventions")
    claude = project / "CLAUDE.md"
    bare = ("## ScrumIA composition\n\n| Module | What to know |\n|---|---|\n"
            "| `scrumia-tdd` | Tests first. |\n"
            "| `acme-conventions` | Tabs, not spaces. |\n")
    claude.write_text(bare, encoding="utf-8")

    code, out, _ = run(["--claims"], config, shared=shared)
    check("on the machine that wrote it, every claim is honoured",
          code == 0 and "honoured" in out and "claimed |" not in out, f"exit {code}: {out[:300]}")

    code, out, err = run(["--claims"], config)
    check("on a clone, the unreachable claim is named", code != 0, code)
    check("with the module, its state and where it would have come from",
          "acme-conventions" in err and "absent" in err and "shared:" in err, err.strip())
    check("and the honoured one is not swept up with it",
          "| `tibs245/scrumia:scrumia-tdd` | marketplace | resolved | yes | honoured |"
          in out, out[:400])

    # The same file, saying where the module comes from. Nothing about the composition
    # changed — only what the file claims about it.
    claude.write_text(bare.replace("`acme-conventions`", "`shared:acme-conventions`"),
                      encoding="utf-8")
    code, out, _ = run(["--claims"], config)
    check("naming the declaration key instead is an absence the file states, not a claim",
          code == 0 and "named as absent" in out, f"exit {code}: {out[:300]}")

    claude.write_text("## ScrumIA composition\n\nNothing to say.\n", encoding="utf-8")
    code, out, _ = run(["--claims"], config)
    check("a file that mentions none of its declarations fails, naming each one (AC-14)",
          code != 0 and "not claimed" in out, f"exit {code}: {out[:300]}")

    claude.unlink()
    code, _, err = run(["--claims"], config)
    check("and a project whose CLAUDE.md went away fails on its unclaimed declarations",
          code != 0 and "does not exist" in err, f"exit {code}: {err.strip()}")
    shutil.rmtree(project)

    # A key the grammar refuses names no module to look for, and looking for nothing finds
    # it everywhere — so it must leave the table rather than answer for a file it never read.
    project = project_with("""
project: { name: "Refused" }
modules:
  "foo:": {}
  "tibs245/scrumia:scrumia-tdd": {}
""")
    (project / "CLAUDE.md").write_text("| `scrumia-tdd` | Tests first. |\n",
                                       encoding="utf-8")
    code, out, _ = run(["--claims"], project / ".scrumia" / "config.yaml")
    check("a key that is not a declaration is not reconciled against anything",
          code == 0 and "foo:" not in out, f"exit {code}: {out[:300]}")
    shutil.rmtree(project)


def test_claims_matches_a_name_at_its_edges_and_only_where_reach_is_at_stake() -> None:
    print("AC-7 — what counts as naming a module, and which absence the file is answerable for")

    # A name found inside a path or inside a longer name is not a claim; the keyed
    # forms below are, and the assertion checks only the keyed ones match.
    project = project_with("""
project: { name: "Edges" }
modules:
  "shared:tools": {}
  "shared:acme": {}
  "shared:scrumia": {}
""")
    (project / "CLAUDE.md").write_text(
        "Run `python3 tools/validate.py` before pushing.\n"
        "| `acme-lint` | Lints. |\n"
        "| `scrumia-tdd` | Tests first. |\n"
        "We use `shared:tools`, `shared:acme`, and `shared:scrumia` here.\n",
        encoding="utf-8")
    code, out, _ = run(["--claims"], project / ".scrumia" / "config.yaml")
    check("a name inside a path is not a claim about the module of that name",
          code == 0, f"exit {code}: {out[:400]}")
    check("nor is one inside a longer module name — only the keyed form is",
          out.count("named as absent") == 3, out[:400])
    shutil.rmtree(project)

    # BR-8's subject: the location a clone cannot reach. A marketplace module nobody
    # installed is absent too, and the answer there is a fetch, not a sentence to correct.
    project = project_with("""
project: { name: "Reach" }
modules:
  "acme/mk:acme-lint": {}
  "local:acme-docs": {}
  "shared:acme-conventions": {}
""")
    (project / "CLAUDE.md").write_text(
        "| `acme-lint` | Lints. |\n| `acme-docs` | Docs. |\n"
        "| `acme-conventions` | Tabs. |\n", encoding="utf-8")
    code, out, err = run(["--claims"], project / ".scrumia" / "config.yaml")
    verdicts = {line.split("|")[1].strip().strip("`"): line.split("|")[5].strip()
                for line in out.splitlines() if line.startswith("| `")}
    check("a marketplace module nobody installed is reachable, not a claim",
          verdicts.get("acme/mk:acme-lint") == "reachable", verdicts)
    check("nor is one inside the project, which arrives with the clone",
          verdicts.get("local:acme-docs") == "reachable", verdicts)
    check("only the shared checkout is a capability the reader cannot reach",
          verdicts.get("shared:acme-conventions") == "claimed", verdicts)
    check("and it alone decides the exit status",
          code != 0 and err.count("comes from a shared checkout") == 1, f"exit {code}: {err}")
    shutil.rmtree(project)

    # A key left behind by a promotion. Failing here would demand a `shared:` row over a
    # module the repository ships.
    project = project_with("""
project: { name: "Promoted" }
modules:
  "local:acme-conventions": {}
  "shared:acme-conventions": {}
""")
    make_module(project / ".scrumia" / "modules" / "acme-conventions", "acme-conventions")
    (project / "CLAUDE.md").write_text("| `acme-conventions` | Tabs. |\n", encoding="utf-8")
    code, out, _ = run(["--claims"], project / ".scrumia" / "config.yaml")
    check("a module another key already bound is not claimed against the stale one",
          code == 0 and "| claimed |" not in out, f"exit {code}: {out[:400]}")
    shutil.rmtree(project)

    # Three keys state no origin the tool can use, so no wording of the file could have
    # repeated one.
    for label, body in [
        ("from the retired list", 'extends:\n  - acme-conventions\n'),
        ("with no source at all", 'modules:\n  ":acme-conventions": {}\n'),
        ("with a source the grammar refuses", 'modules:\n  "foo:acme-conventions": {}\n'),
    ]:
        project = project_with(f'project: {{ name: "Unsourced" }}\n{body}')
        (project / "CLAUDE.md").write_text("| `acme-conventions` | Tabs. |\n",
                                           encoding="utf-8")
        code, out, _ = run(["--claims"], project / ".scrumia" / "config.yaml")
        check(f"a declaration {label} is unsourced, not an absence the file stated",
              code == 0 and "| unsourced |" in out, f"exit {code}: {out[:400]}")
        shutil.rmtree(project)

    # The carve-out: `local:` next to `shared:`, where the local resolves and the
    # shared does not — what makes the second verdict `reachable`, not `claimed`.
    project = project_with("""
project: { name: "Shadowed and stale" }
modules:
  "local:scrumia-tdd": {}
  "shared:scrumia-tdd": {}
""")
    make_module(project / ".scrumia" / "modules" / "scrumia-tdd",
                "scrumia-tdd")
    (project / "CLAUDE.md").write_text("| `scrumia-tdd` | Tests first. |\n",
                                       encoding="utf-8")
    code, out, _ = run(["--claims"], project / ".scrumia" / "config.yaml")
    stale = [line for line in out.splitlines()
             if line.startswith("| `shared:scrumia-tdd`")]
    check("a module a shadow bound is reachable for the stale key beside it",
          code == 0 and len(stale) == 1 and stale[0].endswith("| reachable |"),
          f"exit {code}: {stale or out[:400]}")
    shutil.rmtree(project)

    shared = Path(tempfile.mkdtemp(prefix="scrumia-shared-"))
    make_module(shared / "acme-conventions", "acme-conventions")
    make_module(shared / "acme-conventions-fork", "acme-conventions")
    project = project_with(SHADOWING)
    (project / "CLAUDE.md").write_text("| `acme-conventions` | Tabs. |\n", encoding="utf-8")
    code, out, _ = run(["--claims"], project / ".scrumia" / "config.yaml", shared=shared)
    check("a conflicted declaration stating no origin is unsourced, not claimed",
          code == 0 and "| unsourced |" in out and "conflict" in out, f"exit {code}: {out[:400]}")
    shutil.rmtree(project)
    shutil.rmtree(shared)

    project = project_with(MARKETPLACE)
    (project / "CLAUDE.md").write_text("Nothing about the composition.\n", encoding="utf-8")
    code, out, _ = run(["--claims"], project / ".scrumia" / "config.yaml")
    check("a module the file never names, that resolves, is unclaimed",
          code == 0 and "| unclaimed |" in out, f"exit {code}: {out[:400]}")
    shutil.rmtree(project)


def test_claims_refuses_to_answer_when_it_could_not_read() -> None:
    print("AC-7 — a read that failed never reports as a composition claiming nothing")

    # A half-migration makes the query fail, and read as an empty composition it would clear
    # a live claim and exit 0.
    project = project_with("""
project: { name: "Half migrated" }
modules:
  - "shared:acme-conventions"
""")
    (project / "CLAUDE.md").write_text("We run `acme-conventions` here.\n", encoding="utf-8")
    config = project / ".scrumia" / "config.yaml"
    for args in (["--claims"], ["--check"], ["--modules"], ["implement"]):
        code, out, err = run(args, config)
        check(f"{' '.join(args)} refuses the config rather than reading it as empty",
              code != 0 and "could not be read as a composition" in err,
              f"exit {code}: {err.strip()[:200] or out[:200]}")

    # The default file being a directory is not the default file being absent.
    project2 = project_with(MARKETPLACE)
    (project2 / "CLAUDE.md").mkdir()
    code, _, err = run(["--claims"], project2 / ".scrumia" / "config.yaml")
    check("a directory at the default path is an error, not a file claiming nothing",
          code != 0 and "is not a file" in err, f"exit {code}: {err.strip()}")
    shutil.rmtree(project)
    shutil.rmtree(project2)


def test_claims_answers_for_a_shadow_a_conflict_and_a_named_file() -> None:
    print("AC-7 — the states other than absent, and a file the caller named")

    shared = Path(tempfile.mkdtemp(prefix="scrumia-shared-"))
    make_module(shared / "acme-conventions", "acme-conventions")
    make_module(shared / "acme-conventions-fork", "acme-conventions")

    # A conflict binds nothing, so the module contributes nowhere — a file naming it bare
    # promises a capability that is not running, exactly as an absence does.
    project = project_with(CONFLICTING)
    (project / "CLAUDE.md").write_text("| `acme-conventions` | Tabs. |\n", encoding="utf-8")
    config = project / ".scrumia" / "config.yaml"
    code, out, _ = run(["--claims"], config, shared=shared)
    check("a conflicted module named bare is a claim the reader cannot reach",
          code != 0 and "| claimed |" in out, f"exit {code}: {out[:400]}")
    shutil.rmtree(project)

    shutil.rmtree(shared)

    # A shadow binds and is used, so the claim is simply true — reported, never failed.
    # Its own shared directory: the fork above would make this one a conflict instead.
    shared = Path(tempfile.mkdtemp(prefix="scrumia-shared-"))
    make_module(shared / "acme-conventions", "acme-conventions")
    project = project_with(SHADOWING)
    (project / "CLAUDE.md").write_text("| `acme-conventions` | Tabs. |\n", encoding="utf-8")
    make_module(project / ".scrumia" / "modules" / "acme-conventions", "acme-conventions")
    config = project / ".scrumia" / "config.yaml"
    code, out, _ = run(["--claims"], config, shared=shared)
    check("a shadowed module is honoured, since the narrowest copy is running",
          code == 0 and "| honoured |" in out, f"exit {code}: {out[:400]}")
    shutil.rmtree(project)
    shutil.rmtree(shared)

    # One module declared project-wide and by an app is one claim, not two rows.
    project = project_with("""
project: { name: "Twice" }
modules:
  "tibs245/scrumia:scrumia-tdd": {}
apps:
  - name: "web"
    path: "apps/web"
    modules:
      "tibs245/scrumia:scrumia-tdd": {}
""")
    (project / "CLAUDE.md").write_text("| `scrumia-tdd` | Tests. |\n",
                                       encoding="utf-8")
    config = project / ".scrumia" / "config.yaml"
    code, out, _ = run(["--claims"], config)
    check("a module declared in two scopes is reconciled once",
          code == 0 and out.count("scrumia-tdd") == 1, out[:400])

    # A file the caller named is an assertion it is there. Read as empty it would clear
    # every claim and exit clean, which is the answer this surface must never give.
    for arg, label in [(str(project), "a directory"), (str(project / "nope.md"), "a typo")]:
        code, _, err = run(["--claims", arg], config)
        check(f"{label} passed as the file is an error, not a file claiming nothing",
              code != 0 and "is not a file" in err, f"exit {code}: {err.strip()}")
    shutil.rmtree(project)


def test_ac14_per_app_stub_is_reconciled_against_its_own_scope() -> None:
    print("AC-14 — --claims walks per-app stubs alongside the root file, reconciling per scope")

    # The recommended shape: app stub names its own declaration bare, so the verdict is
    # `claimed` — but the scope is the app's stub, so the run does not fail on it.
    project = project_with("""
project: { name: "App claims" }
modules: {}
apps:
  - name: "site"
    path: "apps/site"
    modules:
      "shared:acme-web": {}
""")
    (project / "apps" / "site").mkdir(parents=True)
    (project / "apps" / "site" / "CLAUDE.md").write_text(
        "## The site app\n\n| `acme-web` | Web bits. |\n", encoding="utf-8")
    code, out, err = run(["--claims"], project / ".scrumia" / "config.yaml")
    app_section = [line for line in out.splitlines()
                   if line.startswith("# claims") and "site" in line]
    app_rows = [line for line in out.splitlines() if line.startswith("| `")]
    check("an app stub is reconciled against the app's own scope",
          len(app_section) == 1 and "scope: site" in app_section[0],
          f"exit {code}: {out[:400]}")
    check("the verdict on the app stub's claim is `claimed`",
          len(app_rows) == 1 and app_rows[0].endswith("| claimed |"),
          f"exit {code}: {out[:400]}")
    check("and the stub's verdict does not fail the run",
          code == 0, f"exit {code}: {err.strip()}")
    shutil.rmtree(project)

    # A module declared in the root config and mentioned nowhere: `not claimed`, fails.
    project = project_with("""
project: { name: "Unclaimed" }
modules:
  "shared:acme-web": {}
""")
    (project / "CLAUDE.md").write_text("Nothing to say.\n", encoding="utf-8")
    code, out, err = run(["--claims"], project / ".scrumia" / "config.yaml")
    check("a declaration the root file does not mention is `not claimed`",
          "not claimed" in out and "`shared:acme-web`" in out, f"exit {code}: {out[:400]}")
    check("and the run exits non-zero on it",
          code != 0, f"exit {code}: {err.strip()}")
    shutil.rmtree(project)

    # Both scopes in one run: the root claim fails (root scope, `claimed`), the app stub
    # does not — the failure names the root file, not the app's path.
    project = project_with("""
project: { name: "Both" }
modules:
  "shared:acme-root": {}
apps:
  - name: "site"
    path: "apps/site"
    modules:
      "shared:acme-app": {}
""")
    (project / "CLAUDE.md").write_text("| `acme-root` | Root. |\n", encoding="utf-8")
    (project / "apps" / "site").mkdir(parents=True)
    (project / "apps" / "site" / "CLAUDE.md").write_text(
        "| `acme-app` | App. |\n", encoding="utf-8")
    code, out, err = run(["--claims"], project / ".scrumia" / "config.yaml")
    root_rows = [line for line in out.splitlines()
                 if line.startswith("| `shared:acme-root`")]
    app_rows = [line for line in out.splitlines()
                if line.startswith("| `shared:acme-app`")]
    check("the root file's claim is held against the root scope",
          len(root_rows) == 1 and root_rows[0].endswith("| claimed |"),
          f"exit {code}: {out[:400]}")
    check("the app stub's claim is held against the app's scope",
          len(app_rows) == 1 and app_rows[0].endswith("| claimed |"),
          f"exit {code}: {out[:400]}")
    check("and the app stub's verdict is not what makes the run fail",
          code != 0 and "apps/site/CLAUDE.md" not in err, f"exit {code}: {err.strip()}")
    shutil.rmtree(project)


def test_ac8_local_material_without_a_module_is_not_a_malformed_module() -> None:
    print("AC-8 — directives and a rules section are a correct extension, not a broken module")

    project = project_with("""
project: { name: "No module of its own" }
modules:
  "tibs245/scrumia:scrumia-tdd": {}
""")
    config = project / ".scrumia" / "config.yaml"
    rules = project / "docs" / "house-rules.md"
    rules.parent.mkdir(parents=True, exist_ok=True)
    rules.write_text("# House rules\n\nOne topic, grown past CLAUDE.md.\n", encoding="utf-8")
    (project / ".scrumia" / "extends.json").write_text(json.dumps({"implement": [
        {"name": "House rules", "type": "norm", "when": "required",
         "summary": "what this project does differently", "read": "docs/house-rules.md"},
        {"name": "Naming", "type": "norm", "when": "optional",
         "summary": "one more, to make it a set", "read": "docs/house-rules.md"}]}),
        encoding="utf-8")

    code, out, err = run(["implement", "--json"], config)
    rows = json.loads(out)
    check("the directives appear in their register",
          [r["name"] for r in rows][:2] == ["House rules", "Naming"], rows)
    check("the rules section is reached through the directive that names it",
          rows and rows[0]["read"] == "docs/house-rules.md", rows[:1])
    check("reading it is not a failure", code == 0, code)
    check("and nothing on the way calls anything malformed",
          "malformed" not in err and "ignored" not in err, err.strip())

    for args in (["--check"], ["--modules", "--json"]):
        code, _, err = run(args, config)
        check(f"{' '.join(args)} reports the project correctly extended", code == 0,
              f"exit {code}: {err.strip()}")

    code, out, _ = run(["--modules", "--json"], config)
    check("no declaration is unaccounted for, so nothing is reported missing",
          all(r["state"] == "resolved" for r in json.loads(out)), out[:200])

    # There is no module tree here to hand the checker, and `not_a_module` rather than
    # `findings` is the whole of the difference AC-8 turns on.
    proc = subprocess.run([str(MODULE_TOOL), "check", str(project / ".scrumia")],
                          cwd=ROOT, capture_output=True, text=True, timeout=60)
    check("the checker refuses the project's own .scrumia/ rather than finding it broken",
          proc.returncode == 4, f"exit {proc.returncode}: {proc.stdout[:200]}")
    check("and says what it is, not what is wrong with it",
          "not a module" in (proc.stdout + proc.stderr), (proc.stdout + proc.stderr)[:200])

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
    test_ac11_a_bare_name_answered_twice_is_a_shadow_not_a_conflict()
    test_ac5_identity_and_declaration_settle_the_other_two_cases()
    test_env_local_is_read_or_reported_never_silently_empty()
    test_ac9_ac10_no_versioned_path_and_no_installation()
    test_ac6_a_clone_that_cannot_reach_the_module_is_told_and_still_works()
    test_ac7_what_claude_md_claims_survives_a_clone()
    test_claims_matches_a_name_at_its_edges_and_only_where_reach_is_at_stake()
    test_claims_answers_for_a_shadow_a_conflict_and_a_named_file()
    test_claims_refuses_to_answer_when_it_could_not_read()
    test_ac14_per_app_stub_is_reconciled_against_its_own_scope()
    test_ac8_local_material_without_a_module_is_not_a_malformed_module()
    print(f"\n{len(FAILURES)} failure(s)")
    return 1 if FAILURES else 0


if __name__ == "__main__":
    sys.exit(main())
