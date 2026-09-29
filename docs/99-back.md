
# Coverage of the seed set

{{COVERAGE_TABLE}}

**Concepts deliberately covered across the set:** solving `Ax = b` (sparse, dense, ill-posed, over a finite field), least squares (batch and recursive), eigenvalue problems (standard, generalized, dominant-only), the SVD (as optimal approximation, as homogeneous solver, as manifold projection), null spaces and rank, nonnegative matrices and Perron–Frobenius, stochastic matrices, projections, conditioning and preconditioning, tensor products, and linear algebra over a field other than ℝ.

**Not yet represented:** graph Laplacians and spectral methods, Krylov subspace methods on their own terms, optimization duality and linear programming, tensor decompositions beyond the matrix case, randomized numerical linear algebra, and anything from pure mathematics.

---

# Backlog — candidates for expansion

Grouped by what they would add that the seed set does not have.

### Would add: Tier 1 coverage — 2D/3D graphics and scalars beyond the reals

This group exists because the seed set is thin at Tier 1 and silent on vector spaces whose scalars are
not real numbers. Every entry here is small-dimension and needs nothing past a first course, with
the one exception marked below.

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
  equation into an algebraic one. *Tier 3, not Tier 1:* the phasor method is a technique for solving
  linear ODEs with sinusoidal forcing, so reading the entry requires the ODE. It stays in this group
  because it is the clearest example of complex scalars doing real work; the small DFT below is the
  Tier 1 complex-scalar entry.
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
  (Tier 2 in its discrete-time DeGroot form, a difference equation; the continuous-time version,
  dx/dt = −L x, is an ODE and would be Tier 3)

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
   promote Tier 1 entries into the seed set. Under the rule that any differential equation means Tier 3,
   only {{N_SEED_TIER1}} of the {{N_SEED}} seed entries are Tier 1, which is the wrong first impression for a
   general audience. The Tier 1 backlog group above is the natural source.
3. ~~Decide whether the organizing axis is field or concept.~~ **Decided: field**, for the reasons in
   "Audience and organizing principle" above. The concept coverage table remains as the secondary
   cross-reference. Remaining work: extend the terminology map beyond the ten seed entries — it
   currently covers {{N_TERMS}} terms across those ten only, and the backlog entries most likely to generate
   domain-specific questions (power systems, portfolio optimization, seismic tomography, MDPs) have no
   terminology coverage yet.
