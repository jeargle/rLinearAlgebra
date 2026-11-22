---
id: 15
slug: linear-programming-and-the-simplex-method
status: written
title: 'Linear programming: the simplex method as a walk between basis matrices'
short_title: Linear programming and the simplex method
field_label: Operations research, production planning, scheduling, logistics, economics
tier_note: 'each corner of the feasible region is the solution of one square system B x_B = b, and
  each simplex step swaps one column of B, a rank-one update. That much is first-course linear algebra;
  the entry is Tier 2 because whether those solves can be trusted at scale depends on the condition
  numbers of the basis matrices and on updated factorizations. Duality, complementary slackness,
  convexity proofs and interior-point theory need convex analysis and are Tier 3, named in Extensions.'
nav_field: Economics, Finance & Operations Research
field: Mathematics
subfield: Operations research
tier: 2
tier_ceiling: 3
prereq_beyond_la: convex duality; polyhedral theory
scalar_field: R
vector_space: 'R^n with n = products + resources, one coordinate per decision variable or slack
  variable. The feasible set {x : A x = b, x ≥ 0} is a polyhedron, not a subspace: it is closed under
  neither negation nor scaling by negative numbers. The vectors x_B of basic variables live in R^m, one
  coordinate per constraint'
underlying_equations: 'A linear production model: resource use is an accounting identity, amount per
  item times number of items summed over products, giving inequalities G x ≤ b with x ≥ 0 and a linear
  profit cᵀ x to maximize; slack variables turn them into the equations A x = b with A = [G I]'
core_la_object: Basis matrices and rank-one updates
la_concepts: basis exchange; duality; total unimodularity
primary_method: Revised simplex; interior point
matrix_structure: sparse constraint matrix
typical_size: 1e5-1e7 variables
worked_example_size: 2 products and 3 resources (5 variables with slacks) with all 10 bases listed and a 2-pivot simplex run by hand
terminology:
  linear program (LP): maximize cᵀ x subject to A x = b and x ≥ 0 entrywise
  decision variable: an unknown entry x_j, the level of one activity
  constraint: one row of A x = b, or of G x ≤ b before slacks are added
  slack variable s_i: the unused amount of resource i, an added unknown that turns ≤ into =
  feasible region: 'the polyhedron {x : A x = b, x ≥ 0}'
  vertex (corner): a point of the feasible region that is the solution of B x_B = b for some basis
  basis: a choice of m linearly independent columns of A, forming the m × m matrix B
  basic variables x_B: the m unknowns solved for by B x_B = b
  nonbasic variables x_N: the n − m unknowns held at 0
  basic feasible solution: x_B = B⁻¹ b with x_B ≥ 0 and x_N = 0; the algebraic name for a vertex
  reduced cost d_j: c_j − yᵀ a_j, the change in profit per unit of nonbasic variable x_j
  simplex multipliers y: the solution of Bᵀ y = c_B
  entering variable: the nonbasic variable with d_j > 0 chosen to increase
  ratio test: t = min over u_i > 0 of x_B,i / u_i, the step to the next vertex
  leaving variable: the basic variable that reaches 0 first in the ratio test
  pivot: replacing one column of B, a rank-one update B + (a_j − B e_r) e_rᵀ
  eta matrix E: the identity with one column replaced, so that the new B⁻¹ is E times the old one
  degenerate vertex: a basic feasible solution with some basic variable equal to 0
  totally unimodular matrix: every square submatrix has determinant 0, 1 or −1, so every vertex is integer for integer b
---

## Start here

A furniture workshop makes two products from limited wood, labor and machine time. Each product earns a
known profit and uses known amounts of each resource. How many of each should it make? Problems of this
shape, the best plan within limits when everything scales in proportion, are linear programs. They
schedule airline crews, blend animal feed and route freight.

In school, a two-variable version is solved by graphing each limit as a line, shading the region that
obeys all of them, and checking the profit at each corner, where the best plan always lies. With
thousands of products the corners cannot be drawn or listed, but each is still the solution of a square
linear system. The simplex method walks uphill from corner to neighboring corner, changing one column
of a matrix per step.

## The problem

Linear programming (LP) chooses nonnegative quantities to maximize, or minimize, a linear function of
them under linear limits. The unknowns are decision variables, for example the numbers of tables and
bookcases a workshop makes in a week. Each limit is a constraint: the use of one resource must not
exceed its capacity, for example at most 6 boards of wood a week. The function maximized is the
objective, here profit. A plan obeying every constraint with no negative quantity is feasible, and all
feasible plans form the feasible region, a polygon in two variables. A constraint is tight when it
holds with equality, so the resource is used up. A vertex, or corner, is a feasible plan where enough
constraints are tight to pin it down: in two variables, two of them.

