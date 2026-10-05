"""Check and export the marimo notebooks in notebooks/ into site/notebooks/.

Each notebook is named after its entry (notebooks/05-leontief-input-output-economics.py
for entries/05-leontief-input-output-economics.md) and is exported as one self-contained
HTML page that runs Python in the browser (Pyodide, WebAssembly). `--single-file` loads
marimo's interface and the Python runtime from a CDN, so each page is under 100 KB and
there is no shared assets/ folder to keep alongside it.

Run this AFTER build_site.py, which deletes and recreates site/.

Usage:
    uv run --group notebooks python build/build_notebooks.py           # check, then export
    uv run --group notebooks python build/build_notebooks.py --check   # run as scripts only
"""
import argparse
import os
import subprocess
import sys
from pathlib import Path

# Make the script runnable from any working directory, and under PYTHONSAFEPATH.
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import ROOT, notebook_paths

SITE = ROOT / "site"


def check(nb):
    """Run the notebook top to bottom as a plain Python script; its asserts must pass."""
    env = dict(os.environ, MPLBACKEND="Agg")
    result = subprocess.run([sys.executable, str(nb)], env=env, cwd=ROOT)
    if result.returncode != 0:
        print(f"error: {nb.relative_to(ROOT)} failed when run as a script", file=sys.stderr)
    return result.returncode == 0


def export(nb):
    out = SITE / "notebooks" / f"{nb.stem}.html"
    out.unlink(missing_ok=True)
    cmd = [sys.executable, "-m", "marimo", "export", "html-wasm", str(nb), "-o", str(out),
           "--single-file", "--mode", "run", "--show-code", "--force"]
    result = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
    # marimo can exit 0 without writing the page (e.g. when uv is missing), so check the file
    if result.returncode != 0 or not out.exists():
        print(result.stdout + result.stderr, file=sys.stderr)
        print(f"error: export of {nb.relative_to(ROOT)} produced no page", file=sys.stderr)
        return False
    print(f"exported {out.relative_to(ROOT)} ({out.stat().st_size // 1024} KB)")
    return True


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true",
                        help="only run each notebook as a script; do not export")
    args = parser.parse_args()
    notebooks = notebook_paths()
    if not all(check(nb) for nb in notebooks):
        return 1
    print(f"{len(notebooks)} notebook(s) ran cleanly as scripts")
    if args.check:
        return 0
    if not (SITE / "index.html").exists():
        print("error: run build/build_site.py first; it recreates site/", file=sys.stderr)
        return 1
    return 0 if all(export(nb) for nb in notebooks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
