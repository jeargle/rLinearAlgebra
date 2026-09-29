# Empirical orthogonal functions: finding the dominant patterns in climate data

### Start here

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

**Field:** Atmospheric and ocean science, climatology  
**Tier:** 2 — truncated SVD and the Eckart–Young optimality statement; no differential equation is used. Relating EOFs to the dynamics through a stochastic ODE is a Tier 3 extension.  
**Scalar field:** R  
**Vectors:** each time slice is a spatial field in R^s (s grid points); EOFs live in R^s and principal-component series in R^t (t time steps)  
**Underlying equations:** None used: a statistical decomposition of observed data (the ocean itself obeys PDEs that the method ignores)

### The problem

A century of monthly sea-surface temperatures on a global grid is a matrix with 10⁴–10⁵ spatial points and 10³ time steps. Extract the few spatial patterns that account for most of the variability — the objects a climatologist can actually reason about, like El Niño.

### Variables

| Symbol | Name | What it holds | Shape | Units |
|---|---|---|---|---|
| s | number of grid points | spatial locations with data | integer | — |
| t | number of time steps | months in the record | integer | — |
| T_gk | sea-surface temperature | temperature at grid point g in month k | scalar | °C |
| X | anomaly matrix | x_gk = T_gk minus the long-term average for that calendar month at that grid point | s × t | K (a temperature difference, so K and °C agree) |
| W | area weights | diagonal matrix of √cos(latitude), so small high-latitude grid cells do not count as much as large tropical ones | s × s | dimensionless |
| U | EOFs | columns u_i are spatial patterns of unit length | s × ρ | dimensionless |
| Σ | singular values | diagonal σ_1 ≥ σ_2 ≥ … ≥ 0: the strength of each pattern | ρ × ρ | K |
| V | normalized time series | columns v_i of unit length | t × ρ | dimensionless |
| a_i | principal-component time series | a_i = σ_i v_i: how strongly pattern i is present each month | t × 1 | K |
| ρ | rank | number of nonzero singular values, at most min(s, t) | integer | — |
| q | modes retained | how many patterns are kept after truncation | integer | — |
| C | spatial covariance | C = X Xᵀ / (t − 1) | s × s | K² |

### Formulation

**Where the equations come from.** No differential equation is used. The ocean and atmosphere obey partial differential equations of fluid flow and heat transport, but EOF analysis ignores them entirely: it is a statistical decomposition of observed data. That is its strength, since no model is needed, and its main limitation, since nothing forces the patterns it finds to be dynamical modes of the system.

**The decomposition.**

```
X = U Σ Vᵀ = Σ_i σ_i u_i v_iᵀ
```

This models the anomaly field as a sum of rank-one pieces, each a fixed spatial pattern u_i multiplied by a time series σ_i v_i. Read by columns: the map for month k is Σ_i u_i (σ_i v_ik), a weighted combination of the patterns with weights that change month by month.

**Truncation.** Keeping the first q terms gives the best possible rank-q approximation of X, and pattern i accounts for the fraction σ_i² / Σ_j σ_j² of the total variance. Equivalently, the u_i are the eigenvectors of the covariance matrix C, with eigenvalues σ_i² / (t − 1). That is why EOFs are called principal components.

**Area weighting.** On a latitude–longitude grid, cells shrink toward the poles. The SVD is therefore applied to W X, and the resulting patterns are divided by the weights before they are plotted.

### Matrix structure

Tall or wide but dense; the effective rank is low — typically 5–10 modes capture most of the variance, which is why the technique works at all.

### What is computed

Truncated SVD (randomized SVD or Lanczos bidiagonalization for large grids). The Eckart–Young theorem guarantees that the rank-k truncation is the best possible rank-k approximation in both the Frobenius and spectral norms — an optimality statement, not a heuristic.

### Why linear algebra is the right tool

The field is spatially correlated: neighboring grid points are far from independent. Low-rank structure is a mathematical restatement of physical coherence, and the SVD finds it without being told any physics.

### Pitfall worth teaching

EOFs are constrained to be orthogonal, and physical modes are generally not. A leading EOF can be a mathematical mixture of two distinct physical mechanisms, and a second EOF can be an artifact of orthogonality to the first (North's rule of thumb gives a degeneracy test). This is the best example in the collection of a decomposition whose mathematical optimality does not imply physical interpretability — worth teaching alongside the same caution for PCA in genomics.

### Extensions

Proper orthogonal decomposition and reduced-order models in fluid dynamics; dynamic mode decomposition, which extracts an approximate linear operator (Koopman) rather than just a basis; the same SVD machinery in latent semantic analysis, recommender systems, and matrix completion.

**The link to dynamics, and why it is weak.** If the anomalies obeyed a linear stochastic ODE, dx/dt = B x + noise, the EOFs would be eigenvectors of the resulting covariance. Those coincide with the eigenvectors of B, the actual dynamical modes, only in special cases, such as when B is symmetric and the noise is equally strong in every direction. This is the precise sense in which an optimal pattern need not be a physical mode.

### Terminology

How this field's vocabulary reads as linear algebra.

| Domain term | In linear algebra |
|---|---|
| EOF | a left singular vector — one spatial pattern |
| principal component time series | the corresponding right singular vector, scaled |
| explained variance | sigma_i^2 as a fraction of the total |
| loading | one entry of an EOF, i.e. one grid point's weight in that pattern |
| anomaly field | the mean-centered data matrix |
| rotated EOF (varimax) | a deliberately non-orthogonal re-basis of the leading subspace |
| North's rule of thumb | a test for whether two singular values are too close to separate the modes |

---

[Back to the index](/r/LinearAlgebra/wiki/applications)
