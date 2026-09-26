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

17 fields, sized so that no heading is a catch-all. `Engineering` and `Computer Science` from the
original index were too coarse to navigate once field became the primary axis, and have been split; the
original coarse `field` column is retained for coarse filtering.

| Field | Entries | of which Tier 1 |
|---|---|---|
| Computer Graphics & Vision | 6 | 5 |
| Life Sciences | 5 | 0 |
| Machine Learning & Data | 5 | 0 |
| Mathematics & Numerical Analysis | 4 | 3 |
| Signal Processing | 4 | 2 |
| Chemistry & Chemical Engineering | 3 | 2 |
| Computer Science & Networks | 3 | 1 |
| Earth & Climate Science | 3 | 1 |
| Economics, Finance & Operations Research | 3 | 1 |
| Electrical Engineering | 3 | 2 |
| Statistics | 3 | 3 |
| Civil & Mechanical Engineering | 2 | 2 |
| Communications & Information Theory | 2 | 2 |
| Control & Robotics | 2 | 1 |
| Cryptography & Security | 2 | 1 |
| Medicine & Imaging | 1 | 0 |
| Physics & Quantum Chemistry | 1 | 0 |

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

**Current distribution.** Of the 10 seed entries, 4 are Tier 1 (structural statics, stoichiometric
matrices, Leontief, error-correcting codes) and 6 are Tier 2; none is Tier 3 as posed, though 5 have a
Tier 3 ceiling. Across all 52 catalogued problems the split is 26 / 21 / 5.

---

## 1. Structural analysis: will the bridge hold, and at what frequency does it ring?

<details>
<summary><b>Start here — the problem in plain terms</b></summary>

A bridge under load bends a little. Every joint shifts, and how far it shifts depends on how hard the
neighbouring members pull back. Each member behaves like a stiff spring: stretch it twice as far and it
pulls back twice as hard. That proportionality is the whole reason this problem is linear.

So write one equation per joint saying "the forces here balance". Each equation involves the movement of
that joint and of the joints connected to it — nowhere else, because a member can only pull on its own
two ends. Collect those equations and you have a system: known forces on one side, unknown movements on
the other, and a big table of spring constants in between. Solve it and you know how the structure
deforms.

The second question engineers ask is what happens with no load at all: let the structure wobble freely
and only certain shapes of wobble sustain themselves, each at its own frequency. Finding those special
shapes is what eigenvalues are for, and it is why bridges are checked against the frequencies of
marching feet and wind.

</details>

**Field:** Civil and mechanical engineering (finite element analysis)

**Tier:** 1 — equilibrium is a plain `Ax = b` solve; rank and conditioning carry the insight. Modal analysis (Tier 2) is an extension.

**Scalars and vectors.** Scalar field: R. Vectors: R^n, n = number of unrestrained degrees of freedom (2 or 3 per node); displacements and forces live in the same space.

**The problem.** Given a structure — truss, bridge deck, turbine blade, engine block — discretized into elements, find the displacement at every node under a given load, and separately find the frequencies at which the structure resonates.

**Formulation.** Assemble a global stiffness matrix `K` from per-element contributions. Static equilibrium is

```
K u = f
```

with `u` nodal displacements and `f` applied forces. Free vibration is the generalized symmetric eigenproblem

```
K φ = λ M φ,     ω = √λ
```

with `M` the mass matrix; eigenvectors `φ` are mode shapes.

**Matrix structure.** `K` is symmetric positive definite (after boundary conditions are applied), extremely sparse — each node couples only to its mesh neighbors — and often banded or block-structured. Industrial models run 10⁶–10⁸ degrees of freedom.

**What is computed.** Sparse Cholesky with fill-reducing reordering (AMD, nested dissection) for the static solve; Lanczos or shift-and-invert Arnoldi for the lowest few dozen eigenpairs. Nobody forms `K⁻¹`.

**Why linear algebra is the right tool.** The underlying PDE (linear elasticity) is linear in the small-strain regime, so superposition holds exactly: the response to a load combination is the combination of responses. Sparsity is a direct encoding of physical locality.

**Pitfall worth teaching.** A near-singular `K` is not a numerical accident — it means the structure has a near-mechanism, a direction in which it can deform with almost no restoring force. The condition number is a physical diagnostic, not just a numerical one.

**Terminology map.** How this field's vocabulary reads as linear algebra.

| Domain term | In linear algebra |
|---|---|
| stiffness matrix | the coefficient matrix K; symmetric positive definite once restraints are applied |
| degree of freedom (DOF) | one scalar unknown — one component of the displacement vector |
| load vector | the right-hand side b |
| restraint / boundary condition | deleting the corresponding rows and columns, or adding constraint rows |
| assembly | summing small element matrices into the global matrix at shared DOF indices |
| mode shape | an eigenvector of K phi = lambda M phi |
| natural frequency | square root of the corresponding eigenvalue |
| mechanism | a nontrivial null space of K — the structure can move with no restoring force |
| bandwidth / skyline | the sparsity pattern induced by node numbering |

**Extensions.** Buckling as a different generalized eigenproblem (`K φ = λ K_geometric φ`); substructuring and domain decomposition; the same modal analysis applied to molecules gives normal-mode analysis and elastic network models.

---

## 2. Kalman filtering: where is the vehicle, given noisy and incomplete measurements?

<details>
<summary><b>Start here — the problem in plain terms</b></summary>

You are trying to work out where a moving vehicle is, and you have two unreliable sources. One is dead
reckoning: start from a known point and add up your measured motion. It is smooth but drifts, because
small errors accumulate. The other is GPS: it does not drift, but each individual reading is noisy and
sometimes missing entirely.

Neither is right. The sensible thing is a compromise, weighted by how much you trust each — and the
trick is that "how much you trust each" is something you can compute rather than guess. If dead
reckoning has been running unchecked for a while, trust it less. If GPS has just given three consistent
readings, trust it more.

A Kalman filter does exactly this, once per time step, forever. What makes it more than a rule of thumb
is that it carries an explicit bookkeeping of its own uncertainty — not one number but a whole table,
because being unsure about north-south position is different from being unsure about speed, and the two
uncertainties interact.