The motivating contrast is between equations and inequalities. A square linear system pins down its
solution, as in the Leontief entry. Constraints with ≤ leave a whole region of plans and ask which is
best. Given: each item's resource use, the capacities and the profits. Solved for: the quantities, and
which constraints end up tight.

## Variables

| Symbol | Name | What it holds | Shape | Units |
|---|---|---|---|---|
| k | number of products | how many decision variables there are | integer | — |
| m | number of resources | how many constraints there are | integer | — |
| n | number of variables | k products plus m slack variables, n = k + m | integer | — |
| x_j | decision variable | quantity of product j | scalar ≥ 0 | items |
| s_i | slack variable | unused amount of resource i | scalar ≥ 0 | units of resource i |
| x | variable vector | (x_1, …, x_k, s_1, …, s_m) | n × 1 | mixed: items and resource units |
| G | resource-use matrix | entry g_ij is the amount of resource i one item of product j uses | m × k | resource units per item |
| b | capacity vector | entry b_i is the available amount of resource i | m × 1 | resource units |
| c | profit vector | profit per item for each product, 0 for each slack | n × 1 | dollars per item |
| z | objective | total profit cᵀ x | scalar | dollars |
| A | constraint matrix | [G I]: the resource-use matrix with an identity block for the slacks | m × n | mixed |
| I | identity matrix |  | m × m | — |
| a_j | column j of A | resource use of variable j | m × 1 | resource units per item |
| B | basis matrix | m chosen linearly independent columns of A; B_P, B_Q at corners P and Q | m × m | mixed |
| N | nonbasic matrix | the other n − m columns of A | m × (n − m) | mixed |
| x_B, x_N | basic, nonbasic variables | the entries of x for the columns in B, in N | m × 1, (n − m) × 1 | mixed |
| c_B, c_N | basic, nonbasic profits | the entries of c for the columns in B, in N | m × 1, (n − m) × 1 | dollars per item |
| y | simplex multipliers | solution of Bᵀ y = c_B | m × 1 | dollars per resource unit |
| d_j, d_N | reduced cost | profit change per unit increase of nonbasic variable x_j; d_N collects them | scalar, (n − m) × 1 | dollars per item |
| u | edge direction | u = B⁻¹ a_j: how fast each basic variable falls as x_j rises | m × 1 | mixed |
| t | step length | how far x_j rises before a basic variable reaches 0 | scalar ≥ 0 | items |
| e_r | unit vector | 1 in position r, 0 elsewhere | m × 1 | — |
| E | eta matrix | identity with column r replaced; the new B⁻¹ is E times the old | m × m | mixed |
| w, v | update vectors | a rank-one change B + w vᵀ; for a pivot, w = a_j − B e_r and v = e_r | m × 1 each | mixed |
| D | diagonal scaling | weights used by interior-point methods (Extensions) | n × n | mixed |

## Formulation

**Where the equations come from.** One item of product j uses g_ij units of resource i and earns c_j,
so total use and total profit are sums over products: accounting identities, which must stay within
capacity.

**The familiar method.** A table takes 1 board, 1 labor hour and 2 machine hours; a bookcase takes 1
board, 3 labor hours and 1 machine hour. The week has 6 boards, 12 labor hours and 10 machine hours,
and profits are 3 and 2 (hundreds of dollars). The scalar problem is

```
maximize    z = 3 x_1 + 2 x_2
subject to      x_1 +   x_2 ≤ 6     (wood)
                x_1 + 3 x_2 ≤ 12    (labor)
              2 x_1 +   x_2 ≤ 10    (machine)
                x_1 ≥ 0,  x_2 ≥ 0
```

The three lines and two axes bound a five-sided region with corners O, P, Q, R and S. Checking the
profit at each corner is the school method:

```
corner   tight constraints   (x_1, x_2)   z
O        x_1 ≥ 0, x_2 ≥ 0    (0, 0)       0
P        machine, x_2 ≥ 0    (5, 0)       15
Q        wood, machine       (4, 2)       16
R        wood, labor         (3, 3)       15
S        labor, x_1 ≥ 0      (0, 4)       8
```

The best plan is Q: four tables and two bookcases, profit 16, with 2 labor hours idle.

**One constraint as an equation.** The wood constraint x_1 + x_2 ≤ 6 becomes x_1 + x_2 + s_1 = 6 with
s_1 ≥ 0, the wood left over. It is called a slack variable because it measures the slack in the
constraint: s_1 = 0 exactly when the constraint is tight.

**All constraints: standard form.** Adding a slack to each constraint gives three equations in five
unknowns, all nonnegative:

