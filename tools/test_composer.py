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
STYLE_CSS = REPO / "site" / "assets" / "style.css"
MODULES_JSON = REPO / "site" / "modules.json"
KERNEL = "scrumia-core"

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


def js_regex(name: str) -> re.Pattern:
    """Lift one `var NAME = /.../;` literal out of composer.js and compile it here.

    The shipped pattern is what gets exercised. A copy of it restated in this file
    would only ever test itself, which is how a guard passes while the thing it
    guards is wrong.
    """
    match = re.search(rf"var {name} = /(.+?)/;", COMPOSER_JS.read_text(encoding="utf-8"))
    if not match:
        raise SystemExit(f"composer.js: no `var {name} = /.../;` to read")
    return re.compile(match.group(1))


APPS = js_object("APPS")
PRACTICES = js_object("PRACTICES")
SOURCE = js_string("SOURCE")


def source_key(module: str) -> str:
    return f"{SOURCE}:{module}"


# --- reading the page --------------------------------------------------------


VOID = {"input", "br", "img", "hr", "meta", "link", "source", "area", "col", "embed", "wbr"}


class Composer(HTMLParser):
    """The composer's inputs, its additions block and its two pre-rendered files."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.inputs: list[dict] = []
        self.strings: dict[str, str] = {}
        self.pre: dict[str, str] = {}
        self.details_names: list[str] = []
        self.additions: list[dict] = []   # every element inside #composer-additions
        self._depth = 0          # >0 while inside <section id="composer">
        self._add_depth = 0      # >0 while inside the additions block
        self._pre_id: str | None = None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "section" and a.get("id") == "composer":
            self._depth = 1
            return
        if a.get("id") == "composer-strings":
            self.strings = {k[5:]: v for k, v in a.items() if k.startswith("data-")}
        if not self._depth:
            return
        if "additions" in a.get("class", "").split():
            self._add_depth = 1
        elif self._add_depth and tag not in VOID:
            self._add_depth += 1
        if self._add_depth:
            self.additions.append({"tag": tag, "class": a.get("class", ""),
                                   "name": a.get("name", ""), "value": a.get("value", "")})
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
        if self._add_depth and tag not in VOID:
            self._add_depth -= 1

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
        check(f"{lang}: no input group beyond the seven slots and the additions block",
              c.groups() == {"c-" + s for s in SINGLE} | {"c-impl", "c-practice", "c-add", "c-free"},
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

        # Every #composer-strings entry the script writes into a YAML line; the
        # rest of that element is prose for the notes paragraph, which is not one.
        for key in ("marketplace", "install", "then-init", "config", "project", "app-empty"):
            value = c.strings.get(key, "")
            check(f"{lang}: composer-strings' {key} is a YAML comment",
                  value.startswith("#"), repr(value[:40]))


def offered_additions() -> list[str]:
    """The modules the composer must offer past the seven slots, derived the way
    build_site.py derives them: everything filling no slot, minus the kernel.

    Derived here too, deliberately. A test naming `scrumia-rules` would go on
    passing the day a thirteenth module fills no slot and is never offered — which
    is the failure mode a list validated entry by entry never catches.
    """
    data = json.loads(MODULES_JSON.read_text(encoding="utf-8"))
    return sorted(name for name, facts in data.items()
                  if not name.startswith("_") and not facts.get("slot") and name != KERNEL)


def test_ac9_the_shelf_offers_every_module_that_fills_no_slot() -> None:
    print("AC-9 the additions shelf is exactly the slot-less modules, minus the kernel")
    want = offered_additions()
    check("site/modules.json has something to offer", bool(want))
    for lang, page in PAGES.items():
        c = read(page)
        got = sorted(i["value"] for i in c.inputs if i["name"] == "c-add")
        check(f"{lang}: the shelf offers exactly the modules that fill no slot",
              got == want, f"{got} != {want}")
        # The kernel is installed unconditionally, so offering it would describe a
        # choice the visitor does not have.
        check(f"{lang}: the kernel is not offered", KERNEL not in got)
        check(f"{lang}: no addition is checked by default — picking none is complete",
              not [i for i in c.inputs if i["name"] == "c-add" and i["checked"]])


def test_ac9_the_additions_block_is_a_shelf_not_an_eighth_row() -> None:
    print("AC-9 the additions block carries no sign, no leader, no fill and no <details>")
    for lang, page in PAGES.items():
        c = read(page)
        check(f"{lang}: the block is in the page", bool(c.additions))
        drawn = [e for e in c.additions if e["tag"] in ("details", "summary")
                 or any(k in e["class"] for k in ("slot-sign", "slot-lead", "slot-fill", "slot-row"))]
        check(f"{lang}: nothing in the block draws a slot row", not drawn, str(drawn))
        check(f"{lang}: it is built from .shelf and .opt, like a row's own body",
              any("shelf" in e["class"] for e in c.additions)
              and any("opt" in e["class"].split() for e in c.additions))


def test_ac10_the_visitors_own_module_reaches_the_config_and_only_the_config() -> None:
    print("AC-10 no install command is emitted for a module the site does not ship")
    js = COMPOSER_JS.read_text(encoding="utf-8")
    body = re.search(r"function installParts\(result\) \{(.*?)\n  \}", js, re.DOTALL)
    check("installParts is readable", bool(body))
    if body:
        # It prints `result.modules` and nothing else, and `compute` keeps the
        # visitor's own key out of that list — so the omission is structural rather
        # than a line someone has to remember not to add.
        check("the install block prints result.modules alone",
              "result.modules" in body.group(1) and "result.own" not in body.group(1),
              body.group(1).strip()[:120])
    compute = re.search(r"function compute\(\) \{(.*?)\n  \}", js, re.DOTALL)
    check("compute is readable", bool(compute))
    if compute:
        check("compute returns the own key beside the module list, never inside it",
              "own: ownEntry" in compute.group(1)
              and not re.search(r"modules\.push\(\s*own", compute.group(1)))
        # Structural: the emission only differs after an interaction, and this suite
        # has no JS engine to drive one.
        check("a key the mapping already carries is dropped rather than duplicated",
              re.search(r"modules\.indexOf\(ownEntry.*?\)\s*!==\s*-1", compute.group(1))
              is not None, compute.group(1)[-300:])


def test_ac10_a_key_with_no_source_is_refused() -> None:
    print("AC-10 the free entry takes <source>:<module> and refuses everything else")
    key = js_regex("KEY")
    accept = ["local:acme-docs-rules", "shared:acme-conventions",
              "tibs245/scrumia:scrumia-rules", "acme/market:their_module.v2"]
    # The first is the one the ticket names: a bare name is refused rather than
    # assumed published. The rest are keys that would break the file they land in.
    refuse = ["acme-docs-rules", "local:", ":acme-rules", "local:acme rules",
              "local:acme:rules", "acme:docs", "/x:y", "x/:y", "local:acme/rules",
              '"local:x"', "local:x#y", "", "  ", "shared :x"]
    for value in accept:
        check(f"accepts {value!r}", bool(key.fullmatch(value)))
    for value in refuse:
        check(f"refuses {value!r}", not key.fullmatch(value))


def test_ac11_the_free_entry_is_the_only_thing_gated_on_script() -> None:
    print("AC-11 the free entry needs script; the seven rows and the shelf do not")
    # Prose discusses these selectors, and a sentence is not a rule.
    css = re.sub(r"/\*.*?\*/", "", STYLE_CSS.read_text(encoding="utf-8"), flags=re.DOTALL)
    head = (REPO / "site" / "templates" / "partials" / "head.html").read_text(encoding="utf-8")

    # `.js` means script AND motion wanted, so a capability gated on it would be
    # deleted by a motion preference. `.has-js` means script alone.
    check("head.html sets a gate that means script alone",
          "classList.add('has-js')" in head)
    check("and still sets the motion-aware gate separately", "classList.add('js')" in head)

    gated = [s.strip() for s in re.findall(r"^([^{}]*\.has-js[^{}]*)\{", css, re.MULTILINE)]
    check("the capability gate is used", bool(gated))
    # The class, not the instances: anything else put behind this gate later fails
    # here, because the seven rows and the known additions must keep working alone.
    for selector in gated:
        check(f"only the free entry sits behind the gate: {selector!r}", "opt-free" in selector)
    check("nothing about the free entry is gated on the motion class instead",
          not re.search(r"\.js\s+[^{}]*(opt-free|key-entry)[^{}]*\{", css))

    check("the option is absent until then",
          bool(re.search(r"^\.opt-free \{[^{}]*display: none", css, re.MULTILINE)))
    check("and its field is revealed only by a checked box, never by script",
          bool(re.search(r"^\.key-entry \{[^{}]*display: none", css, re.MULTILINE))
          and bool(re.search(r"^\.opt-free:has\(> input:checked\) \.key-entry \{", css, re.MULTILINE)))

    for lang, page in PAGES.items():
        c = read(page)
        free = [i for i in c.inputs if i["name"] == "c-free"]
        check(f"{lang}: the block carries exactly one free entry", len(free) == 1)
        check(f"{lang}: it is unchecked at rest, so the section holds no open box",
              bool(free) and not free[0]["checked"])
        opts = [e for e in c.additions if "opt" in e["class"].split()]
        check(f"{lang}: it is the shelf's last option",
              bool(opts) and "opt-free" in opts[-1]["class"], str([o["class"] for o in opts]))
        check(f"{lang}: the field carries a label of its own, not a placeholder alone",
              any("key-entry-label" in e["class"] for e in c.additions))


def main() -> int:
    for test in (test_ac3_install_block_matches_the_rows,
                 test_ac3_config_block_matches_the_rows,
                 test_ac3_every_key_is_source_qualified,
                 test_ac5_the_two_indexes_stay_two_accordions,
                 test_ac6_no_slot_is_answered_without_being_asked,
                 test_ac9_the_shelf_offers_every_module_that_fills_no_slot,
                 test_ac9_the_additions_block_is_a_shelf_not_an_eighth_row,
                 test_ac10_the_visitors_own_module_reaches_the_config_and_only_the_config,
                 test_ac10_a_key_with_no_source_is_refused,
                 test_ac11_the_free_entry_is_the_only_thing_gated_on_script):
        test()
    print()
    if FAILURES:
        print(f"{len(FAILURES)} failure(s)")
        return 1
    print("all checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
