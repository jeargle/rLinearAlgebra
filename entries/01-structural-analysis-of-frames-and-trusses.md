---
id: 1
slug: structural-analysis-of-frames-and-trusses
status: seed
title: 'Structural analysis: will the bridge hold, and at what frequency does it ring?'
short_title: Structural analysis of frames and trusses
field_label: Civil and mechanical engineering (finite element analysis)
tier_note: equilibrium is a plain `Ax = b` solve; rank and conditioning carry the insight. Modal analysis
  (Tier 2) is an extension.
nav_field: Civil & Mechanical Engineering
field: Engineering
subfield: Civil/mechanical FEA
tier: 1
tier_ceiling: 2
prereq_beyond_la: ''
scalar_field: R
vector_space: R^n, n = number of unrestrained degrees of freedom (2 or 3 per node); displacements and
  forces live in the same space
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

## Formulation

Assemble a global stiffness matrix `K` from per-element contributions. Static equilibrium is

```
K u = f
```

with `u` nodal displacements and `f` applied forces. Free vibration is the generalized symmetric eigenproblem

```
K φ = λ M φ,     ω = √λ
```

with `M` the mass matrix; eigenvectors `φ` are mode shapes.

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
