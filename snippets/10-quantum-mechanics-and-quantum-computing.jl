# Julia version of notebooks/10-quantum-mechanics-and-quantum-computing.py: benzene's Hückel
# matrix diagonalized by its ring symmetry, Hückel theory on other molecules, then n qubits in
# (C^2)^⊗n, using the notebook's variable names. Runs as it stands, with only the standard
# library:
#
#     julia 10-quantum-mechanics-and-quantum-computing.jl
#
# Each section is shown on the entry page next to its Python twin. The @assert lines check the
# results: the toy against the numbers worked by hand, the larger parts against properties any
# correct answer must have. Lines ending in #hide run but are not shown.

# --- snippet setup: The benzene Hückel matrix ---
using LinearAlgebra
alpha, beta = 0.0, -1.0       # energies measured from α, in units of |β| (β < 0)
A_benz = Float64[0 1 0 0 0 1
                 1 0 1 0 0 0
                 0 1 0 1 0 0
                 0 0 1 0 1 0
                 0 0 0 1 0 1
                 1 0 0 0 1 0]   # carbon j bonded to j ± 1 (mod 6)
H_benz = alpha * I + beta * A_benz
@assert issymmetric(H_benz)

# --- snippet fourier: Diagonalizing by the ring's symmetry ---
j_site = 0:5
F_benz = exp.(2im * π * j_site * j_site' / 6) / sqrt(6)   # column k+1: φ_k
mu_benz = 2 * cos.(2π * j_site / 6)        # adjacency eigenvalues 2, 1, -1, -2, -1, 1
E_benz = alpha .+ beta * mu_benz
@assert F_benz' * F_benz ≈ I                         # F is unitary
@assert H_benz * F_benz ≈ F_benz * Diagonal(E_benz)  # H φ_k = E_k φ_k for every k
@assert sort(E_benz) ≈ alpha .+ beta * [2, 1, 1, -1, -1, -2]
@show E_benz

# --- snippet real_basis: A real basis for the degenerate pairs ---
c(k) = sqrt(2 / 6) * cos.(2π * k * j_site / 6)   #hide
s(k) = sqrt(2 / 6) * sin.(2π * k * j_site / 6)   #hide
Q_benz = hcat(ones(6) / sqrt(6), c(1), s(1), c(2), s(2), (-1.0) .^ j_site / sqrt(6))
E_real = alpha .+ beta * [2, 1, 1, -1, -1, -2]
@assert Q_benz' * Q_benz ≈ I                          # orthonormal, real
@assert Q_benz' * H_benz * Q_benz ≈ Diagonal(E_real)  # and it diagonalizes H
E_eigh, V_eigh = eigen(Symmetric(H_benz))   # LAPACK's own choice inside each degenerate pair
@assert E_eigh ≈ E_real
P_real = Q_benz[:, 2:3] * Q_benz[:, 2:3]'   # projector onto the α + β level
P_eigh = V_eigh[:, 2:3] * V_eigh[:, 2:3]'
@assert P_real ≈ P_eigh                     # the level is the same plane either way

# --- snippet energy: π energy and delocalization ---
occ_benz = [2, 2, 2, 0, 0, 0]               # six π electrons, two per orbital
E_pi_benz = occ_benz' * E_real              # 6α + 8β
H_eth = alpha * I + beta * [0.0 1.0
                            1.0 0.0]
E_eth = eigvals(Symmetric(H_eth))           # α + β, α − β
E_pi_eth = 2 * E_eth[1]                     # 2α + 2β
deloc_benz = E_pi_benz - 3 * E_pi_eth       # 2β
@assert E_pi_benz ≈ 6alpha + 8beta && deloc_benz ≈ 2beta
@show E_pi_benz deloc_benz

# --- snippet hop: An electron hopping round the ring ---
hbar = 1.0                                  # time in units of ħ/|β|
t_hop = 1.0                                 # the slider
U_hop = V_eigh * Diagonal(exp.(-im * E_eigh * t_hop / hbar)) * V_eigh'
psi0_hop = [1.0, 0, 0, 0, 0, 0]             # electron starts on carbon C0
psi_hop = U_hop * psi0_hop
prob_hop = abs2.(psi_hop)
@assert U_hop' * U_hop ≈ I && sum(prob_hop) ≈ 1
@assert abs2.(U_hop * Q_benz[:, 1]) ≈ fill(1 / 6, 6)   # a stationary state stays put
@show round.(prob_hop, digits=4)

# --- snippet molecules: Hückel matrices from molecular graphs ---
function adjacency(n, edges)
    A = zeros(n, n)
    for (i, j) in edges
        A[i+1, j+1] = A[j+1, i+1] = 1    # 0-based carbon labels, as in the notebook
    end
    return A
end

ring(n) = [(i, mod(i + 1, n)) for i in 0:n-1]
chain(n) = [(i, i + 1) for i in 0:n-2]
molecules = [
    "ethylene" => adjacency(2, chain(2)),
    "butadiene" => adjacency(4, chain(4)),
    "cyclobutadiene" => adjacency(4, ring(4)),
    "hexatriene" => adjacency(6, chain(6)),
    "benzene" => adjacency(6, ring(6)),
    "naphthalene" => adjacency(10, [ring(6); [(4, 6), (6, 7), (7, 8), (8, 9), (9, 5)]]),
]
mol_results = Dict{String,Any}()
for (name, A_mol) in molecules
    n_c = size(A_mol, 1)
    E_mol = alpha .+ beta * reverse(eigvals(Symmetric(A_mol)))   # ascending, since β < 0
    E_pi = 2 * sum(E_mol[1:n_c÷2])                                # n_c electrons, 2 per level
    mol_results[name] = (n=n_c, E=E_mol, E_pi=E_pi, deloc=E_pi - (n_c ÷ 2) * E_pi_eth,
                         gap=E_mol[n_c÷2+1] - E_mol[n_c÷2])
    @assert isapprox(sum(E_mol), tr(alpha * I(n_c) + beta * A_mol), atol=1e-9)
    @assert maximum(abs.(E_mol .- alpha)) <= abs(beta) * maximum(sum(A_mol, dims=1)) + 1e-12
    @assert sort(E_mol .- alpha) ≈ -reverse(sort(E_mol .- alpha))   # pairing
end
@assert mol_results["benzene"].deloc ≈ 2beta
@assert abs(mol_results["cyclobutadiene"].deloc) < 1e-12
for (name, _) in molecules
    r = mol_results[name]
    println(rpad(name, 16), "deloc = ", round(r.deloc / beta, digits=3) + 0.0,
            " β   gap = ", round(r.gap / abs(beta), digits=3), " |β|")
end

# --- snippet polyene: The HOMO–LUMO gap of a polyene chain ---
N_chain = 10                                # the slider: carbons in the chain (even)
E_chain = alpha .+ beta * reverse(eigvals(Symmetric(adjacency(N_chain, chain(N_chain)))))
gap_chain = E_chain[N_chain÷2+1] - E_chain[N_chain÷2]
@assert gap_chain ≈ 4 * abs(beta) * sin(π / (2N_chain + 2))
@assert all(alpha + 2beta - 1e-12 .<= E_chain .<= alpha - 2beta + 1e-12)
@show gap_chain

# --- snippet qubits: Qubit states as Kronecker products ---
ket0 = ComplexF64[1, 0]
X = ComplexF64[0 1
               1 0]
Z = ComplexF64[1 0
               0 -1]
Hgate = ComplexF64[1 1
                   1 -1] / sqrt(2)
CNOT = ComplexF64[1 0 0 0
                  0 1 0 0
                  0 0 0 1
                  0 0 1 0]
psi_prod = kron(ket0, ket0)                     # |00⟩
psi_bell = CNOT * kron(Hgate * ket0, ket0)      # (|00⟩ + |11⟩)/√2
for G in (X, Z, Hgate, CNOT)
    @assert G' * G ≈ I                          # every gate is unitary
end
# Julia reshapes column-major, so this is the transpose of NumPy's reshape: same rank
rank_prod = rank(reshape(psi_prod, 2, 2))
rank_bell = rank(reshape(psi_bell, 2, 2))
@assert psi_bell ≈ [1 / sqrt(2), 0, 0, 1 / sqrt(2)]
@assert rank_prod == 1 && rank_bell == 2        # rank 2: does not factor, so entangled

# --- snippet ising: The transverse-field Ising chain ---
kron_list(ops) = reduce(kron, ops)

function ising_hamiltonian(n, J, h)
    I2 = Matrix{ComplexF64}(I, 2, 2)
    H = zeros(ComplexF64, 2^n, 2^n)
    for i in 0:n-2
        H -= J * kron_list([k in (i, i + 1) ? Z : I2 for k in 0:n-1])
    end
    for i in 0:n-1
        H -= h * kron_list([k == i ? X : I2 for k in 0:n-1])
    end
    return H
end

n_q, J, h_field = 8, 1.0, 1.0               # the sliders
H_ising = ising_hamiltonian(n_q, J, h_field)
E_ising, V_ising = eigen(Hermitian(H_ising))
psi_gs = V_ising[:, 1]
@assert ishermitian(H_ising)                # Hermitian
@assert isapprox(sum(E_ising), real(tr(H_ising)), atol=1e-9)   # eigenvalues sum to the trace
@show E_ising[1]

# --- snippet entanglement: Entanglement from the SVD ---
schmidt(psi, n, cut) = svdvals(reshape(psi, 2^(n - cut), 2^cut))   # column-major: transposed

function entropy_bits(s)
    p = s[s .> 1e-12] .^ 2
    return -sum(p .* log2.(p))
end

cut = n_q ÷ 2
s_gs = schmidt(psi_gs, n_q, cut)
using Random
rng = MersenneTwister(10)                    # a different stream from NumPy's: bounds, not values
psi_rand = randn(rng, ComplexF64, 2^n_q)
psi_rand /= norm(psi_rand)
s_rand = schmidt(psi_rand, n_q, cut)
S_gs, S_rand = entropy_bits(s_gs), entropy_bits(s_rand)
@assert sum(s_gs .^ 2) ≈ 1 && sum(s_rand .^ 2) ≈ 1
@assert S_gs < 1.5 < 2.5 < S_rand <= cut     # ground state: thin slice; random: near maximal
@show S_gs S_rand

# --- snippet quench: Unitary time evolution ---
t_q = range(0, 6, length=121)
psi0_q = zeros(ComplexF64, 2^n_q)
psi0_q[1] = 1                                # |00…0⟩: every spin up along z
c_q = V_ising' * psi0_q                      # expand in stationary states
z_diag = real(diag(sum(kron_list([k == i ? Z : Matrix{ComplexF64}(I, 2, 2) for k in 0:n_q-1])
                       for i in 0:n_q-1))) / n_q
psi_t = V_ising * (exp.(-im * E_ising * t_q' / hbar) .* c_q)   # column per t
mz_t = vec(z_diag' * abs2.(psi_t))           # mean magnetization ⟨Z⟩
S_t = [entropy_bits(schmidt(psi_t[:, k], n_q, cut)) for k in eachindex(t_q)]
U_q = V_ising * Diagonal(exp.(-im * E_ising * t_q[end] / hbar)) * V_ising'
@assert U_q' * U_q ≈ I                                   # unitary
@assert all(norm.(eachcol(psi_t)) .≈ 1)                  # so the norm is conserved
@assert mz_t[1] ≈ 1 && S_t[1] < 1e-9 < S_t[end]
@show S_t[end] mz_t[end]
