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

### The problem

Given photographs of a scene from unknown viewpoints, recover both the camera positions and the 3D geometry. This is the engine behind phone panorama stitching, drone mapping, visual SLAM, and photogrammetric reconstruction.

### Formulation

Homogeneous coordinates turn the nonlinear perspective projection into a linear map:

```
λ [u, v, 1]ᵀ = K [R | t] [X, Y, Z, 1]ᵀ
```

Two views of the same rigid scene are related by the essential matrix `E` through the epipolar constraint

```
x'ᵀ E x = 0
```

Stacking that constraint over ≥8 point correspondences gives a homogeneous system `A e = 0`; the solution is the right singular vector of `A` with the smallest singular value.

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
