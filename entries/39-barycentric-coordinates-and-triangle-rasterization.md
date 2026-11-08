---
id: 39
slug: barycentric-coordinates-and-triangle-rasterization
status: written
title: 'Barycentric coordinates: one 3 × 3 system decides which pixels a triangle covers and what colour
  they get'
short_title: Barycentric coordinates and triangle rasterization
field_label: Computer graphics, GPU hardware, game engines, mesh processing, computational geometry
tier_note: 'a pixel''s barycentric coordinates are its coordinates relative to the triangle''s corners, the
  solution of one 3 × 3 linear system. Their signs decide coverage, and the same weights blend colour and
  depth. The finite element method uses the same coordinates as basis functions for differential
  equations, which is Tier 3.'
nav_field: Computer Graphics & Vision
field: Computer Science
subfield: Computer graphics
tier: 1
tier_ceiling: 3
prereq_beyond_la: ''
scalar_field: R
vector_space: 'the plane R^2 of screen positions, with each point described by three barycentric
  coordinates (α, β, γ) relative to the triangle''s corners, constrained by α + β + γ = 1. Appending a 1
  to each position turns finding them into a 3 × 3 linear system in R^3'
underlying_equations: 'Affine combination: a point X of the plane is X = α P + β Q + γ R with
  α + β + γ = 1, and each attribute of the triangle, such as colour or depth, is blended with the same
  weights'
core_la_object: Coordinates relative to a simplex basis
la_concepts: coordinates with respect to a basis; affine and convex combinations; convex hull; 3 × 3
  linear system and its inverse; determinant as signed area; Cramer's rule; linear interpolation
primary_method: One 3 × 3 inverse per triangle, then three additions per pixel step (edge functions)
matrix_structure: dense 3 × 3 with a bottom row of 1s; its inverse is applied at every pixel
typical_size: 3 × 3 per triangle, evaluated at every pixel the triangle might cover
worked_example_size: one triangle and four pixels (inside, inside, outside and on an edge), with
  interpolated colour and depth
terminology:
  pixel centre: the point in the middle of a pixel; a pixel is drawn when its centre is covered
  rasterization: deciding which pixel centres a shape covers, turning a vector description into pixels
  barycentric coordinates: the weights (α, β, γ) that write a point as a weighted average of the three
    corners
  affine combination: a weighted sum whose weights add up to 1
  convex combination: an affine combination with no negative weights; these fill the triangle
  edge function: a barycentric coordinate written as a linear function of the pixel position
  attribute: a value stored at each corner (colour, depth, texture coordinate) and blended across the
    triangle
  Gouraud shading: colouring a triangle by blending its corner colours
  texture coordinates: the position in an image (a texture) that each corner is mapped to
  perspective-correct interpolation: blending attributes using the 3D weights rather than the screen
    weights
  top-left rule: the tie-break that assigns a pixel exactly on a shared edge to just one triangle
---

## Start here

Everything a GPU draws is broken into triangles, and the screen is a grid of pixels. For every
triangle, two questions have to be answered at every pixel nearby. Is this pixel inside the triangle?
If so, what colour and depth should it get, given the values at the three corners?

Both questions have one answer: describe the pixel as a weighted average of the triangle's three
corners. The three weights are called barycentric coordinates, after the barycentre, the centre of
mass that the corners would have if they carried those weights. If all three weights are positive the
pixel is inside. And to blend colours, depths or anything else from the corners, use the same three
weights.

Finding the weights is a 3 × 3 linear system, and because the matrix belongs to the triangle rather
than the pixel, it is inverted once per triangle and reused at every pixel. A GPU does this billions of
times a second.

## The problem

A triangle arrives with its corners P, Q and R already in screen coordinates, measured in pixels, as
the output of the 3D viewing pipeline. Each corner also carries **attributes**: a colour, a depth, and
often **texture coordinates**, the position in an image that is to be painted onto the triangle. The
**pixel centre** is the point in the middle of a pixel, and the pixel is drawn when its centre lies
inside the triangle. **Rasterization** is the job of finding those pixels. It is where a vector
description, three corners that could be drawn at any resolution, becomes a raster image, a fixed grid
of samples, the contrast at the heart of the Bézier-curve entry.

For each pixel centre X near the triangle, decide whether X is inside, and if so compute its colour and
depth by blending the corner values. The known quantities are P, Q, R, the corner attributes and X.
The unknowns are three weights per pixel.

## Variables

