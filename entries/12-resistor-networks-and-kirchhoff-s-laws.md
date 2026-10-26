---
id: 12
slug: resistor-networks-and-kirchhoff-s-laws
status: written
title: 'Resistor networks: Kirchhoff''s laws as a graph Laplacian'
short_title: Resistor networks and Kirchhoff's laws
field_label: Electrical engineering, circuit theory, chip power-grid analysis
tier_note: a DC network of resistors is one symmetric linear system L φ = s, and grounding a node is
  removing a one-dimensional null space. Effective resistance through the pseudoinverse and its link to
  random walks are Tier 2.
nav_field: Electrical Engineering
field: Physics
subfield: Circuit theory
tier: 1
tier_ceiling: 2
prereq_beyond_la: ''
scalar_field: R
vector_space: 'two different spaces: node potentials in R^n (n nodes) and edge currents in R^m (m resistors).
  The incidence matrix maps the first to the second. Potentials are only defined up to adding the same
  constant to every node, so physically they live in R^n modulo the all-ones vector'
underlying_equations: 'Algebraic circuit laws: Ohm''s law (V = IR) for each resistor and Kirchhoff''s current law at each node'
core_la_object: Graph Laplacian as a physical operator
la_concepts: incidence matrix; Laplacian L = A^T C A; null space and grounding; column space and the
  solvability condition; cycle space; effective resistance; pseudoinverse
primary_method: Sparse Cholesky of the grounded Laplacian; preconditioned conjugate gradient at scale
matrix_structure: sparse symmetric positive semidefinite, rows summing to zero, rank n-1 when connected
typical_size: 1e3-1e6 nodes (1e8 for on-chip power grids)
worked_example_size: 4-node Wheatstone bridge
terminology:
  node voltage (potential): one entry of the vector φ in R^n
  ground (reference node): the node whose potential is fixed at 0, removing the null space spanned by
    the all-ones vector
  nodal conductance (admittance) matrix: the weighted graph Laplacian L = A^T C A
  Kirchhoff's current law (KCL): A^T I = s, a statement about the left null space of A
  Kirchhoff's voltage law (KVL): voltage drops lie in the column space of A, so they sum to zero around
    every loop
  loop (mesh) currents: coordinates in a basis of the cycle space, the null space of A^T, dimension m - n
    + 1
  nodal analysis vs mesh analysis: solving in potential space (dimension n - 1) vs in cycle space (dimension
    m - n + 1)
  effective (Thevenin) resistance: (e_a - e_b)^T L^+ (e_a - e_b), a quadratic form in the pseudoinverse
  superposition: linearity of the solution map s -> φ
  reciprocity: symmetry of L, so the potential at b due to a source at a equals the potential at a due
    to the same source at b
  bridge balance: a choice of resistances that puts one edge current at zero
---

## Start here

A circuit board, a strain gauge, or the metal wiring that carries power across a computer chip can be
pictured as wires meeting at junctions, with a resistor on each wire. Push current in at one junction
and take it out at another: how much current flows along each wire, and what is the voltage at every
junction?

Two rules decide it. First, current through a resistor is proportional to the voltage difference across
it. Second, at every junction, the current flowing in equals the current flowing out, because charge does
not pile up. Write the second rule once per junction and substitute the first, and you get one equation
per junction with the junction voltages as the unknowns.

One thing is odd about the answer. Raising every voltage by the same amount changes no current, because
only differences matter. So the equations cannot pin down the voltages until one junction is declared
to be zero, which is what electricians call ground. In linear algebra terms, that missing piece of
information is a null space, and choosing a ground is how it is removed.

## The problem

Given a network of resistors and the currents injected at some nodes (or the voltages held fixed at
some nodes by sources), find the potential at every node and the current through every resistor. A
common special case is to find the single resistance the whole network presents between two terminals.

## Variables

| Symbol | Name | What it holds | Shape | Units |
|---|---|---|---|---|
| n | number of nodes | junctions in the network | integer | — |
| m | number of edges | resistors, each joining two nodes | integer | — |
| R_e | resistance of edge e | — | scalar per edge | ohms (Ω) |
| C | conductance matrix | diagonal, with 1/R_e for each edge | m × m | siemens (S) |
| A | incidence matrix | row e has +1 at the node where edge e starts and −1 where it ends (the direction is an arbitrary bookkeeping choice) | m × n | dimensionless |
| φ | node potentials | the voltage at each node, relative to an arbitrary reference | n × 1 | volts (V) |
| v | voltage drops | v = A φ, the drop along each edge in its chosen direction | m × 1 | volts |
| I | edge currents | current through each resistor, positive in the edge's direction | m × 1 | amperes (A) |
| s | injected currents | current fed into each node from outside; 0 at internal junctions | n × 1 | amperes |
| L | Laplacian (nodal conductance matrix) | L = Aᵀ C A | n × n | siemens |
| 1 | all-ones vector | — | n × 1 | — |
| R_eff | effective resistance | the resistance the whole network presents between two nodes | scalar | ohms |

Potentials and currents live in different spaces: φ has one entry per node and I has one entry per
edge. The incidence matrix A carries potentials to edge drops, and its transpose Aᵀ carries edge
currents back to node totals.

## Formulation

**Where the equations come from.** A direct-current network of
resistors is described by two algebraic laws, one per edge and one per node.

**Ohm's law, one equation per edge.** For a single resistor, Ohm's law is the familiar V = IR: the
voltage V across it equals the current I through it times its resistance R. Solved for the current,
I = V/R. With the drops v = A φ in place of V and the conductances 1/R_e on the diagonal of C, all m
resistors at once read

