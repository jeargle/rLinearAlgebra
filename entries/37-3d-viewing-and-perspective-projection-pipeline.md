---
id: 37
slug: 3d-viewing-and-perspective-projection-pipeline
status: written
title: '3D viewing: the model-view-projection chain, and the one division that makes perspective'
short_title: 3D viewing and perspective projection pipeline
field_label: Computer graphics, game engines, scientific visualization, augmented and virtual reality
tier_note: 'every stage of the pipeline is a 4 × 4 matrix acting on homogeneous coordinates, and
  perspective is a single division by the fourth coordinate after the last product. Recovering a real
  camera''s matrices from photographs uses the SVD, which is Tier 2.'
nav_field: Computer Graphics & Vision
field: Computer Science
subfield: Computer graphics
tier: 1
tier_ceiling: 2
prereq_beyond_la: ''
scalar_field: R
vector_space: 'points of R^3 carried as homogeneous vectors in R^4: (x, y, z, 1) for a point, and after
  the projection matrix (x_c, y_c, z_c, w_c), which stands for the point (x_c/w_c, y_c/w_c, z_c/w_c).
  Every stage before the division is a linear map of R^4'
underlying_equations: 'Pinhole projection: a point at distance d in front of the eye, at height y, appears
  at height y/d on an image plane at distance 1, written as a linear map in homogeneous coordinates
  followed by division by w'
core_la_object: Model-view-projection chain
la_concepts: homogeneous coordinates; change of basis between coordinate frames; composition of linear
  maps; matrix inverse; a 2 × 2 linear system for the depth row; projective division
primary_method: Dense 4 × 4 products, one combined matrix per object, then one division per vertex
matrix_structure: dense 4 × 4; model and view matrices have bottom row (0, 0, 0, 1), the perspective
  matrix has bottom row (0, 0, −1, 0)
typical_size: 4 × 4, applied to 1e3-1e7 vertices per frame
worked_example_size: a cube through the full chain, one vertex by hand and all eight in a table
terminology:
  vertex: a corner of a triangle; the pipeline moves vertices, and the triangles follow
  object, world and camera coordinates: the frames attached to a model, to the scene, and to the eye
  model matrix: places an object in the world (object to world coordinates)
  view matrix: re-expresses the world relative to the camera (world to camera coordinates)
  projection matrix: maps the visible region to clip coordinates and puts the depth into w
  clip coordinates: the homogeneous 4-vector after the projection matrix, before division
  perspective division: dividing by w, the step that makes distant objects smaller
  normalized device coordinates (NDC): the cube −1 ≤ x, y, z ≤ 1 that the visible region lands in
  viewport transform: the final scaling from NDC to pixels
  near and far planes: the closest and farthest distances that are drawn
  field of view: the angle the camera sees, top to bottom
  view frustum: the truncated pyramid between the near and far planes that the camera sees
  depth buffer (z-buffer): the per-pixel record of the nearest depth drawn so far
  z-fighting: flickering between surfaces whose depths the depth buffer cannot tell apart
---

## Start here

A 3D game draws millions of triangles many times a second. Every corner of every triangle goes
through the same short chain of matrix products: place the object in the scene, look at the scene from
the camera, and project it onto the flat screen. Graphics hardware is built to do exactly this, as
fast as possible.

The everyday fact that makes the last step interesting is perspective. Railway tracks meet at the
horizon, and a person twice as far away looks half as tall. Perspective divides by distance, and
division is not linear, so it seems that it cannot be a matrix.

The trick is the extra coordinate from the 2D affine-transform entry, now used in a new way. With four
numbers standing for three, translation, rotation and the perspective set-up are all 4 × 4 matrices.
Only one division is left, at the very end, by the fourth number. Everything before it is ordinary
linear algebra.

## The problem

