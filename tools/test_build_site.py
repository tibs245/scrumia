#!/usr/bin/env python3
"""Tests for the module-page family of tools/build_site.py.

Run from anywhere: python3 tools/test_build_site.py
Exit code 0 when everything passes, 1 otherwise. No dependencies.

The failure modes run against a throwaway fixture tree, not the repo: a guard is
only proven by a build that actually fails, and the repo's own build must pass.
"""

import json
import shutil
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_site as bs  # noqa: E402

REPO = Path(__file__).resolve().parent.parent
FAILURES: list[str] = []


def check(name: str, condition: bool, detail: str = "") -> None:
    if condition:
        print(f"  ok   {name}")
    else:
        FAILURES.append(f"{name}{': ' + detail if detail else ''}")
        print(f"  FAIL {name}{': ' + detail if detail else ''}")


# --- fixture -----------------------------------------------------------------

STUB_TEMPLATE = """<!doctype html>
<html lang="{{@lang}}"><head><title>{{title}}</title></head>
<body><h1>{{@mod_emoji}} {{@mod_name}}</h1>
<p>{{@mod_slot}} {{@mod_version}}</p>
<ul>{{@mod_skills}}</ul>
<ul>{{@mod_tags}}</ul>
<code>{{@mod_install}}</code><a href="{{@mod_source}}">src</a>
<div>{{responsibilities}}</div>
{{@mod_connects}}
{{@mod_pairs}}
</body></html>
"""


def make_fixture(root: Path, plugins=("alpha", "beta"), extra=None, prose=None, tags=("t",),
                  prose_extra=None) -> None:
    """A miniature site: two plugins, one stub template, one prose file per language."""
    (root / ".claude-plugin").mkdir(parents=True)
    (root / ".claude-plugin" / "marketplace.json").write_text(json.dumps({
        "name": "fixture",
        "plugins": [{"name": p, "version": "1.0.0", "tags": list(tags)} for p in plugins],
    }), encoding="utf-8")

    for p in plugins:
        skill = root / "plugins" / p / "skills" / f"{p}-skill"
        skill.mkdir(parents=True)
        (skill / "SKILL.md").write_text("---\nname: x\n---\n", encoding="utf-8")

    # The builder mirrors the design vocabulary into the site; without one here,
    # every fixture build would report a missing tokens file as a real error.
    (root / "design").mkdir(parents=True)
    (root / "design" / "tokens.css").write_text(":root { --x: 0 }\n", encoding="utf-8")

    site = root / "site"
    (site / "templates" / "partials").mkdir(parents=True)
    (site / "assets").mkdir(parents=True)
    (site / "templates" / "module.html").write_text(STUB_TEMPLATE, encoding="utf-8")
    (site / "modules.json").write_text(json.dumps(
        extra if extra is not None else {p: {"emoji": e, "slot": None} for p, e in zip(plugins, "🅰🅱🅲🅳")}
    ), encoding="utf-8")

    for lang in ("en", "fr"):
        d = site / "i18n" / lang
        (d / "modules").mkdir(parents=True)
        (d / "common.json").write_text(json.dumps({"mod_no_slot": "none"}), encoding="utf-8")
        for p in plugins:
            body = prose if prose is not None else {"title": f"{p} [{lang}]", "responsibilities": "<p>r</p>"}
            if prose_extra and p in prose_extra:
                body = {**body, **prose_extra[p]}
            (d / "modules" / f"{p}.json").write_text(json.dumps(body), encoding="utf-8")


def run_fixture(root: Path) -> tuple[int, list[str]]:
    """Point the builder at the fixture and build only the module pages."""
    bs.ROOT, bs.SITE = root, root / "site"
    bs.TPL, bs.I18N = bs.SITE / "templates", bs.SITE / "i18n"
    bs.MARKETPLACE = root / ".claude-plugin" / "marketplace.json"
    bs.MODULES_DATA = bs.SITE / "modules.json"
    bs.TOKENS_SRC = root / "design" / "tokens.css"
    bs.TOKENS_OUT = bs.SITE / "assets" / "tokens.css"
    bs.PAGES = []
    bs.LANGS = {
        "en": {"out": bs.SITE, "prefix": "", "root": ""},
        "fr": {"out": bs.SITE / "fr", "prefix": "fr/", "root": "../"},
    }
    bs.ERRORS.clear()
    code = bs.build()
    return code, list(bs.ERRORS)


