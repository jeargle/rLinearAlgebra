# Applied Linear Algebra

A collection of real problems from across science, engineering, and mathematics, each one worked as a
linear-algebra problem — with the domain's own vocabulary translated as you go.

It is built for the person *answering* a domain-specific question who knows the linear algebra but not
the field. Entries are organized by field for that reason, and every entry carries a terminology map
from the field's words to the mathematical objects they name.

## Source of truth

Two places, and only two:

| Path | Holds |
|---|---|
| `entries/*.md` | One written entry each: YAML frontmatter (all metadata) + markdown body (all prose) |
| `backlog.yaml` | Catalogued but unwritten candidates — metadata only |

`docs/00-front.md` and `docs/99-back.md` hold the surrounding editorial prose, with `{{PLACEHOLDER}}`
slots wherever a number or table is computed from the entries.

**Everything in `dist/` is generated. Do not edit it, and do not hand-maintain a copy of anything that
appears in an entry's frontmatter.** Field tallies, tier counts, the index, and the glossary all derive
from the entry files, so the prose cannot drift away from the metadata.

An entry graduates from `backlog.yaml` into `entries/` when someone writes it up.

## Building

Dependencies are managed with [uv](https://docs.astral.sh/uv/). `uv run` creates and syncs the
environment on demand, so there is no activation step:

```sh
uv run python build/build_all.py        # everything
```

or individually:

| Command | Output |
|---|---|
| `uv run python build/build_index.py` | `dist/index.csv` — every entry, all metadata columns |
| `uv run python build/build_glossary.py` | `dist/domain_terminology_map.csv` — domain term → linear-algebra meaning |
| `uv run python build/build_catalog.py` | `dist/applied_linear_algebra_catalog.md` — the single-document catalog |
| `uv run python build/build_wiki.py` | `dist/reddit_wiki/*.md` — one page per entry plus index and glossary |
| `uv run python build/build_site.py` | `site/` — static HTML, deployable to GitHub Pages (not committed) |

`pyproject.toml` declares the dependencies and `uv.lock` pins exact versions; both are committed, and
CI installs with `uv sync --locked` so it fails rather than silently re-resolving if they disagree.
`praw` is in a separate `publish` dependency group, so an ordinary build never installs it:

```sh
uv sync --group publish        # only needed to push to the wiki
```

To preview the site exactly as it will be served:

```sh
uv run python build/build_site.py
uv run python -m http.server --directory site 8000
```

Opening the files directly from disk is not equivalent — serve over HTTP.

## Notebooks

`notebooks/` holds one [marimo](https://marimo.io) notebook per entry that has one, named after
its entry file (`notebooks/05-leontief-input-output-economics.py` for
`entries/05-leontief-input-output-economics.md`). The entry's site and wiki pages link to it
automatically. Each notebook starts with a tiny toy version of the problem that can be checked by
hand; when the realistic version is large, a second, realistic-size problem follows.

```sh
uv run --group notebooks marimo edit notebooks/05-leontief-input-output-economics.py   # work on one
uv run --group notebooks python build/build_notebooks.py --check   # run all as plain scripts
uv run --group notebooks python build/build_notebooks.py           # also export into site/notebooks/
```

Run the export after `build_site.py`, which recreates `site/`. Each notebook is exported as a single
HTML page that runs Python in the browser (Pyodide); marimo's interface and the Python runtime load
from a CDN, so nothing large is deployed. Notebooks must embed their data or compute it, since the
browser has no access to the repository.

Real datasets are prepared by scripts in `data/`, which download the source and write the numbers
into a marked block in the notebook. For example, `uv run --group data python
data/prepare_bea_2023.py` rebuilds the Leontief notebook's 15-sector US table from the Bureau of
Economic Analysis release. Downloads are cached in `data/.cache/`, which is not committed.

## Code snippets (Python and Julia)

`snippets/` holds, for an entry, a matched pair of files: `snippets/NN-slug.py` and
`snippets/NN-slug.jl`. Each is split into named sections, one per core computation:

```
# --- snippet solve: Solve (I − A) x = d ---
```

Both files must have the same section names and titles, in the same order, or the build fails.
Snippets use the notebook's own variable names (`A_toy`, `x_toy`, `A_us`, `L_us`, ...), so the
Python cell and the Julia block beneath it read alike. A line ending in `#hide` runs but is not
shown; sections that mirror the realistic part of a notebook use it to load the toy numbers under
the realistic names and to keep checks against toy values out of sight.
Every section asserts its result on the entry's hand-worked toy example, so the files are
runnable tests:

```sh
uv run --group notebooks python build/check_snippets.py   # runs both languages; needs julia on PATH
```

The sections appear in two places. The entry's site page gets an **In code** section with
Python and Julia tabs. The entry's notebook shows the Julia sections behind a *Show Julia
equivalents* switch, beneath the Python cells that do the same work. The notebook can't run
Julia, so `build/sync_snippets.py` (part of `build_all.py`) copies the Julia text into a generated
block in the notebook. CI fails if a committed notebook's block is out of date. The Reddit wiki
does not show snippets.

## Continuous integration

`.github/workflows/build.yml` runs on every push to `main` and on pull requests:

1. installs with `uv sync --locked --group notebooks`, runs the linker tests, runs each notebook
   as a plain script, installs Julia, and runs every Python and Julia snippet file;
2. regenerates `dist/` from `entries/` and `backlog.yaml`, and the Julia blocks in `notebooks/`
   from `snippets/`;
3. **fails if the committed `dist/` or `notebooks/` differs from what the sources produce** — this
   is what makes "generated files are generated" an enforced rule rather than a convention. If it
   fails, run `uv run python build/build_all.py` locally and commit the result;
4. builds `site/`, exports the notebooks into `site/notebooks/`, and checks that no link is absolute
   (an absolute path breaks a project site served under `/rLinearAlgebra/`) and that
   `site/.nojekyll` exists;
5. on `main` only, deploys `site/` to GitHub Pages.

**One-time setup:** Settings → Pages → Build and deployment → Source → **GitHub Actions**. Without
this the deploy step fails.

`.github/workflows/wiki.yml` (shown as *publish-wiki* in the Actions tab) is manual
(`workflow_dispatch`) and defaults to a dry run that
renders the pages and lists them in the job summary. A live push requires unchecking *dry run* and
typing `publish` in the confirmation field, and reads these repository secrets: `REDDIT_CLIENT_ID`,
`REDDIT_CLIENT_SECRET`, `REDDIT_USERNAME`, `REDDIT_PASSWORD`, plus an optional `REDDIT_SUBREDDIT`
repository variable.

## Publishing to the subreddit wiki

`build_wiki.py` renders only. Publishing is a separate explicit flag so a build never posts by accident:

```sh
uv run --group publish python build/build_wiki.py --push
```

It reads `REDDIT_CLIENT_ID`, `REDDIT_CLIENT_SECRET`, `REDDIT_USERNAME`, `REDDIT_PASSWORD`, and
optionally `REDDIT_SUBREDDIT` (default `LinearAlgebra`), from the environment — repository secrets in
CI. You need a script-type OAuth app registered on the Reddit account.

Set the wiki to moderator-only editing. The wiki is a generated mirror; anything edited there directly
is overwritten by the next push. Contributions belong in issues and pull requests here.

## Rendering differences between targets

The same entry renders differently per destination, and the generators handle it:

- **Catalog / static site** — the plain-terms introduction is a collapsible `<details>` block.
- **Reddit wiki** — Reddit strips raw HTML, so the same section becomes a plain `### Start here`
  heading, kept at the top of the page. Reddit also has no dependable math typesetting, which is why
  display equations live in fenced code blocks throughout.

Pipes inside table cells are escaped at render time, so terminology entries like `G = [I | P]` survive.

## Wikipedia links

`terms.yaml` lists terms used in the entries, each with the Wikipedia article that explains it.
Every term with a `url` is linked **once per page, at its first use**. The same rules apply to the
catalog, the wiki, and the site:

- **Entry pages** link only the terms whose `entries` list includes that entry. A word or abbreviation
  can mean different things in different fields (DFT is density functional theory in the quantum
  entry but the discrete Fourier transform elsewhere), so matching is never global.
- **The catalog** is one page: each term is linked at its first use in any entry section. Its editorial
  front and back matter is not linked.
- **Glossary pages** link only their introductory prose. **Index pages** are navigation and get no links.
- Nothing inside code, display equations, headings, table rows (including the Variables and terminology
  tables), existing links, or URLs is ever linked.

Each term's `match` field holds the regular expressions for its link text. See the comment at the top of
`terms.yaml` for the rules. When adding a term, check that its article exists and is not a
disambiguation page, and record where it is used in `entries`. A pattern that is too general links the
wrong sense of a word: `observab` once linked "observables" in the quantum entry to control-theory
observability. The fix is to narrow the pattern or the entry list, not to delete the term.

`uv run python tests/test_linker.py` checks the linker's rules; CI runs it on every push.

## Adding an entry

1. Move its row out of `backlog.yaml` and create `entries/NN-slug.md`.
2. Frontmatter needs at minimum: `id`, `slug`, `status`, `title`, `short_title`, `field_label`,
   `tier`, `tier_note`, `tier_ceiling`, `nav_field`, `field`, `subfield`, `scalar_field`,
   `vector_space`, `underlying_equations`, and the remaining index columns.
3. The body needs these sections, in order:
   `## Start here`, `## The problem`, `## Variables`, `## Formulation`, `## Matrix structure`,
   `## What is computed`, `## Why linear algebra is the right tool`, `## Pitfall worth teaching`,
   `## Extensions`. The build fails if any is missing.
   - **Variables** is a table with columns *Symbol, Name, What it holds, Shape, Units*. Every symbol
     used in an equation must appear here first. Do not put a raw `|` inside a cell; it splits the row.
   - **GF(2) must be defined at its first use** on every page except Tier 3 entry pages, because few
     readers have taken abstract algebra. "First use" includes the tier note and the scalar-field
     line, which render near the top of the page. The build fails if "modulo 2" (or "mod 2") does not
     appear near the first "GF(2)". The shared wording lives in `build/common.py` (`GF2_DEF`,
     `GF2_SHORT`, `FIELD_DEF`); the index and glossary pages insert it automatically.
   - **Formulation** states what each equation models. If the matrix problem comes from a differential
     equation, start from that equation, show the step that produces the matrix problem, and say what a
     matrix solution means for the differential equation's solutions.
4. Add a `terminology:` mapping — this is the collection's most-used asset.
5. Run `uv run python build/build_all.py`.
