"""Assemble dist/applied_linear_algebra_catalog.md from docs/ + entries/.

Structure:
    docs/00-front.md   editorial prose with {{PLACEHOLDER}} slots for computed values
    entries/*.md       one written entry each
    docs/99-back.md    coverage, backlog, next steps

Every count, field tally, and metadata line in the output is computed from the entry
files, so the prose cannot disagree with the index.

Usage:  python build/build_catalog.py
"""
import re
import sys
from pathlib import Path
from collections import Counter

# Make the script runnable from any working directory, and under PYTHONSAFEPATH.
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import BLOCKS, DIST, DOCS, escape_cell, load_all, load_entries

SUMMARY = "Start here — the problem in plain terms"


def nav_table(rows):
    total = Counter(r["nav_field"] for r in rows)
    tier1 = Counter(r["nav_field"] for r in rows if r["tier"] == 1)
    order = sorted(total, key=lambda f: (-total[f], f))
    lines = ["| Field | Entries | of which Tier 1 |", "|---|---|---|"]
    lines += [f"| {f} | {total[f]} | {tier1[f]} |" for f in order]
    return "\n".join(lines)


def coverage_table():
    """Editorial per-entry labels live in docs/coverage_labels.tsv; ids are verified."""
    path = DOCS / "coverage_labels.tsv"
    body = [ln for ln in path.read_text().splitlines() if ln.strip()]
    seed_ids = {m["id"] for m in load_entries()}
    labelled = {int(ln.strip().strip("|").split("|")[0]) for ln in body}
    if labelled != seed_ids:
        raise ValueError(
            f"coverage_labels.tsv covers {sorted(labelled)}, seed entries are {sorted(seed_ids)}"
        )
    header = ["| # | Field | Core linear-algebra object | Dominant method |",
              "|---|-------|---------------------------|-----------------|"]
    return "\n".join(header + body)


def render_entry(meta):
    sections = meta["_sections"]
    out = [f"## {meta['id']}. {meta['title']}", ""]
    out += ["<details>", f"<summary><b>{SUMMARY}</b></summary>", "",
            sections["Start here"], "", "</details>", ""]
    out += [f"**Field:** {meta['field_label']}", ""]
    out += [f"**Tier:** {meta['tier']} — {meta['tier_note']}", ""]
    out += [f"**Scalars and vectors.** Scalar field: {meta['scalar_field']}. "
            f"Vectors: {meta['vector_space']}.", ""]
    if meta.get("underlying_equations"):
        out += [f"**Underlying equations.** {meta['underlying_equations']}.", ""]
    for name in BLOCKS:
        if name == "Extensions":
            out += ["**Terminology map.** How this field's vocabulary reads as linear algebra.", "",
                    "| Domain term | In linear algebra |", "|---|---|"]
            out += [f"| {escape_cell(t)} | {escape_cell(m)} |"
                    for t, m in (meta.get("terminology") or {}).items()]
            out += [""]
        text = sections[name]
        # A block that opens with a list, table, or fence must start on its own line,
        # or the lead-in swallows the first item.
        if re.match(r"(?:[-*+] |\d+\. |\||```)", text):
            out += [f"**{name}.**", text, ""]
        else:
            out += [f"**{name}.** {text}", ""]
    out += ["---"]
    return "\n".join(out)


def main():
    entries = load_entries()
    rows = load_all()
    tiers = Counter(r["tier"] for r in rows)
    seed_tiers = Counter(m["tier"] for m in entries)
    ceiling3 = sum(1 for m in entries if m["tier_ceiling"] == 3)

    values = {
        "NAV_TABLE": nav_table(rows),
        "COVERAGE_TABLE": coverage_table(),
        "N_TOTAL": str(len(rows)),
        "N_SEED": str(len(entries)),
        "N_SEED_TIER1": str(seed_tiers[1]),
        "N_SEED_TIER2": str(seed_tiers[2]),
        "N_SEED_CEIL3": str(ceiling3),
        "TIER_SPLIT": f"{tiers[1]} / {tiers[2]} / {tiers[3]}",
        "N_TERMS": str(sum(len(m.get("terminology") or {}) for m in entries)),
        "N_FIELDS": str(len({r["nav_field"] for r in rows})),
    }

    pieces = [(DOCS / "00-front.md").read_text().rstrip("\n")]
    pieces += [render_entry(m).rstrip("\n") for m in entries]
    pieces += [(DOCS / "99-back.md").read_text().strip("\n")]
    text = "\n\n".join(pieces) + "\n"

    for key, value in values.items():
        text = text.replace("{{" + key + "}}", value)

    leftover = sorted(set(re.findall(r"\{\{([A-Z0-9_]+)\}\}", text)))
    if leftover:
        print(f"error: unresolved placeholders {leftover}", file=sys.stderr)
        return 1

    DIST.mkdir(exist_ok=True)
    path = DIST / "applied_linear_algebra_catalog.md"
    path.write_text(text)
    print(f"wrote {path.relative_to(DIST.parent)}: {len(entries)} entries, "
          f"{len(text)} bytes, tiers {values['TIER_SPLIT']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