</details>

**Field:** Aerospace, robotics, control engineering

**Tier:** 2 — the covariance recursion needs positive definiteness and observability rank; the static GNSS special case is a Tier 1 on-ramp. Full stochastic treatment is Tier 3.

**Scalars and vectors.** Scalar field: R. Vectors: state in R^n (n = 6-50); measurements in R^m; covariances live in Sym_n, the real vector space of symmetric n x n matrices, dimension n(n+1)/2.

**The problem.** A vehicle carries an inertial measurement unit that drifts, plus a GNSS receiver that is accurate but intermittent and noisy. Produce a continuously updated best estimate of position, velocity, and attitude — with an honest uncertainty attached.

**Formulation.** Linear-Gaussian state-space model:

```
x_{k+1} = F x_k + w_k,    w ~ N(0, Q)      (dynamics)
z_k     = H x_k + v_k,    v ~ N(0, R)      (measurement)
```

The filter propagates a mean and a covariance matrix:

```
P⁻ = F P Fᵀ + Q
K  = P⁻ Hᵀ (H P⁻ Hᵀ + R)⁻¹        (Kalman gain)
P⁺ = (I − K H) P⁻
```

**Matrix structure.** Small and dense (state dimension 6–50 for navigation, thousands for SLAM). `P`, `Q`, `R` are symmetric positive semidefinite. The covariance recursion is a discrete Riccati equation.

**What is computed.** A weighted least-squares update, done recursively so no measurement history is stored. Square-root and UD-factored forms (Potter, Bierman–Thornton) propagate a Cholesky factor of `P` instead of `P` itself to guarantee the covariance stays positive definite in finite precision — this is why Apollo's navigation filter was implemented in square-root form.

**Why linear algebra is the right tool.** The Kalman gain is an orthogonal-projection operator in a metric defined by the noise covariances. "Optimal fusion of uncertain information" turns out to be a projection, which is why the formula is a matrix expression and not a heuristic.

**Pitfall worth teaching.** Rank of the observability matrix `[H; HF; HF²; …]` tells you which state directions the sensors can ever pin down. An unobservable direction shows up as a covariance that grows without bound — the filter tells you honestly that it does not know.

**Terminology map.** How this field's vocabulary reads as linear algebra.

| Domain term | In linear algebra |
|---|---|
| state vector | the unknown x being estimated |
| process noise / measurement noise | the covariance matrices Q and R |
| covariance matrix P | the uncertainty ellipsoid; symmetric positive semidefinite |
| Kalman gain | the projection weight matrix that blends prediction and measurement |
| innovation / residual | z - Hx, the part of the measurement the prediction did not explain |
| observation model H | the linear map from state space to measurement space |
| observability | rank of the stacked matrix [H; HF; HF^2; ...] |
| filter divergence | P losing positive definiteness in finite precision, or an unobservable direction growing without bound |
| square-root filter | propagating a Cholesky factor of P instead of P |

**Extensions.** Static GNSS trilateration as the nonrecursive special case (Gauss–Newton on an overdetermined system); extended and unscented filters for nonlinear dynamics; ensemble Kalman filters for weather data assimilation at 10⁸ state dimensions.

---

## 3. Computed tomography: reconstructing an interior from its shadows

<details>
<summary><b>Start here — the problem in plain terms</b></summary>

Shine an X-ray through a body and it comes out dimmer. How much dimmer tells you the total amount of
dense material it passed through — but not where along the path that material was. One reading is a sum
along a line.

Now take hundreds of thousands of such readings, along lines at every angle. Each one is a different sum
over a different set of points. The question is whether all those sums together pin down the individual
values: can you reconstruct a picture of the interior from a very large collection of line totals?

Mostly yes, and that reconstruction is what a CT scanner computes between the scan finishing and the
image appearing. But "mostly" hides the interesting part. Some patterns of density barely affect any
measurement — they are nearly invisible to every ray — so their reconstructed values are wildly
sensitive to noise. The fix is to add an assumption, usually that real tissue does not vary wildly from
one point to the next, and that assumption is doing real work in the picture a radiologist reads.

</details>

**Field:** Medical imaging (and, with different physics, seismic tomography and electron microscopy)

**Tier:** 2 — ill-posedness is explained through the singular-value spectrum. A small noisy system solved two ways (naive vs regularized) works at Tier 1; the Radon-transform theory is Tier 3.

**Scalars and vectors.** Scalar field: R (nonnegative in practice). Vectors: image in R^N (N voxels); measurements in R^M (M rays); A maps R^N to R^M with M != N.

**The problem.** An X-ray source and detector rotate around a patient. Each measurement is the total attenuation along one line through the body. Recover the 3D attenuation field.

**Formulation.** Discretize the body into voxels `x`; each ray `i` gives

```
∑_j a_ij x_j = b_i,     A x = b
```

where `a_ij` is the length of ray `i` inside voxel `j`. `A` is a discretized Radon transform.

**Matrix structure.** Enormous (10⁶–10⁹ rows and columns), very sparse — a ray touches only O(n^{1/3}) of n voxels — and severely ill-conditioned. Singular values decay smoothly toward zero with no gap, which is the signature of an ill-posed inverse problem.

**What is computed.** Either filtered backprojection (an analytic spectral inverse, fast, the classical approach) or iterative reconstruction: Kaczmarz/ART row-action sweeps, conjugate gradient on the normal equations, or a regularized objective

```
min_x ‖A x − b‖² + λ ‖L x‖²      (Tikhonov)
```

with total-variation penalties now standard in commercial scanners.

**Why linear algebra is the right tool.** Beer–Lambert attenuation is multiplicative in intensity, hence additive in log-intensity — that logarithm is what makes the whole problem linear and the entire field of algebraic reconstruction possible.

**Pitfall worth teaching.** The naive least-squares solution amplifies noise through the small singular values. Regularization is not cosmetic smoothing; it is the choice of which part of the null space and near-null space to fill in, and it is where clinical judgment enters the mathematics. Fewer projection angles means lower dose to the patient but a worse-conditioned `A` — the linear algebra sits directly on a medical trade-off.

