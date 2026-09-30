# Quantum mechanics and quantum computing: when the vector space *is* the physics

### Start here

In quantum mechanics a system's state is not a position and a velocity — it is a list of complex
numbers, one for each configuration the system could be found in. Their sizes determine the
probabilities of each outcome. This is not an approximation or a modelling convenience; the theory is
stated this way.

Two consequences follow immediately. First, adding two valid states gives another valid state — this is
superposition, and it is just the statement that states form a vector space. Second, every measurable
quantity (energy, momentum, spin) corresponds to a matrix, and the values you can actually observe are
that matrix's [eigenvalues](https://en.wikipedia.org/wiki/Eigenvalues_and_eigenvectors). Asking "what energies can this molecule have?" is literally asking for the
eigenvalues of a particular matrix.

The difficulty is size. Combining two systems multiplies their dimensions rather than adding them, so
n quantum bits need a vector with 2^n entries — past about fifty, larger than any computer's memory.
Much of modern quantum chemistry and quantum computing is about exploiting the fact that the states
that actually occur in nature occupy a very thin slice of that enormous space.

**Field:** Physics, quantum chemistry, quantum information  
**Tier:** 3 — the eigenproblem comes from [separating variables](https://en.wikipedia.org/wiki/Separation_of_variables) in the [Schrödinger equation](https://en.wikipedia.org/wiki/Schr%C3%B6dinger_equation), and its meaning is a statement about that [ODE](https://en.wikipedia.org/wiki/Ordinary_differential_equation)'s solutions. On-ramp: [benzene](https://en.wikipedia.org/wiki/Benzene)'s 6×6 [Hückel](https://en.wikipedia.org/wiki/H%C3%BCckel_method) matrix can be diagonalized with no quantum background at all.  
**Scalar field:** C (real [symmetric](https://en.wikipedia.org/wiki/Symmetric_matrix) in the Huckel special case)  
**Vectors:** unit vectors in C^d; for n [qubits](https://en.wikipedia.org/wiki/Qubit) d = 2^n and the space is the [tensor product](https://en.wikipedia.org/wiki/Tensor_product) (C^2)^(x)n. Global phase is unphysical, so states are really points of [CP^(d-1)](https://en.wikipedia.org/wiki/Complex_projective_space). Observables are [Hermitian](https://en.wikipedia.org/wiki/Hermitian_matrix) matrices, which form a REAL vector space of dimension d^2  
**Underlying equations:** Linear Schrödinger equation iħ dψ/dt = H ψ; separation of variables gives the eigenproblem H φ = E φ

### The problem

Two versions. (a) Compute the energy levels and spectra of a molecule. (b) Simulate or design a quantum circuit.

### Variables

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

### Formulation

**Where the equations come from.** The dynamics are the time-dependent Schrödinger equation, a linear [partial differential equation](https://en.wikipedia.org/wiki/Partial_differential_equation) that is first order in time. Written in a finite basis it becomes a system of d linear ordinary differential equations with complex coefficients:

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

so its eigenvectors are exactly those of the ring's [adjacency matrix](https://en.wikipedia.org/wiki/Adjacency_matrix), and its energies are E = α + β μ_k, where μ_k are the adjacency eigenvalues. For a 6-cycle, μ_k = 2 cos(2πk/6), giving 2, 1, 1, −1, −1, −2. Since β < 0 the lowest level is α + 2β, then α + β twice, α − β twice, and α − 2β. Benzene's six π electrons fill the three lowest orbitals, two per orbital. Dropping the orthonormality assumption turns this into a [generalized eigenproblem](https://en.wikipedia.org/wiki/Eigendecomposition_of_a_matrix#Generalized_eigenvalue_problem), H φ = E S φ, where S is the orbital overlap matrix.

**Many particles.** n qubits (or n two-level systems) live in the tensor product (ℂ²)^⊗n, of dimension d = 2ⁿ. Combining systems multiplies dimensions rather than adding them.

### Matrix structure

Hermitian (hence real eigenvalues, orthogonal eigenvectors) and, in a local basis, [sparse](https://en.wikipedia.org/wiki/Sparse_matrix) — Hamiltonians typically couple only nearby sites or orbitals. The dimension is the problem: it grows exponentially in system size.

### What is computed

[Lanczos](https://en.wikipedia.org/wiki/Lanczos_algorithm) and Davidson methods for the lowest few eigenpairs of matrices too large to store; [self-consistent field](https://en.wikipedia.org/wiki/Hartree%E2%80%93Fock_method) iteration (Hartree–Fock, [DFT](https://en.wikipedia.org/wiki/Density_functional_theory)) as a nonlinear eigenproblem solved by repeated dense diagonalization; quantum circuit simulation as a sequence of sparse structured matrix–vector products.

### Why linear algebra is the right tool

It is not a modeling convenience here — the superposition principle *is* linearity, and the postulates of quantum mechanics are stated directly in terms of Hilbert spaces, Hermitian operators, and unitary evolution. This is the entry where the mathematics is not applied to the physics but constitutive of it.

### Pitfall worth teaching

The tensor-product structure means the state space grows as 2ⁿ, which makes exact methods hopeless past ~50 qubits. The response is again low-rank structure: [matrix product states](https://en.wikipedia.org/wiki/Matrix_product_state) and tensor networks exploit the fact that physically relevant states occupy a very thin, low-entanglement slice of the full space. [Low-rank approximation](https://en.wikipedia.org/wiki/Low-rank_approximation) appears here for the same reason it appears in entry 9, in a completely different setting.

### Extensions

Hückel molecular orbital theory, where the Hamiltonian is α I + β A for the molecular graph's adjacency matrix A, so the orbitals are exactly A's eigenvectors and the orbital energies are an affine function of its eigenvalues — the cleanest bridge between graph theory and chemistry. Also: [density matrices](https://en.wikipedia.org/wiki/Density_matrix) as [positive semidefinite](https://en.wikipedia.org/wiki/Definite_matrix) operators, [quantum channels](https://en.wikipedia.org/wiki/Quantum_channel) as completely positive maps, and [variational quantum eigensolvers](https://en.wikipedia.org/wiki/Variational_quantum_eigensolver).

### Terminology

How this field's vocabulary reads as linear algebra.

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

---

[Back to the index](/r/LinearAlgebra/wiki/applications)
