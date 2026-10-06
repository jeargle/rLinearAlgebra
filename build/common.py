"""Shared loading for the applied-linear-algebra collection build.

Single source of truth:
  entries/*.md   one written entry each: YAML frontmatter + markdown body
  backlog.yaml   candidate entries, metadata only (no prose yet)

Everything under dist/ is generated. Do not hand-edit it.
"""
from pathlib import Path
import re
import yaml

ROOT = Path(__file__).resolve().parents[1]
ENTRIES_DIR = ROOT / "entries"
BACKLOG = ROOT / "backlog.yaml"
DOCS = ROOT / "docs"
DIST = ROOT / "dist"
NOTEBOOKS_DIR = ROOT / "notebooks"

# Public address of the GitHub Pages site. Only the wiki needs it: the site itself uses
# relative links, but a Reddit wiki page can only link out with a full URL.
SITE_URL = "https://jeargle.github.io/rLinearAlgebra/"
REPO_URL = "https://github.com/jeargle/rLinearAlgebra/blob/main/"

# Order of the analytical blocks in a rendered entry.
BLOCKS = [
    "The problem",
    "Variables",
    "Formulation",
    "Matrix structure",
    "What is computed",
    "Why linear algebra is the right tool",
    "Pitfall worth teaching",
    "Extensions",
]

# Columns of the generated index, in order.
INDEX_COLUMNS = [
    "id", "status", "title", "nav_field", "field", "subfield", "core_la_object",
    "la_concepts", "primary_method", "matrix_structure", "typical_size",
    "worked_example_size", "tier", "tier_ceiling", "prereq_beyond_la",
    "scalar_field", "vector_space", "underlying_equations",
]

FRONTMATTER = re.compile(r"\A---\n(.*?)\n---\n\n?(.*)\Z", re.S)


def parse_entry(path):
    """Return (frontmatter dict, {block name: markdown}) for one entry file."""
    match = FRONTMATTER.match(Path(path).read_text())
    if not match:
        raise ValueError(f"{path}: missing or malformed YAML frontmatter")
    meta = yaml.safe_load(match.group(1))
    body = match.group(2)

    sections = {}
    parts = re.split(r"^## ", body, flags=re.M)
    for part in parts:
        if not part.strip():
            continue
        name, _, text = part.partition("\n")
        sections[name.strip()] = text.strip()

    expected = ["Start here"] + BLOCKS
    missing = [s for s in expected if s not in sections]
    if missing:
        raise ValueError(f"{path}: missing sections {missing}")
    return meta, sections


def load_entries():
    """All written entries, ordered by id."""
    out = []
    for path in sorted(ENTRIES_DIR.glob("*.md")):
        meta, sections = parse_entry(path)
        meta["_sections"] = sections
        meta["_path"] = path
        out.append(meta)
    out.sort(key=lambda m: m["id"])
    return out


def notebook_paths():
    """Notebook sources, each named after its entry file (NN-slug.py for NN-slug.md)."""
    stems = {p.stem for p in ENTRIES_DIR.glob("*.md")}
    paths = sorted(NOTEBOOKS_DIR.glob("[0-9]*.py"))
    orphans = [p.name for p in paths if p.stem not in stems]
    if orphans:
        raise ValueError(f"notebooks with no matching entry file: {orphans}")
    return paths


SNIPPETS_DIR = ROOT / "snippets"
SNIPPET_LANGS = {"py": "Python", "jl": "Julia"}
_SNIPPET_MARK = re.compile(r"^# --- snippet (\w+): (.+?) ---$", re.M)


def parse_snippets(path):
    """{name: (title, code)} for one snippet file, in file order.

    A section starts at a line `# --- snippet NAME: Title ---` and runs to the next one;
    anything before the first marker is a file header and is not shown. A line ending in
    `#hide` runs but is not shown: it lets a section use the notebook's variable names
    (A_us, L_us, ...) while its check runs on the hand-worked toy.
    """
    text = Path(path).read_text()
    marks = list(_SNIPPET_MARK.finditer(text))
    out = {}
    for i, mark in enumerate(marks):
        end = marks[i + 1].start() if i + 1 < len(marks) else len(text)
        lines = text[mark.end():end].split("\n")
        shown = "\n".join(line for line in lines if not line.rstrip().endswith("#hide"))
        out[mark.group(1)] = (mark.group(2), shown.strip("\n"))
    return out


