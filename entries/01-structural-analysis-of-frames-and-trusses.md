---
id: 1
slug: structural-analysis-of-frames-and-trusses
status: seed
title: 'Structural analysis: will the bridge hold, and at what frequency does it ring?'
short_title: Structural analysis of frames and trusses
field_label: Civil and mechanical engineering (finite element analysis)
tier_note: 'the matrix problem comes from the ODE system M ü + K u = f: statics sets ü = 0, vibration
  assumes harmonic motion. On-ramp: the static solve K u = f itself needs only first-course linear algebra.'
nav_field: Civil & Mechanical Engineering
field: Engineering
subfield: Civil/mechanical FEA
tier: 3
tier_ceiling: 3
prereq_beyond_la: ordinary differential equations (second order, from the PDE of linear elasticity)
scalar_field: R
vector_space: R^n, n = number of unrestrained degrees of freedom (2 or 3 per node); displacements and
  forces live in the same space
underlying_equations: Linear second-order ODE system M ü + K u = f, from the PDE of linear elasticity;
  statics sets ü = 0
core_la_object: Sparse SPD linear system and generalized eigenproblem
la_concepts: linear solve; symmetric positive definite; generalized eigenproblem; conditioning
primary_method: Sparse Cholesky; Lanczos
matrix_structure: symmetric, positive definite, sparse, banded
typical_size: 1e6-1e8 DOF
worked_example_size: 12-bar planar truss
terminology:
  stiffness matrix: the coefficient matrix K; symmetric positive definite once restraints are applied
  degree of freedom (DOF): one scalar unknown — one component of the displacement vector
  load vector: the right-hand side b
  restraint / boundary condition: deleting the corresponding rows and columns, or adding constraint rows
  assembly: summing small element matrices into the global matrix at shared DOF indices
  mode shape: an eigenvector of K phi = lambda M phi
  natural frequency: square root of the corresponding eigenvalue
  mechanism: a nontrivial null space of K — the structure can move with no restoring force
  bandwidth / skyline: the sparsity pattern induced by node numbering
---

## Start here

A bridge under load bends a little. Every joint shifts, and how far it shifts depends on how hard the
neighbouring members pull back. Each member behaves like a stiff spring: stretch it twice as far and it
pulls back twice as hard. That proportionality is the whole reason this problem is linear.

So write one equation per joint saying "the forces here balance". Each equation involves the movement of
that joint and of the joints connected to it — nowhere else, because a member can only pull on its own
two ends. Collect those equations and you have a system: known forces on one side, unknown movements on
the other, and a big table of spring constants in between. Solve it and you know how the structure
deforms.

The second question engineers ask is what happens with no load at all: let the structure wobble freely
and only certain shapes of wobble sustain themselves, each at its own frequency. Finding those special
shapes is what eigenvalues are for, and it is why bridges are checked against the frequencies of
marching feet and wind.

## The problem

Given a structure — truss, bridge deck, turbine blade, engine block — discretized into elements, find the displacement at every node under a given load, and separately find the frequencies at which the structure resonates.

## Variables

| Symbol | Name | What it holds | Shape | Units |
|---|---|---|---|---|
| n | number of degrees of freedom (DOFs) | count of unrestrained displacement components: 2 per free joint in a planar truss, 3 in a space truss | scalar (integer) | — |
| u | displacement vector | how far each joint moves, in each coordinate direction, from its unloaded position | n × 1 | m |
| f | load vector | external force applied at each joint in each direction: gravity, traffic, wind | n × 1 | N |
| K | global stiffness matrix | k_ij is the force that appears at DOF i when DOF j alone is displaced by one unit | n × n | N/m |
| k_e | element stiffness | stiffness of one bar along its axis, k_e = E A / L | scalar | N/m |
| E, A, L | Young's modulus, cross-sectional area, length | material stiffness and geometry of one bar | scalars | Pa (N/m²), m², m |
| M | mass matrix | how the structure's mass is distributed over the DOFs | n × n | kg |
| ü | acceleration vector | second time derivative of u | n × 1 | m/s² |
| φ | mode shape | the relative pattern of motion in one mode of vibration; only its shape matters, so it is normalized | n × 1 | dimensionless |
| ω | natural angular frequency | how fast a mode oscillates; the frequency in hertz is ω / 2π | scalar | rad/s |
| λ | eigenvalue | λ = ω² | scalar | s⁻² |

In a truss every DOF is a translation, so every entry of u is in metres. Frames and beams add rotational DOFs, and then u mixes metres with radians and f mixes newtons with newton-metres. The equations are unchanged, but entries of K then carry different units, which is one reason raw entry sizes of K should not be compared directly.

## Formulation

**Where the equations come from.** The underlying physics is linear elasticity: for small deformations, stress in a solid is proportional to strain, and the motion obeys a partial differential equation in space and time. The finite element method replaces the continuous structure by its n joint displacements, which turns that PDE into a system of n linear second-order ordinary differential equations in time:

```
M ü(t) + K u(t) = f(t)
```

Row i is Newton's second law for DOF i: mass times acceleration equals the applied force minus the elastic restoring force from the bars attached there. (Damping is omitted here; it adds a term C u̇.)

**Statics.** If loads are applied slowly and held, the structure comes to rest, ü = 0, and the ODE reduces to a linear system:

```
K u = f
```

This models force balance at every joint: row i says that the elastic forces from all the bars meeting at DOF i sum to the external load there. The solution u is the deformed shape. The force in each bar then follows from its change in length, k_e times elongation. The system has a unique solution only if the supports prevent every rigid-body motion; otherwise K is singular (see the pitfall below).

**Free vibration.** With no load, f = 0, look for solutions in which every DOF oscillates in step at one frequency, u(t) = φ cos(ωt). Then ü = −ω² φ cos(ωt), and substituting gives

```
K φ = λ M φ,     λ = ω²
```

A nonzero φ exists only for special values of λ, the eigenvalues. This is what the eigenproblem means for the ODE: there are exactly n such synchronized motions, the modes, and because the equations are linear, every free vibration is a superposition of them,

```
u(t) = Σ_i φ_i (a_i cos ω_i t + b_i sin ω_i t)
```

with the constants a_i, b_i fixed by the initial displacement and velocity. A load that oscillates near one of the ω_i drives that mode into resonance.

## Matrix structure

`K` is symmetric positive definite (after boundary conditions are applied), extremely sparse — each node couples only to its mesh neighbors — and often banded or block-structured. Industrial models run 10⁶–10⁸ degrees of freedom.

## What is computed

Sparse Cholesky with fill-reducing reordering (AMD, nested dissection) for the static solve; Lanczos or shift-and-invert Arnoldi for the lowest few dozen eigenpairs. Nobody forms `K⁻¹`.

## Why linear algebra is the right tool

The underlying PDE (linear elasticity) is linear in the small-strain regime, so superposition holds exactly: the response to a load combination is the combination of responses. Sparsity is a direct encoding of physical locality.

## Pitfall worth teaching

A near-singular `K` is not a numerical accident — it means the structure has a near-mechanism, a direction in which it can deform with almost no restoring force. The condition number is a physical diagnostic, not just a numerical one.

## Extensions

Buckling as a different generalized eigenproblem (`K φ = λ K_geometric φ`); substructuring and domain decomposition; the same modal analysis applied to molecules gives normal-mode analysis and elastic network models.
