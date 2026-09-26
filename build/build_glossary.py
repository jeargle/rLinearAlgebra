"""Generate dist/domain_terminology_map.csv from the terminology blocks in entries/*.md.

This is the collection's fastest lookup for a reader holding one unfamiliar domain word.

Usage:  python build/build_glossary.py
"""
import csv
import sys
from pathlib import Path

# Make the script runnable from any working directory, and under PYTHONSAFEPATH.
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import DIST, load_entries

COLUMNS = ["domain_term", "entry_id", "linear_algebra_meaning",
           "entry_title", "field", "subfield"]


def main():
    rows = []
    for meta in load_entries():
        terms = meta.get("terminology") or {}
        if not terms:
            print(f"warning: entry {meta['id']} has no terminology map", file=sys.stderr)
        for term, meaning in terms.items():
            rows.append({
                "domain_term": term,
                "entry_id": meta["id"],
                "linear_algebra_meaning": meaning,
                "entry_title": meta.get("short_title", meta.get("title", "")),
                "field": meta.get("field", ""),
                "subfield": meta.get("subfield", ""),
            })

    rows.sort(key=lambda r: (r["domain_term"], r["entry_id"]))

    collisions = {}
    for r in rows:
        collisions.setdefault(r["domain_term"], []).append(r["entry_id"])
    shared = {t: ids for t, ids in collisions.items() if len(ids) > 1}
    if shared:
        # Not an error: the same word legitimately means different things in different
        # fields, which is exactly what this table exists to disambiguate.
        print(f"note: {len(shared)} term(s) appear in more than one entry: "
              f"{sorted(shared)}", file=sys.stderr)

    DIST.mkdir(exist_ok=True)
    path = DIST / "domain_terminology_map.csv"
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=COLUMNS)
        writer.writeheader()
        writer.writerows(rows)

    print(f"wrote {path.relative_to(DIST.parent)}: {len(rows)} terms "
          f"from {len({r['entry_id'] for r in rows})} entries")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
