"""Generate dist/reddit_wiki/*.md — the read surface for a subreddit wiki.

Differences from the site/catalog rendering, all forced by Reddit's markdown:
  * raw HTML is stripped, so the collapsible "Start here" block becomes a plain
    `### Start here` heading, kept at the top of the page where its audience needs it;
  * no dependable math typesetting, so display equations stay in fenced code blocks;
  * one page per entry plus a field-grouped index, since long pages read badly;
  * pipes inside table cells are escaped.

Writing to Reddit is a separate, explicit step (--push) so a build never publishes
by accident. It needs a script-type OAuth app and these environment variables:
    REDDIT_CLIENT_ID  REDDIT_CLIENT_SECRET  REDDIT_USERNAME  REDDIT_PASSWORD
    REDDIT_SUBREDDIT  (default: LinearAlgebra)

Usage:
    python build/build_wiki.py            # render to dist/reddit_wiki/
    python build/build_wiki.py --push     # render, then publish
"""
import argparse
import os
import sys
from pathlib import Path
from collections import defaultdict

# Make the script runnable from any working directory, and under PYTHONSAFEPATH.
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import (BLOCKS, DIST, FIELD_DEF, GF2_DEF, GF2_SHORT, escape_cell, link_first_uses,
                    load_all, load_entries, load_terms, require_gf2_definition, terms_for_entry)

WIKI_ROOT = "applications"


def page_path(meta):
    return f"{WIKI_ROOT}/{meta['slug']}"


def render_entry(meta, link_terms=()):
    sections = meta["_sections"]
    out = [f"# {meta['title']}", ""]
    out += ["### Start here", "", sections["Start here"], ""]
    out += [f"**Field:** {meta['field_label']}  ",
            f"**Tier:** {meta['tier']} — {meta['tier_note']}  ",
            f"**Scalar field:** {meta['scalar_field']}  ",
            f"**Vectors:** {meta['vector_space']}  ",
            f"**Underlying equations:** {meta.get('underlying_equations') or 'not yet recorded'}", ""]
    for name in BLOCKS:
        out += [f"### {name}", "", sections[name], ""]
    terms = meta.get("terminology") or {}
    if terms:
        out += ["### Terminology", "",
                "How this field's vocabulary reads as linear algebra.", "",
                "| Domain term | In linear algebra |", "|---|---|"]
        out += [f"| {escape_cell(t)} | {escape_cell(m)} |" for t, m in terms.items()]
        out += [""]
    out += ["---", "", f"[Back to the index](/r/{os.environ.get('REDDIT_SUBREDDIT', 'LinearAlgebra')}"
            f"/wiki/{WIKI_ROOT})", ""]
    # Wikipedia links at first use, using only this entry's terms
    return link_first_uses("\n".join(out), terms_for_entry(link_terms, meta["id"]), set())


def render_index(entries, rows):
    written = {m["id"]: m for m in entries}
    by_field = defaultdict(list)
    for row in rows:
        by_field[row["nav_field"]].append(row)

    out = ["# Applied linear algebra, by field", "",
           "Real problems from each field, with the domain vocabulary translated into "
           "linear algebra. Entries marked *(planned)* are catalogued but not yet written up.", ""]
    gf2_defined = False
    for field in sorted(by_field):
        out += [f"## {field}", ""]
        for row in sorted(by_field[field], key=lambda r: r["id"]):
            label = f"Tier {row['tier']}"
            if row["id"] in written:
                meta = written[row["id"]]
                line = f"* [{meta['short_title']}]({page_path(meta)}) — {label}"
            else:
                line = f"* {row['short_title']} — {label} *(planned)*"
            if not gf2_defined and "GF(2)" in row["short_title"]:
                line += f" ({GF2_SHORT})"   # define at the page's first use
                gf2_defined = True
            out.append(line)
        out += [""]
    return "\n".join(out)


def render_glossary(entries, terms=()):
    rows = []
    for meta in entries:
        for term, meaning in (meta.get("terminology") or {}).items():
            rows.append((term, meaning, meta))
    rows.sort(key=lambda r: r[0].lower())
    out = ["# Domain terminology, translated", "",
           "One unfamiliar word from a question, and what it means mathematically.", "",
           "### Two general terms", "", FIELD_DEF, ""]
    if any("GF(2)" in m for _, m, _ in rows):
        out += [GF2_DEF, ""]
    out += ["### By field", "",
            "| Domain term | In linear algebra | Entry |", "|---|---|---|"]
    out += [f"| {escape_cell(t)} | {escape_cell(m)} | [{meta['short_title']}]({page_path(meta)}) |"
            for t, m, meta in rows]
    # tables and headings are never linked, so only the introductory prose receives links
    return link_first_uses("\n".join(out + [""]), terms, set())


def build():
    entries = load_entries()
    rows = load_all()
    outdir = DIST / "reddit_wiki"
    outdir.mkdir(parents=True, exist_ok=True)

    terms = load_terms()
    pages = {WIKI_ROOT: render_index(entries, rows),          # navigation only: no links
             f"{WIKI_ROOT}/glossary": render_glossary(entries, terms)}
    tier3 = set()
    for meta in entries:
        pages[page_path(meta)] = render_entry(meta, terms)
        if meta["tier"] == 3:
            tier3.add(page_path(meta))

    for name, text in pages.items():
        if name not in tier3:
            require_gf2_definition(text, f"wiki:{name}")
        path = outdir / (name.replace("/", "__") + ".md")
        path.write_text(text)
        if "<details>" in text or "<summary>" in text:
            raise ValueError(f"{name}: raw HTML would be stripped by Reddit")
    print(f"rendered {len(pages)} wiki pages to {outdir.relative_to(DIST.parent)}")
    return pages


def push(pages):
    try:
        import praw
    except ImportError:
        print("error: --push needs praw (pip install praw)", file=sys.stderr)
        return 1
    required = ["REDDIT_CLIENT_ID", "REDDIT_CLIENT_SECRET",
                "REDDIT_USERNAME", "REDDIT_PASSWORD"]
    missing = [k for k in required if not os.environ.get(k)]
    if missing:
        print(f"error: missing environment variables {missing}", file=sys.stderr)
        return 1

    reddit = praw.Reddit(
        client_id=os.environ["REDDIT_CLIENT_ID"],
        client_secret=os.environ["REDDIT_CLIENT_SECRET"],
        username=os.environ["REDDIT_USERNAME"],
        password=os.environ["REDDIT_PASSWORD"],
        user_agent="applied-linear-algebra-collection/0.1 wiki sync",
    )
    subreddit = reddit.subreddit(os.environ.get("REDDIT_SUBREDDIT", "LinearAlgebra"))
    for name, text in sorted(pages.items()):
        subreddit.wiki[name].edit(content=text, reason="sync from repository")
        print(f"pushed {name} ({len(text)} bytes)")
    return 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--push", action="store_true",
                        help="publish the rendered pages to the subreddit wiki")
    args = parser.parse_args()
    pages = build()
    return push(pages) if args.push else 0


if __name__ == "__main__":
    raise SystemExit(main())
