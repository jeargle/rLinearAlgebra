---
id: 52
slug: mass-balance-in-a-chemical-process-flowsheet
status: written
title: 'Process mass balances: a recycle loop is what makes it a system of equations'
short_title: Mass balance in a chemical process flowsheet
field_label: Chemical engineering, process design, plant operations
tier_note: with fixed conversions and split fractions every balance is linear, and the flowsheet is
  one square linear system. Why the unit-by-unit recycle iteration converges, and how fast, is a
  spectral-radius question and Tier 2.
nav_field: Chemistry & Chemical Engineering
field: Engineering
subfield: Chemical engineering
tier: 1
tier_ceiling: 2
prereq_beyond_la: ''
scalar_field: R, with physical flows restricted to nonnegative values
vector_space: 'R^6 in the worked case: one coordinate per unknown component flow, a component in a
  given stream (mol/h of A in the reactor feed, mol/h of B in the product, and so on). A stream is not a
  single coordinate; it contributes one coordinate per component it carries'
underlying_equations: 'Steady-state balances for each unit and each component: input + generation =
  output + consumption, with fixed conversions and split fractions'
core_la_object: Small dense linear system with recycle coupling
la_concepts: linear systems; rank and consistency; redundant equations; degrees of freedom; fixed-point
  iteration as a Neumann series
primary_method: Simultaneous linear solve; sequential iteration around the recycle
matrix_structure: sparse square system, block triangular except for the recycle coupling
typical_size: 6 × 6 by hand; 1e3-1e5 equations in plant-wide models
worked_example_size: mixer, reactor and separator with an unreacted-feed recycle
terminology:
  stream: a pipe between units; contributes one unknown per component it carries
  component balance: one row of the system, for one component around one unit
  overall (total) balance: the sum of the component balances, a linearly dependent row
  single-pass conversion: the fraction of the reactant entering the reactor that reacts, a fixed
    coefficient
  split fraction: the fraction of a component a separator sends to a given outlet, a fixed coefficient
  recycle stream: the coupling that turns a triangular system into a genuinely simultaneous one
  tear stream: the unknown guessed to start the unit-by-unit iteration around a loop
  sequential modular vs equation-oriented simulation: fixed-point iteration around loops vs solving the
    whole linear system at once
  degrees of freedom: unknowns minus independent equations; it must be zero for a unique answer
  purge stream: a small bleed that keeps an inert component from accumulating in the loop
---

## Start here

A chemical plant is a network of units connected by pipes: mixers that combine streams, reactors that
convert one substance into another, and separators that split a stream into its parts. The first job in
designing or running one is bookkeeping. Every hour, how much of each substance flows through each
pipe?

The rule is simple: with the plant running steadily, whatever goes into a unit comes out, except for
what the reaction makes or uses up. Applying it to each substance at each unit gives one equation each.

Without loops this is easy: start at the feed and work forward, one unit at a time. Real plants almost
always recycle, though. A reactor rarely converts all of its feed, so the separator sends the unreacted
material back to the front to try again. Now the reactor's feed depends on the separator's output,
which depends on the reactor. The equations can no longer be solved one at a time. They have to be
solved together, which makes the flowsheet a system of linear equations.

## The problem

Given the fresh feed to a process and the performance of each unit (how much of each reactant
converts, and how each separator divides each component), find the flow of every component in every
stream, and check that the specification determines them uniquely.

## Variables

| Symbol | Name | What it holds | Shape | Units |
|---|---|---|---|---|
| F | fresh feed | pure A fed to the process | scalar | mol/h |
| X | single-pass conversion | fraction of the A entering the reactor that becomes B | scalar in (0, 1) | dimensionless |
| s | recycle split fraction | fraction of the separator's A sent back to the mixer | scalar in [0, 1) | dimensionless |
| A_1, A_2, A_3, A_4 | flows of A | in the reactor feed (1), reactor outlet (2), product (3) and recycle (4) | scalars | mol/h |
| B_2, B_3 | flows of B | in the reactor outlet (2) and product (3) | scalars | mol/h |
| u | unknown vector | (A_1, A_2, B_2, A_3, B_3, A_4) | 6 × 1 | mol/h |
| K | balance matrix | one row per independent balance | 6 × 6 | dimensionless |
| r | known terms | the fresh feed in the row it enters, zeros elsewhere | 6 × 1 | mol/h |

## Formulation