def with_fixture(**kwargs) -> tuple[int, list[str], Path]:
    tmp = Path(tempfile.mkdtemp())
    make_fixture(tmp, **kwargs)
    code, errors = run_fixture(tmp)
    return code, errors, tmp


# --- AC-1 --------------------------------------------------------------------


def test_ac1_one_page_per_plugin_per_language() -> None:
    print("AC-1 the pages generate from one template and one fact source")
    market = json.loads((REPO / ".claude-plugin" / "marketplace.json").read_text(encoding="utf-8"))
    names = [p["name"] for p in market["plugins"]]
    check("one template, not one per module", (REPO / "site" / "templates" / "module.html").exists())
    missing = [f"{lang}/{n}" for n in names
               for lang, base in (("en", REPO / "site"), ("fr", REPO / "site" / "fr"))
               if not (base / "modules" / f"{n}.html").exists()]
    check(f"{len(names) * 2} committed module pages", not missing, f"missing {missing}")
    for name in names:
        page = (REPO / "site" / "modules" / f"{name}.html").read_text(encoding="utf-8")
        check(f"{name} carries the manifest facts",
              f"/plugin install {name}@scrumia" in page and f"/tree/main/plugins/{name}" in page)

    code, errors, tmp = with_fixture()
    check("a stub template is enough to build (AC-5)", code == 0, str(errors))
    check("the stub pages land in both languages",
          (tmp / "site" / "modules" / "alpha.html").exists() and (tmp / "site" / "fr" / "modules" / "beta.html").exists())
    shutil.rmtree(tmp)


# --- AC-2 --------------------------------------------------------------------


def test_ac2_guards() -> None:
    print("AC-2 a missing string, an unused string, an orphan file or a plugin without prose fails the build")

    code, errors, tmp = with_fixture()
    (tmp / "site" / "i18n" / "fr" / "modules" / "beta.json").unlink()
    bs.ERRORS.clear()
    code = bs.build()
    check("a plugin with no prose in one language fails",
          code == 1 and any("fr/modules/beta.json" in e and "missing" in e for e in bs.ERRORS), str(bs.ERRORS))
    shutil.rmtree(tmp)

    code, errors, tmp = with_fixture()
    (tmp / "site" / "i18n" / "en" / "modules" / "ghost.json").write_text("{}", encoding="utf-8")
    bs.ERRORS.clear()
    code = bs.build()
    check("an i18n file naming no plugin fails",
          code == 1 and any("ghost.json" in e for e in bs.ERRORS), str(bs.ERRORS))
    shutil.rmtree(tmp)

    code, errors, tmp = with_fixture(prose={"title": "t"})  # responsibilities is missing
    check("a string the template needs and a language lacks fails",
          code == 1 and any("missing string 'responsibilities'" in e for e in errors), str(errors))
    shutil.rmtree(tmp)

    code, errors, tmp = with_fixture(
        prose={"title": "t", "responsibilities": "<p>r</p>", "ghost_key": "leftover"})
    check("a page-level string no template reads fails the build (#114)",
          code == 1 and any("unused string 'ghost_key'" in e for e in errors), str(errors))
    shutil.rmtree(tmp)


# --- AC-3 --------------------------------------------------------------------


