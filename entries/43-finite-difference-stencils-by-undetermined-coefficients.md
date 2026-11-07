---
id: 43
slug: finite-difference-stencils-by-undetermined-coefficients
status: written
title: 'Finite-difference stencils: derivative formulas from a small linear system'
short_title: Finite-difference stencils by undetermined coefficients
field_label: Numerical analysis, scientific computing, computational physics and engineering
tier_note: 'the weights of a derivative formula solve one small square system, a transposed Vandermonde
  matrix whose rows say the formula is exact on 1, x, x², …. Using the stencils to discretize a
  differential equation is Tier 3.'
nav_field: Mathematics & Numerical Analysis
field: Mathematics
subfield: Numerical analysis
tier: 1
tier_ceiling: 3
prereq_beyond_la: Taylor series
scalar_field: R
vector_space: 'R^n, the n weights of a stencil. A stencil is a linear functional (samples in, one
  number out), and the conditions ask it to agree with the k-th derivative on a basis of P_(n−1), the
  polynomials of degree below n'
underlying_equations: 'Taylor-series matching conditions: the weights c_j must satisfy Σ_j c_j s_j^m = k!
  for m = k and 0 for the other m below n, so that the formula is exact for every polynomial of degree
  below n'
core_la_object: Small Vandermonde solve for derivative weights
la_concepts: linear functionals; Taylor constraints as linear equations; transposed Vandermonde system;
  basis of a polynomial space; exactness on a subspace; banded Toeplitz matrices
primary_method: Dense small solve; Fornberg's recursive algorithm for general offsets
matrix_structure: dense transposed Vandermonde, n × n, for the weights; the stencil applied across a
  grid is a banded Toeplitz matrix (tridiagonal for three points)
typical_size: 3-9 points per stencil; the grid operator has 1e3-1e9 rows
worked_example_size: 3-point and 5-point second-derivative stencils derived from scratch
terminology:
  grid and grid spacing h: equally spaced points x + s h at which the function is known
  offset s_j: the position of a sample, counted in grid steps from the point x where the derivative is
    wanted
  stencil: a list of offsets and weights; the estimate is the weighted sum of the samples
  method of undetermined coefficients: writing the weights as unknowns and solving the conditions they
    must satisfy
  order of accuracy: the power p in an error proportional to h^p
  truncation error: the error from cutting off the Taylor series, present even in exact arithmetic
  central, forward and one-sided differences: stencils whose offsets are symmetric about x, start at x,
    or lie on one side of it
  rounding (cancellation) error: the loss of digits when nearly equal sample values are subtracted
  Fornberg's algorithm: a recursion that produces the weights for any offsets and derivative orders
    without forming the matrix
---

## Start here

A computer that knows a function only through its values at evenly spaced points cannot differentiate
it the way calculus does. It estimates the derivative from the values it has. The estimate everyone
meets first is the slope between two neighbouring points: the change in height divided by the step.

Every such estimate combines a few neighbouring values with fixed weights. The pattern of weights,
laid over the grid of points like a stencil over paper, is called a finite-difference stencil.
Stencils are the basic tool for turning the laws of physics into arithmetic, in weather and climate
models, in simulations of heat flow and fluid flow, and in the edge detectors of image processing.

Tables of stencils contain formulas such as (1, −2, 1) for a second derivative, or the less obvious
(−1, 16, −30, 16, −1)/12. They need not be memorized, because each one is the solution of a small
linear system. Ask the formula to give the right answer for the functions 1, x, x², … in turn, and the
weights are forced. The same few lines of linear algebra produce a formula for any derivative, from
any set of points.

## The problem

The function f is known on a **grid**: the points x + s h, where h is the **grid spacing** and s is a
whole number of steps. A **stencil** for the k-th derivative at x is a set of **offsets** s_1, …, s_n,
which name the grid points used, together with **weights** w_1, …, w_n. Its estimate is

```
f^(k)(x)  ≈  w_1 f(x + s_1 h) + w_2 f(x + s_2 h) + … + w_n f(x + s_n h)
```

For example, the three-point central stencil uses offsets −1, 0, 1: the point x itself and its two
neighbours. A stencil has **order of accuracy** p when its error shrinks like h^p as the grid is
refined.

Given the derivative order k and the offsets, find the weights that make the estimate as accurate as
possible, find its order of accuracy, and choose a grid spacing h that gives a useful answer on a
computer.

## Variables

| Symbol | Name | What it holds | Shape | Units |
|---|---|---|---|---|
| f | function | the function being differentiated | known only at grid points | units of f |
| x | evaluation point | where the derivative is wanted | number | units of x |
| h | grid spacing | distance between neighbouring grid points | number | units of x |
| k | derivative order | 1 for a first derivative, 2 for a second | integer | — |
| n | stencil size | number of grid points used | integer | — |
| s_j | offsets | position of sample j, in grid steps from x | n numbers | dimensionless |
| w_j | weights | multiplier of the sample f(x + s_j h) | n × 1 | per (units of x)^k |
| c_j | scaled weights | w_j = c_j / h^k, independent of h | n × 1 | dimensionless |
| m | power | index of the condition: exactness on x^m | 0, 1, …, n − 1 | — |
| M | moment matrix | M_mj = s_j^m | n × n | dimensionless |
| r | right-hand side | k! in position m = k, 0 elsewhere | n × 1 | dimensionless |
| p | order of accuracy | the error is proportional to h^p | integer | — |

