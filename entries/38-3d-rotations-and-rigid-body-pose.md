---
id: 38
slug: 3d-rotations-and-rigid-body-pose
status: written
title: '3D rotations and pose: orthogonal matrices for robots, drones and spacecraft'
short_title: 3D rotations and rigid-body pose
field_label: Robotics, aerospace guidance and attitude control, computer vision, animation
tier_note: 'rotations are 3 × 3 orthogonal matrices with determinant +1, poses are 4 × 4 homogeneous
  matrices, and composing them is multiplication. Quaternions and the rotation group as a Lie group are
  the Tier 3 extensions.'
nav_field: Control & Robotics
field: Engineering
subfield: Robotics/graphics
tier: 1
tier_ceiling: 3
prereq_beyond_la: Lie groups and quaternions if pushed further
scalar_field: R
vector_space: 'vectors in R^3 (directions, positions, angular axes). A rotation is a 3 × 3 matrix in
  the set SO(3) of orthogonal matrices with determinant +1. SO(3) is a group under multiplication but not
  a subspace of the 9-dimensional space of 3 × 3 matrices: the sum or average of two rotations is
  generally not a rotation. Poses (rotation plus position) are 4 × 4 matrices in SE(3), acting on
  homogeneous coordinates (x, y, z, 1)'
underlying_equations: 'Matrix products: v′ = R v for a rotation, and p′ = T p for a pose in homogeneous
  coordinates'
core_la_object: Orthogonal matrices with determinant +1
la_concepts: orthogonal matrices; determinant; composition and noncommutativity; change of basis;
  homogeneous coordinates; inverse as transpose; groups vs subspaces
primary_method: Dense small products
matrix_structure: orthogonal 3 × 3; SE(3) 4 × 4 with bottom row (0, 0, 0, 1)
typical_size: 3 × 3 and 4 × 4, chained 6-20 deep in a robot arm
worked_example_size: two 90° turns in both orders; gimbal lock at 90° pitch; averaging two rotations
terminology:
  attitude / orientation: a rotation matrix R relating a body frame to a reference frame
  direction cosine matrix (DCM): the rotation matrix; its entries are cosines of angles between axes
  body frame vs world frame: two orthonormal bases; R changes coordinates from one to the other
  yaw, pitch, roll (Euler angles): coordinates on the set of rotations, R = R_z(ψ) R_y(θ) R_x(φ)
  gimbal lock: Euler angles at which two of the three angles turn about the same axis
  pose (frame, transform): a rotation and a translation together, a 4 × 4 matrix in SE(3)
  forward kinematics: the product of the joint transforms along a robot arm
  homogeneous transformation: the 4 × 4 matrix [R t; 0 1]
  re-orthonormalization: projecting a drifted matrix back onto the orthogonal matrices
  handedness: the sign of the determinant; +1 for rotations, −1 for reflections
---

## Start here

A robot arm, a drone, a satellite and a character in an animated film all have to keep track of which
way they are facing. The usual way to describe an orientation is to say where an object's own
front, left and up directions point, measured in the coordinates of the room, the Earth or the stars.

Those three directions are always perpendicular to each other and always of unit length, because
turning an object cannot bend or stretch it. Written as the columns of a three-by-three table of
numbers, they form a rotation matrix. Turning an object twice is multiplying two such matrices, and,
as anyone who has rotated a book about two different axes knows, the order of the turns matters.

The popular alternative, three angles called yaw, pitch and roll, is easier to read but has a famous
flaw. At one particular pitch, two of the three angles start turning the object about the same axis,
and one direction of motion simply disappears from the description. Spacecraft guidance systems had to
be designed around that flaw. The matrix description has no such blind spot, but it has its own trap,
which this entry ends with.

## The problem

Represent the orientation of a rigid body in three dimensions, combine successive rotations, convert
vectors between the body's own axes and a fixed reference frame, track position and orientation
together (pose) along a chain of joints, and avoid the failure modes of angle-based descriptions.

## Variables

| Symbol | Name | What it holds | Shape | Units |
|---|---|---|---|---|
| R | rotation matrix | its columns are the body's x, y and z axes, written in reference-frame coordinates | 3 × 3 | dimensionless |
| v | vector | a direction or displacement | 3 × 1 | metres, or dimensionless for directions |
| R_x(φ), R_y(θ), R_z(ψ) | elementary rotations | turns about the x, y or z axis by the given angle | 3 × 3 | dimensionless |
| φ, θ, ψ | roll, pitch, yaw | Euler angles, here in the z-y-x convention | scalars | radians or degrees |
| t | position | where the body's origin sits in the reference frame | 3 × 1 | metres |
| T | pose | the 4 × 4 matrix [R t; 0 0 0 1] | 4 × 4 | mixed: R dimensionless, t in metres |
| p | homogeneous point | (x, y, z, 1) | 4 × 1 | metres in the first three entries |
| I | identity matrix | — | 3 × 3 | — |

## Formulation

**Where the equations come from.** The model is the geometry of rigid motion: a rotation preserves
lengths and angles and does not turn left-handed into right-handed.

**What makes a matrix a rotation.** Preserving lengths and angles means preserving dot products, so
(R u) · (R v) = u · v for all u and v. That is equivalent to

```
Rᵀ R = I
```

that is, the columns of R are orthonormal. Then det(R)² = 1, so det R = ±1. Rotations have det R = +1;
matrices with det R = −1 are reflections, which swap left and right. The condition Rᵀ R = I also says
that the inverse is the transpose, R⁻¹ = Rᵀ, so undoing a rotation costs nothing.