def test_ac3_one_file_owns_the_emoji() -> None:
    print("AC-3 exactly one file declares the emoji, and the twelve are unique")

    market = json.loads((REPO / ".claude-plugin" / "marketplace.json").read_text(encoding="utf-8"))
    data = json.loads((REPO / "site" / "modules.json").read_text(encoding="utf-8"))
    entries = {k: v for k, v in data.items() if not k.startswith("_")}
    emojis = [v["emoji"] for v in entries.values()]
    check("every module declares one", all(emojis) and len(emojis) == len(market["plugins"]), str(len(emojis)))
    check("no emoji is reused", len(set(emojis)) == len(emojis))

    # Generated HTML is not a source, and the favicon is the site's own mark.
    sources = [REPO / ".claude-plugin" / "marketplace.json",
               *(REPO / "site" / "templates").rglob("*.html"),
               *(REPO / "site" / "i18n").rglob("*.json")]
    restating = sorted({str(f.relative_to(REPO)) for f in sources
                        for e in emojis
                        if e in "\n".join(l for l in f.read_text(encoding="utf-8").splitlines()
                                          if 'rel="icon"' not in l)})
    check("no other source file restates one", not restating, str(restating))

    code, errors, tmp = with_fixture(extra={"alpha": {"emoji": "🅰"}, "beta": {"emoji": "🅰"}})
    check("a reused emoji fails the build",
          code == 1 and any("reuses the emoji" in e for e in errors), str(errors))
    shutil.rmtree(tmp)

    code, errors, tmp = with_fixture(extra={"alpha": {"emoji": "🅰"}})
    check("a plugin with no entry fails the build",
          code == 1 and any("no entry for plugin 'beta'" in e for e in errors), str(errors))
    shutil.rmtree(tmp)

    code, errors, tmp = with_fixture(extra={"alpha": {"emoji": "🅰"}, "beta": {"emoji": "🅱"}, "ghost": {"emoji": "🅲"}})
    check("an entry naming no plugin fails the build",
          code == 1 and any("'ghost' is not a plugin" in e for e in errors), str(errors))
    shutil.rmtree(tmp)


# --- AC-4 --------------------------------------------------------------------


def test_ac4_sitemap() -> None:
    print("AC-4 the sitemap covers the generated pages")
    sitemap = (REPO / "site" / "sitemap.xml").read_text(encoding="utf-8")
    names = [p["name"] for p in json.loads(
        (REPO / ".claude-plugin" / "marketplace.json").read_text(encoding="utf-8"))["plugins"]]
    missing = [u for n in names
               for u in (f"{bs.SITE_URL}modules/{n}.html", f"{bs.SITE_URL}fr/modules/{n}.html")
               if u not in sitemap]
    check("both language URLs per module are listed", not missing, str(missing))


# --- AC-6 --------------------------------------------------------------------


def test_ac6_malformed_page_json_is_reported_not_raised() -> None:
    print("AC-6 a malformed page string file is reported, never raised")

    tmp = Path(tempfile.mkdtemp())
    make_fixture(tmp)
    # load_strings already parses this file under a try; the unused-key reparse
    # in render_page must not raise a second time on the same broken file.
    (tmp / "site" / "i18n" / "en" / "modules" / "alpha.json").write_text("{not json", encoding="utf-8")
    try:
        code, errors = run_fixture(tmp)
        raised = False
    except json.JSONDecodeError:
        code, errors, raised = 1, [], True
    check("build() does not raise on invalid JSON", not raised)
    check("the failure is reported, exit code 1", code == 1)
    check("load_strings' own error is the one reported",
          any("modules/alpha.json" in e and "invalid JSON" in e for e in errors), str(errors))
    shutil.rmtree(tmp)


# --- AC-7 --------------------------------------------------------------------


def test_ac7_manifest_facts_are_escaped() -> None:
    print("AC-7 a manifest fact interpolated into markup is escaped")

    code, errors, tmp = with_fixture(tags=("<b>x</b>",))
    check("a tag with markup still builds", code == 0, str(errors))
    page = (tmp / "site" / "modules" / "alpha.html").read_text(encoding="utf-8")
    check("the raw tag is not in the output", "<li><b>x</b></li>" not in page)
    check("the tag is HTML-escaped", "<li>&lt;b&gt;x&lt;/b&gt;</li>" in page, page)
    shutil.rmtree(tmp)


