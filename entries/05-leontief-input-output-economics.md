---
id: 5
slug: leontief-input-output-economics
status: seed
title: 'Leontief input–output: how much steel does a car actually take?'
short_title: Leontief input-output economics
field_label: Economics (and, in its modern form, environmental footprint accounting)
tier_note: posing and solving `(I − A)x = d` needs only a linear solve. The Perron–Frobenius convergence
  condition lifts it to Tier 2.
nav_field: Economics, Finance & Operations Research
field: Economics
subfield: Macroeconomics/EEIO
tier: 1
tier_ceiling: 2
prereq_beyond_la: ''
scalar_field: R (nonnegative)
vector_space: outputs and demands in R^n, n = number of sectors
core_la_object: Nonnegative matrix and its resolvent
la_concepts: matrix inverse; Neumann series; Perron-Frobenius; spectral radius
primary_method: Dense LU; Neumann expansion
matrix_structure: nonnegative, column sums < 1
typical_size: 400-500 sectors (1e4 multiregion)
worked_example_size: 5-sector toy economy
terminology:
  technical coefficient matrix A: input from sector i per unit output of sector j
  final demand: the right-hand side d
  gross / total output: the unknown x
  Leontief inverse: (I - A)^-1
  multiplier: a single entry of the Leontief inverse
  productive economy: spectral radius of A below 1, so the Neumann series converges
  direct vs indirect requirements: the successive terms A, A^2, A^3 of the Neumann series
  embodied / Scope 3 emissions: an appended satellite row multiplied through the same inverse
---

## Start here

Building a car takes steel. Making steel takes electricity. Generating electricity takes steel. The
requirements are circular, so you cannot just add them up — following the chain never terminates.

Suppose you want one more car delivered to a customer. You need some steel for it directly. But you also
need extra electricity to make that steel, and extra steel to make that electricity, and so on forever.
Each round is smaller than the last, so the total is finite; the question is what it adds up to.

Economists answer this by writing one equation per industry: total output equals what other industries
consume from it, plus what consumers finally take. Solving the system gives every industry's required
output at once, with the infinite chain of indirect requirements already accounted for.

The same computation, with pollution added as an extra row, is how the carbon footprint of a product is
usually estimated — including all the emissions from its suppliers' suppliers.

## The problem

Industries consume each other's output. Making a car needs steel; making steel needs electricity; making electricity needs steel. Given final consumer demand, find the total production every sector must run.

## Formulation

Let `A` be the technical-coefficient matrix, where `a_ij` is the input from sector `i` needed per unit of sector `j` output. Total output `x` satisfies

```
x = A x + d      ⟹      (I − A) x = d
```

## Matrix structure

Square, entrywise nonnegative, dense-ish, with column sums below 1 for a productive economy. National tables run 400–500 sectors; the global multi-region tables (EXIOBASE, WIOD) reach tens of thousands.

## What is computed

`(I − A)⁻¹`, the Leontief inverse, is the object of interest itself — entry `(i,j)` is the total output of `i` required per unit of final demand for `j`, summed over all supply-chain depths. The Neumann series

```
(I − A)⁻¹ = I + A + A² + A³ + …
```

has a direct reading: direct requirements, then requirements of requirements, and so on.

## Why linear algebra is the right tool

The circularity that makes the accounting hard by hand — steel needs electricity needs steel — is precisely what a matrix inverse resolves in closed form.

## Pitfall worth teaching

By Perron–Frobenius, the series converges exactly when the spectral radius of `A` is below 1. That is not a technical condition: it is the statement that the economy produces more than it consumes in production. A nonnegative matrix's dominant eigenvalue carries economic meaning.

## Extensions

Environmentally-extended I/O appends rows for CO₂, water, and land use, and the same inverse yields the full upstream carbon footprint of a product — this is how most corporate Scope 3 emissions are estimated. Same mathematics: Markov chain fundamental matrices, and structural path analysis.