| Symbol | Name | What it holds | Shape | Units |
|---|---|---|---|---|
| P, Q, R | corners | screen positions of the triangle's corners | 2 × 1 each | pixels |
| X | pixel centre | (x, y), the point being tested | 2 × 1 | pixels |
| α, β, γ | barycentric coordinates | weights on P, Q and R | 3 numbers, α + β + γ = 1 | dimensionless |
| T | corner matrix | columns (P, 1), (Q, 1), (R, 1) | 3 × 3 | pixels in the first two rows |
| c_P, c_Q, c_R | corner colours | red, green and blue intensities | 3 × 1 each | 0 to 1 |
| z_P, z_Q, z_R | corner depths | the depths z_n from the viewing pipeline | numbers | dimensionless |
| w_P, w_Q, w_R | corner w values | each corner's fourth clip coordinate, its distance from the camera | numbers | scene units |
| u | texture coordinate | position along the texture image | number | 0 to 1 |
| s, t | edge fractions | how far along an edge, in 3D (s) and on screen (t) | numbers in [0, 1] | dimensionless |

## Formulation

**Where the equations come from.** The model is the affine combination: a point of the plane written
as a weighted sum of the three corners, with weights that add up to 1,

```
X = α P + β Q + γ R,       α + β + γ = 1
```

Because the weights add up to 1, the answer does not depend on where the origin is: moving all four
points by the same amount leaves α, β and γ unchanged.

**The familiar case.** On a line segment from P to Q, the point a fraction t of the way along is
(1 − t) P + t Q, and a value that varies linearly along the segment is (1 − t) a_P + t a_Q, where a_P
and a_Q are its values at the ends. That is linear interpolation, and its weights 1 − t and t are the
barycentric coordinates of a segment. A triangle needs three weights.

**One coordinate first.** The weight α measures how close X is to the corner P, compared with the
opposite edge QR. It is 1 at P, 0 everywhere on the line through Q and R, and changes linearly in
between. Its sign says which side of that line X is on: α is negative exactly when X is on the far side
of QR from P. The same holds for β with the edge RP and for γ with the edge PQ. So X is inside the
triangle exactly when all three weights are nonnegative, and the points with nonnegative weights adding
up to 1, the **convex combinations**, fill the triangle.

**Stacking the conditions.** Written as scalar equations, the definition is two coordinate equations
plus the condition on the sum:

```
α P_x  +  β Q_x  +  γ R_x  =  x
α P_y  +  β Q_y  +  γ R_y  =  y
α      +  β      +  γ      =  1
```

As a matrix product, T (α, β, γ) = (x, y, 1), where T has the corners as columns with a 1 appended to
each, the homogeneous coordinates of the 2D affine-transform entry. The determinant of T is twice the
signed area of the triangle, so T is invertible unless the triangle has collapsed onto a line.
Cramer's rule gives each weight as a ratio of determinants, which is a ratio of areas:
α = area(XQR) / area(PQR), and similarly for β and γ.

**Blending attributes.** Once the weights are known, every attribute is blended with them:

```
colour  =  α c_P + β c_Q + γ c_R,        depth  =  α z_P + β z_Q + γ z_R
```

Blending colours this way is called **Gouraud shading**.

**Worked case: one triangle, four pixels.** Take P = (1, 1), Q = (7, 3) and R = (3, 7). The system is

```
[ 1  7  3 ] [ α ]   [ x ]
[ 1  3  7 ] [ β ] = [ y ]
[ 1  1  1 ] [ γ ]   [ 1 ]
```

with det T = 32, so the triangle has area 16 square pixels. The inverse, computed once for the
triangle, is

```
         [ −1/8    −1/8     5/4 ]
T⁻¹  =   [  3/16   −1/16   −1/8 ]
         [ −1/16    3/16   −1/8 ]
```

and every pixel is one product with it. For the pixel centre X = (3, 3):

```
[ −1/8    −1/8     5/4 ] [ 3 ]   [ 1/2 ]
[  3/16   −1/16   −1/8 ] [ 3 ] = [ 1/4 ]
[ −1/16    3/16   −1/8 ] [ 1 ]   [ 1/4 ]
```

All three weights are positive, so (3, 3) is inside. The other pixels give

```
X = (5, 3):   (α, β, γ) = (1/4, 5/8, 1/8)       inside
X = (6, 5):   (α, β, γ) = (−1/8, 11/16, 7/16)   outside: beyond the edge QR
X = (2, 4):   (α, β, γ) = (1/2, 0, 1/2)         exactly on the edge PR
```

