---
id: 2
slug: kalman-filtering-for-navigation
status: seed
title: 'Kalman filtering: where is the vehicle, given noisy and incomplete measurements?'
short_title: Kalman filtering for navigation
field_label: Aerospace, robotics, control engineering
tier_note: the covariance recursion needs positive definiteness and observability rank; the static GNSS
  special case is a Tier 1 on-ramp. Full stochastic treatment is Tier 3.
nav_field: Control & Robotics
field: Engineering
subfield: Aerospace/control
tier: 2
tier_ceiling: 3
prereq_beyond_la: probability; stochastic processes
scalar_field: R
vector_space: state in R^n (n = 6-50); measurements in R^m; covariances live in Sym_n, the real vector
  space of symmetric n x n matrices, dimension n(n+1)/2
core_la_object: Covariance projection and Riccati recursion
la_concepts: least squares; projection; positive semidefinite; observability rank
primary_method: Recursive weighted least squares; square-root filtering
matrix_structure: small dense symmetric PSD
typical_size: 6-50 states
worked_example_size: constant-velocity tracker with GNSS dropouts
terminology:
  state vector: the unknown x being estimated
  process noise / measurement noise: the covariance matrices Q and R
  covariance matrix P: the uncertainty ellipsoid; symmetric positive semidefinite
  Kalman gain: the projection weight matrix that blends prediction and measurement
  innovation / residual: z - Hx, the part of the measurement the prediction did not explain
  observation model H: the linear map from state space to measurement space
  observability: rank of the stacked matrix [H; HF; HF^2; ...]
  filter divergence: P losing positive definiteness in finite precision, or an unobservable direction
    growing without bound
  square-root filter: propagating a Cholesky factor of P instead of P
---

## Start here

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

## The problem

A vehicle carries an inertial measurement unit that drifts, plus a GNSS receiver that is accurate but intermittent and noisy. Produce a continuously updated best estimate of position, velocity, and attitude — with an honest uncertainty attached.

## Formulation

Linear-Gaussian state-space model:

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

## Matrix structure

Small and dense (state dimension 6–50 for navigation, thousands for SLAM). `P`, `Q`, `R` are symmetric positive semidefinite. The covariance recursion is a discrete Riccati equation.

## What is computed

A weighted least-squares update, done recursively so no measurement history is stored. Square-root and UD-factored forms (Potter, Bierman–Thornton) propagate a Cholesky factor of `P` instead of `P` itself to guarantee the covariance stays positive definite in finite precision — this is why Apollo's navigation filter was implemented in square-root form.

## Why linear algebra is the right tool

The Kalman gain is an orthogonal-projection operator in a metric defined by the noise covariances. "Optimal fusion of uncertain information" turns out to be a projection, which is why the formula is a matrix expression and not a heuristic.

## Pitfall worth teaching

Rank of the observability matrix `[H; HF; HF²; …]` tells you which state directions the sensors can ever pin down. An unobservable direction shows up as a covariance that grows without bound — the filter tells you honestly that it does not know.

## Extensions

Static GNSS trilateration as the nonrecursive special case (Gauss–Newton on an overdetermined system); extended and unscented filters for nonlinear dynamics; ensemble Kalman filters for weather data assimilation at 10⁸ state dimensions.