```
  x_1 +   x_2 + s_1             = 6
  x_1 + 3 x_2       + s_2       = 12
2 x_1 +   x_2             + s_3 = 10
```

With x = (x_1, x_2, s_1, s_2, s_3) these are A x = b, with known A, b and c:

```
      x_1  x_2  s_1  s_2  s_3
A = [ 1    1    1    0    0 ]    wood
    [ 1    3    0    1    0 ]    labor
    [ 2    1    0    0    1 ]    machine

b = [ 6  ]
    [ 12 ]
    [ 10 ]

c = [ 3  2  0  0  0 ]
```

In general A = [G I] is m × n, with G the resource-use columns (here the first two columns of A), and
the standard form is: maximize z = cᵀ x subject to A x = b and x ≥ 0, where cᵀ x is the dot product c_1
x_1 + … + c_n x_n.

Inequalities between vectors are read entrywise: x ≥ 0 means every entry of x is at least 0, so (3,
0) ≥ 0 holds but (3, −1) ≥ 0 does not, and one vector is ≤ another when each entry is ≤ the matching
entry, as in (1, 2) ≤ (2, 2).

**Corners are bases.** Choose m = 3 linearly independent columns of A as a basis, collected into the
basis matrix B, and set the other two variables to 0. One square system B x_B = b remains. If x_B ≥ 0,
the point is a basic feasible solution, the algebraic name for a vertex. For example, Q has
s_1 = s_3 = 0, so its basis is the columns of x_1, x_2 and s_2:

```
[ 1  1  0 ]   [ x_1 ]   [ 6  ]
[ 1  3  1 ] × [ x_2 ] = [ 12 ]
[ 2  1  0 ]   [ s_2 ]   [ 10 ]
```

with solution (x_1, x_2, s_2) = (4, 2, 2). Of the 10 ways to choose 3 of the 5 columns, all give
nonsingular B; 5 give x_B ≥ 0 and are exactly O, P, Q, R and S, and 5 have a negative entry. For
example, the basis x_1, x_2, s_1 gives the meeting point of the labor and machine lines, (18/5, 14/5),
with s_1 = −2/5: more wood than exists. In general there can be n choose m bases, so listing corners
fails beyond toy size.

**One edge: the reduced cost.** At P = (5, 0) the basic variables, in the order (s_1, s_2, x_1), solve

```
[ 1  0  1 ]   [ s_1 ]   [ 6  ]
[ 0  1  1 ] × [ s_2 ] = [ 12 ]
[ 0  0  2 ]   [ x_1 ]   [ 10 ]
```

giving (s_1, s_2, x_1) = (1, 7, 5) and z = 15. Raise the nonbasic x_2 from 0 to t while s_3 stays 0,
moving along the machine line, an edge of the region. The basic variables must solve B x_B = b − t a_2,
so they change by −t u with u = B⁻¹ a_2 = (1/2, 5/2, 1/2): each bookcase takes half a table's machine
time. Profit changes by 2t − 3 × (t/2) = t/2. That rate, 1/2 per bookcase, is the reduced cost of x_2:
its profit c_2 reduced by the value of what the basic variables give up.

For any nonbasic column a_j, d_j = c_j − c_Bᵀ B⁻¹ a_j. One solve serves every column: let y solve Bᵀ
y = c_B, where Bᵀ is the transpose (so y = B⁻ᵀ c_B), and then d_j = c_j − yᵀ a_j, or d_N = c_N − Nᵀ y.
At P, y = (0, 0, 3/2), so x_2 has d = 2 − (1, 3, 1) · y = 1/2 and s_3 has d = −3/2. A positive
reduced cost means the edge goes uphill; if every d_j ≤ 0, the vertex is optimal.

**How far: the ratio test.** Basic variable i hits 0 at t = x_B,i / u_i, so the step is t = min over
u_i > 0 of x_B,i / u_i, the smallest of those ratios. At P they are 1/(1/2) = 2 for s_1, 7/(5/2) = 2.8
for s_2 and 5/(1/2) = 10 for x_1, so t = 2 and s_1 leaves the basis: the wood runs out first.

**The whole run.** At O the slacks form the basis: B = I, x_B = (6, 12, 10), y = 0, and the
reduced costs are the profits 3 and 2. x_1 enters, u = (1, 1, 2), the ratios are 6, 12 and 5, and s_3
leaves at t = 5, reaching P with z = 15. From P, x_2 enters and s_1 leaves at t = 2, reaching Q = (4,
2) with z = 15 + 2 × (1/2) = 16. At Q, with basis order (x_2, s_2, x_1), y = (1, 0, 1), and s_1 and s_3
both have reduced cost −1, so Q is optimal, matching the corner list.