The scene is made of triangles, and a **vertex** is a corner of a triangle. Three coordinate frames
matter. **Object coordinates** are the ones a model is built in, such as a cube centred on its own
origin. **World coordinates** place all the objects in one scene. **Camera coordinates** describe the
scene as the eye sees it, and by the convention used here (OpenGL's) the camera sits at the origin,
looks along the negative z-axis, and has y pointing up. A point in front of the camera therefore has
negative z, and its **distance** in front of the camera is d = −z.

Only points between two distances are drawn: the **near plane** at distance n and the **far plane** at
distance f. The **field of view** θ is the angle the camera sees from the bottom of the image to the
top. Together they cut out a **view frustum**, a pyramid with its tip cut off. The pipeline maps the
frustum onto the cube −1 ≤ x, y, z ≤ 1 of **normalized device coordinates**, and then onto the pixels
of a W × H image.

Given a vertex in object coordinates, where the object sits in the world, and where the camera is and
what it sees, compute the pixel where the vertex appears and its depth.

## Variables

| Symbol | Name | What it holds | Shape | Units |
|---|---|---|---|---|
| X | vertex | (x, y, z, 1), a point in object coordinates | 4 × 1 | scene units in the first three entries |
| R | rotation | the turning part of a pose | 3 × 3, orthogonal | dimensionless |
| t | translation | where an object's origin sits in the world | 3 × 1 | scene units |
| c | camera position | where the camera sits in the world | 3 × 1 | scene units |
| M | model matrix | object coordinates to world coordinates | 4 × 4 | mixed |
| V | view matrix | world coordinates to camera coordinates | 4 × 4 | mixed |
| x_e | camera coordinates | (x_e, y_e, z_e, 1) = V M X | 4 × 1 | scene units |
| d | distance | d = −z_e, how far in front of the camera | number | scene units |
| n, f | near and far distances | the range of distances that is drawn | numbers, 0 < n < f | scene units |
| θ | field of view | vertical viewing angle | angle | degrees |
| g | focal scale | g = 1 / tan(θ/2) | number | dimensionless |
| a | aspect ratio | image width divided by height | number | dimensionless |
| P | projection matrix | camera coordinates to clip coordinates | 4 × 4 | mixed |
| x_c | clip coordinates | (x_c, y_c, z_c, w_c) = P x_e | 4 × 1 | scene units |
| (x_n, y_n, z_n) | normalized device coordinates | (x_c, y_c, z_c) / w_c | 3 numbers in [−1, 1] | dimensionless |
| W, H | image size | width and height | integers | pixels |
| α, β | depth coefficients | entries of the third row of P | numbers | dimensionless and scene units |

## Formulation

**Where the equations come from.** The model is a pinhole camera. A point at distance d in front of
the eye and at height y lines up, by similar triangles, with height y/d on an image plane at distance 1.
Far objects look smaller because their heights are divided by a larger d.

**The familiar formula.** The perspective projection taught in drawing and geometry classes is

```
x′ = x / d,      y′ = y / d
```

for a point at (x, y) across and up from the line of sight, at distance d. The rest of the pipeline is
built so that this division happens once, at the end.

**Step 1: the model matrix.** An object is built in its own coordinates and placed in the world by a
rotation R and a translation t. As in the 2D affine-transform and 3D rotation entries, homogeneous
coordinates make this one matrix:

```
    [ R   t ]
M = [       ]       with bottom row (0, 0, 0, 1)
    [ 0   1 ]
```

**Step 2: the view matrix.** The camera also has a pose in the world: a rotation and a position c. The
view matrix answers the opposite question, where each world point is relative to the camera, so it is
the inverse of the camera's pose matrix. It is a change of basis: the same point, given coordinates in
the camera's frame instead of the world's. For a camera at c = (0, 0, 3) that is not rotated, the view
matrix simply moves everything 3 units along −z:

```
    [ 1  0  0   0 ]
V = [ 0  1  0   0 ]
    [ 0  0  1  −3 ]
    [ 0  0  0   1 ]
```

**Step 3: the projection matrix puts the distance into w.** A homogeneous vector (x_c, y_c, z_c, w_c)
stands for the point (x_c/w_c, y_c/w_c, z_c/w_c). So if a matrix copies the distance d = −z_e into the
fourth coordinate, the division by w later performs the perspective division. That is the job of the
bottom row (0, 0, −1, 0). The first two rows scale x and y by g = 1/tan(θ/2), with an extra 1/a for x,
so that the edges of the field of view land on ±1.

The third row must keep some measure of depth, because the hardware needs it to decide which surface
is in front. Any row (0, 0, α, β) gives z_n = (α z_e + β)/d after the division. Choose α and β so that
the near plane maps to −1 and the far plane to +1. Those are two scalar equations,

```
near plane, z_e = −n:    (−α n + β) / n  =  −1      so    −n α + β  =  −n
far plane,  z_e = −f:    (−α f + β) / f  =  +1      so    −f α + β  =   f
```

which as a matrix product are

```
[ −n   1 ] [ α ]   [ −n ]
[ −f   1 ] [ β ] = [  f ]
```

Subtracting the first equation from the second gives α = −(f + n)/(f − n), and then β = −2fn/(f − n).
The projection matrix is

```
    [ g/a   0          0                0          ]
P = [  0    g          0                0          ]
    [  0    0   −(f + n)/(f − n)   −2fn/(f − n)    ]
    [  0    0         −1                0          ]
```

**Step 4: division and viewport.** Divide by w_c to get normalized device coordinates, and scale to
pixels with ((x_n + 1) W/2, (y_n + 1) H/2). On screens whose pixel rows count downwards, the y formula
is flipped.

**The whole chain.** A vertex becomes x_c = P V M X, read right to left: model, then view, then
projection. The product P V M is computed once per object and applied to all its vertices.

**Worked case: a cube.** Take the cube with corners (±1, ±1, ±1), placed in the world unchanged, so
M = I. Use the camera above at (0, 0, 3), a 90° field of view (g = 1), a square image (a = 1), n = 1,
f = 5, and a 400 × 400 viewport. Then α = −6/4 = −1.5 and β = −10/4 = −2.5, and

```
    [ 1  0    0     0  ]                 [ 1  0    0    0 ]
P = [ 0  1    0     0  ]        P V  =   [ 0  1    0    0 ]
    [ 0  0  −1.5  −2.5 ]                 [ 0  0  −1.5   2 ]
    [ 0  0   −1     0  ]                 [ 0  0   −1    3 ]
```

Follow the front top-right corner X = (1, 1, 1, 1) through each step:

```
camera:  V X  =  (1, 1, −2, 1)              distance d = 2
clip:    P (1, 1, −2, 1)  =  (1, 1, −1.5·(−2) − 2.5, 2)  =  (1, 1, 0.5, 2)
NDC:     divide by w_c = 2:  (0.5, 0.5, 0.25)
pixels:  ((0.5 + 1)·200, (0.5 + 1)·200)  =  (300, 300)
```

The back top-right corner (1, 1, −1) is at distance 4 and comes out at clip coordinates (1, 1, 3.5, 4),
NDC (0.25, 0.25, 0.875) and pixel (250, 250). All eight corners:

| Corner | Distance d | Clip coordinates | NDC | Pixel |
|---|---|---|---|---|
| front (±1, ±1, 1) | 2 | (±1, ±1, 0.5, 2) | (±0.5, ±0.5, 0.25) | 100 or 300 in each axis |
| back (±1, ±1, −1) | 4 | (±1, ±1, 3.5, 4) | (±0.25, ±0.25, 0.875) | 150 or 250 in each axis |

The front face spans 200 pixels and the back face 100: twice as far away, half as large. The depths
0.25 and 0.875 keep the two faces in the right order for the depth buffer.

## Matrix structure

M and V are affine: bottom row (0, 0, 0, 1), with a rotation in the top-left 3 × 3 block. The inverse of
a pose with rotation R and position c is therefore cheap, with rotation Rᵀ and translation −Rᵀ c, which
is how the view matrix is computed from the camera's pose. P is the only matrix with a different bottom
row. Its determinant is −(g²/a) · 2fn/(f − n), which is −2.5 in the worked case, so P is invertible and
loses nothing. The flattening from 3D to 2D happens only when the pixel position is read from x_n and
y_n while z_n goes to the depth buffer.

## What is computed

In a GPU program, the vertex shader computes P V M X for each vertex, usually as one matrix uploaded
per object. The hardware then clips triangles against the frustum in clip coordinates, where the
frustum is the set of linear inequalities −w_c ≤ x_c, y_c, z_c ≤ w_c, before any division. It then
divides by w_c, applies the viewport, and fills the triangles. Libraries build the matrices: GLM's
perspective and lookAt functions in C++, and the PerspectiveCamera class in three.js. Conventions
differ between systems: Direct3D and Vulkan map depth to [0, 1] rather than [−1, 1], and some systems
look along +z, so the same scene has different matrices in different APIs.

## Why linear algebra is the right tool

Every change of coordinate frame in the pipeline is a matrix, chaining frames is matrix multiplication,
and the camera's view is a matrix inverse. Homogeneous coordinates turn translation into a matrix, as
in the 2D entry, and they also turn the set-up of perspective into a matrix, which leaves only one
scalar division per vertex. Because the whole chain is one matrix per object, it is computed once and
applied to every vertex, and because clipping happens before the division, it is a set of linear
inequalities rather than a nonlinear test.

## Pitfall worth teaching

Depth in normalized device coordinates is not proportional to distance. After the division,

```
z_n  =  (f + n)/(f − n)  −  (2fn/(f − n)) · (1/d)
```

which is affine in 1/d, not in d. In the worked case the point halfway between the near and far planes,
at d = 3, gets z_n ≈ 0.667, not 0. With realistic settings the effect is drastic. For n = 0.1 and
f = 1000, half of the whole depth range from −1 to 1 is used up by distances between 0.1 and 0.2, and
everything farther than 1 unit shares the last 10%. A 24-bit depth buffer then separates depths about
6 × 10⁻⁵ apart at distance 10, but only 0.006 apart at 100 and 0.15 apart at 500. Two surfaces closer
together than that, such as a road marking painted on a road, flicker through each other as the camera
moves. This is z-fighting.

The precision depends mainly on the near distance. Moving n from 0.1 to 1 makes the resolution at
distance 500 ten times finer, about 0.015. Modern engines also reverse the depth range and store it as
floating point, which spreads the precision far more evenly.

## Extensions

Orthographic projection, used in CAD and technical drawing, has bottom row (0, 0, 0, 1) and no
division, so parallel lines stay parallel. The multiple-view geometry entry runs the chain backwards,
recovering the camera matrix K [R | t] from photographs with the SVD (Tier 2). Rational Bézier curves,
mentioned in the Bézier entry, use the same homogeneous trick to stay exact under perspective. Colours
and textures must be interpolated across a triangle using 1/w, the perspective-correct interpolation
described in the barycentric-coordinates entry. Surface normals transform by the inverse transpose of
the model matrix's 3 × 3 block, not by the block itself, so that they stay perpendicular to surfaces
after non-uniform scaling. Shadow mapping renders the scene a second time from the light, with the
light's own view and projection matrices. The 3D rotations entry covers the rotations inside M and V,
and the 2D affine-transform entry is the planar case of M.