**Terminology map.** How this field's vocabulary reads as linear algebra.

| Domain term | In linear algebra |
|---|---|
| projection / ray sum | one row of A applied to x — a line integral through the object |
| sinogram | the measurement vector b, arranged by angle and detector position |
| attenuation coefficient | the unknown x, one value per voxel |
| system matrix / forward projector | A, the discretized Radon transform |
| backprojection | applying A transpose to the data |
| filtered backprojection (FBP) | an analytic spectral inverse of the forward operator |
| ART / SIRT | Kaczmarz row-action and related simultaneous iterations |
| regularization strength | the Tikhonov parameter lambda trading data fit against smoothness |
| streak artifact | the visible signature of undersampling — energy in the near-null space |

**Extensions.** Compressed sensing MRI (sparsity in a transform domain replaces smoothness); cryo-EM reconstruction, which adds unknown orientations; electrical impedance tomography, which is nonlinear.

---

## 4. Stoichiometric matrices: what a reaction network can and cannot do at steady state

<details>
<summary><b>Start here — the problem in plain terms</b></summary>

A living cell runs thousands of chemical reactions at once. Write down a table: one row per chemical,
one column per reaction, and in each cell how many molecules that reaction consumes or produces. That
table is the entire bookkeeping of the cell's chemistry — and notably, it says nothing about how *fast*
anything happens.

Two questions turn out to be answerable from the table alone. First: which combinations of reaction
rates leave every chemical's concentration unchanged? A cell in steady operation must be running one of
these; everything produced is consumed at the same rate. Second: are there quantities that never change
no matter what the rates are? Total phosphate, say, or the total amount of an enzyme across all its
forms — these are conserved by the structure of the chemistry, not by any tuning of the speeds.

This matters because reaction rates are extremely hard to measure and the table is easy to write down.
You get real conclusions from the cheap information.

</details>

**Field:** Chemistry, chemical engineering, systems biology

**Tier:** 1 — null spaces and rank, nothing more. Chemical-equation balancing is the Tier 1 entry point; flux balance analysis is Tier 2.

**Scalars and vectors.** Scalar field: Q or R (S itself has integer entries). Vectors: fluxes in R^r (r reactions); concentrations in R^m (m species); S maps flux space to species space - two different spaces that are easy to conflate.

**The problem.** Given a network of chemical reactions, determine which combinations of reaction rates are compatible with steady state, which quantities are conserved no matter what the kinetics are, and how many reactions are genuinely independent.

**Formulation.** Build the stoichiometric matrix `S` with one row per species and one column per reaction, entries being signed stoichiometric coefficients. Species concentrations evolve as

```
dc/dt = S v
```

with `v` the flux vector. Steady state means `S v = 0`.

**Matrix structure.** Sparse, integer-valued, typically rank-deficient in both directions. Genome-scale metabolic models reach ~2,000 species × ~3,000 reactions.

**What is computed.**
- **Right null space** of `S`: the space of steady-state flux distributions. Its dimension counts the network's degrees of freedom; its nonnegative extreme rays are the elementary flux modes.
- **Left null space** of `S`: conservation laws. A vector `y` with `yᵀS = 0` means `yᵀc` is constant for all time, independent of rate constants — conserved moieties like total ATP+ADP+AMP, or total enzyme.
- **Rank** of `S`: the number of independent reactions, which is what distinguishes an overdetermined mechanism from an underdetermined one.

**Why linear algebra is the right tool.** These conclusions hold without knowing a single rate constant. Structural conclusions from the network topology alone are exactly what null spaces deliver, and kinetic parameters are the hardest thing to measure.

**Pitfall worth teaching.** Balancing a chemical equation is finding an integer vector in the null space of the element–species matrix — the same operation students do by trial and error in first-year chemistry. Showing that equivalence is a good hook.

**Terminology map.** How this field's vocabulary reads as linear algebra.

| Domain term | In linear algebra |
|---|---|
| stoichiometric matrix S | species by reactions, signed integer coefficients |
| flux | v, the vector of reaction rates |
| steady state | Sv = 0 — v lies in the right null space |
| conserved moiety | a left null vector y; y^T c is constant for all time |
| elementary flux mode | an extreme ray of the nonnegative part of the null space |
| degrees of freedom of the network | the nullity of S |
| balancing an equation | finding an integer null vector of the element-by-species matrix |

**Extensions.** Flux balance analysis adds a linear objective and flux bounds, turning the null space into a linear program. Chemical reaction network theory (Feinberg) uses the *deficiency*, a rank-based integer, to predict whether multiple steady states are possible.

---

## 5. Leontief input–output: how much steel does a car actually take?

<details>
<summary><b>Start here — the problem in plain terms</b></summary>

Building a car takes steel. Making steel takes electricity. Generating electricity takes steel. The
requirements are circular, so you cannot just add them up — following the chain never terminates.

Suppose you want one more car delivered to a customer. You need some steel for it directly. But you also
need extra electricity to make that steel, and extra steel to make that electricity, and so on forever.
Each round is smaller than the last, so the total is finite; the question is what it adds up to.

Economists answer this by writing one equation per industry: total output equals what other industries
consume from it, plus what consumers finally take. Solving the system gives every industry's required
output at once, with the infinite chain of indirect requirements already accounted for.

The same computation, with pollution added as an extra row, is how the carbon footprint of a product is
usually estimated — including all the emissions from its suppliers' suppliers.

</details>

**Field:** Economics (and, in its modern form, environmental footprint accounting)

**Tier:** 1 — posing and solving `(I − A)x = d` needs only a linear solve. The Perron–Frobenius convergence condition lifts it to Tier 2.

**Scalars and vectors.** Scalar field: R (nonnegative). Vectors: outputs and demands in R^n, n = number of sectors.

**The problem.** Industries consume each other's output. Making a car needs steel; making steel needs electricity; making electricity needs steel. Given final consumer demand, find the total production every sector must run.

**Formulation.** Let `A` be the technical-coefficient matrix, where `a_ij` is the input from sector `i` needed per unit of sector `j` output. Total output `x` satisfies

