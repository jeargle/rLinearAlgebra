# Applied Linear Algebra: An Initial Collection

**Version 0.2 — a seed set of 10 problems, and 12 further written entries**

Selection criteria for the seed set:

1. **One application domain each.** No two entries come from the same subfield or community of practice. At the coarse level used in the companion index, three entries fall under Engineering (civil/mechanical FEA, aerospace/control, communications) and two under Computer Science (network science, computer vision); these are distinct disciplines in practice, sharing only a top-level bucket. The set spans seven coarse fields and ten distinct subfields.
2. **One distinct linear-algebra concept each.** Entry 1 is a sparse SPD solve; entry 5 is a nonnegative-matrix spectral radius; entry 7 is linear algebra over a finite field, a number system with finitely many elements (defined under Difficulty tiers). If two problems reduce to the same mathematical object, only one is in the seed set and the other is in the backlog.
3. **Deployed, not illustrative.** Every entry is something an engineer, scientist, or company actually runs in production or in published research — not a textbook exercise dressed in application clothing.
4. **The matrix structure is the point.** In each case, *what kind of matrix it is* (sparse, symmetric, stochastic, rank-deficient, over GF(2), the numbers 0 and 1 with arithmetic modulo 2) determines which algorithm is viable. That is the through-line worth teaching.

Entries written after the seed set have status `written` in the index. They keep criteria 3 and 4
but not 1 and 2. Field is the organizing axis, so the same linear-algebra concept appears in the
vocabulary of several fields, and an entry for each field is the point; entries that share a concept
name each other under Extensions.

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
4. **Underlying equations** — one line naming the kind of equation the linear algebra comes from. A
   differential equation is named as one, with its kind: ordinary or partial, deterministic or
   stochastic, linear or not. Otherwise the line names what the model is (an accounting identity, a
   difference equation, algebraic laws, projective geometry, a statistical model, polynomial
   evaluation). Also an index column.
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

**Current distribution.** Of the 22 written entries, 14 are Tier 1,
3 are Tier 2, and 5 are Tier 3. Of the 10 seed entries, 2 are Tier 1
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
| load vector | the right-hand side f |
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