# --- AC-8 --------------------------------------------------------------------


def test_ac8_index_links_to_every_module() -> None:
    print("AC-8 every module is reachable from the site's navigation")
    market = json.loads((REPO / ".claude-plugin" / "marketplace.json").read_text(encoding="utf-8"))
    names = [p["name"] for p in market["plugins"]]

    for lang, index in (("en", REPO / "site" / "index.html"), ("fr", REPO / "site" / "fr" / "index.html")):
        page = index.read_text(encoding="utf-8")
        missing = [n for n in names if f'<a class="mod-name" href="modules/{n}.html">{n}</a>' not in page]
        check(f"[{lang}] every module card links to its page", not missing, str(missing))


# --- AC-9 --------------------------------------------------------------------


def test_ac9_link_is_generated_not_hand_written() -> None:
    print("AC-9 the link is generated, not twelve hand-written hrefs")

    template = (REPO / "site" / "templates" / "index.html").read_text(encoding="utf-8")
    check("the template carries no literal modules/*.html href",
          'href="modules/' not in template and 'href="{{@lroot}}modules/' not in template)
    check("the template uses one @modlink_<name> special per card",
          template.count("{{@modlink_") == len(
              json.loads((REPO / ".claude-plugin" / "marketplace.json").read_text(encoding="utf-8"))["plugins"]))

    # The special itself comes from a function of the module list, not a name
    # hardcoded anywhere near it — arbitrary module names produce matching hrefs.
    specials = bs.module_link_specials([{"name": "zeta"}, {"name": "a-b-c"}])
    check("the URL is derived from the module name",
          specials == {"@modlink_zeta": "modules/zeta.html", "@modlink_a-b-c": "modules/a-b-c.html"}, str(specials))


# --- AC-10 -------------------------------------------------------------------


def test_ac10_reference_links_to_every_module() -> None:
    print("AC-10 every module is reachable from the reference page too")
    market = json.loads((REPO / ".claude-plugin" / "marketplace.json").read_text(encoding="utf-8"))
    names = [p["name"] for p in market["plugins"]]

    for lang, ref in (("en", REPO / "site" / "reference.html"), ("fr", REPO / "site" / "fr" / "reference.html")):
        page = ref.read_text(encoding="utf-8")
        missing = [n for n in names if f'<h3><a href="modules/{n}.html"><code>{n}</code></a>' not in page]
        check(f"[{lang}] every module heading links to its page", not missing, str(missing))


# --- AC-11 -------------------------------------------------------------------


def test_ac11_reference_link_is_generated_not_hand_written() -> None:
    print("AC-11 the reference page's link is generated too")

    template = (REPO / "site" / "templates" / "reference.html").read_text(encoding="utf-8")
    check("the template carries no literal modules/*.html href",
          'href="modules/' not in template and 'href="{{@lroot}}modules/' not in template)
    check("the template uses one @modlink_<name> special per heading",
          template.count("{{@modlink_") == len(
              json.loads((REPO / ".claude-plugin" / "marketplace.json").read_text(encoding="utf-8"))["plugins"]))


# --- AC-12 -------------------------------------------------------------------


