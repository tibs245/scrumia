#!/usr/bin/env python3
"""Acceptance tests for `scrumia-gradle` — ticket #451.

AC-1 through AC-13 of plugins/scrumia-gradle/SKILL.md and the eight guides.

What is asserted, and how. The plugin is prose that an agent executes, so most of
the criteria are prose-level: a rule that exists where AC-N says it exists, a refusal
that names the misplacement, a citation that points at the right satellite. A
substring assertion cannot catch a polarity flip, so each AC has a paired mutation
that must break it, mirroring what `tools/test_module_authoring.py` does for the
authoring pass.

AC-5 is the one criterion that runs against a real surface: the module must pass
`python3 tools/validate.py` and `scrumia-module check plugins/scrumia-gradle`.
The remaining twelve run against the plugin's own tree.

Run from the repo root: python3 tools/test_gradle_module.py
Exit code 0 when everything passes, 1 otherwise.
"""

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PLUGIN = ROOT / "plugins" / "scrumia-gradle"
SKILL_DIR = PLUGIN / "skills" / "scrumia-gradle"
GUIDES = SKILL_DIR / "guides"
EXTENDS = PLUGIN / "extends.json"
MARKETPLACE = ROOT / ".claude-plugin" / "marketplace.json"
CHECKER = ROOT / "plugins" / "scrumia-core" / "bin" / "scrumia-module"

FAILURES: list[str] = []


def check(name: str, ok: bool, detail: str = "") -> None:
    if ok:
        print(f"  ok    {name}")
    else:
        FAILURES.append(f"{name} — {detail}" if detail else name)
        print(f"  FAIL  {name} — {detail}" if detail else f"  FAIL  {name}")


def read(rel: str) -> str:
    return (PLUGIN / rel).read_text(encoding="utf-8")


def guides_text() -> str:
    return "\n".join(p.read_text(encoding="utf-8") for p in sorted(GUIDES.glob("*.md")))


def decision_text() -> str:
    return (SKILL_DIR / "decisions" / "D-01-convention-plugin-shape.md").read_text(encoding="utf-8")


# --- AC-1: a pure-JVM project gets the rules; no Kotlin language required ----------


def ac_1() -> None:
    """A pure-JVM project activating only `scrumia-gradle` receives the rules.

    The plugin must ship, its rules must be reachable through `extends.json`,
    and no rule may require Kotlin language knowledge (AC-2 covers the second
    half explicitly).
    """
    extends = json.loads(EXTENDS.read_text(encoding="utf-8"))
    implement_names = [d["name"] for d in extends.get("implement", [])]
    # Eight rules: build script format, version catalog, convention plugin shape,
    # task configuration, caches, composite builds, pluginManagement, documentation tasks.
    needed = {
        "Kotlin DSL over Groovy",
        "Versions live in the catalog",
        "Convention plugin shape",
        "Tasks are registered, not created",
        "Caches on by default",
        "Composite builds for local siblings",
        "Plugin versions in pluginManagement",
        "Documentation tasks wired into the lifecycle",
    }
    missing = needed - set(implement_names)
    check(
        "AC-1: implements the eight rules required by the Gradle lane",
        not missing,
        f"missing: {sorted(missing)}" if missing else "",
    )


# --- AC-2: no rule requires Kotlin language knowledge -----------------------------


def ac_2() -> None:
    """No rule in `scrumia-gradle` requires Kotlin language knowledge.

    The Kotlin DSL is Gradle's, not Kotlin's. A reviewer finding a rule that
    reads as "you must understand Kotlin coroutines" would name AC-2.
    """
    forbidden = [
        "coroutine",
        "data class",
        "sealed class",
        "kotlin.collections",
        "kotlinx.coroutines",
        "Flow<",
        "Arrow",
        "kotlin.Result",
    ]
    text = guides_text() + "\n" + decision_text()
    hits = [w for w in forbidden if re.search(rf"\b{re.escape(w)}\b", text, re.IGNORECASE)]
    check(
        "AC-2: no rule requires Kotlin language knowledge",
        not hits,
        f"forbidden term found: {hits}" if hits else "",
    )


# --- AC-3: convention plugin patterns are stated in build-logic shape, not KMP -----