**Tier:** 1 — posing and solving (I − A) x = d needs only a linear solve. The [Perron–Frobenius](https://en.wikipedia.org/wiki/Perron%E2%80%93Frobenius_theorem) convergence condition is Tier 2; the dynamic [Leontief](https://en.wikipedia.org/wiki/Input%E2%80%93output_model) model, an ODE, is Tier 3.

**Scalars and vectors.** Scalar field: R (nonnegative). Vectors: outputs and demands in R^n, n = number of sectors.

**Underlying equations.** A static accounting identity for one period: each sector's output is used by other industries or by final users, x = A x + d.

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

**Formulation.** **Where the equations come from.** The model is a static accounting identity over one period, usually a year: every sector's output goes either to other industries or to final users,

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

**Underlying equations.** A linear [difference equation](https://en.wikipedia.org/wiki/Recurrence_relation) π_{t+1} = G π_t, i.e. a discrete-time Markov chain.

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

**Formulation.** **Where the equations come from.** The model is a dynamical system in discrete time: a random surfer who, at each step, follows a random link from the current page with probability α and otherwise jumps to a page chosen uniformly at random. The distribution over pages evolves by a linear difference equation:

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

**Underlying equations.** Linear algebraic constraints over GF(2), arithmetic modulo 2: every codeword c satisfies H cᵀ = 0.

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

**Formulation.** **Where the equations come from.** The model is a set of linear constraints over the two-element field GF(2).

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

**Underlying equations.** Projective geometry of the ideal [pinhole camera](https://en.wikipedia.org/wiki/Pinhole_camera_model).

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

**Formulation.** **Where the equations come from.** The model is the geometry of an ideal pinhole camera.

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

**Tier:** 2 — truncated SVD and the [Eckart–Young](https://en.wikipedia.org/wiki/Low-rank_approximation) optimality statement. Relating [EOFs](https://en.wikipedia.org/wiki/Empirical_orthogonal_functions) to the dynamics through a stochastic ODE is a Tier 3 extension.

**Scalars and vectors.** Scalar field: R. Vectors: each time slice is a spatial field in R^s (s grid points); EOFs live in R^s and [principal-component](https://en.wikipedia.org/wiki/Principal_component_analysis) series in R^t (t time steps).

**Underlying equations.** A statistical decomposition of observed data; no physical model of the ocean or atmosphere is used.

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

**Formulation.** **Where the equations come from.** EOF analysis is a statistical decomposition of observed data and uses no physical model of the ocean or atmosphere. That is its strength, since no model is needed, and its main limitation, since nothing forces the patterns it finds to be dynamical modes of the system.

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

## 12. Resistor networks: Kirchhoff's laws as a graph Laplacian

<details>
<summary><b>Start here — the problem in plain terms</b></summary>

A circuit board, a [strain gauge](https://en.wikipedia.org/wiki/Strain_gauge), or the metal wiring that carries power across a computer chip can be
pictured as wires meeting at junctions, with a resistor on each wire. Push current in at one junction
and take it out at another: how much current flows along each wire, and what is the voltage at every
junction?

Two rules decide it. First, current through a resistor is proportional to the voltage difference across
it. Second, at every junction, the current flowing in equals the current flowing out, because charge does
not pile up. Write the second rule once per junction and substitute the first, and you get one equation
per junction with the junction voltages as the unknowns.

One thing is odd about the answer. Raising every voltage by the same amount changes no current, because
only differences matter. So the equations cannot pin down the voltages until one junction is declared
to be zero, which is what electricians call [ground](https://en.wikipedia.org/wiki/Ground_%28electricity%29). In linear algebra terms, that missing piece of
information is a null space, and choosing a ground is how it is removed.

</details>

**Field:** Electrical engineering, circuit theory, chip power-grid analysis

**Tier:** 1 — a DC network of resistors is one symmetric linear system L φ = s, and grounding a node is removing a one-dimensional null space. [Effective resistance](https://en.wikipedia.org/wiki/Resistance_distance) through the [pseudoinverse](https://en.wikipedia.org/wiki/Moore%E2%80%93Penrose_inverse) and its link to random walks are Tier 2.

**Scalars and vectors.** Scalar field: R. Vectors: two different spaces: node potentials in R^n (n nodes) and edge currents in R^m (m resistors). The [incidence matrix](https://en.wikipedia.org/wiki/Incidence_matrix) maps the first to the second. Potentials are only defined up to adding the same constant to every node, so physically they live in R^n modulo the all-ones vector.

**Underlying equations.** Algebraic circuit laws: [Ohm's law](https://en.wikipedia.org/wiki/Ohm's_law) (V = IR) for each resistor and [Kirchhoff's](https://en.wikipedia.org/wiki/Kirchhoff's_circuit_laws) current law at each node.

**The problem.** Given a network of resistors and the currents injected at some nodes (or the voltages held fixed at
some nodes by sources), find the potential at every node and the current through every resistor. A
common special case is to find the single resistance the whole network presents between two terminals.

**Variables.**
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

**Formulation.** **Where the equations come from.** A direct-current network of
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
of the resistor joining i and j (0 if there is none). This is the weighted [Laplacian](https://en.wikipedia.org/wiki/Laplacian_matrix) of the network
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

**Worked case: a [Wheatstone bridge](https://en.wikipedia.org/wiki/Wheatstone_bridge).** Four nodes: the top a, two middle nodes b and c, and the bottom g.
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

**Matrix structure.** `L` is sparse, with one nonzero per node on the diagonal and two off-diagonal nonzeros per resistor. It
is symmetric positive semidefinite with zero row sums, and singular with rank n − (number of connected
components). After grounding it is symmetric positive definite and [diagonally dominant](https://en.wikipedia.org/wiki/Diagonally_dominant_matrix), the best-behaved
kind of large linear system there is.

**What is computed.** Ground a node (or eliminate every node held at a known voltage), then solve the remaining symmetric
positive definite system. Circuit-sized problems use a sparse Cholesky factorization. The power grids
that deliver current across a modern chip have tens of millions of nodes, and checking them for voltage
droop is done with preconditioned conjugate gradient or [multigrid](https://en.wikipedia.org/wiki/Multigrid_method). Graph theory has its own fast
Laplacian solvers, which run in nearly linear time in the number of edges.

**Why linear algebra is the right tool.** Each of the circuit-theory rules is a statement about the four fundamental subspaces of the incidence
matrix A. Kirchhoff's voltage law says that edge drops are in the column space of A. Kirchhoff's current
law constrains Aᵀ I. Ground is the null space of A, and the loops that [mesh analysis](https://en.wikipedia.org/wiki/Mesh_analysis) works with form a
basis of the null space of Aᵀ, whose dimension m − n + 1 counts the independent loops. The textbook
choice between [nodal analysis](https://en.wikipedia.org/wiki/Nodal_analysis) and mesh analysis is a choice of which of two complementary subspaces to
solve in: nodal analysis needs n − 1 unknowns, mesh analysis needs m − n + 1, and engineers pick
whichever is smaller. Reciprocity, the surprising fact that swapping where a source is applied and where
the response is measured gives the same reading, is just the symmetry of L.

**Pitfall worth teaching.** Two mistakes produce a singular or meaningless system. The first is forgetting to ground. L itself is
singular, so a direct solver either fails or, worse, returns potentials offset by an arbitrary constant
because of rounding. The second is inconsistent sources: injected currents that do not sum to zero put s
outside the column space, and no potentials satisfy the equations. Voltage sources need a third kind of
care. A node whose voltage is fixed is not an unknown, so its known potential moves to the right-hand
side, as in the bridge example. The current the source supplies is unknown, so that node's row of
L φ = s cannot be used as an equation; it gives the source current afterwards. Keeping that row with
s set to 0 is a common source of wrong answers. In each case the system was set up before deciding which
quantities are known, which are unknown, and what fixes the free constant.

**Terminology map.** How this field's vocabulary reads as linear algebra.

| Domain term | In linear algebra |
|---|---|
| node voltage (potential) | one entry of the vector φ in R^n |
| ground (reference node) | the node whose potential is fixed at 0, removing the null space spanned by the all-ones vector |
| nodal conductance (admittance) matrix | the weighted graph Laplacian L = A^T C A |
| Kirchhoff's current law (KCL) | A^T I = s, a statement about the left null space of A |
| Kirchhoff's voltage law (KVL) | voltage drops lie in the column space of A, so they sum to zero around every loop |
| loop (mesh) currents | coordinates in a basis of the cycle space, the null space of A^T, dimension m - n + 1 |
| nodal analysis vs mesh analysis | solving in potential space (dimension n - 1) vs in cycle space (dimension m - n + 1) |
| effective (Thevenin) resistance | (e_a - e_b)^T L^+ (e_a - e_b), a quadratic form in the pseudoinverse |
| superposition | linearity of the solution map s -> φ |
| reciprocity | symmetry of L, so the potential at b due to a source at a equals the potential at a due to the same source at b |
| bridge balance | a choice of resistances that puts one edge current at zero |

**Extensions.** Effective resistance between every pair of nodes can be read from the pseudoinverse L⁺, and it equals
the expected time for a random walk to go from one node to the other and back, divided by twice the
total conductance; both facts are Tier 2. The same Laplacian appears as the Y-bus matrix of power-grid
load flow, in modified nodal analysis inside circuit simulators such as [SPICE](https://en.wikipedia.org/wiki/SPICE), and in spectral graph
clustering, where its eigenvectors rather than its solves are the object of interest. Adding capacitors
and inductors turns the network equations into ODEs; with sinusoidal sources, phasors turn them back into
a complex linear system (the AC circuits entry, Tier 3). The same incidence-matrix structure, with flows
and conservation at nodes, appears in the traffic-flow and process mass-balance entries.

---

## 20. Least-squares regression: fitting a model is projecting onto a column space

<details>
<summary><b>Start here — the problem in plain terms</b></summary>

You have measured something at several settings — sales at several prices, a plant's height on
several days, a reaction's speed at several temperatures — and you want the straight line that best
describes the trend. The points never lie exactly on a line, so "best" needs a definition. The usual
one is to make the vertical misses as small as possible overall, by minimizing the sum of their
squares.

Here is the picture that makes the whole subject simple. List all the measured values as one long
list of numbers, one per data point. Every possible straight line, evaluated at the same settings,
gives another such list, and all of those lists together form a flat sheet through the origin of a
high-dimensional space. Your data sit somewhere off that sheet. The best-fitting line is the point
on the sheet directly beneath the data, found by dropping a perpendicular, exactly as the shortest
path from a point to a floor goes straight down.

Everything a statistician computes about a fit — the fitted values, the leftovers, how much each
data point influences its own fit — comes from that one perpendicular drop.

</details>

**Field:** Statistics, econometrics, data science, every experimental science

**Tier:** 1 — fitting, fitted values, residuals and [leverage](https://en.wikipedia.org/wiki/Leverage_%28statistics%29) all come from an orthogonal projection, with no eigenvalues needed. Conditioning and the SVD view of [collinearity](https://en.wikipedia.org/wiki/Multicollinearity) are Tier 2; confidence intervals and p-values need statistical inference beyond linear algebra.

**Scalars and vectors.** Scalar field: R. Vectors: two spaces: the observations y, fitted values and residuals live in R^n (one coordinate per data point), while the coefficients β live in R^k (one per predictor). The [design matrix](https://en.wikipedia.org/wiki/Design_matrix) maps R^k into R^n, and the fitted values fill out only a k-dimensional subspace of R^n, its column space.

**Underlying equations.** A statistical model, y = X β + noise, fitted by minimizing a sum of squares.

**The problem.** Given n observations of a response and k predictors, find the coefficients of the linear model that
minimize the sum of squared residuals, and describe the fit: fitted values, residuals, and how much
influence each observation has.

**Variables.**
| Symbol | Name | What it holds | Shape | Units |
|---|---|---|---|---|
| n | number of observations | data points | integer | — |
| k | number of coefficients | predictors, counting the intercept | integer | — |
| y | response vector | the measured values | n × 1 | units of the response |
| X | design matrix | column j holds predictor j at every observation; the first column is all 1s | n × k | each column in its predictor's units |
| β | coefficients | intercept and slopes | k × 1 | response units per predictor unit |
| β̂ | fitted coefficients | the least-squares solution | k × 1 | as β |
| ŷ | fitted values | ŷ = X β̂ | n × 1 | response units |
| r | residuals | r = y − ŷ | n × 1 | response units |
| H | hat matrix | H = X (XᵀX)⁻¹ Xᵀ, which maps y to ŷ | n × n | dimensionless |
| h_ii | leverage | diagonal entry i of H | scalar per observation | dimensionless |
| Q, R | QR factors | X = Q R with Q having orthonormal columns and R upper triangular | n × k and k × k | Q dimensionless; R in X's units |

**Formulation.** **Where the equations come from.** The model is a statistical
assumption: each response is a linear combination of the predictors plus random noise,

```
y = X β + noise
```

and the coefficients are chosen to minimize the sum of squared residuals ‖y − X β‖².

**The familiar case.** For a straight line, y ≈ b_0 + b_1 x, X has two columns, the 1s and the x
values, and β = (b_0, b_1). The answer from a first statistics course,

```
b_1 = Σ (x_i − x̄)(y_i − ȳ) / Σ (x_i − x̄)²,     b_0 = ȳ − b_1 x̄
```

is the general formula below worked out for two columns.

**The geometry.** As β ranges over ℝ^k, the vector X β ranges over the column space of X, a
k-dimensional subspace of ℝ^n. Minimizing ‖y − X β‖ asks for the point of that subspace closest to y.
The closest point is the orthogonal projection, characterized by a residual perpendicular to every
column of X:

```
Xᵀ (y − X β̂) = 0     ⟺     Xᵀ X β̂ = Xᵀ y
```

These are the normal equations, "normal" meaning perpendicular. When the columns of X are linearly
independent, XᵀX is invertible and

```
β̂ = (XᵀX)⁻¹ Xᵀ y,     ŷ = H y,     H = X (XᵀX)⁻¹ Xᵀ
```

H is called the [hat matrix](https://en.wikipedia.org/wiki/Projection_matrix) because it puts the hat on y, turning the data y into the fitted values ŷ.
It is a projection: H² = H (projecting twice changes nothing) and Hᵀ = H (the
projection is orthogonal). Its trace is k, the dimension of the subspace it projects onto, which is
why a fit with k coefficients uses up k [degrees of freedom](https://en.wikipedia.org/wiki/Degrees_of_freedom_%28statistics%29) and leaves n − k for the residuals.

**Worked case: a line through four points.** Take the points (0, 1), (1, 3), (2, 4), (3, 4). Then
x̄ = 1.5, ȳ = 3, Σ (x_i − x̄)(y_i − ȳ) = 5 and Σ (x_i − x̄)² = 5, so the slope is 1 and the intercept is
1.5. The fitted values are (1.5, 2.5, 3.5, 4.5) and the residuals (−0.5, 0.5, 0.5, −0.5). They add
up to zero, which is their orthogonality to the column of 1s, and (0, 1, 2, 3) · (−0.5, 0.5, 0.5, −0.5) = 0
is their orthogonality to the x column. The hat matrix is

```
H = [  0.7   0.4   0.1  −0.2 ]
    [  0.4   0.3   0.2   0.1 ]
    [  0.1   0.2   0.3   0.4 ]
    [ −0.2   0.1   0.4   0.7 ]
```

Its diagonal, the leverages (0.7, 0.3, 0.3, 0.7), adds up to k = 2. The two end points have more than
twice the leverage of the middle two, because a line pivots about its centre.

**Matrix structure.** `X` is tall and thin. It is dense for ordinary regression and sparse when most predictors are
indicator variables (categories, fixed effects). `XᵀX` is k × k, symmetric and positive semidefinite,
and positive definite exactly when the columns of X are independent. `H` is n × n, symmetric,
idempotent and of rank k. It is never formed for large n; its diagonal can be read from the rows of Q.

**What is computed.** The careful method factors X = Q R with [Householder](https://en.wikipedia.org/wiki/Householder_transformation) reflections and solves R β̂ = Qᵀ y by back
substitution; R's `lm` does this. Other packages use the SVD, or a Cholesky factorization of XᵀX,
which is fast but inherits the pitfall below. With [QR](https://en.wikipedia.org/wiki/QR_decomposition),
ŷ = Q Qᵀ y and h_ii = ‖row i of Q‖². Forming XᵀX and solving the normal equations is faster but loses
accuracy when the columns are nearly dependent, as the pitfall shows. Very large sparse problems use
iterative solvers such as LSQR.

**Why linear algebra is the right tool.** The geometry answers questions that formulas alone obscure. Residuals sum to zero because the column
of 1s is in the subspace. Adding a predictor can never increase the residual sum of squares, because
it enlarges the subspace. A predictor that is a combination of others adds nothing, because it leaves
the subspace unchanged, and it makes β not unique, because X then has a null space. Leverage is a
property of X alone, so an influential design point can be spotted before any response is measured.
Even [R²](https://en.wikipedia.org/wiki/Coefficient_of_determination) is a squared cosine: that of the angle between the centered data vector and the centered
fitted vector.

**Pitfall worth teaching.** Solving the normal equations squares the difficulty of the problem. A measure of how close the columns
of X are to dependent is its condition number, the factor by which relative errors in the data can be
magnified in the answer. XᵀX has the square of X's condition number. Regress the worked example's y on
the calendar years 2001–2004 instead of 0–3, and the column of years is almost parallel to the column
of 1s. The condition number of X becomes about 3.6 million and that of XᵀX about 1.3 × 10¹³, close to
the limit of double-precision arithmetic, so the normal equations lose about 13 of the 16 significant
digits available. QR works with X directly, and for a fit with small residuals its accuracy depends
on the condition number of X rather than its square. Centering the predictor (using
years since 2000, or deviations from the mean) removes the problem, which is the linear-algebra reason
for statisticians' standard advice to center. The exactly dependent version is the [dummy variable](https://en.wikipedia.org/wiki/Dummy_variable_%28statistics%29) trap:
one indicator column per category plus an intercept makes X rank-deficient, and β̂ is not unique.

**Terminology map.** How this field's vocabulary reads as linear algebra.

| Domain term | In linear algebra |
|---|---|
| design matrix (model matrix) X | the n × k matrix whose columns are the predictors, including a column of 1s for the intercept |
| regression coefficients β | coordinates of the fitted vector in the basis given by the columns of X |
| fitted values ŷ | the orthogonal projection of y onto the column space of X |
| residuals | the component of y in the orthogonal complement of the column space |
| hat matrix H | the projection matrix X (XᵀX)⁻¹ Xᵀ, so ŷ = H y |
| leverage h_ii | the i-th diagonal entry of H; how strongly observation i pulls its own fitted value |
| degrees of freedom | dimensions; k for the model (the trace of H) and n − k for the residuals |
| normal equations | Xᵀ X β = Xᵀ y, the statement that the residual is orthogonal to every column of X |
| multicollinearity | columns of X that are nearly linearly dependent, so β is poorly determined |
| dummy variable trap | an exactly dependent set of indicator columns, which makes X rank-deficient |
| R² | the squared length of the centered fitted vector over that of the centered data vector |

**Extensions.** Weighted and generalized least squares change the inner product, so the projection is orthogonal in a
different geometry. [Ridge regression](https://en.wikipedia.org/wiki/Ridge_regression) adds a multiple of the identity to XᵀX. The SVD of X shows which
combinations of predictors are poorly determined and is the natural language for collinearity (Tier 2).
The same projection is used in other fields' vocabularies in the basis-fitting entry (fitting curves
with chosen basis functions), the Massey and Colley ranking entry (least squares on pairwise game
results), and the geodetic network adjustment entry, where least squares was invented. Recursive
least squares, which updates β̂ as data arrive, leads to the Kalman filter.

---

## 24. Geodetic network adjustment: least squares where it was invented, and the datum it cannot see

<details>
<summary><b>Start here — the problem in plain terms</b></summary>

Surveyors build maps and height systems by measuring between points: how much higher one marker is than
another, how far apart two hilltops are, which direction one lies from the other. They always take more
measurements than strictly needed, because every measurement has small errors and the extras reveal
them. Walk a loop measuring height differences and add them up, and you should return to zero, but you
never quite do.

Making all the measurements agree, by spreading those discrepancies as fairly as possible, is called
adjusting the network. It is where the method of least squares was invented, around 1800, by [Legendre](https://en.wikipedia.org/wiki/Adrien-Marie_Legendre)
and [Gauss](https://en.wikipedia.org/wiki/Carl_Friedrich_Gauss), and national mapping agencies still do exactly this, with millions of measurements.

There is a subtlety at the heart of it. Every measurement compares two points, so the measurements
together say nothing about where the whole network sits. Raise every height by a metre and every
measured difference stays the same. Some outside choice, called the [datum](https://en.wikipedia.org/wiki/Geodetic_datum), has to anchor the network,
such as declaring one marker to be at a known height above sea level. In linear algebra terms, the
equations have a null space, and the datum is how it is removed.

</details>

**Field:** [Geodesy](https://en.wikipedia.org/wiki/Geodesy), land surveying, mapping, GNSS reference frames

**Tier:** 1 — an adjustment is a least-squares fit whose design matrix is rank-deficient by construction, and choosing a datum is choosing how to remove the null space. Precision and reliability analysis through the covariance of the estimates, and its eigenvalues, are Tier 2.

**Scalars and vectors.** Scalar field: R. Vectors: two spaces, as in any least-squares problem: the unknown station coordinates in R^u (u = number of stations for heights, 2 or 3 times that for horizontal or 3D positions) and the observations in R^m. Measurements are differences, so the design matrix has a null space, the datum defect; only coordinate differences are determined.

**Underlying equations.** Observation equations: each measured height difference, distance or direction is a function of station coordinates, plus a measurement error; for [levelling](https://en.wikipedia.org/wiki/Levelling) they are linear, h_j − h_i = measured difference.

**The problem.** Given redundant measurements between stations of a survey network, estimate the station coordinates
that best fit all the measurements, quantify the discrepancies, and fix the network's position (its
datum) so that the coordinates are unique, while recognising which results depend on that choice and
which do not.

**Variables.**
| Symbol | Name | What it holds | Shape | Units |
|---|---|---|---|---|
| u | number of unknowns | station heights (levelling) or coordinates | integer | — |
| m | number of observations | measured height differences, distances, directions | integer | — |
| h | station heights | the unknowns of a levelling network | u × 1 | metres |
| ℓ | observations | the measured height differences | m × 1 | metres |
| A | design matrix | row k has −1 for the station a measurement starts from and +1 for the station it ends at | m × u | dimensionless |
| v | residuals (corrections) | v = A h − ℓ, what each observation must change by to fit the adjusted heights | m × 1 | metres |
| W | weight matrix | diagonal, with the inverse variance of each observation | m × m | 1/metres² |
| d | datum defect | dimension of the null space of A | integer | — |

**Formulation.** **Where the equations come from.** The model is a set of observation equations: each measurement is a
known function of the station coordinates plus a small random error.

**One observation.** A levelling run from [benchmark](https://en.wikipedia.org/wiki/Benchmark_%28surveying%29) i to benchmark j measures the height difference
between them. The familiar surveying relation is

```
h_j − h_i = ℓ_k + v_k
```

the true height difference equals the measured value plus the correction it needs. Only two unknowns
appear, with coefficients −1 and +1.

**All observations at once.** Stacking one such row per measurement gives

```
A h = ℓ + v
```

with one row of A per observation and one column per station. With more observations than needed, the
measured ℓ is not in the column space of A, so no heights satisfy every equation exactly. The
adjustment chooses h to minimize the weighted sum of squared corrections, vᵀ W v, which leads to the
normal equations

```
Aᵀ W A h = Aᵀ W ℓ
```

the same equations as in the regression entry, with the weights recording that some measurements are
more reliable than others.

**The datum defect.** Every row of A has one +1 and one −1, so A 1 = 0: adding the same constant to
every height leaves every residual unchanged. The null space of A is spanned by the all-ones vector,
the datum defect is d = 1, and Aᵀ W A is singular. The normal equations have infinitely many solutions,
all differing by a constant. A datum is the extra information that picks one: hold a benchmark at a
known height (a minimal constraint), or choose the solution of minimum length (a free network).

**Worked case: a levelling loop.** Three benchmarks P, Q, R. Benchmark P is held at h_P = 100.000 m, and
three equally weighted runs give

```
h_Q − h_P = 2.0 m,     h_R − h_Q = 1.0 m,     h_R − h_P = 3.1 m
```

Around the loop the first two should add up to the third, but 2.0 + 1.0 = 3.0, a misclosure of 0.1 m.
With h_P fixed, two unknowns remain and three equations, and the least-squares solution is

```
h_Q = 102.033 m,     h_R = 103.067 m,     v = (+0.033, +0.033, −0.033) m
```

The misclosure is shared equally among the three equally reliable runs. Holding R at 103.000 m instead
gives h_P = 99.933 m and h_Q = 101.967 m: different heights, but exactly the same height differences and
the same corrections. The free-network (minimum-norm) solution near (100, 102, 103) gives
(99.967, 102.000, 103.033), again with the same differences.

**Matrix structure.** `A` is sparse: a levelling observation has two nonzeros, a horizontal distance or direction four to six.
For levelling it is the incidence matrix of the network graph, the same matrix as in the resistor and
traffic entries, and Aᵀ W A is a weighted graph Laplacian. Its null space, the datum defect, has
dimension 1 for heights, 3 for a 2D network of distances (two shifts and a rotation), 4 for a 2D network
of angles only (add scale), and up to 7 in 3D (three shifts, three rotations and a scale).

**What is computed.** [Weighted least squares](https://en.wikipedia.org/wiki/Weighted_least_squares) with datum constraints. Large adjustments form Aᵀ W A, which is sparse, and solve
it with sparse Cholesky after removing the datum, or use QR on A. National datums were built this way;
the North American height datum [NAVD 88](https://en.wikipedia.org/wiki/North_American_Vertical_Datum_of_1988) is a continent-wide levelling adjustment held at a single tide
gauge benchmark in Quebec. Modern GNSS reference frames such as the [International Terrestrial Reference](https://en.wikipedia.org/wiki/International_Terrestrial_Reference_System_and_Frame)
Frame are adjustments of millions of satellite observations with the same rank-deficient structure.

**Why linear algebra is the right tool.** The surveyor's notions are subspace notions. Redundancy means more rows than the rank, misclosure means
the observations are not in the column space, and the adjustment is an orthogonal projection onto it
(weighted by W). The datum defect is the null space, its size depends on what was measured (heights,
distances, angles), and choosing a datum is choosing a complement to it. Quantities that do not depend
on the datum, such as height differences and distances, are the estimable ones: those whose value is
the same for every solution of the normal equations.

**Pitfall worth teaching.** Coordinates from different datums cannot be compared, even though each set is correct. In the worked
case, fixing P or fixing R gives heights that differ by 0.067 m at every benchmark, with identical
differences. Deformation and subsidence monitoring compares a network's coordinates between surveys
years apart, and if the two adjustments used different datum points, or a datum point that itself moved,
the comparison shows apparent motion everywhere that is entirely an artefact of the datum. The test is
the one linear algebra suggests: compare only datum-independent quantities, or transform both solutions
to the same datum first. A second consequence is that a solver handed the unconstrained normal equations
either fails, because Aᵀ W A is singular, or returns one particular solution chosen silently by its
pivoting, so the datum has to be chosen explicitly.

**Terminology map.** How this field's vocabulary reads as linear algebra.

| Domain term | In linear algebra |
|---|---|
| benchmark (station, control point) | a surveyed point; its coordinates are unknowns |
| observation equation | one row of the system, an observation written in terms of the unknowns |
| levelling (spirit levelling) | measuring height differences between benchmarks |
| misclosure | the amount by which observations around a loop fail to add up to zero |
| adjustment | least-squares estimation of the coordinates from redundant, inconsistent observations |
| residual (correction) v | the change to each observation that makes the set consistent |
| datum | the choice that fixes the null space, such as a benchmark held at a known height |
| datum defect | the dimension of the null space of the design matrix |
| minimally constrained vs overconstrained adjustment | removing exactly the null space vs also forcing the network to fit fixed points |
| free network | a minimum-norm solution, with no point held fixed |
| estimable quantity | a function of the coordinates that does not depend on the datum, such as a height difference |
| weight | the inverse of an observation's variance; longer levelling lines get smaller weights |

**Extensions.** Horizontal and 3D networks have nonlinear observation equations (distances and angles), solved by
linearizing about approximate coordinates and adjusting repeatedly, each step a rank-deficient linear
least-squares problem like this one. The covariance matrix (Aᵀ W A)⁻¹, computed in a chosen datum,
describes precision, and its eigenvectors give error ellipses (Tier 2). The regression entry is the same
projection in statistical vocabulary; the Massey and Colley ranking entry has exactly this
incidence-matrix structure and the same one-dimensional null space, because game results, like height
differences, only compare pairs; and GNSS positioning is the trilateration on-ramp of the Kalman
filtering entry.

---

## 36. 2D transforms in SVG, CSS and Canvas: why translation needs a third coordinate

<details>
<summary><b>Start here — the problem in plain terms</b></summary>

Every web page, drawing program and vector illustration moves shapes around: it shifts them, turns them,
stretches them and slants them. Web designers write these moves as short instructions, such as
"translate this by 50 pixels, then rotate it by 30 degrees", and the browser applies them to every point
of the shape.

Two facts surprise people. The first is that order matters: turning a shape and then sliding it puts
it somewhere different from sliding it and then turning it. The second is that the code which
represents these moves uses tables of nine numbers, three by three, even though the screen is only two
dimensional.

Both have the same explanation. Turning and stretching are the kind of operation a matrix performs, and
doing one after another is multiplying matrices, which depends on the order. Sliding is different: it
moves the origin, and a matrix acting on two coordinates can never do that. The fix is to give every
point a third coordinate that is always 1. With it, a slide becomes a matrix too, and every combination
of moves, however long, collapses into a single three-by-three matrix.

</details>

**Field:** Computer graphics, web front-end development, vector illustration, user interfaces

**Tier:** 1 — every transform is a 3 × 3 matrix acting on homogeneous coordinates, and a transform stack is a matrix product. Splitting a general transform back into rotation, scale and [shear](https://en.wikipedia.org/wiki/Shear_mapping) uses the SVD or the [polar decomposition](https://en.wikipedia.org/wiki/Polar_decomposition), which are Tier 2.

**Scalars and vectors.** Scalar field: R. Vectors: points of the plane R^2, represented in homogeneous coordinates as vectors (x, y, 1) in R^3. The points themselves form the plane z = 1 inside R^3, which is not a subspace (it misses the origin); the [affine](https://en.wikipedia.org/wiki/Affine_transformation) maps of the plane are the 3 × 3 matrices with bottom row (0, 0, 1), which map that plane to itself.

**Underlying equations.** Matrix products acting on homogeneous coordinates: p′ = M p.

**The problem.** Represent the moves of 2D graphics (translation, rotation, scaling, shear, and any sequence of them) so
that a whole sequence can be combined into one transform, applied quickly to every point of a drawing,
inverted (to find which point of a shape lies under the mouse pointer), and written in the notations
that [SVG](https://en.wikipedia.org/wiki/SVG), [CSS](https://en.wikipedia.org/wiki/CSS) and the HTML [Canvas](https://en.wikipedia.org/wiki/Canvas_element) use.

**Variables.**
| Symbol | Name | What it holds | Shape | Units |
|---|---|---|---|---|
| (x, y) | point | a point of the drawing | 2 numbers | pixels or user units |
| p | homogeneous point | (x, y, 1) | 3 × 1 | pixels in the first two entries |
| L | linear part | rotation, scaling and shear together | 2 × 2 | dimensionless |
| t | translation | the shift (e, f) | 2 × 1 | pixels |
| M | affine transform | the 3 × 3 matrix with L in its top-left 2 × 2 block, t in its last column, and bottom row (0, 0, 1) | 3 × 3 | mixed: L dimensionless, t in pixels |
| T(e, f) | translation matrix | moves every point by (e, f) | 3 × 3 | — |
| R(θ) | rotation matrix | turns every point by θ about the origin | 3 × 3 | — |
| S(s_x, s_y) | scaling matrix | stretches by s_x horizontally and s_y vertically | 3 × 3 | — |
| θ | angle | rotation angle; positive turns the x-axis toward the y-axis | scalar | degrees or radians |
| c | centre | a point about which to rotate or scale | 2 × 1 | pixels |

Screen coordinates usually point y downwards, so a positive θ in SVG and CSS turns shapes clockwise on
the screen, even though the matrix is the same as the textbook rotation.

**Formulation.** **Where the equations come from.** The model is a choice of coordinates: points carry an extra
coordinate fixed at 1 so that every move of the plane becomes a matrix product.

**Linear moves.** Rotation, scaling and shear fix the origin and act on (x, y) through a 2 × 2 matrix.
The familiar rotation formula,

```
x′ = x cos θ − y sin θ
y′ = x sin θ + y cos θ
```

is the matrix-vector product

```
[ x′ ]   [ cos θ  −sin θ ] [ x ]
[ y′ ] = [ sin θ   cos θ ] [ y ]
```

and this 2 × 2 matrix is the linear part L of a rotation.

**Translation is not linear.** The shift x′ = x + e, y′ = y + f moves the origin to (e, f), and every
linear map sends the origin to itself, so no 2 × 2 matrix can do it. A general move of the plane is an
affine map, a linear part followed by a shift: (x′, y′) = L (x, y) + t.

**Homogeneous coordinates.** Represent (x, y) by p = (x, y, 1). Then the affine map is one matrix
product in ℝ³:

```
[ x′ ]   [ a  c  e ] [ x ]                  [ a  c ]              [ e ]
[ y′ ] = [ b  d  f ] [ y ]       with   L = [ b  d ]   and   t = [ f ]
[ 1  ]   [ 0  0  1 ] [ 1 ]
```

The 1 in the last coordinate picks up the translation column, and the bottom row keeps it equal to 1.
This 3 × 3 matrix is exactly what SVG and CSS write as matrix(a, b, c, d, e, f): the six numbers are
the first two rows, read column by column.

**A transform stack is a product.** SVG's transform="translate(2, 0) rotate(90)", CSS's
transform: translate(2px, 0) rotate(90deg), and the Canvas calls ctx.translate(2, 0); ctx.rotate(…)
all mean the matrix

```
M = T(2, 0) R(90°)
```

applied to each point as M p = T(2, 0) (R(90°) p). The rightmost transform acts on the point first.

**Worked case: one point, two orders.** The two elementary matrices are

```
            [ 1  0  2 ]                [ 0  −1  0 ]
T(2, 0)  =  [ 0  1  0 ]     R(90°)  =  [ 1   0  0 ]
            [ 0  0  1 ]                [ 0   0  1 ]
```

and their products in the two orders are

```
                    [ 0  −1  2 ]                        [ 0  −1  0 ]
T(2, 0) R(90°)  =   [ 1   0  0 ]     R(90°) T(2, 0)  =  [ 1   0  2 ]
                    [ 0   0  1 ]                        [ 0   0  1 ]
```

Applied to the point (1, 0), written as (1, 0, 1):

```
[ 0  −1  2 ] [ 1 ]   [ 2 ]          [ 0  −1  0 ] [ 1 ]   [ 0 ]
[ 1   0  0 ] [ 0 ] = [ 1 ]          [ 1   0  2 ] [ 0 ] = [ 3 ]
[ 0   0  1 ] [ 1 ]   [ 1 ]          [ 0   0  1 ] [ 1 ]   [ 1 ]

translate(2, 0) rotate(90):         rotate(90) translate(2, 0):
rotate to (0, 1), shift to (2, 1)   shift to (3, 0), rotate to (0, 3)
```

Matrix multiplication does not commute, and the two programs draw in different places.

**Rotating about a point.** rotate(θ, c_x, c_y) in SVG, or a CSS transform-origin, turns a shape about
the point c rather than about the origin. It is three moves: shift c to the origin, rotate, shift back,

```
T(c) R(θ) T(−c)
```

For θ = 90° about c = (1, 1):

```
[ 1  0  1 ] [ 0  −1  0 ] [ 1  0  −1 ]   [ 0  −1  2 ]
[ 0  1  1 ] [ 1   0  0 ] [ 0  1  −1 ] = [ 1   0  0 ]
[ 0  0  1 ] [ 0   0  1 ] [ 0  0   1 ]   [ 0   0  1 ]
   T(c)        R(90°)       T(−c)
```

and the result sends (2, 1) to (1, 2):

```
[ 0  −1  2 ] [ 2 ]   [ 1 ]
[ 1   0  0 ] [ 1 ] = [ 2 ]
[ 0   0  1 ] [ 1 ]   [ 1 ]
```

a quarter turn about (1, 1). That matrix happens to equal T(2, 0) R(90°) from the worked case: a rotation
about one point is the same move as a rotation about the origin followed by some translation.

**Undoing a transform.** The inverse of a product reverses the order: (T R)⁻¹ = R⁻¹ T⁻¹, so to undo
"rotate, then translate" you untranslate first and then unrotate. For an affine matrix the inverse is

```
[ L   t ]⁻¹     [ L⁻¹   −L⁻¹ t ]
[ 0   1 ]    =  [  0       1   ]
```

written in blocks (the 0 is the row (0, 0)), which exists whenever L is invertible.

**Matrix structure.** Dense 3 × 3 with bottom row (0, 0, 1), so six numbers determine it. Products and inverses of such
matrices have the same bottom row: affine maps are closed under composition and inversion. Rotations
have an orthogonal L, uniform scalings a multiple of the identity, and shears a triangular L.

**What is computed.** A renderer multiplies the transforms along the path from the page down to each shape into one current
transformation matrix, then applies it to every point (6 multiplications and 4 additions per point).
For mouse events and hit testing it applies the inverse matrix to the pointer position, to find where
in the shape's own coordinates the click landed. Browsers expose these matrices directly, for example
through DOMMatrix and getScreenCTM().

**Why linear algebra is the right tool.** Representing moves as matrices turns composition into multiplication, so any sequence of transforms,
however long or nested, is one matrix computed once. Laws that designers learn by trial and error are
theorems: order matters because multiplication does not commute; undoing a sequence reverses its order;
rotating about a point is a conjugation T(c) R T(−c). Affine maps send straight lines to straight lines
and parallel lines to parallel lines, but not circles to circles or right angles to right angles, which
is why a scaled circle becomes an ellipse.

**Pitfall worth teaching.** The same list of transforms can be read in two opposite orders, and both readings are correct. Read
right to left, translate(2, 0) rotate(90) rotates the point in the original axes and then shifts it.
Read left to right, it first moves the coordinate system by (2, 0) and then rotates the moved axes, and
the shape is drawn in those new axes. Both describe the matrix product T R, and both put (1, 0) at
(2, 1). Mixing the two readings within one stack is how most "the rotation happened about the wrong
point" bugs start. A second trap is the convention for writing vectors. SVG, CSS and Canvas use column
vectors, M p, but some graphics libraries use row vectors, p M, with every matrix transposed and every
product reversed. Copying a matrix or a multiplication order between the two conventions without
transposing gives a transform that is close enough to look plausible and wrong enough to fail.

**Terminology map.** How this field's vocabulary reads as linear algebra.

| Domain term | In linear algebra |
|---|---|
| transform attribute / CSS transform property | a list of elementary transforms whose matrices are multiplied in the order written |
| matrix(a, b, c, d, e, f) | the SVG/CSS notation for the 3 × 3 matrix with columns (a, b, 0), (c, d, 0), (e, f, 1) |
| current transformation matrix (CTM) | the product of every transform in effect for an element |
| user space vs viewport space | two coordinate systems related by the CTM |
| transform-origin | the point about which rotation and scaling happen, a conjugation T(c) M T(−c) |
| translate, rotate, scale, skew | the elementary matrices of the stack |
| local vs global coordinates | reading a product right to left (each step in the parent's frame) or left to right (each step in the newly moved frame) |
| identity transform | the 3 × 3 identity, matrix(1, 0, 0, 1, 0, 0) |

**Extensions.** 3D graphics uses the same idea with 4 × 4 matrices, and adds the perspective projection that affine
maps cannot express (the 3D viewing entry). Rigid motions, rotation plus translation with no stretching,
are the 3D rotations and rigid-body pose entry. Splitting a general matrix(a, b, c, d, e, f) back into
"rotate, scale, rotate", which animation libraries do to interpolate between two transforms, is the SVD
or the polar decomposition (Tier 2). [Bézier curves](https://en.wikipedia.org/wiki/B%C3%A9zier_curve) transform correctly when their control points are
transformed by an affine map, which is why fonts and SVG paths can be scaled losslessly (the Bézier
entry).

---

## 38. 3D rotations and pose: orthogonal matrices for robots, drones and spacecraft

<details>
<summary><b>Start here — the problem in plain terms</b></summary>

A robot arm, a drone, a satellite and a character in an animated film all have to keep track of which
way they are facing. The usual way to describe an orientation is to say where an object's own
front, left and up directions point, measured in the coordinates of the room, the Earth or the stars.

Those three directions are always perpendicular to each other and always of unit length, because
turning an object cannot bend or stretch it. Written as the columns of a three-by-three table of
numbers, they form a [rotation matrix](https://en.wikipedia.org/wiki/Rotation_matrix). Turning an object twice is multiplying two such matrices, and,
as anyone who has rotated a book about two different axes knows, the order of the turns matters.

The popular alternative, three angles called [yaw](https://en.wikipedia.org/wiki/Aircraft_principal_axes), pitch and roll, is easier to read but has a famous
flaw. At one particular pitch, two of the three angles start turning the object about the same axis,
and one direction of motion simply disappears from the description. Spacecraft guidance systems had to
be designed around that flaw. The matrix description has no such blind spot, but it has its own trap,
which this entry ends with.

</details>

**Field:** Robotics, aerospace guidance and attitude control, computer vision, animation

**Tier:** 1 — rotations are 3 × 3 [orthogonal matrices](https://en.wikipedia.org/wiki/Orthogonal_matrix) with [determinant](https://en.wikipedia.org/wiki/Determinant) +1, poses are 4 × 4 homogeneous matrices, and composing them is multiplication. [Quaternions](https://en.wikipedia.org/wiki/Quaternions_and_spatial_rotation) and the rotation group as a [Lie group](https://en.wikipedia.org/wiki/Lie_group) are the Tier 3 extensions.

**Scalars and vectors.** Scalar field: R. Vectors: vectors in R^3 (directions, positions, angular axes). A rotation is a 3 × 3 matrix in the set [SO(3)](https://en.wikipedia.org/wiki/3D_rotation_group) of orthogonal matrices with determinant +1. SO(3) is a group under multiplication but not a subspace of the 9-dimensional space of 3 × 3 matrices: the sum or average of two rotations is generally not a rotation. Poses (rotation plus position) are 4 × 4 matrices in SE(3), acting on homogeneous coordinates (x, y, z, 1).

**Underlying equations.** Matrix products: v′ = R v for a rotation, and p′ = T p for a pose in homogeneous coordinates.

**The problem.** Represent the orientation of a rigid body in three dimensions, combine successive rotations, convert
vectors between the body's own axes and a fixed reference frame, track position and orientation
together (pose) along a chain of joints, and avoid the failure modes of angle-based descriptions.

**Variables.**
| Symbol | Name | What it holds | Shape | Units |
|---|---|---|---|---|
| R | rotation matrix | its columns are the body's x, y and z axes, written in reference-frame coordinates | 3 × 3 | dimensionless |
| v | vector | a direction or displacement | 3 × 1 | metres, or dimensionless for directions |
| R_x(φ), R_y(θ), R_z(ψ) | elementary rotations | turns about the x, y or z axis by the given angle | 3 × 3 | dimensionless |
| φ, θ, ψ | roll, pitch, yaw | Euler angles, here in the z-y-x convention | scalars | radians or degrees |
| t | position | where the body's origin sits in the reference frame | 3 × 1 | metres |
| T | pose | the 4 × 4 matrix [R t; 0 0 0 1] | 4 × 4 | mixed: R dimensionless, t in metres |
| p | homogeneous point | (x, y, z, 1) | 4 × 1 | metres in the first three entries |
| I | identity matrix | — | 3 × 3 | — |

**Formulation.** **Where the equations come from.** The model is the geometry of rigid motion: a rotation preserves
lengths and angles and does not turn left-handed into right-handed.

**What makes a matrix a rotation.** Preserving lengths and angles means preserving dot products, so
(R u) · (R v) = u · v for all u and v. That is equivalent to

```
Rᵀ R = I
```

that is, the columns of R are orthonormal. Then det(R)² = 1, so det R = ±1. Rotations have det R = +1;
matrices with det R = −1 are reflections, which swap left and right. The condition Rᵀ R = I also says
that the inverse is the transpose, R⁻¹ = Rᵀ, so undoing a rotation costs nothing.

**The elementary rotations.** Turning about one coordinate axis leaves that axis alone and applies the
familiar 2D rotation to the other two coordinates. About the x-axis by φ, the y–z plane turns:

```
R_x(φ) = [ 1     0        0    ]
         [ 0   cos φ   −sin φ  ]
         [ 0   sin φ    cos φ  ]
```

About the y-axis by θ, the z–x plane turns:

```
R_y(θ) = [  cos θ   0   sin θ ]
         [    0     1     0   ]
         [ −sin θ   0   cos θ ]
```

About the z-axis by ψ, the x–y plane turns:

```
R_z(ψ) = [ cos ψ  −sin ψ   0 ]
         [ sin ψ   cos ψ   0 ]
         [   0       0     1 ]
```

The minus sign in R_y sits below the diagonal rather than above it. That is not a different
convention: a positive turn about y carries z toward x (the cyclic order x → y → z → x), and in the
usual x, y, z ordering of rows and columns that puts −sin θ in the bottom-left corner.

**Composition, and its order.** Applying R_1 and then R_2 is the product R_2 R_1, and it depends on the
order. Take the vector e_1 = (1, 0, 0) and two quarter turns:

```
R_x(90°) R_z(90°) e_1 = (0, 0, 1)     first about z, then about x
R_z(90°) R_x(90°) e_1 = (0, 1, 0)     first about x, then about z
```

**[Euler angles](https://en.wikipedia.org/wiki/Euler_angles).** Aerospace and robotics often describe an attitude by yaw ψ, pitch θ and roll φ, with

```
R = R_z(ψ) R_y(θ) R_x(φ)
```

Three numbers are enough, because a rotation matrix has nine entries but six independent constraints
(three unit lengths and three right angles), leaving three degrees of freedom.

**Worked case: [gimbal lock](https://en.wikipedia.org/wiki/Gimbal_lock).** At pitch θ = 90°, the product collapses. Computing it gives

```
R_z(ψ) R_y(90°) R_x(φ) = [   0    sin(φ − ψ)   cos(φ − ψ) ]
                         [   0    cos(φ − ψ)  −sin(φ − ψ) ]
                         [  −1        0             0     ]
```

which depends on yaw and roll only through their difference φ − ψ. Increasing both by the same amount
changes nothing: two of the three angles now turn the body about the same axis, and one direction of
rotation cannot be expressed by small changes of the angles at all. The orientation is fine; the
coordinates describing it have failed. A spacecraft guidance platform built from three physical gimbals
has the same failure mechanically, which is why the Apollo crews had to keep their spacecraft away from
that orientation.

**Pose.** Position and orientation together act on homogeneous coordinates, exactly as in the 2D
affine-transforms entry:

```
T = [ R   t ]        T p = (R (x, y, z) + t, 1)        T⁻¹ = [ Rᵀ   −Rᵀ t ]
    [ 0   1 ]                                                [ 0      1   ]
```

A robot arm's [forward kinematics](https://en.wikipedia.org/wiki/Forward_kinematics) is the product T_1 T_2 ⋯ T_k of the transforms of its joints, read
from the base out to the gripper.

**Matrix structure.** Rotations are dense 3 × 3 orthogonal matrices with determinant +1; poses are 4 × 4 with bottom row
(0, 0, 0, 1). Both sets are closed under multiplication and inversion, which makes them groups, SO(3)
and SE(3). Neither is closed under addition or scaling, so neither is a vector space, and that fact is
the pitfall below.

**What is computed.** Products of small matrices: composing joint transforms, converting sensor readings from a body frame to
a world frame (v_world = R v_body) and back (v_body = Rᵀ v_world). Flight software and robot
controllers do this thousands of times per second. Long chains of products accumulate rounding error,
so software periodically re-orthonormalizes R, for example with [Gram–Schmidt](https://en.wikipedia.org/wiki/Gram%E2%80%93Schmidt_process) on its columns, and many
systems store orientations as quaternions instead.

**Why linear algebra is the right tool.** A rotation is a change between two orthonormal bases, the body's axes and the reference axes, and
everything follows from that. Its matrix has the new axes as columns; its inverse is its transpose
because the bases are orthonormal; composing rotations multiplies matrices, so order matters; and a
pose is a rotation plus a translation, which homogeneous coordinates turn into one matrix. Gimbal lock
is understood as a failure of a coordinate system on the set of rotations, not of the rotations, which
is why the cure is a better description rather than a better angle.

**Pitfall worth teaching.** Rotations are not a subspace, so the operations that work on vectors do not work on rotations.
Averaging two rotation matrices entry by entry does not give a rotation halfway between them. The
average of the identity and R_z(180°) is diag(0, 0, 1), which squashes every vector onto the z-axis and
is not invertible. The average of the identity and R_z(60°) has determinant 0.75 and shrinks vectors in
the xy-plane to about 87% of their length, although the rotation halfway between them, R_z(30°), shrinks
nothing. The same failure appears when animating by interpolating matrix entries, when smoothing noisy
attitude estimates with an ordinary filter, and when integrating small rotation updates by addition:
the result drifts away from orthogonality and objects visibly shrink or shear. Interpolating the angle
works for rotations about one fixed axis; in general it needs quaternions or the rotation group's own
geometry (the Tier 3 extensions).

**Terminology map.** How this field's vocabulary reads as linear algebra.

| Domain term | In linear algebra |
|---|---|
| attitude / orientation | a rotation matrix R relating a body frame to a reference frame |
| direction cosine matrix (DCM) | the rotation matrix; its entries are cosines of angles between axes |
| body frame vs world frame | two orthonormal bases; R changes coordinates from one to the other |
| yaw, pitch, roll (Euler angles) | coordinates on the set of rotations, R = R_z(ψ) R_y(θ) R_x(φ) |
| gimbal lock | Euler angles at which two of the three angles turn about the same axis |
| pose (frame, transform) | a rotation and a translation together, a 4 × 4 matrix in SE(3) |
| forward kinematics | the product of the joint transforms along a robot arm |
| homogeneous transformation | the 4 × 4 matrix [R t; 0 1] |
| re-orthonormalization | projecting a drifted matrix back onto the orthogonal matrices |
| handedness | the sign of the determinant; +1 for rotations, −1 for reflections |

**Extensions.** Unit quaternions represent rotations with four numbers and no gimbal lock, and interpolating them
([slerp](https://en.wikipedia.org/wiki/Spherical_linear_interpolation)) gives the "halfway rotation" that averaging matrices does not. The rotation group SO(3) is a Lie
group, and small rotations correspond to [skew-symmetric](https://en.wikipedia.org/wiki/Skew-symmetric_matrix) matrices, the setting of modern attitude
estimation and robot control (Tier 3). Rotation averaging in multiple-view geometry estimates many
camera orientations at once (the multiple-view geometry entry). The 2D affine-transforms entry is the
planar case of the pose matrix, and the 3D viewing entry adds the perspective projection that takes
poses to the screen. [Inertial navigation](https://en.wikipedia.org/wiki/Inertial_navigation_system) uses R to rotate accelerometer readings into the world frame
before integrating them (the Kalman filtering entry).

---

## 41. Polynomial interpolation: one polynomial, many bases, very different arithmetic

<details>
<summary><b>Start here — the problem in plain terms</b></summary>

Through two points there is exactly one straight line, and through three points (with different
x-values) exactly one parabola. In general, n points with different x-values determine exactly one
polynomial of degree n − 1 passing through all of them. Finding that polynomial is called
[interpolation](https://en.wikipedia.org/wiki/Polynomial_interpolation), and it sits underneath numerical integration, root finding, graphics, and the formulas
that let a computer estimate a derivative from a table of numbers.

The polynomial itself is unambiguous, but there are many ways to write it down. The familiar way is as
a sum of powers of x with coefficients. Another way chooses building-block polynomials so that the
coefficients turn out to be the data values themselves. A third adds one point at a time. They are all
the same polynomial, written in different coordinates.

Which way you choose has dramatic consequences on a computer. Written as powers of x, the coefficients
of a polynomial through twenty points can be so sensitive that rounding errors destroy every digit.
Written in a better choice of building blocks, the same polynomial can be computed to full accuracy.
Choosing the building blocks is choosing a basis, and that is the whole subject of this entry.

</details>

**Field:** Numerical analysis, scientific computing, approximation theory

**Tier:** 1 — interpolation is one square linear system in a polynomial space, and the monomial, [Lagrange](https://en.wikipedia.org/wiki/Lagrange_polynomial), Newton and Chebyshev forms are four bases for the same space. Measuring how badly a basis behaves uses the condition number, which is Tier 2.

**Scalars and vectors.** Scalar field: R. Vectors: P_d, the real polynomials of degree at most d, a vector space of dimension d + 1 whose vectors are functions. Interpolating at d + 1 distinct nodes is a linear map from P_d to R^(d+1) (a polynomial goes to its list of values), and it is invertible.

**Underlying equations.** Polynomial evaluation: the interpolant must satisfy p(x_i) = y_i at each node.

**The problem.** Given d + 1 data points (x_0, y_0), …, (x_d, y_d) with distinct x_i, find the polynomial of degree at
most d that passes through all of them, represent it in a form that is accurate and cheap to evaluate,
and choose the nodes x_i, when one has that freedom, so that the answer is not overly sensitive to
errors in the data.

**Variables.**
| Symbol | Name | What it holds | Shape | Units |
|---|---|---|---|---|
| d | degree | highest power allowed | integer | — |
| x_0, …, x_d | nodes | distinct points where the data are given | d + 1 numbers | units of x |
| y_0, …, y_d | data values | values the polynomial must take at the nodes | (d + 1) × 1 | units of y |
| p | interpolant | the polynomial with p(x_i) = y_i | element of P_d | maps x units to y units |
| V | Vandermonde matrix | row i is (1, x_i, x_i², …, x_i^d) | (d + 1) × (d + 1) | mixed: column j has units of x^j |
| a | monomial coefficients | p(x) = a_0 + a_1 x + … + a_d x^d | (d + 1) × 1 | a_j in y units per x^j |
| ℓ_0, …, ℓ_d | Lagrange basis | ℓ_j(x_i) = 1 if i = j and 0 otherwise | elements of P_d | dimensionless |
| c | Newton coefficients | p(x) = c_0 + c_1 (x − x_0) + c_2 (x − x_0)(x − x_1) + … | (d + 1) × 1 | mixed |
| T_j | Chebyshev polynomials | T_j(cos θ) = cos(j θ) | elements of P_d | dimensionless |

**Formulation.** **Where the equations come from.** The conditions are that a
polynomial takes given values at given points, and each condition is linear in the polynomial.

**The space and the map.** The polynomials of degree at most d form a vector space P_d of dimension
d + 1: they can be added and scaled, and 1, x, …, x^d is a basis. Evaluating at the nodes,

```
p  ↦  (p(x_0), p(x_1), …, p(x_d))
```

is a linear map from P_d to ℝ^(d+1). Both spaces have dimension d + 1, and a nonzero polynomial of
degree at most d has at most d roots, so the only polynomial sent to zero is the zero polynomial. The
map is therefore invertible, and every set of data values has exactly one interpolant.

**The monomial basis gives a Vandermonde system.** Writing p in powers of x turns the conditions into

```
V a = y
```

with det V = Π_(i<j) (x_j − x_i), nonzero exactly when the nodes are distinct.

**The Lagrange basis gives the identity.** The basis polynomials

```
ℓ_j(x) = Π_(m ≠ j) (x − x_m) / (x_j − x_m)
```

are 1 at node j and 0 at the others. In this basis the matrix of the evaluation map is the identity,
so the coordinates of p are the data values: p = y_0 ℓ_0 + … + y_d ℓ_d. Nothing needs to be solved.

**The [Newton basis](https://en.wikipedia.org/wiki/Newton_polynomial) gives a triangular system.** Each Newton basis polynomial vanishes at all earlier
nodes, so the matrix is lower triangular, and the coefficients (the [divided differences](https://en.wikipedia.org/wiki/Divided_differences)) come from
forward substitution. Adding a new node adds a row and a column without changing the earlier
coefficients.

**Worked case: a parabola through (0, 1), (1, 3), (2, 2).** In the monomial basis, the three
conditions p(0) = 1, p(1) = 3, p(2) = 2 are the Vandermonde system

```
[ 1  0  0 ] [ a_0 ]   [ 1 ]
[ 1  1  1 ] [ a_1 ] = [ 3 ]          so   a = (1, 3.5, −1.5)   and   p(x) = 1 + 3.5x − 1.5x²
[ 1  2  4 ] [ a_2 ]   [ 2 ]
```

The other two bases give the same polynomial with no dense solve:

```
Newton:    c_0 = 1,  c_1 = (3 − 1)/(1 − 0) = 2,  c_2 = ((2 − 3)/(2 − 1) − 2)/(2 − 0) = −1.5
           p(x) = 1 + 2x − 1.5 x(x − 1)
Lagrange:  p(x) = 1·ℓ_0(x) + 3·ℓ_1(x) + 2·ℓ_2(x)
```

Expanding the Newton or Lagrange form gives back the monomial coefficients: three coordinate vectors
for one element of P_2.

**Matrix structure.** The same linear map has a dense matrix in the monomial basis, a lower-triangular one in the Newton
basis, and the identity in the Lagrange basis. The change-of-basis matrices between them are dense. With
[Chebyshev polynomials](https://en.wikipedia.org/wiki/Chebyshev_polynomials) as the basis and [Chebyshev points](https://en.wikipedia.org/wiki/Chebyshev_nodes) x_i = cos((2i + 1)π / (2d + 2)) as the nodes,
the matrix has orthogonal columns, and its condition number is √2 whatever the number of nodes.

**What is computed.** Practical codes avoid the Vandermonde system altogether. They evaluate the Lagrange form with the
barycentric formula, which costs O(d) per point once O(d²) weights are computed and is numerically
stable, or build the Newton form when nodes arrive one at a time. For approximating a function on an
interval they use Chebyshev points and coefficients, as the [Chebfun](https://en.wikipedia.org/wiki/Chebfun) system does, computed with the fast
cosine transform.

**Why linear algebra is the right tool.** Existence and uniqueness of the interpolant are a dimension count: an injective linear map between
spaces of the same finite dimension is invertible. The various interpolation formulas taught as
separate recipes are coordinates of one vector in different bases, and the work each requires is
visible in the shape of its matrix: dense, triangular or diagonal. The numerical trouble with
high-degree interpolation is a property of the basis and the nodes, not of the polynomial, which is
why it can be cured by changing them.

**Pitfall worth teaching.** The monomial basis is a poor basis on a computer even though it is the one everyone learns. On [0, 1]
the functions x^6 and x^7 are nearly indistinguishable, so the columns of V are nearly parallel. With
8 equally spaced nodes on [0, 1] the condition number of V is about 2.7 × 10⁵, with 16 about
3 × 10¹², and with 20 about 10¹⁶, at which point a double-precision solve can lose every digit. The
interpolating polynomial is perfectly well defined throughout; only its monomial coordinates are
unstable. Changing the basis to Chebyshev polynomials at Chebyshev nodes brings the condition number
down to √2 for any number of nodes. A second, separate failure is the [Runge phenomenon](https://en.wikipedia.org/wiki/Runge's_phenomenon): at equally
spaced nodes, high-degree interpolants of perfectly smooth functions oscillate wildly near the ends of
the interval, whichever basis is used. That one is cured by moving the nodes, not by changing the basis.

**Terminology map.** How this field's vocabulary reads as linear algebra.

| Domain term | In linear algebra |
|---|---|
| nodes (interpolation points) | the d + 1 distinct x-values where the polynomial must match the data |
| interpolant | the unique element of P_d with the prescribed values at the nodes |
| monomial (power) form | coordinates in the basis 1, x, x², …, x^d |
| Lagrange form | coordinates in the basis that is dual to evaluation at the nodes, so the coordinates are the data values themselves |
| Newton form and divided differences | coordinates in the basis 1, (x − x_0), (x − x_0)(x − x_1), …, computed by a triangular solve |
| Chebyshev polynomials and nodes | a basis and a set of nodes for which the interpolation problem is well conditioned |
| barycentric formula | a stable way to evaluate the Lagrange form |
| Runge phenomenon | large oscillations of high-degree interpolants at equally spaced nodes |
| Lebesgue constant | how much the interpolation map can amplify errors in the data |

**Extensions.** Least-squares fitting with more points than coefficients is the basis-fitting entry, and the same
Vandermonde matrix appears there as a design matrix. Shamir secret sharing interpolates over GF(p),
where there is no rounding and the conditioning problem disappears. Finite-difference stencils solve a
small Vandermonde system for derivative weights. Bézier curves use the [Bernstein](https://en.wikipedia.org/wiki/Bernstein_polynomial) basis of the same
polynomial space. [Splines](https://en.wikipedia.org/wiki/Spline_interpolation) interpolate with piecewise polynomials and avoid the Runge phenomenon.
[Gaussian quadrature](https://en.wikipedia.org/wiki/Gaussian_quadrature) chooses its nodes as the roots of orthogonal polynomials, and the [Lebesgue constant](https://en.wikipedia.org/wiki/Lebesgue_constant)
measures how much a choice of nodes can amplify data errors.

---

## 42. Bézier curves: every letter on the screen is a point in a polynomial space

<details>
<summary><b>Start here — the problem in plain terms</b></summary>

Every letter in a modern font is drawn from a short list of curved pieces. A designer does not store the
thousands of pixels in a letter "S"; the font file stores a few points, and the computer works out a
smooth curve from them at whatever size the letter is printed, from a phone screen to a billboard.

For each curved piece the font stores four points. The curve starts at the first and ends at the fourth.
The two middle points are not on the curve at all: they act like magnets that pull it towards themselves,
setting the direction in which it leaves the start and arrives at the end. Moving one of them reshapes
the curve smoothly, which is why the "handles" in a drawing program behave the way they do.

The mathematics underneath is that each piece is a polynomial of degree 3, and the four points are the
polynomial's coordinates in a well-chosen basis. The everyday operations of a font or drawing program —
scaling a letter, converting a font between formats, cutting a curve in two — all turn out to be changes
of basis or other linear maps between spaces of polynomials.

</details>

**Field:** Typography, [vector graphics](https://en.wikipedia.org/wiki/Vector_graphics), computer-aided design, animation

**Tier:** 1 — a Bézier curve is a polynomial written in a particular basis, and every common operation on it is a [change of basis](https://en.wikipedia.org/wiki/Change_of_basis) or a linear map between polynomial spaces of degree at most 3. No eigenvalues are involved.

**Scalars and vectors.** Scalar field: R. Vectors: P_3, the real polynomials of degree at most 3 in a parameter t, which has dimension 4. Each coordinate x(t) and y(t) of a cubic curve is one element of P_3, so a planar cubic segment is a pair of them, a vector in P_3 × P_3 of dimension 8. The control points are its coordinates in the Bernstein basis, not points the curve passes through. [TrueType](https://en.wikipedia.org/wiki/TrueType) fonts use quadratic segments, in P_2 (dimension 3).

**Underlying equations.** Polynomial parametric curves, B(t) = Σ b_k(t) P_k, written in a chosen basis.

**The problem.** An image can be stored in two fundamentally different ways. [Raster graphics](https://en.wikipedia.org/wiki/Raster_graphics) (photographs, PNG and
JPEG files, the screen itself) store a grid of pixels: a fixed number of samples of the picture,
taken at one resolution. Enlarge a raster image and nothing new can appear between the samples, so
each pixel just becomes a bigger square and edges turn jagged and blurry. Vector graphics (fonts, SVG
and PDF drawings, logos, CAD drawings) store the shapes themselves, as curves described by a few numbers
each. The picture is computed from those numbers only when it is shown, so it can be drawn at any
resolution, and a letter zoomed in a hundredfold is as sharp as it was at normal size. It is only turned into pixels
([rasterized](https://en.wikipedia.org/wiki/Rasterisation)) at the last moment, for the particular screen or printer in use.

Both kinds of image are vectors in the linear-algebra sense, but in different spaces. A raster image
is a point in ℝ^(width × height), one coordinate per pixel, and its resolution is fixed by the
dimension of that space. A vector-graphics curve is a point in a space of polynomials, which can be
evaluated at as many parameter values as the output needs.

The problem is to represent smooth curves (glyph outlines, vector illustrations, animation timing) in
that second way, as Bézier curves, and then to draw them at any resolution, transform them, split them,
and convert them between formats that use different polynomial degrees: exactly where possible, and
approximately otherwise.

**Variables.**
| Symbol | Name | What it holds | Shape | Units |
|---|---|---|---|---|
| t | parameter | position along the segment, from its start (t = 0) to its end (t = 1); not distance along the curve | scalar in [0, 1] | dimensionless |
| P_0, …, P_3 | control points | coordinates of the curve in the Bernstein basis | each a 2 × 1 point | font units (often 1/1000 or 1/2048 of the em size) |
| b_0, …, b_3 | Bernstein polynomials | b_k(t) = C(3, k) t^k (1 − t)^(3−k), the basis functions of P_3 | functions in P_3 | dimensionless |
| B(t) | the curve | B(t) = Σ b_k(t) P_k, the point drawn at parameter t | 2 × 1 for each t | font units |
| X | control-point matrix | the control points as rows, (P_0; P_1; P_2; P_3) | 4 × 2 | font units |
| M | change-of-basis matrix | converts Bernstein coordinates to monomial coefficients | 4 × 4 | dimensionless |
| a_0, …, a_3 | monomial coefficients | B(t) = a_0 + a_1 t + a_2 t² + a_3 t³ | each 2 × 1 | font units |
| Q_0, Q_1, Q_2 | quadratic control points | a TrueType segment, in the Bernstein basis of P_2 | each 2 × 1 | font units |

**Formulation.** **Where the equations come from.** A segment is a polynomial curve,
and the modelling choice is only which basis to write it in.

**The Bernstein basis.** For cubics the basis polynomials are

```
b_0 = (1 − t)³,   b_1 = 3t(1 − t)²,   b_2 = 3t²(1 − t),   b_3 = t³
```

They are linearly independent, so they form a basis of the 4-dimensional space P_3. Each is
nonnegative on [0, 1], and by the binomial theorem they add up to ((1 − t) + t)³ = 1. The curve is

```
B(t) = b_0(t) P_0 + b_1(t) P_1 + b_2(t) P_2 + b_3(t) P_3
```

so its x-coordinate is the element of P_3 whose Bernstein coordinates are the four x-values of the
control points, and likewise for y. At t = 0 only b_0 is nonzero, and at t = 1 only b_3, so the curve
passes through P_0 and P_3 and in general through neither middle point.

**Change of basis to monomials.** Expanding the Bernstein polynomials in powers of t gives

```
(a_0; a_1; a_2; a_3) = M X,      M = [  1   0   0   0 ]
                                     [ −3   3   0   0 ]
                                     [  3  −6   3   0 ]
                                     [ −1   3  −3   1 ]
```

Column k of M⁻¹ would give the monomial t^k in Bernstein coordinates. The monomial form is convenient for
evaluating derivatives; the Bernstein form is the one people can edit, because its coordinates are points
in the plane.

**Degree elevation.** A quadratic is also a cubic, because P_2 is a subspace of P_3. In Bernstein
coordinates the inclusion is the linear map

```
P_0 = Q_0,   P_1 = (Q_0 + 2 Q_1)/3,   P_2 = (2 Q_1 + Q_2)/3,   P_3 = Q_2
```

So converting a TrueType outline to cubic (CFF) form is exact. The reverse direction is not: a cubic lies
in P_2 only when its t³ coefficient, a_3 = −P_0 + 3P_1 − 3P_2 + P_3, is zero.

**Worked case: a cubic that is secretly a quadratic.** Take P_0 = (0, 0), P_1 = (2, 2), P_2 = (4, 2),
P_3 = (6, 0). Multiplying by M gives

```
x(t) = 6t,     y(t) = 6t − 6t²
```

Both t³ coefficients vanish, and so does the t² coefficient of x: the curve is the parabola from the
quadratic segment Q_0 = (0, 0), Q_1 = (3, 3), Q_2 = (6, 0), which the degree-elevation formulas send back
to exactly these four points. Its midpoint is B(1/2) = (P_0 + 3P_1 + 3P_2 + P_3)/8 = (3, 1.5), and it
never comes near the middle control points, whose height is 2.

**Evaluation and subdivision by [de Casteljau](https://en.wikipedia.org/wiki/De_Casteljau's_algorithm).** Interpolate linearly between neighbouring control points
at the fraction t, and repeat on the new points until one is left; that point is B(t). At t = 1/2 the
example gives (1, 1), (3, 2), (5, 1), then (2, 1.5), (4, 1.5), then (3, 1.5). The points produced along
the way are, read down the left and right edges, the control points of the two halves:
(0, 0), (1, 1), (2, 1.5), (3, 1.5) and (3, 1.5), (4, 1.5), (5, 1), (6, 0). Splitting a curve is
therefore a change of basis: each half is the same polynomial, written in the Bernstein basis of a
shorter interval.

**Matrix structure.** Every map is a small dense matrix acting on the 4 × 2 array of control points: the 4 × 4 lower
triangular Bernstein-to-monomial matrix M, a 4 × 4 subdivision matrix for each half, and a 4 × 3
degree-elevation matrix from P_2 to P_3. Their entries are fixed rational numbers, so they are computed
once and applied to every segment.

**What is computed.** A renderer evaluates or subdivides each segment (often with de Casteljau steps, which only average
points and are numerically stable) until the pieces are flat enough to treat as straight lines, then
fills the outline. Font-conversion tools elevate quadratic outlines to cubic exactly, and approximate
each cubic by one or more quadratics, splitting it until the error is within a tolerance; the cu2qu
module of the fontTools library does this when fonts are compiled to TrueType.

**Why linear algebra is the right tool.** The control points are coordinates, so every operation that a font or drawing program performs is
linear in them. Changing format is a change of basis or an inclusion of one polynomial space in another;
splitting a curve is a change of basis to a subinterval; and the question "is this cubic really a
quadratic" is whether a vector lies in a subspace, settled by one linear functional. The Bernstein basis
is chosen for geometric reasons (nonnegative functions that sum to 1), which make its coordinates behave
like weighted averages of points. That property is what makes them meaningful to a designer.

**Pitfall worth teaching.** The control points transform correctly under affine maps, and only under them. Because the basis
polynomials sum to 1, B(t) is a weighted average of the control points with weights that add up to 1,
so scaling, rotating, shearing or moving the control points does the same to every point of the curve.
That is why a font can be scaled by transforming a few points. A perspective ([projective) transformation](https://en.wikipedia.org/wiki/Homography)
is not affine: it divides by a quantity that depends on the point, which does not distribute over a
weighted average. Applying a perspective map to the control points and redrawing gives a visibly
different curve from applying it to the curve itself. Representing curves exactly under perspective
requires rational Bézier curves, which use homogeneous coordinates (see the 3D viewing entry). A second
misconception has the same root: the parameter t is not distance along the curve, so equally spaced
values of t give unequally spaced points.

**Terminology map.** How this field's vocabulary reads as linear algebra.

| Domain term | In linear algebra |
|---|---|
| raster image (bitmap) | a vector in R^(width × height), one coordinate per pixel, so its resolution is fixed by the dimension |
| vector graphics | shapes stored as coordinates in a polynomial space, evaluated at whatever resolution the output needs |
| rasterization | sampling the curves onto a pixel grid, a map from the polynomial space into R^(width × height) |
| control points | coordinates of the curve in the Bernstein basis, one point in the plane per basis polynomial |
| on-curve and off-curve points (font editors) | the end control points, which the curve passes through, and the inner control points, which it generally does not |
| control polygon | the broken line through the control points; the curve lies in its convex hull |
| Bernstein polynomials | a basis of P_3 consisting of nonnegative functions that sum to 1 |
| cubic vs quadratic outlines (CFF/PostScript vs TrueType) | curves in P_3 vs curves in P_2 |
| degree elevation | the inclusion P_2 → P_3, written in Bernstein coordinates |
| de Casteljau algorithm | evaluation by repeated linear interpolation |
| subdivision (splitting a curve) | change of basis to the Bernstein basis of a subinterval |
| affine invariance | transforming the control points transforms the curve, because the basis sums to 1 |
| easing curve (CSS cubic-bezier) | a cubic in the same basis, used for timing instead of shape |

**Extensions.** [B-splines](https://en.wikipedia.org/wiki/B-spline) join many polynomial pieces with a basis of a whole space of smooth piecewise polynomials, and
[NURBS](https://en.wikipedia.org/wiki/Non-uniform_rational_B-spline) add weights, which is why CAD systems use them. [Bézier surfaces](https://en.wikipedia.org/wiki/B%C3%A9zier_surface) use the tensor-product basis
b_i(u) b_j(v) of a 16-dimensional space; the [Utah teapot](https://en.wikipedia.org/wiki/Utah_teapot) is 32 such patches. CSS animation timing
functions (cubic-bezier) are cubics in the same basis. Polynomial interpolation through given points is
the same space with a different basis (the polynomial interpolation entry), and least-squares fitting of
a curve to scanned points is the basis-fitting entry. The affine-transform and 3D viewing entries are the
matrices that act on control points.

---

## 47. The discrete Fourier transform: a change to a basis of complex waves

<details>
<summary><b>Start here — the problem in plain terms</b></summary>

Any sound, radio signal or row of pixels can be recorded as a list of numbers: the signal's value at
equally spaced moments. For many purposes that list is the wrong description. A musician wants to know
which notes are present, an engineer which frequencies carry interference, and a compression program
which parts can be thrown away without anyone noticing.

The [discrete Fourier transform](https://en.wikipedia.org/wiki/Discrete_Fourier_transform) answers by rewriting the list as a combination of pure waves: a
constant, a wave that goes up and down once over the block of samples, one that goes twice, and so on.
Each wave gets one coefficient, telling how much of it is present and where in its cycle it starts.
The list of coefficients is the signal's spectrum.

That rewriting is a change of coordinates, from "value at each moment" to "amount of each wave". The
waves are perpendicular to each other, which makes the change easy to undo and means it preserves the
total energy of the signal. To describe both how much of a wave is present and where it starts with a
single number, the coordinates are complex numbers, so this is linear algebra over the complex numbers
instead of the real ones.

</details>

**Field:** Signal processing, audio, communications, image processing, spectroscopy

**Tier:** 1 — the DFT is multiplication by one explicit complex matrix whose columns form an orthogonal basis, so it needs complex numbers but no eigenvalues. That the DFT diagonalizes every [circulant](https://en.wikipedia.org/wiki/Circulant_matrix) matrix, the reason convolution becomes multiplication, is an eigenvector statement and Tier 2.

**Scalars and vectors.** Scalar field: C, the complex numbers, even when the signal itself is real: the basis vectors are complex waves, so the coordinates are complex. Vectors: C^N for a block of N samples, with the complex inner product ⟨u, v⟩ = Σ conj(u_n) v_n. A real signal lies in the real subset R^N, which is not a complex subspace, and its transform has the conjugate symmetry X_(N−k) = conj(X_k).

**Underlying equations.** A change of basis on a finite block of samples, X = F x.

**The problem.** Given a block of N equally spaced samples of a signal, find how much of each of the N basic
frequencies it contains, and be able to rebuild the samples exactly from those amounts.

**Variables.**
| Symbol | Name | What it holds | Shape | Units |
|---|---|---|---|---|
| N | block length | number of samples | integer | — |
| x | signal | samples x_0, …, x_(N−1) | N × 1, complex in general (often real) | signal units (volts, pressure, brightness) |
| ω | root of unity | ω = e^(−2πi/N), so ω^N = 1 | complex scalar | dimensionless |
| w_k | wave of frequency k | (w_k)_n = e^(2πi kn/N): k complete cycles over the block | N × 1 complex | dimensionless |
| F | DFT matrix | F_kn = ω^(kn), for k, n = 0, …, N − 1; row k is the conjugated wave w_k | N × N complex | dimensionless |
| X | spectrum | X = F x; X_k is the coefficient of frequency k | N × 1 complex | signal units |
| U | unitary DFT | U = F / √N | N × N complex | dimensionless |
| Fᴴ | conjugate transpose | the transpose with every entry replaced by its complex conjugate | N × N | dimensionless |

Bin k corresponds to k cycles per block, which is k / (N Δt) cycles per second if the samples are Δt
seconds apart.

**Formulation.** **Where the equations come from.** The model is a choice of basis
for the space of length-N blocks of samples.

**One frequency at a time.** The wave of frequency k is the vector w_k whose n-th entry is

```
(w_k)_n = e^(2πi kn/N) = cos(2π kn/N) + i sin(2π kn/N),     n = 0, …, N − 1
```

As n runs through the block, its angle 2π kn/N goes round the unit circle exactly k times, so w_k
makes k complete cycles: w_0 is the constant vector, w_1 one slow cycle, and so on. To measure how much
of this wave the signal contains, multiply each sample by the complex conjugate of the wave's value at
that moment and add the results:

```
X_k = Σ_(n=0)^(N−1) x_n · conj((w_k)_n) = Σ_(n=0)^(N−1) x_n e^(−2πi kn/N)
```

This is the familiar DFT formula from signal processing. It is the complex inner product of the wave
with the signal, X_k = ⟨w_k, x⟩, where the inner product on ℂ^N conjugates its first argument,
⟨u, v⟩ = Σ conj(u_n) v_n, so that ⟨v, v⟩ = Σ |v_n|² is a length squared. Splitting the exponential
into its cosine and sine parts shows what the number means. The real part of X_k is Σ x_n cos(2π kn/N),
the correlation of the signal with a cosine of frequency k, and the imaginary part is
−Σ x_n sin(2π kn/N), the correlation with a sine. Together they say how large the frequency-k
component is, |X_k|, and where in its cycle it starts, the angle of X_k.

**All frequencies at once.** Doing this for every k = 0, …, N − 1 gives N inner products, one per
frequency. Stacking them, row k of a matrix holds the conjugated wave, e^(−2πi kn/N) = ω^(kn) in
column n, and the whole spectrum is one matrix-vector product:

```
X = F x,     F_kn = ω^(kn)
```

**Orthogonality, and the inverse.** With the complex inner product, the N waves w_0, …, w_(N−1) are
mutually orthogonal and each has squared length N:

```
Fᴴ F = N I
```

So the inverse is just the [conjugate transpose](https://en.wikipedia.org/wiki/Conjugate_transpose), scaled: x = (1/N) Fᴴ X, which is the inverse DFT
formula x_n = (1/N) Σ X_k e^(2πi kn/N). Scaled to U = F/√N, the matrix is unitary, Uᴴ U = I: the
complex version of an orthogonal matrix, a rotation of ℂ^N.

**[Parseval](https://en.wikipedia.org/wiki/Parseval's_theorem)'s identity.** A unitary change of basis preserves length, so Σ |x_n|² = (1/N) Σ |X_k|²:
the energy of the signal can be added up over time or over frequency.

**Worked case: N = 4.** Here ω = e^(−2πi/4) = −i, so every entry of F is 1, −i, −1 or i:

```
F = [ 1    1    1    1 ]
    [ 1   −i   −1    i ]
    [ 1   −1    1   −1 ]
    [ 1    i   −1   −i ]
```

For x = (1, 2, 3, 4), one coefficient at a time, X_1 multiplies the samples by the row
(1, −i, −1, i) and adds them:

```
X_1 = 1·1 + 2·(−i) + 3·(−1) + 4·(i) = −2 + 2i
```

and doing the same with every row gives the whole spectrum:

```
X = F x = (10,  −2 + 2i,  −2,  −2 − 2i)
```

X_0 = 10 is the sum, four times the mean (the DC component). X_2 = −2 is the alternating pattern
+ − + −, the fastest wave four samples can hold. X_3 is the complex conjugate of X_1, as it must be for
a real signal. Parseval checks: 1 + 4 + 9 + 16 = 30, and (100 + 8 + 4 + 8)/4 = 30. Multiplying X by
Fᴴ/4 returns (1, 2, 3, 4).

**Matrix structure.** `F` is dense, complex and symmetric (F_kn = F_nk), but it is not Hermitian, because the conjugate of
its transpose is a different matrix. Scaled by 1/√N it is unitary. All its entries are powers of a
single number ω, which lie on the unit circle, and that repetition is what lets the matrix be factored
into about log₂ N sparse factors.

**What is computed.** For small N, or a handful of frequencies, the transform is computed directly as a matrix-vector
product. For anything larger, the [fast Fourier transform](https://en.wikipedia.org/wiki/Fast_Fourier_transform) computes exactly the same product in
O(N log N) operations instead of O(N²) by factoring F into sparse matrices (the FFT entry). Libraries
such as FFTW, numpy.fft and Julia's FFTW.jl differ in scaling conventions, which the pitfall
discusses.

**Why linear algebra is the right tool.** Seeing the DFT as a change of basis explains its properties without computation. It is invertible
because the waves are a basis. The inverse is cheap because the basis is orthogonal, and energy is
preserved because the change is unitary. Filtering is "change basis, scale some coordinates, change
back". [Leakage](https://en.wikipedia.org/wiki/Spectral_leakage), the spreading of a pure tone across many bins, happens because a wave whose frequency
is not a whole number of cycles per block is not one of the N basis vectors, so its coordinates in that
basis are spread out. Compression works because many real signals have most of their length in a few
coordinates of a well-chosen basis.

**Pitfall worth teaching.** In ℂ^N, the transpose is not the inverse of a unitary matrix; the conjugate transpose is. Using the
plain transpose, as one would for a real orthogonal matrix, is a common bug: Uᵀ U is not the identity.
For N = 4 it is the matrix that reverses the order of bins 1 to 3, so "inverting" with the transpose
returns the signal with time running backwards (x_0, x_3, x_2, x_1) instead of an error message. In
NumPy, `U.T` is the transpose and `U.conj().T` the conjugate transpose; in MATLAB and Julia, `'`
conjugates and `.'` or `transpose` does not. The same bug appears as forgetting to conjugate when
computing a complex inner product. A second source of disagreement is convention: libraries put the
1/N on the inverse (NumPy, MATLAB), split it as 1/√N on both sides (the unitary convention), or
leave it to the user (FFTW), and some fields use e^(+2πi kn/N) in the forward transform. All of them
are the same change of basis with differently scaled or conjugated basis vectors.

**Terminology map.** How this field's vocabulary reads as linear algebra.

| Domain term | In linear algebra |
|---|---|
| samples | the coordinates of the signal in the standard basis (one per time step) |
| frequency bin k | the coefficient of the k-th complex wave in the Fourier basis |
| spectrum | the coordinate vector in the Fourier basis; its magnitudes are what a spectrum analyzer shows |
| inverse DFT | the change of basis back, using the conjugate transpose |
| twiddle factor ω^(kn) | an entry of the DFT matrix |
| DC component | bin 0, the coefficient of the constant vector, N times the mean |
| Nyquist bin | bin N/2, the fastest wave a block of N samples can represent |
| negative frequencies | bins N/2 + 1 to N − 1, the complex conjugates of positive ones for a real signal |
| Parseval's theorem | the change of basis preserves length (energy), up to the factor N |
| spectral leakage | energy of a wave that is not one of the N basis waves, spread across many coordinates |
| FFT | a factorization of the DFT matrix into sparse factors, not a different transform |

**Extensions.** The DFT matrix diagonalizes every circulant matrix, which is why convolution in time becomes
multiplication in frequency; that is an eigenvector statement (Tier 2). The FFT as a matrix
factorization is its own entry. The [discrete cosine transform](https://en.wikipedia.org/wiki/Discrete_cosine_transform) of JPEG compression is a real orthogonal
cousin (the JPEG entry), and Fourier series are the same idea for functions on an interval rather than
finite blocks (the Fourier series entry). Orthogonal [frequency-division multiplexing](https://en.wikipedia.org/wiki/Orthogonal_frequency-division_multiplexing) (OFDM), used in
Wi-Fi, 4G and 5G, transmits data directly as DFT coordinates. Quantum computing's quantum Fourier
transform is this unitary matrix acting on the amplitudes of n qubits, with N = 2^n.

---

## 48. Shamir secret sharing: a threshold is a theorem about interpolation

<details>
<summary><b>Start here — the problem in plain terms</b></summary>

Suppose a company's master password must never be in one person's hands, but any three of its five
directors acting together should be able to recover it. Splitting the password into five pieces does not
work: each piece gives part of the password away, and losing one piece loses the password.

The trick uses a fact from school algebra: two points determine a line, three points determine a
parabola, and in general k points determine a polynomial of degree k − 1. Hide the password as the
height of a parabola where it crosses the vertical axis, choose the rest of the parabola at random, and
give each director one point on it. Any three directors can rebuild the parabola and read off the
password. Any two cannot, and this is the surprising part: through two points there is a parabola
crossing the axis at every possible height, all equally likely, so two points reveal nothing at all.

For this to be exact, the arithmetic is done with whole numbers that wrap around at a fixed prime, like
the hours on a clock. That number system still allows division, which interpolation needs, and it has no
rounding and no sizes that leak information.

</details>

**Field:** Cryptography, key management, distributed systems security

**Tier:** 1 — everything is polynomial interpolation, a Vandermonde solve, done in the integers [modulo](https://en.wikipedia.org/wiki/Modular_arithmetic) a prime p. Arithmetic modulo a prime obeys the usual rules of algebra, including division by any nonzero number, and nothing more from abstract algebra is needed. The byte-wise version used in practice works in GF(2^8), which is Tier 3.

**Scalars and vectors.** Scalar field: GF(p), the integers 0 to p − 1 with arithmetic modulo a prime p (in practice p is a prime larger than any possible secret, often 127 or more bits). Vectors: P_(k−1)(GF(p)), the polynomials of degree at most k − 1 with coefficients in GF(p), a k-dimensional space; the n shares are a vector in GF(p)^n, the image of a polynomial under the evaluation map.

**Underlying equations.** Polynomial evaluation and interpolation over the finite field GF(p).

**The problem.** Split a secret s into n shares so that any k of them determine s, while any k − 1 of them give no
information about s whatsoever.

**Variables.**
| Symbol | Name | What it holds | Shape | Units |
|---|---|---|---|---|
| p | modulus | a prime larger than the secret and than n | integer | — |
| s | secret | the value to be protected, an element of GF(p) | scalar | — |
| k | threshold | number of shares needed to reconstruct | integer | — |
| n | number of shares | number of parties | integer | — |
| a_1, …, a_(k−1) | random coefficients | chosen uniformly at random from GF(p) by the dealer | scalars | — |
| f | sharing polynomial | f(x) = s + a_1 x + … + a_(k−1) x^(k−1), so f(0) = s | element of P_(k−1) | — |
| x_i | evaluation point | the public label of party i; distinct and nonzero | scalar per party | — |
| y_i | share value | y_i = f(x_i), kept secret by party i | scalar per party | — |
| V | Vandermonde matrix | row i is (1, x_i, x_i², …, x_i^(k−1)) | k × k for k parties | — |
| c | coefficient vector | (s, a_1, …, a_(k−1)), the coordinates of f in the basis 1, x, …, x^(k−1) | k × 1 | — |
| λ_i | Lagrange coefficients | weights such that s = Σ λ_i y_i | one per participating party | — |

Every quantity is an element of GF(p), the integers 0, 1, …, p − 1 with addition and multiplication
modulo p, so there are no physical units. Because p is prime, every nonzero element has a reciprocal:
in GF(13), for example, 1/2 = 7, since 2 × 7 = 14 = 1 modulo 13.

**Formulation.** **Where the equations come from.** The model is polynomial evaluation
over the finite field GF(p).

**Sharing.** The dealer puts the secret in the constant term and picks the other k − 1 coefficients at
random:

```
f(x) = s + a_1 x + a_2 x² + … + a_(k−1) x^(k−1)
y_i = f(x_i)          for i = 1, …, n
```

The map that sends a polynomial to its values at x_1, …, x_n is linear, from the k-dimensional space
P_(k−1) to GF(p)^n. In coordinates it is the n × k Vandermonde matrix with rows (1, x_i, …, x_i^(k−1)).

**Reconstruction from k shares.** Any k parties hold k equations in the k unknown coefficients:

```
V c = y
```

A square Vandermonde matrix with distinct x_i has determinant Π_(i<j) (x_j − x_i), which is nonzero, so
the system has exactly one solution, and the secret is its first entry. Nobody needs the full solution.
Writing f in the Lagrange basis gives the secret directly as a fixed linear combination of the shares:

```
s = f(0) = Σ λ_i y_i,     λ_i = Π_(j ≠ i) x_j / (x_j − x_i)
```

The weights depend only on which parties are present, not on the secret.

**Secrecy against k − 1 shares.** With only k − 1 equations, V is (k − 1) × k and has a one-dimensional
null space. For every candidate secret s′, adding the equation f(0) = s′ gives a square Vandermonde
system (with the extra point x = 0), which has exactly one solution. So each of the p possible secrets is
consistent with exactly one polynomial, and since the dealer chose the coefficients uniformly, every
secret is equally likely given what the k − 1 parties see.

**Worked case: 3 of 5 over GF(13).** Take s = 7 and f(x) = 7 + 3x + 5x² modulo 13. The five shares are
(1, 2), (2, 7), (3, 9), (4, 8), (5, 4). Parties 1, 2 and 3 compute

```
λ_1 = (2·3)/((2−1)(3−1)) = 3
λ_2 = (1·3)/((1−2)(3−2)) = −3 = 10
λ_3 = (1·2)/((1−3)(2−3)) = 1
s = 3·2 + 10·7 + 1·9 = 85 = 7   (mod 13)
```

Parties 1 and 2 alone, holding (1, 2) and (2, 7), find that s = 0 fits f(x) = 7x + 8x², s = 1 fits
1 + 12x + 2x², s = 2 fits 2 + 4x + 9x², and so on through all thirteen values: one polynomial for each
possible secret.

**Matrix structure.** A small dense k × k Vandermonde matrix over GF(p), never formed explicitly in practice: the Lagrange
weights are computed directly, at a cost of O(k²) multiplications and k modular inverses.

**What is computed.** Sharing is k − 1 random draws and n polynomial evaluations by [Horner's](https://en.wikipedia.org/wiki/Horner's_method) rule. Reconstruction is the
Lagrange combination at x = 0. Each [reciprocal modulo](https://en.wikipedia.org/wiki/Modular_multiplicative_inverse) p is computed with the [extended Euclidean](https://en.wikipedia.org/wiki/Extended_Euclidean_algorithm) algorithm
or as a^(p−2) by [Fermat's little theorem](https://en.wikipedia.org/wiki/Fermat's_little_theorem). Real tools, such as the unseal keys of HashiCorp Vault, split
a key byte by byte and do the same arithmetic in GF(2^8), a 256-element field.

**Why linear algebra is the right tool.** The security claim is a rank statement. Reconstruction works because k distinct evaluation points give
an invertible Vandermonde matrix, and secrecy holds because k − 1 points leave a one-dimensional space
of polynomials, every point of which corresponds to a different secret. Both halves of the threshold
property are the single fact that the evaluation map from P_(k−1) to k distinct points is invertible.
The same fact also gives the extras for free: adding two sharings gives a sharing of the sum, which is
the starting point for computing on secrets without revealing them.

**Pitfall worth teaching.** The arithmetic must be done in a field. Over the ordinary integers a single share already leaks: with
x_1 = 2, the share f(2) = s + 2a_1 + 4a_2 has the same parity as s, so the party holding it knows whether
the secret is even or odd. The secrecy argument needs every value of the free coefficient to be equally
likely, and there is no uniform choice of a whole number. Modulo a composite number such as 256 the
argument breaks differently: x_j − x_i can share a factor with the modulus, the reciprocal that the
Lagrange formula needs does not exist, and the Vandermonde determinant Π (x_j − x_i) can be 0 even
though the x_i are distinct. A byte-wise implementation that reduces "modulo 256" instead of working in
the field GF(2^8) is broken in exactly this way. Two further rules are easy to forget: x = 0 must never
be handed out as a share, because f(0) is the secret, and the coefficients a_i must be genuinely random.

**Terminology map.** How this field's vocabulary reads as linear algebra.

| Domain term | In linear algebra |
|---|---|
| dealer | whoever chooses the polynomial and hands out the shares |
| share | a point (x_i, f(x_i)), one coordinate of the evaluation map's output |
| threshold k | the dimension of the polynomial space, deg f + 1 |
| (k, n) scheme | a polynomial in a k-dimensional space evaluated at n distinct points |
| reconstruction | Lagrange interpolation evaluated at x = 0, a fixed linear combination of the shares |
| Lagrange coefficients | the weights λ_i, which depend only on which parties are present |
| perfect (information-theoretic) secrecy | every candidate secret is consistent with the same number of polynomials through any k − 1 shares |
| share refresh (proactive sharing) | adding a sharing of 0, a polynomial from the subspace with f(0) = 0 |
| corrupted share | an error in a Reed-Solomon codeword |

**Extensions.** The shares of one secret form a codeword of a Reed–Solomon code, so a corrupted or dishonest share is a
codeword error, and the [Berlekamp–Welch](https://en.wikipedia.org/wiki/Berlekamp%E2%80%93Welch_algorithm) decoder (one more linear solve) identifies and corrects it
(see the [error-correcting](https://en.wikipedia.org/wiki/Error_correction_code) codes entry). [Verifiable secret sharing](https://en.wikipedia.org/wiki/Verifiable_secret_sharing) lets parties check their shares against
public commitments, which needs exponentiation in a cyclic group (Tier 3). [Threshold signatures](https://en.wikipedia.org/wiki/Threshold_cryptosystem) and
secure [multiparty computation](https://en.wikipedia.org/wiki/Secure_multi-party_computation) build on the linearity noted above. The same interpolation over the reals
is the polynomial interpolation entry, with conditioning problems that a finite field does not have, and
finite-difference stencils solve a similar small Vandermonde system. RAID-6 storage uses the same
Reed–Solomon arithmetic to survive two failed disks (compare the RAID-5 parity entry).

---

## 49. RAID-5: rebuilding a lost disk by solving one linear equation

<details>
<summary><b>Start here — the problem in plain terms</b></summary>

A storage array spreads data across several disks. Disks fail, and copying everything twice to survive
a failure would halve the usable space. RAID-5 survives the loss of any one disk at the cost of just one
disk's worth of extra space.

The trick is a [checksum](https://en.wikipedia.org/wiki/Checksum) of the simplest possible kind. For each group of blocks stored at the same
position on the data disks, the array stores one extra block, built bit by bit: each bit records
whether the matching bits of the data blocks contain an even or an odd number of 1s. If one disk dies,
every one of its bits can be worked out from the others, because the count of 1s in each position has
to come out even again. The missing bit is whatever makes it so.

In algebra this is one equation, data plus check equals zero, in the arithmetic where 1 + 1 = 0, and
recovering a lost disk is solving that equation for its single unknown. Everything about what RAID-5
can and cannot do follows from it being one equation: one unknown can be found, but two cannot, and a
block that is wrong rather than missing can be noticed but not located.

</details>

**Field:** Storage systems, system administration, distributed storage

**Tier:** 1 — one parity equation over GF(2), the numbers 0 and 1 with arithmetic modulo 2 (addition is [XOR](https://en.wikipedia.org/wiki/Exclusive_or)), solved for one unknown. Surviving two failures needs a second independent equation over the larger field GF(2^8), which is Tier 3.

**Scalars and vectors.** Scalar field: GF(2), the numbers 0 and 1 with arithmetic modulo 2 (addition is XOR, and subtraction is the same as addition). Vectors: GF(2)^w for a block of w bits: every block of a stripe is a vector, and the parity equation holds coordinate by coordinate, one bit position at a time. A stripe across n disks is a point of (GF(2)^w)^n, and the valid stripes form the subspace cut out by the parity equation.

**Underlying equations.** One linear equation over GF(2) per stripe, applied to each bit position: the data blocks and the parity block add up to zero modulo 2.

**The problem.** Two words carry the whole subject. A **block** is a fixed-size piece of one disk: a run of consecutive
bits, typically 4 KiB to 1 MiB, and the unit that the array reads, writes and protects (storage
engineers also call it a chunk or stripe unit). The array divides every disk into blocks and lines them
up across the disks. A **stripe** is then the set of n blocks at the same position, one on each disk:
the first block of every disk forms stripe 1, the second block of every disk forms stripe 2, and so on.
In RAID-5, n − 1 blocks of each stripe hold data and the remaining one, the parity block, is computed
from them. Each stripe is protected on its own, so recovering a failed disk means recovering its block
in every stripe, one stripe at a time.

The problem is to store data on n disks so that the contents of any one failed disk can be
reconstructed from the other n − 1, using one block of redundancy per stripe (one disk's worth in
total), and to keep the parity correct as data change.

**Variables.**
| Symbol | Name | What it holds | Shape | Units |
|---|---|---|---|---|
| n | number of disks | disks in the array, including parity | integer | — |
| w | block size | bits per block | integer | bits |
| d_1, …, d_(n−1) | data blocks | the data in one stripe | each a w × 1 vector over GF(2) | bits |
| p | parity block | the check block of the stripe | w × 1 over GF(2) | bits |
| d_old, d_new | one data block | before and after an update | w × 1 | bits |
| p_old, p_new | parity block | before and after the update | w × 1 | bits |

All arithmetic is in GF(2): 0 + 0 = 1 + 1 = 0 and 0 + 1 = 1, which on blocks is the bitwise exclusive
OR (XOR). Since 1 + 1 = 0, every block is its own negative, and subtracting is the same as adding.

**Formulation.** **Where the equations come from.** The model is a design choice: the parity block of every stripe is
defined to make one linear equation hold.

**One bit position.** Look at bit position k of every block in a stripe. The [parity bit](https://en.wikipedia.org/wiki/Parity_bit) is defined by

```
p[k] = d_1[k] + d_2[k] + ⋯ + d_(n−1)[k]     (mod 2)
```

which is the even-or-odd count of 1s: p[k] is 1 exactly when the data bits in position k contain an odd
number of 1s. Moving p[k] to the left side, which costs nothing because subtraction is addition, gives
the equation that every stripe satisfies:

```
d_1[k] + d_2[k] + ⋯ + d_(n−1)[k] + p[k] = 0     (mod 2)
```

**All bit positions at once.** The same equation holds in every one of the w positions, so for whole
blocks it reads d_1 + ⋯ + d_(n−1) + p = 0 in GF(2)^w. In matrix terms each bit position is the 1 × n
system (1 1 ⋯ 1) v = 0, with v the n bits of that position across the disks. Its rank is 1, so the
valid stripes form a subspace of dimension n − 1: any n − 1 blocks can be chosen freely, and the last
is determined.

**Recovering a lost disk.** If disk j fails, its block is the only unknown in the equation. Solving
for it, and remembering that subtraction is addition,

```
d_j = (sum of all the other blocks of the stripe)     (mod 2)
```

so the lost block is the XOR of the survivors.

**Updating one block.** When block d_i changes from d_old to d_new, the equation still has to hold.
Because it is linear, the parity changes by the same amount as the data:

```
p_new = p_old + d_old + d_new
```

so a small write reads only the old data and old parity, not the rest of the stripe.

**Worked case: four disks, 4-bit blocks.** Data d_1 = 1011, d_2 = 0110, d_3 = 1100 give parity
p = 1011 + 0110 + 1100 = 0001. If disk 2 fails, d_2 = d_1 + d_3 + p = 1011 + 1100 + 0001 = 0110, as
stored. If d_2 is then rewritten as 0011, the new parity is 0001 + 0110 + 0011 = 0100, and indeed
1011 + 0011 + 1100 = 0100.

**Matrix structure.** One row of 1s, 1 × n, applied independently to each of the w bit positions, so the whole stripe is a
w × nw system made of w identical copies. Real arrays also rotate which disk holds the parity from
stripe to stripe, so that parity updates do not all land on one disk. That changes which coordinate is
called p, not the equation.

**What is computed.** Writing a full stripe: one XOR across the data blocks. Updating one block: read the old data and
parity, XOR in the change, write both back, which is four disk operations and the reason small writes
are slow on RAID-5. Reading in degraded mode or rebuilding: XOR the surviving blocks of each stripe.
Processors provide vector instructions that XOR many bytes at once, and the Linux md driver chooses the
fastest routine at boot.

**Why linear algebra is the right tool.** Every capability and limit of RAID-5 is a statement about one linear equation. One unknown can be
solved for; two unknowns in one equation leave a one-dimensional solution set, so a second failure
during a rebuild loses data. Updating parity from the change alone works because the equation is
linear. The design generalizes exactly as linear algebra suggests: to survive two failures, add a second
equation independent of the first (RAID-6), and to survive r failures, use r independent equations,
which is an [erasure code](https://en.wikipedia.org/wiki/Erasure_code).

**Pitfall worth teaching.** Parity corrects erasures, not errors. If a disk reports that it has failed, the unknown's position is
known and the equation can be solved. If instead a block is silently wrong, through a firmware bug, a
bit flip or the write hole (a crash after the data block was written but before its parity), the stripe
simply violates its equation. The array can detect that something is wrong, but one equation cannot say
which of the n blocks is the culprit: changing any one of them would restore it. Worse, if the mismatch
goes unnoticed and a disk later fails, the rebuild solves the equation using the wrong block and
reconstructs wrong data without any warning. This is the linear-algebra content of the advice that
RAID is not a backup, and the reason file systems such as [ZFS](https://en.wikipedia.org/wiki/ZFS) add checksums: a checksum locates the bad
block, turning the error back into an erasure.

**Terminology map.** How this field's vocabulary reads as linear algebra.

| Domain term | In linear algebra |
|---|---|
| stripe | one block from each disk at the same position, the unknowns of one parity equation |
| stripe unit (chunk) | one block of a stripe, a vector in GF(2)^w |
| parity block | the block chosen so that every stripe satisfies d_1 + ⋯ + d_(n−1) + p = 0 |
| XOR | addition in GF(2), applied bit by bit |
| degraded mode | one block of each stripe unknown, recovered on every read by solving the equation |
| rebuild (resilvering) | solving the equation for the failed disk's block in every stripe |
| read-modify-write (small write) | updating parity by p_new = p_old + d_old + d_new, which uses linearity |
| write hole | a crash between writing data and parity, which leaves a stripe that violates its equation |
| erasure vs error | a lost block at a known position (solvable) vs a wrong block at an unknown position (only detectable) |
| RAID-6 | a second, independent equation over GF(2^8), so two erasures can be solved |

**Extensions.** RAID-6 adds a second check block, computed with coefficients from the 256-element field GF(2^8), so
that two erasures give two independent equations; the scheme is a Reed–Solomon code (the
error-correcting codes entry, Tier 3 for GF(2^m)). Distributed storage systems use the same idea with
more check blocks, and the error-correcting codes entry shows how several parity checks can locate an
error as well as fill an erasure. Shamir secret sharing is the same equations-from-redundancy idea over
GF(p), arranged so that too few shares reveal nothing. [CRC](https://en.wikipedia.org/wiki/Cyclic_redundancy_check) checksums, which detect errors in
transmitted data, are also linear over GF(2) (the CRC entry).

---

## 51. Traffic flow: why counting cars at the edges leaves a free variable inside

<details>
<summary><b>Start here — the problem in plain terms</b></summary>

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

</details>

**Field:** Transportation engineering, traffic monitoring, [network flow](https://en.wikipedia.org/wiki/Flow_network)

**Tier:** 1 — conservation at each intersection is a linear system with more unknowns than independent equations, solved by elimination into a particular solution plus the null space. Choosing among the admissible flows by optimization (network flow, [linear programming](https://en.wikipedia.org/wiki/Linear_programming)) is Tier 2.

**Scalars and vectors.** Scalar field: R; flows on one-way streets are further restricted to nonnegative values. Vectors: R^m, one coordinate per internal road segment (m = 4 in the worked case), each the net flow along a chosen reference direction. The equations are indexed by intersections, so the incidence matrix maps R^m to R^n with n intersections. On one-way streets the physically possible flows are the nonnegative solutions, which form a [convex set](https://en.wikipedia.org/wiki/Convex_set) (here a ray), not a subspace.

**Underlying equations.** A conservation law at each intersection: cars per hour in equals cars per hour out.

**The problem.** Given the traffic entering and leaving a road network at each intersection, find all flows on the
internal road segments that are consistent with conservation, identify which flows are determined and
which are free, and find the range each flow can take when the streets are one-way, so that no flow
can be negative.

**Variables.**
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

**Formulation.** **Where the equations come from.** The model is conservation of vehicles at each intersection over a
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
the rank of A is n − 1. In the worked case the S equation is minus the sum of the other three.

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

**Matrix structure.** `A` is the node-by-segment incidence matrix of a directed graph: sparse, with exactly one +1 and one −1
in every column. Its rank is n minus the number of connected pieces of the network, and its null space
is spanned by the loops. These are the same objects, transposed, as the incidence matrix of the
resistor-network entry, where the null space of Aᵀ was the space of loop currents.

**What is computed.** For a small district: [Gaussian elimination](https://en.wikipedia.org/wiki/Gaussian_elimination) to reduced [echelon form](https://en.wikipedia.org/wiki/Row_echelon_form), which separates pivot variables
from free ones and writes the solution as a particular solution plus null-space vectors. Traffic
agencies then add constraints and data: detector counts on some segments, capacity limits, and
nonnegativity. Estimating flows that fit the counts best is a least-squares or linear programming
problem, and predicting how drivers will divide among routes is [traffic assignment](https://en.wikipedia.org/wiki/Route_assignment).

**Why linear algebra is the right tool.** The questions an engineer asks are rank questions. Are the edge counts enough? Only if the network
has no loops, since each loop adds a dimension to the null space. How many segments must be counted
inside? As many as the null space has dimensions, chosen so that the counted coordinates pin every
null-space vector down. Which segments are determined by the edge counts alone? Exactly those on which
every null-space vector is zero, such as a bridge that is the only route between two parts of the
network. The structure of the answer, a particular solution plus a subspace, is the general theorem
about solutions of linear systems, with the subspace given a physical meaning.

**Pitfall worth teaching.** On one-way streets, the solution set of the equations is a subspace shifted by a particular solution,
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

**Terminology map.** How this field's vocabulary reads as linear algebra.

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

**Extensions.** Choosing the cheapest admissible flows is a network flow problem, a linear program whose constraint
matrix is this incidence matrix. Such matrices are [totally unimodular](https://en.wikipedia.org/wiki/Unimodular_matrix), so whole-number data give
whole-number optimal flows automatically (see the linear programming entry). Estimating the
origin-destination table from a few detector counts is an underdetermined least-squares problem with
nonnegativity (compare the regression entry). The same conservation-at-nodes structure describes
current in the resistor-network entry, material in the process mass-balance entry, and money between
sectors in the Leontief entry.

---

## 52. Process mass balances: a recycle loop is what makes it a system of equations

<details>
<summary><b>Start here — the problem in plain terms</b></summary>

A chemical plant is a network of units connected by pipes: mixers that combine streams, [reactors](https://en.wikipedia.org/wiki/Chemical_reactor) that
convert one substance into another, and separators that split a stream into its parts. The first job in
designing or running one is bookkeeping. Every hour, how much of each substance flows through each
pipe?

The rule is simple: with the plant running steadily, whatever goes into a unit comes out, except for
what the reaction makes or uses up. Applying it to each substance at each unit gives one equation each.

Without loops this is easy: start at the feed and work forward, one unit at a time. Real plants almost
always recycle, though. A reactor rarely converts all of its feed, so the separator sends the unreacted
material back to the front to try again. Now the reactor's feed depends on the separator's output,
which depends on the reactor. The equations can no longer be solved one at a time. They have to be
solved together, which makes the [flowsheet](https://en.wikipedia.org/wiki/Process_flow_diagram) a system of linear equations.

</details>

**Field:** Chemical engineering, process design, plant operations

**Tier:** 1 — with fixed conversions and split fractions every balance is linear, and the flowsheet is one square linear system. Why the unit-by-unit recycle iteration converges, and how fast, is a spectral-radius question and Tier 2.

**Scalars and vectors.** Scalar field: R, with physical flows restricted to nonnegative values. Vectors: R^6 in the worked case: one coordinate per unknown component flow, a component in a given stream (mol/h of A in the reactor feed, mol/h of B in the product, and so on). A stream is not a single coordinate; it contributes one coordinate per component it carries.

**Underlying equations.** Steady-state balances for each unit and each component: input + generation = output + consumption, with fixed conversions and split fractions.

**The problem.** Given the fresh feed to a process and the performance of each unit (how much of each reactant
converts, and how each separator divides each component), find the flow of every component in every
stream, and check that the specification determines them uniquely.

**Variables.**
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

**Formulation.** **Where the equations come from.** For a unit running at steady state, the familiar balance of
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

**Matrix structure.** `K` is square and sparse. Without the recycle it would be triangular: each unit's outputs depend only
on units upstream, and forward substitution solves it. The recycle adds a single entry above the
diagonal (A_4 appearing in the mixer's row), and that entry is what makes the system simultaneous.
Plant-wide models have thousands of such rows, with sparsity reflecting which units are connected.

**What is computed.** For a design calculation, the solution of K u = r, either directly (equation-oriented simulators) or by
[fixed-point iteration](https://en.wikipedia.org/wiki/Fixed-point_iteration) around each loop, often accelerated (sequential modular simulators such as Aspen
Plus). Before solving, engineers do a degrees-of-freedom analysis: count the unknowns and the
independent equations and make sure the specifications close the gap exactly.

**Why linear algebra is the right tool.** The degrees-of-freedom analysis taught in every process-design course is a rank computation: a unique
solution needs as many independent equations as unknowns, which is a square system with an invertible
matrix. Over-specifying a process gives an inconsistent system, under-specifying it leaves free
variables, and an extra equation that adds no information is a dependent row. Recycle loops, which
make hand calculation tedious, are just off-diagonal entries, and the convergence of the unit-by-unit
calculation is a property of the loop's coefficients.

**Pitfall worth teaching.** Balances can be linearly dependent, and counting them is not the same as counting independent
equations. Around any unit, the total [mass balance](https://en.wikipedia.org/wiki/Mass_balance) is the sum of the component balances, so writing all
of them gives one equation too many. A solver that is handed the redundant set sees a non-square system.
If the numbers come from plant measurements rather than design values, they almost never satisfy the
redundant equation exactly, so the system is inconsistent and has no solution at all. The fix is to
count rank, not equations: keep an independent set for design calculations, and for measured data use
the redundancy deliberately in [data reconciliation](https://en.wikipedia.org/wiki/Data_validation_and_reconciliation), a least-squares adjustment of the measurements so
they satisfy every balance. A related failure is an inert component in the feed with no way out: with
s = 1 for that component, its loop gain is 1, the matrix is singular, and no steady state exists, which
is why plants add a purge stream.

**Terminology map.** How this field's vocabulary reads as linear algebra.

| Domain term | In linear algebra |
|---|---|
| stream | a pipe between units; contributes one unknown per component it carries |
| component balance | one row of the system, for one component around one unit |
| overall (total) balance | the sum of the component balances, a linearly dependent row |
| single-pass conversion | the fraction of the reactant entering the reactor that reacts, a fixed coefficient |
| split fraction | the fraction of a component a separator sends to a given outlet, a fixed coefficient |
| recycle stream | the coupling that turns a triangular system into a genuinely simultaneous one |
| tear stream | the unknown guessed to start the unit-by-unit iteration around a loop |
| sequential modular vs equation-oriented simulation | fixed-point iteration around loops vs solving the whole linear system at once |
| degrees of freedom | unknowns minus independent equations; it must be zero for a unique answer |
| purge stream | a small bleed that keeps an inert component from accumulating in the loop |

**Extensions.** Once conversions depend on temperature, or separations on [vapour–liquid equilibrium](https://en.wikipedia.org/wiki/Vapor%E2%80%93liquid_equilibrium), the balances
become nonlinear and are solved by [Newton's method](https://en.wikipedia.org/wiki/Newton's_method), a sequence of linear systems with this structure.
Data reconciliation is a constrained least-squares problem (compare the regression entry). The same
conservation-at-nodes structure, without reactions, is the traffic-flow entry. With reactions written
out species by species, it is the stoichiometric-matrix entry, and the recycle iteration is the same
Neumann series as the Leontief entry.

---

# Coverage of the written entries

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
| 12 | Electrical engineering | Graph Laplacian; null space and column space | Grounded sparse Cholesky; PCG |
| 42 | Typography / vector graphics | Polynomial space; Bernstein basis; change of basis | de Casteljau subdivision |
| 48 | Cryptography | Vandermonde system over GF(p) | Lagrange interpolation mod p |
| 20 | Statistics | Orthogonal projection onto a column space | Householder QR |
| 41 | Numerical analysis | Polynomial space; change of basis; Vandermonde system | Barycentric Lagrange; Chebyshev basis |
| 47 | Signal processing | Unitary change of basis over ℂ | Direct product; FFT |
| 49 | Storage systems | One linear equation over GF(2); erasures vs errors | XOR reconstruction |
| 51 | Transportation | Underdetermined system; null space; nonnegativity | Gaussian elimination |
| 52 | Chemical engineering | Square system with recycle coupling; redundant rows | Simultaneous solve; recycle iteration |
| 24 | Geodesy / surveying | Rank-deficient least squares; datum as null space | Constrained normal equations |
| 36 | Computer graphics | Homogeneous coordinates; composition of affine maps | Dense 3 × 3 products |
| 38 | Robotics / aerospace | Orthogonal matrices; SO(3) as a group, not a subspace | Small dense products; re-orthonormalization |

**Concepts deliberately covered across the set:** solving `Ax = b` (sparse, dense, ill-posed, over a finite field), least squares (batch and recursive), eigenvalue problems (standard, generalized, dominant-only), the SVD (as optimal approximation, as homogeneous solver, as manifold projection), null spaces and rank, nonnegative matrices and Perron–Frobenius, stochastic matrices, projections, conditioning and preconditioning, tensor products, and linear algebra over a field other than ℝ.

**Not yet represented:** graph Laplacians and spectral methods, Krylov subspace methods on their own terms, optimization duality and linear programming, tensor decompositions beyond the matrix case, randomized numerical linear algebra, and anything from pure mathematics.

---

# Backlog — candidates for expansion

Grouped by what they would add that the seed set does not have.

### Would add: Tier 1 coverage — 2D/3D graphics and scalars beyond the reals

This group exists because the seed set is thin at Tier 1 and silent on vector spaces whose scalars are
not real numbers. Every entry here is small-dimension and needs nothing past a first course, with
the one exception marked below.

*Graphics and small-dimension geometry (index 37, 39–40)*
- **3D viewing and perspective projection** — the model-view-projection chain; why the fourth coordinate exists
- **Barycentric coordinates and triangle rasterization** — a 3×3 solve per pixel; coordinates relative to a basis
- **Color spaces as change of basis** — sRGB ↔ XYZ ↔ LMS as 3×3 basis changes; gamut as a convex cone

*Polynomial and function spaces (index 41–45)*
- **Finite-difference stencils by undetermined coefficients** — derivative weights as the solution of a small
  linear system; differentiation as a linear operator
- **Fourier series as orthogonal projection** — an inner-product space of functions; best approximation
- **Least-squares fitting in a chosen function basis** — the design matrix as a basis choice made explicit

*Complex scalars (index 46–47)*
- **AC circuit analysis with complex impedance** — a 3×3 complex linear system; phasors make a differential
  equation into an algebraic one. *Tier 3, not Tier 1:* the phasor method is a technique for solving
  linear ODEs with sinusoidal forcing, so reading the entry requires the ODE. It stays in this group
  because it is the clearest example of complex scalars doing real work; the small DFT entry, now
  written, is the Tier 1 complex-scalar entry.

*Finite fields (index 50)*
- **CRC checksums** — polynomials over GF(2) modulo a generator

### Would add: graph Laplacians and spectral methods
- **Spectral clustering and image segmentation** — Fiedler vector, normalized cuts, Cheeger inequality
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
- **Matrix completion and recommender systems** — nuclear-norm minimization, the Netflix Prize
- **Word embeddings and latent semantic analysis** — factorization of a co-occurrence matrix
- **Attention in transformers** — QKᵀ as a learned bilinear form; low-rank adapters (LoRA) as explicit rank constraints on weight updates

### Would add: geosciences and geometry
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
   entry in the `tier`, `tier_ceiling`, and `prereq_beyond_la` columns of the index. Under the rule that
   any differential equation means Tier 3, only 2 of the 10 seed entries are Tier 1,
   which is the wrong first impression for a general audience. Remaining work is to write up the Tier 1
   backlog, which is under way: 14 of the 22 written entries are now Tier 1.
3. ~~Decide whether the organizing axis is field or concept.~~ **Decided: field**, for the reasons in
   "Audience and organizing principle" above. The concept coverage table remains as the secondary
   cross-reference. Remaining work: extend the terminology map as entries are written — it
   currently covers 209 terms across the 22 written entries, and the backlog entries most likely to generate
   domain-specific questions (power systems, portfolio optimization, seismic tomography, MDPs) have no
   terminology coverage yet.