```
x = A x + d      ⟹      (I − A) x = d
```

**Matrix structure.** Square, entrywise nonnegative, dense-ish, with column sums below 1 for a productive economy. National tables run 400–500 sectors; the global multi-region tables (EXIOBASE, WIOD) reach tens of thousands.

**What is computed.** `(I − A)⁻¹`, the Leontief inverse, is the object of interest itself — entry `(i,j)` is the total output of `i` required per unit of final demand for `j`, summed over all supply-chain depths. The Neumann series

```
(I − A)⁻¹ = I + A + A² + A³ + …
```

has a direct reading: direct requirements, then requirements of requirements, and so on.

**Why linear algebra is the right tool.** The circularity that makes the accounting hard by hand — steel needs electricity needs steel — is precisely what a matrix inverse resolves in closed form.

**Pitfall worth teaching.** By Perron–Frobenius, the series converges exactly when the spectral radius of `A` is below 1. That is not a technical condition: it is the statement that the economy produces more than it consumes in production. A nonnegative matrix's dominant eigenvalue carries economic meaning.

**Terminology map.** How this field's vocabulary reads as linear algebra.

| Domain term | In linear algebra |
|---|---|
| technical coefficient matrix A | input from sector i per unit output of sector j |
| final demand | the right-hand side d |
| gross / total output | the unknown x |
| Leontief inverse | (I - A)^-1 |
| multiplier | a single entry of the Leontief inverse |
| productive economy | spectral radius of A below 1, so the Neumann series converges |
| direct vs indirect requirements | the successive terms A, A^2, A^3 of the Neumann series |
| embodied / Scope 3 emissions | an appended satellite row multiplied through the same inverse |

**Extensions.** Environmentally-extended I/O appends rows for CO₂, water, and land use, and the same inverse yields the full upstream carbon footprint of a product — this is how most corporate Scope 3 emissions are estimated. Same mathematics: Markov chain fundamental matrices, and structural path analysis.

---

## 6. PageRank: ranking by the structure of a network

<details>
<summary><b>Start here — the problem in plain terms</b></summary>

How do you rank web pages by importance when importance is circular? A page matters if important pages
link to it — but that definition refers to itself.

Picture someone clicking links at random forever. From whatever page they are on, they pick an outgoing
link at random and follow it. Occasionally, out of boredom, they jump to a completely random page
instead. Over a very long time, what fraction of their clicks land on each page?

That fraction is the ranking. Pages with many incoming links get visited often; pages linked from
frequently-visited pages get visited often too, which is exactly the circular definition, now made
precise as a statement about long-run behaviour.

The computation is remarkably simple: guess a distribution, push it through one round of clicking, and
repeat. It converges quickly, and the boredom-jump is not a detail — without it the process can get
permanently stuck in a corner of the web, and the whole thing falls apart.

</details>

**Field:** Computer science, network science

**Tier:** 2 — a dominant-eigenvector problem by construction.

**Scalars and vectors.** Scalar field: R. Vectors: R^n over pages, but the solution is constrained to the probability simplex (nonnegative, entries summing to 1), which is NOT a subspace.

**The problem.** Order the pages of the web (or papers in a citation graph, or proteins in an interaction network) by importance, where importance is recursive: a page is important if important pages link to it.

**Formulation.** Let `P` be the column-stochastic link matrix. PageRank is the stationary distribution

```
r = α P r + (1 − α)/n · 1,      equivalently     G r = r
```

with `G = α P + (1 − α)/n · 11ᵀ` the Google matrix and `α ≈ 0.85`.

**Matrix structure.** `P` is sparse (average out-degree in the tens) and stochastic; `G` is dense but never formed — the damping term is a rank-one update applied on the fly, so each matrix–vector product still costs O(nnz).

**What is computed.** Power iteration. Convergence rate is governed by `|λ₂/λ₁| ≤ α`, so the damping factor directly sets the iteration count: roughly 50–100 iterations at α = 0.85 regardless of graph size.

**Why linear algebra is the right tool.** The circular definition of importance is a fixed-point equation, and Perron–Frobenius guarantees for an irreducible aperiodic nonnegative matrix that the fixed point exists, is unique, and is positive. The damping factor is what buys irreducibility — a modeling choice made to secure a theorem.

**Pitfall worth teaching.** Dangling nodes (no outlinks) break stochasticity, and the standard patch — treating them as linking to everything — is a modeling decision with real effects on the ranking. Every "algorithm detail" here is a mathematical requirement in disguise.

**Terminology map.** How this field's vocabulary reads as linear algebra.

| Domain term | In linear algebra |
|---|---|
| link matrix | the column-stochastic matrix P built from the graph |
| dangling node | a zero column, which breaks stochasticity |
| damping factor (alpha) | the weight on P versus the uniform teleportation term |
| teleportation | the rank-one correction that makes the chain irreducible |
| stationary distribution | the dominant eigenvector, normalized |
| power iteration | repeated multiplication by the matrix |
| centrality | a score defined as an eigenvector, or a function, of the graph matrix |

**Extensions.** Leslie matrices in population ecology (same dominant-eigenvector structure, eigenvalue = population growth rate); the next-generation matrix in epidemiology, whose spectral radius *is* R₀; Katz centrality and hub/authority (HITS) scores; personalized PageRank as a graph kernel in ML.

---

## 7. Error-correcting codes: linear algebra over a finite field

<details>
<summary><b>Start here — the problem in plain terms</b></summary>

You want to send a string of bits over a connection that occasionally flips one. Repeating everything
three times would work, but it triples what you send.

Here is a better idea. Alongside your data bits, send some extra bits, each one computed as the parity
(the even-or-odd count) of a chosen subset of the data bits. The receiver recomputes those parities from
what it received. If everything matches, no error. If some of them disagree, the exact *pattern* of
disagreement identifies which bit flipped — different bit positions participate in different subsets, so
each one produces its own distinctive signature of failures.

The design problem is choosing the subsets so that every possible single error produces a unique
signature. That is a question about independence: no two error patterns may look alike.

One thing to adjust up front. The arithmetic here is not ordinary addition — it is parity, where
1 + 1 = 0. Everything about subspaces and independence still works, but nothing about lengths or angles
does.

