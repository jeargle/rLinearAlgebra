---
id: 4
slug: stoichiometric-matrices-of-reaction-networks
status: seed
title: 'Stoichiometric matrices: what a reaction network can and cannot do at steady state'
short_title: Stoichiometric matrices of reaction networks
field_label: Chemistry, chemical engineering, systems biology
tier_note: 'the matrix S is read out of the ODE dc/dt = S v(c), and conservation laws are statements about
  that ODE''s solutions. On-ramp: chemical-equation balancing, a null-space problem with no ODE.'
nav_field: Chemistry & Chemical Engineering
field: Chemistry
subfield: Chem-eng/systems biology
tier: 3
tier_ceiling: 3
prereq_beyond_la: ordinary differential equations (nonlinear kinetics)
scalar_field: Q or R (S itself has integer entries)
vector_space: fluxes in R^r (r reactions); concentrations in R^m (m species); S maps flux space to species
  space - two different spaces that are easy to conflate
underlying_equations: Nonlinear ODE system dc/dt = S v(c); every linear-algebra conclusion uses only the
  constant matrix S
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

## Variables

| Symbol | Name | What it holds | Shape | Units |
|---|---|---|---|---|
| m | number of species | distinct chemicals in the network | integer | — |
| r | number of reactions |  | integer | — |
| c(t) | concentration vector | amount of each species per unit volume at time t | m × 1 | mol/L (M), often mM |
| v | flux (rate) vector | how many times per unit time, per unit volume, each reaction occurs | r × 1 | mol L⁻¹ s⁻¹; genome-scale models use mmol per gram dry weight per hour |
| S | stoichiometric matrix | s_ij is the number of molecules of species i produced (positive) or consumed (negative) each time reaction j occurs | m × r | dimensionless (molecules per reaction event) |
| k | rate constants | kinetic parameters inside v(c) | varies | depend on reaction order |
| y | conservation vector | weights for which yᵀc never changes, such as the number of phosphate groups in each species | m × 1 | dimensionless |
| Z | atom-count matrix | z_ei is the number of atoms of element e in one molecule of species i | (number of elements) × m | atoms per molecule |
| s | a single reaction's coefficients | the column being solved for when balancing one equation | m × 1 | molecules |

Flux vectors live in ℝʳ, one entry per reaction; concentration vectors live in ℝᵐ, one entry per species. S maps the first space into the second. Keeping the two apart is most of the work of reading this entry.

## Formulation

**Where the equations come from.** Each species' concentration changes at a rate equal to the sum over reactions of (molecules produced or consumed per event) × (events per unit time). That is a system of m ordinary differential equations:

```
dc/dt = S v(c)
```

S is a constant matrix fixed by the chemistry. The fluxes v(c) are the kinetics, and they are generally nonlinear. For example, under mass action the reaction A + B → C runs at v = k c_A c_B. So the ODE itself is nonlinear, and solving it requires rate constants that are rarely known. The linear algebra here extracts what holds for every possible choice of kinetics.

**Steady state.** A cell in steady operation has dc/dt = 0:

```
S v = 0
```

This models every species being produced exactly as fast as it is consumed. Whatever the kinetics are, any steady-state flux vector lies in the null space of S.

**Conservation laws.** If a vector y satisfies yᵀS = 0, then

```
d(yᵀc)/dt = yᵀ S v = 0      ⟹      yᵀc(t) = yᵀc(0)   for all t
```

This is a statement about the solutions of the nonlinear ODE, obtained without knowing v. Each independent left-null vector removes one degree of freedom, and every trajectory stays on the affine subspace c(0) + range(S) (the stoichiometric compatibility class), whose dimension is rank(S).

**Balancing a single reaction.** Atoms are neither created nor destroyed, so a reaction's coefficients s must satisfy Z s = 0: for each element, atoms consumed equal atoms produced. Balancing an equation means finding an integer vector in the null space of Z.

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