def entry_snippets(meta):
    """[(name, title, {lang: code})] for an entry, or [] if it has no snippet files.

    Every language's file must define the same sections with the same titles, so the
    tabs on a page always show the same computation side by side.
    """
    stem = Path(meta["_path"]).stem
    files = {lang: SNIPPETS_DIR / f"{stem}.{lang}" for lang in SNIPPET_LANGS}
    present = {lang: p for lang, p in files.items() if p.exists()}
    if not present:
        return []
    if len(present) != len(files):
        raise ValueError(f"{stem}: snippet files must come as a set: {sorted(files.values())}")
    parsed = {lang: parse_snippets(p) for lang, p in present.items()}
    reference = parsed["py"]
    for lang, sections in parsed.items():
        if [(n, t) for n, (t, _) in sections.items()] != [(n, t) for n, (t, _) in reference.items()]:
            raise ValueError(f"{stem}.{lang}: snippet names and titles differ from {stem}.py")
    return [(name, title, {lang: parsed[lang][name][1] for lang in SNIPPET_LANGS})
            for name, (title, _) in reference.items()]


def notebook_page(meta):
    """Path of the entry's exported notebook relative to the site root, or None."""
    stem = Path(meta["_path"]).stem
    if (NOTEBOOKS_DIR / f"{stem}.py").exists():
        return f"notebooks/{stem}.html"
    return None


def load_backlog():
    """Candidate entries, ordered by id."""
    data = yaml.safe_load(BACKLOG.read_text()) or {}
    rows = data.get("backlog", [])
    rows.sort(key=lambda m: m["id"])
    return rows


def load_all():
    """Written entries plus backlog candidates, ordered by id."""
    rows = load_entries() + load_backlog()
    rows.sort(key=lambda m: m["id"])
    ids = [r["id"] for r in rows]
    if len(set(ids)) != len(ids):
        dupes = sorted({i for i in ids if ids.count(i) > 1})
        raise ValueError(f"duplicate entry ids: {dupes}")
    return rows


def escape_cell(text):
    """Escape a pipe so it survives a markdown table cell."""
    return str(text).replace("|", r"\|")


# ---------------------------------------------------------------------------
# Shared definitions. Few readers have taken abstract algebra, so these terms are
# defined in plain language wherever a page first needs them.

FIELD_DEF = (
    "A **field** is a number system in which addition, subtraction, multiplication, and division by "
    "any nonzero number all behave the way they do for ordinary numbers. The rational numbers ℚ, the "
    "real numbers ℝ, the complex numbers ℂ, and the integers modulo a prime p all qualify. The integers "
    "modulo 6 do not: there 2 × 3 = 0, so 2 has no reciprocal and nothing can be divided by 2. The "
    "scalars of every vector space come from a field, which is why each entry names its scalar field."
)

GF2_DEF = (
    "**GF(2)** is the smallest field: just the two numbers 0 and 1, added and multiplied modulo 2, so "
    "1 + 1 = 0. Addition is the same as XOR, and multiplication is the same as AND. GF(p) is the same "
    "construction using the integers modulo a prime p."
)

GF2_SHORT = "GF(2) is the number system {0, 1} with arithmetic modulo 2, so 1 + 1 = 0"

# ---------------------------------------------------------------------------
# Wikipedia links at first use (terms.yaml)

TERMS = ROOT / "terms.yaml"

# Regions of markdown that must never receive a link: fenced and inline code, headings,
# table rows, existing links, and bare URLs.
_PROTECTED = re.compile(
    r"```.*?```"                 # fenced code, including display equations
    r"|`[^`\n]*`"                # inline code
    r"|^#[^\n]*$"                # headings (one line; re.S would let .* run to end of page)
    r"|^\|[^\n]*$"               # table rows
    r"|!?\[[^\]\n]*\]\([^)\n]*\)"  # existing links and images
    r"|<https?://[^>\s]+>"       # autolinks
    r"|https?://\S+",            # bare URLs
    re.S | re.M,
)