## Formulation

**Where the equations come from.** The equations are Taylor's theorem applied to each sample. Near x,

```
f(x + s h)  =  f(x)  +  s h f'(x)  +  (s h)²/2! f''(x)  +  (s h)³/3! f'''(x)  +  …
```

so every sample is a known combination of the derivatives of f at x. The estimate is a combination
of samples, so it is also a combination of derivatives, and the coefficients of that combination are
linear in the weights.

**The familiar formula.** The definition of the derivative suggests f'(x) ≈ (f(x + h) − f(x)) / h, the
forward difference, with offsets 0 and 1 and weights −1/h and 1/h. Taylor's theorem shows its error:

```
(f(x + h) − f(x)) / h  =  f'(x)  +  (h/2) f''(x)  +  …
```

The error is proportional to h, so the forward difference is first-order accurate. It is the simplest
case of the system below.

**One condition at a time.** Write each weight as w_j = c_j / h^k, so that the scaled weights c_j do
not depend on h. Substituting the Taylor series into the estimate and collecting the terms that
contain f^(m)(x) gives

```
Σ_j c_j f(x + s_j h) / h^k  =  Σ_m  ( Σ_j c_j s_j^m )  h^(m−k)  f^(m)(x) / m!
```

The bracket for each m is a single number fixed by the weights. For the right side to equal f^(k)(x),
the bracket must be k! when m = k, which leaves exactly f^(k)(x). For m below k it must be 0, because
those terms carry negative powers of h and would blow up as the grid is refined. For m above k it
should be 0 as far as possible, because each surviving term adds an error proportional to h^(m−k).

Each condition has a plain meaning. Apply the stencil to the polynomial g(t) = (t − x)^m: the samples
are (s_j h)^m, so the estimate is h^(m−k) times the bracket, while the true k-th derivative of g at x
is k! when m = k and 0 otherwise. Condition m says that **the stencil is exact on the m-th power**. The
condition for m = 0, Σ c_j = 0, says that the estimate of a derivative of a constant is zero.

**Stacking the conditions.** With n weights there is room for n conditions, m = 0, 1, …, n − 1:

```
M c = r,      M_mj = s_j^m,      r_m = k!  if m = k,  0 otherwise
```

M is the transpose of the Vandermonde matrix of the polynomial-interpolation entry, with the offsets
as nodes. It is invertible whenever the offsets are distinct, so the weights exist and are unique.
There is a cleaner way to see what the solution achieves. The k-th derivative at x and the stencil
are both linear functionals: each takes a function and returns one number, and each respects sums
and multiples. Two linear functionals that agree on a basis agree on the whole space. The conditions
make them agree on the basis 1, (t − x), …, (t − x)^(n−1), so the stencil is exact for every polynomial
of degree below n. Equivalently, the stencil computes the k-th derivative of the polynomial that
interpolates the n samples.

**Worked case: three points, second derivative.** Take offsets −1, 0, 1 and k = 2, so n = 3 and
2! = 2. The three conditions, written as scalar equations, are

```
m = 0:    c_(−1) + c_0 + c_1  =  0
m = 1:   −c_(−1)       + c_1  =  0
m = 2:    c_(−1)       + c_1  =  2
```

and as a matrix product they are

```
[  1   1   1 ] [ c_(−1) ]   [ 0 ]
[ −1   0   1 ] [ c_0    ] = [ 0 ]
[  1   0   1 ] [ c_1    ]   [ 2 ]
```

The last two rows give c_(−1) = c_1 = 1, and the first row then gives c_0 = −2. The stencil is

```
f''(x)  ≈  ( f(x − h) − 2 f(x) + f(x + h) ) / h²
```

The conditions that were not imposed show the accuracy. For m = 3 the bracket is −1 + 1 = 0, a free
bonus of the symmetric offsets. For m = 4 it is 1 + 1 = 2, so the leading error is
(2/4!) h² f''''(x) = (h²/12) f''''(x), and the stencil is second-order accurate.

**Worked case: five points.** With offsets −2, −1, 0, 1, 2 and k = 2 the system is

```
[  1   1   1   1   1 ] [ c_(−2) ]   [ 0 ]
[ −2  −1   0   1   2 ] [ c_(−1) ]   [ 0 ]
[  4   1   0   1   4 ] [ c_0    ] = [ 2 ]
[ −8  −1   0   1   8 ] [ c_1    ]   [ 0 ]
[ 16   1   0   1  16 ] [ c_2    ]   [ 0 ]
```

