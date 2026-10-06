"""Build the 15-sector US input-output table used by the Leontief notebook.

Source: US Bureau of Economic Analysis (BEA), annual input-output accounts, sector
level (15 industries), year 2023, Make and Use tables after redefinitions, producer
prices, millions of dollars. Release bundle dated September 2024:
    https://apps.bea.gov/industry/iTables%20Static%20Files/AllTablesIO.zip

BEA's tables are commodity-by-industry. The notebook needs a square
industry-by-industry flow matrix Z, so this script applies BEA's standard
market-share transformation (Concepts and Methods of the U.S. Input-Output
Accounts, ch. 12):

    B = U g^-1          commodity inputs per dollar of industry output
    D = V q^-1          share of each commodity produced by each industry,
                        scaled up by 1/(1 - scrap share) of each industry
    Z = D U,  d = D f   industry-by-industry flows and final demand

so that A = Z x^-1 = D B with x = g, industry gross output. With these numbers,
(I - A)^-1 d recovers every industry's published 2023 gross output to within
about 0.1%, which the notebook shows as a check.

The result is written as plain literals into three places, each between BEGIN/END
BEA DATA markers: the notebook (so it runs in the browser with no data files) and
the `data` section of both snippet files (so snippets/05-*.jl and .py run on the
real table as they stand).

Usage (maintainers only; needs network access and openpyxl):
    uv run --group data python data/prepare_bea_2023.py
"""
import io
import json
import sys
import urllib.request
import zipfile
from pathlib import Path

import numpy as np
import openpyxl

ROOT = Path(__file__).resolve().parent.parent
NOTEBOOK = ROOT / "notebooks" / "05-leontief-input-output-economics.py"
CACHE = ROOT / "data" / ".cache" / "AllTablesIO.zip"
URL = "https://apps.bea.gov/industry/iTables%20Static%20Files/AllTablesIO.zip"
YEAR = "2023"
USE = "IOUse_After_Redefinitions_PRO_1997-2023_Sector.xlsx"
MAKE = "IOMake_After_Redefinitions_PRO_1997-2023_Sector.xlsx"
BEGIN, END = "    # BEGIN BEA DATA", "    # END BEA DATA"
N = 15

SHORT = {"11": "Agriculture", "21": "Mining", "22": "Utilities", "23": "Construction",
         "31G": "Manufacturing", "42": "Wholesale trade", "44RT": "Retail trade",
         "48TW": "Transportation", "51": "Information", "FIRE": "Finance & real estate",
         "PROF": "Professional services", "6": "Education & health",
         "7": "Arts, food & lodging", "81": "Other services", "G": "Government"}


def fetch():
    if not CACHE.exists():
        CACHE.parent.mkdir(parents=True, exist_ok=True)
        with urllib.request.urlopen(URL) as resp:
            CACHE.write_bytes(resp.read())
    return zipfile.ZipFile(CACHE)


def sheet(zf, name):
    wb = openpyxl.load_workbook(io.BytesIO(zf.read(name)), read_only=True, data_only=True)
    return [list(r) for r in wb[YEAR].iter_rows(values_only=True)]


def num(c):
    return 0.0 if c in (None, "...", "") else float(c)


def block(rows, r0, nrows, c0, ncols):
    """Numeric block; r0 and c0 are 0-based indices into the sheet."""
    return np.array([[num(c) for c in r[c0:c0 + ncols]] for r in rows[r0:r0 + nrows]])


def find_row(rows, label):
    return next(i for i, r in enumerate(rows) if r[1] and str(r[1]).startswith(label))


def build(zf):
    use, make = sheet(zf, USE), sheet(zf, MAKE)
    r0 = next(i for i, r in enumerate(use) if r[0] == "11")   # first commodity row
    codes = [str(r[0]) for r in use[r0:r0 + N]]
    assert codes == list(SHORT), f"unexpected sector codes {codes}"
    U = block(use, r0, N, 2, N)                                # commodity x industry
    # columns after the industries: Total Intermediate, 6 final-use columns, Total Final Uses
    f = block(use, r0, N, 2 + N + 7, 1)[:, 0]                  # Total Final Uses (net of imports)
    g = block(use, find_row(use, "Total Industry Output"), 1, 2, N)[0]
    m0 = next(i for i, r in enumerate(make) if r[0] == "11")
    V = block(make, m0, N, 2, N + 2)                           # industry x (15 + Used + Other)
    q = block(make, find_row(make, "Total Commodity Output"), 1, 2, N + 2)[0]
    scrap = V[:, N] / g
    D = (V[:, :N] / q[:N]) / (1 - scrap)[:, None]
    return codes, D @ U, D @ f, g


def fmt(v):
    return f"{v:.0f}"


def literal_py(codes, Z, d, x, begin, end, pad):
    """Python literals; `pad` indents them (the notebook block sits inside a cell)."""
    lines = [begin, f"{pad}sectors = " + repr([SHORT[c] for c in codes]), f"{pad}Z_us = np.array(["]
    lines += [f"{pad}    [" + ", ".join(fmt(v) for v in row) + "]," for row in Z]
    lines += [f"{pad}], dtype=float)",
              f"{pad}d_us = np.array([" + ", ".join(fmt(v) for v in d) + "], dtype=float)",
              f"{pad}x_us = np.array([" + ", ".join(fmt(v) for v in x) + "], dtype=float)",
              end]
    return "\n".join(lines)


def literal_jl(codes, Z, d, x, begin, end):
    """Julia literals: a matrix is written row by row, entries separated by spaces."""
    lines = [begin, "sectors = " + json.dumps([SHORT[c] for c in codes]), "Z_us = Float64["]
    lines += ["    " + " ".join(fmt(v) for v in row) for row in Z]
    lines += ["]",
              "d_us = Float64[" + ", ".join(fmt(v) for v in d) + "]",
              "x_us = Float64[" + ", ".join(fmt(v) for v in x) + "]",
              end]
    return "\n".join(lines)


SNIPPET_BEGIN = (f"# BEGIN BEA DATA: US {YEAR}, 15 sectors, $ millions "
                 "(written by data/prepare_bea_2023.py)")
SNIPPET_END = "# END BEA DATA  #hide"
SNIPPETS = ROOT / "snippets" / "05-leontief-input-output-economics"


def targets(codes, Z, d, x):
    """(file, begin marker, end marker, replacement text) for every copy of the data."""
    nb_begin = BEGIN + f" (generated by data/prepare_bea_2023.py; {YEAR}, $ millions)"
    return [
        (NOTEBOOK, BEGIN, END, literal_py(codes, Z, d, x, nb_begin, END, "    ")),
        (SNIPPETS.with_suffix(".py"), "# BEGIN BEA DATA", SNIPPET_END,
         literal_py(codes, Z, d, x, SNIPPET_BEGIN, SNIPPET_END, "")),
        (SNIPPETS.with_suffix(".jl"), "# BEGIN BEA DATA", SNIPPET_END,
         literal_jl(codes, Z, d, x, SNIPPET_BEGIN, SNIPPET_END)),
    ]


def main():
    codes, Z, d, x = build(fetch())
    A = Z / x
    err = np.abs(np.linalg.solve(np.eye(N) - A, d) / x - 1).max()
    assert err < 0.005, f"closure check failed: max relative error {err:.4f}"
    for path, begin, end, new in targets(codes, Z, d, x):
        text = path.read_text()
        start, stop = text.index(begin), text.index(end) + len(end)
        path.write_text(text[:start] + new + text[stop:])
        print(f"wrote BEA {YEAR} data into {path.relative_to(ROOT)}")
    print(f"closure error {err:.2e}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
