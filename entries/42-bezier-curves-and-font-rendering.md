---
id: 42
slug: bezier-curves-and-font-rendering
status: written
title: 'Bézier curves: every letter on the screen is a point in a polynomial space'
short_title: Bezier curves and font rendering
field_label: Typography, vector graphics, computer-aided design, animation
tier_note: 'a Bézier curve is a polynomial written in a particular basis, and every common operation on
  it is a change of basis or a linear map between polynomial spaces of degree at most 3. No eigenvalues
  and no differential equations are involved.'
nav_field: Computer Graphics & Vision
field: Computer Science
subfield: Typography/vector graphics
tier: 1
tier_ceiling: 1
prereq_beyond_la: ''
scalar_field: R
vector_space: 'P_3, the real polynomials of degree at most 3 in a parameter t, which has dimension 4.
  Each coordinate x(t) and y(t) of a cubic curve is one element of P_3, so a planar cubic segment is a
  pair of them, a vector in P_3 × P_3 of dimension 8. The control points are its coordinates in the
  Bernstein basis, not points the curve passes through. TrueType fonts use quadratic segments, in P_2
  (dimension 3)'
underlying_equations: 'None: polynomial curves written in a chosen basis'
core_la_object: Bernstein basis of a polynomial space
la_concepts: basis of a function space; change of basis; coordinates; partition of unity; affine
  combinations; inclusion of subspaces (degree elevation); linear maps between polynomial spaces
primary_method: Basis-change matrix; de Casteljau evaluation and subdivision
matrix_structure: dense 4 × 4, lower triangular in the monomial-Bernstein change of basis
typical_size: 4 × 4 per segment; thousands of segments per font
worked_example_size: one cubic segment that is secretly quadratic; conversion to the monomial basis;
  subdivision at t = 1/2
terminology:
  raster image (bitmap): a vector in R^(width × height), one coordinate per pixel, so its resolution is
    fixed by the dimension
  vector graphics: shapes stored as coordinates in a polynomial space, evaluated at whatever resolution
    the output needs
  rasterization: sampling the curves onto a pixel grid, a map from the polynomial space into R^(width ×
    height)
  control points: coordinates of the curve in the Bernstein basis, one point in the plane per basis
    polynomial
  on-curve and off-curve points (font editors): the end control points, which the curve passes through,
    and the inner control points, which it generally does not
  control polygon: the broken line through the control points; the curve lies in its convex hull
  Bernstein polynomials: a basis of P_3 consisting of nonnegative functions that sum to 1
  cubic vs quadratic outlines (CFF/PostScript vs TrueType): curves in P_3 vs curves in P_2
  degree elevation: the inclusion P_2 → P_3, written in Bernstein coordinates
  de Casteljau algorithm: evaluation by repeated linear interpolation
  subdivision (splitting a curve): change of basis to the Bernstein basis of a subinterval
  affine invariance: transforming the control points transforms the curve, because the basis sums to 1
  easing curve (CSS cubic-bezier): a cubic in the same basis, used for timing instead of shape
---

## Start here

Every letter in a modern font is drawn from a short list of curved pieces. A designer does not store the
thousands of pixels in a letter "S"; the font file stores a few points, and the computer works out a
smooth curve from them at whatever size the letter is printed, from a phone screen to a billboard.

For each curved piece the font stores four points. The curve starts at the first and ends at the fourth.
The two middle points are not on the curve at all: they act like magnets that pull it towards themselves,
setting the direction in which it leaves the start and arrives at the end. Moving one of them reshapes
the curve smoothly, which is why the "handles" in a drawing program behave the way they do.

The mathematics underneath is that each piece is a polynomial of degree 3, and the four points are the
polynomial's coordinates in a well-chosen basis. The everyday operations of a font or drawing program —
scaling a letter, converting a font between formats, cutting a curve in two — all turn out to be changes
of basis or other linear maps between spaces of polynomials.

## The problem