def test_ac12_module_page_shows_what_it_plugs_into() -> None:
    print("AC-12 a module page shows what it plugs into, derived and never declared")

    link_specials = {"@modlink_a": "modules/a.html", "@modlink_b": "modules/b.html", "@modlink_c": "modules/c.html"}
    labels = {"mod_h_plugs_into": "Plugs into", "th_conn_register": "Register",
              "th_conn_direction": "Direction", "th_conn_module": "Module",
              "conn_dir_opens": "opens", "conn_dir_contributes": "contributes",
              "conn_no_contribution": "no contribution"}

    check("a module opening and extending nothing shows no section at all",
          bs.module_connections_html("ghost", {}, {}, link_specials, labels) == "")

    regs = {"reg1": {"module": "a", "skill": "s"}}
    out = bs.module_connections_html("a", regs, {}, link_specials, labels)
    check("a register with no contributor is shown, not omitted (BR-1)",
          '<span class="conn-none">no contribution</span>' in out and out.count("<tbody>") == 1
          and out.split("<tbody>")[1].count("<tr>") == 1, out)

    dirs = {"reg1": [{"module": "b", "name": "x", "summary": "y"}]}
    out = bs.module_connections_html("a", regs, dirs, link_specials, labels)
    check("a contributor is named and linked to its own page",
          '<a href="../modules/b.html"><code>b</code></a>' in out and ">opens<" in out, out)

    out = bs.module_connections_html("b", regs, dirs, link_specials, labels)
    check("the contributing module names the register and the module that opened it",
          '<a href="../modules/a.html"><code>a</code></a>' in out and ">contributes<" in out, out)

    bs.ERRORS.clear()
    bs.module_connections_html("c", {}, {"orphan": [{"module": "c", "name": "x", "summary": "y"}]},
                                link_specials, labels)
    check("a contributed register nobody opens fails the build rather than a dead link",
          any("opened by no module of the marketplace" in e for e in bs.ERRORS), str(bs.ERRORS))
    bs.ERRORS.clear()

    tmp = Path(tempfile.mkdtemp())
    (tmp / "x").mkdir(parents=True)
    (tmp / "x" / "registers.json").write_text(json.dumps({"reg": {"skill": "s"}}), encoding="utf-8")
    (tmp / "y").mkdir(parents=True)
    (tmp / "y" / "extends.json").write_text(json.dumps({"reg": [{"name": "n", "summary": "s"}]}), encoding="utf-8")
    market_map = bs.load_extends_map(["x", "y"], plugins_root=tmp)
    check("a marketplace-wide walk sees both sides, whatever this project's own composition runs",
          market_map["registers"] == {"reg": {"module": "x", "skill": "s"}}
          and market_map["directives"]["reg"][0]["module"] == "y", str(market_map))
    shutil.rmtree(tmp)

    tmp = Path(tempfile.mkdtemp())
    make_fixture(tmp, extra={"alpha": {"emoji": "🅰"}, "beta": {"emoji": "🅱"}})
    (tmp / "plugins" / "alpha" / "registers.json").write_text(json.dumps({"reg": {"skill": "s"}}), encoding="utf-8")
    (tmp / "plugins" / "beta" / "extends.json").write_text(
        json.dumps({"reg": [{"name": "n", "summary": "s"}]}), encoding="utf-8")
    code, errors = run_fixture(tmp)
    check("the full pipeline wires the walk into the module page", code == 0, str(errors))
    page = (tmp / "site" / "modules" / "alpha.html").read_text(encoding="utf-8")
    check("alpha's page names beta, linked to its own page",
          '<a href="../modules/beta.html">' in page and "<code>reg</code>" in page, page)
    shutil.rmtree(tmp)

    core = (REPO / "site" / "modules" / "scrumia-core.html").read_text(encoding="utf-8")
    check("a module declaring neither file carries no plugs-into section",
          '<section id="plugs-into">' not in core, )
    ghp = (REPO / "site" / "modules" / "scrumia-github-project.html").read_text(encoding="utf-8")
    check("the module with the most contributors names all seven, each linked",
          all(f'<a href="../modules/{n}.html">' in ghp for n in
              ("scrumia-design", "scrumia-specs", "scrumia-impl-rust", "scrumia-impl-solidjs",
               "scrumia-practice-solid", "scrumia-practice-tanstack-query", "scrumia-practice-tdd")))
    discovery = (REPO / "site" / "modules" / "scrumia-discovery.html").read_text(encoding="utf-8")
    check("an opened register with no contributor still shows, spelled out",
          discovery.count('<span class="conn-none">no contribution</span>') == 2, discovery)


# --- AC-13 -------------------------------------------------------------------


