# Applied Linear Algebra: An Initial Collection

**Version 0.1 — seed set of 10 problems**

Selection criteria for this first pass:

1. **One application domain each.** No two entries come from the same subfield or community of practice. At the coarse level used in the companion index, three entries fall under Engineering (civil/mechanical FEA, aerospace/control, communications) and two under Computer Science (network science, computer vision); these are distinct disciplines in practice, sharing only a top-level bucket. The set spans seven coarse fields and ten distinct subfields.
2. **One distinct linear-algebra concept each.** Entry 1 is a sparse SPD solve; entry 5 is a nonnegative-matrix spectral radius; entry 7 is linear algebra over a finite field, a number system with finitely many elements (defined under Difficulty tiers). If two problems reduce to the same mathematical object, only one is in the seed set and the other is in the backlog.
3. **Deployed, not illustrative.** Every entry is something an engineer, scientist, or company actually runs in production or in published research — not a textbook exercise dressed in application clothing.
4. **The matrix structure is the point.** In each case, *what kind of matrix it is* (sparse, symmetric, stochastic, rank-deficient, over GF(2), the numbers 0 and 1 with arithmetic modulo 2) determines which algorithm is viable. That is the through-line worth teaching.

## Entry template

Each entry follows the same template so the collection can grow uniformly.

1. **Start here** — the problem in plain terms, for a reader with calculus and a first course in linear
   algebra who knows nothing about the field. No domain jargon, no notation; it should be readable by
   someone deciding whether this is even the right entry. Collapsed by default where the renderer
   supports it.
2. **Field** and **Tier**.
3. **Scalars and vectors** — the scalar field and the vector space, stated explicitly rather than left
   to be inferred. Which field the scalars come from (ℝ, ℂ, GF(2), GF(p), ℚ), what the vectors actually
   are (ℝⁿ for a stated n, polynomials of degree at most 3, continuous functions on [0,1], the tensor
   product (ℂ²)^⊗n), and where the objects live when that is easy to get wrong — that flux vectors and
   concentration vectors inhabit *different* spaces, that a probability distribution is not a subspace,
   that a covariance matrix is a vector in the space of symmetric matrices, that an essential matrix is
   determined only up to scale. Both values are also index columns (`scalar_field`, `vector_space`).
4. **Underlying equations** — one line saying whether a differential equation sits underneath the
   linear algebra, and which kind: ordinary or partial, deterministic or stochastic, linear or not. When
   there is none, the entry says so and names what the model is instead (an accounting identity, a
   difference equation, projective geometry, a statistical decomposition). Also an index column.
5. **The problem**.
6. **Variables** — a table introducing every scalar, vector, and matrix before it is used: its symbol,
   its name in the field, what information it holds, its shape, and its physical units (or
   "dimensionless", or a note when units are mixed). No symbol appears in an equation before it appears
   here.
7. **Formulation** — the equations, each followed by a statement of what it models. When the linear
   algebra comes from a differential equation, the formulation starts from that equation, shows the step
   that produces the matrix problem (discretization, a steady-state assumption, separation of
   variables), and says what the matrix solution means for the solutions of the differential equation.
8. **Matrix structure**, **What is computed**, **Why linear algebra is the right tool**, **Pitfall worth
   teaching**.
9. **Terminology map** — the field's vocabulary against the linear-algebra object each word names.
10. **Extensions**.

**A rendering caveat.** The "Start here" block uses `<details>`/`<summary>`, which collapses on GitHub,
in Quarto and Jupyter Book output, and in most static site generators — but **not on a Reddit wiki**,
which renders markdown only and strips raw HTML. The wiki build must therefore emit that block as an
ordinary `### Start here` subsection instead. Since the wiki is the planned front door for a
non-specialist audience, and this section is written precisely for that audience, it should stay at the
top of the page there rather than being moved or dropped.

---

# Audience and organizing principle

**Primary reader.** Someone competent in linear algebra who encounters a question posed in a field they
do not know. This is the recurring situation in general linear-algebra forums: a question arrives
carrying domain vocabulary — stiffness matrix, flux mode, syndrome, EOF, Leontief inverse — and the
mathematics is well within the reader's reach once the terminology is decoded. The bottleneck is
translation, not technique.

That makes the collection a **decoder**, not only a tour. Three consequences:

1. **Field is the primary organizing axis.** A reader arrives knowing the domain the question came from
   and nothing else about it. Navigation is by discipline; the linear-algebra concept index is the
   secondary cross-reference, for the reverse lookup ("this is a dominant-eigenvector problem — where
   else does that show up?").
2. **Every entry carries a terminology map.** A two-column table from the field's own vocabulary to the
   linear-algebra object it names. These are aggregated into a single sorted lookup table,
   `domain_terminology_map.csv`, which is the fastest path for a reader who has one unfamiliar word and
   needs to know what it means mathematically.
3. **Entries must name the question shapes, not just the mathematics.** What a practitioner in the field
   actually asks — and the vocabulary they will use to ask it — matters as much as the formulation.

The three kinds of question this is meant to serve (homework, a problem at work, and general curiosity
from outside mathematics) differ in tier but not in structure: all three need the same domain-to-linear-
algebra bridge, which is why the tier scheme and the field axis are independent of one another.

## Navigation taxonomy

17 fields, sized so that no heading is a catch-all. `Engineering` and `Computer Science` from the
original index were too coarse to navigate once field became the primary axis, and have been split; the
original coarse `field` column is retained for coarse filtering.

| Field | Entries | of which Tier 1 |
|---|---|---|
| Computer Graphics & Vision | 6 | 5 |
| Life Sciences | 5 | 0 |
| Machine Learning & Data | 5 | 0 |
| Mathematics & Numerical Analysis | 4 | 3 |
| Signal Processing | 4 | 2 |
| Chemistry & Chemical Engineering | 3 | 1 |
| Computer Science & Networks | 3 | 1 |
| Earth & Climate Science | 3 | 1 |
| Economics, Finance & Operations Research | 3 | 1 |
| Electrical Engineering | 3 | 1 |
| Statistics | 3 | 3 |
| Civil & Mechanical Engineering | 2 | 1 |
| Communications & Information Theory | 2 | 2 |
| Control & Robotics | 2 | 1 |
| Cryptography & Security | 2 | 1 |
| Medicine & Imaging | 1 | 0 |
| Physics & Quantum Chemistry | 1 | 0 |

**Thin spots now visible.** Making field the navigation spine exposes where the spine is weak. Medicine &
Imaging and Physics & Quantum Chemistry each hold a single entry, and Physics is represented only by
quantum mechanics — nothing from classical mechanics, optics, thermodynamics, or relativity. Life
Sciences and Machine Learning & Data have no Tier 1 entry at all, so a reader arriving from either field
meets an eigenvalue problem immediately. There is no materials science, no acoustics, and no social
science outside economics. These gaps were invisible when the collection was organized by concept.

# Difficulty tiers

Three tiers, defined by what a reader must already know. Tier boundaries are set by *prerequisite
knowledge*, not by how hard the problem is to solve or how large the matrices get — a Tier 1 entry may
involve a genuinely difficult modeling question, and a Tier 3 entry may reduce to a two-line
computation once the setup is understood.

### Tier 1 — first-course linear algebra, up to but not including eigenvalues

Vectors and matrices, matrix multiplication and its noncommutativity, linear systems and Gaussian
elimination, LU, inverses, determinants, rank, the four fundamental subspaces, linear independence,
bases and dimension, change of basis, inner products and orthogonality, projections, least squares,
Gram–Schmidt and QR.

Deliberately included at this tier: vector spaces over scalars other than the reals. Polynomial spaces,
complex-valued vectors, finite fields such as GF(2) and GF(p), and function spaces with an integral
inner product all belong here, because each of them exercises the *definition* of a vector space rather
than any machinery beyond a first course. So do the 2D and 3D graphics transformations, which are pure
change-of-basis and composition problems in small dimension.

Few readers arrive having taken abstract algebra, so the collection defines its one piece of algebraic
vocabulary here, in plain terms, rather than assuming it:

A **field** is a number system in which addition, subtraction, multiplication, and division by any nonzero number all behave the way they do for ordinary numbers. The rational numbers ℚ, the real numbers ℝ, the complex numbers ℂ, and the integers modulo a prime p all qualify. The integers modulo 6 do not: there 2 × 3 = 0, so 2 has no reciprocal and nothing can be divided by 2. The scalars of every vector space come from a field, which is why each entry names its scalar field.

**GF(2)** is the smallest field: just the two numbers 0 and 1, added and multiplied modulo 2, so 1 + 1 = 0. Addition is the same as XOR, and multiplication is the same as AND. GF(p) is the same construction using the integers modulo a prime p. Everything about subspaces, bases, rank, and null spaces works over GF(2) exactly as over the
real numbers. Lengths, angles, and least squares do not. They depend on a vector's dot product with
itself being positive, which fails over GF(2): the nonzero vector (1, 1) has (1, 1)·(1, 1) = 1 + 1 = 0,
so it is orthogonal to itself.

Larger finite fields such as GF(2ᵐ), which Reed–Solomon codes need, are built as polynomials modulo an
irreducible polynomial. That construction requires quotient rings and is Tier 3.

### Tier 2 — eigenvalues, eigenvectors, and later-course material

Eigenvalues and eigenvectors, diagonalization, the spectral theorem, similarity, the SVD, positive
definiteness, matrix norms and condition numbers, pseudoinverses, Perron–Frobenius, stochastic matrices
and stationary distributions, Jordan form, and iterative methods for large systems.

### Tier 3 — requires substantial mathematics outside linear algebra

The linear algebra may be no harder than Tier 2, but the problem cannot be posed or interpreted without
another body of theory: differential equations (ordinary or partial), abstract algebra beyond basic
finite fields (field extensions, quotient rings, group representations), measure-theoretic probability
or stochastic processes, convex analysis and duality, functional analysis, or algebraic geometry. The
index records the specific prerequisite per entry in `prereq_beyond_la`.

**Differential equations always mean Tier 3.** If a differential equation appears anywhere in how an
entry is posed — ordinary or partial, deterministic or stochastic, linear or not — the entry is Tier 3,
even when the matrix problem it produces is first-course linear algebra. "How an entry is posed" means
its Formulation: if the Formulation derives the matrix problem from a differential equation, the entry
is Tier 3, even when the equation's only role is that derivation, as with a steady state (setting a
time derivative to zero) or separation of variables. Reading such an entry still requires understanding
the equation and what its solutions are. Each entry's `underlying_equations` field says which equation
is involved, or states that there is none.

The test is whether the entry *uses* the equation, not whether some equation *exists*. Many static
models are special cases of a dynamic one. The static Leontief model, for instance, is the steady state
of the dynamic Leontief ODE. When an entry derives its matrix problem without the differential equation
and mentions the dynamic model only in Extensions, the equation is not part of how the entry is posed.
In that case it raises the entry's ceiling, as described in the next section.

### Boundary conventions

- An entry is tiered by **how it is posed in this collection**, not by the deepest treatment that
  exists in the literature. The index carries a separate `tier_ceiling` column recording the tier its
  extensions reach.
- Where a Tier 2 or Tier 3 entry has a genuine Tier 1 entry point — static GNSS trilateration under
  Kalman filtering, chemical-equation balancing under stoichiometric matrices, the 2D homography under
  multiple-view geometry — that on-ramp is named in the entry rather than split into a separate row.
- A differential equation that appears only in an entry's **Extensions**, and that the Formulation
  does not use, raises the entry's `tier_ceiling` but not its tier. The Leontief entry is the example.
  Its Formulation derives (I − A) x = d from an accounting identity and a fixed-proportions assumption,
  with no time derivative anywhere, so it is Tier 1. The dynamic model, whose steady state gives the same
  equation, is an ODE noted under Extensions, so its ceiling is 3. The EOF entry is treated the same way.
  If an entry's Formulation instead reached its matrix problem by setting the ODE's time derivative to
  zero, the entry would be Tier 3.
