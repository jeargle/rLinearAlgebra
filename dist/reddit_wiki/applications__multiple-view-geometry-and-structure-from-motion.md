# Multiple-view geometry: 3D structure from 2D images

### Start here

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

**Field:** Computer vision, photogrammetry, robotics  
**Tier:** 2 — the SVD does the work. The 2D homography and the transformation pipeline behind it sit at Tier 1; pose refinement on SE(3) is Tier 3.  
**Scalar field:** R  
**Vectors:** scene points in R^3, written in homogeneous R^4 up to scale (projective space P^3); image points in R^2 as homogeneous R^3 up to scale (P^2). The unknown essential matrix is vectorized to R^9 and recovered only up to scale, so it is really a point of P^8  
**Underlying equations:** None: projective geometry of the pinhole camera

### The problem

Given photographs of a scene from unknown viewpoints, recover both the camera positions and the 3D geometry. This is the engine behind phone panorama stitching, drone mapping, visual SLAM, and photogrammetric reconstruction.

### Variables

| Symbol | Name | What it holds | Shape | Units |
|---|---|---|---|---|
| X̃ | homogeneous world point | [X, Y, Z, 1]ᵀ: a scene point's position in world coordinates, with a 1 appended | 4 × 1 | m (last entry dimensionless) |
| R | rotation matrix | the camera's orientation relative to the world; orthogonal with determinant +1 | 3 × 3 | dimensionless |
| t | translation | the world origin expressed in camera coordinates | 3 × 1 | m |
| K | intrinsic (calibration) matrix | [[f_x, γ, c_x], [0, f_y, c_y], [0, 0, 1]]: converts camera-frame directions into pixels | 3 × 3 | pixels (last row dimensionless) |
| f_x, f_y | focal length | focal length measured in pixel widths and heights | scalars | pixels |
| c_x, c_y | principal point | the pixel where the optical axis meets the image | scalars | pixels |
| γ | skew | non-perpendicular pixel axes; essentially 0 for modern sensors | scalar | pixels |
| (u, v) | pixel coordinates | where the point appears in the image | scalars | pixels |
| x̃ | homogeneous image point | [u, v, 1]ᵀ | 3 × 1 | pixels (last entry dimensionless) |
| λ | projective depth | the point's depth along the camera's viewing axis (its Z coordinate in the camera frame) | scalar | m |
| x̂ | normalized image coordinates | x̂ = K⁻¹ x̃: the direction of the viewing ray, scaled so its last entry is 1 | 3 × 1 | dimensionless |
| [t]ₓ | cross-product matrix | the skew-symmetric matrix with [t]ₓ a = t × a for every a | 3 × 3 | m |
| E | essential matrix | E = [t]ₓ R: encodes the relative pose of two calibrated cameras | 3 × 3 | defined only up to scale |
| F | fundamental matrix | F = K′⁻ᵀ E K⁻¹: the same constraint written in pixel coordinates | 3 × 3 | defined only up to scale |
| N | number of correspondences | matched points visible in both images; at least 8 here | integer | — |
| A | constraint matrix | one row per correspondence, built from the products of their coordinates | N × 9 | dimensionless |
| e | vectorized E | the nine entries of E stacked into a column | 9 × 1 | dimensionless |

Primes mark the second view: x̂′ is the same scene point seen by the second camera, and K′ is that camera's intrinsic matrix.

### Formulation

**Where the equations come from.** There is no differential equation; the model is the geometry of an ideal pinhole camera.

**Projection.**

```
λ x̃ = K [R | t] X̃
```

Read right to left. [R | t] X̃ rotates and translates the world point into camera coordinates (in metres). K converts those coordinates into pixels. The scalar λ is the depth, and dividing by it is the perspective effect that makes distant objects smaller. Homogeneous coordinates isolate that division in one scalar, so everything else is matrix multiplication. Units check: pixels × metres on the right, λ in metres on the left, leaving pixels.

**Two views.** Place the first camera at the world origin (R = I, t = 0) and the second at an unknown R, t. A scene point appears at x̂ in the first image and x̂′ in the second, both in normalized coordinates. The two viewing rays and the baseline t between the cameras lie in one plane, and that coplanarity is the epipolar constraint:

```
x̂′ᵀ E x̂ = 0,      E = [t]ₓ R
```

In pixel coordinates the same constraint reads x̃′ᵀ F x̃ = 0. Each correspondence gives one equation that is linear in the nine unknown entries of E, and stacking N of them gives

```
A e = 0
```

**What a solution means.** The equation is homogeneous, so if e solves it, so does any multiple of e. E, and therefore t, is recovered only up to scale: from images alone, a building and an accurate scale model of it are indistinguishable. The estimate is the unit vector that minimizes ‖A e‖, which is the right singular vector of A with the smallest singular value. Decomposing E then yields R and the direction of t; of the four candidate decompositions, the right one places the scene points in front of both cameras.

### Matrix structure

`A` is small and dense (n × 9). The later bundle-adjustment stage produces a large, sparse, highly structured Jacobian with the characteristic "arrowhead" block pattern from cameras and points.

### What is computed

SVD, twice and for two different reasons: once to solve the homogeneous least-squares problem (smallest singular vector), and once to project the estimate onto the manifold of valid essential matrices by zeroing the third singular value and equalizing the first two. Bundle adjustment then refines everything by sparse Levenberg–Marquardt with the Schur complement trick to eliminate the 3D points.

### Why linear algebra is the right tool

Projective geometry in homogeneous coordinates is the reason: a genuinely nonlinear operation (perspective division) becomes a linear map followed by a normalization. Adding one coordinate buys linearity.

### Pitfall worth teaching

Conditioning matters more than the algorithm here. Hartley's normalized 8-point algorithm — translate and scale the image points before forming `A` — is the difference between usable and useless results, and the only change is a preconditioning of the input. It is one of the cleanest real demonstrations that condition number is not an academic concern.

### Extensions

Homography estimation and image stitching; the PnP problem; the Perron-like structure in rotation averaging; SE(3) and Lie-group optimization for pose graphs.

### Terminology

How this field's vocabulary reads as linear algebra.

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

---

[Back to the index](/r/LinearAlgebra/wiki/applications)
