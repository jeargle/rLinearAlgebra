"""Build the Wikipedia hyperlink network used by the PageRank notebook.

The pages are the articles listed in Wikipedia's "Linear algebra" navigation box
(Template:Linear algebra), minus its outline, glossary, list and comparison pages. A link
from article j to article i means that the text of article j, as its editors wrote it,
contains a [[wikilink]] to article i (directly or through a redirect). Links that a
navigation template adds are not counted: every article in the box carries the same box,
which would link each of them to all of the others and wash out the structure.

Every page is read at its last revision before SNAPSHOT, so rerunning the script gives the
same graph. Redirects are resolved as they stand when the script runs; that can change a
link only if a redirect is retargeted, which is rare.

Wikipedia's text is CC BY-SA; only article titles and the link structure are kept here.

The network is written, as a list of titles and one list of link targets per article, into
the block between the BEGIN/END WIKIPEDIA DATA markers in the notebook and into the `data`
section of both snippet files (snippets/06-*.py and .jl), so all three run standalone.

Usage (maintainers only; needs network access, standard library only):
    uv run python data/prepare_wikipedia_links.py
"""
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STEM = "06-pagerank-and-network-centrality"
NOTEBOOK = ROOT / "notebooks" / f"{STEM}.py"
SNIPPETS = ROOT / "snippets" / STEM
CACHE = ROOT / "data" / ".cache" / "wikipedia_linear_algebra.json"
API = "https://en.wikipedia.org/w/api.php"
USER_AGENT = "rLinearAlgebra-data-prep/0.1 (https://github.com/jeargle/rLinearAlgebra)"
NAVBOX = "Template:Linear algebra"
SNAPSHOT = "2026-10-01T00:00:00Z"
SKIP_PREFIXES = ("Outline of", "Glossary of", "List of", "Comparison of", "Template:")
NON_ARTICLE = {"file", "image", "template", "category", "wikipedia", "help", "wikt", "w",
               "s", "commons", "special", "portal", "draft", "user", "talk", "mos"}
WIKILINK = re.compile(r"\[\[([^\[\]|#]+)(?:#[^\[\]|]*)?(?:\|[^\[\]]*)?\]\]")


def call(**params):
    """One API request, waiting and retrying when Wikipedia asks us to slow down."""
    params.update(format="json", formatversion=2)
    data = urllib.parse.urlencode(params).encode()
    for _ in range(10):
        req = urllib.request.Request(API, data=data, headers={"User-Agent": USER_AGENT})
        try:
            with urllib.request.urlopen(req) as resp:
                result = json.load(resp)
            time.sleep(0.5)
            return result
        except urllib.error.HTTPError as err:
            if err.code != 429:
                raise
            time.sleep(int(err.headers.get("Retry-After", 10)) + 1)
    raise RuntimeError("Wikipedia kept rate-limiting the requests; try again later")


def revision(title):
    """(canonical title, revision id, wikitext) of a page's last revision before SNAPSHOT."""
    q = call(action="query", titles=title, prop="revisions", rvprop="ids|content",
             rvslots="main", rvstart=SNAPSHOT, rvdir="older", rvlimit=1, redirects=1)
    page = q["query"]["pages"][0]
    rev = page["revisions"][0]
    return page["title"], rev["revid"], rev["slots"]["main"]["content"]


def wikilinks(text):
    """Targets of the article-namespace [[links]] written in a page's wikitext."""
    found = []
    for m in WIKILINK.finditer(text):
        target = m.group(1).strip().replace("_", " ")
        if not target or target.startswith(":"):
            continue
        if ":" in target and target.split(":")[0].strip().lower() in NON_ARTICLE:
            continue
        found.append(target[0].upper() + target[1:])
    return found


def resolve(targets):
    """{link target: canonical article title}, following normalization and redirects."""
    canon = {}
    targets = sorted(set(targets))
    for i in range(0, len(targets), 50):
        batch = targets[i:i + 50]
        q = call(action="query", titles="|".join(batch), redirects=1)["query"]
        norm = {n["from"]: n["to"] for n in q.get("normalized", [])}
        redirect = {r["from"]: r["to"] for r in q.get("redirects", [])}
        for t in batch:
            t2 = norm.get(t, t)
            canon[t] = redirect.get(t2, t2)
    return canon


