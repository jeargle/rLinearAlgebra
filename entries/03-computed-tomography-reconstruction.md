---
id: 3
slug: computed-tomography-reconstruction
status: seed
title: 'Computed tomography: reconstructing an interior from its shadows'
short_title: Computed tomography reconstruction
field_label: Medical imaging (and, with different physics, seismic tomography and electron microscopy)
tier_note: ill-posedness is explained through the singular-value spectrum. A small noisy system solved
  two ways (naive vs regularized) works at Tier 1; the Radon-transform theory is Tier 3.
nav_field: Medicine & Imaging
field: Medicine
subfield: Medical imaging
tier: 2
tier_ceiling: 3
prereq_beyond_la: integral transforms; inverse-problem theory
scalar_field: R (nonnegative in practice)
vector_space: image in R^N (N voxels); measurements in R^M (M rays); A maps R^N to R^M with M != N
core_la_object: Ill-posed sparse linear system
la_concepts: ill-posedness; SVD spectrum; Tikhonov regularization; row-action methods
primary_method: Kaczmarz/ART; CG on normal equations
matrix_structure: very sparse, severely ill-conditioned
typical_size: 1e6-1e9 unknowns
worked_example_size: 32x32 Shepp-Logan phantom
terminology:
  projection / ray sum: one row of A applied to x — a line integral through the object
  sinogram: the measurement vector b, arranged by angle and detector position
  attenuation coefficient: the unknown x, one value per voxel
  system matrix / forward projector: A, the discretized Radon transform
  backprojection: applying A transpose to the data
  filtered backprojection (FBP): an analytic spectral inverse of the forward operator
  ART / SIRT: Kaczmarz row-action and related simultaneous iterations
  regularization strength: the Tikhonov parameter lambda trading data fit against smoothness
  streak artifact: the visible signature of undersampling — energy in the near-null space
---

## Start here

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

## The problem

An X-ray source and detector rotate around a patient. Each measurement is the total attenuation along one line through the body. Recover the 3D attenuation field.

## Formulation

Discretize the body into voxels `x`; each ray `i` gives

```
∑_j a_ij x_j = b_i,     A x = b
```

where `a_ij` is the length of ray `i` inside voxel `j`. `A` is a discretized Radon transform.

## Matrix structure

Enormous (10⁶–10⁹ rows and columns), very sparse — a ray touches only O(n^{1/3}) of n voxels — and severely ill-conditioned. Singular values decay smoothly toward zero with no gap, which is the signature of an ill-posed inverse problem.

## What is computed

Either filtered backprojection (an analytic spectral inverse, fast, the classical approach) or iterative reconstruction: Kaczmarz/ART row-action sweeps, conjugate gradient on the normal equations, or a regularized objective

```
min_x ‖A x − b‖² + λ ‖L x‖²      (Tikhonov)
```

with total-variation penalties now standard in commercial scanners.

## Why linear algebra is the right tool

Beer–Lambert attenuation is multiplicative in intensity, hence additive in log-intensity — that logarithm is what makes the whole problem linear and the entire field of algebraic reconstruction possible.

## Pitfall worth teaching

The naive least-squares solution amplifies noise through the small singular values. Regularization is not cosmetic smoothing; it is the choice of which part of the null space and near-null space to fill in, and it is where clinical judgment enters the mathematics. Fewer projection angles means lower dose to the patient but a worse-conditioned `A` — the linear algebra sits directly on a medical trade-off.

## Extensions

Compressed sensing MRI (sparsity in a transform domain replaces smoothness); cryo-EM reconstruction, which adds unknown orientations; electrical impedance tomography, which is nonlinear.
