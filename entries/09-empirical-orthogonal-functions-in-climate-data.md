---
id: 9
slug: empirical-orthogonal-functions-in-climate-data
status: seed
title: 'Empirical orthogonal functions: finding the dominant patterns in climate data'
short_title: Empirical orthogonal functions in climate data
field_label: Atmospheric and ocean science, climatology
tier_note: truncated SVD and the Eckart–Young optimality statement.
nav_field: Earth & Climate Science
field: Earth Science
subfield: Climatology/oceanography
tier: 2
tier_ceiling: 2
prereq_beyond_la: ''
scalar_field: R
vector_space: each time slice is a spatial field in R^s (s grid points); EOFs live in R^s and principal-component
  series in R^t (t time steps)
core_la_object: Low-rank approximation of a data matrix
la_concepts: SVD; Eckart-Young optimality; variance partitioning; interpretability limits
primary_method: Truncated/randomized SVD
matrix_structure: dense, low effective rank
typical_size: 1e4-1e5 x 1e3
worked_example_size: synthetic SST field with two planted modes
terminology:
  EOF: a left singular vector — one spatial pattern
  principal component time series: the corresponding right singular vector, scaled
  explained variance: sigma_i^2 as a fraction of the total
  loading: one entry of an EOF, i.e. one grid point's weight in that pattern
  anomaly field: the mean-centered data matrix
  rotated EOF (varimax): a deliberately non-orthogonal re-basis of the leading subspace
  North's rule of thumb: a test for whether two singular values are too close to separate the modes
---

## Start here

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

## The problem

A century of monthly sea-surface temperatures on a global grid is a matrix with 10⁴–10⁵ spatial points and 10³ time steps. Extract the few spatial patterns that account for most of the variability — the objects a climatologist can actually reason about, like El Niño.

## Formulation

Center the data matrix `X` (space × time) and take the SVD:

```
X = U Σ Vᵀ
```

Columns of `U` are the empirical orthogonal functions (spatial patterns), rows of `Vᵀ` are their principal-component time series, and `σᵢ²` is the variance each pattern explains.

## Matrix structure

Tall or wide but dense; the effective rank is low — typically 5–10 modes capture most of the variance, which is why the technique works at all.

## What is computed

Truncated SVD (randomized SVD or Lanczos bidiagonalization for large grids). The Eckart–Young theorem guarantees that the rank-k truncation is the best possible rank-k approximation in both the Frobenius and spectral norms — an optimality statement, not a heuristic.

## Why linear algebra is the right tool

The field is spatially correlated: neighboring grid points are far from independent. Low-rank structure is a mathematical restatement of physical coherence, and the SVD finds it without being told any physics.

## Pitfall worth teaching

EOFs are constrained to be orthogonal, and physical modes are generally not. A leading EOF can be a mathematical mixture of two distinct physical mechanisms, and a second EOF can be an artifact of orthogonality to the first (North's rule of thumb gives a degeneracy test). This is the best example in the collection of a decomposition whose mathematical optimality does not imply physical interpretability — worth teaching alongside the same caution for PCA in genomics.

## Extensions

Proper orthogonal decomposition and reduced-order models in fluid dynamics; dynamic mode decomposition, which extracts an approximate linear operator (Koopman) rather than just a basis; the same SVD machinery in latent semantic analysis, recommender systems, and matrix completion.
