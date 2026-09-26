"""Generate dist/index.csv from entries/*.md frontmatter and backlog.yaml.

Usage:  python build/build_index.py
"""
import csv
import sys
from pathlib import Path

# Make the script runnable from any working directory, and under PYTHONSAFEPATH.
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import DIST, INDEX_COLUMNS, load_all


def row_for(meta):
    out = {}
    for col in INDEX_COLUMNS:
        if col == "title":
            # The index carries the short title; the long prose title lives in the entry.
            value = meta.get("short_title", meta.get("title", ""))
        else:
            value = meta.get(col, "")
        out[col] = "" if value is None else value
    return out


def main():
    rows = [row_for(m) for m in load_all()]

    missing = [
        (r["id"], col)
        for r in rows
        for col in ("title", "nav_field", "tier", "scalar_field", "vector_space")
        if r[col] == ""
    ]
    if missing:
        print(f"error: required fields empty: {missing}", file=sys.stderr)
        return 1

    DIST.mkdir(exist_ok=True)
    path = DIST / "index.csv"
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=INDEX_COLUMNS)
        writer.writeheader()
        writer.writerows(rows)

    seed = sum(1 for r in rows if r["status"] == "seed")
    tiers = {t: sum(1 for r in rows if r["tier"] == t) for t in (1, 2, 3)}
    print(f"wrote {path.relative_to(DIST.parent)}: {len(rows)} entries "
          f"({seed} seed), tiers {tiers[1]}/{tiers[2]}/{tiers[3]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
