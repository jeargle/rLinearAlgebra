---
id: 24
slug: geodetic-network-adjustment
status: written
title: 'Geodetic network adjustment: least squares where it was invented, and the datum it cannot see'
short_title: Geodetic network adjustment
field_label: Geodesy, land surveying, mapping, GNSS reference frames
tier_note: an adjustment is a least-squares fit whose design matrix is rank-deficient by construction,
  and choosing a datum is choosing how to remove the null space. Precision and reliability analysis
  through the covariance of the estimates, and its eigenvalues, are Tier 2.
nav_field: Earth & Climate Science
field: Earth Science
subfield: Geodesy/surveying
tier: 1
tier_ceiling: 2
prereq_beyond_la: ''
scalar_field: R
vector_space: 'two spaces, as in any least-squares problem: the unknown station coordinates in R^u
  (u = number of stations for heights, 2 or 3 times that for horizontal or 3D positions) and the
  observations in R^m. Measurements are differences, so the design matrix has a null space, the
  datum defect; only coordinate differences are determined'
underlying_equations: 'Observation equations: each measured height difference, distance or direction
  is a function of station coordinates, plus a measurement error; for levelling they are linear,
  h_j − h_i = measured difference'
core_la_object: Rank-deficient least squares
la_concepts: least squares; normal equations; rank deficiency; null space; datum constraints;
  minimum-norm solutions; estimable quantities; weighted least squares
primary_method: Normal equations with datum constraints, or a minimum-norm solution
matrix_structure: sparse, one row per observation with two nonzeros for levelling, rank-deficient by
  the datum defect
typical_size: 1e2-1e6 stations
worked_example_size: a three-benchmark levelling loop with a 0.1 m misclosure
terminology:
  benchmark (station, control point): a surveyed point; its coordinates are unknowns
  observation equation: one row of the system, an observation written in terms of the unknowns
  levelling (spirit levelling): measuring height differences between benchmarks
  misclosure: the amount by which observations around a loop fail to add up to zero
  adjustment: least-squares estimation of the coordinates from redundant, inconsistent observations
  residual (correction) v: the change to each observation that makes the set consistent
  datum: the choice that fixes the null space, such as a benchmark held at a known height
  datum defect: the dimension of the null space of the design matrix
  minimally constrained vs overconstrained adjustment: removing exactly the null space vs also forcing
    the network to fit fixed points
  free network: a minimum-norm solution, with no point held fixed
  estimable quantity: a function of the coordinates that does not depend on the datum, such as a height
    difference
  weight: the inverse of an observation's variance; longer levelling lines get smaller weights
---

## Start here

Surveyors build maps and height systems by measuring between points: how much higher one marker is than
another, how far apart two hilltops are, which direction one lies from the other. They always take more
measurements than strictly needed, because every measurement has small errors and the extras reveal
them. Walk a loop measuring height differences and add them up, and you should return to zero, but you
never quite do.

Making all the measurements agree, by spreading those discrepancies as fairly as possible, is called
adjusting the network. It is where the method of least squares was invented, around 1800, by Legendre
and Gauss, and national mapping agencies still do exactly this, with millions of measurements.

There is a subtlety at the heart of it. Every measurement compares two points, so the measurements
together say nothing about where the whole network sits. Raise every height by a metre and every
measured difference stays the same. Some outside choice, called the datum, has to anchor the network,
such as declaring one marker to be at a known height above sea level. In linear algebra terms, the
equations have a null space, and the datum is how it is removed.

## The problem

Given redundant measurements between stations of a survey network, estimate the station coordinates
that best fit all the measurements, quantify the discrepancies, and fix the network's position (its
datum) so that the coordinates are unique, while recognising which results depend on that choice and
which do not.

## Variables

| Symbol | Name | What it holds | Shape | Units |
|---|---|---|---|---|
| u | number of unknowns | station heights (levelling) or coordinates | integer | — |
| m | number of observations | measured height differences, distances, directions | integer | — |
| h | station heights | the unknowns of a levelling network | u × 1 | metres |
| ℓ | observations | the measured height differences | m × 1 | metres |
| A | design matrix | row k has −1 for the station a measurement starts from and +1 for the station it ends at | m × u | dimensionless |
| v | residuals (corrections) | v = A h − ℓ, what each observation must change by to fit the adjusted heights | m × 1 | metres |
| W | weight matrix | diagonal, with the inverse variance of each observation | m × m | 1/metres² |
| d | datum defect | dimension of the null space of A | integer | — |

## Formulation

**Where the equations come from.** The model is a set of observation equations: each measurement is a
known function of the station coordinates plus a small random error.

**One observation.** A levelling run from benchmark i to benchmark j measures the height difference
between them. The familiar surveying relation is

```
h_j − h_i = ℓ_k + v_k
```

