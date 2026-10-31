"""Embed the E. coli core metabolic model used by the stoichiometric-matrix notebook.

The model is BiGG's `e_coli_core` (Orth, Fleming and Palsson, EcoSal Plus 2010): 72
metabolites and 95 reactions of central carbon metabolism, including the exchange
reactions (EX_*) that let metabolites enter and leave the cell and one biomass reaction.
It is downloaded once from BiGG as JSON and cached under data/.cache/.

Only what the linear algebra needs is kept: the metabolite ids, names, formulas and
charges, the reaction ids and names, and the nonzero entries of the stoichiometric matrix
S, one list per reaction (column). Each entry is written as (metabolite index, numerator,
denominator), so the coefficients stay exact rationals in both languages: almost all are
small integers, and the decimals of the biomass reaction (59.81 ATP, ...) become
fractions such as 5981/100.

The data are written into the block between the BEGIN/END BIGG DATA markers in the
notebook and into the `data` section of both snippet files (snippets/04-*.py and .jl),
so all three run standalone.

Usage (maintainers only; needs network access, standard library only):
    uv run python data/prepare_ecoli_core.py
"""
import json
import sys
import urllib.request
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STEM = "04-stoichiometric-matrices-of-reaction-networks"
NOTEBOOK = ROOT / "notebooks" / f"{STEM}.py"
SNIPPETS = ROOT / "snippets" / STEM
CACHE = ROOT / "data" / ".cache" / "e_coli_core.json"
URL = "http://bigg.ucsd.edu/static/models/e_coli_core.json"
EXPECTED_SHAPE = (72, 95)   # metabolites x reactions in the published model


def load():
    """The BiGG JSON model, downloaded on first use and cached."""
    if not CACHE.exists():
        CACHE.parent.mkdir(parents=True, exist_ok=True)
        with urllib.request.urlopen(URL) as resp:
            CACHE.write_bytes(resp.read())
    return json.loads(CACHE.read_text())


def exact(c):
    """A coefficient from the JSON as an exact fraction (the shortest decimal it prints as)."""
    q = Fraction(repr(float(c)))
    if q.limit_denominator(10_000) != q:
        raise ValueError(f"coefficient {c!r} is not a short decimal")
    return q


def model(raw):
    """(metabolites, reactions, columns); columns[j] is a sorted list of
    (0-based metabolite index, Fraction) for reaction j."""
    mets = raw["metabolites"]
    rxns = raw["reactions"]
    index = {m["id"]: i for i, m in enumerate(mets)}
    columns = []
    for r in rxns:
        unknown = set(r["metabolites"]) - set(index)
        if unknown:
            raise ValueError(f"reaction {r['id']} uses unknown metabolites {sorted(unknown)}")
        col = sorted((index[m], exact(c)) for m, c in r["metabolites"].items() if c != 0)
        columns.append(col)
    used = {i for col in columns for i, _ in col}
    if len(used) != len(mets):
        raise ValueError("some metabolites take part in no reaction")
    shape = (len(mets), len(rxns))
    if shape != EXPECTED_SHAPE:
        raise ValueError(f"model is {shape[0]} x {shape[1]}, expected {EXPECTED_SHAPE}; "
                         "BiGG may have changed it, so check the notebook's text")
    return mets, rxns, columns


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


def literal_list(name, items, indent, comment=""):
    """`name = [ ... ]` over several lines; items are already literals."""
    pad = indent + "    "
    return [f"{indent}{name} = [{comment}"] + wrap(items, 100, pad) + [f"{indent}]"]


def column_lines(columns, rxns, indent, base):
    """One line per reaction: [(metabolite index, numerator, denominator), ...]."""
    pad = indent + "    "
    out = []
    for r, col in zip(rxns, columns):
        cells = ", ".join(f"({i + base}, {q.numerator}, {q.denominator})" for i, q in col)
        out.append(f"{pad}[{cells}],   # {r['id']}")
    return out


def block(mets, rxns, columns, indent, julia):
    """The data as Python literals (0-based indices) or Julia literals (1-based)."""
    q = (lambda s: json.dumps(s, ensure_ascii=False)) if julia else repr
    base = 1 if julia else 0
    out = []
    out += literal_list("met_ids", [q(m["id"]) for m in mets], indent)
    out += literal_list("met_names", [q(m["name"]) for m in mets], indent)
    out += literal_list("met_formulas", [q(m["formula"]) for m in mets], indent)
    out += literal_list("met_charges", [str(int(m["charge"])) for m in mets], indent)
    out += literal_list("rxn_ids", [q(r["id"]) for r in rxns], indent)
    out += literal_list("rxn_names", [q(r["name"]) for r in rxns], indent)
    where = "1-based" if julia else "0-based"
    out.append(f"{indent}S_columns = [   # S_columns[j]: (metabolite index ({where}), "
               "numerator, denominator) for each species in reaction j")
    out += column_lines(columns, rxns, indent, base)
    out.append(f"{indent}]")
    return out


def replace_block(path, begin, end, new):
    text = path.read_text()
    start, stop = text.index(begin), text.index(end) + len(end)
    path.write_text(text[:start] + new + text[stop:])
    print(f"wrote the model into {path.relative_to(ROOT)}")


def main():
    raw = load()
    mets, rxns, columns = model(raw)
    nnz = sum(map(len, columns))
    note = f"BiGG {raw['id']}, {len(mets)} metabolites x {len(rxns)} reactions, {nnz} nonzeros"
    nb_begin, nb_end = "    # BEGIN BIGG DATA", "    # END BIGG DATA"
    nb = [f"{nb_begin} (generated by data/prepare_ecoli_core.py; {note})"]
    replace_block(NOTEBOOK, nb_begin, nb_end,
                  "\n".join(nb + block(mets, rxns, columns, "    ", False) + [nb_end]))
    sn_begin, sn_end = "# BEGIN BIGG DATA", "# END BIGG DATA  #hide"
    head = f"{sn_begin}: {note} (written by data/prepare_ecoli_core.py)"
    replace_block(SNIPPETS.with_suffix(".py"), sn_begin, sn_end,
                  "\n".join([head] + block(mets, rxns, columns, "", False) + [sn_end]))
    replace_block(SNIPPETS.with_suffix(".jl"), sn_begin, sn_end,
                  "\n".join([head] + block(mets, rxns, columns, "", True) + [sn_end]))
    print(note)
    return 0


if __name__ == "__main__":
    sys.exit(main())
