# Traffic flow: why counting cars at the edges leaves a free variable inside

### Start here

At every road intersection, the cars that drive in must drive out again, because cars do not pile up
or vanish in the middle of a junction (at least not for long). Traffic engineers count cars entering
and leaving a district at its edges and want to know how many use each street inside it.

Write the in-equals-out rule once for every intersection and you get a set of equations, one per
intersection, with the unknown street flows as the unknowns. Usually the equations do not pin down an
answer. Whenever the streets form a loop, some traffic could be circling the loop without ever entering
or leaving, and the edge counts cannot see it. So there is a whole family of possible answers, and
exactly as many numbers left undetermined as there are independent loops.

That family has a familiar shape from a first linear algebra course: one particular answer, plus any
amount of the circling traffic. On one-way streets flows cannot be negative, and that turns the family into a
range of admissible values: the smallest flow each street must carry, and where the remaining freedom
lies. Measuring one street inside the loop removes the uncertainty entirely.

**Field:** Transportation engineering, traffic monitoring, [network flow](https://en.wikipedia.org/wiki/Flow_network)  
**Tier:** 1 — conservation at each intersection is a linear system with more unknowns than independent equations, solved by elimination into a particular solution plus the [null space](https://en.wikipedia.org/wiki/Kernel_%28linear_algebra%29). Choosing among the admissible flows by optimization (network flow, [linear programming](https://en.wikipedia.org/wiki/Linear_programming)) is Tier 2.  
**Scalar field:** R; flows on one-way streets are further restricted to nonnegative values  
**Vectors:** R^m, one coordinate per internal road segment (m = 4 in the worked case), each the net flow along a chosen reference direction. The equations are indexed by intersections, so the [incidence matrix](https://en.wikipedia.org/wiki/Incidence_matrix) maps R^m to R^n with n intersections. On one-way streets the physically possible flows are the nonnegative solutions, which form a [convex set](https://en.wikipedia.org/wiki/Convex_set) (here a ray), not a subspace  
**Underlying equations:** A conservation law at each intersection: cars per hour in equals cars per hour out

### The problem

Given the traffic entering and leaving a road network at each intersection, find all flows on the
internal road segments that are consistent with conservation, identify which flows are determined and
which are free, and find the range each flow can take when the streets are one-way, so that no flow
can be negative.

### Variables

| Symbol | Name | What it holds | Shape | Units |
|---|---|---|---|---|
| n | number of intersections | nodes of the network | integer | — |
| m | number of segments | internal roads joining two intersections, each with a chosen reference direction | integer | — |
| x | segment flows | x_j is the net flow on segment j along its reference direction | m × 1 | vehicles per hour |
| A | incidence matrix | A_ij = +1 if segment j's arrow leaves intersection i, −1 if it points to i, 0 otherwise | n × m | dimensionless |
| u_i | boundary inflow | counted traffic entering the district at intersection i | scalar per intersection | vehicles per hour |
| w_i | boundary outflow | counted traffic leaving the district at intersection i | scalar per intersection | vehicles per hour |
| b | net boundary traffic | b_i = u_i − w_i | n × 1 | vehicles per hour |
| x_p | particular solution | any one solution of A x = b | m × 1 | vehicles per hour |
| t | free variable | the amount of circulation | scalar | vehicles per hour |

### Formulation

**Where the equations come from.** The model is conservation of vehicles at each intersection over a
period of steady traffic, such as an hour of the morning peak.

**Two kinds of road.** Boundary roads cross the edge of the district: traffic on them enters or leaves
the network, and those flows are counted, so they are known numbers. Internal segments join two
intersections inside the district, and their flows x_j are the unknowns.

**Directions are bookkeeping.** Each internal segment is given an arrow, a reference direction chosen
once and for all, just as each resistor in the resistor-network entry is given a direction for its
current. The arrow does not mean the street is one-way. The unknown x_j is the net flow along the arrow:
traffic going the arrow's way minus traffic going the other way. So x_j can be negative, meaning more
traffic travels against the arrow than with it. Only for a one-way street with its arrow pointing the
legal way (or when each direction of a two-way street is modelled as its own segment) does x_j ≥ 0
become a physical constraint.

**One intersection.** At intersection i, everything arriving equals everything leaving:

```
(internal flows arriving at i) + (boundary traffic entering at i)
    = (internal flows leaving i) + (boundary traffic leaving at i)
```

Collecting the unknown internal flows on the left and the known boundary counts on the right,

```
(internal flows leaving i) − (internal flows arriving at i) = u_i − w_i = b_i
```

So each segment's flow appears with +1 in the equation of the intersection its arrow leaves, with −1 in
the equation of the intersection its arrow points to, and not at all elsewhere. Everything known about
intersection i, its boundary traffic, is summarized in the single number b_i.

**Worked case, one intersection at a time.** Four intersections P, Q, R and S are joined in a loop by
four internal segments, with arrows x_1: P → Q, x_2: Q → R, x_3: R → S and x_4: S → P. The boundary
counts, in vehicles per hour, are

```
intersection     entering u_i    leaving w_i    b_i = u_i − w_i
P                     500            200             300
Q                     100            200            −100
R                       0            400            −400
S                     300            100             200
```

Altogether 900 vehicles per hour enter and 900 leave. Segment x_1 leaves P and arrives at Q, x_4
leaves S and arrives at P, and so on, so the four equations are

```
P:   x_1             − x_4 =  300
Q:  −x_1 + x_2             = −100
R:        −x_2 + x_3       = −400
S:              −x_3 + x_4 =  200
```

**All intersections at once.** The coefficients of the four equations form the incidence matrix, with
one row per intersection and one column per segment:

```
             x_1  x_2  x_3  x_4
A  =   P  [   1    0    0   −1 ]
       Q  [  −1    1    0    0 ]
       R  [   0   −1    1    0 ]
       S  [   0    0   −1    1 ]

x  =  (x_1, x_2, x_3, x_4)          b  =  (300, −100, −400, 200)
```

and the system is A x = b. In general A_ij is +1 if segment j's arrow leaves intersection i, −1 if it
points to intersection i, and 0 otherwise. A describes how the district's streets are connected, x holds
the unknown internal flows, and b holds what the boundary counts say about each intersection.

**Consistency.** Every column of A has exactly one +1 and one −1, so the n rows add up to the zero row,
and adding all n equations gives 0 = Σ b_i. The system has a solution only if the traffic entering the
district equals the traffic leaving it. One equation is therefore redundant, and for a connected network
the [rank](https://en.wikipedia.org/wiki/Rank_%28linear_algebra%29) of A is n − 1. In the worked case the S equation is minus the sum of the other three.

**The solution set.** With m unknowns and rank n − 1, elimination leaves m − n + 1 free variables, and
every solution is one particular solution plus a combination of null-space vectors. A null-space vector
is a circulation: traffic going round a loop, which adds as much to each intersection's leaving flows as
to its arriving flows. The number of free variables is the number of independent loops. In the worked
case the rank is 3, x_4 = t is free, and

```
x = (300 + t,  200 + t,  −200 + t,  t) = (300, 200, −200, 0) + t (1, 1, 1, 1)
```

where (1, 1, 1, 1) is t vehicles per hour circling the loop. If all four streets are two-way, every
value of t is possible, and the counts leave the flows undetermined. If they are one-way in the
direction of the arrows, every flow must be nonnegative, which requires t ≥ 200: S → P must carry at
least 200 vehicles per hour, R → S at least 0, P → Q at least 500 and Q → R at least 400. Either way, one
count on any segment of the loop fixes t and so every flow.

### Matrix structure

`A` is the node-by-segment incidence matrix of a directed graph: [sparse](https://en.wikipedia.org/wiki/Sparse_matrix), with exactly one +1 and one −1
in every column. Its rank is n minus the number of connected pieces of the network, and its null space
is spanned by the loops. These are the same objects, transposed, as the incidence matrix of the
resistor-network entry, where the null space of Aᵀ was the space of loop currents.

### What is computed

For a small district: [Gaussian elimination](https://en.wikipedia.org/wiki/Gaussian_elimination) to reduced [echelon form](https://en.wikipedia.org/wiki/Row_echelon_form), which separates pivot variables
from free ones and writes the solution as a particular solution plus null-space vectors. Traffic
agencies then add constraints and data: detector counts on some segments, capacity limits, and
nonnegativity. Estimating flows that fit the counts best is a [least-squares](https://en.wikipedia.org/wiki/Least_squares) or linear programming
problem, and predicting how drivers will divide among routes is [traffic assignment](https://en.wikipedia.org/wiki/Route_assignment).

### Why linear algebra is the right tool

The questions an engineer asks are rank questions. Are the edge counts enough? Only if the network
has no loops, since each loop adds a dimension to the null space. How many segments must be counted
inside? As many as the null space has dimensions, chosen so that the counted coordinates pin every
null-space vector down. Which segments are determined by the edge counts alone? Exactly those on which
every null-space vector is zero, such as a bridge that is the only route between two parts of the
network. The structure of the answer, a particular solution plus a subspace, is the general theorem
about solutions of linear systems, with the subspace given a physical meaning.

### Pitfall worth teaching

On one-way streets, the solution set of the equations is a subspace shifted by a particular solution,
but the set of physically possible flows is not. Flows against a one-way arrow are impossible, so the
possible flows are the part of that shifted subspace where every coordinate is at least zero, a convex
set (in the worked case, the ray t ≥ 200). Software that returns one solution chooses for you. Asked for
a least-squares or minimum-norm solution of the worked case, a numerical library returns
x = (225, 125, −275, −75), the solution closest to the origin. On two-way streets that is one
legitimate pattern among infinitely many, with net traffic flowing S → R and P → S, and nothing in the
counts singles it out. On one-way streets it is impossible. The same distinction explains closures:
closing segment S → P forces t = 0 and x_3 = −200. If R–S is a two-way street, that just means 200
vehicles per hour now drive from S to R. If it is one-way from R to S, no traffic pattern is consistent
with the counts, and either the counts must change (drivers reroute) or another road must open. A free
variable means "not determined by these equations", not "anything goes".

### Extensions

Choosing the cheapest admissible flows is a network flow problem, a linear program whose constraint
matrix is this incidence matrix. Such matrices are [totally unimodular](https://en.wikipedia.org/wiki/Unimodular_matrix), so whole-number data give
whole-number optimal flows automatically (see the linear programming entry). Estimating the
origin-destination table from a few detector counts is an underdetermined least-squares problem with
nonnegativity (compare the regression entry). The same conservation-at-nodes structure describes
current in the resistor-network entry, material in the process mass-balance entry, and money between
sectors in the [Leontief](https://en.wikipedia.org/wiki/Input%E2%80%93output_model) entry.

### Terminology

How this field's vocabulary reads as linear algebra.

| Domain term | In linear algebra |
|---|---|
| link (road segment) | one coordinate of the flow vector |
| reference direction | the arrow chosen for a segment; a negative flow means net traffic against it |
| boundary (cordon) counts | known traffic entering and leaving at the district's edge, summarized in b |
| node (intersection) | one row of the conservation system |
| flow (volume) | cars per hour on a segment, an entry of x |
| conservation of flow (continuity) | A x = b, one equation per intersection |
| origin and destination volumes | the entries of b, net traffic entering the network at each node |
| circulation | traffic going round a closed loop, a vector in the null space of A |
| traffic counts (detector or loop counts) | measured coordinates of x, used to pin down the free variables |
| link closure | forcing a coordinate of x to zero, which may leave no admissible solution |
| network flow problem | choosing among the admissible x by minimizing a cost, a linear program |

---

[Back to the index](/r/LinearAlgebra/wiki/applications)
