"""Run every snippet file in snippets/, so each language's asserts must pass.

Python files run with this interpreter (they need numpy: use the notebooks group).
Julia files run with `julia` from PATH. Locally a missing Julia is skipped with a
warning; in CI (CI=true, set by GitHub Actions) or with --require-julia it is an error.

Usage:
    uv run --group notebooks python build/check_snippets.py
"""
import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

# Make the script runnable from any working directory, and under PYTHONSAFEPATH.
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import ROOT, SNIPPETS_DIR, entry_snippets, load_entries


def run(cmd, path):
    result = subprocess.run(cmd + [str(path)], cwd=ROOT, stdin=subprocess.DEVNULL)
    if result.returncode != 0:
        print(f"error: {path.relative_to(ROOT)} failed", file=sys.stderr)
    return result.returncode == 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--require-julia", action="store_true",
                        help="fail instead of skipping when julia is not installed")
    args = parser.parse_args()
    for meta in load_entries():
        entry_snippets(meta)              # validates that each set of files matches
    julia = shutil.which("julia")
    if julia is None and (args.require_julia or os.environ.get("CI") == "true"):
        print("error: julia not found on PATH", file=sys.stderr)
        return 1
    ok, count = True, 0
    for path in sorted(SNIPPETS_DIR.glob("*.py")):
        ok &= run([sys.executable], path)
        count += 1
    for path in sorted(SNIPPETS_DIR.glob("*.jl")):
        if julia is None:
            print(f"warning: julia not found; skipped {path.relative_to(ROOT)}")
            continue
        ok &= run([julia, "--startup-file=no"], path)
        count += 1
    if ok:
        print(f"{count} snippet file(s) ran cleanly")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
