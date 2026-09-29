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

## Continuous integration

`.github/workflows/build.yml` runs on every push to `main` and on pull requests:

1. installs with `uv sync --locked` and regenerates `dist/` from `entries/` and `backlog.yaml`;
2. **fails if the committed `dist/` differs from what the sources produce** — this is what makes
   "`dist/` is generated" an enforced rule rather than a convention. If it fails, run
   `uv run python build/build_all.py` locally and commit the result;
3. builds `site/` and checks that no link is absolute (an absolute path breaks a project site served
   under `/rLinearAlgebra/`) and that `site/.nojekyll` exists;
4. on `main` only, deploys `site/` to GitHub Pages.

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
   - **Formulation** states what each equation models. If the matrix problem comes from a differential
     equation, start from that equation, show the step that produces the matrix problem, and say what a
     matrix solution means for the differential equation's solutions.
4. Add a `terminology:` mapping — this is the collection's most-used asset.
5. Run `uv run python build/build_all.py`.