An image can be stored in two fundamentally different ways. Raster graphics (photographs, PNG and
JPEG files, the screen itself) store a grid of pixels: a fixed number of samples of the picture,
taken at one resolution. Enlarge a raster image and nothing new can appear between the samples, so
each pixel just becomes a bigger square and edges turn jagged and blurry. Vector graphics (fonts, SVG
and PDF drawings, logos, CAD drawings) store the shapes themselves, as curves described by a few numbers
each. The picture is computed from those numbers only when it is shown, so it can be drawn at any
resolution, and a letter zoomed in a hundredfold is as sharp as it was at normal size. It is only turned into pixels
(rasterized) at the last moment, for the particular screen or printer in use.

Both kinds of image are vectors in the linear-algebra sense, but in different spaces. A raster image
is a point in ℝ^(width × height), one coordinate per pixel, and its resolution is fixed by the
dimension of that space. A vector-graphics curve is a point in a space of polynomials, which can be
evaluated at as many parameter values as the output needs.

The problem is to represent smooth curves (glyph outlines, vector illustrations, animation timing) in
that second way, as Bézier curves, and then to draw them at any resolution, transform them, split them,
and convert them between formats that use different polynomial degrees: exactly where possible, and
approximately otherwise.

## Variables

| Symbol | Name | What it holds | Shape | Units |
|---|---|---|---|---|
| t | parameter | position along the segment, from its start (t = 0) to its end (t = 1); not distance along the curve | scalar in [0, 1] | dimensionless |
| P_0, …, P_3 | control points | coordinates of the curve in the Bernstein basis | each a 2 × 1 point | font units (often 1/1000 or 1/2048 of the em size) |
| b_0, …, b_3 | Bernstein polynomials | b_k(t) = C(3, k) t^k (1 − t)^(3−k), the basis functions of P_3 | functions in P_3 | dimensionless |
| B(t) | the curve | B(t) = Σ b_k(t) P_k, the point drawn at parameter t | 2 × 1 for each t | font units |
| X | control-point matrix | the control points as rows, (P_0; P_1; P_2; P_3) | 4 × 2 | font units |
| M | change-of-basis matrix | converts Bernstein coordinates to monomial coefficients | 4 × 4 | dimensionless |
| a_0, …, a_3 | monomial coefficients | B(t) = a_0 + a_1 t + a_2 t² + a_3 t³ | each 2 × 1 | font units |
| Q_0, Q_1, Q_2 | quadratic control points | a TrueType segment, in the Bernstein basis of P_2 | each 2 × 1 | font units |

## Formulation

**Where the equations come from.** There is no differential equation. A segment is a polynomial curve,
and the modelling choice is only which basis to write it in.

**The Bernstein basis.** For cubics the basis polynomials are

```
b_0 = (1 − t)³,   b_1 = 3t(1 − t)²,   b_2 = 3t²(1 − t),   b_3 = t³
```

They are linearly independent, so they form a basis of the 4-dimensional space P_3. Each is
nonnegative on [0, 1], and by the binomial theorem they add up to ((1 − t) + t)³ = 1. The curve is

```
B(t) = b_0(t) P_0 + b_1(t) P_1 + b_2(t) P_2 + b_3(t) P_3
```

so its x-coordinate is the element of P_3 whose Bernstein coordinates are the four x-values of the
control points, and likewise for y. At t = 0 only b_0 is nonzero, and at t = 1 only b_3, so the curve
passes through P_0 and P_3 and in general through neither middle point.

**Change of basis to monomials.** Expanding the Bernstein polynomials in powers of t gives

```
(a_0; a_1; a_2; a_3) = M X,      M = [  1   0   0   0 ]
                                     [ −3   3   0   0 ]
                                     [  3  −6   3   0 ]
                                     [ −1   3  −3   1 ]
```

Column k of M⁻¹ would give the monomial t^k in Bernstein coordinates. The monomial form is convenient for
evaluating derivatives; the Bernstein form is the one people can edit, because its coordinates are points
in the plane.

**Degree elevation.** A quadratic is also a cubic, because P_2 is a subspace of P_3. In Bernstein
coordinates the inclusion is the linear map

```
P_0 = Q_0,   P_1 = (Q_0 + 2 Q_1)/3,   P_2 = (2 Q_1 + Q_2)/3,   P_3 = Q_2
```