def _compile_pattern(pattern):
    """All-lowercase patterns are case-insensitive; any capital letter makes it case-sensitive."""
    flags = 0 if re.search(r"[A-Z]", pattern.replace(r"\b", "")) else re.I
    # not preceded by a word character or hyphen, and extended to the end of its word
    return re.compile(r"(?<![\w-])(?:" + pattern + r")\w*", flags)


def load_terms():
    """Terms that have a Wikipedia URL, with compiled match patterns."""
    if not TERMS.exists():
        return []
    data = yaml.safe_load(TERMS.read_text()) or {}
    out = []
    for term in data.get("terms", []):
        if not term.get("url"):
            continue
        out.append({
            "term": term["term"],
            "url": term["url"],
            "entries": set(term.get("entries") or []),
            "patterns": [_compile_pattern(p) for p in term.get("match") or []],
        })
    return out


def terms_for_entry(terms, entry_id):
    """Only the terms recorded for this entry, so an abbreviation keeps its entry's meaning."""
    return [t for t in terms if entry_id in t["entries"]]


def _free_spans(text):
    """(start, end) spans of text that may receive links."""
    spans, pos = [], 0
    for m in _PROTECTED.finditer(text):
        if m.start() > pos:
            spans.append((pos, m.start()))
        pos = m.end()
    if pos < len(text):
        spans.append((pos, len(text)))
    return spans


def _first_matches(text, terms, done):
    """Earliest match of each not-yet-linked term, restricted to free spans."""
    spans = _free_spans(text)
    found = []
    for term in terms:
        if term["term"] in done:
            continue
        best = None
        for rx in term["patterns"]:
            m = _earliest(rx, text, spans)
            if m and (best is None or m.start() < best[0]):
                best = (m.start(), m.end(), term)
        if best:
            found.append(best)
    return found


def _earliest(rx, text, spans):
    """First match of rx inside any free span (spans are in text order)."""
    for lo, hi in spans:
        m = rx.search(text, lo, hi)
        if m:
            return m
    return None


def _resolve_overlaps(found):
    """Keep non-overlapping matches, preferring the earlier and then the longer one."""
    kept, last_end = [], -1
    for start, end, term in sorted(found, key=lambda f: (f[0], -(f[1] - f[0]))):
        if start >= last_end:
            kept.append((start, end, term))
            last_end = end
    return kept


def link_first_uses(text, terms, done):
    """Link each term's first use in markdown `text`; `done` records terms already linked on the page.

    Call repeatedly, in page order, with the same `done` set when a page is assembled in pieces.
    """
    kept = _resolve_overlaps(_first_matches(text, terms, done))
    out, pos = [], 0
    for start, end, term in kept:
        out.append(text[pos:start])
        out.append(f"[{text[start:end]}]({term['url']})")
        done.add(term["term"])
        pos = end
    out.append(text[pos:])
    return "".join(out)


_GF2 = re.compile(r"GF\(2\)")
_GF2_DEFINED = re.compile(r"modulo 2|mod 2")
GF2_WINDOW = 320  # characters on either side of the first use


def require_gf2_definition(text, page):
    """Fail the build if a page uses GF(2) without defining it near its first use.

    Applies to every page except entry pages at Tier 3, whose readers are assumed to
    know finite fields. The test is deliberately simple: a phrase like "modulo 2" must
    appear within GF2_WINDOW characters of the first occurrence of "GF(2)".
    """
    match = _GF2.search(text)
    if not match:
        return
    lo = max(0, match.start() - GF2_WINDOW)
    hi = match.end() + GF2_WINDOW
    if not _GF2_DEFINED.search(text[lo:hi]):
        snippet = text[max(0, match.start() - 60):match.end() + 60].replace("\n", " ")
        raise ValueError(f"{page}: first use of GF(2) is not defined nearby: …{snippet}…")
