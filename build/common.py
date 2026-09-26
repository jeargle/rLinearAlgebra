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
    "scalar_field", "vector_space",
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
