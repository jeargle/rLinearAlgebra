"""Run every generator in order. Nothing here publishes; see build_wiki.py --push.

Usage:  python build/build_all.py
"""
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
STEPS = ["build_index.py", "build_glossary.py", "build_catalog.py", "build_wiki.py",
         "sync_snippets.py"]


def main():
    for step in STEPS:
        result = subprocess.run([sys.executable, str(HERE / step)])
        if result.returncode != 0:
            print(f"error: {step} failed", file=sys.stderr)
            return result.returncode
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
