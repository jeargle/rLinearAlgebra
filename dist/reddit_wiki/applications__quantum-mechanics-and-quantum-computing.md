# Quantum mechanics and quantum computing: when the vector space *is* the physics

### Start here

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

**Field:** Physics, quantum chemistry, quantum information  
**Tier:** 2 — as posed (benzene's 6×6 Hückel eigenproblem). The full quantum formalism is Tier 3.  
**Scalar field:** C (real symmetric in the Huckel special case)  
**Vectors:** unit vectors in C^d; for n qubits d = 2^n and the space is the tensor product (C^2)^(x)n. Global phase is unphysical, so states are really points of CP^(d-1). Observables are Hermitian matrices, which form a REAL vector space of dimension d^2

### The problem

Two versions. (a) Compute the energy levels and spectra of a molecule. (b) Simulate or design a quantum circuit.

### Formulation

A state is a unit vector in a complex Hilbert space. Observables are Hermitian operators; measurable values are their eigenvalues. The time-independent Schrödinger equation is an eigenproblem

```
H ψ = E ψ
```

Quantum gates are unitary matrices, and composite systems combine by tensor product, so `n` qubits live in `C^{2ⁿ}`.

### Matrix structure

Hermitian (hence real eigenvalues, orthogonal eigenvectors) and, in a local basis, sparse — Hamiltonians typically couple only nearby sites or orbitals. The dimension is the problem: it grows exponentially in system size.

### What is computed

Lanczos and Davidson methods for the lowest few eigenpairs of matrices too large to store; self-consistent field iteration (Hartree–Fock, DFT) as a nonlinear eigenproblem solved by repeated dense diagonalization; quantum circuit simulation as a sequence of sparse structured matrix–vector products.

### Why linear algebra is the right tool

It is not a modeling convenience here — the superposition principle *is* linearity, and the postulates of quantum mechanics are stated directly in terms of Hilbert spaces, Hermitian operators, and unitary evolution. This is the entry where the mathematics is not applied to the physics but constitutive of it.

### Pitfall worth teaching

The tensor-product structure means the state space grows as 2ⁿ, which makes exact methods hopeless past ~50 qubits. The response is again low-rank structure: matrix product states and tensor networks exploit the fact that physically relevant states occupy a very thin, low-entanglement slice of the full space. Low-rank approximation appears here for the same reason it appears in entry 9, in a completely different setting.

### Extensions

Hückel molecular orbital theory, where the Hamiltonian is literally the adjacency matrix of the molecular graph and orbital energies are its eigenvalues — the cleanest bridge between graph theory and chemistry. Also: density matrices as positive semidefinite operators, quantum channels as completely positive maps, and variational quantum eigensolvers.

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