</details>

**Field:** Communications, information theory, storage systems

**Tier:** 1 — rank and null space over GF(2), using the finite-field material this collection wants at Tier 1. Reed–Solomon over GF(2^m) is Tier 3.

**Scalars and vectors.** Scalar field: GF(2) = {0,1} with XOR as addition; GF(2^m) for Reed-Solomon. Vectors: GF(2)^n; the code is a k-dimensional subspace of it. There is no Euclidean length here - Hamming weight is a metric, not a norm from an inner product.

**The problem.** Send bits over a channel that flips some of them. Detect and correct the errors without retransmission.

**Formulation.** Work over the field GF(2), where arithmetic is XOR. A linear `[n, k]` code is a `k`-dimensional subspace of GF(2)ⁿ. Encoding is

```
c = G m        (G: k × n generator matrix)
```

Every valid codeword lies in the null space of the parity-check matrix `H`:

```
H cᵀ = 0
```

A received word `y = c + e` gives the syndrome

```
s = H yᵀ = H eᵀ
```

which depends only on the error pattern, not on the message.

**Matrix structure.** Entries in GF(2); LDPC codes use very sparse `H`; Reed–Solomon works over GF(2^m) with a Vandermonde-structured generator.

**What is computed.** Syndrome decoding: look up or infer the minimum-weight `e` consistent with `s`. For LDPC codes, belief propagation on the bipartite graph of `H`. For Reed–Solomon, polynomial interpolation, which is a structured linear solve.

**Why linear algebra is the right tool.** Distance properties — the whole point of a code — become rank conditions. A code corrects `t` errors if and only if every `2t` columns of `H` are linearly independent. Searching an exponentially large space of codewords collapses to a statement about column ranks.

**Pitfall worth teaching.** This is where the abstraction of "field" earns its keep. Everything from linear algebra (rank, null space, dimension, bases) carries over unchanged; everything from geometry (angles, lengths, positive-definiteness, least squares) does not. A good exercise in what the axioms actually buy.

**Terminology map.** How this field's vocabulary reads as linear algebra.

| Domain term | In linear algebra |
|---|---|
| codeword | an element of the k-dimensional subspace of GF(2)^n |
| generator matrix G | a basis of the code, written as rows |
| parity-check matrix H | a basis of the code's orthogonal complement; codewords are its null space |
| syndrome | H y^T — depends only on the error, not the message |
| minimum distance | the smallest weight of a nonzero codeword |
| systematic form | G = [I \| P], so the message appears verbatim in the codeword |
| code rate | k/n, the subspace dimension over the ambient dimension |
| erasure vs error | known vs unknown error position — a column selection vs a search |

**Extensions.** Reed–Solomon in QR codes, CDs, and RAID-6; LDPC in 5G and Wi-Fi 6; polar codes in 5G control channels. Separately, the same GF(2) linear algebra at massive scale — sparse nullspace via block Lanczos or Wiedemann — is the final stage of the number field sieve used to factor RSA moduli.

---

## 8. Multiple-view geometry: 3D structure from 2D images

<details>
<summary><b>Start here — the problem in plain terms</b></summary>

Take two photos of the same building from different positions. A human can see they show the same
structure, and can roughly tell how the photographer moved between them. Getting a computer to do this
is the foundation of drone mapping, phone panoramas, and robot navigation.

Start with what is recoverable: matching points. Find a window corner visible in both photos. You do not
know where it is in 3D, and you do not know how the camera moved — but the two are linked. If you
hypothesise a camera motion, then a point in the first image is restricted to a single line in the
second. Each matched pair therefore constrains the possible motions, and with enough pairs only one
motion survives.

The awkward part is perspective: objects twice as far away appear half as large, which is division, not
a linear operation. The standard fix is to add one extra coordinate to every point and do the division
only at the very end. With that trick the entire camera pipeline becomes matrix multiplication, which is
why graphics hardware is built the way it is.

</details>

**Field:** Computer vision, photogrammetry, robotics

**Tier:** 2 — the SVD does the work. The 2D homography and the transformation pipeline behind it sit at Tier 1; pose refinement on SE(3) is Tier 3.

**Scalars and vectors.** Scalar field: R. Vectors: scene points in R^3, written in homogeneous R^4 up to scale (projective space P^3); image points in R^2 as homogeneous R^3 up to scale (P^2). The unknown essential matrix is vectorized to R^9 and recovered only up to scale, so it is really a point of P^8.

**The problem.** Given photographs of a scene from unknown viewpoints, recover both the camera positions and the 3D geometry. This is the engine behind phone panorama stitching, drone mapping, visual SLAM, and photogrammetric reconstruction.

**Formulation.** Homogeneous coordinates turn the nonlinear perspective projection into a linear map:

```
λ [u, v, 1]ᵀ = K [R | t] [X, Y, Z, 1]ᵀ
```

Two views of the same rigid scene are related by the essential matrix `E` through the epipolar constraint

```
x'ᵀ E x = 0
```

Stacking that constraint over ≥8 point correspondences gives a homogeneous system `A e = 0`; the solution is the right singular vector of `A` with the smallest singular value.

**Matrix structure.** `A` is small and dense (n × 9). The later bundle-adjustment stage produces a large, sparse, highly structured Jacobian with the characteristic "arrowhead" block pattern from cameras and points.

**What is computed.** SVD, twice and for two different reasons: once to solve the homogeneous least-squares problem (smallest singular vector), and once to project the estimate onto the manifold of valid essential matrices by zeroing the third singular value and equalizing the first two. Bundle adjustment then refines everything by sparse Levenberg–Marquardt with the Schur complement trick to eliminate the 3D points.

**Why linear algebra is the right tool.** Projective geometry in homogeneous coordinates is the reason: a genuinely nonlinear operation (perspective division) becomes a linear map followed by a normalization. Adding one coordinate buys linearity.

**Pitfall worth teaching.** Conditioning matters more than the algorithm here. Hartley's normalized 8-point algorithm — translate and scale the image points before forming `A` — is the difference between usable and useless results, and the only change is a preconditioning of the input. It is one of the cleanest real demonstrations that condition number is not an academic concern.