```
I = C A φ
```

Row e reads I_e = (φ_start − φ_end) / R_e, which is V = IR for resistor e.

**Kirchhoff's current law, one equation per node.** Charge does not accumulate at a junction, so the
current leaving each node through its resistors equals the current injected there from outside:

```
Aᵀ I = s
```

Row i of Aᵀ adds the currents on edges leaving node i and subtracts those on edges arriving.

**The node equations.** Substituting the first law into the second gives one symmetric system in the
potentials alone:

```
L φ = s,     L = Aᵀ C A
```

Entry L_ii is the total conductance of the resistors touching node i, and L_ij is minus the conductance
of the resistor joining i and j (0 if there is none). This is the weighted Laplacian of the network
graph, and in circuit theory it is called the nodal conductance or admittance matrix.

**The null space, and grounding.** Every row of L sums to zero, so L 1 = 0: adding the same constant to
every potential changes no drop and no current. For a connected network the null space is exactly the
span of 1, so the rank of L is n − 1 and the potentials are determined only up to that constant. Fixing
one node's potential at 0 (grounding it) and deleting its row and column leaves an (n − 1) × (n − 1)
matrix that is symmetric positive definite and therefore invertible.

**The solvability condition.** L φ = s has a solution only if s is in the column space of L, which for a
symmetric matrix is the orthogonal complement of its null space. Here that means 1ᵀ s = 0: the injected
currents must add up to zero, because whatever current goes in must come out somewhere. The
mathematics and the physics state the same condition.

**Effective resistance.** Inject 1 A at node a and remove it at node b, so s = e_a − e_b. The resulting
potential difference φ_a − φ_b, in volts per ampere, is the effective resistance between the two nodes.

**Worked case: a Wheatstone bridge.** Four nodes: the top a, two middle nodes b and c, and the bottom g.
The resistors are a–b 100 Ω, a–c 150 Ω, b–g 200 Ω, c–g 300 Ω, and a 50 Ω meter across b–c. A 10 V
source holds φ_a = 10 V and φ_g = 0 V. With the known potentials moved to the right-hand side, the two
equations for the unknown middle nodes are

```
(1/100 + 1/200 + 1/50) φ_b − (1/50) φ_c = 10/100
−(1/50) φ_b + (1/150 + 1/300 + 1/50) φ_c = 10/150
```

and their solution is φ_b = φ_c = 20/3 V, so no current flows through the meter. The bridge is
balanced, because 100/200 = 150/300. Change the 300 Ω resistor to 330 Ω, as a strain gauge does when it
is stretched, and about 0.95 mA flows through the meter. Measuring that current is how a strain gauge,
a load cell, or a pressure sensor turns a tiny resistance change into a reading.

## Matrix structure

`L` is sparse, with one nonzero per node on the diagonal and two off-diagonal nonzeros per resistor. It
is symmetric positive semidefinite with zero row sums, and singular with rank n − (number of connected
components). After grounding it is symmetric positive definite and diagonally dominant, the best-behaved
kind of large linear system there is.

## What is computed

Ground a node (or eliminate every node held at a known voltage), then solve the remaining symmetric
positive definite system. Circuit-sized problems use a sparse Cholesky factorization. The power grids
that deliver current across a modern chip have tens of millions of nodes, and checking them for voltage
droop is done with preconditioned conjugate gradient or multigrid. Graph theory has its own fast
Laplacian solvers, which run in nearly linear time in the number of edges.

## Why linear algebra is the right tool

Each of the circuit-theory rules is a statement about the four fundamental subspaces of the incidence
matrix A. Kirchhoff's voltage law says that edge drops are in the column space of A. Kirchhoff's current
law constrains Aᵀ I. Ground is the null space of A, and the loops that mesh analysis works with form a
basis of the null space of Aᵀ, whose dimension m − n + 1 counts the independent loops. The textbook
choice between nodal analysis and mesh analysis is a choice of which of two complementary subspaces to
solve in: nodal analysis needs n − 1 unknowns, mesh analysis needs m − n + 1, and engineers pick
whichever is smaller. Reciprocity, the surprising fact that swapping where a source is applied and where
the response is measured gives the same reading, is just the symmetry of L.

## Pitfall worth teaching

Two mistakes produce a singular or meaningless system. The first is forgetting to ground. L itself is
singular, so a direct solver either fails or, worse, returns potentials offset by an arbitrary constant
because of rounding. The second is inconsistent sources: injected currents that do not sum to zero put s
outside the column space, and no potentials satisfy the equations. Voltage sources need a third kind of
care. A node whose voltage is fixed is not an unknown, so its known potential moves to the right-hand
side, as in the bridge example. The current the source supplies is unknown, so that node's row of
L φ = s cannot be used as an equation; it gives the source current afterwards. Keeping that row with
s set to 0 is a common source of wrong answers. In each case the system was set up before deciding which
quantities are known, which are unknown, and what fixes the free constant.

## Extensions

Effective resistance between every pair of nodes can be read from the pseudoinverse L⁺, and it equals
the expected time for a random walk to go from one node to the other and back, divided by twice the
total conductance; both facts are Tier 2. The same Laplacian appears as the Y-bus matrix of power-grid
load flow, in modified nodal analysis inside circuit simulators such as SPICE, and in spectral graph
clustering, where its eigenvectors rather than its solves are the object of interest. Adding capacitors
and inductors turns the network equations into ODEs; with sinusoidal sources, phasors turn them back into
a complex linear system (the AC circuits entry, Tier 3). The same incidence-matrix structure, with flows
and conservation at nodes, appears in the traffic-flow and process mass-balance entries.
