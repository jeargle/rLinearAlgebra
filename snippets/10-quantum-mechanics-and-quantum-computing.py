# Python version of notebooks/10-quantum-mechanics-and-quantum-computing.py: benzene's Hückel
# matrix diagonalized by its ring symmetry, Hückel theory on other molecules, then n qubits in
# (C^2)^⊗n, using the notebook's variable names. Runs as it stands, with only numpy:
#
#     python 10-quantum-mechanics-and-quantum-computing.py
#
# Each section is shown on the entry page next to its Julia twin. The assert lines check the
# results: the toy against the numbers worked by hand, the larger parts against properties any
# correct answer must have. Lines ending in #hide run but are not shown.

# --- snippet setup: The benzene Hückel matrix ---
import numpy as np
alpha, beta = 0.0, -1.0       # energies measured from α, in units of |β| (β < 0)
A_benz = np.array([[0, 1, 0, 0, 0, 1],
                   [1, 0, 1, 0, 0, 0],
                   [0, 1, 0, 1, 0, 0],
                   [0, 0, 1, 0, 1, 0],
                   [0, 0, 0, 1, 0, 1],
                   [1, 0, 0, 0, 1, 0]], dtype=float)   # carbon j bonded to j ± 1 (mod 6)
H_benz = alpha * np.eye(6) + beta * A_benz
assert np.allclose(H_benz, H_benz.T)

# --- snippet fourier: Diagonalizing by the ring's symmetry ---
j_site = np.arange(6)
F_benz = np.exp(2j * np.pi * np.outer(j_site, j_site) / 6) / np.sqrt(6)  # column k: φ_k
mu_benz = 2 * np.cos(2 * np.pi * j_site / 6)       # adjacency eigenvalues 2, 1, -1, -2, -1, 1
E_benz = alpha + beta * mu_benz
assert np.allclose(F_benz.conj().T @ F_benz, np.eye(6))     # F is unitary
assert np.allclose(H_benz @ F_benz, F_benz * E_benz)        # H φ_k = E_k φ_k for every k
assert np.allclose(np.sort(E_benz), alpha + beta * np.array([2, 1, 1, -1, -1, -2]))
print("E_benz =", E_benz)

# --- snippet real_basis: A real basis for the degenerate pairs ---
_c = lambda k: np.sqrt(2 / 6) * np.cos(2 * np.pi * k * j_site / 6)   #hide
_s = lambda k: np.sqrt(2 / 6) * np.sin(2 * np.pi * k * j_site / 6)   #hide
Q_benz = np.column_stack([np.ones(6) / np.sqrt(6), _c(1), _s(1),
                          _c(2), _s(2), (-1.0) ** j_site / np.sqrt(6)])
E_real = alpha + beta * np.array([2, 1, 1, -1, -1, -2])
assert np.allclose(Q_benz.T @ Q_benz, np.eye(6))                  # orthonormal, real
assert np.allclose(Q_benz.T @ H_benz @ Q_benz, np.diag(E_real))   # and it diagonalizes H
E_eigh, V_eigh = np.linalg.eigh(H_benz)        # LAPACK's own choice inside each degenerate pair
assert np.allclose(E_eigh, E_real)
P_real = Q_benz[:, 1:3] @ Q_benz[:, 1:3].T     # projector onto the α + β level
P_eigh = V_eigh[:, 1:3] @ V_eigh[:, 1:3].T
assert np.allclose(P_real, P_eigh)             # the level is the same plane either way

# --- snippet energy: π energy and delocalization ---
occ_benz = np.array([2, 2, 2, 0, 0, 0])        # six π electrons, two per orbital
E_pi_benz = occ_benz @ E_real                  # 6α + 8β
H_eth = alpha * np.eye(2) + beta * np.array([[0.0, 1.0],
                                             [1.0, 0.0]])
E_eth = np.linalg.eigvalsh(H_eth)              # α + β, α − β
E_pi_eth = 2 * E_eth[0]                        # 2α + 2β
deloc_benz = E_pi_benz - 3 * E_pi_eth          # 2β
assert np.isclose(E_pi_benz, 6 * alpha + 8 * beta) and np.isclose(deloc_benz, 2 * beta)
print("E_pi_benz =", E_pi_benz, " deloc_benz =", deloc_benz)

