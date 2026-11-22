
# Coverage of the written entries

{{COVERAGE_TABLE}}

**Concepts deliberately covered across the set:** solving `Ax = b` (sparse, dense, ill-posed, over a finite field), least squares (batch and recursive), eigenvalue problems (standard, generalized, dominant-only), the SVD (as optimal approximation, as homogeneous solver, as manifold projection), null spaces and rank, nonnegative matrices and Perron–Frobenius, stochastic matrices, projections, conditioning and preconditioning, tensor products, and linear algebra over a field other than ℝ.

**Not yet represented:** Krylov subspace methods on their own terms, optimization duality, tensor decompositions beyond the matrix case, randomized numerical linear algebra, and anything from pure mathematics.

---

# Backlog — candidates for expansion

Grouped by what they would add that the seed set does not have.

### Would add: Tier 1 coverage — scalars beyond the reals

This group exists because the seed set is thin at Tier 1 and silent on vector spaces whose scalars are
not real numbers. Every entry here is small-dimension and needs nothing past a first course, with
the one exception marked below.

*Complex scalars (index 46–47)*
- **AC circuit analysis with complex impedance** — a 3×3 complex linear system; phasors make a differential
  equation into an algebraic one. *Tier 3, not Tier 1:* the phasor method is a technique for solving
  linear ODEs with sinusoidal forcing, so reading the entry requires the ODE. It stays in this group
  because it is the clearest example of complex scalars doing real work; the small DFT entry, now
  written, is the Tier 1 complex-scalar entry.

### Would add: graph Laplacians and spectral methods
- **Laplacian eigenmaps and diffusion maps** — nonlinear dimensionality reduction with a linear core

### Would add: large-scale iterative methods as the subject
- **Poisson/Navier–Stokes discretization** — finite differences or finite volumes, conjugate gradient, multigrid, preconditioner design
- **Circuit simulation (SPICE)** — modified nodal analysis, sparse LU with pivoting under structural constraints
- **Power-grid load flow and state estimation** — sparse Newton with a Jacobian that changes structure under contingency; Sherman–Morrison for N−1 analysis

### Would add: optimization and duality
- **Support vector machines / kernel methods** — Gram matrices, positive definiteness, the representer theorem

### Would add: statistics and machine learning proper
- **Matrix completion and recommender systems** — nuclear-norm minimization, the Netflix Prize

### Would add: geosciences and geometry
- **Seismic tomography** — same inverse-problem structure as entry 3 with far worse ray coverage
- **X-ray crystallography** — the phase problem; Patterson maps; structure factors as Fourier coefficients

### Would add: discrete and algebraic applications
- **Cryptanalysis: sparse GF(2) nullspace in the number field sieve** — block Lanczos/Wiedemann at 10⁸ scale
- **Combinatorial design and coding bounds** — rank arguments proving combinatorial impossibility results

### Would add: molecular and biological (matched to your background)
- **Phylogenetic invariants** — polynomial relations among expected site-pattern frequencies; linear algebra that shades into algebraic geometry

---

# Suggested next steps

1. **Add a runnable notebook per entry.** Each of these can be posed at a size that runs in seconds and still shows the real phenomenon — a 12-bar truss, a 32×32 tomographic phantom, a 10-sector I/O table, a Hamming(7,4) code. The pedagogical payload is usually in the failure mode (ill-conditioning, rank deficiency, slow convergence), which small examples show faithfully.
2. ~~Standardize a difficulty tier per entry.~~ **Decided:** the three-tier scheme above, recorded per
   entry in the `tier`, `tier_ceiling`, and `prereq_beyond_la` columns of the index. Under the rule that
   any differential equation means Tier 3, only {{N_SEED_TIER1}} of the {{N_SEED}} seed entries are Tier 1,
   which is the wrong first impression for a general audience. Remaining work is to write up the Tier 1
   backlog, which is under way: {{N_ENTRIES_TIER1}} of the {{N_ENTRIES}} written entries are now Tier 1.
3. ~~Decide whether the organizing axis is field or concept.~~ **Decided: field**, for the reasons in
   "Audience and organizing principle" above. The concept coverage table remains as the secondary
   cross-reference. Remaining work: extend the terminology map as entries are written — it
   currently covers {{N_TERMS}} terms across the {{N_ENTRIES}} written entries, and the backlog entries most likely to generate
   domain-specific questions (power systems, portfolio optimization, seismic tomography, MDPs) have no
   terminology coverage yet.