**The elementary rotations.** Turning about one coordinate axis leaves that axis alone and applies the
familiar 2D rotation to the other two coordinates. About the x-axis by φ, the y–z plane turns:

```
R_x(φ) = [ 1     0        0    ]
         [ 0   cos φ   −sin φ  ]
         [ 0   sin φ    cos φ  ]
```

About the y-axis by θ, the z–x plane turns:

```
R_y(θ) = [  cos θ   0   sin θ ]
         [    0     1     0   ]
         [ −sin θ   0   cos θ ]
```

About the z-axis by ψ, the x–y plane turns:

```
R_z(ψ) = [ cos ψ  −sin ψ   0 ]
         [ sin ψ   cos ψ   0 ]
         [   0       0     1 ]
```

The minus sign in R_y sits below the diagonal rather than above it. That is not a different
convention: a positive turn about y carries z toward x (the cyclic order x → y → z → x), and in the
usual x, y, z ordering of rows and columns that puts −sin θ in the bottom-left corner.

**Composition, and its order.** Applying R_1 and then R_2 is the product R_2 R_1, and it depends on the
order. Take the vector e_1 = (1, 0, 0) and two quarter turns:

```
R_x(90°) R_z(90°) e_1 = (0, 0, 1)     first about z, then about x
R_z(90°) R_x(90°) e_1 = (0, 1, 0)     first about x, then about z
```

**Euler angles.** Aerospace and robotics often describe an attitude by yaw ψ, pitch θ and roll φ, with

```
R = R_z(ψ) R_y(θ) R_x(φ)
```

Three numbers are enough, because a rotation matrix has nine entries but six independent constraints
(three unit lengths and three right angles), leaving three degrees of freedom.

**Worked case: gimbal lock.** At pitch θ = 90°, the product collapses. Computing it gives

```
R_z(ψ) R_y(90°) R_x(φ) = [   0    sin(φ − ψ)   cos(φ − ψ) ]
                         [   0    cos(φ − ψ)  −sin(φ − ψ) ]
                         [  −1        0             0     ]
```

which depends on yaw and roll only through their difference φ − ψ. Increasing both by the same amount
changes nothing: two of the three angles now turn the body about the same axis, and one direction of
rotation cannot be expressed by small changes of the angles at all. The orientation is fine; the
coordinates describing it have failed. A spacecraft guidance platform built from three physical gimbals
has the same failure mechanically, which is why the Apollo crews had to keep their spacecraft away from
that orientation.

**Pose.** Position and orientation together act on homogeneous coordinates, exactly as in the 2D
affine-transforms entry:

```
T = [ R   t ]        T p = (R (x, y, z) + t, 1)        T⁻¹ = [ Rᵀ   −Rᵀ t ]
    [ 0   1 ]                                                [ 0      1   ]
```

A robot arm's forward kinematics is the product T_1 T_2 ⋯ T_k of the transforms of its joints, read
from the base out to the gripper.

## Matrix structure

Rotations are dense 3 × 3 orthogonal matrices with determinant +1; poses are 4 × 4 with bottom row
(0, 0, 0, 1). Both sets are closed under multiplication and inversion, which makes them groups, SO(3)
and SE(3). Neither is closed under addition or scaling, so neither is a vector space, and that fact is
the pitfall below.

## What is computed

Products of small matrices: composing joint transforms, converting sensor readings from a body frame to
a world frame (v_world = R v_body) and back (v_body = Rᵀ v_world). Flight software and robot
controllers do this thousands of times per second. Long chains of products accumulate rounding error,
so software periodically re-orthonormalizes R, for example with Gram–Schmidt on its columns, and many
systems store orientations as quaternions instead.

## Why linear algebra is the right tool

A rotation is a change between two orthonormal bases, the body's axes and the reference axes, and
everything follows from that. Its matrix has the new axes as columns; its inverse is its transpose
because the bases are orthonormal; composing rotations multiplies matrices, so order matters; and a
pose is a rotation plus a translation, which homogeneous coordinates turn into one matrix. Gimbal lock
is understood as a failure of a coordinate system on the set of rotations, not of the rotations, which
is why the cure is a better description rather than a better angle.

## Pitfall worth teaching

Rotations are not a subspace, so the operations that work on vectors do not work on rotations.
Averaging two rotation matrices entry by entry does not give a rotation halfway between them. The
average of the identity and R_z(180°) is diag(0, 0, 1), which squashes every vector onto the z-axis and
is not invertible. The average of the identity and R_z(60°) has determinant 0.75 and shrinks vectors in
the xy-plane to about 87% of their length, although the rotation halfway between them, R_z(30°), shrinks
nothing. The same failure appears when animating by interpolating matrix entries, when smoothing noisy
attitude estimates with an ordinary filter, and when integrating small rotation updates by addition:
the result drifts away from orthogonality and objects visibly shrink or shear. Interpolating the angle
works for rotations about one fixed axis; in general it needs quaternions or the rotation group's own
geometry (the Tier 3 extensions).

## Extensions

Unit quaternions represent rotations with four numbers and no gimbal lock, and interpolating them
(slerp) gives the "halfway rotation" that averaging matrices does not. The rotation group SO(3) is a Lie
group, and small rotations correspond to skew-symmetric matrices, the setting of modern attitude
estimation and robot control (Tier 3). Rotation averaging in multiple-view geometry estimates many
camera orientations at once (the multiple-view geometry entry). The 2D affine-transforms entry is the
planar case of the pose matrix, and the 3D viewing entry adds the perspective projection that takes
poses to the screen. Inertial navigation uses R to rotate accelerometer readings into the world frame
before integrating them (the Kalman filtering entry).
