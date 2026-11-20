# Normal modes and elastic network models: the collective motions a protein structure makes easy

### Start here

A protein is not rigid. A published structure is a snapshot of a molecule that is constantly jiggling
at body temperature, and many proteins work by moving: two lobes close around a molecule they bind, or
a lid swings shut over it. Rather than simulate every atom, one can ask which motions the shape itself
makes easy.

Picture the protein as beads, one per building block, with a spring between every pair that sit close
together. Push it and it wobbles. A few special patterns of wobble repeat cleanly, each at its own
rate, and every other wobble mixes them. The slowest patterns are the floppiest directions, and they
often turn out to be the motions the protein uses to do its job.

Finding those patterns is an [eigenvalue](https://en.wikipedia.org/wiki/Eigenvalues_and_eigenvectors) problem. The entry needs two ideas from outside linear algebra,
explained just far enough to set up the matrix: differential equations, which describe motion, and
statistical mechanics, which says how far a molecule strays at a given temperature.

**Field:** Biophysics, structural biology, protein dynamics, computational chemistry, vibrational spectroscopy  
**Tier:** 3 — the modes are the solutions of the [ODE](https://en.wikipedia.org/wiki/Ordinary_differential_equation) M ẍ = −H x for small oscillations about an energy minimum, and reading them as thermal fluctuations needs the [Boltzmann distribution](https://en.wikipedia.org/wiki/Boltzmann_distribution) of statistical mechanics. On-ramps: the static spring-network solve K u = f of the structural analysis entry (Tier 1), and the graph [Laplacian](https://en.wikipedia.org/wiki/Laplacian_matrix) eigenvectors of the [spectral clustering](https://en.wikipedia.org/wiki/Spectral_clustering) entry (Tier 2).  
**Scalar field:** R  
**Vectors:** R^3N: x stacks the x, y and z displacements of N atoms or residues. The [Gaussian network model](https://en.wikipedia.org/wiki/Gaussian_network_model) works in R^N, one coordinate per residue, because it treats x, y and z alike. Rigid-body motions span the [null space](https://en.wikipedia.org/wiki/Kernel_%28linear_algebra%29) of H, of dimension 6 for a connected nonlinear structure in 3D  
**Underlying equations:** Linear second-order ODE system with constant coefficients, M ẍ = −H x (Newton's second law with the potential energy expanded to second order about a minimum); the trial solution x = v cos(ωt) gives the [generalized eigenproblem](https://en.wikipedia.org/wiki/Eigendecomposition_of_a_matrix#Generalized_eigenvalue_problem) H v = ω² M v. Thermal averages come from the Boltzmann distribution, a Gaussian with [covariance](https://en.wikipedia.org/wiki/Covariance_matrix) k_B T H⁺

### The problem

Some vocabulary first. A **residue** is one amino acid in a protein chain. A **structure** is a list of
atomic coordinates, determined for example by X-ray crystallography and deposited in the
[Protein Data Bank](https://en.wikipedia.org/wiki/Protein_Data_Bank). Coordinates are in ångströms (Å, 10⁻¹⁰ m), masses in daltons (Da, grams per mole),
times in picoseconds (ps, 10⁻¹² s) and energies in kilocalories per mole (kcal/mol). Coarse-grained
models keep one point per residue, its **C-alpha atom**, the backbone carbon that carries the side
chain. A **conformational change** is the difference between two structures of one protein, e.g. two
domains (compact, separately folded parts of the chain) closing around a bound ligand. The **B-factor**
(temperature factor) reported for each atom of a crystal structure measures how far it fluctuates. A
**[normal mode](https://en.wikipedia.org/wiki/Normal_mode)** is a motion in which every coordinate oscillates in step at one frequency.

The motivating contrast is simulating motion versus analyzing it. [Molecular dynamics](https://en.wikipedia.org/wiki/Molecular_dynamics) (MD) integrates
Newton's equations for every atom in femtosecond (10⁻¹⁵ s) steps, so a microsecond motion needs about
10⁹ of them. Normal mode analysis (NMA) treats the energy as quadratic near one structure and reads the
motions off one matrix. An elastic network model (ENM) replaces the chemistry by identical springs
between nearby C-alpha atoms; its two standard forms are the Gaussian network model (GNM) and the
[anisotropic network model](https://en.wikipedia.org/wiki/Anisotropic_Network_Model) (ANM).

Given one structure, find its normal modes, predict each residue's thermal fluctuation for comparison
with the B-factors, and identify the slow collective motions, such as hinge bending, that a
conformational change is likely to follow.

**On-ramp.** A spring network held still by a constant force f obeys H x = f, the static stiffness
solve K u = f ([stiffness matrix](https://en.wikipedia.org/wiki/Stiffness_matrix) K, displacements u) of the structural analysis entry (Tier 1). The GNM
computations, eigenvectors and a [pseudoinverse](https://en.wikipedia.org/wiki/Moore%E2%80%93Penrose_inverse) of a graph Laplacian, are those of the
spectral clustering entry (Tier 2). The differential equation is what makes those eigenvectors motions.

### Variables

| Symbol | Name | What it holds | Shape | Units |
|---|---|---|---|---|
| N | number of nodes | atoms in NMA; residues (C-alpha atoms) in an ENM | integer | — |
| R_i | equilibrium position | coordinates of node i in the structure | 3 × 1 | Å |
| x | displacement vector | every coordinate's departure from the minimum, stacked: x_1, …, x_3N | 3N × 1 | Å |
| ΔR_i | displacement of node i | the three entries of x that belong to node i | 3 × 1 | Å |
| t | time | | scalar | ps |
| ẍ | acceleration | d²x/dt², the second time derivative of x | 3N × 1 | Å/ps² |
| V | potential energy | energy as a function of the coordinates, minimal at x = 0 | scalar | kcal/mol |
| H | Hessian | H_ij = ∂²V/∂x_i∂x_j at the minimum: the molecule's stiffness matrix | 3N × 3N | kcal mol⁻¹ Å⁻² |
| M | mass matrix | diagonal; each node's mass m_i repeated for its three coordinates | 3N × 3N | Da |
| q | mass-weighted coordinates | q = M^(1/2) x | 3N × 1 | Å Da^(1/2) |
| ω_k | angular frequency | how fast mode k oscillates | scalar | rad/ps |
| λ_k, v_k | eigenpair | eigenvalue and mode shape of mode k, sorted λ_1 ≤ λ_2 ≤ …; λ_k = ω_k² when masses are included | scalar, 3N × 1 | ps⁻², dimensionless |
| a_k, b_k | mode amplitudes | fixed by the starting positions and velocities | scalars | Å |
| f | applied force | a constant external force on each coordinate | 3N × 1 | kcal mol⁻¹ Å⁻¹ |
| r_c | cutoff distance | nodes closer than r_c are joined by a spring | scalar | Å |
| γ | spring constant | the same for every spring | scalar | kcal mol⁻¹ Å⁻² |
| Γ | Kirchhoff matrix | GNM contact matrix: −1 per contact, contact counts on the diagonal | N × N | dimensionless |
| e_ij | bond direction | unit vector from R_i to R_j | 3 × 1 | dimensionless |
| k_B T | thermal energy | Boltzmann constant times absolute temperature; about 0.59 kcal/mol at 298 K | scalar | kcal/mol |
| ⟨ · ⟩ | thermal average | mean over the molecule's fluctuations at temperature T | — | — |
| H⁺, Γ⁺ | pseudoinverses | the inverse of H or Γ on the nonzero modes | 3N × 3N, N × N | Å² mol/kcal, dimensionless |
| B_i | B-factor | mean squared fluctuation of node i, times 8π²/3 | scalar | Å² |
| d | conformational change | difference between two structures after superposition | 3N × 1 (N × 1 in the GNM) | Å |
| O_k | overlap | cosine of the angle between v_k and d | scalar | dimensionless |
| u_i | residue share | fraction of a mode's squared displacement on residue i | scalar | dimensionless |
| κ | collectivity | how evenly a mode's motion is spread over the residues | scalar | dimensionless |

### Formulation

**Where the equations come from.** The familiar formula is one mass m on a spring of stiffness k:
Newton's second law with [Hooke's law](https://en.wikipedia.org/wiki/Hooke's_law), m ẍ = −k x. Here ẍ (read "x double-dot") is d²x/dt², the
acceleration; for example x = cos 2t has ẍ = −4 cos 2t, so it solves ẍ = −4x. The solutions are
x(t) = a cos ωt + b sin ωt with ω = √(k/m): one frequency forever, with amplitude and phase set by the
start.

**One coordinate.** At a minimum of V the gradient is zero, so V(x) ≈ V(0) + ½ xᵀ H x, with H the
[Hessian](https://en.wikipedia.org/wiki/Hessian_matrix) of second derivatives: the harmonic approximation. The force on coordinate i is −(H x)_i, so
m_i ẍ_i = −Σ_j H_ij x_j: the spring equation with k replaced by a row of H.

**All coordinates at once.** Stacking the 3N rows gives a linear system of second-order
ordinary differential equations (ODEs) with constant coefficients, whose unknown is a function of time,
x(t):

```
M ẍ = −H x
```

As in the structural analysis entry, try a solution in which every coordinate moves in step,
x(t) = v cos(ωt). Then ẍ = −ω² v cos(ωt), and substituting gives the generalized eigenproblem

```
H v = ω² M v
```

M^(−1/2) is the diagonal matrix of reciprocals 1/√m_i; for example a carbon of mass 12 Da gets
1/√12 ≈ 0.289. Substituting x = M^(−1/2) q, with q the mass-weighted coordinates, turns the problem
into an ordinary [symmetric](https://en.wikipedia.org/wiki/Symmetric_matrix) one for the mass-weighted Hessian M^(−1/2) H M^(−1/2), with eigenvalues
λ_k = ω_k². By the [spectral theorem](https://en.wikipedia.org/wiki/Spectral_theorem) it has 3N orthogonal eigenvectors, and at a minimum every λ_k ≥ 0.

**What the solutions are.** In the basis of modes the equations decouple into 3N single springs, so
every solution is a sum of normal modes,

```
x(t) = Σ_k v_k (a_k cos ω_k t + b_k sin ω_k t)
```

with a_k, b_k fixed by the initial positions and velocities. A zero eigenvalue contributes
(a_k + b_k t) v_k instead: a drift with no restoring force, a rigid motion of the whole molecule.

**Elastic network models.** Tirion's simplification replaces the [force field](https://en.wikipedia.org/wiki/Force_field_%28chemistry%29) by a spring of constant γ
between every pair of nodes closer than r_c, so the structure is the minimum by construction. To second
order a spring's stretch is e_ijᵀ (ΔR_j − ΔR_i). The ANM keeps that direction: each contact puts the
3 × 3 block −γ e_ij e_ijᵀ at block (i, j) of H, and each diagonal block is minus the sum of the others
in its row. The GNM penalizes the whole relative displacement, (γ/2) Σ over contacts ‖ΔR_j − ΔR_i‖², so
x, y and z decouple and each sees the same N × N matrix γ Γ, with Γ_ij = −1 for a contact and Γ_ii the
number of contacts of node i. Γ is called the Kirchhoff matrix because Kirchhoff wrote it down for
electrical networks (the resistor-network entry, with unit conductances); it is the graph Laplacian of
the contact graph. All nodes get one mass, so the modes are the eigenvectors of H or Γ.

**Thermal fluctuations.** At temperature T the probability density of x is proportional to
exp(−V(x) / k_B T), the Boltzmann distribution of statistical mechanics. With V quadratic this is a
multivariate Gaussian whose covariance would be k_B T H⁻¹, but H is singular. Superposing each snapshot
onto the reference removes the rigid-body motions, and

```
⟨x xᵀ⟩ = k_B T H⁺,      H⁺ = Σ over λ_k > 0 of v_k v_kᵀ / λ_k
```

⟨ ⟩ is a thermal average: if x_1 is +1 Å half the time and −1 Å the rest, ⟨x_1²⟩ = 1 Å². H⁺, the
Moore–Penrose pseudoinverse, built from unit eigenvectors, inverts H on the nonzero modes and sends
zero modes to 0. The weight 1/λ_k is the [equipartition](https://en.wikipedia.org/wiki/Equipartition_theorem) theorem: each mode holds an average
potential energy k_B T / 2, so its mean squared amplitude is k_B T / λ_k: the slowest modes dominate.
In the GNM, ⟨ΔR_i · ΔR_j⟩ = (3 k_B T / γ) [Γ⁺]_ij, and the [Debye–Waller](https://en.wikipedia.org/wiki/Debye%E2%80%93Waller_factor) relation gives

```
B_i = (8π²/3) ⟨‖ΔR_i‖²⟩ = (8π² k_B T / γ) [Γ⁺]_ii
```

**Known and unknown.** The coordinates R_i, the cutoff r_c and, for NMA, the force field and masses are
given; H or Γ is built from them. The unknowns are the eigenpairs and H⁺. The free parameter γ is
fitted to the experimental B-factors.

**Worked case: three beads.** Beads P, Q, R lie in a row, joined by springs P–Q and Q–R, with γ = 1 and
unit masses. For motion along the chain the scalar equations are

```
ẍ_P = −(x_P − x_Q)
ẍ_Q = −(x_Q − x_P) − (x_Q − x_R)
ẍ_R = −(x_R − x_Q)
```

so ẍ = −Γ x with x = (x_P, x_Q, x_R) and

```
      P    Q    R
Γ = [ 1    −1   0  ]   P
    [ −1   2    −1 ]   Q
    [ 0    −1   1  ]   R
```

The eigenvalues are 0, 1 and 3, with eigenvectors (1, 1, 1), (1, 0, −1) and (1, −2, 1):

```
[ 1    −1   0  ]   [ 1  ]   [ 1  ]       [ 1  ]
[ −1   2    −1 ] × [ 0  ] = [ 0  ] = 1 × [ 0  ]
[ 0    −1   1  ]   [ −1 ]   [ −1 ]       [ −1 ]

[ 1    −1   0  ]   [ 1  ]   [ 3  ]       [ 1  ]
[ −1   2    −1 ] × [ −2 ] = [ −6 ] = 3 × [ −2 ]
[ 0    −1   1  ]   [ 1  ]   [ 3  ]       [ 1  ]
```

The zero mode is a rigid translation. In the slowest nonzero mode P and R move in opposite directions
while Q stays put: Q is a node, and in a protein the residues where a slow GNM mode changes sign mark
the hinges between domains.

The pseudoinverse adds the nonzero modes with unit vectors and weights 1/λ:
Γ⁺ = (1/2)(1, 0, −1)(1, 0, −1)ᵀ + (1/18)(1, −2, 1)(1, −2, 1)ᵀ, which is

```
             P    Q    R
Γ⁺ = (1/9) [ 5    −1   −4 ]   P
           [ −1   2    −1 ]   Q
           [ −4   −1   5  ]   R
```

The diagonal predicts B-factors in the ratio 5 : 2 : 5: the ends fluctuate most, as chain termini do in
real proteins. The slowest mode supplies 1 of the trace 4/3, or 75% of the total fluctuation, because
its weight 1/λ is three times that of the fastest mode. Normalized by the diagonal, the P, R entry is
−4/5 = −0.8: the ends move in opposite directions.

**Why three dimensions give six zero modes.** In the ANM a rigid translation or an infinitesimal
rotation changes no distance, so it stretches no spring and lies in the null space of H; 3D has three
of each. The same three beads in a straight line give a 9 × 9 ANM Hessian of [rank](https://en.wikipedia.org/wiki/Rank_%28linear_algebra%29) 2 with seven
zero modes, because bending stretches no spring to first order. Adding a P–R spring to make an
equilateral triangle of unit side gives eigenvalues 0 (six times), 1.5, 1.5 and 3: only the six
rigid-body motions are free.

### Matrix structure

H is symmetric [positive semidefinite](https://en.wikipedia.org/wiki/Definite_matrix), its null space the six rigid-body motions of a connected
nonlinear structure. In an ENM it is [sparse](https://en.wikipedia.org/wiki/Sparse_matrix), with the 3 × 3 block pattern of the contact graph: each
C-alpha atom has a few to a few dozen neighbors within the cutoff, whatever the protein's size. Γ has
nonpositive off-diagonal entries and zero row sums, and its nullity is the number of
[connected components](https://en.wikipedia.org/wiki/Component_%28graph_theory%29) of the contact graph. All-atom NMA needs a careful energy minimization first,
because away from a minimum H has negative eigenvalues.

### What is computed

Only the lowest 10 to 100 nonzero modes are wanted. For large assemblies they come from
[Lanczos](https://en.wikipedia.org/wiki/Lanczos_algorithm) iteration ([ARPACK](https://en.wikipedia.org/wiki/ARPACK) through SciPy's eigsh) in shift-invert mode, which iterates with the inverse
of H minus a shift so that eigenvalues near the shift converge first. The shift is a small negative
number, because H is singular and cannot be factored at exactly 0. From the modes come predicted
B-factors, a cross-correlation map (entries of H⁺ normalized by their diagonals) and the overlap
O_k = |v_kᵀ d| / (‖v_k‖ ‖d‖) with a known conformational change d, the cosine of the angle between
them. In the worked case d = (2, −1, −1) has overlap √3/2 ≈ 0.87 with the slowest mode and 0.5 with the
fastest; the squares sum to 1 because d is orthogonal to the translation. For many proteins solved open
and closed, one or two of the slowest ANM modes overlap strongly with the change, e.g. the closure of
[adenylate kinase](https://en.wikipedia.org/wiki/Adenylate_kinase)'s LID domain and nucleoside monophosphate (NMP) binding domain over its substrates.
The collectivity κ = exp(−Σ u_i ln u_i) / N, with u_i residue i's share of the mode's squared
displacement (the u_i sum to 1), is 1 when all residues move equally and 1/N when one moves alone.

### Why linear algebra is the right tool

The harmonic approximation makes the ODE linear, and the spectral theorem turns 3N coupled equations
into 3N independent springs. The same eigenvectors then serve the statistical mechanics: the
fluctuation covariance is H⁺, a sum of rank-one terms weighted by 1/λ_k, so a handful of slow modes
carries most of the motion.

### Pitfall worth teaching

The modes are harmonic about one structure. Real energy surfaces are anharmonic with many minima, so a
mode of the open form can predict the direction of closure but not its path or barriers. Proteins in
water are also overdamped: slow motions are diffusive, not oscillations, so only mode shapes and
relative amplitudes should be read. The cutoff matters: too small, and the network falls apart into
extra zero modes, as in the straight ANM chain; too large, and it stiffens uniformly and blurs the
domains. Experimental B-factors also contain lattice disorder, so a perfect fit is not expected.

### Extensions

Tools include ProDy (Python), Bio3D (R), the elNémo and WEBnm@ web servers, and CHARMM or GROMACS for
all-atom NMA. The [Rayleigh quotient](https://en.wikipedia.org/wiki/Rayleigh_quotient) ω² = vᵀ H v / vᵀ M v underlies coarse graining: restricting v to
the rigid motions of blocks of residues (the rotations–translations of blocks method) gives a smaller
generalized eigenproblem whose eigenvalues are upper bounds (the [Rayleigh–Ritz](https://en.wikipedia.org/wiki/Rayleigh%E2%80%93Ritz_method) principle). The
covariance of an MD trajectory gives [principal component analysis](https://en.wikipedia.org/wiki/Principal_component_analysis) (PCA) of the motion, also called
essential dynamics, the decomposition of the population genetics PCA entry. For small molecules,
Wilson's GF method, named for its kinematic matrix G and force-constant matrix F (Wilson, Decius and
Cross, Molecular Vibrations), solves the same eigenproblem to assign vibrational spectra. The
sparse eigensolvers are those of the spectral clustering entry.

### Terminology

How this field's vocabulary reads as linear algebra.

| Domain term | In linear algebra |
|---|---|
| normal mode v_k | an eigenvector of H v = ω² M v; every coordinate oscillates in step at frequency ω_k |
| normal mode analysis (NMA) | the eigenpairs of the Hessian at an energy minimum |
| Hessian H | second derivatives of the potential energy V; the molecule's stiffness matrix |
| mass-weighted Hessian | M^(−1/2) H M^(−1/2), symmetric, with eigenvalues ω² |
| elastic network model (ENM) | identical Hookean springs of constant γ between nodes closer than r_c |
| Kirchhoff matrix Γ (GNM) | the graph Laplacian of the contact graph, N × N |
| ANM Hessian | 3N × 3N, with the 3 × 3 block −γ e_ij e_ijᵀ for each contact i, j |
| zero modes | the null space of H; three rigid translations and three rigid rotations |
| slow (low-frequency) modes | eigenvectors of the smallest nonzero eigenvalues; largest thermal amplitude |
| hinge site | a residue where a slow mode changes sign |
| B-factor (temperature factor) B_i | (8π²/3) ⟨‖ΔR_i‖²⟩, proportional to [Γ⁺]_ii in the GNM |
| cross-correlation map | the entries of H⁺ (or Γ⁺) normalized by their diagonals |
| overlap O_k | cosine of the angle between v_k and an observed conformational change d |
| collectivity κ | exp(−Σ u_i ln u_i) / N, how evenly a mode's motion is spread over the residues |

---

[Back to the index](/r/LinearAlgebra/wiki/applications)