**Terminology map.** How this field's vocabulary reads as linear algebra.

| Domain term | In linear algebra |
|---|---|
| homogeneous coordinates | an added coordinate that turns perspective division into a linear map plus a normalization |
| intrinsic matrix K | the camera's internal calibration, an upper-triangular 3x3 |
| extrinsic parameters [R\|t] | the rigid transform from world to camera frame |
| essential / fundamental matrix | the rank-2 bilinear form satisfying x'^T E x = 0 |
| epipolar constraint | the bilinear equation relating corresponding points in two views |
| DLT (direct linear transform) | stacking constraints into A and taking the smallest right singular vector |
| reprojection error | the nonlinear least-squares objective minimized in refinement |
| bundle adjustment | sparse nonlinear least squares over all cameras and points at once |
| degenerate configuration | point placement that makes A rank-deficient, so the solution is not unique |

**Extensions.** Homography estimation and image stitching; the PnP problem; the Perron-like structure in rotation averaging; SE(3) and Lie-group optimization for pose graphs.

---

## 9. Empirical orthogonal functions: finding the dominant patterns in climate data

<details>
<summary><b>Start here — the problem in plain terms</b></summary>

Here is a century of monthly sea-surface temperature maps: tens of thousands of grid points, over a
thousand time steps. Far too much to look at directly, and most of it is redundant — neighbouring points
in the ocean do not behave independently.

What a climatologist wants is the handful of recurring patterns that account for most of the variation.
El Nino is one: a specific spatial signature of warm and cool regions that strengthens and weakens over
time. If you can identify a few such patterns, each with a single time series saying how strongly it is
present each month, you have compressed the whole dataset into something you can reason about.

That decomposition is what the SVD provides, and it comes with a guarantee: no other set of that many
patterns reconstructs the data more accurately.

The caveat is worth absorbing early. The method forces the patterns to be mutually perpendicular, and
nature is under no obligation to comply. A pattern that is optimal mathematically can still be a blend
of two unrelated physical processes.

</details>

**Field:** Atmospheric and ocean science, climatology

**Tier:** 2 — truncated SVD and the Eckart–Young optimality statement.

**Scalars and vectors.** Scalar field: R. Vectors: each time slice is a spatial field in R^s (s grid points); EOFs live in R^s and principal-component series in R^t (t time steps).

**The problem.** A century of monthly sea-surface temperatures on a global grid is a matrix with 10⁴–10⁵ spatial points and 10³ time steps. Extract the few spatial patterns that account for most of the variability — the objects a climatologist can actually reason about, like El Niño.

**Formulation.** Center the data matrix `X` (space × time) and take the SVD:

```
X = U Σ Vᵀ
```

Columns of `U` are the empirical orthogonal functions (spatial patterns), rows of `Vᵀ` are their principal-component time series, and `σᵢ²` is the variance each pattern explains.

**Matrix structure.** Tall or wide but dense; the effective rank is low — typically 5–10 modes capture most of the variance, which is why the technique works at all.

**What is computed.** Truncated SVD (randomized SVD or Lanczos bidiagonalization for large grids). The Eckart–Young theorem guarantees that the rank-k truncation is the best possible rank-k approximation in both the Frobenius and spectral norms — an optimality statement, not a heuristic.

**Why linear algebra is the right tool.** The field is spatially correlated: neighboring grid points are far from independent. Low-rank structure is a mathematical restatement of physical coherence, and the SVD finds it without being told any physics.