def download():
    """Fetch the navbox, every article in it and the redirect map; cache the result."""
    _, navbox_rev, navbox_text = revision(NAVBOX)
    members = [t for t in dict.fromkeys(wikilinks(navbox_text))
               if not t.startswith(SKIP_PREFIXES)]
    pages = {}
    for k, title in enumerate(members, 1):
        canonical, rev, text = revision(title)
        pages.setdefault(canonical, {"revid": rev, "links": wikilinks(text)})
        print(f"\r  fetched {k}/{len(members)} articles", end="", flush=True)
    print()
    canon = resolve([t for p in pages.values() for t in p["links"]])
    return {"snapshot": SNAPSHOT, "navbox_revid": navbox_rev, "pages": pages, "canon": canon}


def load():
    if CACHE.exists():
        return json.loads(CACHE.read_text())
    raw = download()
    CACHE.parent.mkdir(parents=True, exist_ok=True)
    CACHE.write_text(json.dumps(raw, ensure_ascii=False, indent=1))
    return raw


def network(raw):
    """(titles in alphabetical order, links) where links[j] lists, in increasing order, the
    0-based indices of the articles that article j links to. Self-links are dropped and
    repeated links counted once."""
    titles = sorted(raw["pages"])
    index = {t: i for i, t in enumerate(titles)}
    canon = raw["canon"]
    links = []
    for j, t in enumerate(titles):
        hits = {index[canon[x]] for x in raw["pages"][t]["links"] if canon.get(x) in index}
        links.append(sorted(hits - {j}))
    return titles, links


def wrap(items, width, indent):
    """Comma-separated items in lines of at most `width` characters."""
    lines, line = [], ""
    for item in items:
        piece = item + ", "
        if line and len(indent) + len(line) + len(piece) > width:
            lines.append(indent + line.rstrip())
            line = ""
        line += piece
    if line:
        lines.append(indent + line.rstrip())
    return lines


def python_block(titles, links, indent):
    """The data as Python literals (0-based link indices)."""
    pad = indent + "    "
    out = [f"{indent}titles = ["]
    out += wrap([repr(t) for t in titles], 100, pad)
    out += [f"{indent}]",
            f"{indent}links = [   # links[j]: indices of the articles that article j links to"]
    out += [f"{pad}[{', '.join(map(str, row))}]," for row in links]
    out += [f"{indent}]"]
    return out


def julia_block(titles, links):
    """The same data as Julia literals (1-based link indices)."""
    out = ["titles = ["]
    out += wrap([json.dumps(t, ensure_ascii=False) for t in titles], 100, "    ")
    out += ["]",
            "links = [   # links[j]: indices of the articles that article j links to (1-based)"]
    # Int[] keeps an empty row typed, so links stays a Vector{Vector{Int}}
    out += [f"    [{', '.join(str(i + 1) for i in row)}]," if row else "    Int[],"
            for row in links]
    out += ["]"]
    return out


def replace_block(path, begin, end, new):
    text = path.read_text()
    start, stop = text.index(begin), text.index(end) + len(end)
    path.write_text(text[:start] + new + text[stop:])
    print(f"wrote the network into {path.relative_to(ROOT)}")


def main():
    raw = load()
    titles, links = network(raw)
    n, m = len(titles), sum(map(len, links))
    assert n > 100 and m > 1000, (n, m)
    note = f"Wikipedia, revisions as of {raw['snapshot'][:10]}; {n} articles, {m} links"
    nb_begin, nb_end = "    # BEGIN WIKIPEDIA DATA", "    # END WIKIPEDIA DATA"
    nb = [f"{nb_begin} (generated by data/prepare_wikipedia_links.py; {note})"]
    replace_block(NOTEBOOK, nb_begin, nb_end,
                  "\n".join(nb + python_block(titles, links, "    ") + [nb_end]))
    sn_begin, sn_end = "# BEGIN WIKIPEDIA DATA", "# END WIKIPEDIA DATA  #hide"
    head = f"{sn_begin}: {note} (written by data/prepare_wikipedia_links.py)"
    replace_block(SNIPPETS.with_suffix(".py"), sn_begin, sn_end,
                  "\n".join([head] + python_block(titles, links, "") + [sn_end]))
    replace_block(SNIPPETS.with_suffix(".jl"), sn_begin, sn_end,
                  "\n".join([head] + julia_block(titles, links) + [sn_end]))
    dangling = [titles[j] for j in range(n) if not links[j]]
    print(f"{n} articles, {m} links; no out-links: {dangling}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
