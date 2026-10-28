---
id: 41
slug: polynomial-interpolation-and-change-of-basis
status: written
title: 'Polynomial interpolation: one polynomial, many bases, very different arithmetic'
short_title: Polynomial interpolation and change of basis
field_label: Numerical analysis, scientific computing, approximation theory
tier_note: 'interpolation is one square linear system in a polynomial space, and the monomial, Lagrange,
  Newton and Chebyshev forms are four bases for the same space. Measuring how badly a basis behaves uses
  the condition number, which is Tier 2.'
nav_field: Mathematics & Numerical Analysis
field: Mathematics
subfield: Numerical analysis
tier: 1
tier_ceiling: 2
prereq_beyond_la: ''
scalar_field: R
vector_space: 'P_d, the real polynomials of degree at most d, a vector space of dimension d + 1 whose
  vectors are functions. Interpolating at d + 1 distinct nodes is a linear map from P_d to R^(d+1) (a
  polynomial goes to its list of values), and it is invertible'
underlying_equations: 'Polynomial evaluation: the interpolant must satisfy p(x_i) = y_i at each node'
core_la_object: Vandermonde system in a polynomial vector space
la_concepts: basis and dimension of a function space; coordinates; change of basis; Vandermonde matrix;
  invertibility; triangular and diagonal systems; conditioning
primary_method: Barycentric Lagrange formula; Newton divided differences; Chebyshev nodes and basis
matrix_structure: dense Vandermonde (monomial basis), lower triangular (Newton basis), identity
  (Lagrange basis)
typical_size: 3-100 nodes
worked_example_size: a parabola through 3 points in three bases; conditioning of 8 to 20 nodes
terminology:
  nodes (interpolation points): the d + 1 distinct x-values where the polynomial must match the data
  interpolant: the unique element of P_d with the prescribed values at the nodes
  monomial (power) form: coordinates in the basis 1, x, x², …, x^d
  Lagrange form: coordinates in the basis that is dual to evaluation at the nodes, so the coordinates
    are the data values themselves
  Newton form and divided differences: coordinates in the basis 1, (x − x_0), (x − x_0)(x − x_1), …,
    computed by a triangular solve
  Chebyshev polynomials and nodes: a basis and a set of nodes for which the interpolation problem is
    well conditioned
  barycentric formula: a stable way to evaluate the Lagrange form
  Runge phenomenon: large oscillations of high-degree interpolants at equally spaced nodes
  Lebesgue constant: how much the interpolation map can amplify errors in the data
---

## Start here

Through two points there is exactly one straight line, and through three points (with different
x-values) exactly one parabola. In general, n points with different x-values determine exactly one
polynomial of degree n − 1 passing through all of them. Finding that polynomial is called
interpolation, and it sits underneath numerical integration, root finding, graphics, and the formulas
that let a computer estimate a derivative from a table of numbers.

The polynomial itself is unambiguous, but there are many ways to write it down. The familiar way is as
a sum of powers of x with coefficients. Another way chooses building-block polynomials so that the
coefficients turn out to be the data values themselves. A third adds one point at a time. They are all
the same polynomial, written in different coordinates.

Which way you choose has dramatic consequences on a computer. Written as powers of x, the coefficients
of a polynomial through twenty points can be so sensitive that rounding errors destroy every digit.
Written in a better choice of building blocks, the same polynomial can be computed to full accuracy.
Choosing the building blocks is choosing a basis, and that is the whole subject of this entry.

## The problem

Given d + 1 data points (x_0, y_0), …, (x_d, y_d) with distinct x_i, find the polynomial of degree at
most d that passes through all of them, represent it in a form that is accurate and cheap to evaluate,
and choose the nodes x_i, when one has that freedom, so that the answer is not overly sensitive to
errors in the data.

## Variables

| Symbol | Name | What it holds | Shape | Units |
|---|---|---|---|---|
| d | degree | highest power allowed | integer | — |
| x_0, …, x_d | nodes | distinct points where the data are given | d + 1 numbers | units of x |
| y_0, …, y_d | data values | values the polynomial must take at the nodes | (d + 1) × 1 | units of y |
| p | interpolant | the polynomial with p(x_i) = y_i | element of P_d | maps x units to y units |
| V | Vandermonde matrix | row i is (1, x_i, x_i², …, x_i^d) | (d + 1) × (d + 1) | mixed: column j has units of x^j |
| a | monomial coefficients | p(x) = a_0 + a_1 x + … + a_d x^d | (d + 1) × 1 | a_j in y units per x^j |
| ℓ_0, …, ℓ_d | Lagrange basis | ℓ_j(x_i) = 1 if i = j and 0 otherwise | elements of P_d | dimensionless |
| c | Newton coefficients | p(x) = c_0 + c_1 (x − x_0) + c_2 (x − x_0)(x − x_1) + … | (d + 1) × 1 | mixed |
| T_j | Chebyshev polynomials | T_j(cos θ) = cos(j θ) | elements of P_d | dimensionless |

## Formulation

**Where the equations come from.** The conditions are that a
polynomial takes given values at given points, and each condition is linear in the polynomial.