def test_ac13_module_page_shows_what_it_goes_well_with() -> None:
    print("AC-13 a module page says what it goes well with, and cannot invent one")

    link_specials = {"@modlink_x": "modules/x.html", "@modlink_y": "modules/y.html"}
    labels = {"mod_h_pairs": "Goes well with"}

    out, preused = bs.module_pairs_html("en", {"name": "a", "pairs_with": []}, {}, labels, link_specials)
    check("a module with nothing to say carries no such section", out == "" and preused == set())

    module = {"name": "a", "pairs_with": ["x", "y"]}
    bs.ERRORS.clear()
    out, preused = bs.module_pairs_html("en", module, {}, labels, link_specials)
    check("a declared complement with no prose fails the build rather than a blank line",
          out == "" and any("missing 'pairs_with'" in e for e in bs.ERRORS), str(bs.ERRORS))
    bs.ERRORS.clear()

    out, preused = bs.module_pairs_html("en", module, {"pairs_with": "because:"}, labels, link_specials)
    check("the prose names each complement, linked to its own page",
          '<a href="../modules/x.html"><code>x</code></a>' in out
          and '<a href="../modules/y.html"><code>y</code></a>' in out, out)
    check("the prose is read outside the token engine, marked used so it isn't flagged an orphan",
          preused == {"pairs_with"})

    code, errors, tmp = with_fixture(
        extra={"alpha": {"emoji": "🅰", "pairs_with": ["ghost"]}, "beta": {"emoji": "🅱"}})
    check("a complement naming a module that doesn't exist fails the build",
          code == 1 and any("pairs_with 'ghost'" in e and "not a plugin" in e for e in errors), str(errors))
    shutil.rmtree(tmp)

    code, errors, tmp = with_fixture(
        extra={"alpha": {"emoji": "🅰", "pairs_with": ["alpha"]}, "beta": {"emoji": "🅱"}})
    check("a module naming itself fails the build",
          code == 1 and any("names itself in pairs_with" in e for e in errors), str(errors))
    shutil.rmtree(tmp)

    code, errors, tmp = with_fixture(
        extra={"alpha": {"emoji": "🅰", "pairs_with": ["beta"]}, "beta": {"emoji": "🅱"}},
        prose_extra={"alpha": {"pairs_with": "why:"}})
    check("a complement with its own prose builds clean", code == 0, str(errors))
    page = (tmp / "site" / "modules" / "alpha.html").read_text(encoding="utf-8")
    check("the page names the complement, linked to its own page",
          '<a href="../modules/beta.html">' in page, page)
    beta_page = (tmp / "site" / "modules" / "beta.html").read_text(encoding="utf-8")
    check("beta has nothing to say, so it carries no such section",
          '<section id="pairs-with">' not in beta_page, beta_page)
    shutil.rmtree(tmp)

    core = (REPO / "site" / "modules" / "scrumia-core.html").read_text(encoding="utf-8")
    check("scrumia-core, which declares neither register file, still says what it goes well with",
          '<section id="pairs-with">' in core
          and '<a href="../modules/scrumia-github-project.html">' in core, core)
    ghp = (REPO / "site" / "modules" / "scrumia-github-project.html").read_text(encoding="utf-8")
    check("a module already covered by AC-12's derivation carries no editorial line",
          '<section id="pairs-with">' not in ghp, ghp)


def main() -> int:
    for test in (test_ac1_one_page_per_plugin_per_language, test_ac2_guards,
                 test_ac3_one_file_owns_the_emoji, test_ac4_sitemap,
                 test_ac6_malformed_page_json_is_reported_not_raised,
                 test_ac7_manifest_facts_are_escaped,
                 test_ac8_index_links_to_every_module, test_ac9_link_is_generated_not_hand_written,
                 test_ac10_reference_links_to_every_module,
                 test_ac11_reference_link_is_generated_not_hand_written,
                 test_ac12_module_page_shows_what_it_plugs_into,
                 test_ac13_module_page_shows_what_it_goes_well_with):
        test()
    print()
    if FAILURES:
        print(f"{len(FAILURES)} failure(s)")
        return 1
    print("all checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