**Where the equations come from.** For a unit running at steady state, the familiar balance of
chemical engineering holds for each component:

```
input + generation = output + consumption
```

Mixers and separators neither generate nor consume, so for them input equals output. In the reactor,
the reaction A → B consumes A and generates the same number of moles of B. With conversions and split
fractions fixed by the design, every balance is linear in the unknown flows.

**The flowsheet.** Fresh feed F of pure A joins the recycle in a mixer (stream 1), passes through the
reactor (stream 2), and a separator sends all of the B and a fraction 1 − s of the A to the product
(stream 3) and returns the remaining fraction s of the A to the mixer (stream 4). One balance per
component per unit:

```
mixer, A:      A_1 = F + A_4
reactor, A:    A_2 = (1 − X) A_1
reactor, B:    B_2 = X A_1
separator, A:  A_4 = s A_2        and   A_3 = (1 − s) A_2
separator, B:  B_3 = B_2
```

Moved to one side, these six equations are K u = r, a square system in the six unknown component flows.

**Worked case.** Take F = 100 mol/h, X = 0.75 and s = 0.8. Substituting around the loop,

```
A_1 = 100 + 0.8 × 0.25 × A_1 = 100 + 0.2 A_1     ⟹     A_1 = 125
```

and then A_2 = 31.25, B_2 = 93.75, A_4 = 25, A_3 = 6.25 and B_3 = 93.75 mol/h. The reactor converts
only 75% of what it receives, but the process converts 93.75% of its fresh feed, because unreacted A
gets further passes. Balances check: 100 mol/h of A enters, and 6.25 of A plus 93.75 of B leave.

**Solving unit by unit.** Process simulators often do not form K. They guess the recycle (the tear
stream), compute each unit in turn, and update the guess. Here that is A_4 ← 0.2 (100 + A_4), which
from A_4 = 0 gives 20, 24, 24.8, 24.96, … → 25. Each pass multiplies the error by 0.2, the fraction of
A that survives one trip round the loop. This is the same sum of rounds as the Leontief entry's
d + A d + A² d + ⋯, and it converges because that loop gain is less than 1.

## Matrix structure

`K` is square and sparse. Without the recycle it would be triangular: each unit's outputs depend only
on units upstream, and forward substitution solves it. The recycle adds a single entry above the
diagonal (A_4 appearing in the mixer's row), and that entry is what makes the system simultaneous.
Plant-wide models have thousands of such rows, with sparsity reflecting which units are connected.

## What is computed

For a design calculation, the solution of K u = r, either directly (equation-oriented simulators) or by
fixed-point iteration around each loop, often accelerated (sequential modular simulators such as Aspen
Plus). Before solving, engineers do a degrees-of-freedom analysis: count the unknowns and the
independent equations and make sure the specifications close the gap exactly.

## Why linear algebra is the right tool

The degrees-of-freedom analysis taught in every process-design course is a rank computation: a unique
solution needs as many independent equations as unknowns, which is a square system with an invertible
matrix. Over-specifying a process gives an inconsistent system, under-specifying it leaves free
variables, and an extra equation that adds no information is a dependent row. Recycle loops, which
make hand calculation tedious, are just off-diagonal entries, and the convergence of the unit-by-unit
calculation is a property of the loop's coefficients.

## Pitfall worth teaching

Balances can be linearly dependent, and counting them is not the same as counting independent
equations. Around any unit, the total mass balance is the sum of the component balances, so writing all
of them gives one equation too many. A solver that is handed the redundant set sees a non-square system.
If the numbers come from plant measurements rather than design values, they almost never satisfy the
redundant equation exactly, so the system is inconsistent and has no solution at all. The fix is to
count rank, not equations: keep an independent set for design calculations, and for measured data use
the redundancy deliberately in data reconciliation, a least-squares adjustment of the measurements so
they satisfy every balance. A related failure is an inert component in the feed with no way out: with
s = 1 for that component, its loop gain is 1, the matrix is singular, and no steady state exists, which
is why plants add a purge stream.

## Extensions

Once conversions depend on temperature, or separations on vapour–liquid equilibrium, the balances
become nonlinear and are solved by Newton's method, a sequence of linear systems with this structure.
Data reconciliation is a constrained least-squares problem (compare the regression entry). The same
conservation-at-nodes structure, without reactions, is the traffic-flow entry. With reactions written
out species by species, it is the stoichiometric-matrix entry, and the recycle iteration is the same
Neumann series as the Leontief entry.
