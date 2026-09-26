---
id: 4
slug: stoichiometric-matrices-of-reaction-networks
status: seed
title: 'Stoichiometric matrices: what a reaction network can and cannot do at steady state'
short_title: Stoichiometric matrices of reaction networks
field_label: Chemistry, chemical engineering, systems biology
tier_note: null spaces and rank, nothing more. Chemical-equation balancing is the Tier 1 entry point;
  flux balance analysis is Tier 2.
nav_field: Chemistry & Chemical Engineering
field: Chemistry
subfield: Chem-eng/systems biology
tier: 1
tier_ceiling: 2
prereq_beyond_la: ''
scalar_field: Q or R (S itself has integer entries)
vector_space: fluxes in R^r (r reactions); concentrations in R^m (m species); S maps flux space to species
  space - two different spaces that are easy to conflate
core_la_object: Null spaces and rank of an integer matrix
la_concepts: right null space; left null space; rank; conservation laws
primary_method: Nullspace basis; rational/integer arithmetic
matrix_structure: sparse integer, rank-deficient
typical_size: 2e3 x 3e3 (genome scale)
worked_example_size: glycolysis core model
terminology:
  stoichiometric matrix S: species by reactions, signed integer coefficients
  flux: v, the vector of reaction rates
  steady state: Sv = 0 — v lies in the right null space
  conserved moiety: a left null vector y; y^T c is constant for all time
  elementary flux mode: an extreme ray of the nonnegative part of the null space
  degrees of freedom of the network: the nullity of S
  balancing an equation: finding an integer null vector of the element-by-species matrix
---

## Start here

A living cell runs thousands of chemical reactions at once. Write down a table: one row per chemical,
one column per reaction, and in each cell how many molecules that reaction consumes or produces. That
table is the entire bookkeeping of the cell's chemistry — and notably, it says nothing about how *fast*
anything happens.

Two questions turn out to be answerable from the table alone. First: which combinations of reaction
rates leave every chemical's concentration unchanged? A cell in steady operation must be running one of
these; everything produced is consumed at the same rate. Second: are there quantities that never change
no matter what the rates are? Total phosphate, say, or the total amount of an enzyme across all its
forms — these are conserved by the structure of the chemistry, not by any tuning of the speeds.

This matters because reaction rates are extremely hard to measure and the table is easy to write down.
You get real conclusions from the cheap information.

## The problem

Given a network of chemical reactions, determine which combinations of reaction rates are compatible with steady state, which quantities are conserved no matter what the kinetics are, and how many reactions are genuinely independent.

## Formulation

Build the stoichiometric matrix `S` with one row per species and one column per reaction, entries being signed stoichiometric coefficients. Species concentrations evolve as

```
dc/dt = S v
```

with `v` the flux vector. Steady state means `S v = 0`.

## Matrix structure

Sparse, integer-valued, typically rank-deficient in both directions. Genome-scale metabolic models reach ~2,000 species × ~3,000 reactions.

## What is computed

- **Right null space** of `S`: the space of steady-state flux distributions. Its dimension counts the network's degrees of freedom; its nonnegative extreme rays are the elementary flux modes.
- **Left null space** of `S`: conservation laws. A vector `y` with `yᵀS = 0` means `yᵀc` is constant for all time, independent of rate constants — conserved moieties like total ATP+ADP+AMP, or total enzyme.
- **Rank** of `S`: the number of independent reactions, which is what distinguishes an overdetermined mechanism from an underdetermined one.

## Why linear algebra is the right tool

These conclusions hold without knowing a single rate constant. Structural conclusions from the network topology alone are exactly what null spaces deliver, and kinetic parameters are the hardest thing to measure.

## Pitfall worth teaching

Balancing a chemical equation is finding an integer vector in the null space of the element–species matrix — the same operation students do by trial and error in first-year chemistry. Showing that equivalence is a good hook.

## Extensions

Flux balance analysis adds a linear objective and flux bounds, turning the null space into a linear program. Chemical reaction network theory (Feinberg) uses the *deficiency*, a rank-based integer, to predict whether multiple steady states are possible.
