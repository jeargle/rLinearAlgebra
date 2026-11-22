# Flux balance analysis: a linear program over the null space of the stoichiometric matrix

### Start here

A bacterium growing on sugar runs a few thousand chemical reactions at once. How fast does each one
run: how much sugar is burned for energy, how much built into new cells? Measuring every rate directly
is impractical, and so is measuring every enzyme's speed.

[Flux balance analysis](https://en.wikipedia.org/wiki/Flux_balance_analysis) predicts the rates from bookkeeping plus one assumption. The bookkeeping says
that every chemical inside the cell is made exactly as fast as it is used. That leaves many possible
patterns of rates, so add limits, such as how fast sugar can enter and which reactions run only
forward. Then assume the cell grows as fast as those limits allow, and pick that pattern. The pick is a
[linear programming](https://en.wikipedia.org/wiki/Linear_programming) problem: maximize a linear quantity subject to linear equations and inequalities.

Two pieces of outside mathematics are needed: the bookkeeping is the resting state of a differential
equation for how amounts change over time, and the prices the method puts on each chemical come from
the duality theory of linear programming. A gentler way in is the chemical process entry, where the
same bookkeeping is plain arithmetic, and the [stoichiometric](https://en.wikipedia.org/wiki/Stoichiometry) matrix entry, which studies the table
itself.

**Field:** Systems biology, metabolic engineering, microbiology, biotechnology  
**Tier:** 3 — S v = 0 is the quasi-steady state of the mass-balance [ordinary differential equation](https://en.wikipedia.org/wiki/Ordinary_differential_equation) dc/dt = S v − μ c, justified by a separation of timescales; picking one flux vector is a linear program, and its [shadow prices](https://en.wikipedia.org/wiki/Shadow_price) come from linear programming duality. On-ramps: the null-space view of the stoichiometric matrices entry, and the process [flowsheet](https://en.wikipedia.org/wiki/Process_flow_diagram) entry, where the same balance is an accounting identity with no time derivative.  
**Scalar field:** R  
**Vectors:** R^r flux space, one coordinate per reaction (r = 5 in the worked case). The steady-state fluxes form the [null space](https://en.wikipedia.org/wiki/Kernel_%28linear_algebra%29) of S, a subspace; adding the bounds lb ≤ v ≤ ub cuts it down to a convex [polytope](https://en.wikipedia.org/wiki/Convex_polytope), which is not a subspace. Concentrations live in a different space, R^m, one coordinate per metabolite, and shadow prices live in that same metabolite space  
**Underlying equations:** Mass-balance ordinary differential equation dc/dt = S v(c) − μ c, first order, nonlinear through the enzyme kinetics in v(c); at quasi-steady state it reduces to the linear equations S v = 0, and flux balance analysis then solves the linear program max wᵀ v subject to S v = 0 and lb ≤ v ≤ ub

### The problem

A **metabolite** is a small molecule that the cell makes, consumes or exchanges with its surroundings,
for example glucose, pyruvate, or [adenosine triphosphate](https://en.wikipedia.org/wiki/Adenosine_triphosphate) (ATP), the cell's main carrier of chemical
energy. A **reaction** converts metabolites into others in fixed integer proportions, for example
glucose + 6 O2 → 6 CO2 + 6 H2O for the complete oxidation of glucose. A **flux** is the rate of one
reaction, per gram of cell dry weight per hour; gDW abbreviates gram dry weight, so fluxes are in
mmol gDW⁻¹ h⁻¹. For example, [Escherichia coli](https://en.wikipedia.org/wiki/Escherichia_coli) (E. coli) growing aerobically on glucose takes up roughly
10 mmol gDW⁻¹ h⁻¹ of it. An **exchange reaction** moves one metabolite across the system boundary, as
uptake from the medium or secretion into it. The **biomass reaction** is a modeling device: a drain
that consumes amino acids, nucleotides, lipids and ATP in the proportions measured in one gram of dry
cells, so that its flux equals the growth rate μ, in h⁻¹. A **genome-scale reconstruction** lists every
reaction the organism's genome encodes an enzyme for, with rules linking genes to reactions.

The motivating contrast is between kinetic modeling and constraint-based modeling. A kinetic model
needs rate laws and rate constants for every enzyme, known for few, and predicts concentrations over
time. A constraint-based model needs only stoichiometry, flux bounds and an objective, so it scales to
the genome, but it predicts fluxes only.

Given a reconstruction's stoichiometric matrix, flux bounds and an objective, find a steady-state
flux vector maximizing the objective, and how far each flux can vary among the optima.

### Variables

| Symbol | Name | What it holds | Shape | Units |
|---|---|---|---|---|
| m | number of metabolites | rows of S | integer | — |
| r | number of reactions | columns of S, exchange and biomass reactions included | integer | — |
| c(t) | concentration vector | amount of each intracellular metabolite per gram of dry weight at time t | m × 1 | mmol gDW⁻¹ |
| v | flux vector | rate of each reaction | r × 1 | mmol gDW⁻¹ h⁻¹ |
| S | stoichiometric matrix | s_ij = molecules of metabolite i produced (+) or consumed (−) each time reaction j runs | m × r | dimensionless |
| μ | growth rate | flux of the biomass reaction; also the rate at which growth dilutes c | scalar | h⁻¹ |
| lb, ub | flux bounds | lower and upper limit on each flux | r × 1 each | mmol gDW⁻¹ h⁻¹ |
| w | objective vector | weight of each flux in the objective; usually 1 at the biomass reaction, 0 elsewhere | r × 1 | dimensionless |
| z | objective value | z = wᵀ v | scalar | h⁻¹ when w picks the biomass flux |
| n_1, n_2 | null-space basis | two flux vectors spanning the worked case's steady states | 5 × 1 each | mmol gDW⁻¹ h⁻¹ |
| v∗ | optimal flux distribution | a maximizer of z | r × 1 | mmol gDW⁻¹ h⁻¹ |
| π | shadow prices | dual variable for each row of S v = 0 | m × 1 | objective units per mmol gDW⁻¹ h⁻¹ |

Fluxes live in ℝʳ, one coordinate per reaction; concentrations and shadow prices live in ℝᵐ. S maps
flux space into metabolite space.

### Formulation

**The familiar formula.** For one pool: rate of change = rate in − rate out. If pyruvate is made at 20
and consumed at 19 mmol gDW⁻¹ h⁻¹, its amount rises at 1 mmol gDW⁻¹ h⁻¹.

**One metabolite.** Reaction j makes s_ij molecules of metabolite i each time it runs, and it runs at
rate v_j, so metabolite i changes at Σ_j s_ij v_j, which is row i of S times v. Growth dilutes the pool
into new cell volume, subtracting μ c_i. Stacking all m rows gives an ordinary differential equation,
an equation whose unknown is the function c(t):

```
dc/dt = S v(c) − μ c
```

Here dc/dt is the vector of time derivatives, one per metabolite; for example dc/dt = (0.5, −0.2) would
mean the first pool is rising by 0.5 and the second falling by 0.2 mmol gDW⁻¹ per hour. The system is
first order and nonlinear, because each flux depends on concentrations through enzyme kinetics. Its
solutions are trajectories c(t) fixed by the initial concentrations, and computing them needs the
missing rate laws.

**Quasi-steady state.** The step that removes the kinetics is a timescale separation. Intracellular
metabolite pools are small and turn over in seconds to minutes, while the cell doubles in about an hour
and changes its enzyme levels over minutes to hours. On the slow timescale the fast pools relax almost
at once to a quasi-steady state, where dc/dt ≈ 0, and the dilution term μ c is negligible next to the
fluxes passing through each pool. What remains is the [mass balance](https://en.wikipedia.org/wiki/Mass_balance)

```
S v = 0
```

so every quasi-steady flux vector lies in the null space of S. The concentrations drop out.

**Bounds.** Fluxes are limited entrywise, lb ≤ v ≤ ub, meaning lb_j ≤ v_j ≤ ub_j for every j. For
example (0, −2) ≤ (1, 3) holds because 0 ≤ 1 and −2 ≤ 3, while neither of (0, 5) and (1, 3) is ≤ the
other. A reaction with a large negative [Gibbs free energy](https://en.wikipedia.org/wiki/Gibbs_free_energy) change is irreversible, so lb_j = 0; an
uptake is capped by transport, for example glucose uptake ≤ 10 mmol gDW⁻¹ h⁻¹.

**The linear program.** Flux balance analysis (FBA) chooses one point by maximizing z = wᵀ v:

```
maximize    wᵀ v
subject to  S v = 0,   lb ≤ v ≤ ub
```

Known: S, lb, ub and w. Unknown: v. Many FBA papers write the objective vector as c, which here is the
concentration vector. The feasible set, the null space cut by a box, is a convex polytope, and the
maximum lies at a vertex, where the [simplex method](https://en.wikipedia.org/wiki/Simplex_algorithm) of the linear programming entry searches.

**Worked case: two pathways of different yield.** Three metabolites (glucose, oxygen, ATP) and five
reactions:

```
v_1  glucose uptake:   → glucose                    0 ≤ v_1 ≤ 10
v_2  oxygen uptake:    → oxygen                     0 ≤ v_2 ≤ 12
v_3  fermentation:     glucose → 2 ATP              v_3 ≥ 0
v_4  respiration:      glucose + 6 oxygen → 18 ATP  v_4 ≥ 0
v_5  biomass:          glucose + 2 ATP →            v_5 ≥ 0
```

The yields are stylized (real values are about 2 and 26 to 30 ATP per glucose), and
adenosine diphosphate (ADP), lactate and CO2 are left outside the system. The balances, one per
metabolite, are

```
glucose:  v_1 − v_3 − v_4 − v_5 = 0
oxygen:   v_2 − 6 v_4 = 0
ATP:      2 v_3 + 18 v_4 − 2 v_5 = 0
```

and row by row,

```
      v_1  v_2  v_3  v_4  v_5
S = [ 1    0    −1   −1   −1  ]   glucose
    [ 0    1    0    −6   0   ]   oxygen
    [ 0    0    2    18   −2  ]   ATP
```

S has [rank](https://en.wikipedia.org/wiki/Rank_%28linear_algebra%29) 3, so the null space has dimension 5 − 3 = 2. Taking v_3 and v_4 as free, the ATP row gives
v_5 = v_3 + 9 v_4, the oxygen row v_2 = 6 v_4, and the glucose row v_1 = 2 v_3 + 10 v_4. Setting
(v_3, v_4) = (1, 0) and (0, 1) gives the basis n_1 = (2, 0, 1, 0, 1), pure fermentation, and
n_2 = (10, 6, 0, 1, 9), pure respiration. Every steady state is v = v_3 n_1 + v_4 n_2. Checking n_2:

```
[ 1  0  −1  −1  −1 ]   [ 10 ]   [ 10 − 0 − 1 − 9 ]   [ 0 ]
[ 0  1  0   −6  0  ]   [ 6  ]   [ 6 − 6          ]   [ 0 ]
[ 0  0  2   18  −2 ] × [ 0  ] = [ 0 + 18 − 18    ] = [ 0 ]
                       [ 1  ]
                       [ 9  ]
```

In the coordinates (v_3, v_4) the bounds become v_3 ≥ 0, v_4 ≥ 0, 2 v_3 + 10 v_4 ≤ 10 and 6 v_4 ≤ 12.
The last is implied by the others, so the feasible set is the triangle with vertices (0, 0), (5, 0) and
(0, 1), where v_5 = v_3 + 9 v_4 equals 0, 5 and 9. The optimum is the third vertex,

```
v∗ = (10, 6, 0, 1, 9),   z = 9
```

All glucose is respired: the higher-yield pathway turns 10 glucose into 9 units of biomass, against 5
for fermentation.

The shadow prices are the dual variables on the rows of S v = 0. Each is the gain in z per unit of that
metabolite supplied free: π = (0.9, 0, 0.05) for glucose, oxygen and ATP. Oxygen is worth nothing: its
bound is slack. Lowering the oxygen limit to 3 moves the optimum to the vertex where both uptake limits
bind, v∗ = (10, 3, 2.5, 0.5, 7), with z = 7 and π = (0.5, 0.67, 0.25): the cell respires what oxygen
allows and ferments the rest, the FBA picture of [overflow metabolism](https://en.wikipedia.org/wiki/Overflow_metabolism).

Here the optimum is a single vertex. When the objective vector is perpendicular to a whole edge or
face, the whole face is optimal; these alternative optima are typical at genome scale, for example from
[isoenzymes](https://en.wikipedia.org/wiki/Isozyme) (distinct enzymes that catalyze the same reaction, giving identical columns of S) or
parallel routes of equal yield. Flux variability analysis (FVA) maps them by holding z at its optimum,
or a fraction of it, and minimizing and maximizing each v_j in turn. In the worked case every range at
the optimum is a single point; requiring only 90% of the optimum (v_5 ≥ 8.1) lets fermentation range
from 0 to 1.125 and respiration from 0.775 to 1.

### Matrix structure

S is [sparse](https://en.wikipedia.org/wiki/Sparse_matrix) with small integer entries: a typical column has 2 to 6 nonzeros, an exchange column
exactly one, and the biomass column dozens of non-integer ones. The BiGG (Biochemical, Genetic and
Genomic) E. coli core model, e_coli_core, has 72 metabolites and 95 reactions, rank 67 and nullity 28.
Genome-scale reconstructions reach about 2,000 metabolites by 3,000 reactions for E. coli (iML1515),
and human Recon3D is several times larger.

### What is computed

One linear program per scenario, solved by dual simplex or [interior-point methods](https://en.wikipedia.org/wiki/Interior-point_method) (GLPK, HiGHS, CPLEX
or Gurobi) in under a second at genome scale; FVA takes 2r more. Each solve also returns shadow prices
π and [reduced costs](https://en.wikipedia.org/wiki/Reduced_cost), which say which metabolites and bounds limit growth. A gene knockout sets lb_j =
ub_j = 0 for every reaction needing the deleted gene.

### Why linear algebra is the right tool

Steady state is a null space, which the stoichiometry alone determines. Bounds make it a polytope, a
linear objective selects a vertex, and a vertex solves one square system in a basis of columns (the
basis exchange of the linear programming entry). Duality prices each row of S: a vector in metabolite
space beside the flux vector in reaction space.

### Pitfall worth teaching

The objective is a hypothesis about evolution, not a law. Maximal growth matches E. coli well after
laboratory [adaptive evolution](https://en.wikipedia.org/wiki/Experimental_evolution), for example on glycerol, but poorly for freshly engineered strains or
most mammalian cells. A second trap is thermodynamically infeasible cycles: a closed loop of internal
reactions, for example P → Q → R → P, is a null vector with no net conversion, so any amount of flux
can circulate without changing z, inflating FVA ranges. Finally, FBA predicts fluxes, not
concentrations: S v = 0 holds for any constant c, so metabolite levels need kinetics or extra data.

### Extensions

Complementary slackness, from the full duality theory, says that a reaction carrying flux strictly
between its bounds has zero reduced cost. Parsimonious FBA minimizes total flux Σ |v_j| among the
optima, a second linear program. Minimization of metabolic adjustment (MOMA) predicts a knockout's
fluxes as the feasible point closest in Euclidean norm to the wild type, a [quadratic program](https://en.wikipedia.org/wiki/Quadratic_programming) and a
[least-squares](https://en.wikipedia.org/wiki/Least_squares) projection onto a polytope (see the least squares entries). Loopless FBA removes
thermodynamically infeasible cycles with integer variables. Dynamic FBA keeps a differential equation
on the slow scale, for biomass and medium concentrations, with an FBA solve at each time step setting μ
and the uptakes. Overflow metabolism with oxygen to spare (acetate in E. coli, the [Crabtree effect](https://en.wikipedia.org/wiki/Crabtree_effect) in
yeast, the [Warburg effect](https://en.wikipedia.org/wiki/Warburg_effect_%28oncology%29) in tumors) needs an extra capacity constraint, such as a proteome budget. The
worked case's n_1 and n_2 are its two [elementary flux modes](https://en.wikipedia.org/wiki/Elementary_modes), extreme rays of the cone treated in the
stoichiometric matrices entry. COBRA (constraint-based reconstruction and analysis) software: COBRApy
(Python), the COBRA Toolbox (MATLAB) and COBREXA.jl (Julia).

### Terminology

How this field's vocabulary reads as linear algebra.

| Domain term | In linear algebra |
|---|---|
| metabolite | a row of S; one coordinate of the concentration vector c |
| reaction | a column of S; one coordinate of the flux vector v |
| flux | v_j, the rate of reaction j in mmol gDW⁻¹ h⁻¹ |
| stoichiometric matrix S | metabolites by reactions, s_ij molecules of metabolite i made (+) or used (−) per reaction event |
| steady state (mass balance) | S v = 0, v in the null space of S |
| flux bounds | lb ≤ v ≤ ub entrywise; lb_j = 0 for an irreversible reaction |
| exchange reaction | a column with a single nonzero entry, moving one metabolite across the boundary |
| biomass reaction | the column that drains precursors and ATP in cell proportions; its flux is μ |
| objective function | z = wᵀ v, usually w picks out the biomass flux |
| flux distribution / flux map | one feasible or optimal vector v |
| shadow price | π_i, the dual variable on row i of S v = 0 |
| alternative optima | an optimal face of the polytope rather than a single vertex |
| flux variability analysis (FVA) | min and max of each v_j over the optimal (or near-optimal) set |
| elementary flux mode | an extreme ray of the cone {v : S v = 0, v_j ≥ 0 for irreversible j} |
| thermodynamically infeasible loop | a nonzero null vector using only internal reactions |

---

[Back to the index](/r/LinearAlgebra/wiki/applications)