So converting a TrueType outline to cubic (CFF) form is exact. The reverse direction is not: a cubic lies
in P_2 only when its t³ coefficient, a_3 = −P_0 + 3P_1 − 3P_2 + P_3, is zero.

**Worked case: a cubic that is secretly a quadratic.** Take P_0 = (0, 0), P_1 = (2, 2), P_2 = (4, 2),
P_3 = (6, 0). Multiplying by M gives

```
x(t) = 6t,     y(t) = 6t − 6t²
```

Both t³ coefficients vanish, and so does the t² coefficient of x: the curve is the parabola from the
quadratic segment Q_0 = (0, 0), Q_1 = (3, 3), Q_2 = (6, 0), which the degree-elevation formulas send back
to exactly these four points. Its midpoint is B(1/2) = (P_0 + 3P_1 + 3P_2 + P_3)/8 = (3, 1.5), and it
never comes near the middle control points, whose height is 2.

**Evaluation and subdivision by de Casteljau.** Interpolate linearly between neighbouring control points
at the fraction t, and repeat on the new points until one is left; that point is B(t). At t = 1/2 the
example gives (1, 1), (3, 2), (5, 1), then (2, 1.5), (4, 1.5), then (3, 1.5). The points produced along
the way are, read down the left and right edges, the control points of the two halves:
(0, 0), (1, 1), (2, 1.5), (3, 1.5) and (3, 1.5), (4, 1.5), (5, 1), (6, 0). Splitting a curve is
therefore a change of basis: each half is the same polynomial, written in the Bernstein basis of a
shorter interval.

## Matrix structure

Every map is a small dense matrix acting on the 4 × 2 array of control points: the 4 × 4 lower
triangular Bernstein-to-monomial matrix M, a 4 × 4 subdivision matrix for each half, and a 4 × 3
degree-elevation matrix from P_2 to P_3. Their entries are fixed rational numbers, so they are computed
once and applied to every segment.

## What is computed

A renderer evaluates or subdivides each segment (often with de Casteljau steps, which only average
points and are numerically stable) until the pieces are flat enough to treat as straight lines, then
fills the outline. Font-conversion tools elevate quadratic outlines to cubic exactly, and approximate
each cubic by one or more quadratics, splitting it until the error is within a tolerance; the cu2qu
module of the fontTools library does this when fonts are compiled to TrueType.

## Why linear algebra is the right tool

The control points are coordinates, so every operation that a font or drawing program performs is
linear in them. Changing format is a change of basis or an inclusion of one polynomial space in another;
splitting a curve is a change of basis to a subinterval; and the question "is this cubic really a
quadratic" is whether a vector lies in a subspace, settled by one linear functional. The Bernstein basis
is chosen for geometric reasons (nonnegative functions that sum to 1), which make its coordinates behave
like weighted averages of points. That property is what makes them meaningful to a designer.

## Pitfall worth teaching

The control points transform correctly under affine maps, and only under them. Because the basis
polynomials sum to 1, B(t) is a weighted average of the control points with weights that add up to 1,
so scaling, rotating, shearing or moving the control points does the same to every point of the curve.
That is why a font can be scaled by transforming a few points. A perspective (projective) transformation
is not affine: it divides by a quantity that depends on the point, which does not distribute over a
weighted average. Applying a perspective map to the control points and redrawing gives a visibly
different curve from applying it to the curve itself. Representing curves exactly under perspective
requires rational Bézier curves, which use homogeneous coordinates (see the 3D viewing entry). A second
misconception has the same root: the parameter t is not distance along the curve, so equally spaced
values of t give unequally spaced points.

## Extensions

B-splines join many polynomial pieces with a basis of a whole space of smooth piecewise polynomials, and
NURBS add weights, which is why CAD systems use them. Bézier surfaces use the tensor-product basis
b_i(u) b_j(v) of a 16-dimensional space; the Utah teapot is 32 such patches. CSS animation timing
functions (cubic-bezier) are cubics in the same basis. Polynomial interpolation through given points is
the same space with a different basis (the polynomial interpolation entry), and least-squares fitting of
a curve to scanned points is the basis-fitting entry. The affine-transform and 3D viewing entries are the
matrices that act on control points.
