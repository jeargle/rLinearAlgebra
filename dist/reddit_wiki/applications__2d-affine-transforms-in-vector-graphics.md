# 2D transforms in SVG, CSS and Canvas: why translation needs a third coordinate

### Start here

Every web page, drawing program and vector illustration moves shapes around: it shifts them, turns them,
stretches them and slants them. Web designers write these moves as short instructions, such as
"translate this by 50 pixels, then rotate it by 30 degrees", and the browser applies them to every point
of the shape.

Two facts surprise people. The first is that order matters: turning a shape and then sliding it puts
it somewhere different from sliding it and then turning it. The second is that the code which
represents these moves uses tables of nine numbers, three by three, even though the screen is only two
dimensional.

Both have the same explanation. Turning and stretching are the kind of operation a matrix performs, and
doing one after another is multiplying matrices, which depends on the order. Sliding is different: it
moves the origin, and a matrix acting on two coordinates can never do that. The fix is to give every
point a third coordinate that is always 1. With it, a slide becomes a matrix too, and every combination
of moves, however long, collapses into a single three-by-three matrix.

**Field:** Computer graphics, web front-end development, vector illustration, user interfaces  
**Tier:** 1 — every transform is a 3 × 3 matrix acting on [homogeneous coordinates](https://en.wikipedia.org/wiki/Homogeneous_coordinates), and a transform stack is a matrix product. Splitting a general transform back into rotation, scale and [shear](https://en.wikipedia.org/wiki/Shear_mapping) uses the [SVD](https://en.wikipedia.org/wiki/Singular_value_decomposition) or the [polar decomposition](https://en.wikipedia.org/wiki/Polar_decomposition), which are Tier 2.  
**Scalar field:** R  
**Vectors:** points of the plane R^2, represented in homogeneous coordinates as vectors (x, y, 1) in R^3. The points themselves form the plane z = 1 inside R^3, which is not a subspace (it misses the origin); the [affine](https://en.wikipedia.org/wiki/Affine_transformation) maps of the plane are the 3 × 3 matrices with bottom row (0, 0, 1), which map that plane to itself  
**Underlying equations:** Matrix products acting on homogeneous coordinates: p′ = M p

### The problem

Represent the moves of 2D graphics (translation, rotation, scaling, shear, and any sequence of them) so
that a whole sequence can be combined into one transform, applied quickly to every point of a drawing,
inverted (to find which point of a shape lies under the mouse pointer), and written in the notations
that [SVG](https://en.wikipedia.org/wiki/SVG), [CSS](https://en.wikipedia.org/wiki/CSS) and the HTML [Canvas](https://en.wikipedia.org/wiki/Canvas_element) use.

### Variables

| Symbol | Name | What it holds | Shape | Units |
|---|---|---|---|---|
| (x, y) | point | a point of the drawing | 2 numbers | pixels or user units |
| p | homogeneous point | (x, y, 1) | 3 × 1 | pixels in the first two entries |
| L | linear part | rotation, scaling and shear together | 2 × 2 | dimensionless |
| t | translation | the shift (e, f) | 2 × 1 | pixels |
| M | affine transform | the 3 × 3 matrix with L in its top-left 2 × 2 block, t in its last column, and bottom row (0, 0, 1) | 3 × 3 | mixed: L dimensionless, t in pixels |
| T(e, f) | translation matrix | moves every point by (e, f) | 3 × 3 | — |
| R(θ) | rotation matrix | turns every point by θ about the origin | 3 × 3 | — |
| S(s_x, s_y) | scaling matrix | stretches by s_x horizontally and s_y vertically | 3 × 3 | — |
| θ | angle | rotation angle; positive turns the x-axis toward the y-axis | scalar | degrees or radians |
| c | centre | a point about which to rotate or scale | 2 × 1 | pixels |

Screen coordinates usually point y downwards, so a positive θ in SVG and CSS turns shapes clockwise on
the screen, even though the matrix is the same as the textbook rotation.

### Formulation

**Where the equations come from.** The model is a choice of coordinates: points carry an extra
coordinate fixed at 1 so that every move of the plane becomes a matrix product.

**Linear moves.** Rotation, scaling and shear fix the origin and act on (x, y) through a 2 × 2 matrix.
The familiar rotation formula,

```
x′ = x cos θ − y sin θ
y′ = x sin θ + y cos θ
```

is the matrix-vector product

```
[ x′ ]   [ cos θ  −sin θ ] [ x ]
[ y′ ] = [ sin θ   cos θ ] [ y ]
```

and this 2 × 2 matrix is the linear part L of a rotation.

**Translation is not linear.** The shift x′ = x + e, y′ = y + f moves the origin to (e, f), and every
linear map sends the origin to itself, so no 2 × 2 matrix can do it. A general move of the plane is an
affine map, a linear part followed by a shift: (x′, y′) = L (x, y) + t.

**Homogeneous coordinates.** Represent (x, y) by p = (x, y, 1). Then the affine map is one matrix
product in ℝ³:

```
[ x′ ]   [ a  c  e ] [ x ]                  [ a  c ]              [ e ]
[ y′ ] = [ b  d  f ] [ y ]       with   L = [ b  d ]   and   t = [ f ]
[ 1  ]   [ 0  0  1 ] [ 1 ]
```

The 1 in the last coordinate picks up the translation column, and the bottom row keeps it equal to 1.
This 3 × 3 matrix is exactly what SVG and CSS write as matrix(a, b, c, d, e, f): the six numbers are
the first two rows, read column by column.

**A transform stack is a product.** SVG's transform="translate(2, 0) rotate(90)", CSS's
transform: translate(2px, 0) rotate(90deg), and the Canvas calls ctx.translate(2, 0); ctx.rotate(…)
all mean the matrix

```
M = T(2, 0) R(90°)
```

applied to each point as M p = T(2, 0) (R(90°) p). The rightmost transform acts on the point first.

**Worked case: one point, two orders.** The two elementary matrices are

```
            [ 1  0  2 ]                [ 0  −1  0 ]
T(2, 0)  =  [ 0  1  0 ]     R(90°)  =  [ 1   0  0 ]
            [ 0  0  1 ]                [ 0   0  1 ]
```

and their products in the two orders are

```
                    [ 0  −1  2 ]                        [ 0  −1  0 ]
T(2, 0) R(90°)  =   [ 1   0  0 ]     R(90°) T(2, 0)  =  [ 1   0  2 ]
                    [ 0   0  1 ]                        [ 0   0  1 ]
```

Applied to the point (1, 0), written as (1, 0, 1):

```
[ 0  −1  2 ] [ 1 ]   [ 2 ]          [ 0  −1  0 ] [ 1 ]   [ 0 ]
[ 1   0  0 ] [ 0 ] = [ 1 ]          [ 1   0  2 ] [ 0 ] = [ 3 ]
[ 0   0  1 ] [ 1 ]   [ 1 ]          [ 0   0  1 ] [ 1 ]   [ 1 ]

translate(2, 0) rotate(90):         rotate(90) translate(2, 0):
rotate to (0, 1), shift to (2, 1)   shift to (3, 0), rotate to (0, 3)
```

Matrix multiplication does not commute, and the two programs draw in different places.

**Rotating about a point.** rotate(θ, c_x, c_y) in SVG, or a CSS transform-origin, turns a shape about
the point c rather than about the origin. It is three moves: shift c to the origin, rotate, shift back,

```
T(c) R(θ) T(−c)
```

For θ = 90° about c = (1, 1):

```
[ 1  0  1 ] [ 0  −1  0 ] [ 1  0  −1 ]   [ 0  −1  2 ]
[ 0  1  1 ] [ 1   0  0 ] [ 0  1  −1 ] = [ 1   0  0 ]
[ 0  0  1 ] [ 0   0  1 ] [ 0  0   1 ]   [ 0   0  1 ]
   T(c)        R(90°)       T(−c)
```

and the result sends (2, 1) to (1, 2):

```
[ 0  −1  2 ] [ 2 ]   [ 1 ]
[ 1   0  0 ] [ 1 ] = [ 2 ]
[ 0   0  1 ] [ 1 ]   [ 1 ]
```

a quarter turn about (1, 1). That matrix happens to equal T(2, 0) R(90°) from the worked case: a rotation
about one point is the same move as a rotation about the origin followed by some translation.

**Undoing a transform.** The inverse of a product reverses the order: (T R)⁻¹ = R⁻¹ T⁻¹, so to undo
"rotate, then translate" you untranslate first and then unrotate. For an affine matrix the inverse is

```
[ L   t ]⁻¹     [ L⁻¹   −L⁻¹ t ]
[ 0   1 ]    =  [  0       1   ]
```

written in blocks (the 0 is the row (0, 0)), which exists whenever L is invertible.

### Matrix structure

Dense 3 × 3 with bottom row (0, 0, 1), so six numbers determine it. Products and inverses of such
matrices have the same bottom row: affine maps are closed under composition and inversion. Rotations
have an orthogonal L, uniform scalings a multiple of the identity, and shears a triangular L.

### What is computed

A renderer multiplies the transforms along the path from the page down to each shape into one current
transformation matrix, then applies it to every point (6 multiplications and 4 additions per point).
For mouse events and hit testing it applies the inverse matrix to the pointer position, to find where
in the shape's own coordinates the click landed. Browsers expose these matrices directly, for example
through DOMMatrix and getScreenCTM().

### Why linear algebra is the right tool

Representing moves as matrices turns composition into multiplication, so any sequence of transforms,
however long or nested, is one matrix computed once. Laws that designers learn by trial and error are
theorems: order matters because multiplication does not commute; undoing a sequence reverses its order;
rotating about a point is a conjugation T(c) R T(−c). Affine maps send straight lines to straight lines
and parallel lines to parallel lines, but not circles to circles or right angles to right angles, which
is why a scaled circle becomes an ellipse.

### Pitfall worth teaching

The same list of transforms can be read in two opposite orders, and both readings are correct. Read
right to left, translate(2, 0) rotate(90) rotates the point in the original axes and then shifts it.
Read left to right, it first moves the coordinate system by (2, 0) and then rotates the moved axes, and
the shape is drawn in those new axes. Both describe the matrix product T R, and both put (1, 0) at
(2, 1). Mixing the two readings within one stack is how most "the rotation happened about the wrong
point" bugs start. A second trap is the convention for writing vectors. SVG, CSS and Canvas use column
vectors, M p, but some graphics libraries use row vectors, p M, with every matrix transposed and every
product reversed. Copying a matrix or a multiplication order between the two conventions without
transposing gives a transform that is close enough to look plausible and wrong enough to fail.

### Extensions

3D graphics uses the same idea with 4 × 4 matrices, and adds the perspective projection that affine
maps cannot express (the 3D viewing entry). Rigid motions, rotation plus translation with no stretching,
are the 3D rotations and rigid-body pose entry. Splitting a general matrix(a, b, c, d, e, f) back into
"rotate, scale, rotate", which animation libraries do to interpolate between two transforms, is the SVD
or the polar decomposition (Tier 2). [Bézier curves](https://en.wikipedia.org/wiki/B%C3%A9zier_curve) transform correctly when their control points are
transformed by an affine map, which is why fonts and SVG paths can be scaled losslessly (the Bézier
entry).

### Terminology

How this field's vocabulary reads as linear algebra.

| Domain term | In linear algebra |
|---|---|
| transform attribute / CSS transform property | a list of elementary transforms whose matrices are multiplied in the order written |
| matrix(a, b, c, d, e, f) | the SVG/CSS notation for the 3 × 3 matrix with columns (a, b, 0), (c, d, 0), (e, f, 1) |
| current transformation matrix (CTM) | the product of every transform in effect for an element |
| user space vs viewport space | two coordinate systems related by the CTM |
| transform-origin | the point about which rotation and scaling happen, a conjugation T(c) M T(−c) |
| translate, rotate, scale, skew | the elementary matrices of the stack |
| local vs global coordinates | reading a product right to left (each step in the parent's frame) or left to right (each step in the newly moved frame) |
| identity transform | the 3 × 3 identity, matrix(1, 0, 0, 1, 0, 0) |

---

[Back to the index](/r/LinearAlgebra/wiki/applications)
