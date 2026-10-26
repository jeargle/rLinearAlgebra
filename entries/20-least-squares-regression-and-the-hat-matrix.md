---
id: 20
slug: least-squares-regression-and-the-hat-matrix
status: written
title: 'Least-squares regression: fitting a model is projecting onto a column space'
short_title: Least squares regression and the hat matrix
field_label: Statistics, econometrics, data science, every experimental science
tier_note: fitting, fitted values, residuals and leverage all come from an orthogonal projection, with
  no eigenvalues needed. Conditioning and the SVD view of collinearity are Tier 2; confidence intervals
  and p-values need statistical inference beyond linear algebra.
nav_field: Statistics
field: Statistics
subfield: Applied statistics
tier: 1
tier_ceiling: 2
prereq_beyond_la: statistical inference for the diagnostics
scalar_field: R
vector_space: 'two spaces: the observations y, fitted values and residuals live in R^n (one coordinate
  per data point), while the coefficients β live in R^k (one per predictor). The design matrix maps R^k
  into R^n, and the fitted values fill out only a k-dimensional subspace of R^n, its column space'
underlying_equations: 'A statistical model, y = X β + noise, fitted by minimizing a sum of squares'
core_la_object: Orthogonal projection onto a column space
la_concepts: column space; orthogonal projection; normal equations; orthogonal complement; QR
  factorization; rank and collinearity; trace of a projection
primary_method: QR factorization (Householder); normal equations only when well conditioned
matrix_structure: tall dense or sparse design matrix, n × k with n much larger than k
typical_size: 1e2-1e7 rows, 1-1e3 columns
worked_example_size: a straight line through 4 points by hand, with its 4 × 4 hat matrix
terminology:
  design matrix (model matrix) X: the n × k matrix whose columns are the predictors, including a column
    of 1s for the intercept
  regression coefficients β: coordinates of the fitted vector in the basis given by the columns of X
  fitted values ŷ: the orthogonal projection of y onto the column space of X
  residuals: the component of y in the orthogonal complement of the column space
  hat matrix H: the projection matrix X (XᵀX)⁻¹ Xᵀ, so ŷ = H y
  leverage h_ii: the i-th diagonal entry of H; how strongly observation i pulls its own fitted value
  degrees of freedom: dimensions; k for the model (the trace of H) and n − k for the residuals
  normal equations: Xᵀ X β = Xᵀ y, the statement that the residual is orthogonal to every column of X
  multicollinearity: columns of X that are nearly linearly dependent, so β is poorly determined
  dummy variable trap: an exactly dependent set of indicator columns, which makes X rank-deficient
  R²: the squared length of the centered fitted vector over that of the centered data vector
---

## Start here

You have measured something at several settings — sales at several prices, a plant's height on
several days, a reaction's speed at several temperatures — and you want the straight line that best
describes the trend. The points never lie exactly on a line, so "best" needs a definition. The usual
one is to make the vertical misses as small as possible overall, by minimizing the sum of their
squares.

Here is the picture that makes the whole subject simple. List all the measured values as one long
list of numbers, one per data point. Every possible straight line, evaluated at the same settings,
gives another such list, and all of those lists together form a flat sheet through the origin of a
high-dimensional space. Your data sit somewhere off that sheet. The best-fitting line is the point
on the sheet directly beneath the data, found by dropping a perpendicular, exactly as the shortest
path from a point to a floor goes straight down.

Everything a statistician computes about a fit — the fitted values, the leftovers, how much each
data point influences its own fit — comes from that one perpendicular drop.

## The problem

Given n observations of a response and k predictors, find the coefficients of the linear model that
minimize the sum of squared residuals, and describe the fit: fitted values, residuals, and how much
influence each observation has.

## Variables

| Symbol | Name | What it holds | Shape | Units |
|---|---|---|---|---|
| n | number of observations | data points | integer | — |
| k | number of coefficients | predictors, counting the intercept | integer | — |
| y | response vector | the measured values | n × 1 | units of the response |
| X | design matrix | column j holds predictor j at every observation; the first column is all 1s | n × k | each column in its predictor's units |
| β | coefficients | intercept and slopes | k × 1 | response units per predictor unit |
| β̂ | fitted coefficients | the least-squares solution | k × 1 | as β |
| ŷ | fitted values | ŷ = X β̂ | n × 1 | response units |
| r | residuals | r = y − ŷ | n × 1 | response units |
| H | hat matrix | H = X (XᵀX)⁻¹ Xᵀ, which maps y to ŷ | n × n | dimensionless |
| h_ii | leverage | diagonal entry i of H | scalar per observation | dimensionless |
| Q, R | QR factors | X = Q R with Q having orthonormal columns and R upper triangular | n × k and k × k | Q dimensionless; R in X's units |

## Formulation

**Where the equations come from.** The model is a statistical
assumption: each response is a linear combination of the predictors plus random noise,

```
y = X β + noise
```

and the coefficients are chosen to minimize the sum of squared residuals ‖y − X β‖².

**The familiar case.** For a straight line, y ≈ b_0 + b_1 x, X has two columns, the 1s and the x
values, and β = (b_0, b_1). The answer from a first statistics course,

