#!/usr/bin/env python3
"""Tests for the home page's composer (#56).

Run from anywhere: python3 tools/test_composer.py
Exit code 0 when everything passes, 1 otherwise. No dependencies.

The composer states its result twice: once in the rows a reader chooses from,
and once in the two files pre-rendered in the template so the takeaway is
correct with no script running. Nothing in the browser keeps those two in step
— composer.js only rewrites the files *after* the first change — so a default
edited on one side and not the other ships a page whose install commands do not
match the composition it claims. That is what these checks are for.

The module and practice tables are read out of composer.js rather than restated
here: re-deriving them would test the test.
"""

import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
PAGES = {"en": REPO / "site" / "index.html", "fr": REPO / "site" / "fr" / "index.html"}
COMPOSER_JS = REPO / "site" / "assets" / "composer.js"

FAILURES: list[str] = []


def check(name: str, condition: bool, detail: str = "") -> None:
    if condition:
        print(f"  ok   {name}")
    else:
        FAILURES.append(f"{name}{': ' + detail if detail else ''}")
        print(f"  FAIL {name}{': ' + detail if detail else ''}")


# --- reading composer.js's tables --------------------------------------------


def js_object(name: str) -> dict:
    """Lift one `var NAME = { ... };` literal out of composer.js as data."""
    source = COMPOSER_JS.read_text(encoding="utf-8")
    match = re.search(rf"var {name} = (\{{.*?\n  \}});", source, re.DOTALL)
    if not match:
        raise SystemExit(f"composer.js: no `var {name} = {{...}};` to read")
    body = match.group(1)
    body = re.sub(r"^(\s*)//.*$", "", body, flags=re.MULTILINE)
    body = re.sub(r"(\w+):", r'"\1":', body)          # bare keys → JSON keys
    body = body.replace("'", '"')
    body = re.sub(r",(\s*[}\]])", r"\1", body)        # no trailing commas in JSON
    return json.loads(body)


APPS = js_object("APPS")
PRACTICES = js_object("PRACTICES")


# --- reading the page --------------------------------------------------------


class Composer(HTMLParser):
    """The composer's inputs and its two pre-rendered files."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.inputs: list[dict] = []
        self.pre: dict[str, str] = {}
        self.details_names: list[str] = []
        self._depth = 0          # >0 while inside <section id="composer">
        self._pre_id: str | None = None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "section" and a.get("id") == "composer":
            self._depth = 1
            return
        if not self._depth:
            return
        if tag == "section":
            self._depth += 1
        elif tag == "input":
            self.inputs.append({"name": a.get("name", ""), "value": a.get("value", ""),
                                "checked": "checked" in a})
        elif tag == "details":
            self.details_names.append(a.get("name", ""))
        elif tag == "pre" and a.get("id"):
            self._pre_id = a["id"]
            self.pre[self._pre_id] = ""

    def handle_endtag(self, tag):
        if tag == "pre":
            self._pre_id = None
        elif tag == "section" and self._depth:
            self._depth -= 1

    def handle_data(self, data):
        if self._pre_id is not None:
            self.pre[self._pre_id] += data

    def checked(self, name: str) -> list[str]:
        return [i["value"] for i in self.inputs if i["name"] == name and i["checked"]]

    def groups(self) -> set[str]:
        return {i["name"] for i in self.inputs if i["name"]}


def read(page: Path) -> Composer:
    parser = Composer()
    parser.feed(page.read_text(encoding="utf-8"))
    return parser


SINGLE = ["specs", "tracker", "team", "discovery", "design"]


def expected_modules(c: Composer) -> list[str]:
    modules = ["scrumia-core"]
    for slot in SINGLE:
        value = (c.checked("c-" + slot) or [""])[0]
        if value and value != "other":
            modules.append(value)
    for stack in c.checked("c-impl"):
        impl = APPS[stack]["impl"]
        if impl:
            modules.append(impl)
    for practice in c.checked("c-practice"):
        modules.append(PRACTICES[practice]["module"])
    return list(dict.fromkeys(modules))


# --- the checks --------------------------------------------------------------


def test_ac3_install_block_matches_the_rows() -> None:
    print("AC-3 the pre-rendered install block installs exactly what the rows chose")
    for lang, page in PAGES.items():
        c = read(page)
        printed = re.findall(r"^/plugin install (\S+)@scrumia$", c.pre["composer-install"],
                             re.MULTILINE)
        check(f"{lang}: install lines match the checked options",
              printed == expected_modules(c), f"{printed} != {expected_modules(c)}")


def test_ac3_config_block_matches_the_rows() -> None:
    print("AC-3 the pre-rendered config declares exactly what the rows chose")
    for lang, page in PAGES.items():
        c = read(page)
        config = c.pre["composer-config"]

        for slot in SINGLE:
            value = (c.checked("c-" + slot) or [""])[0]
            want = value if value and value != "other" else "null"
            line = re.search(rf"^  {slot}: (\S+)", config, re.MULTILINE)
            check(f"{lang}: composition.{slot} is {want}",
                  line is not None and line.group(1) == want,
                  f"got {line.group(1) if line else 'no line'}")

        stacks = c.checked("c-impl")
        names = re.findall(r"^  - name: (\S+)$", config, re.MULTILINE)
        check(f"{lang}: one apps[] entry per checked stack",
              names == [APPS[s]["name"] for s in stacks],
              f"{names} != {[APPS[s]['name'] for s in stacks]}")

        # A practice belongs only under the app types it speaks for: a backend
        # declaring a frontend data-fetching practice is the bug this catches.
        chosen = [PRACTICES[p] for p in c.checked("c-practice")]
        blocks = re.findall(r"^  - name: \S+\n    path: \S+\n    type: (\S+)\n"
                            r"    implementation: (\S+)\n    practices: \[(.*)\]$",
                            config, re.MULTILINE)
        check(f"{lang}: every apps[] entry parses", len(blocks) == len(names),
              f"{len(blocks)} of {len(names)}")
        for app_type, _impl, listed in blocks:
            want = [p["module"] for p in chosen if app_type in p["types"]]
            got = [m for m in listed.split(", ") if m]
            check(f"{lang}: {app_type} app carries only its own practices",
                  got == want, f"{got} != {want}")


def test_ac5_the_two_indexes_stay_two_accordions() -> None:
    print("AC-5 the composer's rows are grouped apart from the reporting index")
    for lang, page in PAGES.items():
        c = read(page)
        check(f"{lang}: seven rows, all named composer-slot",
              c.details_names == ["composer-slot"] * 7, str(c.details_names))


def test_ac6_no_slot_is_answered_without_being_asked() -> None:
    print("AC-6 every single-fill slot is asked, and answered exactly once")
    for lang, page in PAGES.items():
        c = read(page)
        for slot in SINGLE:
            picked = c.checked("c-" + slot)
            check(f"{lang}: {slot} has exactly one default answer",
                  len(picked) == 1, f"{len(picked)} checked")
        check(f"{lang}: no input group beyond the seven slots",
              c.groups() == {"c-" + s for s in SINGLE} | {"c-impl", "c-practice"},
              str(sorted(c.groups())))


def main() -> int:
    for test in (test_ac3_install_block_matches_the_rows,
                 test_ac3_config_block_matches_the_rows,
                 test_ac5_the_two_indexes_stay_two_accordions,
                 test_ac6_no_slot_is_answered_without_being_asked):
        test()
    print()
    if FAILURES:
        print(f"{len(FAILURES)} failure(s)")
        return 1
    print("all checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
