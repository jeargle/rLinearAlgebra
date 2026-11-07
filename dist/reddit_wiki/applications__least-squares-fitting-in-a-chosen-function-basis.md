# Least-squares fitting in a chosen basis: the span is the model, the basis is the arithmetic

### Start here

Fitting a straight line to data is the regression entry. Many data sets are not straight: a population
grows, temperatures rise and fall with the seasons, a spectrum has peaks. The standard approach picks
a family of building-block functions, such as powers of t, sines and cosines, or smoothly joined pieces
of cubics, and looks for the combination of them that comes closest to the data.

The surprising part is that a curved fit uses exactly the same linear algebra as a straight line.
The unknowns are the amounts of each building block, and those enter the fitted curve linearly, even
though the blocks themselves are curved. The word linear in linear [least squares](https://en.wikipedia.org/wiki/Least_squares) refers to the
coefficients, not to the shape of the curve.

The real decision is which building blocks to use. That choice decides which curves the fit can
produce at all, how accurately a computer can find the coefficients, and how the fitted curve behaves
away from the data, where the data have no say.

**Field:** Statistics, data analysis, curve fitting in every experimental science, signal processing  
**Tier:** 1 — each choice of basis functions gives a [design matrix](https://en.wikipedia.org/wiki/Design_matrix), and fitting is the [orthogonal projection](https://en.wikipedia.org/wiki/Projection_%28linear_algebra%29) of the data onto its column space. Diagnosing a poorly determined fit with the [singular value decomposition](https://en.wikipedia.org/wiki/Singular_value_decomposition), or measuring how a basis amplifies noise, is Tier 2.  
**Scalar field:** R  
**Vectors:** three spaces: the k-dimensional function space spanned by the chosen basis functions (the possible models), the coefficients in R^k (the coordinates of a model in that basis), and the data in R^n. Evaluating the basis functions at the n data points maps R^k into R^n, and the image is the column space of the design matrix  
**Underlying equations:** A statistical model, y_i = c_1 φ_1(t_i) + … + c_k φ_k(t_i) + noise, fitted by minimizing the sum of squared residuals

### The problem

The data are n points (t_1, y_1), …, (t_n, y_n). The **basis functions** φ_1, …, φ_k are fixed functions
of t, chosen in advance, with k smaller than n. A candidate curve is a combination

```
p(t)  =  c_1 φ_1(t)  +  c_2 φ_2(t)  +  …  +  c_k φ_k(t)
```

The known quantities are the data t_i and y_i and the basis functions; the unknowns are the
coefficients c_1, …, c_k. The **design matrix** X has one row per data point and one column per basis
function, with X_ij = φ_j(t_i). For example, with the basis 1, t, t² for a parabola, the row for a
data point at t = 2 is (1, 2, 4).

Choose a basis, find the coefficients that minimize the sum of squared residuals
Σ_i (y_i − p(t_i))², and judge whether the fitted curve can be trusted, inside and outside the range
of the data.

### Variables

| Symbol | Name | What it holds | Shape | Units |
|---|---|---|---|---|
| t_i | data positions | where the measurements were taken, often times | n numbers | units of t |
| y_i | data values | the measurements | n × 1 vector y | units of y |
| n | number of data points | rows of X | integer | — |
| k | number of basis functions | columns of X | integer, k < n | — |
| φ_j | basis functions | fixed functions chosen in advance | k functions | dimensionless |
| c | coefficients | p = c_1 φ_1 + … + c_k φ_k | k × 1 | units of y |
| p | fitted curve | the combination with the best coefficients | function of t | units of y |
| X | design matrix | X_ij = φ_j(t_i) | n × k | dimensionless |
| ŷ | fitted values | p(t_i) at the data points, ŷ = X ĉ | n × 1 | units of y |
| e | residuals | e = y − ŷ | n × 1 | units of y |
| B | change-of-basis matrix | expresses one basis in terms of another | k × k, invertible | dimensionless |
| u | rescaled position | u = 2t − 3 in the worked case | number | dimensionless |

### Formulation

**Where the equations come from.** The model is a statistical assumption: each measurement is the
value of some curve in the model space plus random noise,

```
y_i  =  c_1 φ_1(t_i)  +  …  +  c_k φ_k(t_i)  +  noise
```

and the coefficients are chosen to minimize the sum of squared residuals.

**The familiar case.** The line of best fit is the basis 1, t, with coefficients the intercept and
the slope. Its formulas, worked out in the regression entry, are the two-column case of everything
below.

**One row at a time.** The fitted value at the i-th data point is

```
p(t_i)  =  c_1 φ_1(t_i)  +  …  +  c_k φ_k(t_i)  =  ( φ_1(t_i), …, φ_k(t_i) ) · c
```

the dot product of row i of X with the coefficient vector. Stacking the n rows gives X c, and the fit
asks for X c ≈ y. Column j of X is the basis function φ_j sampled at the data points, so the column
space of X is the set of all curves in the model space, as seen at the data points. The fit is the
orthogonal projection of y onto that column space, and it satisfies the normal equations

```
Xᵀ X ĉ  =  Xᵀ y
```

Entry (j, l) of XᵀX is Σ_i φ_j(t_i) φ_l(t_i), a sampled version of the inner product of functions in
the Fourier series entry.

**Same span, different basis.** If a second basis is related to the first by an invertible matrix B,
its design matrix is X B. That matrix has the same column space as X, so the projection is the same:
the same fitted values ŷ, the same residuals e, the same curve p. Only the coordinates change, and
they are related by B. Changing the basis changes the arithmetic: how well conditioned XᵀX is, and
whether it is diagonal. Changing the span changes the model, and with it the fit.

**Worked case: a parabola through four points, in two bases.** The data are (0, 1), (1, 2), (2, 2),
(3, 5). In the basis 1, t, t² the design matrix and the normal equations are

```
    [ 1  0  0 ]
X = [ 1  1  1 ]          [  4   6  14 ] [ c_1 ]   [ 10 ]
    [ 1  2  4 ]          [  6  14  36 ] [ c_2 ] = [ 21 ]
    [ 1  3  9 ]          [ 14  36  98 ] [ c_3 ]   [ 55 ]
```

Solving the dense 3 × 3 system gives ĉ = (1.2, −0.3, 0.5), so p(t) = 1.2 − 0.3t + 0.5t².

Now centre and scale the positions with u = 2t − 3, which takes the values −3, −1, 1, 3, and use the
basis 1, u, u² − 5. The three columns are (1, 1, 1, 1), (−3, −1, 1, 3) and (4, −4, −4, 4), and every pair
of them has dot product zero. The normal equations become diagonal:

```
[ 4   0   0 ] [ c_1 ]   [ 10 ]
[ 0  20   0 ] [ c_2 ] = [ 12 ]          so   ĉ = (2.5, 0.6, 0.125)
[ 0   0  64 ] [ c_3 ]   [  8 ]
```

Each coefficient is one division. Substituting u = 2t − 3 gives
2.5 + 0.6(2t − 3) + 0.125(4t² − 12t + 4) = 1.2 − 0.3t + 0.5t², the same parabola. In either basis the
fitted values are (1.2, 1.4, 2.6, 4.8) and the residuals are (−0.2, 0.6, −0.6, 0.2), which are
orthogonal to all three columns. The functions 1, u and u² − 5 are [orthogonal polynomials](https://en.wikipedia.org/wiki/Orthogonal_polynomials) for these four
points, the discrete counterpart of the orthogonal sines and cosines of the Fourier series entry.

**Different spans.** Take 50 equally spaced points on [0, 1] and three bases of 5 functions each: the
polynomials 1, t, …, t⁴; cubic [B-splines](https://en.wikipedia.org/wiki/B-spline) with one knot at t = 0.5; and the Fourier basis 1, cos 2πt,
sin 2πt, cos 4πt, sin 4πt. Fit two noise-free signals: a seasonal cycle over one year,
s(t) = 10 − 8 cos 2πt + 2 sin 4πt, and exponential growth, g(t) = e^t. The [root-mean-square](https://en.wikipedia.org/wiki/Root_mean_square) residuals are

| Signal | Polynomial | Spline | Fourier |
|---|---|---|---|
| seasonal cycle s | 1.2 | 1.2 | 3 × 10⁻¹⁵ |
| growth g | 1.8 × 10⁻⁵ | 4.9 × 10⁻⁵ | 0.27 |

The seasonal signal lies in the Fourier span, so the Fourier fit reproduces it to rounding error,
while the other two bases cannot follow its second harmonic. Growth is the opposite. Every Fourier
basis function takes the same value at t = 0 and t = 1, but e^0 ≠ e^1, and the Fourier fit has its
largest error, 0.89, at the ends: the [Gibbs phenomenon](https://en.wikipedia.org/wiki/Gibbs_phenomenon) of the Fourier series entry, at the seam.

### Matrix structure

X is tall and thin. It is dense for polynomial and Fourier bases and banded for B-splines, where each
basis function is nonzero over at most four knot intervals, so each row of X has at most four
nonzeros. The [condition number](https://en.wikipedia.org/wiki/Condition_number) of X on the 50 points is about 643 for the polynomials, 5.2 for the
B-splines and 1.4 for the Fourier basis. For the same polynomials evaluated at raw calendar years
2000 to 2049 it is about 10²², far beyond double precision, although the model space is identical.
When the basis is orthogonal on the data points, XᵀX is diagonal, as in the worked case.

### What is computed

General-purpose software fits with a [QR](https://en.wikipedia.org/wiki/QR_decomposition) factorization of X, or the SVD when X may be [rank-deficient](https://en.wikipedia.org/wiki/Rank_%28linear_algebra%29),
rather than forming XᵀX. The libraries also change the basis for the user. R's poly() builds
orthogonal polynomials for the given data points, the second basis of the worked case. NumPy's
Polynomial.fit maps the data range onto [−1, 1] before fitting. SciPy's make_lsq_spline fits a B-spline
basis by least squares.

### Why linear algebra is the right tool

Because the coefficients enter linearly, a fit with curved basis functions is an orthogonal projection,
and everything the regression entry says about projections carries over. The residuals are
orthogonal to every basis function, adding a basis function can never increase the residual sum of
squares, and a basis function that is a combination of the others adds nothing. Most usefully, the
distinction between a basis and its span separates two decisions that are easy to confuse. The span
decides what the model can represent and therefore what the fit is. The basis decides only how well
the computer can find the coefficients.

### Pitfall worth teaching

A small residual inside the data says nothing about the curve outside it, and using a fitted curve
beyond the range of the data is called [extrapolation](https://en.wikipedia.org/wiki/Extrapolation). Extend the two fits above half a period beyond the
data, to t = 1.5. For the seasonal cycle, the true value is 18 and the Fourier fit gives 18, but the
degree-4 polynomial fit, which has a residual of only 1.2 inside the data, gives about 176. For growth,
the true value is e^1.5 ≈ 4.48 and the polynomial fit gives 4.47, but the Fourier fit gives 1.66,
because it repeats with period 1 and so returns to its values near t = 0.5.

Outside the data, the fitted curve is decided entirely by the basis. Polynomials run off towards
infinity, Fourier sums repeat, and splines continue their last cubic piece. Choosing a basis is
choosing an assumption about how the signal behaves where nothing was measured. A related trap is
that adding basis functions always lowers the residual, because it enlarges the span, so a smaller
residual is not evidence of a better model. The usual check is to hold some data back and compare
the fits on the points they did not see.

### Extensions

[Smoothing splines](https://en.wikipedia.org/wiki/Smoothing_spline) and [ridge regression](https://en.wikipedia.org/wiki/Ridge_regression) add a penalty on the coefficients, which keeps a large basis
from [overfitting](https://en.wikipedia.org/wiki/Overfitting). [Weighted least squares](https://en.wikipedia.org/wiki/Weighted_least_squares) changes the inner product on the data. With as many basis
functions as data points the fit becomes [interpolation](https://en.wikipedia.org/wiki/Polynomial_interpolation), and with the monomial basis the design matrix
becomes the [Vandermonde](https://en.wikipedia.org/wiki/Vandermonde_matrix) matrix of the polynomial interpolation entry. The Fourier series entry is the
continuous version, with the sum over data points replaced by an integral. [Savitzky–Golay](https://en.wikipedia.org/wiki/Savitzky%E2%80%93Golay_filter) filters fit a
low-degree polynomial in a sliding window, which gives smoothed derivatives in the spirit of the
finite-difference entry. Records with both a trend and a cycle are fitted in mixed bases: a common
model for the [Mauna Loa carbon-dioxide record](https://en.wikipedia.org/wiki/Keeling_Curve) combines a polynomial trend with a few annual harmonics.
When the unknowns sit inside the basis functions, such as an unknown frequency or decay rate, the
problem becomes [nonlinear least squares](https://en.wikipedia.org/wiki/Non-linear_least_squares). The Massey and Colley ranking entry and the geodetic network
adjustment entry use the same projection in other fields' vocabularies.

### Terminology

How this field's vocabulary reads as linear algebra.

| Domain term | In linear algebra |
|---|---|
| basis functions | fixed functions of t, chosen before seeing the coefficients, whose combinations are the candidate curves |
| design matrix | the matrix whose column j is basis function j evaluated at every data point |
| model space | the span of the basis functions, every curve the fit could produce |
| linear least squares | least squares in which the coefficients enter linearly, whatever the shape of the basis functions |
| orthogonal polynomials (for a set of points) | polynomials whose sampled values are orthogonal, so that the design matrix has orthogonal columns |
| B-splines and knots | piecewise-cubic basis functions joined smoothly at chosen points called knots, each nonzero over only a few intervals |
| Fourier basis | a constant together with sines and cosines of whole-number multiples of a fundamental frequency |
| extrapolation | using a fitted curve outside the range of the data |
| overfitting | fitting the noise in the data by using too many basis functions |

---

[Back to the index](/r/LinearAlgebra/wiki/applications)