Reversing the offsets turns any solution into another solution, and the solution is unique, so it is
symmetric: c_(−2) = c_2 = a and c_(−1) = c_1 = b. The rows for m = 1 and m = 3 then hold automatically.
The rows for m = 2 and m = 4 become 8a + 2b = 2 and 32a + 2b = 0, so a = −1/12 and b = 4/3, and the
first row gives c_0 = −2a − 2b = −5/2. Over a common denominator the weights are
(−1, 16, −30, 16, −1)/12, the formula from the table. The bracket for m = 5 vanishes by symmetry and the
one for m = 6 is −8, so the leading error is (−8/6!) h⁴ f⁽⁶⁾(x) = −(h⁴/90) f⁽⁶⁾(x): fourth order.

## Matrix structure

M is a small dense n × n matrix. Its determinant is Π_(i<j) (s_j − s_i), which is 288 for the
five-point stencil, and its condition number, about 42 there, grows with n. For the stencil sizes used
in practice this is harmless.

The weights depend on where the offsets sit relative to x, not only on their spacing. Offsets 0, 1, 2
give the same weights (1, −2, 1), but now the estimate is of f'' at the left end point. The bracket for
m = 3 is 6 rather than 0, and the formula is only first-order accurate.

Applying one stencil at every grid point gives a matrix with the weights running down its diagonals,
a banded Toeplitz matrix. For the three-point second derivative on four interior grid points, with the
function taken to be zero at the two ends, it is

```
          [ −2   1   0   0 ]
D = 1/h²  [  1  −2   1   0 ]
          [  0   1  −2   1 ]
          [  0   0   1  −2 ]
```

This sparse matrix is what a simulation code builds when it discretizes a differential equation.

## What is computed

Stencils on uniform grids are derived once and tabulated. For arbitrary offsets, such as non-uniform
grids or one-sided stencils at a boundary, Fornberg's algorithm (1988) computes the weights for every
derivative order up to k at once by a recursion, without forming M. Libraries expose both: Python's
findiff package returns the coefficients for a requested derivative and accuracy, Julia's
FiniteDifferences.jl builds stencils such as central_fdm(5, 2), and NumPy's gradient function applies
the second-order central difference for first derivatives at interior points.

## Why linear algebra is the right tool

Every entry in a table of stencils is the solution of a linear system, and the method of undetermined
coefficients replaces the table by one recipe that works for any derivative and any offsets. The
existence and uniqueness of the weights are the invertibility of a Vandermonde matrix. The order of
accuracy is a count of how many conditions hold, which is the dimension of the space of polynomials on
which the stencil is exact. And the reason exactness on a few powers of x is enough is that the
derivative and the stencil are linear functionals, so agreement on a basis is agreement on the span.

## Pitfall worth teaching

A smaller grid spacing is not always more accurate. Estimate f'' for f(x) = e^x at x = 0, where the
true value is 1, with the three-point stencil. In double precision the error is about 8.3 × 10⁻⁴ at
h = 0.1, 8.3 × 10⁻⁶ at h = 0.01 and 8.3 × 10⁻⁸ at h = 0.001, falling by 100 at each step exactly as
h²/12 predicts. At h = 10⁻⁴ it is about 6 × 10⁻⁹, and then it rises: about 8 × 10⁻⁸ at h = 10⁻⁵,
1.3 × 10⁻⁴ at h = 10⁻⁶ and 8 × 10⁻⁴ at h = 10⁻⁷.

The cause is built into the linear algebra. The m = 0 condition makes the weights sum to zero, so the
stencil subtracts nearly equal numbers. Each sample carries a relative rounding error of about
ε ≈ 2.2 × 10⁻¹⁶, the numerator therefore carries an error of a few ε, and dividing by h² magnifies it
to about 4ε/h². The total error is roughly h²/12 + 4ε/h², which is smallest near h = (48ε)^(1/4), about
3 × 10⁻⁴, and even there only about half of the sixteen available digits are correct. A higher-order
stencil does better at a larger h: the five-point formula reaches an error of about 10⁻¹⁰ at h = 0.01.
Noise in measured data is far larger than ε, which pushes the best h up further and is why
derivatives of measured data are usually estimated by fitting before differencing.

## Extensions

Applying D to the unknown values of a function turns a differential equation, such as the heat or
Poisson equation, into a large sparse linear system (Tier 3), and the eigenvalues of D, known in
closed form, govern the stability of time-stepping schemes (Tier 2). Richardson extrapolation combines
estimates at two grid spacings to cancel the leading error term, the same idea applied to the error
instead of the samples. Replacing differentiation by integration in the conditions gives quadrature
weights, such as Simpson's rule, from the same transposed Vandermonde system. The polynomial
interpolation entry solves the untransposed system, and Shamir secret sharing solves one over a finite
field. Savitzky–Golay filters estimate derivatives of noisy data from a local least-squares fit,
which is the basis-fitting entry applied in a sliding window. The complex-step derivative,
Im f(x + ih)/h, avoids the subtraction altogether for first derivatives of analytic functions.