# --- snippet hop: An electron hopping round the ring ---
hbar = 1.0                                     # time in units of ħ/|β|
t_hop = 1.0                                    # the slider
U_hop = V_eigh @ np.diag(np.exp(-1j * E_eigh * t_hop / hbar)) @ V_eigh.T
psi0_hop = np.eye(6)[0]                        # electron starts on carbon C0
psi_hop = U_hop @ psi0_hop
prob_hop = np.abs(psi_hop) ** 2
assert np.allclose(U_hop.conj().T @ U_hop, np.eye(6)) and np.isclose(prob_hop.sum(), 1)
assert np.allclose(np.abs(U_hop @ Q_benz[:, 0]) ** 2, 1 / 6)   # a stationary state stays put
print("prob_hop =", prob_hop.round(4))

# --- snippet molecules: Hückel matrices from molecular graphs ---
def adjacency(n, edges):
    A = np.zeros((n, n))
    for i, j in edges:
        A[i, j] = A[j, i] = 1
    return A

ring = lambda n: [(i, (i + 1) % n) for i in range(n)]
chain = lambda n: [(i, i + 1) for i in range(n - 1)]
molecules = {
    "ethylene": adjacency(2, chain(2)),
    "butadiene": adjacency(4, chain(4)),
    "cyclobutadiene": adjacency(4, ring(4)),
    "hexatriene": adjacency(6, chain(6)),
    "benzene": adjacency(6, ring(6)),
    "naphthalene": adjacency(10, ring(6) + [(4, 6), (6, 7), (7, 8), (8, 9), (9, 5)]),
}
mol_results = {}
for name, A_mol in molecules.items():
    n_c = len(A_mol)
    E_mol = alpha + beta * np.linalg.eigvalsh(A_mol)[::-1]          # ascending, since β < 0
    E_pi = 2 * E_mol[: n_c // 2].sum()                              # n_c electrons, 2 per level
    mol_results[name] = dict(n=n_c, E=E_mol, E_pi=E_pi,
                             deloc=E_pi - (n_c // 2) * E_pi_eth,
                             gap=E_mol[n_c // 2] - E_mol[n_c // 2 - 1])
    assert np.isclose(E_mol.sum(), np.trace(alpha * np.eye(n_c) + beta * A_mol))
    assert np.abs(E_mol - alpha).max() <= abs(beta) * A_mol.sum(axis=0).max() + 1e-12
    assert np.allclose(np.sort(E_mol - alpha), -np.sort(E_mol - alpha)[::-1])  # pairing
assert np.isclose(mol_results["benzene"]["deloc"], 2 * beta)
assert np.isclose(mol_results["cyclobutadiene"]["deloc"], 0)
for name, r in mol_results.items():
    print(f"{name:15s} deloc = {round(r['deloc'] / beta, 3) + 0.0:.3f} β   gap = {r['gap'] / abs(beta):.3f} |β|")

# --- snippet polyene: The HOMO–LUMO gap of a polyene chain ---
N_chain = 10                                   # the slider: carbons in the chain (even)
E_chain = alpha + beta * np.linalg.eigvalsh(adjacency(N_chain, chain(N_chain)))[::-1]
gap_chain = E_chain[N_chain // 2] - E_chain[N_chain // 2 - 1]
assert np.isclose(gap_chain, 4 * abs(beta) * np.sin(np.pi / (2 * N_chain + 2)))
assert (E_chain >= alpha + 2 * beta - 1e-12).all() and (E_chain <= alpha - 2 * beta + 1e-12).all()
print("gap_chain =", gap_chain)

# --- snippet qubits: Qubit states as Kronecker products ---
ket0 = np.array([1, 0], dtype=complex)
X = np.array([[0, 1],
              [1, 0]], dtype=complex)
Z = np.array([[1, 0],
              [0, -1]], dtype=complex)
Hgate = np.array([[1, 1],
                  [1, -1]], dtype=complex) / np.sqrt(2)
CNOT = np.array([[1, 0, 0, 0],
                 [0, 1, 0, 0],
                 [0, 0, 0, 1],
                 [0, 0, 1, 0]], dtype=complex)
psi_prod = np.kron(ket0, ket0)                       # |00⟩
psi_bell = CNOT @ np.kron(Hgate @ ket0, ket0)        # (|00⟩ + |11⟩)/√2
for G in (X, Z, Hgate, CNOT):
    assert np.allclose(G.conj().T @ G, np.eye(len(G)))   # every gate is unitary
rank_prod = np.linalg.matrix_rank(psi_prod.reshape(2, 2))
rank_bell = np.linalg.matrix_rank(psi_bell.reshape(2, 2))
assert np.allclose(psi_bell, [1 / np.sqrt(2), 0, 0, 1 / np.sqrt(2)])
assert rank_prod == 1 and rank_bell == 2             # rank 2: does not factor, so entangled

# --- snippet ising: The transverse-field Ising chain ---
from functools import reduce
def kron_list(ops):
    return reduce(np.kron, ops)

def ising_hamiltonian(n, J, h):
    I2 = np.eye(2)
    H = np.zeros((2 ** n, 2 ** n), dtype=complex)
    for i in range(n - 1):
        H -= J * kron_list([Z if k in (i, i + 1) else I2 for k in range(n)])
    for i in range(n):
        H -= h * kron_list([X if k == i else I2 for k in range(n)])
    return H

n_q, J, h_field = 8, 1.0, 1.0                  # the sliders
H_ising = ising_hamiltonian(n_q, J, h_field)
E_ising, V_ising = np.linalg.eigh(H_ising)
psi_gs = V_ising[:, 0]
assert np.allclose(H_ising, H_ising.conj().T)            # Hermitian
assert np.isclose(E_ising.sum(), np.trace(H_ising).real) # eigenvalues sum to the trace
print("ground-state energy =", E_ising[0])

# --- snippet entanglement: Entanglement from the SVD ---
def schmidt(psi, n, cut):
    return np.linalg.svd(psi.reshape(2 ** cut, 2 ** (n - cut)), compute_uv=False)

def entropy_bits(s):
    p = s[s > 1e-12] ** 2
    return float(-(p * np.log2(p)).sum())

cut = n_q // 2
s_gs = schmidt(psi_gs, n_q, cut)
rng = np.random.default_rng(10)
psi_rand = rng.normal(size=2 ** n_q) + 1j * rng.normal(size=2 ** n_q)
psi_rand /= np.linalg.norm(psi_rand)
s_rand = schmidt(psi_rand, n_q, cut)
S_gs, S_rand = entropy_bits(s_gs), entropy_bits(s_rand)
assert np.isclose((s_gs ** 2).sum(), 1) and np.isclose((s_rand ** 2).sum(), 1)
assert S_gs < 1.5 < 2.5 < S_rand <= cut        # ground state: thin slice; random: near maximal
print("S_gs =", S_gs, " S_rand =", S_rand)

# --- snippet quench: Unitary time evolution ---
t_q = np.linspace(0, 6, 121)
psi0_q = np.zeros(2 ** n_q, dtype=complex)
psi0_q[0] = 1                                  # |00…0⟩: every spin up along z
c_q = V_ising.conj().T @ psi0_q                # expand in stationary states
z_diag = np.diag(sum(kron_list([Z if k == i else np.eye(2) for k in range(n_q)])
                     for i in range(n_q))).real / n_q
psi_t = V_ising @ (np.exp(-1j * np.outer(E_ising, t_q) / hbar) * c_q[:, None])  # column per t
mz_t = z_diag @ np.abs(psi_t) ** 2             # mean magnetization ⟨Z⟩
S_t = np.array([entropy_bits(schmidt(psi_t[:, k], n_q, cut)) for k in range(len(t_q))])
U_q = V_ising @ np.diag(np.exp(-1j * E_ising * t_q[-1] / hbar)) @ V_ising.conj().T
assert np.allclose(U_q.conj().T @ U_q, np.eye(2 ** n_q))        # unitary
assert np.allclose(np.linalg.norm(psi_t, axis=0), 1)            # so the norm is conserved
assert np.isclose(mz_t[0], 1) and S_t[0] < 1e-9 < S_t[-1]
print("S_t[-1] =", S_t[-1], " mz_t[-1] =", mz_t[-1])
