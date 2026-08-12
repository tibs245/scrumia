#!/usr/bin/env python3
"""Tests for the home page's composer (#56).

Run from anywhere: python3 tools/test_composer.py
Exit code 0 when everything passes, 1 otherwise. Needs PyYAML, which the site
build already requires: the config block is parsed rather than pattern-matched,
so a key this repo quotes wrongly fails here instead of at whoever pastes it.

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

import yaml

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


def js_string(name: str) -> str:
    """Lift one `var NAME = '...';` literal out of composer.js."""
    match = re.search(rf"var {name} = '([^']*)';", COMPOSER_JS.read_text(encoding="utf-8"))
    if not match:
        raise SystemExit(f"composer.js: no `var {name} = '...';` to read")
    return match.group(1)


APPS = js_object("APPS")
PRACTICES = js_object("PRACTICES")
SOURCE = js_string("SOURCE")


def source_key(module: str) -> str:
    return f"{SOURCE}:{module}"


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
                                "checked": "checked" in a, "note": a.get("data-note", "")})
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
        try:
            config = yaml.safe_load(c.pre["composer-config"])
        except yaml.YAMLError as e:
            check(f"{lang}: the config block is YAML", False, str(e))
            continue
        check(f"{lang}: the config block is YAML", isinstance(config, dict))

        want = [source_key(v) for v in
                ((c.checked("c-" + s) or [""])[0] for s in SINGLE)
                if v and v != "other"]
        got = list((config.get("modules") or {}).keys())
        check(f"{lang}: modules: holds one key per slot answered with a module",
              got == want, f"{got} != {want}")

        stacks = c.checked("c-impl")
        apps = config.get("apps") or []
        names = [a.get("name") for a in apps]
        check(f"{lang}: one apps[] entry per checked stack",
              names == [APPS[s]["name"] for s in stacks],
              f"{names} != {[APPS[s]['name'] for s in stacks]}")

        # A practice belongs only under the app types it speaks for: a backend
        # declaring a frontend data-fetching practice is the bug this catches.
        chosen = [PRACTICES[p] for p in c.checked("c-practice")]
        for stack, app in zip(stacks, apps, strict=True):
            impl = APPS[stack]["impl"]
            app_type = app.get("type")
            want = [source_key(m) for m in
                    ([impl] if impl else []) +
                    [p["module"] for p in chosen if app_type in p["types"]]]
            got = list((app.get("modules") or {}).keys())
            check(f"{lang}: the {app_type} app declares its stack and only its own practices",
                  got == want, f"{got} != {want}")


def test_ac3_every_key_is_source_qualified() -> None:
    print("AC-3 every emitted key is <source>:<module>, and the source is a real one")
    for lang, page in PAGES.items():
        c = read(page)
        try:
            config = yaml.safe_load(c.pre["composer-config"])
        except yaml.YAMLError as e:
            check(f"{lang}: the config block is YAML", False, str(e))
            continue
        keys = list((config.get("modules") or {}).keys())
        for app in config.get("apps") or []:
            keys += list((app.get("modules") or {}).keys())
        check(f"{lang}: the config declares at least one module", bool(keys))
        for key in keys:
            source, _, module = key.rpartition(":")
            # BR-13's three sources; a bare name is a key nothing resolves.
            valid = module and (source in ("local", "shared")
                                or re.fullmatch(r"[^/]+/[^/]+", source))
            check(f"{lang}: '{key}' is keyed by its source", bool(valid))
        check(f"{lang}: every value is an empty mapping — the composer writes no params",
              all(v == {} for v in (config.get("modules") or {}).values()))


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

        # The note is the whole of its line now: one that lost its `#` is parsed
        # as configuration rather than read as a weaker statement of the cost.
        for slot in SINGLE:
            for i in c.inputs:
                if i["name"] == "c-" + slot and i["value"] in ("", "other"):
                    label = i["value"] or "empty"
                    check(f"{lang}: {slot}'s '{label}' option states its consequence",
                          bool(i["note"]), "no data-note")
                    check(f"{lang}: {slot}'s '{label}' consequence is a YAML comment",
                          i["note"].startswith("#"), repr(i["note"][:40]))


def main() -> int:
    for test in (test_ac3_install_block_matches_the_rows,
                 test_ac3_config_block_matches_the_rows,
                 test_ac3_every_key_is_source_qualified,
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
