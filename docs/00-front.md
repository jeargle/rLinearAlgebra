# Applied Linear Algebra: An Initial Collection

**Version 0.1 — seed set of 10 problems**

Selection criteria for this first pass:

1. **One application domain each.** No two entries come from the same subfield or community of practice. At the coarse level used in the companion index, three entries fall under Engineering (civil/mechanical FEA, aerospace/control, communications) and two under Computer Science (network science, computer vision); these are distinct disciplines in practice, sharing only a top-level bucket. The set spans seven coarse fields and ten distinct subfields.
2. **One distinct linear-algebra concept each.** Entry 1 is a sparse SPD solve; entry 5 is a nonnegative-matrix spectral radius; entry 7 is linear algebra over a finite field. If two problems reduce to the same mathematical object, only one is in the seed set and the other is in the backlog.
3. **Deployed, not illustrative.** Every entry is something an engineer, scientist, or company actually runs in production or in published research — not a textbook exercise dressed in application clothing.
4. **The matrix structure is the point.** In each case, *what kind of matrix it is* (sparse, symmetric, stochastic, rank-deficient, over GF(2)) determines which algorithm is viable. That is the through-line worth teaching.

## Entry template

Each entry follows the same template so the collection can grow uniformly.

1. **Start here** — the problem in plain terms, for a reader with calculus and a first course in linear
   algebra who knows nothing about the field. No domain jargon, no notation; it should be readable by
   someone deciding whether this is even the right entry. Collapsed by default where the renderer
   supports it.
2. **Field** and **Tier**.
3. **Scalars and vectors** — the scalar field and the vector space, stated explicitly rather than left
   to be inferred. Which field the scalars come from (ℝ, ℂ, GF(2), GF(p), ℚ), what the vectors actually
   are (ℝⁿ for a stated n, polynomials of degree at most 3, continuous functions on [0,1], the tensor
   product (ℂ²)^⊗n), and where the objects live when that is easy to get wrong — that flux vectors and
   concentration vectors inhabit *different* spaces, that a probability distribution is not a subspace,
   that a covariance matrix is a vector in the space of symmetric matrices, that an essential matrix is
   determined only up to scale. Both values are also index columns (`scalar_field`, `vector_space`).
4. **The problem**, **Formulation**, **Matrix structure**, **What is computed**, **Why linear algebra is
   the right tool**, **Pitfall worth teaching**.
5. **Terminology map** — the field's vocabulary against the linear-algebra object each word names.
6. **Extensions**.

**A rendering caveat.** The "Start here" block uses `<details>`/`<summary>`, which collapses on GitHub,
in Quarto and Jupyter Book output, and in most static site generators — but **not on a Reddit wiki**,
which renders markdown only and strips raw HTML. The wiki build must therefore emit that block as an
ordinary `### Start here` subsection instead. Since the wiki is the planned front door for a
non-specialist audience, and this section is written precisely for that audience, it should stay at the
top of the page there rather than being moved or dropped.

---

# Audience and organizing principle

**Primary reader.** Someone competent in linear algebra who encounters a question posed in a field they
do not know. This is the recurring situation in general linear-algebra forums: a question arrives
carrying domain vocabulary — stiffness matrix, flux mode, syndrome, EOF, Leontief inverse — and the
mathematics is well within the reader's reach once the terminology is decoded. The bottleneck is
translation, not technique.

That makes the collection a **decoder**, not only a tour. Three consequences:

1. **Field is the primary organizing axis.** A reader arrives knowing the domain the question came from
   and nothing else about it. Navigation is by discipline; the linear-algebra concept index is the
   secondary cross-reference, for the reverse lookup ("this is a dominant-eigenvector problem — where
   else does that show up?").
2. **Every entry carries a terminology map.** A two-column table from the field's own vocabulary to the
   linear-algebra object it names. These are aggregated into a single sorted lookup table,
   `domain_terminology_map.csv`, which is the fastest path for a reader who has one unfamiliar word and
   needs to know what it means mathematically.
3. **Entries must name the question shapes, not just the mathematics.** What a practitioner in the field
   actually asks — and the vocabulary they will use to ask it — matters as much as the formulation.

The three kinds of question this is meant to serve (homework, a problem at work, and general curiosity
from outside mathematics) differ in tier but not in structure: all three need the same domain-to-linear-
algebra bridge, which is why the tier scheme and the field axis are independent of one another.

## Navigation taxonomy

{{N_FIELDS}} fields, sized so that no heading is a catch-all. `Engineering` and `Computer Science` from the
original index were too coarse to navigate once field became the primary axis, and have been split; the
original coarse `field` column is retained for coarse filtering.

{{NAV_TABLE}}

**Thin spots now visible.** Making field the navigation spine exposes where the spine is weak. Medicine &
Imaging and Physics & Quantum Chemistry each hold a single entry, and Physics is represented only by
quantum mechanics — nothing from classical mechanics, optics, thermodynamics, or relativity. Life
Sciences and Machine Learning & Data have no Tier 1 entry at all, so a reader arriving from either field
meets an eigenvalue problem immediately. There is no materials science, no acoustics, and no social
science outside economics. These gaps were invisible when the collection was organized by concept.

# Difficulty tiers

Three tiers, defined by what a reader must already know. Tier boundaries are set by *prerequisite
knowledge*, not by how hard the problem is to solve or how large the matrices get — a Tier 1 entry may
involve a genuinely difficult modeling question, and a Tier 3 entry may reduce to a two-line
computation once the setup is understood.

### Tier 1 — first-course linear algebra, up to but not including eigenvalues

Vectors and matrices, matrix multiplication and its noncommutativity, linear systems and Gaussian
elimination, LU, inverses, determinants, rank, the four fundamental subspaces, linear independence,
bases and dimension, change of basis, inner products and orthogonality, projections, least squares,
Gram–Schmidt and QR.

Deliberately included at this tier: vector spaces over scalars other than the reals. Polynomial spaces,
complex-valued vectors, finite fields such as GF(2) and GF(p), and function spaces with an integral
inner product all belong here, because each of them exercises the *definition* of a vector space rather
than any machinery beyond a first course. So do the 2D and 3D graphics transformations, which are pure
change-of-basis and composition problems in small dimension.

### Tier 2 — eigenvalues, eigenvectors, and later-course material

Eigenvalues and eigenvectors, diagonalization, the spectral theorem, similarity, the SVD, positive
definiteness, matrix norms and condition numbers, pseudoinverses, Perron–Frobenius, stochastic matrices
and stationary distributions, Jordan form, and iterative methods for large systems.

### Tier 3 — requires substantial mathematics outside linear algebra

The linear algebra may be no harder than Tier 2, but the problem cannot be posed or interpreted without
another body of theory: differential equations (ordinary or partial), abstract algebra beyond basic
finite fields (field extensions, quotient rings, group representations), measure-theoretic probability
or stochastic processes, convex analysis and duality, functional analysis, or algebraic geometry. The
index records the specific prerequisite per entry in `prereq_beyond_la`.

### Boundary conventions

- An entry is tiered by **how it is posed in this collection**, not by the deepest treatment that
  exists in the literature. The index carries a separate `tier_ceiling` column recording the tier its
  extensions reach.
- Where a Tier 2 or Tier 3 entry has a genuine Tier 1 entry point — static GNSS trilateration under
  Kalman filtering, chemical-equation balancing under stoichiometric matrices, the 2D homography under
  multiple-view geometry — that on-ramp is named in the entry rather than split into a separate row.
- Calculus is assumed throughout and does not by itself raise an entry to Tier 3; the Fourier-series
  projection entry needs integration but stays at Tier 1.

**Current distribution.** Of the {{N_SEED}} seed entries, {{N_SEED_TIER1}} are Tier 1 (structural statics, stoichiometric
matrices, Leontief, error-correcting codes) and {{N_SEED_TIER2}} are Tier 2; none is Tier 3 as posed, though {{N_SEED_CEIL3}} have a
Tier 3 ceiling. Across all {{N_TOTAL}} catalogued problems the split is {{TIER_SPLIT}}.

---