- Calculus is assumed throughout and does not by itself raise an entry to Tier 3. Derivatives and
  integrals are not differential equations: the Fourier-series projection needs integration, and the
  finite-difference stencil entry approximates derivatives, but neither poses an equation whose unknown
  is a function, and both stay at Tier 1.
- Difference equations are not differential equations. PageRank's random-surfer recurrence,
  π_{t+1} = G π_t, is a discrete-time linear system and does not by itself raise the tier.

**Current distribution.** Of the 10 seed entries, 2 are Tier 1
(Leontief input-output economics; Linear error-correcting codes), 3 are Tier 2, and 5 are Tier 3. Across all
52 catalogued problems the split is 23 / 14 / 15.

---

## 1. Structural analysis: will the bridge hold, and at what frequency does it ring?

<details>
<summary><b>Start here — the problem in plain terms</b></summary>

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
shapes is what [eigenvalues](https://en.wikipedia.org/wiki/Eigenvalues_and_eigenvectors) are for, and it is why bridges are checked against the frequencies of
marching feet and wind.

</details>

**Field:** Civil and mechanical engineering ([finite element](https://en.wikipedia.org/wiki/Finite_element_method) analysis)

**Tier:** 3 — the matrix problem comes from the [ODE](https://en.wikipedia.org/wiki/Ordinary_differential_equation) system M ü + K u = f: statics sets ü = 0, vibration assumes harmonic motion. On-ramp: the static solve K u = f itself needs only first-course linear algebra.

**Scalars and vectors.** Scalar field: R. Vectors: R^n, n = number of unrestrained degrees of freedom (2 or 3 per node); displacements and forces live in the same space.

**Underlying equations.** Linear second-order ODE system M ü + K u = f, from the [PDE](https://en.wikipedia.org/wiki/Partial_differential_equation) of [linear elasticity](https://en.wikipedia.org/wiki/Linear_elasticity); statics sets ü = 0.

**The problem.** Given a structure — [truss](https://en.wikipedia.org/wiki/Truss), bridge deck, turbine blade, engine block — discretized into elements, find the displacement at every node under a given load, and separately find the frequencies at which the structure resonates.

**Variables.**
| Symbol | Name | What it holds | Shape | Units |
|---|---|---|---|---|
| n | number of degrees of freedom (DOFs) | count of unrestrained displacement components: 2 per free joint in a planar truss, 3 in a space truss | scalar (integer) | — |
| u | displacement vector | how far each joint moves, in each coordinate direction, from its unloaded position | n × 1 | m |
| f | load vector | external force applied at each joint in each direction: gravity, traffic, wind | n × 1 | N |
| K | global stiffness matrix | k_ij is the force that appears at DOF i when DOF j alone is displaced by one unit | n × n | N/m |
| k_e | element stiffness | stiffness of one bar along its axis, k_e = E A / L | scalar | N/m |
| E, A, L | Young's modulus, cross-sectional area, length | material stiffness and geometry of one bar | scalars | Pa (N/m²), m², m |
| M | mass matrix | how the structure's mass is distributed over the DOFs | n × n | kg |
| ü | acceleration vector | second time derivative of u | n × 1 | m/s² |
| φ | mode shape | the relative pattern of motion in one mode of vibration; only its shape matters, so it is normalized | n × 1 | dimensionless |
| ω | natural angular frequency | how fast a mode oscillates; the frequency in hertz is ω / 2π | scalar | rad/s |
| λ | eigenvalue | λ = ω² | scalar | s⁻² |

In a truss every DOF is a translation, so every entry of u is in metres. Frames and beams add rotational DOFs, and then u mixes metres with radians and f mixes newtons with newton-metres. The equations are unchanged, but entries of K then carry different units, which is one reason raw entry sizes of K should not be compared directly.

**Formulation.** **Where the equations come from.** The underlying physics is linear elasticity: for small deformations, stress in a solid is proportional to strain, and the motion obeys a partial differential equation in space and time. The finite element method replaces the continuous structure by its n joint displacements, which turns that PDE into a system of n linear second-order ordinary differential equations in time:

```
M ü(t) + K u(t) = f(t)
```

Row i is Newton's second law for DOF i: mass times acceleration equals the applied force minus the elastic restoring force from the bars attached there. (Damping is omitted here; it adds a term C u̇.)

**Statics.** If loads are applied slowly and held, the structure comes to rest, ü = 0, and the ODE reduces to a linear system:

```
K u = f
```

This models force balance at every joint: row i says that the elastic forces from all the bars meeting at DOF i sum to the external load there. The solution u is the deformed shape. The force in each bar then follows from its change in length, k_e times elongation. The system has a unique solution only if the supports prevent every rigid-body motion; otherwise K is singular (see the pitfall below).

**Free vibration.** With no load, f = 0, look for solutions in which every DOF oscillates in step at one frequency, u(t) = φ cos(ωt). Then ü = −ω² φ cos(ωt), and substituting gives

```
K φ = λ M φ,     λ = ω²
```

A nonzero φ exists only for special values of λ, the eigenvalues. This is what the eigenproblem means for the ODE: there are exactly n such synchronized motions, the modes, and because the equations are linear, every free vibration is a superposition of them,

```
u(t) = Σ_i φ_i (a_i cos ω_i t + b_i sin ω_i t)
```

with the constants a_i, b_i fixed by the initial displacement and velocity. A load that oscillates near one of the ω_i drives that mode into [resonance](https://en.wikipedia.org/wiki/Resonance).

**Matrix structure.** `K` is [symmetric](https://en.wikipedia.org/wiki/Symmetric_matrix) [positive definite](https://en.wikipedia.org/wiki/Definite_matrix) (after boundary conditions are applied), extremely [sparse](https://en.wikipedia.org/wiki/Sparse_matrix) — each node couples only to its mesh neighbors — and often banded or block-structured. Industrial models run 10⁶–10⁸ degrees of freedom.

**What is computed.** Sparse [Cholesky](https://en.wikipedia.org/wiki/Cholesky_decomposition) with fill-reducing reordering ([AMD](https://en.wikipedia.org/wiki/Minimum_degree_algorithm), [nested dissection](https://en.wikipedia.org/wiki/Nested_dissection)) for the static solve; [Lanczos](https://en.wikipedia.org/wiki/Lanczos_algorithm) or shift-and-invert [Arnoldi](https://en.wikipedia.org/wiki/Arnoldi_iteration) for the lowest few dozen eigenpairs. Nobody forms `K⁻¹`.

**Why linear algebra is the right tool.** The underlying PDE (linear elasticity) is linear in the small-strain regime, so superposition holds exactly: the response to a load combination is the combination of responses. Sparsity is a direct encoding of physical locality.

**Pitfall worth teaching.** A near-singular `K` is not a numerical accident — it means the structure has a near-mechanism, a direction in which it can deform with almost no restoring force. The [condition number](https://en.wikipedia.org/wiki/Condition_number) is a physical diagnostic, not just a numerical one.

**Terminology map.** How this field's vocabulary reads as linear algebra.

| Domain term | In linear algebra |
|---|---|
| stiffness matrix | the coefficient matrix K; symmetric positive definite once restraints are applied |
| degree of freedom (DOF) | one scalar unknown — one component of the displacement vector |
| load vector | the right-hand side b |
| restraint / boundary condition | deleting the corresponding rows and columns, or adding constraint rows |
| assembly | summing small element matrices into the global matrix at shared DOF indices |
| mode shape | an eigenvector of K phi = lambda M phi |
| natural frequency | square root of the corresponding eigenvalue |
| mechanism | a nontrivial null space of K — the structure can move with no restoring force |
| bandwidth / skyline | the sparsity pattern induced by node numbering |

**Extensions.** [Buckling](https://en.wikipedia.org/wiki/Buckling) as a different [generalized eigenproblem](https://en.wikipedia.org/wiki/Eigendecomposition_of_a_matrix#Generalized_eigenvalue_problem) (`K φ = λ K_geometric φ`); substructuring and domain decomposition; the same [modal analysis](https://en.wikipedia.org/wiki/Normal_mode) applied to molecules gives normal-mode analysis and elastic network models.

---

## 2. Kalman filtering: where is the vehicle, given noisy and incomplete measurements?

<details>
<summary><b>Start here — the problem in plain terms</b></summary>

You are trying to work out where a moving vehicle is, and you have two unreliable sources. One is dead
reckoning: start from a known point and add up your measured motion. It is smooth but drifts, because
small errors accumulate. The other is [GPS](https://en.wikipedia.org/wiki/Satellite_navigation): it does not drift, but each individual reading is noisy and
sometimes missing entirely.

Neither is right. The sensible thing is a compromise, weighted by how much you trust each — and the
trick is that "how much you trust each" is something you can compute rather than guess. If dead
reckoning has been running unchecked for a while, trust it less. If GPS has just given three consistent
readings, trust it more.

A [Kalman filter](https://en.wikipedia.org/wiki/Kalman_filter) does exactly this, once per time step, forever. What makes it more than a rule of thumb
is that it carries an explicit bookkeeping of its own uncertainty — not one number but a whole table,
because being unsure about north-south position is different from being unsure about speed, and the two
uncertainties interact.

</details>

**Field:** Aerospace, robotics, control engineering

**Tier:** 3 — the model is a stochastic ODE discretized in time, and the filter propagates a probability distribution. On-ramp: static GNSS [trilateration](https://en.wikipedia.org/wiki/True-range_multilateration), a plain [least-squares](https://en.wikipedia.org/wiki/Least_squares) problem.

**Scalars and vectors.** Scalar field: R. Vectors: state in R^n (n = 6-50); measurements in R^m; [covariances](https://en.wikipedia.org/wiki/Covariance_matrix) live in Sym_n, the real vector space of symmetric n x n matrices, dimension n(n+1)/2.

**Underlying equations.** Linear ODE driven by random noise (a [stochastic differential equation](https://en.wikipedia.org/wiki/Stochastic_differential_equation)), dx/dt = A x + noise, discretized exactly to x_{k+1} = F x_k + w_k.

**The problem.** A vehicle carries an [inertial measurement unit](https://en.wikipedia.org/wiki/Inertial_measurement_unit) that drifts, plus a GNSS receiver that is accurate but intermittent and noisy. Produce a continuously updated best estimate of position, velocity, and attitude — with an honest uncertainty attached.

**Variables.**
| Symbol | Name | What it holds | Shape | Units |
|---|---|---|---|---|
| k | time-step index | which update we are on | integer | — |
| Δt | time step | interval between updates | scalar | s |
| x_k | state vector | the quantities being estimated at step k; in the running example, position p and velocity v along one axis, x = [p, v]ᵀ | n × 1 (n = 2 here) | mixed: m and m/s |
| A | continuous-time system matrix | how the state changes instantaneously; [[0, 1], [0, 0]] says dp/dt = v and dv/dt = 0 apart from noise | n × n | entries in s⁻¹ |
| F | state-transition matrix | how the state at step k predicts the state at step k+1; here [[1, Δt], [0, 1]] | n × n | mixed: dimensionless and s |
| w_k | process noise | what the model leaves out over one step: unknown accelerations, gusts, wheel slip | n × 1 | same as x |
| Q | process-noise covariance | how large and how correlated w_k is | n × n | products of state units: m², m²/s, m²/s² |
| z_k | measurement vector | what the sensor reports at step k; for GNSS, a measured position | m × 1 (m = 1 here) | m |
| H | observation matrix | which combination of the state the sensor sees; [1, 0] when it measures position only | m × n | measurement units per state unit |
| η_k | measurement noise | sensor error at step k | m × 1 | m |
| R | measurement-noise covariance | spread of the sensor error; a few metres squared for a consumer GNSS fix | m × m | m² |
| x̂⁻, x̂⁺ | state estimate | the filter's best estimate before and after using z_k | n × 1 | same as x |
| P⁻, P⁺ | estimate covariance | uncertainty of the estimate before and after using z_k; diagonal entries are variances (squared standard deviations), off-diagonal entries say how errors in different components move together | n × n | products of state units |
| ỹ | innovation | measured minus predicted measurement | m × 1 | m |
| K | Kalman gain | how much to correct each state component per unit of innovation | n × m | state units per measurement unit: dimensionless for p, s⁻¹ for v |
| N(0, Q) | Gaussian distribution | mean zero, covariance Q | — | — |

**Formulation.** **Where the equations come from.** The vehicle's motion obeys an ordinary differential equation in continuous time. For the constant-velocity model, dp/dt = v and dv/dt = a(t), where the acceleration a(t) is unknown and is modelled as random noise. In matrix form this is dx/dt = A x + noise. Because the ODE is driven by a random input it is a stochastic differential equation, and its solution is not a single trajectory but a probability distribution over trajectories. That is why the filter carries a covariance and not just an estimate.

Integrating the ODE exactly over one step gives the discrete model. For this A the [matrix exponential](https://en.wikipedia.org/wiki/Matrix_exponential) is simple: F = exp(A Δt) = [[1, Δt], [0, 1]], which just says p_{k+1} = p_k + Δt v_k and v_{k+1} = v_k.

**The model.**

```
x_{k+1} = F x_k + w_k,     w_k ~ N(0, Q)      (dynamics)
z_k     = H x_k + η_k,     η_k ~ N(0, R)      (measurement)
```

The first line models how the true state evolves between measurements; the second models what the sensor reports about it. Both are linear, and both noises are [Gaussian](https://en.wikipedia.org/wiki/Multivariate_normal_distribution).

**The filter.** Each step has two stages. *Predict* pushes the estimate and its uncertainty forward through the dynamics:

```
x̂⁻ = F x̂⁺_{k−1}
P⁻ = F P⁺_{k−1} Fᵀ + Q
```

F P Fᵀ is how a covariance transforms under the linear map F, and adding Q makes uncertainty grow by what the model leaves out. *Update* blends the prediction with the new measurement, weighted by their uncertainties:

```
ỹ  = z_k − H x̂⁻                      (innovation)
K  = P⁻ Hᵀ (H P⁻ Hᵀ + R)⁻¹           (Kalman gain)
x̂⁺ = x̂⁻ + K ỹ
P⁺ = (I − K H) P⁻
```

H P⁻ Hᵀ + R is the covariance of the innovation: prediction uncertainty seen through the sensor, plus sensor noise. When R is large relative to H P⁻ Hᵀ the gain is small and the filter mostly trusts its prediction; when R is small it mostly trusts the sensor.

**What a solution means.** At each step the output is a Gaussian distribution with mean x̂⁺ and covariance P⁺. For a linear model with Gaussian noise this is exact: it is the distribution of the true state given every measurement so far, and x̂⁺ is the minimum-mean-squared-error estimate.

**Matrix structure.** Small and dense (state dimension 6–50 for navigation, thousands for [SLAM](https://en.wikipedia.org/wiki/Simultaneous_localization_and_mapping)). `P`, `Q`, `R` are symmetric positive semidefinite. The covariance recursion is a [discrete Riccati equation](https://en.wikipedia.org/wiki/Algebraic_Riccati_equation).

**What is computed.** A weighted least-squares update, done recursively so no measurement history is stored. Square-root and UD-factored forms (Potter, Bierman–Thornton) propagate a Cholesky factor of `P` instead of `P` itself to guarantee the covariance stays positive definite in finite precision — this is why Apollo's navigation filter was implemented in square-root form.

**Why linear algebra is the right tool.** The Kalman gain is an [orthogonal-projection](https://en.wikipedia.org/wiki/Projection_%28linear_algebra%29) operator in a metric defined by the noise covariances. "Optimal fusion of uncertain information" turns out to be a projection, which is why the formula is a matrix expression and not a heuristic.

**Pitfall worth teaching.** [Rank](https://en.wikipedia.org/wiki/Rank_%28linear_algebra%29) of the [observability](https://en.wikipedia.org/wiki/Observability) matrix `[H; HF; HF²; …]` tells you which state directions the sensors can ever pin down. An unobservable direction shows up as a covariance that grows without bound — the filter tells you honestly that it does not know.

**Terminology map.** How this field's vocabulary reads as linear algebra.

| Domain term | In linear algebra |
|---|---|
| state vector | the unknown x being estimated |
| process noise / measurement noise | the covariance matrices Q and R |
| covariance matrix P | the uncertainty ellipsoid; symmetric positive semidefinite |
| Kalman gain | the projection weight matrix that blends prediction and measurement |
| innovation / residual | z - Hx, the part of the measurement the prediction did not explain |
| observation model H | the linear map from state space to measurement space |
| observability | rank of the stacked matrix [H; HF; HF^2; ...] |
| filter divergence | P losing positive definiteness in finite precision, or an unobservable direction growing without bound |
| square-root filter | propagating a Cholesky factor of P instead of P |

**Extensions.** Static GNSS trilateration as the nonrecursive special case ([Gauss–Newton](https://en.wikipedia.org/wiki/Gauss%E2%80%93Newton_algorithm) on an overdetermined system); [extended and unscented](https://en.wikipedia.org/wiki/Extended_Kalman_filter) filters for nonlinear dynamics; [ensemble Kalman](https://en.wikipedia.org/wiki/Ensemble_Kalman_filter) filters for weather [data assimilation](https://en.wikipedia.org/wiki/Data_assimilation) at 10⁸ state dimensions.

---

## 3. Computed tomography: reconstructing an interior from its shadows

<details>
<summary><b>Start here — the problem in plain terms</b></summary>

Shine an X-ray through a body and it comes out dimmer. How much dimmer tells you the total amount of
dense material it passed through — but not where along the path that material was. One reading is a sum
along a line.

Now take hundreds of thousands of such readings, along lines at every angle. Each one is a different sum
over a different set of points. The question is whether all those sums together pin down the individual
values: can you reconstruct a picture of the interior from a very large collection of line totals?

Mostly yes, and that reconstruction is what a [CT](https://en.wikipedia.org/wiki/CT_scan) scanner computes between the scan finishing and the
image appearing. But "mostly" hides the interesting part. Some patterns of density barely affect any
measurement — they are nearly invisible to every ray — so their reconstructed values are wildly
sensitive to noise. The fix is to add an assumption, usually that real tissue does not vary wildly from
one point to the next, and that assumption is doing real work in the picture a radiologist reads.

</details>

**Field:** Medical imaging (and, with different physics, seismic tomography and electron microscopy)

**Tier:** 3 — the linearity comes from solving the [Beer–Lambert](https://en.wikipedia.org/wiki/Beer%E2%80%93Lambert_law) ODE along each ray and taking a logarithm; [ill-posedness](https://en.wikipedia.org/wiki/Well-posed_problem) is read from the singular-value spectrum. On-ramp: a small noisy A x = b solved naively and with regularization.

**Scalars and vectors.** Scalar field: R (nonnegative in practice). Vectors: image in R^N (N voxels); measurements in R^M (M rays); A maps R^N to R^M with M != N.

**Underlying equations.** First-order linear ODE along each ray (Beer–Lambert law), dI/ds = −μ I; the logarithm of its solution is linear in μ.

**The problem.** An X-ray source and detector rotate around a patient. Each measurement is the total attenuation along one line through the body. Recover the 3D attenuation field.

**Variables.**
| Symbol | Name | What it holds | Shape | Units |
|---|---|---|---|---|
| μ(r) | linear attenuation coefficient | fraction of X-ray photons removed per unit path length at location r; this is what the image shows | function of position | m⁻¹ (clinically often cm⁻¹) |
| s | path length | distance travelled along a ray | scalar | m |
| I(s) | beam intensity | photon flux remaining after travelling distance s | scalar | photon counts |
| I₀ | unattenuated intensity | detector reading with nothing in the beam (from calibration) | scalar per ray | photon counts |
| I_i | measured intensity | detector reading for ray i | scalar | photon counts |
| N | number of voxels | the image is divided into N small cubes (pixels in 2D) | integer | — |
| M | number of rays | detector elements × projection angles | integer | — |
| x | image vector | x_j is μ inside voxel j, voxels listed in a fixed order | N × 1 | m⁻¹ |
| b | measurement vector (sinogram) | b_i = −ln(I_i / I₀), total attenuation along ray i | M × 1 | dimensionless |
| A | system matrix (forward projector) | a_ij is the length of ray i inside voxel j; zero for the vast majority of pairs | M × N | m |
| λ | regularization weight | how strongly smoothness is favoured over fitting the data (used in What is computed) | scalar | chosen so the two terms are comparable |
| L | regularization operator | typically differences between neighbouring voxels, so ‖L x‖ measures roughness | p × N | depends on the choice |

**Formulation.** **Where the equations come from.** As a beam travels a short distance ds through material, the fraction of photons removed is μ ds. The intensity along a ray therefore obeys a first-order linear ordinary differential equation, the Beer–Lambert law:

```
dI/ds = −μ(s) I(s)
```

Its solution is I = I₀ exp(−∫ μ(s) ds). Taking the logarithm:

```
b_i = −ln(I_i / I₀) = ∫_{ray i} μ(s) ds
```

This is the step that makes CT a linear problem. The raw reading depends exponentially on μ, but the log-transformed reading is a line integral of μ, which is linear in μ. The set of all such line integrals is the [Radon transform](https://en.wikipedia.org/wiki/Radon_transform) of μ.

**Discretization.** Assume μ is constant inside each voxel. The integral along ray i then becomes a sum over the voxels it crosses, each term being the length inside the voxel times the value there:

```
b_i = Σ_j a_ij x_j      for every ray i,      i.e.   A x = b
```

Units check: metres times m⁻¹ is dimensionless, matching b. This models each measurement as the total attenuation met by one ray, and it defines M equations in N unknowns.

**What a solution means.** x is an estimate of μ, one value per voxel. For display it is converted to [Hounsfield units](https://en.wikipedia.org/wiki/Hounsfield_scale), HU = 1000 (μ − μ_water) / μ_water, which puts water at 0 and air at −1000. The system is not solved exactly: photon counts are noisy, M and N differ, and A is badly conditioned, so the reconstruction is posed as regularized least squares (see What is computed).

**Where the model is approximate.** The ODE assumes a single X-ray energy. Real tubes emit a spectrum, low-energy photons are absorbed first, and μ in fact depends on energy. That mismatch, called beam hardening, is a standard source of artifacts precisely because it violates the linearity above.

**Matrix structure.** Enormous (10⁶–10⁹ rows and columns), very sparse — a ray touches only O(n^{1/3}) of n voxels — and severely ill-conditioned. [Singular values](https://en.wikipedia.org/wiki/Singular_value_decomposition) decay smoothly toward zero with no gap, which is the signature of an ill-posed inverse problem.

**What is computed.** Either [filtered backprojection](https://en.wikipedia.org/wiki/Tomographic_reconstruction) (an analytic spectral inverse, fast, the classical approach) or iterative reconstruction: [Kaczmarz](https://en.wikipedia.org/wiki/Kaczmarz_method)/ART row-action sweeps, [conjugate gradient](https://en.wikipedia.org/wiki/Conjugate_gradient_method) on the normal equations, or a regularized objective

```
min_x ‖A x − b‖² + λ ‖L x‖²      (Tikhonov)
```

with [total-variation](https://en.wikipedia.org/wiki/Total_variation_denoising) penalties now standard in commercial scanners.

**Why linear algebra is the right tool.** Beer–Lambert attenuation is multiplicative in intensity, hence additive in log-intensity — that logarithm is what makes the whole problem linear and the entire field of algebraic reconstruction possible.

**Pitfall worth teaching.** The naive least-squares solution amplifies noise through the small singular values. Regularization is not cosmetic smoothing; it is the choice of which part of the [null space](https://en.wikipedia.org/wiki/Kernel_%28linear_algebra%29) and near-null space to fill in, and it is where clinical judgment enters the mathematics. Fewer projection angles means lower dose to the patient but a worse-conditioned `A` — the linear algebra sits directly on a medical trade-off.

**Terminology map.** How this field's vocabulary reads as linear algebra.

| Domain term | In linear algebra |
|---|---|
| projection / ray sum | one row of A applied to x — a line integral through the object |
| sinogram | the measurement vector b, arranged by angle and detector position |
| attenuation coefficient | the unknown x, one value per voxel |
| system matrix / forward projector | A, the discretized Radon transform |
| backprojection | applying A transpose to the data |
| filtered backprojection (FBP) | an analytic spectral inverse of the forward operator |
| ART / SIRT | Kaczmarz row-action and related simultaneous iterations |
| regularization strength | the Tikhonov parameter lambda trading data fit against smoothness |
| streak artifact | the visible signature of undersampling — energy in the near-null space |

**Extensions.** [Compressed sensing](https://en.wikipedia.org/wiki/Compressed_sensing) MRI (sparsity in a transform domain replaces smoothness); [cryo-EM](https://en.wikipedia.org/wiki/Cryo-electron_microscopy) reconstruction, which adds unknown orientations; [electrical impedance tomography](https://en.wikipedia.org/wiki/Electrical_impedance_tomography), which is nonlinear.

---

## 4. Stoichiometric matrices: what a reaction network can and cannot do at steady state

<details>
<summary><b>Start here — the problem in plain terms</b></summary>

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

</details>

**Field:** Chemistry, chemical engineering, systems biology

**Tier:** 3 — the matrix S is read out of the ODE dc/dt = S v(c), and conservation laws are statements about that ODE's solutions. On-ramp: chemical-equation balancing, a null-space problem with no ODE.

**Scalars and vectors.** Scalar field: Q or R (S itself has integer entries). Vectors: fluxes in R^r (r reactions); concentrations in R^m (m species); S maps flux space to species space - two different spaces that are easy to conflate.

**Underlying equations.** Nonlinear ODE system dc/dt = S v(c); every linear-algebra conclusion uses only the constant matrix S.

**The problem.** Given a network of chemical reactions, determine which combinations of reaction rates are compatible with steady state, which quantities are conserved no matter what the kinetics are, and how many reactions are genuinely independent.

**Variables.**
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

**Formulation.** **Where the equations come from.** Each species' concentration changes at a rate equal to the sum over reactions of (molecules produced or consumed per event) × (events per unit time). That is a system of m ordinary differential equations:

```
dc/dt = S v(c)
```

S is a constant matrix fixed by the chemistry. The fluxes v(c) are the kinetics, and they are generally nonlinear. For example, under [mass action](https://en.wikipedia.org/wiki/Law_of_mass_action) the reaction A + B → C runs at v = k c_A c_B. So the ODE itself is nonlinear, and solving it requires rate constants that are rarely known. The linear algebra here extracts what holds for every possible choice of kinetics.

**Steady state.** A cell in steady operation has dc/dt = 0:

```
S v = 0
```

This models every species being produced exactly as fast as it is consumed. Whatever the kinetics are, any steady-state flux vector lies in the null space of S.

**Conservation laws.** If a vector y satisfies yᵀS = 0, then

```
d(yᵀc)/dt = yᵀ S v = 0      ⟹      yᵀc(t) = yᵀc(0)   for all t
```

This is a statement about the solutions of the nonlinear ODE, obtained without knowing v. Each independent left-null vector removes one degree of freedom, and every trajectory stays on the affine subspace c(0) + range(S) (the [stoichiometric](https://en.wikipedia.org/wiki/Stoichiometry) compatibility class), whose dimension is rank(S).

**Balancing a single reaction.** Atoms are neither created nor destroyed, so a reaction's coefficients s must satisfy Z s = 0: for each element, atoms consumed equal atoms produced. Balancing an equation means finding an integer vector in the null space of Z.

**Matrix structure.** Sparse, integer-valued, typically rank-deficient in both directions. Genome-scale metabolic models reach ~2,000 species × ~3,000 reactions.

**What is computed.**
- **Right null space** of `S`: the space of steady-state flux distributions. Its dimension counts the network's degrees of freedom; its nonnegative extreme rays are the [elementary flux modes](https://en.wikipedia.org/wiki/Elementary_modes).
- **Left null space** of `S`: conservation laws. A vector `y` with `yᵀS = 0` means `yᵀc` is constant for all time, independent of rate constants — conserved moieties like total ATP+ADP+AMP, or total enzyme.
- **Rank** of `S`: the number of independent reactions, which is what distinguishes an overdetermined mechanism from an underdetermined one.

**Why linear algebra is the right tool.** These conclusions hold without knowing a single rate constant. Structural conclusions from the network topology alone are exactly what null spaces deliver, and kinetic parameters are the hardest thing to measure.

**Pitfall worth teaching.** Balancing a chemical equation is finding an integer vector in the null space of the element–species matrix — the same operation students do by trial and error in first-year chemistry. Showing that equivalence is a good hook.

**Terminology map.** How this field's vocabulary reads as linear algebra.

| Domain term | In linear algebra |
|---|---|
| stoichiometric matrix S | species by reactions, signed integer coefficients |
| flux | v, the vector of reaction rates |
| steady state | Sv = 0 — v lies in the right null space |
| conserved moiety | a left null vector y; y^T c is constant for all time |
| elementary flux mode | an extreme ray of the nonnegative part of the null space |
| degrees of freedom of the network | the nullity of S |
| balancing an equation | finding an integer null vector of the element-by-species matrix |

**Extensions.** [Flux balance analysis](https://en.wikipedia.org/wiki/Flux_balance_analysis) adds a linear objective and flux bounds, turning the null space into a linear program. [Chemical reaction network theory](https://en.wikipedia.org/wiki/Chemical_reaction_network_theory) (Feinberg) uses the *deficiency*, a rank-based integer, to predict whether multiple steady states are possible.

---

## 5. Leontief input–output: how much steel does a car actually take?

<details>
<summary><b>Start here — the problem in plain terms</b></summary>

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

</details>

**Field:** Economics (and, in its modern form, environmental footprint accounting)

**Tier:** 1 — posing and solving (I − A) x = d needs only a linear solve, with no differential equation. The [Perron–Frobenius](https://en.wikipedia.org/wiki/Perron%E2%80%93Frobenius_theorem) convergence condition is Tier 2; the dynamic [Leontief](https://en.wikipedia.org/wiki/Input%E2%80%93output_model) model, an ODE, is Tier 3.

**Scalars and vectors.** Scalar field: R (nonnegative). Vectors: outputs and demands in R^n, n = number of sectors.

**Underlying equations.** None: a static accounting identity for one period (the dynamic Leontief model adds an ODE).

**The problem.** Industries consume each other's output. Making a car needs steel; making steel needs electricity; making electricity needs steel. Given final consumer demand, find the total production every sector must run.

**Variables.**
| Symbol | Name | What it holds | Shape | Units |
|---|---|---|---|---|
| n | number of sectors | industries in the table | integer | — |
| Z | inter-industry flow matrix | z_ij is the value of sector i's output bought by sector j during the year | n × n | currency per year ($/yr) |
| x | gross output | total output of each sector during the year | n × 1 | $/yr |
| d | final demand | output delivered to final users: households, government, investment, exports | n × 1 | $/yr |
| A | technical-coefficient matrix | a_ij = z_ij / x_j, the input from sector i per dollar of sector j's output | n × n | dimensionless ($ per $) |
| I | identity matrix |  | n × n | — |
| L | Leontief inverse | L = (I − A)⁻¹; l_ij is the total output of sector i required per dollar of final demand for sector j, all rounds of the supply chain included | n × n | dimensionless |
| e | emission intensities (row vector) | direct emissions per dollar of each sector's output | 1 × n | kg CO₂e per $ |

Everything is measured in money at base-year prices, which is why a_ij is dimensionless. Physical tables in tonnes or joules exist, but then A carries mixed units and the coefficients are no longer comparable across rows.

**Formulation.** **Where the equations come from.** There is no differential equation here. The model is a static accounting identity over one period, usually a year: every sector's output goes either to other industries or to final users,

```
x_i = Σ_j z_ij + d_i
```

**The modelling assumption.** Leontief's assumption is that each industry uses inputs in fixed proportion to its output: z_ij = a_ij x_j. It is a fixed recipe, with no substitution between inputs and constant returns to scale. Substituting it into the identity:

```
x = A x + d      ⟹      (I − A) x = d      ⟹      x = L d
```

This models, for any given final demand, the gross output each industry must produce. The solution x is the level of production that exactly meets final demand plus all of the intermediate demand that meeting it induces.

**Footprints.** Multiplying by emission intensities gives total emissions, e L d, in kg CO₂e per year. The row vector e L gives emissions per dollar of final demand for each product, including every upstream supplier.

**Matrix structure.** Square, entrywise nonnegative, dense-ish, with column sums below 1 for a productive economy. National tables run 400–500 sectors; the global multi-region tables (EXIOBASE, WIOD) reach tens of thousands.

**What is computed.** `(I − A)⁻¹`, the Leontief inverse, is the object of interest itself — entry `(i,j)` is the total output of `i` required per unit of final demand for `j`, summed over all supply-chain depths. The [Neumann series](https://en.wikipedia.org/wiki/Neumann_series)

```
(I − A)⁻¹ = I + A + A² + A³ + …
```

has a direct reading: direct requirements, then requirements of requirements, and so on.

**Why linear algebra is the right tool.** The circularity that makes the accounting hard by hand — steel needs electricity needs steel — is precisely what a matrix inverse resolves in closed form.

**Pitfall worth teaching.** By Perron–Frobenius, the series converges exactly when the [spectral radius](https://en.wikipedia.org/wiki/Spectral_radius) of `A` is below 1. That is not a technical condition: it is the statement that the economy produces more than it consumes in production. A nonnegative matrix's dominant eigenvalue carries economic meaning.

**Terminology map.** How this field's vocabulary reads as linear algebra.

| Domain term | In linear algebra |
|---|---|
| technical coefficient matrix A | input from sector i per unit output of sector j |
| final demand | the right-hand side d |
| gross / total output | the unknown x |
| Leontief inverse | (I - A)^-1 |
| multiplier | a single entry of the Leontief inverse |
| productive economy | spectral radius of A below 1, so the Neumann series converges |
| direct vs indirect requirements | the successive terms A, A^2, A^3 of the Neumann series |
| embodied / Scope 3 emissions | an appended satellite row multiplied through the same inverse |

**Extensions.** [Environmentally-extended I/O](https://en.wikipedia.org/wiki/Environmentally_extended_input%E2%80%93output_analysis) appends rows for CO₂, water, and land use, and the same inverse yields the full upstream carbon footprint of a product — this is how most corporate [Scope 3](https://en.wikipedia.org/wiki/Carbon_accounting) emissions are estimated. Same mathematics: [Markov chain](https://en.wikipedia.org/wiki/Markov_chain) fundamental matrices, and structural path analysis.

**The differential-equation version.** The dynamic Leontief model adds investment in productive capacity: x = A x + B dx/dt + d, where B holds capital coefficients (capital stock from sector i needed per unit increase of output rate in sector j). That is a system of linear ODEs and is a Tier 3 extension; this entry uses only the static model.

---

## 6. PageRank: ranking by the structure of a network

<details>
<summary><b>Start here — the problem in plain terms</b></summary>

How do you rank web pages by importance when importance is circular? A page matters if important pages
link to it — but that definition refers to itself.

Picture someone clicking links at random forever. From whatever page they are on, they pick an outgoing
link at random and follow it. Occasionally, out of boredom, they jump to a completely random page
instead. Over a very long time, what fraction of their clicks land on each page?

That fraction is the ranking. Pages with many incoming links get visited often; pages linked from
frequently-visited pages get visited often too, which is exactly the circular definition, now made
precise as a statement about long-run behaviour.

The computation is remarkably simple: guess a distribution, push it through one round of clicking, and
repeat. It converges quickly, and the boredom-jump is not a detail — without it the process can get
permanently stuck in a corner of the web, and the whole thing falls apart.

</details>

**Field:** Computer science, network science

**Tier:** 2 — a dominant-eigenvector problem by construction.

**Scalars and vectors.** Scalar field: R. Vectors: R^n over pages, but the solution is constrained to the probability simplex (nonnegative, entries summing to 1), which is NOT a subspace.

**Underlying equations.** None; a linear [difference equation](https://en.wikipedia.org/wiki/Recurrence_relation) π_{t+1} = G π_t, i.e. a discrete-time Markov chain.

**The problem.** Order the pages of the web (or papers in a citation graph, or proteins in an interaction network) by importance, where importance is recursive: a page is important if important pages link to it.

**Variables.**
| Symbol | Name | What it holds | Shape | Units |
|---|---|---|---|---|
| n | number of pages |  | integer | — |
| outdeg(j) | out-degree | number of links on page j | integer | — |
| P | link (transition) matrix | p_ij = 1 / outdeg(j) if page j links to page i, else 0; column j says where a surfer on page j goes next | n × n | dimensionless (probabilities) |
| α | damping factor | probability that the surfer follows a link rather than jumping to a random page; conventionally 0.85 | scalar | dimensionless |
| 1 | all-ones vector |  | n × 1 | — |
| G | Google matrix | G = α P + ((1 − α)/n) 1 1ᵀ | n × n | dimensionless |
| t | step index | number of clicks so far | integer | — |
| π_t | distribution after t clicks | probability that the surfer is on each page after t clicks; entries are nonnegative and sum to 1 | n × 1 | dimensionless |
| r | PageRank vector | long-run fraction of time spent on each page | n × 1 | dimensionless; entries sum to 1 |

**Formulation.** **Where the equations come from.** There is no differential equation, but there is a dynamical system in discrete time: a random surfer who, at each step, follows a random link from the current page with probability α and otherwise jumps to a page chosen uniformly at random. The distribution over pages evolves by a linear difference equation:

```
π_{t+1} = G π_t
```

Row i reads: the probability of being on page i next equals the sum over pages j of (probability of being on j now) × (probability of moving from j to i).

**What a solution means.** The difference equation's solution is π_t = Gᵗ π_0. Because α < 1 every entry of G is positive, and the Perron–Frobenius theorem then guarantees that π_t converges to the same limit r for every starting distribution π_0. That limit is the stationary distribution:

```
G r = r,     r ≥ 0,     1ᵀ r = 1
```

r is the eigenvector of G with eigenvalue 1, scaled to sum to one. Using 1ᵀ r = 1, the same equation can be written without forming the dense matrix G:

```
r = α P r + ((1 − α)/n) 1
```

This models importance as long-run visit frequency: a page ranks highly if a surfer wandering indefinitely spends a large fraction of time there. P is stochastic only if every page has at least one outgoing link; pages without links (dangling nodes) must be patched first.

**Matrix structure.** `P` is sparse (average out-degree in the tens) and stochastic; `G` is dense but never formed — the damping term is a rank-one update applied on the fly, so each matrix–vector product still costs O(nnz).

**What is computed.** [Power iteration](https://en.wikipedia.org/wiki/Power_iteration). Convergence rate is governed by `|λ₂/λ₁| ≤ α`, so the damping factor directly sets the iteration count: roughly 50–100 iterations at α = 0.85 regardless of graph size.

**Why linear algebra is the right tool.** The circular definition of importance is a fixed-point equation, and Perron–Frobenius guarantees for an irreducible aperiodic nonnegative matrix that the fixed point exists, is unique, and is positive. The damping factor is what buys irreducibility — a modeling choice made to secure a theorem.

**Pitfall worth teaching.** Dangling nodes (no outlinks) break [stochasticity](https://en.wikipedia.org/wiki/Stochastic_matrix), and the standard patch — treating them as linking to everything — is a modeling decision with real effects on the ranking. Every "algorithm detail" here is a mathematical requirement in disguise.

**Terminology map.** How this field's vocabulary reads as linear algebra.

| Domain term | In linear algebra |
|---|---|
| link matrix | the column-stochastic matrix P built from the graph |
| dangling node | a zero column, which breaks stochasticity |
| damping factor (alpha) | the weight on P versus the uniform teleportation term |
| teleportation | the rank-one correction that makes the chain irreducible |
| stationary distribution | the dominant eigenvector, normalized |
| power iteration | repeated multiplication by the matrix |
| centrality | a score defined as an eigenvector, or a function, of the graph matrix |

**Extensions.** [Leslie matrices](https://en.wikipedia.org/wiki/Leslie_matrix) in population ecology (same dominant-eigenvector structure, eigenvalue = population growth rate); the [next-generation matrix](https://en.wikipedia.org/wiki/Next-generation_matrix) in epidemiology, whose spectral radius *is* [R₀](https://en.wikipedia.org/wiki/Basic_reproduction_number); [Katz centrality](https://en.wikipedia.org/wiki/Katz_centrality) and [hub/authority](https://en.wikipedia.org/wiki/HITS_algorithm) (HITS) scores; personalized [PageRank](https://en.wikipedia.org/wiki/PageRank) as a graph kernel in ML.

---

## 7. Error-correcting codes: linear algebra over a finite field

<details>
<summary><b>Start here — the problem in plain terms</b></summary>

You want to send a string of bits over a connection that occasionally flips one. Repeating everything
three times would work, but it triples what you send.

Here is a better idea. Alongside your data bits, send some extra bits, each one computed as the parity
(the even-or-odd count) of a chosen subset of the data bits. The receiver recomputes those parities from
what it received. If everything matches, no error. If some of them disagree, the exact *pattern* of
disagreement identifies which bit flipped — different bit positions participate in different subsets, so
each one produces its own distinctive signature of failures.

The design problem is choosing the subsets so that every possible single error produces a unique
signature. That is a question about independence: no two error patterns may look alike.

One thing to adjust up front. The arithmetic here is not ordinary addition — it is parity, where
1 + 1 = 0. Everything about subspaces and independence still works, but nothing about lengths or angles
does.

</details>

**Field:** Communications, information theory, storage systems

**Tier:** 1 — rank and null space over [GF(2)](https://en.wikipedia.org/wiki/GF%282%29), the smallest [finite field](https://en.wikipedia.org/wiki/Finite_field): just the numbers 0 and 1, added and multiplied modulo 2, so 1 + 1 = 0. Nothing from abstract algebra is needed beyond that. [Reed–Solomon](https://en.wikipedia.org/wiki/Reed%E2%80%93Solomon_error_correction) codes use the larger fields GF(2^m), which are Tier 3.

**Scalars and vectors.** Scalar field: GF(2), the numbers 0 and 1 with arithmetic modulo 2 (addition is XOR, multiplication is AND); Reed–Solomon codes use GF(2^m). Vectors: GF(2)^n; the code is a k-dimensional subspace of it. There is no Euclidean length here - [Hamming weight](https://en.wikipedia.org/wiki/Hamming_distance) is a metric, not a norm from an inner product.

**Underlying equations.** None: algebraic constraints over GF(2).

**The problem.** Send bits over a channel that flips some of them. Detect and correct the errors without retransmission.

**Variables.**
| Symbol | Name | What it holds | Shape | Units |
|---|---|---|---|---|
| k | message length | information bits per block | integer | — |
| n | block length | bits actually transmitted per block | integer | — |
| m | message | the k data bits to send | 1 × k row vector over GF(2) | bits |
| G | generator matrix | its rows are a basis of the code | k × n | bits |
| c | codeword | the n bits transmitted, c = m G | 1 × n | bits |
| H | parity-check matrix | each row is one parity check; its rows span the code's orthogonal complement | (n − k) × n | bits |
| e | error pattern | 1 in each position the channel flipped | 1 × n | bits |
| y | received word | y = c + e | 1 × n | bits |
| s | syndrome | which parity checks fail | (n − k) × 1 | bits |
| d | minimum distance | fewest positions in which two distinct codewords differ | integer | — |
| t | correctable errors | t = ⌊(d − 1)/2⌋ | integer | — |

There are no physical units: every entry is a bit, and all arithmetic is modulo 2, so 1 + 1 = 0 and subtraction is the same as addition. Coding theory conventionally writes messages and codewords as row vectors; that convention is used throughout this entry.

**Formulation.** **Where the equations come from.** There is no differential equation; the model is a set of linear constraints over the two-element field GF(2).

**Encoding.**

```
c = m G
```

This models the transmitted block as a combination of the rows of G, with the message bits choosing which rows to add. The dimensions are 1 × k times k × n, giving 1 × n. A common choice is systematic form, G = [I_k  B] with B a k × (n − k) matrix, so the first k bits of c are the message itself and the rest are check bits.

**Parity checks.** With H = [Bᵀ  I_{n−k}], every codeword satisfies

```
H cᵀ = 0
```

because G Hᵀ = B + B = 0 in GF(2). Each row of H is one parity check: the bits it selects must XOR to zero. The code is exactly the null space of H.

**Receiving and decoding.** If the channel flips the bits marked by e, the receiver gets y = c + e and computes

```
s = H yᵀ = H cᵀ + H eᵀ = H eᵀ
```

The [syndrome](https://en.wikipedia.org/wiki/Decoding_methods#Syndrome_decoding) depends only on the error pattern, not on the message. Decoding means finding the error pattern with the fewest 1s that satisfies H eᵀ = s, and then recovering c = y + e.

**Worked case: [Hamming(7,4)](https://en.wikipedia.org/wiki/Hamming%287,4%29).** Here k = 4, n = 7, d = 3, and t = 1. The seven columns of H are the seven nonzero 3-bit vectors. A single flipped bit in position i produces a syndrome equal to column i of H, so the syndrome directly names the position of the error.

**Matrix structure.** Entries in GF(2); [LDPC](https://en.wikipedia.org/wiki/Low-density_parity-check_code) codes use very sparse `H`; Reed–Solomon works over GF(2^m) with a [Vandermonde](https://en.wikipedia.org/wiki/Vandermonde_matrix)-structured generator.

**What is computed.** Syndrome decoding: look up or infer the minimum-weight `e` consistent with `s`. For LDPC codes, [belief propagation](https://en.wikipedia.org/wiki/Belief_propagation) on the bipartite graph of `H`. For Reed–Solomon, polynomial interpolation, which is a structured linear solve.

**Why linear algebra is the right tool.** Distance properties — the whole point of a code — become rank conditions. A code corrects `t` errors if and only if every `2t` columns of `H` are linearly independent. Searching an exponentially large space of codewords collapses to a statement about column ranks.

**Pitfall worth teaching.** This is where the abstraction of "field" earns its keep. Everything from linear algebra (rank, null space, dimension, bases) carries over unchanged; everything from geometry (angles, lengths, positive-definiteness, least squares) does not. A good exercise in what the axioms actually buy.

**Terminology map.** How this field's vocabulary reads as linear algebra.

| Domain term | In linear algebra |
|---|---|
| codeword | an element of the k-dimensional subspace of GF(2)^n |
| generator matrix G | a basis of the code, written as rows |
| parity-check matrix H | a basis of the code's orthogonal complement; codewords are its null space |
| syndrome | H y^T — depends only on the error, not the message |
| minimum distance | the smallest weight of a nonzero codeword |
| systematic form | G = [I \| P], so the message appears verbatim in the codeword |
| code rate | k/n, the subspace dimension over the ambient dimension |
| erasure vs error | known vs unknown error position — a column selection vs a search |

**Extensions.** Reed–Solomon in [QR codes](https://en.wikipedia.org/wiki/QR_code), CDs, and [RAID](https://en.wikipedia.org/wiki/Standard_RAID_levels)-6; LDPC in 5G and Wi-Fi 6; [polar codes](https://en.wikipedia.org/wiki/Polar_code_%28coding_theory%29) in 5G control channels. Separately, the same GF(2) linear algebra at massive scale — sparse nullspace via [block Lanczos](https://en.wikipedia.org/wiki/Block_Lanczos_algorithm) or [Wiedemann](https://en.wikipedia.org/wiki/Block_Wiedemann_algorithm) — is the final stage of the [number field sieve](https://en.wikipedia.org/wiki/General_number_field_sieve) used to factor RSA moduli.

---

## 8. Multiple-view geometry: 3D structure from 2D images

<details>
<summary><b>Start here — the problem in plain terms</b></summary>

Take two photos of the same building from different positions. A human can see they show the same
structure, and can roughly tell how the photographer moved between them. Getting a computer to do this
is the foundation of drone mapping, phone panoramas, and robot navigation.

Start with what is recoverable: matching points. Find a window corner visible in both photos. You do not
know where it is in 3D, and you do not know how the camera moved — but the two are linked. If you
hypothesise a camera motion, then a point in the first image is restricted to a single line in the
second. Each matched pair therefore constrains the possible motions, and with enough pairs only one
motion survives.

The awkward part is perspective: objects twice as far away appear half as large, which is division, not
a linear operation. The standard fix is to add one extra coordinate to every point and do the division
only at the very end. With that trick the entire camera pipeline becomes matrix multiplication, which is
why graphics hardware is built the way it is.

</details>

**Field:** Computer vision, [photogrammetry](https://en.wikipedia.org/wiki/Photogrammetry), robotics

**Tier:** 2 — the SVD does the work. The 2D [homography](https://en.wikipedia.org/wiki/Homography_%28computer_vision%29) and the transformation pipeline behind it sit at Tier 1; pose refinement on [SE(3)](https://en.wikipedia.org/wiki/Rigid_transformation) is Tier 3.

**Scalars and vectors.** Scalar field: R. Vectors: scene points in R^3, written in homogeneous R^4 up to scale ([projective space](https://en.wikipedia.org/wiki/Projective_space) P^3); image points in R^2 as homogeneous R^3 up to scale (P^2). The unknown [essential matrix](https://en.wikipedia.org/wiki/Essential_matrix) is vectorized to R^9 and recovered only up to scale, so it is really a point of P^8.

**Underlying equations.** None: projective geometry of the [pinhole camera](https://en.wikipedia.org/wiki/Pinhole_camera_model).

**The problem.** Given photographs of a scene from unknown viewpoints, recover both the camera positions and the 3D geometry. This is the engine behind phone [panorama stitching](https://en.wikipedia.org/wiki/Image_stitching), drone mapping, visual SLAM, and photogrammetric reconstruction.

**Variables.**
| Symbol | Name | What it holds | Shape | Units |
|---|---|---|---|---|
| X̃ | homogeneous world point | [X, Y, Z, 1]ᵀ: a scene point's position in world coordinates, with a 1 appended | 4 × 1 | m (last entry dimensionless) |
| R | rotation matrix | the camera's orientation relative to the world; orthogonal with determinant +1 | 3 × 3 | dimensionless |
| t | translation | the world origin expressed in camera coordinates | 3 × 1 | m |
| K | intrinsic (calibration) matrix | [[f_x, γ, c_x], [0, f_y, c_y], [0, 0, 1]]: converts camera-frame directions into pixels | 3 × 3 | pixels (last row dimensionless) |
| f_x, f_y | focal length | focal length measured in pixel widths and heights | scalars | pixels |
| c_x, c_y | principal point | the pixel where the optical axis meets the image | scalars | pixels |
| γ | skew | non-perpendicular pixel axes; essentially 0 for modern sensors | scalar | pixels |
| (u, v) | pixel coordinates | where the point appears in the image | scalars | pixels |
| x̃ | homogeneous image point | [u, v, 1]ᵀ | 3 × 1 | pixels (last entry dimensionless) |
| λ | projective depth | the point's depth along the camera's viewing axis (its Z coordinate in the camera frame) | scalar | m |
| x̂ | normalized image coordinates | x̂ = K⁻¹ x̃: the direction of the viewing ray, scaled so its last entry is 1 | 3 × 1 | dimensionless |
| [t]ₓ | cross-product matrix | the skew-symmetric matrix with [t]ₓ a = t × a for every a | 3 × 3 | m |
| E | essential matrix | E = [t]ₓ R: encodes the relative pose of two calibrated cameras | 3 × 3 | defined only up to scale |
| F | fundamental matrix | F = K′⁻ᵀ E K⁻¹: the same constraint written in pixel coordinates | 3 × 3 | defined only up to scale |
| N | number of correspondences | matched points visible in both images; at least 8 here | integer | — |
| A | constraint matrix | one row per correspondence, built from the products of their coordinates | N × 9 | dimensionless |
| e | vectorized E | the nine entries of E stacked into a column | 9 × 1 | dimensionless |

Primes mark the second view: x̂′ is the same scene point seen by the second camera, and K′ is that camera's [intrinsic](https://en.wikipedia.org/wiki/Camera_resectioning#Intrinsic_parameters) matrix.

**Formulation.** **Where the equations come from.** There is no differential equation; the model is the geometry of an ideal pinhole camera.

**Projection.**

```
λ x̃ = K [R | t] X̃
```

Read right to left. [R | t] X̃ rotates and translates the world point into camera coordinates (in metres). K converts those coordinates into pixels. The scalar λ is the depth, and dividing by it is the perspective effect that makes distant objects smaller. [Homogeneous coordinates](https://en.wikipedia.org/wiki/Homogeneous_coordinates) isolate that division in one scalar, so everything else is matrix multiplication. Units check: pixels × metres on the right, λ in metres on the left, leaving pixels.

**Two views.** Place the first camera at the world origin (R = I, t = 0) and the second at an unknown R, t. A scene point appears at x̂ in the first image and x̂′ in the second, both in normalized coordinates. The two viewing rays and the baseline t between the cameras lie in one plane, and that coplanarity is the [epipolar](https://en.wikipedia.org/wiki/Epipolar_geometry) constraint:

```
x̂′ᵀ E x̂ = 0,      E = [t]ₓ R
```

In pixel coordinates the same constraint reads x̃′ᵀ F x̃ = 0. Each correspondence gives one equation that is linear in the nine unknown entries of E, and stacking N of them gives

```
A e = 0
```

**What a solution means.** The equation is homogeneous, so if e solves it, so does any multiple of e. E, and therefore t, is recovered only up to scale: from images alone, a building and an accurate scale model of it are indistinguishable. The estimate is the unit vector that minimizes ‖A e‖, which is the right singular vector of A with the smallest singular value. Decomposing E then yields R and the direction of t; of the four candidate decompositions, the right one places the scene points in front of both cameras.

**Matrix structure.** `A` is small and dense (n × 9). The later bundle-adjustment stage produces a large, sparse, highly structured Jacobian with the characteristic "arrowhead" block pattern from cameras and points.

**What is computed.** SVD, twice and for two different reasons: once to solve the homogeneous least-squares problem (smallest singular vector), and once to project the estimate onto the manifold of valid essential matrices by zeroing the third singular value and equalizing the first two. [Bundle adjustment](https://en.wikipedia.org/wiki/Bundle_adjustment) then refines everything by sparse [Levenberg–Marquardt](https://en.wikipedia.org/wiki/Levenberg%E2%80%93Marquardt_algorithm) with the [Schur complement](https://en.wikipedia.org/wiki/Schur_complement) trick to eliminate the 3D points.

**Why linear algebra is the right tool.** Projective geometry in homogeneous coordinates is the reason: a genuinely nonlinear operation (perspective division) becomes a linear map followed by a normalization. Adding one coordinate buys linearity.

**Pitfall worth teaching.** Conditioning matters more than the algorithm here. Hartley's normalized [8-point](https://en.wikipedia.org/wiki/Eight-point_algorithm) algorithm — translate and scale the image points before forming `A` — is the difference between usable and useless results, and the only change is a preconditioning of the input. It is one of the cleanest real demonstrations that condition number is not an academic concern.

**Terminology map.** How this field's vocabulary reads as linear algebra.

| Domain term | In linear algebra |
|---|---|
| homogeneous coordinates | an added coordinate that turns perspective division into a linear map plus a normalization |
| intrinsic matrix K | the camera's internal calibration, an upper-triangular 3x3 |
| extrinsic parameters [R\|t] | the rigid transform from world to camera frame |
| essential / fundamental matrix | the rank-2 bilinear form satisfying x'^T E x = 0 |
| epipolar constraint | the bilinear equation relating corresponding points in two views |
| DLT (direct linear transform) | stacking constraints into A and taking the smallest right singular vector |
| reprojection error | the nonlinear least-squares objective minimized in refinement |
| bundle adjustment | sparse nonlinear least squares over all cameras and points at once |
| degenerate configuration | point placement that makes A rank-deficient, so the solution is not unique |

**Extensions.** Homography estimation and image stitching; the [PnP](https://en.wikipedia.org/wiki/Perspective-n-Point) problem; the Perron-like structure in rotation averaging; SE(3) and Lie-group optimization for pose graphs.

---

## 9. Empirical orthogonal functions: finding the dominant patterns in climate data

<details>
<summary><b>Start here — the problem in plain terms</b></summary>

Here is a century of monthly [sea-surface temperature](https://en.wikipedia.org/wiki/Sea_surface_temperature) maps: tens of thousands of grid points, over a
thousand time steps. Far too much to look at directly, and most of it is redundant — neighbouring points
in the ocean do not behave independently.

What a climatologist wants is the handful of recurring patterns that account for most of the variation.
[El Nino](https://en.wikipedia.org/wiki/El_Ni%C3%B1o%E2%80%93Southern_Oscillation) is one: a specific spatial signature of warm and cool regions that strengthens and weakens over
time. If you can identify a few such patterns, each with a single time series saying how strongly it is
present each month, you have compressed the whole dataset into something you can reason about.

That decomposition is what the SVD provides, and it comes with a guarantee: no other set of that many
patterns reconstructs the data more accurately.

The caveat is worth absorbing early. The method forces the patterns to be mutually perpendicular, and
nature is under no obligation to comply. A pattern that is optimal mathematically can still be a blend
of two unrelated physical processes.

</details>

**Field:** Atmospheric and ocean science, climatology

**Tier:** 2 — truncated SVD and the [Eckart–Young](https://en.wikipedia.org/wiki/Low-rank_approximation) optimality statement; no differential equation is used. Relating [EOFs](https://en.wikipedia.org/wiki/Empirical_orthogonal_functions) to the dynamics through a stochastic ODE is a Tier 3 extension.

**Scalars and vectors.** Scalar field: R. Vectors: each time slice is a spatial field in R^s (s grid points); EOFs live in R^s and [principal-component](https://en.wikipedia.org/wiki/Principal_component_analysis) series in R^t (t time steps).

**Underlying equations.** None used: a statistical decomposition of observed data (the ocean itself obeys PDEs that the method ignores).

**The problem.** A century of monthly sea-surface temperatures on a global grid is a matrix with 10⁴–10⁵ spatial points and 10³ time steps. Extract the few spatial patterns that account for most of the variability — the objects a climatologist can actually reason about, like El Niño.

**Variables.**
| Symbol | Name | What it holds | Shape | Units |
|---|---|---|---|---|
| s | number of grid points | spatial locations with data | integer | — |
| t | number of time steps | months in the record | integer | — |
| T_gk | sea-surface temperature | temperature at grid point g in month k | scalar | °C |
| X | anomaly matrix | x_gk = T_gk minus the long-term average for that calendar month at that grid point | s × t | K (a temperature difference, so K and °C agree) |
| W | area weights | diagonal matrix of √cos(latitude), so small high-latitude grid cells do not count as much as large tropical ones | s × s | dimensionless |
| U | EOFs | columns u_i are spatial patterns of unit length | s × ρ | dimensionless |
| Σ | singular values | diagonal σ_1 ≥ σ_2 ≥ … ≥ 0: the strength of each pattern | ρ × ρ | K |
| V | normalized time series | columns v_i of unit length | t × ρ | dimensionless |
| a_i | principal-component time series | a_i = σ_i v_i: how strongly pattern i is present each month | t × 1 | K |
| ρ | rank | number of nonzero singular values, at most min(s, t) | integer | — |
| q | modes retained | how many patterns are kept after truncation | integer | — |
| C | spatial covariance | C = X Xᵀ / (t − 1) | s × s | K² |

**Formulation.** **Where the equations come from.** No differential equation is used. The ocean and atmosphere obey partial differential equations of fluid flow and heat transport, but EOF analysis ignores them entirely: it is a statistical decomposition of observed data. That is its strength, since no model is needed, and its main limitation, since nothing forces the patterns it finds to be dynamical modes of the system.

**The decomposition.**

```
X = U Σ Vᵀ = Σ_i σ_i u_i v_iᵀ
```

This models the anomaly field as a sum of rank-one pieces, each a fixed spatial pattern u_i multiplied by a time series σ_i v_i. Read by columns: the map for month k is Σ_i u_i (σ_i v_ik), a weighted combination of the patterns with weights that change month by month.

**Truncation.** Keeping the first q terms gives the best possible rank-q approximation of X, and pattern i accounts for the fraction σ_i² / Σ_j σ_j² of the total variance. Equivalently, the u_i are the eigenvectors of the covariance matrix C, with eigenvalues σ_i² / (t − 1). That is why EOFs are called principal components.

**Area weighting.** On a latitude–longitude grid, cells shrink toward the poles. The SVD is therefore applied to W X, and the resulting patterns are divided by the weights before they are plotted.

**Matrix structure.** Tall or wide but dense; the effective rank is low — typically 5–10 modes capture most of the variance, which is why the technique works at all.

**What is computed.** Truncated SVD (randomized SVD or Lanczos bidiagonalization for large grids). The Eckart–Young theorem guarantees that the rank-k truncation is the best possible rank-k approximation in both the [Frobenius and spectral norms](https://en.wikipedia.org/wiki/Matrix_norm) — an optimality statement, not a heuristic.

**Why linear algebra is the right tool.** The field is spatially correlated: neighboring grid points are far from independent. Low-rank structure is a mathematical restatement of physical coherence, and the SVD finds it without being told any physics.

**Pitfall worth teaching.** EOFs are constrained to be orthogonal, and physical modes are generally not. A leading EOF can be a mathematical mixture of two distinct physical mechanisms, and a second EOF can be an artifact of orthogonality to the first (North's rule of thumb gives a degeneracy test). This is the best example in the collection of a decomposition whose mathematical optimality does not imply physical interpretability — worth teaching alongside the same caution for PCA in genomics.

**Terminology map.** How this field's vocabulary reads as linear algebra.

| Domain term | In linear algebra |
|---|---|
| EOF | a left singular vector — one spatial pattern |
| principal component time series | the corresponding right singular vector, scaled |
| explained variance | sigma_i^2 as a fraction of the total |
| loading | one entry of an EOF, i.e. one grid point's weight in that pattern |
| anomaly field | the mean-centered data matrix |
| rotated EOF (varimax) | a deliberately non-orthogonal re-basis of the leading subspace |
| North's rule of thumb | a test for whether two singular values are too close to separate the modes |

**Extensions.** [Proper orthogonal decomposition](https://en.wikipedia.org/wiki/Proper_orthogonal_decomposition) and reduced-order models in fluid dynamics; [dynamic mode decomposition](https://en.wikipedia.org/wiki/Dynamic_mode_decomposition), which extracts an approximate linear operator ([Koopman](https://en.wikipedia.org/wiki/Composition_operator)) rather than just a basis; the same SVD machinery in [latent semantic analysis](https://en.wikipedia.org/wiki/Latent_semantic_analysis), [recommender systems](https://en.wikipedia.org/wiki/Recommender_system), and [matrix completion](https://en.wikipedia.org/wiki/Matrix_completion).

**The link to dynamics, and why it is weak.** If the anomalies obeyed a linear stochastic ODE, dx/dt = B x + noise, the EOFs would be eigenvectors of the resulting covariance. Those coincide with the eigenvectors of B, the actual dynamical modes, only in special cases, such as when B is symmetric and the noise is equally strong in every direction. This is the precise sense in which an optimal pattern need not be a physical mode.

---

## 10. Quantum mechanics and quantum computing: when the vector space *is* the physics

<details>
<summary><b>Start here — the problem in plain terms</b></summary>

In quantum mechanics a system's state is not a position and a velocity — it is a list of complex
numbers, one for each configuration the system could be found in. Their sizes determine the
probabilities of each outcome. This is not an approximation or a modelling convenience; the theory is
stated this way.

Two consequences follow immediately. First, adding two valid states gives another valid state — this is
superposition, and it is just the statement that states form a vector space. Second, every measurable
quantity (energy, momentum, spin) corresponds to a matrix, and the values you can actually observe are
that matrix's eigenvalues. Asking "what energies can this molecule have?" is literally asking for the
eigenvalues of a particular matrix.

The difficulty is size. Combining two systems multiplies their dimensions rather than adding them, so
n quantum bits need a vector with 2^n entries — past about fifty, larger than any computer's memory.
Much of modern quantum chemistry and quantum computing is about exploiting the fact that the states
that actually occur in nature occupy a very thin slice of that enormous space.

</details>

**Field:** Physics, quantum chemistry, quantum information

**Tier:** 3 — the eigenproblem comes from [separating variables](https://en.wikipedia.org/wiki/Separation_of_variables) in the [Schrödinger equation](https://en.wikipedia.org/wiki/Schr%C3%B6dinger_equation), and its meaning is a statement about that ODE's solutions. On-ramp: [benzene](https://en.wikipedia.org/wiki/Benzene)'s 6×6 [Hückel](https://en.wikipedia.org/wiki/H%C3%BCckel_method) matrix can be diagonalized with no quantum background at all.

**Scalars and vectors.** Scalar field: C (real symmetric in the Huckel special case). Vectors: unit vectors in C^d; for n [qubits](https://en.wikipedia.org/wiki/Qubit) d = 2^n and the space is the [tensor product](https://en.wikipedia.org/wiki/Tensor_product) (C^2)^(x)n. Global phase is unphysical, so states are really points of [CP^(d-1)](https://en.wikipedia.org/wiki/Complex_projective_space). Observables are [Hermitian](https://en.wikipedia.org/wiki/Hermitian_matrix) matrices, which form a REAL vector space of dimension d^2.

**Underlying equations.** Linear Schrödinger equation iħ dψ/dt = H ψ; separation of variables gives the eigenproblem H φ = E φ.

**The problem.** Two versions. (a) Compute the energy levels and spectra of a molecule. (b) Simulate or design a quantum circuit.

**Variables.**
| Symbol | Name | What it holds | Shape | Units |
|---|---|---|---|---|
| ħ | reduced Planck constant | sets the time scale of quantum evolution | scalar | J·s |
| d | basis size | number of basis functions; for Hückel benzene, 6 (one carbon p orbital per atom) | integer | — |
| ψ(t) | state vector | complex coefficient of each basis function at time t; in an orthonormal basis, the squared magnitude of ψ_j is the probability of finding the system in basis state j | d × 1, complex | dimensionless; ‖ψ‖ = 1 |
| H | Hamiltonian matrix | h_ij is the energy coupling between basis states i and j; Hermitian | d × d | energy (eV or hartree) |
| E | energy eigenvalue | an allowed energy level | scalar | energy |
| φ | stationary state | eigenvector of H | d × 1 | dimensionless, normalized |
| U(t) | time-evolution operator | U(t) = exp(−iHt/ħ): maps the initial state to the state at time t; unitary | d × d | dimensionless |
| α | Coulomb integral | energy of an electron in an isolated carbon p orbital | scalar | eV (negative) |
| β | resonance integral | energy coupling between p orbitals on bonded neighbours | scalar | eV (negative) |
| Aᴳ | adjacency matrix | entry 1 if carbons i and j are bonded, else 0; for benzene, a 6-cycle | d × d | dimensionless |
| n | number of qubits |  | integer | — |

A dagger (†) denotes the conjugate transpose, so φ† ψ is the complex inner product.

**Formulation.** **Where the equations come from.** The dynamics are the time-dependent Schrödinger equation, a linear partial differential equation that is first order in time. Written in a finite basis it becomes a system of d linear ordinary differential equations with complex coefficients:

```
iħ dψ/dt = H ψ(t)
```

**[Stationary states](https://en.wikipedia.org/wiki/Stationary_state).** Look for solutions whose shape does not change, ψ(t) = φ e^{−iEt/ħ}. Substituting gives the time-independent Schrödinger equation:

```
H φ = E φ
```

That is what the eigenproblem means for the ODE. An eigenvector is a stationary state: only its complex phase rotates in time, so every measured probability is constant. Because the equation is linear and H is Hermitian (real eigenvalues, orthonormal eigenvectors), every solution is a superposition of stationary states:

```
ψ(t) = Σ_k (φ_k† ψ(0)) φ_k e^{−iE_k t/ħ}      equivalently     ψ(t) = U(t) ψ(0)
```

U(t) is [unitary](https://en.wikipedia.org/wiki/Unitary_matrix), which is why time evolution preserves ‖ψ‖ = 1, and why [quantum gates](https://en.wikipedia.org/wiki/Quantum_logic_gate) are unitary matrices.

**The case posed here: Hückel theory of benzene.** Use one carbon p orbital per atom (d = 6), assume the basis is orthonormal, and keep only nearest-neighbour couplings. The [Hamiltonian](https://en.wikipedia.org/wiki/Hamiltonian_%28quantum_mechanics%29) is then

```
H = α I + β Aᴳ
```

so its eigenvectors are exactly those of the ring's [adjacency matrix](https://en.wikipedia.org/wiki/Adjacency_matrix), and its energies are E = α + β μ_k, where μ_k are the adjacency eigenvalues. For a 6-cycle, μ_k = 2 cos(2πk/6), giving 2, 1, 1, −1, −1, −2. Since β < 0 the lowest level is α + 2β, then α + β twice, α − β twice, and α − 2β. Benzene's six π electrons fill the three lowest orbitals, two per orbital. Dropping the orthonormality assumption turns this into a generalized eigenproblem, H φ = E S φ, where S is the orbital overlap matrix.

**Many particles.** n qubits (or n two-level systems) live in the tensor product (ℂ²)^⊗n, of dimension d = 2ⁿ. Combining systems multiplies dimensions rather than adding them.

**Matrix structure.** Hermitian (hence real eigenvalues, orthogonal eigenvectors) and, in a local basis, sparse — Hamiltonians typically couple only nearby sites or orbitals. The dimension is the problem: it grows exponentially in system size.

**What is computed.** Lanczos and Davidson methods for the lowest few eigenpairs of matrices too large to store; [self-consistent field](https://en.wikipedia.org/wiki/Hartree%E2%80%93Fock_method) iteration (Hartree–Fock, [DFT](https://en.wikipedia.org/wiki/Density_functional_theory)) as a nonlinear eigenproblem solved by repeated dense diagonalization; quantum circuit simulation as a sequence of sparse structured matrix–vector products.

**Why linear algebra is the right tool.** It is not a modeling convenience here — the superposition principle *is* linearity, and the postulates of quantum mechanics are stated directly in terms of Hilbert spaces, Hermitian operators, and unitary evolution. This is the entry where the mathematics is not applied to the physics but constitutive of it.

**Pitfall worth teaching.** The tensor-product structure means the state space grows as 2ⁿ, which makes exact methods hopeless past ~50 qubits. The response is again low-rank structure: [matrix product states](https://en.wikipedia.org/wiki/Matrix_product_state) and tensor networks exploit the fact that physically relevant states occupy a very thin, low-entanglement slice of the full space. Low-rank approximation appears here for the same reason it appears in entry 9, in a completely different setting.

**Terminology map.** How this field's vocabulary reads as linear algebra.

| Domain term | In linear algebra |
|---|---|
| ket / state vector | a unit vector in a complex inner-product space |
| observable | a Hermitian operator; its eigenvalues are the measurable values |
| expectation value | the quadratic form psi^* A psi |
| eigenstate / energy level | eigenvector and eigenvalue of the Hamiltonian |
| Hamiltonian | the Hermitian matrix H in H psi = E psi |
| unitary gate | a norm-preserving complex linear map — the complex analogue of an orthogonal matrix |
| tensor product | the Kronecker product; why n qubits need dimension 2^n |
| entangled state | a vector that does not factor as a tensor product |
| basis set (quantum chemistry) | the chosen basis in which H is expressed |
| SCF iteration | fixed-point iteration on an eigenproblem whose matrix depends on its own solution |
| density matrix | a positive semidefinite matrix with trace 1 |

**Extensions.** Hückel molecular orbital theory, where the Hamiltonian is α I + β A for the molecular graph's adjacency matrix A, so the orbitals are exactly A's eigenvectors and the orbital energies are an affine function of its eigenvalues — the cleanest bridge between graph theory and chemistry. Also: [density matrices](https://en.wikipedia.org/wiki/Density_matrix) as positive semidefinite operators, [quantum channels](https://en.wikipedia.org/wiki/Quantum_channel) as completely positive maps, and [variational quantum eigensolvers](https://en.wikipedia.org/wiki/Variational_quantum_eigensolver).

---

# Coverage of the seed set

| # | Field | Core linear-algebra object | Dominant method |
|---|-------|---------------------------|-----------------|
| 1 | Civil / mechanical engineering | Sparse SPD system; generalized eigenproblem | Sparse Cholesky; Lanczos |
| 2 | Aerospace / control | Covariance projection; Riccati recursion | Recursive weighted least squares |
| 3 | Medical imaging | Ill-posed sparse system | Regularized iterative solve; Kaczmarz |
| 4 | Chemistry / systems biology | Null space (both sides); rank | Nullspace basis; rational arithmetic |
| 5 | Economics | Nonnegative matrix; spectral radius | Matrix inverse; Neumann series |
| 6 | Computer science / networks | Stochastic matrix; dominant eigenvector | Power iteration |
| 7 | Communications | Subspace over GF(2); rank conditions | Syndrome decoding; belief propagation |
| 8 | Computer vision | Homogeneous least squares; rank truncation | SVD; sparse Levenberg–Marquardt |
| 9 | Climate science | Low-rank approximation | Truncated / randomized SVD |
| 10 | Physics / quantum chemistry | Hermitian eigenproblem; tensor products | Lanczos, Davidson; SCF |

**Concepts deliberately covered across the set:** solving `Ax = b` (sparse, dense, ill-posed, over a finite field), least squares (batch and recursive), eigenvalue problems (standard, generalized, dominant-only), the SVD (as optimal approximation, as homogeneous solver, as manifold projection), null spaces and rank, nonnegative matrices and Perron–Frobenius, stochastic matrices, projections, conditioning and preconditioning, tensor products, and linear algebra over a field other than ℝ.

**Not yet represented:** graph Laplacians and spectral methods, Krylov subspace methods on their own terms, optimization duality and linear programming, tensor decompositions beyond the matrix case, randomized numerical linear algebra, and anything from pure mathematics.

---

# Backlog — candidates for expansion

Grouped by what they would add that the seed set does not have.

### Would add: Tier 1 coverage — 2D/3D graphics and scalars beyond the reals

This group exists because the seed set is thin at Tier 1 and silent on vector spaces whose scalars are
not real numbers. Every entry here is small-dimension and needs nothing past a first course, with
the one exception marked below.

*Graphics and small-dimension geometry (index 36–40)*
- **2D affine transforms in vector graphics** — the SVG/CSS/Canvas transform stack; composition order as a
  concrete demonstration that matrix multiplication does not commute
- **3D viewing and perspective projection** — the model-view-projection chain; why the fourth coordinate exists
- **3D rotations and rigid-body pose** — orthogonal matrices with determinant +1; gimbal lock as a
  basis-composition failure, which motivates quaternions without needing them
- **Barycentric coordinates and triangle rasterization** — a 3×3 solve per pixel; coordinates relative to a basis
- **Color spaces as change of basis** — sRGB ↔ XYZ ↔ LMS as 3×3 basis changes; gamut as a convex cone

*Polynomial and function spaces (index 41–45)*
- **Polynomial interpolation and change of basis** — Vandermonde systems; monomial vs Lagrange vs Chebyshev
  bases, and the conditioning consequences of the choice
- **Bézier curves and font rendering** — the Bernstein basis; every glyph on this page is an element of a
  4-dimensional polynomial space
- **Finite-difference stencils by undetermined coefficients** — derivative weights as the solution of a small
  linear system; differentiation as a linear operator
- **Fourier series as orthogonal projection** — an inner-product space of functions; best approximation
- **Least-squares fitting in a chosen function basis** — the design matrix as a basis choice made explicit

*Complex scalars (index 46–47)*
- **AC circuit analysis with complex impedance** — a 3×3 complex linear system; phasors make a differential
  equation into an algebraic one. *Tier 3, not Tier 1:* the phasor method is a technique for solving
  linear ODEs with sinusoidal forcing, so reading the entry requires the ODE. It stays in this group
  because it is the clearest example of complex scalars doing real work; the small DFT below is the
  Tier 1 complex-scalar entry.
- **The small DFT as a complex unitary matrix** — the 8-point transform written out; complex inner products

*Finite fields (index 48–50)*
- **Shamir secret sharing** — Lagrange interpolation over GF(p); the threshold property *is* a uniqueness
  theorem about interpolation
- **RAID-5 parity and XOR recovery** — one linear equation over GF(2), running in every storage array
- **CRC checksums** — polynomials over GF(2) modulo a generator

*Underdetermined systems with free variables (index 51–52)*
- **Traffic flow conservation at intersections** — particular plus homogeneous solution, with nonnegativity
  giving the physically admissible set
- **Mass balance in a process flowsheet** — recycle loops as coupling between equations

### Would add: graph Laplacians and spectral methods
- **Spectral clustering and image segmentation** — Fiedler vector, normalized cuts, Cheeger inequality
- **Resistor networks and Kirchhoff's laws** — the Laplacian as a physical object; effective resistance and commute times
- **Laplacian eigenmaps and diffusion maps** — nonlinear dimensionality reduction with a linear core
- **Consensus and opinion dynamics (DeGroot models)** — convergence rate set by the algebraic connectivity
  (Tier 2 in its discrete-time DeGroot form, a difference equation; the continuous-time version,
  dx/dt = −L x, is an ODE and would be Tier 3)

### Would add: large-scale iterative methods as the subject
- **Poisson/Navier–Stokes discretization** — finite differences or finite volumes, conjugate gradient, multigrid, preconditioner design
- **Circuit simulation (SPICE)** — modified nodal analysis, sparse LU with pivoting under structural constraints
- **Power-grid load flow and state estimation** — sparse Newton with a Jacobian that changes structure under contingency; Sherman–Morrison for N−1 analysis

### Would add: optimization and duality
- **Linear programming and the simplex method** — basis exchange as a sequence of rank-one updates; totally unimodular matrices giving integral solutions for free in network flow
- **Portfolio optimization (Markowitz)** — covariance matrices, shrinkage estimation, the ill-conditioning that makes the textbook version unusable
- **Support vector machines / kernel methods** — Gram matrices, positive definiteness, the representer theorem

### Would add: signal processing
- **The FFT as a matrix factorization** — the DFT matrix factored into sparse blocks; why O(n log n) is a statement about structure
- **Beamforming and MUSIC direction-finding** — signal and noise subspaces of a spatial covariance matrix; radar, sonar, and 5G MIMO
- **JPEG and video compression** — the DCT as a fixed orthogonal basis chosen for decorrelation

### Would add: statistics and machine learning proper
- **Least squares regression and the hat matrix** — QR vs normal equations, leverage, collinearity diagnostics
- **Matrix completion and recommender systems** — nuclear-norm minimization, the Netflix Prize
- **Word embeddings and latent semantic analysis** — factorization of a co-occurrence matrix
- **Attention in transformers** — QKᵀ as a learned bilinear form; low-rank adapters (LoRA) as explicit rank constraints on weight updates

### Would add: geosciences and geometry
- **Geodetic network adjustment** — the historical origin of least squares; rank deficiency from datum choice, resolved by constraints
- **Seismic tomography** — same inverse-problem structure as entry 3 with far worse ray coverage
- **Distance geometry (NMR structure determination)** — Cayley–Menger determinants, classical multidimensional scaling, low-rank Gram matrix recovery
- **X-ray crystallography** — the phase problem; Patterson maps; structure factors as Fourier coefficients

### Would add: discrete and algebraic applications
- **Markov decision processes** — policy evaluation as a linear solve, value iteration as a fixed point
- **Sports and citation ranking (Massey / Colley)** — a least-squares system built from pairwise comparisons
- **Cryptanalysis: sparse GF(2) nullspace in the number field sieve** — block Lanczos/Wiedemann at 10⁸ scale
- **Combinatorial design and coding bounds** — rank arguments proving combinatorial impossibility results

### Would add: molecular and biological (matched to your background)
- **Normal mode analysis and elastic network models** — the Hessian of a coarse-grained potential; low-frequency modes predicting functional motions
- **Flux balance analysis at genome scale** — the LP built on entry 4's null space
- **Population genetics PCA** — the same SVD as entry 9, with the same interpretability caveat and a well-documented history of overreading the modes
- **Phylogenetic invariants** — polynomial relations among expected site-pattern frequencies; linear algebra that shades into algebraic geometry

---

# Suggested next steps

1. **Add a runnable notebook per entry.** Each of these can be posed at a size that runs in seconds and still shows the real phenomenon — a 12-bar truss, a 32×32 tomographic phantom, a 10-sector I/O table, a Hamming(7,4) code. The pedagogical payload is usually in the failure mode (ill-conditioning, rank deficiency, slow convergence), which small examples show faithfully.
2. ~~Standardize a difficulty tier per entry.~~ **Decided:** the three-tier scheme above, recorded per
   entry in the `tier`, `tier_ceiling`, and `prereq_beyond_la` columns of the index. Remaining work is to
   promote Tier 1 entries into the seed set. Under the rule that any differential equation means Tier 3,
   only 2 of the 10 seed entries are Tier 1, which is the wrong first impression for a
   general audience. The Tier 1 backlog group above is the natural source.
3. ~~Decide whether the organizing axis is field or concept.~~ **Decided: field**, for the reasons in
   "Audience and organizing principle" above. The concept coverage table remains as the secondary
   cross-reference. Remaining work: extend the terminology map beyond the ten seed entries — it
   currently covers 84 terms across those ten only, and the backlog entries most likely to generate
   domain-specific questions (power systems, portfolio optimization, seismic tomography, MDPs) have no
   terminology coverage yet.
