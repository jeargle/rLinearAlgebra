"""Regression tests for the first-use Wikipedia linker in build/common.py.

Run with:  uv run python tests/test_linker.py
Exits non-zero on the first failure. No test framework needed.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "build"))

from common import _compile_pattern, link_first_uses, load_terms  # noqa: E402

URL = "https://en.wikipedia.org/wiki/Example"


def term(name, *patterns):
    return {"term": name, "url": URL, "entries": {1},
            "patterns": [_compile_pattern(p) for p in patterns]}


SVD = term("SVD", r"\bSVD\b", r"singular value decomposition")
SPARSE = term("sparse", r"\bsparse\b")
LANCZOS = term("Lanczos", r"Lanczos")
BLOCK = term("block Lanczos", r"block Lanczos")
STOICH = term("stoichiometry", r"stoichiometr")


def linked(text, *terms):
    return link_first_uses(text, list(terms), set())


def test_links_only_first_use():
    out = linked("The SVD is useful. Compute the SVD again.", SVD)
    assert out.count("](") == 1, out
    assert out.startswith(f"The [SVD]({URL})"), out


def test_text_after_a_heading_is_still_linked():
    # Regression: under re.S the heading pattern once swallowed the whole page.
    out = linked("# Title\n\nThe matrix is sparse.\n", SPARSE)
    assert f"[sparse]({URL})" in out, out
    assert out.startswith("# Title\n"), out


def test_text_after_a_table_row_is_still_linked():
    out = linked("| a | b |\n|---|---|\n\nThe matrix is sparse.\n", SPARSE)
    assert f"[sparse]({URL})" in out, out


def test_protected_regions_are_never_linked():
    for text in ["# The SVD\n", "| SVD | x |\n", "`SVD`", "```\nSVD\n```",
                 "[SVD](https://example.org)", "https://example.org/SVD"]:
        assert linked(text, SVD) == text, text


def test_first_use_skips_protected_occurrences():
    out = linked("`SVD` in code, then the SVD in prose.", SVD)
    assert out == f"`SVD` in code, then the [SVD]({URL}) in prose.", out


def test_longer_overlapping_match_wins():
    out = linked("Use block Lanczos here.", LANCZOS, BLOCK)
    assert f"[block Lanczos]({URL})" in out and out.count("](") == 1, out


def test_match_extends_to_end_of_word():
    out = linked("The stoichiometric matrix.", STOICH)
    assert f"[stoichiometric]({URL})" in out, out


def test_no_match_inside_a_hyphenated_or_longer_word():
    assert linked("backprojection and skew-sparse", SPARSE) == "backprojection and skew-sparse"


def test_done_set_is_shared_across_pieces_of_one_page():
    done = set()
    first = link_first_uses("The SVD.", [SVD], done)
    second = link_first_uses("The SVD again.", [SVD], done)
    assert "](" in first and "](" not in second, (first, second)


def test_every_registry_url_is_percent_encoded():
    # A raw ')' in a URL ends a markdown link early, on Reddit and elsewhere.
    for t in load_terms():
        path = t["url"].split("/wiki/", 1)[1]
        assert "(" not in path and ")" not in path and " " not in path, t["url"]


def main():
    tests = [(n, f) for n, f in globals().items() if n.startswith("test_") and callable(f)]
    for name, fn in tests:
        fn()
        print(f"ok  {name}")
    print(f"{len(tests)} tests passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
