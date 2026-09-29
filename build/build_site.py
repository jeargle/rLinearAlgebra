"""Generate site/ — a static HTML reading surface, deployable to GitHub Pages.

Every link is relative, so the site works at a domain root, under a project-site
path prefix (/rLinearAlgebra/), or from a local directory served over HTTP.

Usage:
    python build/build_site.py
    python -m http.server --directory site 8000     # reproduces deployed conditions
"""
import html
import shutil
import sys
from collections import defaultdict
from pathlib import Path

# Make the script runnable from any working directory, and under PYTHONSAFEPATH.
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import (BLOCKS, FIELD_DEF, GF2_DEF, GF2_SHORT, ROOT, escape_cell, load_all,
                    load_entries, require_gf2_definition)

try:
    import markdown
except ImportError:  # pragma: no cover
    print("error: build_site.py needs the markdown package (pip install markdown)",
          file=sys.stderr)
    raise SystemExit(1)

SITE = ROOT / "site"
EXTENSIONS = ["tables", "fenced_code", "sane_lists"]

CSS = """\
:root { --ink:#1a1a1a; --dim:#555; --rule:#d8d8d8; --accent:#1d4ed8; --bg:#fff; }
* { box-sizing:border-box; }
body { margin:0 auto; padding:2rem 1.25rem 4rem; max-width:46rem; background:var(--bg);
  color:var(--ink); font:16px/1.65 -apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif; }
h1 { font-size:1.6rem; line-height:1.25; margin:0 0 .5rem; }
h2 { font-size:1.15rem; margin:2rem 0 .5rem; }
h3 { font-size:1rem; margin:1.5rem 0 .4rem; }
a { color:var(--accent); }
code, pre { font-family:ui-monospace,SFMono-Regular,Menlo,monospace; font-size:.9em; }
pre { background:#f6f7f9; padding:.75rem 1rem; overflow-x:auto; border-radius:4px; }
table { border-collapse:collapse; width:100%; margin:1rem 0; font-size:.93rem; display:block; overflow-x:auto; }
th, td { border:1px solid var(--rule); padding:.4rem .6rem; text-align:left; vertical-align:top; }
th { background:#f6f7f9; }
details { background:#f6f7f9; border:1px solid var(--rule); border-radius:4px; padding:.6rem .9rem; margin:1rem 0; }
details[open] { padding-bottom:.2rem; }
summary { cursor:pointer; font-weight:600; }
.meta { font-size:.9rem; color:var(--dim); border-left:3px solid var(--rule); padding:.1rem 0 .1rem .8rem; margin:1rem 0; }
.meta div { margin:.25rem 0; }
.tier { display:inline-block; font-size:.75rem; font-weight:600; padding:.1rem .45rem;
  border-radius:3px; background:#eceff3; color:var(--dim); vertical-align:.08rem; }
.planned { color:var(--dim); }
.def { font-size:.85rem; color:var(--dim); font-style:italic; }
nav.crumb { font-size:.9rem; margin-bottom:1.5rem; }
ul.entries { list-style:none; padding-left:0; }
ul.entries li { margin:.35rem 0; }
footer { margin-top:3rem; padding-top:1rem; border-top:1px solid var(--rule); font-size:.85rem; color:var(--dim); }
"""


def md(text):
    return markdown.markdown(text, extensions=EXTENSIONS)


def inline(text):
    out = markdown.markdown(text, extensions=EXTENSIONS)
    if out.startswith("<p>") and out.endswith("</p>"):
        out = out[3:-4]
    return out


def page(title, body, depth=0):
    up = "../" * depth
    return (
        "<!doctype html>\n<html lang=\"en\">\n<head>\n"
        "<meta charset=\"utf-8\">\n"
        "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n"
        f"<title>{html.escape(title)}</title>\n"
        f"<link rel=\"stylesheet\" href=\"{up}style.css\">\n"
        "</head>\n<body>\n" + body +
        "\n<footer>Applied Linear Algebra — a collection of real problems, "
        "with each field's vocabulary translated into linear algebra.</footer>\n"
        "</body>\n</html>\n"
    )