**Pitfall worth teaching.** EOFs are constrained to be orthogonal, and physical modes are generally not. A leading EOF can be a mathematical mixture of two distinct physical mechanisms, and a second EOF can be an artifact of orthogonality to the first (North's rule of thumb gives a degeneracy test). This is the best example in the collection of a decomposition whose mathematical optimality does not imply physical interpretability — worth teaching alongside the same caution for PCA in genomics.

**Terminology map.** How this field's vocabulary reads as linear algebra.

| Domain term | In linear algebra |
|---|---|
| EOF | a left singular vector — one spatial pattern |
| principal component time series | the corresponding right singular vector, scaled |
| explained variance | sigma_i^2 as a fraction of the total |
| loading | one entry of an EOF, i.e. one grid point's weight in that pattern |
| anomaly field | the mean-centered data matrix |
| rotated EOF (varimax) | a deliberately non-orthogonal re-basis of the leading subspace |
| North's rule of thumb | a test for whether two singular values are too close to separate the modes |

**Extensions.** Proper orthogonal decomposition and reduced-order models in fluid dynamics; dynamic mode decomposition, which extracts an approximate linear operator (Koopman) rather than just a basis; the same SVD machinery in latent semantic analysis, recommender systems, and matrix completion.

---

## 10. Quantum mechanics and quantum computing: when the vector space *is* the physics

<details>
<summary><b>Start here — the problem in plain terms</b></summary>

In quantum mechanics a system's state is not a position and a velocity — it is a list of complex
numbers, one for each configuration the system could be found in. Their sizes determine the
probabilities of each outcome. This is not an approximation or a modelling convenience; the theory is
stated this way.

Two consequences follow immediately. First, adding two valid states gives another valid state — this is
superposition, and it is just the statement that states form a vector space. Second, every measurable
quantity (energy, momentum, spin) corresponds to a matrix, and the values you can actually observe are
that matrix's eigenvalues. Asking "what energies can this molecule have?" is literally asking for the
eigenvalues of a particular matrix.

The difficulty is size. Combining two systems multiplies their dimensions rather than adding them, so
n quantum bits need a vector with 2^n entries — past about fifty, larger than any computer's memory.
Much of modern quantum chemistry and quantum computing is about exploiting the fact that the states
that actually occur in nature occupy a very thin slice of that enormous space.

</details>

**Field:** Physics, quantum chemistry, quantum information

**Tier:** 2 — as posed (benzene's 6×6 Hückel eigenproblem). The full quantum formalism is Tier 3.

**Scalars and vectors.** Scalar field: C (real symmetric in the Huckel special case). Vectors: unit vectors in C^d; for n qubits d = 2^n and the space is the tensor product (C^2)^(x)n. Global phase is unphysical, so states are really points of CP^(d-1). Observables are Hermitian matrices, which form a REAL vector space of dimension d^2.

**The problem.** Two versions. (a) Compute the energy levels and spectra of a molecule. (b) Simulate or design a quantum circuit.

**Formulation.** A state is a unit vector in a complex Hilbert space. Observables are Hermitian operators; measurable values are their eigenvalues. The time-independent Schrödinger equation is an eigenproblem

```
H ψ = E ψ
```

Quantum gates are unitary matrices, and composite systems combine by tensor product, so `n` qubits live in `C^{2ⁿ}`.

**Matrix structure.** Hermitian (hence real eigenvalues, orthogonal eigenvectors) and, in a local basis, sparse — Hamiltonians typically couple only nearby sites or orbitals. The dimension is the problem: it grows exponentially in system size.

**What is computed.** Lanczos and Davidson methods for the lowest few eigenpairs of matrices too large to store; self-consistent field iteration (Hartree–Fock, DFT) as a nonlinear eigenproblem solved by repeated dense diagonalization; quantum circuit simulation as a sequence of sparse structured matrix–vector products.

**Why linear algebra is the right tool.** It is not a modeling convenience here — the superposition principle *is* linearity, and the postulates of quantum mechanics are stated directly in terms of Hilbert spaces, Hermitian operators, and unitary evolution. This is the entry where the mathematics is not applied to the physics but constitutive of it.

**Pitfall worth teaching.** The tensor-product structure means the state space grows as 2ⁿ, which makes exact methods hopeless past ~50 qubits. The response is again low-rank structure: matrix product states and tensor networks exploit the fact that physically relevant states occupy a very thin, low-entanglement slice of the full space. Low-rank approximation appears here for the same reason it appears in entry 9, in a completely different setting.

**Terminology map.** How this field's vocabulary reads as linear algebra.

| Domain term | In linear algebra |
|---|---|
| ket / state vector | a unit vector in a complex inner-product space |
| observable | a Hermitian operator; its eigenvalues are the measurable values |
| expectation value | the quadratic form psi^* A psi |
| eigenstate / energy level | eigenvector and eigenvalue of the Hamiltonian |
| Hamiltonian | the Hermitian matrix H in H psi = E psi |
| unitary gate | a norm-preserving complex linear map — the complex analogue of an orthogonal matrix |
| tensor product | the Kronecker product; why n qubits need dimension 2^n |
| entangled state | a vector that does not factor as a tensor product |
| basis set (quantum chemistry) | the chosen basis in which H is expressed |
| SCF iteration | fixed-point iteration on an eigenproblem whose matrix depends on its own solution |
| density matrix | a positive semidefinite matrix with trace 1 |

**Extensions.** Hückel molecular orbital theory, where the Hamiltonian is literally the adjacency matrix of the molecular graph and orbital energies are its eigenvalues — the cleanest bridge between graph theory and chemistry. Also: density matrices as positive semidefinite operators, quantum channels as completely positive maps, and variational quantum eigensolvers.

---

# Coverage of the seed set

| # | Field | Core linear-algebra object | Dominant method |
|---|-------|---------------------------|-----------------|
| 1 | Civil / mechanical engineering | Sparse SPD system; generalized eigenproblem | Sparse Cholesky; Lanczos |
| 2 | Aerospace / control | Covariance projection; Riccati recursion | Recursive weighted least squares |
| 3 | Medical imaging | Ill-posed sparse system | Regularized iterative solve; Kaczmarz |
| 4 | Chemistry / systems biology | Null space (both sides); rank | Nullspace basis; rational arithmetic |
| 5 | Economics | Nonnegative matrix; spectral radius | Matrix inverse; Neumann series |
| 6 | Computer science / networks | Stochastic matrix; dominant eigenvector | Power iteration |
| 7 | Communications | Subspace over GF(2); rank conditions | Syndrome decoding; belief propagation |
| 8 | Computer vision | Homogeneous least squares; rank truncation | SVD; sparse Levenberg–Marquardt |
| 9 | Climate science | Low-rank approximation | Truncated / randomized SVD |
| 10 | Physics / quantum chemistry | Hermitian eigenproblem; tensor products | Lanczos, Davidson; SCF |

**Concepts deliberately covered across the set:** solving `Ax = b` (sparse, dense, ill-posed, over a finite field), least squares (batch and recursive), eigenvalue problems (standard, generalized, dominant-only), the SVD (as optimal approximation, as homogeneous solver, as manifold projection), null spaces and rank, nonnegative matrices and Perron–Frobenius, stochastic matrices, projections, conditioning and preconditioning, tensor products, and linear algebra over a field other than ℝ.

**Not yet represented:** graph Laplacians and spectral methods, Krylov subspace methods on their own terms, optimization duality and linear programming, tensor decompositions beyond the matrix case, randomized numerical linear algebra, and anything from pure mathematics.

---

# Backlog — candidates for expansion

Grouped by what they would add that the seed set does not have.

### Would add: Tier 1 coverage — 2D/3D graphics and scalars beyond the reals

This group exists because the seed set is thin at Tier 1 and silent on vector spaces whose scalars are
not real numbers. Every entry here is small-dimension and needs nothing past a first course.

*Graphics and small-dimension geometry (index 36–40)*
- **2D affine transforms in vector graphics** — the SVG/CSS/Canvas transform stack; composition order as a
  concrete demonstration that matrix multiplication does not commute
- **3D viewing and perspective projection** — the model-view-projection chain; why the fourth coordinate exists
- **3D rotations and rigid-body pose** — orthogonal matrices with determinant +1; gimbal lock as a
  basis-composition failure, which motivates quaternions without needing them
- **Barycentric coordinates and triangle rasterization** — a 3×3 solve per pixel; coordinates relative to a basis
- **Color spaces as change of basis** — sRGB ↔ XYZ ↔ LMS as 3×3 basis changes; gamut as a convex cone

*Polynomial and function spaces (index 41–45)*
- **Polynomial interpolation and change of basis** — Vandermonde systems; monomial vs Lagrange vs Chebyshev
  bases, and the conditioning consequences of the choice
- **Bézier curves and font rendering** — the Bernstein basis; every glyph on this page is an element of a
  4-dimensional polynomial space
- **Finite-difference stencils by undetermined coefficients** — derivative weights as the solution of a small
  linear system; differentiation as a linear operator
- **Fourier series as orthogonal projection** — an inner-product space of functions; best approximation
- **Least-squares fitting in a chosen function basis** — the design matrix as a basis choice made explicit

*Complex scalars (index 46–47)*
- **AC circuit analysis with complex impedance** — a 3×3 complex linear system; phasors make a differential
  equation into an algebraic one
- **The small DFT as a complex unitary matrix** — the 8-point transform written out; complex inner products

*Finite fields (index 48–50)*
- **Shamir secret sharing** — Lagrange interpolation over GF(p); the threshold property *is* a uniqueness
  theorem about interpolation
- **RAID-5 parity and XOR recovery** — one linear equation over GF(2), running in every storage array
- **CRC checksums** — polynomials over GF(2) modulo a generator

*Underdetermined systems with free variables (index 51–52)*
- **Traffic flow conservation at intersections** — particular plus homogeneous solution, with nonnegativity
  giving the physically admissible set
- **Mass balance in a process flowsheet** — recycle loops as coupling between equations

### Would add: graph Laplacians and spectral methods
- **Spectral clustering and image segmentation** — Fiedler vector, normalized cuts, Cheeger inequality
- **Resistor networks and Kirchhoff's laws** — the Laplacian as a physical object; effective resistance and commute times
- **Laplacian eigenmaps and diffusion maps** — nonlinear dimensionality reduction with a linear core
- **Consensus and opinion dynamics (DeGroot models)** — convergence rate set by the algebraic connectivity

### Would add: large-scale iterative methods as the subject
- **Poisson/Navier–Stokes discretization** — finite differences or finite volumes, conjugate gradient, multigrid, preconditioner design
- **Circuit simulation (SPICE)** — modified nodal analysis, sparse LU with pivoting under structural constraints
- **Power-grid load flow and state estimation** — sparse Newton with a Jacobian that changes structure under contingency; Sherman–Morrison for N−1 analysis

### Would add: optimization and duality
- **Linear programming and the simplex method** — basis exchange as a sequence of rank-one updates; totally unimodular matrices giving integral solutions for free in network flow
- **Portfolio optimization (Markowitz)** — covariance matrices, shrinkage estimation, the ill-conditioning that makes the textbook version unusable
- **Support vector machines / kernel methods** — Gram matrices, positive definiteness, the representer theorem

### Would add: signal processing
- **The FFT as a matrix factorization** — the DFT matrix factored into sparse blocks; why O(n log n) is a statement about structure
- **Beamforming and MUSIC direction-finding** — signal and noise subspaces of a spatial covariance matrix; radar, sonar, and 5G MIMO
- **JPEG and video compression** — the DCT as a fixed orthogonal basis chosen for decorrelation

### Would add: statistics and machine learning proper
- **Least squares regression and the hat matrix** — QR vs normal equations, leverage, collinearity diagnostics
- **Matrix completion and recommender systems** — nuclear-norm minimization, the Netflix Prize
- **Word embeddings and latent semantic analysis** — factorization of a co-occurrence matrix
- **Attention in transformers** — QKᵀ as a learned bilinear form; low-rank adapters (LoRA) as explicit rank constraints on weight updates

### Would add: geosciences and geometry
- **Geodetic network adjustment** — the historical origin of least squares; rank deficiency from datum choice, resolved by constraints
- **Seismic tomography** — same inverse-problem structure as entry 3 with far worse ray coverage
- **Distance geometry (NMR structure determination)** — Cayley–Menger determinants, classical multidimensional scaling, low-rank Gram matrix recovery
- **X-ray crystallography** — the phase problem; Patterson maps; structure factors as Fourier coefficients

### Would add: discrete and algebraic applications
- **Markov decision processes** — policy evaluation as a linear solve, value iteration as a fixed point
- **Sports and citation ranking (Massey / Colley)** — a least-squares system built from pairwise comparisons
- **Cryptanalysis: sparse GF(2) nullspace in the number field sieve** — block Lanczos/Wiedemann at 10⁸ scale
- **Combinatorial design and coding bounds** — rank arguments proving combinatorial impossibility results

### Would add: molecular and biological (matched to your background)
- **Normal mode analysis and elastic network models** — the Hessian of a coarse-grained potential; low-frequency modes predicting functional motions
- **Flux balance analysis at genome scale** — the LP built on entry 4's null space
- **Population genetics PCA** — the same SVD as entry 9, with the same interpretability caveat and a well-documented history of overreading the modes
- **Phylogenetic invariants** — polynomial relations among expected site-pattern frequencies; linear algebra that shades into algebraic geometry

---

# Suggested next steps

1. **Add a runnable notebook per entry.** Each of these can be posed at a size that runs in seconds and still shows the real phenomenon — a 12-bar truss, a 32×32 tomographic phantom, a 10-sector I/O table, a Hamming(7,4) code. The pedagogical payload is usually in the failure mode (ill-conditioning, rank deficiency, slow convergence), which small examples show faithfully.
2. ~~Standardize a difficulty tier per entry.~~ **Decided:** the three-tier scheme above, recorded per
   entry in the `tier`, `tier_ceiling`, and `prereq_beyond_la` columns of the index. Remaining work is to
   promote a Tier 1 entry into the seed set — the seed set currently reads as a Tier 2 collection with
   four Tier 1 entries, which is the wrong first impression for a general audience.
3. ~~Decide whether the organizing axis is field or concept.~~ **Decided: field**, for the reasons in
   "Audience and organizing principle" above. The concept coverage table remains as the secondary
   cross-reference. Remaining work: extend the terminology map beyond the ten seed entries — it
   currently covers 84 terms across those ten only, and the backlog entries most likely to generate
   domain-specific questions (power systems, portfolio optimization, seismic tomography, MDPs) have no
   terminology coverage yet.
