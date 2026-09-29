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