def entry_page(meta):
    s = meta["_sections"]
    parts = [f"<nav class=\"crumb\"><a href=\"../index.html\">← All fields</a></nav>",
             f"<h1>{inline(meta['title'])}</h1>"]
    parts.append("<details>\n<summary>Start here — the problem in plain terms</summary>\n"
                 + md(s["Start here"]) + "\n</details>")
    parts.append(
        "<div class=\"meta\">"
        f"<div><b>Field:</b> {html.escape(meta['field_label'])}</div>"
        f"<div><b>Tier:</b> {meta['tier']} — {inline(meta['tier_note'])}</div>"
        f"<div><b>Scalar field:</b> {inline(meta['scalar_field'])}</div>"
        f"<div><b>Vectors:</b> {inline(meta['vector_space'])}</div>"
        f"<div><b>Underlying equations:</b> {inline(meta.get('underlying_equations') or 'not yet recorded')}</div>"
        "</div>")
    for name in BLOCKS:
        parts.append(f"<h2>{html.escape(name)}</h2>\n" + md(s[name]))
    terms = meta.get("terminology") or {}
    if terms:
        rows = "\n".join(f"| {escape_cell(t)} | {escape_cell(v)} |" for t, v in terms.items())
        table = "| Domain term | In linear algebra |\n|---|---|\n" + rows
        parts.append("<h2>Terminology</h2>\n"
                     "<p>How this field's vocabulary reads as linear algebra.</p>\n" + md(table))
    return page(meta["short_title"], "\n".join(parts), depth=1)


def index_page(entries, rows):
    written = {m["id"]: m for m in entries}
    by_field = defaultdict(list)
    for row in rows:
        by_field[row["nav_field"]].append(row)

    parts = ["<h1>Applied Linear Algebra</h1>",
             "<p>Real problems from across science, engineering, and mathematics, each worked as a "
             "linear-algebra problem — with the domain's own vocabulary translated as you go. "
             "Entries marked <span class=\"planned\">planned</span> are catalogued but not yet "
             "written up.</p>",
             "<p><a href=\"glossary.html\">Domain terminology, translated</a> — one unfamiliar word "
             "from a question, and what it means mathematically.</p>"]
    gf2_defined = False
    for field in sorted(by_field):
        parts.append(f"<h2>{html.escape(field)}</h2>\n<ul class=\"entries\">")
        for row in sorted(by_field[field], key=lambda r: r["id"]):
            badge = f"<span class=\"tier\">Tier {row['tier']}</span>"
            note = ""
            if not gf2_defined and "GF(2)" in row["short_title"]:
                note = f" <span class=\"def\">({html.escape(GF2_SHORT)})</span>"  # first use
                gf2_defined = True
            if row["id"] in written:
                meta = written[row["id"]]
                parts.append(f"<li><a href=\"entries/{meta['slug']}.html\">"
                             f"{inline(meta['short_title'])}</a> {badge}{note}</li>")
            else:
                parts.append(f"<li class=\"planned\">{inline(row['short_title'])} "
                             f"{badge} planned{note}</li>")
        parts.append("</ul>")
    return page("Applied Linear Algebra", "\n".join(parts))


def glossary_page(entries):
    rows = [(t, v, m) for m in entries for t, v in (m.get("terminology") or {}).items()]
    rows.sort(key=lambda r: r[0].lower())
    body = "\n".join(
        f"| {escape_cell(t)} | {escape_cell(v)} | "
        f"[{escape_cell(m['short_title'])}](entries/{m['slug']}.html) |"
        for t, v, m in rows)
    table = "| Domain term | In linear algebra | Entry |\n|---|---|---|\n" + body
    parts = ["<nav class=\"crumb\"><a href=\"index.html\">← All fields</a></nav>",
             "<h1>Domain terminology, translated</h1>",
             "<h2>Two general terms</h2>", md(FIELD_DEF)]
    if any("GF(2)" in v for _, v, _ in rows):
        parts.append(md(GF2_DEF))
    parts += ["<h2>By field</h2>",
              f"<p>{len(rows)} terms from {len(entries)} entries.</p>", md(table)]
    return page("Domain terminology", "\n".join(parts))


def main():
    entries = load_entries()
    rows = load_all()

    if SITE.exists():
        shutil.rmtree(SITE)
    (SITE / "entries").mkdir(parents=True)

    (SITE / "style.css").write_text(CSS)
    (SITE / ".nojekyll").write_text("")  # or GitHub runs Jekyll and drops _-prefixed paths
    pages = {SITE / "index.html": (index_page(entries, rows), 0),
             SITE / "glossary.html": (glossary_page(entries), 0)}
    for meta in entries:
        pages[SITE / "entries" / f"{meta['slug']}.html"] = (entry_page(meta), meta["tier"])
    for path, (text, tier) in pages.items():
        if tier != 3:
            require_gf2_definition(text, f"site:{path.relative_to(SITE)}")
        path.write_text(text)

    count = sum(1 for _ in SITE.rglob("*") if _.is_file())
    print(f"wrote site/: {count} files ({len(entries)} entry pages, "
          f"{len(rows)} entries listed)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