**A pivot is a rank-one update.** The basis matrices at P and Q differ only in position 1, where the
column of s_1, which is e_1, is replaced by a_2 = (1, 3, 1):

```
        s_1  s_2  x_1              x_2  s_2  x_1
B_P = [ 1    0    1 ]      B_Q = [ 1    0    1 ]
      [ 0    1    1 ]            [ 3    1    1 ]
      [ 0    0    2 ]            [ 1    0    2 ]
```

so B_Q = B_P + (a_2 − e_1) e_1ᵀ. A column times the row e_1ᵀ is a matrix whose only nonzero column is
the first, here (0, 3, 1), so the change has rank one. The Sherman–Morrison formula, (B + w
vᵀ)⁻¹ = B⁻¹ − B⁻¹ w vᵀ B⁻¹ / (1 + vᵀ B⁻¹ w), updates the inverse; here 1 + vᵀ B⁻¹ w = 1/2, the pivot
entry u_1. Equivalently B_Q⁻¹ = E B_P⁻¹, with an eta matrix E, the identity with column 1 replaced by
(1/u_1, −u_2/u_1, −u_3/u_1):

```
[ 2   0  0 ]   [ 1  0  −1/2 ]   [ 2   0  −1 ]
[ −5  1  0 ] × [ 0  1  −1/2 ] = [ −5  1  2  ]
[ −1  0  1 ]   [ 0  0  1/2  ]   [ −1  0  1  ]
   E              B_P⁻¹            B_Q⁻¹
```

This is the product form of the inverse: after several pivots, B⁻¹ is a product of eta matrices times
the starting inverse. The simplex tableau of textbooks performs the same step as Gaussian elimination
on the entering column.

## Matrix structure

A = [G I] is wide (m < n), has full row rank because of its identity block, and is very sparse: for
example, a crew pairing, a sequence of flights one crew can work, covers only a few of an airline's
flights. Each basis matrix changes by one column per pivot and can be far worse conditioned than A: in
the toy, the 2-norm condition number of B is 1 at O, about 3.2 at P and about 24 at Q. In network
problems G is the incidence matrix of a directed graph, which is totally unimodular: every square
submatrix has determinant 0, 1 or −1. By Cramer's rule every vertex is then an integer vector when b
is, so integer flows come free.

## What is computed

The revised simplex method never forms B⁻¹. It keeps an LU factorization (lower and upper triangular
factors) of B, solves B u = a_j and Bᵀ y = c_B per pivot, updates the factors for each rank-one change,
and refactorizes every hundred or so pivots to limit rounding error. At scale, airline crew scheduling
chooses among millions of candidate pairings, each a column of A; the diet problem picks the cheapest
foods meeting nutrient needs; and minimum-cost network flow ships goods along graph edges.

## Why linear algebra is the right tool

A vertex is a nonsingular system B x_B = b, an edge is a one-column exchange, the profit rate along it
is one solve with Bᵀ, and the step length is a ratio of computed vectors. A search over up to
n choose m bases becomes a sequence of rank-one updates.

## Pitfall worth teaching

Degeneracy: when more than m constraints are tight at a vertex, some basic variable is 0, the
ratio test can give t = 0, and a pivot changes the basis without moving. With 9 machine hours instead
of 10, R = (3, 3) lies on all three resource lines, and three bases describe that one corner. A
careless pivoting rule can then cycle among them forever. Bland's rule prevents cycling: among
candidates, always pick the lowest index, to enter and to leave. A second trap is mistaking typical
speed for a guarantee. The Klee–Minty cube, a squashed cube in n dimensions, makes the
largest-reduced-cost rule visit all 2^n vertices, yet on practical problems the simplex method usually
needs a small multiple of m pivots.

## Extensions

At the optimum the multipliers y are shadow prices, the extra profit per unit of each resource. In the
toy, y = (1, 0, 1): an extra board or machine hour is worth 1, idle labor 0, and bᵀ y = 6 + 10 = 16
equals the optimal profit. Making this precise is LP duality, with complementary slackness and
convexity, which are Tier 3. Interior-point methods cross the inside of the region, solving a
positive definite system A D Aᵀ per step with D diagonal. Integer programming is hard in general but
free for totally unimodular matrices such as the incidence matrix of the traffic-flow entry. The
Leontief entry is the equality-only relative, and flux balance analysis applies LP to a
stoichiometric matrix. Up the optimization ladder, the portfolio optimization entry has a quadratic
objective, the entry on distance geometry for nuclear magnetic resonance (NMR) structures optimizes
over positive semidefinite matrices, and the Markov decision processes entry finds its optimal values
with an LP.