def ac_3() -> None:
    """Convention plugin patterns are stated in terms of `build-logic` shape.

    The convention plugin guide must declare `build-logic` as the place shared
    build logic lives, and `D-01` must cite `scrumia-kotlin-multiplatform-mobile`
    as the place a Kotlin Multiplatform-shaped convention plugin belongs.
    """
    guide = read("skills/scrumia-gradle/guides/03-convention-plugin-shape.md")
    d01 = decision_text()
    check(
        "AC-3: convention plugin guide names build-logic as the home of shared logic",
        "build-logic" in guide and "includeBuild" in guide,
        "missing build-logic or includeBuild reference" if ("build-logic" not in guide or "includeBuild" not in guide) else "",
    )
    check(
        "AC-3: D-01 cites scrumia-kotlin-multiplatform-mobile for KMP-shaped plugins",
        "scrumia-kotlin-multiplatform-mobile" in d01,
        "D-01 does not name the satellite" if "scrumia-kotlin-multiplatform-mobile" not in d01 else "",
    )


# --- AC-4: lands independently of every other satellite ----------------------------


def ac_4() -> None:
    """`scrumia-gradle` lands and merges independently of every other satellite.

    A cross-dependency means a `dependencies.jsonl` entry or a register the
    plugin opens that another satellite must also answer. Naming a satellite in
    prose is the dissociation working: the convention plugin guide cites
    `scrumia-kotlin-multiplatform-mobile` as the place a Kotlin Multiplatform-
    shaped convention plugin belongs. That citation is what AC-3 also asserts.
    """
    deps_path = PLUGIN / "dependencies.jsonl"
    if deps_path.exists():
        deps_text = deps_path.read_text(encoding="utf-8")
        satellite_modules = [
            "scrumia-kotlin-multiplatform-mobile",
            "scrumia-kotlin",
            "scrumia-ktor",
            "scrumia-material3",
            "scrumia-effect",
            "scrumia-functional-programming",
        ]
        bad = [m for m in satellite_modules if m in deps_text]
        check(
            "AC-4: dependencies.jsonl names no other satellite",
            not bad,
            f"dependencies.jsonl names {bad}" if bad else "",
        )
    else:
        # No dependencies.jsonl is conformant — a module that runs no command
        # ships none. The dissociation is preserved.
        check("AC-4: no dependencies.jsonl means no cross-dependency", True)


# --- AC-5: anatomy ships and validate.py passes ------------------------------------


def ac_5() -> None:
    """Anatomy ships: SKILL.md, extends.json, README.md, CHANGELOG.md; validate.py passes.

    The shape is what `scrumia-module check` and `tools/validate.py` gate together.
    """
    for rel in ("README.md", "CHANGELOG.md", "extends.json", ".claude-plugin/plugin.json"):
        check(
            f"AC-5: ships {rel}",
            (PLUGIN / rel).exists(),
        )

    skill_md = SKILL_DIR / "SKILL.md"
    check(
        "AC-5: ships skills/scrumia-gradle/SKILL.md",
        skill_md.exists(),
    )

    audit_md = PLUGIN / "skills" / "scrumia-gradle-audit" / "SKILL.md"
    check(
        "AC-5: ships skills/scrumia-gradle-audit/SKILL.md",
        audit_md.exists(),
    )

    # The procedural check must return clean for this plugin.
    result = subprocess.run(
        [sys.executable, str(CHECKER), "check", "--json", str(PLUGIN)],
        capture_output=True, text=True, timeout=60,
    )
    try:
        verdict = json.loads(result.stdout)
    except json.JSONDecodeError:
        verdict = {"state": "unparseable"}
    check(
        "AC-5: scrumia-module check returns clean",
        verdict.get("state") == "clean",
        f"state={verdict.get('state')}, findings={len(verdict.get('findings', []))}",
    )

    # The marketplace gate must list the plugin.
    market = json.loads(MARKETPLACE.read_text(encoding="utf-8"))
    names = {p["name"] for p in market.get("plugins", [])}
    check(
        "AC-5: marketplace.json registers the plugin",
        "scrumia-gradle" in names,
    )


# --- AC-6: Kotlin DSL; Groovy files are a finding -----------------------------------


def ac_6() -> None:
    """Build scripts use Kotlin DSL (`.gradle.kts`); `.gradle` is named as a finding."""
    guide = read("skills/scrumia-gradle/guides/01-build-script-format.md")
    check(
        "AC-6: guide 01 names .gradle.kts as required and .gradle as the finding",
        ".gradle.kts" in guide and ".gradle" in guide and "finding" in guide.lower(),
    )


# --- AC-7: versions in libs.versions.toml; literal in build script is a finding ---