```
b_1 = Σ (x_i − x̄)(y_i − ȳ) / Σ (x_i − x̄)²,     b_0 = ȳ − b_1 x̄
```

is the general formula below worked out for two columns.

**The geometry.** As β ranges over ℝ^k, the vector X β ranges over the column space of X, a
k-dimensional subspace of ℝ^n. Minimizing ‖y − X β‖ asks for the point of that subspace closest to y.
The closest point is the orthogonal projection, characterized by a residual perpendicular to every
column of X:

```
Xᵀ (y − X β̂) = 0     ⟺     Xᵀ X β̂ = Xᵀ y
```

These are the normal equations, "normal" meaning perpendicular. When the columns of X are linearly
independent, XᵀX is invertible and

```
β̂ = (XᵀX)⁻¹ Xᵀ y,     ŷ = H y,     H = X (XᵀX)⁻¹ Xᵀ
```

H is called the hat matrix because it puts the hat on y, turning the data y into the fitted values ŷ.
It is a projection: H² = H (projecting twice changes nothing) and Hᵀ = H (the
projection is orthogonal). Its trace is k, the dimension of the subspace it projects onto, which is
why a fit with k coefficients uses up k degrees of freedom and leaves n − k for the residuals.

**Worked case: a line through four points.** Take the points (0, 1), (1, 3), (2, 4), (3, 4). Then
x̄ = 1.5, ȳ = 3, Σ (x_i − x̄)(y_i − ȳ) = 5 and Σ (x_i − x̄)² = 5, so the slope is 1 and the intercept is
1.5. The fitted values are (1.5, 2.5, 3.5, 4.5) and the residuals (−0.5, 0.5, 0.5, −0.5). They add
up to zero, which is their orthogonality to the column of 1s, and (0, 1, 2, 3) · (−0.5, 0.5, 0.5, −0.5) = 0
is their orthogonality to the x column. The hat matrix is

```
H = [  0.7   0.4   0.1  −0.2 ]
    [  0.4   0.3   0.2   0.1 ]
    [  0.1   0.2   0.3   0.4 ]
    [ −0.2   0.1   0.4   0.7 ]
```

Its diagonal, the leverages (0.7, 0.3, 0.3, 0.7), adds up to k = 2. The two end points have more than
twice the leverage of the middle two, because a line pivots about its centre.

## Matrix structure

`X` is tall and thin. It is dense for ordinary regression and sparse when most predictors are
indicator variables (categories, fixed effects). `XᵀX` is k × k, symmetric and positive semidefinite,
and positive definite exactly when the columns of X are independent. `H` is n × n, symmetric,
idempotent and of rank k. It is never formed for large n; its diagonal can be read from the rows of Q.

## What is computed

The careful method factors X = Q R with Householder reflections and solves R β̂ = Qᵀ y by back
substitution; R's `lm` does this. Other packages use the SVD, or a Cholesky factorization of XᵀX,
which is fast but inherits the pitfall below. With QR,
ŷ = Q Qᵀ y and h_ii = ‖row i of Q‖². Forming XᵀX and solving the normal equations is faster but loses
accuracy when the columns are nearly dependent, as the pitfall shows. Very large sparse problems use
iterative solvers such as LSQR.

## Why linear algebra is the right tool

The geometry answers questions that formulas alone obscure. Residuals sum to zero because the column
of 1s is in the subspace. Adding a predictor can never increase the residual sum of squares, because
it enlarges the subspace. A predictor that is a combination of others adds nothing, because it leaves
the subspace unchanged, and it makes β not unique, because X then has a null space. Leverage is a
property of X alone, so an influential design point can be spotted before any response is measured.
Even R² is a squared cosine: that of the angle between the centered data vector and the centered
fitted vector.

## Pitfall worth teaching

Solving the normal equations squares the difficulty of the problem. A measure of how close the columns
of X are to dependent is its condition number, the factor by which relative errors in the data can be
magnified in the answer. XᵀX has the square of X's condition number. Regress the worked example's y on
the calendar years 2001–2004 instead of 0–3, and the column of years is almost parallel to the column
of 1s. The condition number of X becomes about 3.6 million and that of XᵀX about 1.3 × 10¹³, close to
the limit of double-precision arithmetic, so the normal equations lose about 13 of the 16 significant
digits available. QR works with X directly, and for a fit with small residuals its accuracy depends
on the condition number of X rather than its square. Centering the predictor (using
years since 2000, or deviations from the mean) removes the problem, which is the linear-algebra reason
for statisticians' standard advice to center. The exactly dependent version is the dummy variable trap:
one indicator column per category plus an intercept makes X rank-deficient, and β̂ is not unique.

## Extensions

Weighted and generalized least squares change the inner product, so the projection is orthogonal in a
different geometry. Ridge regression adds a multiple of the identity to XᵀX. The SVD of X shows which
combinations of predictors are poorly determined and is the natural language for collinearity (Tier 2).
The same projection is used in other fields' vocabularies in the basis-fitting entry (fitting curves
with chosen basis functions), the Massey and Colley ranking entry (least squares on pairwise game
results), and the geodetic network adjustment entry, where least squares was invented. Recursive
least squares, which updates β̂ as data arrive, leads to the Kalman filter.
