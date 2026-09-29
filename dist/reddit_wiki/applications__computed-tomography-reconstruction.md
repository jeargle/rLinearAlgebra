# Computed tomography: reconstructing an interior from its shadows

### Start here

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

**Field:** Medical imaging (and, with different physics, seismic tomography and electron microscopy)  
**Tier:** 3 — the linearity comes from solving the Beer–Lambert ODE along each ray and taking a logarithm; ill-posedness is read from the singular-value spectrum. On-ramp: a small noisy A x = b solved naively and with regularization.  
**Scalar field:** R (nonnegative in practice)  
**Vectors:** image in R^N (N voxels); measurements in R^M (M rays); A maps R^N to R^M with M != N  
**Underlying equations:** First-order linear ODE along each ray (Beer–Lambert law), dI/ds = −μ I; the logarithm of its solution is linear in μ

### The problem

An X-ray source and detector rotate around a patient. Each measurement is the total attenuation along one line through the body. Recover the 3D attenuation field.

### Variables

| Symbol | Name | What it holds | Shape | Units |
|---|---|---|---|---|
| μ(r) | linear attenuation coefficient | fraction of X-ray photons removed per unit path length at location r; this is what the image shows | function of position | m⁻¹ (clinically often cm⁻¹) |
| s | path length | distance travelled along a ray | scalar | m |
| I(s) | beam intensity | photon flux remaining after travelling distance s | scalar | photon counts |
| I₀ | unattenuated intensity | detector reading with nothing in the beam (from calibration) | scalar per ray | photon counts |
| I_i | measured intensity | detector reading for ray i | scalar | photon counts |
| N | number of voxels | the image is divided into N small cubes (pixels in 2D) | integer | — |
| M | number of rays | detector elements × projection angles | integer | — |
| x | image vector | x_j is μ inside voxel j, voxels listed in a fixed order | N × 1 | m⁻¹ |
| b | measurement vector (sinogram) | b_i = −ln(I_i / I₀), total attenuation along ray i | M × 1 | dimensionless |
| A | system matrix (forward projector) | a_ij is the length of ray i inside voxel j; zero for the vast majority of pairs | M × N | m |
| λ | regularization weight | how strongly smoothness is favoured over fitting the data (used in What is computed) | scalar | chosen so the two terms are comparable |
| L | regularization operator | typically differences between neighbouring voxels, so ‖L x‖ measures roughness | p × N | depends on the choice |

### Formulation

**Where the equations come from.** As a beam travels a short distance ds through material, the fraction of photons removed is μ ds. The intensity along a ray therefore obeys a first-order linear ordinary differential equation, the Beer–Lambert law:

```
dI/ds = −μ(s) I(s)
```

Its solution is I = I₀ exp(−∫ μ(s) ds). Taking the logarithm:

```
b_i = −ln(I_i / I₀) = ∫_{ray i} μ(s) ds
```

This is the step that makes CT a linear problem. The raw reading depends exponentially on μ, but the log-transformed reading is a line integral of μ, which is linear in μ. The set of all such line integrals is the Radon transform of μ.

**Discretization.** Assume μ is constant inside each voxel. The integral along ray i then becomes a sum over the voxels it crosses, each term being the length inside the voxel times the value there:

```
b_i = Σ_j a_ij x_j      for every ray i,      i.e.   A x = b
```

Units check: metres times m⁻¹ is dimensionless, matching b. This models each measurement as the total attenuation met by one ray, and it defines M equations in N unknowns.

**What a solution means.** x is an estimate of μ, one value per voxel. For display it is converted to Hounsfield units, HU = 1000 (μ − μ_water) / μ_water, which puts water at 0 and air at −1000. The system is not solved exactly: photon counts are noisy, M and N differ, and A is badly conditioned, so the reconstruction is posed as regularized least squares (see What is computed).

**Where the model is approximate.** The ODE assumes a single X-ray energy. Real tubes emit a spectrum, low-energy photons are absorbed first, and μ in fact depends on energy. That mismatch, called beam hardening, is a standard source of artifacts precisely because it violates the linearity above.

### Matrix structure

Enormous (10⁶–10⁹ rows and columns), very sparse — a ray touches only O(n^{1/3}) of n voxels — and severely ill-conditioned. Singular values decay smoothly toward zero with no gap, which is the signature of an ill-posed inverse problem.

### What is computed

Either filtered backprojection (an analytic spectral inverse, fast, the classical approach) or iterative reconstruction: Kaczmarz/ART row-action sweeps, conjugate gradient on the normal equations, or a regularized objective

```
min_x ‖A x − b‖² + λ ‖L x‖²      (Tikhonov)
```

with total-variation penalties now standard in commercial scanners.

### Why linear algebra is the right tool

Beer–Lambert attenuation is multiplicative in intensity, hence additive in log-intensity — that logarithm is what makes the whole problem linear and the entire field of algebraic reconstruction possible.

### Pitfall worth teaching

The naive least-squares solution amplifies noise through the small singular values. Regularization is not cosmetic smoothing; it is the choice of which part of the null space and near-null space to fill in, and it is where clinical judgment enters the mathematics. Fewer projection angles means lower dose to the patient but a worse-conditioned `A` — the linear algebra sits directly on a medical trade-off.

### Extensions

Compressed sensing MRI (sparsity in a transform domain replaces smoothness); cryo-EM reconstruction, which adds unknown orientations; electrical impedance tomography, which is nonlinear.

### Terminology

How this field's vocabulary reads as linear algebra.

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

---

[Back to the index](/r/LinearAlgebra/wiki/applications)