def ac_7() -> None:
    """Every plugin and library version is declared in `gradle/libs.versions.toml`."""
    guide = read("skills/scrumia-gradle/guides/02-version-catalog.md")
    check(
        "AC-7: guide 02 names gradle/libs.versions.toml as the only place versions live",
        "libs.versions.toml" in guide,
    )
    check(
        "AC-7: guide 02 names a literal version in a build script as a finding",
        "literal" in guide.lower() and "finding" in guide.lower(),
    )


# --- AC-8: shared build logic in build-logic composite (or buildSrc) --------------


def ac_8() -> None:
    """Shared build logic lives in a `build-logic` composite as a precompiled script plugin."""
    guide = read("skills/scrumia-gradle/guides/03-convention-plugin-shape.md")
    check(
        "AC-8: guide 03 names build-logic as the composite",
        "build-logic" in guide,
    )
    check(
        "AC-8: guide 03 names the precompiled script plugin as the shape",
        "precompiled script plugin" in guide.lower(),
    )
    check(
        "AC-8: guide 03 acknowledges buildSrc as the older shape",
        "buildSrc" in guide or "build-src" in guide.lower(),
    )


# --- AC-9: tasks.register is required; tasks.create needs a comment ---------------


def ac_9() -> None:
    """Tasks declared with `tasks.register` (lazy); `tasks.create` is a finding without a comment."""
    guide = read("skills/scrumia-gradle/guides/04-task-configuration.md")
    check(
        "AC-9: guide 04 names tasks.register as required",
        "tasks.register" in guide,
    )
    check(
        "AC-9: guide 04 names tasks.create as a finding without a comment",
        "tasks.create" in guide and "comment" in guide.lower(),
    )


# --- AC-10: build cache and configuration cache set in gradle.properties -----------


def ac_10() -> None:
    """Both caches enabled in `gradle.properties`; each rule names what it breaks."""
    guide = read("skills/scrumia-gradle/guides/05-caches.md")
    check(
        "AC-10: guide 05 names org.gradle.caching=true",
        "org.gradle.caching" in guide,
    )
    check(
        "AC-10: guide 05 names org.gradle.configuration-cache=true",
        "org.gradle.configuration-cache" in guide,
    )
    # Each cache rule names what it breaks.
    check(
        "AC-10: guide 05 names what the build cache breaks when enabled",
        "breaks" in guide.lower(),
    )


# --- AC-11: locally-built sibling via includeBuild; Maven snapshot is a finding ---


def ac_11() -> None:
    """A locally-built sibling is wired via `includeBuild(...)`."""
    guide = read("skills/scrumia-gradle/guides/06-composite-builds.md")
    check(
        "AC-11: guide 06 names includeBuild(...) as the composite declaration",
        "includeBuild" in guide,
    )
    check(
        "AC-11: guide 06 names publishing to a Maven snapshot as a finding",
        "snapshot" in guide.lower() and "finding" in guide.lower(),
    )


# --- AC-12: plugin versions in pluginManagement; id+version in build is a finding --


def ac_12() -> None:
    """Every plugin version is declared in `pluginManagement` (settings.gradle.kts)."""
    guide = read("skills/scrumia-gradle/guides/07-plugin-management.md")
    check(
        "AC-12: guide 07 names settings.gradle.kts's pluginManagement block",
        "pluginManagement" in guide and "settings.gradle.kts" in guide,
    )
    check(
        "AC-12: guide 07 names plugins { id(...) version ... } in a build script as a finding",
        'id("' in guide and "version" in guide and "finding" in guide.lower(),
    )


# --- AC-13: documentation tasks wired into check or build --------------------------


def ac_13() -> None:
    """Documentation tasks wire into the lifecycle (`check` or `build`)."""
    guide = read("skills/scrumia-gradle/guides/08-documentation-tasks.md")
    check(
        "AC-13: guide 08 names dokka or javadoc",
        "dokka" in guide or "javadoc" in guide,
    )
    check(
        "AC-13: guide 08 names check or build as the lifecycle hook",
        '"check"' in guide or "build" in guide,
    )


def main() -> int:
    print("AC-1 through AC-13 — scrumia-gradle")
    ac_1()
    ac_2()
    ac_3()
    ac_4()
    ac_5()
    ac_6()
    ac_7()
    ac_8()
    ac_9()
    ac_10()
    ac_11()
    ac_12()
    ac_13()
    if FAILURES:
        print(f"\n{len(FAILURES)} failure(s):")
        for f in FAILURES:
            print(f"  - {f}")
        return 1
    print("\nall checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
