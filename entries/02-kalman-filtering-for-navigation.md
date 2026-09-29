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
underlying_equations: Linear ODE driven by random noise (a stochastic differential equation), dx/dt =
  A x + noise, discretized exactly to x_{k+1} = F x_k + w_k
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

## Variables

| Symbol | Name | What it holds | Shape | Units |
|---|---|---|---|---|
| k | time-step index | which update we are on | integer | — |
| Δt | time step | interval between updates | scalar | s |
| x_k | state vector | the quantities being estimated at step k; in the running example, position p and velocity v along one axis, x = [p, v]ᵀ | n × 1 (n = 2 here) | mixed: m and m/s |
| A | continuous-time system matrix | how the state changes instantaneously; [[0, 1], [0, 0]] says dp/dt = v and dv/dt = 0 apart from noise | n × n | entries in s⁻¹ |
| F | state-transition matrix | how the state at step k predicts the state at step k+1; here [[1, Δt], [0, 1]] | n × n | mixed: dimensionless and s |
| w_k | process noise | what the model leaves out over one step: unknown accelerations, gusts, wheel slip | n × 1 | same as x |
| Q | process-noise covariance | how large and how correlated w_k is | n × n | products of state units: m², m²/s, m²/s² |
| z_k | measurement vector | what the sensor reports at step k; for GNSS, a measured position | m × 1 (m = 1 here) | m |
| H | observation matrix | which combination of the state the sensor sees; [1, 0] when it measures position only | m × n | measurement units per state unit |
| η_k | measurement noise | sensor error at step k | m × 1 | m |
| R | measurement-noise covariance | spread of the sensor error; a few metres squared for a consumer GNSS fix | m × m | m² |
| x̂⁻, x̂⁺ | state estimate | the filter's best estimate before and after using z_k | n × 1 | same as x |
| P⁻, P⁺ | estimate covariance | uncertainty of the estimate before and after using z_k; diagonal entries are variances (squared standard deviations), off-diagonal entries say how errors in different components move together | n × n | products of state units |
| ỹ | innovation | measured minus predicted measurement | m × 1 | m |
| K | Kalman gain | how much to correct each state component per unit of innovation | n × m | state units per measurement unit: dimensionless for p, s⁻¹ for v |
| N(0, Q) | Gaussian distribution | mean zero, covariance Q | — | — |

## Formulation

**Where the equations come from.** The vehicle's motion obeys an ordinary differential equation in continuous time. For the constant-velocity model, dp/dt = v and dv/dt = a(t), where the acceleration a(t) is unknown and is modelled as random noise. In matrix form this is dx/dt = A x + noise. Because the ODE is driven by a random input it is a stochastic differential equation, and its solution is not a single trajectory but a probability distribution over trajectories. That is why the filter carries a covariance and not just an estimate.

Integrating the ODE exactly over one step gives the discrete model. For this A the matrix exponential is simple: F = exp(A Δt) = [[1, Δt], [0, 1]], which just says p_{k+1} = p_k + Δt v_k and v_{k+1} = v_k.

**The model.**

```
x_{k+1} = F x_k + w_k,     w_k ~ N(0, Q)      (dynamics)
z_k     = H x_k + η_k,     η_k ~ N(0, R)      (measurement)
```

The first line models how the true state evolves between measurements; the second models what the sensor reports about it. Both are linear, and both noises are Gaussian.

**The filter.** Each step has two stages. *Predict* pushes the estimate and its uncertainty forward through the dynamics:

```
x̂⁻ = F x̂⁺_{k−1}
P⁻ = F P⁺_{k−1} Fᵀ + Q
```

F P Fᵀ is how a covariance transforms under the linear map F, and adding Q makes uncertainty grow by what the model leaves out. *Update* blends the prediction with the new measurement, weighted by their uncertainties:

```
ỹ  = z_k − H x̂⁻                      (innovation)
K  = P⁻ Hᵀ (H P⁻ Hᵀ + R)⁻¹           (Kalman gain)
x̂⁺ = x̂⁻ + K ỹ
P⁺ = (I − K H) P⁻
```

H P⁻ Hᵀ + R is the covariance of the innovation: prediction uncertainty seen through the sensor, plus sensor noise. When R is large relative to H P⁻ Hᵀ the gain is small and the filter mostly trusts its prediction; when R is small it mostly trusts the sensor.

**What a solution means.** At each step the output is a Gaussian distribution with mean x̂⁺ and covariance P⁺. For a linear model with Gaussian noise this is exact: it is the distribution of the true state given every measurement so far, and x̂⁺ is the minimum-mean-squared-error estimate.

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