the true height difference equals the measured value plus the correction it needs. Only two unknowns
appear, with coefficients −1 and +1.

**All observations at once.** Stacking one such row per measurement gives

```
A h = ℓ + v
```

with one row of A per observation and one column per station. With more observations than needed, the
measured ℓ is not in the column space of A, so no heights satisfy every equation exactly. The
adjustment chooses h to minimize the weighted sum of squared corrections, vᵀ W v, which leads to the
normal equations

```
Aᵀ W A h = Aᵀ W ℓ
```

the same equations as in the regression entry, with the weights recording that some measurements are
more reliable than others.

**The datum defect.** Every row of A has one +1 and one −1, so A 1 = 0: adding the same constant to
every height leaves every residual unchanged. The null space of A is spanned by the all-ones vector,
the datum defect is d = 1, and Aᵀ W A is singular. The normal equations have infinitely many solutions,
all differing by a constant. A datum is the extra information that picks one: hold a benchmark at a
known height (a minimal constraint), or choose the solution of minimum length (a free network).

**Worked case: a levelling loop.** Three benchmarks P, Q, R. Benchmark P is held at h_P = 100.000 m, and
three equally weighted runs give

```
h_Q − h_P = 2.0 m,     h_R − h_Q = 1.0 m,     h_R − h_P = 3.1 m
```

Around the loop the first two should add up to the third, but 2.0 + 1.0 = 3.0, a misclosure of 0.1 m.
With h_P fixed, two unknowns remain and three equations, and the least-squares solution is

```
h_Q = 102.033 m,     h_R = 103.067 m,     v = (+0.033, +0.033, −0.033) m
```

The misclosure is shared equally among the three equally reliable runs. Holding R at 103.000 m instead
gives h_P = 99.933 m and h_Q = 101.967 m: different heights, but exactly the same height differences and
the same corrections. The free-network (minimum-norm) solution near (100, 102, 103) gives
(99.967, 102.000, 103.033), again with the same differences.

## Matrix structure

`A` is sparse: a levelling observation has two nonzeros, a horizontal distance or direction four to six.
For levelling it is the incidence matrix of the network graph, the same matrix as in the resistor and
traffic entries, and Aᵀ W A is a weighted graph Laplacian. Its null space, the datum defect, has
dimension 1 for heights, 3 for a 2D network of distances (two shifts and a rotation), 4 for a 2D network
of angles only (add scale), and up to 7 in 3D (three shifts, three rotations and a scale).

## What is computed

Weighted least squares with datum constraints. Large adjustments form Aᵀ W A, which is sparse, and solve
it with sparse Cholesky after removing the datum, or use QR on A. National datums were built this way;
the North American height datum NAVD 88 is a continent-wide levelling adjustment held at a single tide
gauge benchmark in Quebec. Modern GNSS reference frames such as the International Terrestrial Reference
Frame are adjustments of millions of satellite observations with the same rank-deficient structure.

## Why linear algebra is the right tool

The surveyor's notions are subspace notions. Redundancy means more rows than the rank, misclosure means
the observations are not in the column space, and the adjustment is an orthogonal projection onto it
(weighted by W). The datum defect is the null space, its size depends on what was measured (heights,
distances, angles), and choosing a datum is choosing a complement to it. Quantities that do not depend
on the datum, such as height differences and distances, are the estimable ones: those whose value is
the same for every solution of the normal equations.

## Pitfall worth teaching

Coordinates from different datums cannot be compared, even though each set is correct. In the worked
case, fixing P or fixing R gives heights that differ by 0.067 m at every benchmark, with identical
differences. Deformation and subsidence monitoring compares a network's coordinates between surveys
years apart, and if the two adjustments used different datum points, or a datum point that itself moved,
the comparison shows apparent motion everywhere that is entirely an artefact of the datum. The test is
the one linear algebra suggests: compare only datum-independent quantities, or transform both solutions
to the same datum first. A second consequence is that a solver handed the unconstrained normal equations
either fails, because Aᵀ W A is singular, or returns one particular solution chosen silently by its
pivoting, so the datum has to be chosen explicitly.

## Extensions

Horizontal and 3D networks have nonlinear observation equations (distances and angles), solved by
linearizing about approximate coordinates and adjusting repeatedly, each step a rank-deficient linear
least-squares problem like this one. The covariance matrix (Aᵀ W A)⁻¹, computed in a chosen datum,
describes precision, and its eigenvectors give error ellipses (Tier 2). The regression entry is the same
projection in statistical vocabulary; the Massey and Colley ranking entry has exactly this
incidence-matrix structure and the same one-dimensional null space, because game results, like height
differences, only compare pairs; and GNSS positioning is the trilateration on-ramp of the Kalman
filtering entry.