**The space and the map.** The polynomials of degree at most d form a vector space P_d of dimension
d + 1: they can be added and scaled, and 1, x, …, x^d is a basis. Evaluating at the nodes,

```
p  ↦  (p(x_0), p(x_1), …, p(x_d))
```

is a linear map from P_d to ℝ^(d+1). Both spaces have dimension d + 1, and a nonzero polynomial of
degree at most d has at most d roots, so the only polynomial sent to zero is the zero polynomial. The
map is therefore invertible, and every set of data values has exactly one interpolant.

**The monomial basis gives a Vandermonde system.** Writing p in powers of x turns the conditions into

```
V a = y
```

with det V = Π_(i<j) (x_j − x_i), nonzero exactly when the nodes are distinct.

**The Lagrange basis gives the identity.** The basis polynomials

```
ℓ_j(x) = Π_(m ≠ j) (x − x_m) / (x_j − x_m)
```

are 1 at node j and 0 at the others. In this basis the matrix of the evaluation map is the identity,
so the coordinates of p are the data values: p = y_0 ℓ_0 + … + y_d ℓ_d. Nothing needs to be solved.

**The Newton basis gives a triangular system.** Each Newton basis polynomial vanishes at all earlier
nodes, so the matrix is lower triangular, and the coefficients (the divided differences) come from
forward substitution. Adding a new node adds a row and a column without changing the earlier
coefficients.

**Worked case: a parabola through (0, 1), (1, 3), (2, 2).** In the monomial basis, the three
conditions p(0) = 1, p(1) = 3, p(2) = 2 are the Vandermonde system

```
[ 1  0  0 ] [ a_0 ]   [ 1 ]
[ 1  1  1 ] [ a_1 ] = [ 3 ]          so   a = (1, 3.5, −1.5)   and   p(x) = 1 + 3.5x − 1.5x²
[ 1  2  4 ] [ a_2 ]   [ 2 ]
```

The other two bases give the same polynomial with no dense solve:

```
Newton:    c_0 = 1,  c_1 = (3 − 1)/(1 − 0) = 2,  c_2 = ((2 − 3)/(2 − 1) − 2)/(2 − 0) = −1.5
           p(x) = 1 + 2x − 1.5 x(x − 1)
Lagrange:  p(x) = 1·ℓ_0(x) + 3·ℓ_1(x) + 2·ℓ_2(x)
```

Expanding the Newton or Lagrange form gives back the monomial coefficients: three coordinate vectors
for one element of P_2.

## Matrix structure

The same linear map has a dense matrix in the monomial basis, a lower-triangular one in the Newton
basis, and the identity in the Lagrange basis. The change-of-basis matrices between them are dense. With
Chebyshev polynomials as the basis and Chebyshev points x_i = cos((2i + 1)π / (2d + 2)) as the nodes,
the matrix has orthogonal columns, and its condition number is √2 whatever the number of nodes.

## What is computed

Practical codes avoid the Vandermonde system altogether. They evaluate the Lagrange form with the
barycentric formula, which costs O(d) per point once O(d²) weights are computed and is numerically
stable, or build the Newton form when nodes arrive one at a time. For approximating a function on an
interval they use Chebyshev points and coefficients, as the Chebfun system does, computed with the fast
cosine transform.

## Why linear algebra is the right tool

Existence and uniqueness of the interpolant are a dimension count: an injective linear map between
spaces of the same finite dimension is invertible. The various interpolation formulas taught as
separate recipes are coordinates of one vector in different bases, and the work each requires is
visible in the shape of its matrix: dense, triangular or diagonal. The numerical trouble with
high-degree interpolation is a property of the basis and the nodes, not of the polynomial, which is
why it can be cured by changing them.

## Pitfall worth teaching

The monomial basis is a poor basis on a computer even though it is the one everyone learns. On [0, 1]
the functions x^6 and x^7 are nearly indistinguishable, so the columns of V are nearly parallel. With
8 equally spaced nodes on [0, 1] the condition number of V is about 2.7 × 10⁵, with 16 about
3 × 10¹², and with 20 about 10¹⁶, at which point a double-precision solve can lose every digit. The
interpolating polynomial is perfectly well defined throughout; only its monomial coordinates are
unstable. Changing the basis to Chebyshev polynomials at Chebyshev nodes brings the condition number
down to √2 for any number of nodes. A second, separate failure is the Runge phenomenon: at equally
spaced nodes, high-degree interpolants of perfectly smooth functions oscillate wildly near the ends of
the interval, whichever basis is used. That one is cured by moving the nodes, not by changing the basis.

## Extensions

Least-squares fitting with more points than coefficients is the basis-fitting entry, and the same
Vandermonde matrix appears there as a design matrix. Shamir secret sharing interpolates over GF(p),
where there is no rounding and the conditioning problem disappears. Finite-difference stencils solve a
small Vandermonde system for derivative weights. Bézier curves use the Bernstein basis of the same
polynomial space. Splines interpolate with piecewise polynomials and avoid the Runge phenomenon.
Gaussian quadrature chooses its nodes as the roots of orthogonal polynomials, and the Lebesgue constant
measures how much a choice of nodes can amplify data errors.