Colour the corners pure red, green and blue: c_P = (1, 0, 0), c_Q = (0, 1, 0), c_R = (0, 0, 1). Then a
pixel's colour is its weights themselves, so (3, 3) is (0.5, 0.25, 0.25), a muted red. With depths
z_P = 0.2, z_Q = 0.6 and z_R = 0.4, the depth at (3, 3) is 0.5·0.2 + 0.25·0.6 + 0.25·0.4 = 0.35, and at
(5, 3) it is 0.475.

## Matrix structure

T is a small dense matrix with a bottom row of 1s. The columns of T⁻¹ have a meaning of their own.
Moving one pixel to the right adds the first column to (α, β, γ), and moving one pixel up adds the
second. In the worked case these steps are (−1/8, 3/16, −1/16) and (−1/8, −1/16, 3/16). Each sums to
zero, which keeps α + β + γ = 1, while the third column sums to 1. A rasterizer therefore never repeats
the product: stepping from (3, 3) to (4, 3) is three additions, giving (3/8, 7/16, 3/16). Written as
functions of the pixel position, the three weights are called **edge functions**.

The sign of det T says which way round the corners go: positive for counterclockwise when y points up.
Triangles facing away from the camera arrive clockwise, so the same determinant lets the hardware skip
them.

## What is computed

GPUs evaluate the three edge functions for whole blocks of pixels in parallel, in fixed-point arithmetic
so that results are exact and repeatable. This approach goes back to Pineda's 1988 parallel
rasterization algorithm. A pixel centre exactly on an edge shared by two triangles must be drawn once,
not twice or never, and the **top-left rule** used by Direct3D and others breaks the tie by which kind
of edge it is. The interpolated attributes then reach the program that colours each pixel (the
fragment shader). In GLSL they are perspective-correct by default, and the noperspective qualifier
switches to plain screen-space blending.

## Why linear algebra is the right tool

Barycentric coordinates are coordinates in the ordinary sense: the triangle's corners act as a frame,
and finding a point's coordinates in a frame is solving a linear system. The inside test is the
description of a convex hull as the nonnegative combinations. Interpolation is linear because the
coordinates are affine functions of position. Because the matrix belongs to the triangle, the expensive
step happens once per triangle and each pixel costs a matrix product, or three additions when stepping
across a row. The determinant does three more jobs: area, orientation, and detecting a collapsed
triangle.

## Pitfall worth teaching

Weights measured on the screen are not the weights in the 3D scene. Perspective shrinks distant parts
of a triangle, so equal steps across the screen are unequal steps across the surface. Blending texture
coordinates with screen weights makes textures bend and swim as the camera moves, which was a familiar
sight in games on the original PlayStation, whose hardware did exactly that.

Take one edge, from a near corner at distance w_P = 1 to a far corner at w_Q = 3, with texture
coordinate u = 0 at the near corner and u = 1 at the far one. A point a fraction s of the way along the
edge in 3D appears at the screen fraction

```
t  =  s w_Q / ( (1 − s) w_P + s w_Q )
```

so s = 1/4 lands at t = 3/4 ÷ (3/4 + 3/4) = 1/2. The pixel in the middle of the edge on the screen is
only a quarter of the way along it in 3D. Plain screen blending gives it u = 0.5, but the correct value
is 0.25.

The correction is to blend u/w and 1/w with the screen weights, which is exact because both are affine
functions of screen position, and then divide one by the other:

```
u  =  ( 0.5 · 0/1  +  0.5 · 1/3 )  /  ( 0.5 · 1/1  +  0.5 · 1/3 )  =  (1/6) / (2/3)  =  1/4
```

Depth needs no correction. The viewing entry chose z_n to be affine in 1/d, which makes it vary
linearly across the screen, so screen weights blend it exactly.

## Extensions

The Möller–Trumbore ray–triangle intersection test, used in ray tracing, solves a similar 3 × 3 system
for two barycentric coordinates and the distance along the ray. Texture mapping assigns each corner a
position in an image and blends those positions with the same weights. In the finite element method
the barycentric coordinates of a triangle are the linear basis functions used to approximate solutions
of differential equations (Tier 3). Bézier triangles, the surface version of the Bézier-curve entry,
use barycentric coordinates as their variables. In 3D, a tetrahedron's four barycentric coordinates
solve a 4 × 4 system of the same form, used to interpolate inside volumes. Linear interpolation on a
triangle is the two-variable, degree-1 case of the polynomial interpolation entry. The 3D viewing
entry produces the corner positions and the w values used above.
