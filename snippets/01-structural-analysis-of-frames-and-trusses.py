# Python version of notebooks/01-structural-analysis-of-frames-and-trusses.py: a three-bar
# triangle truss worked by hand, then a 12-panel Pratt truss bridge, using the notebook's
# variable names. Runs as it stands, with only numpy:
#
#     python 01-structural-analysis-of-frames-and-trusses.py
#
# Each section is shown on the entry page next to its Julia twin. The assert lines check the
# results: the toy against the numbers worked by hand, the bridge against properties any correct
# analysis must have (symmetry, positive definiteness, equilibrium, M-orthogonal modes).
# Units are SI throughout: metres, newtons, kilograms. Lines ending in #hide run but are not shown.

# --- snippet setup: The toy truss ---
import numpy as np
names_toy = ["P", "Q", "R"]
nodes_toy = np.array([[0.0, 0.0],      # P: pinned support
                      [8.0, 0.0],      # Q: roller support (free to slide in x)
                      [4.0, 3.0]])     # R: loaded joint
bars_toy = [(0, 1), (0, 2), (1, 2)]    # PQ, PR, QR
EA_toy = 4.0e7                         # N: steel, E = 200 GPa, A = 200 mm²
f_toy = np.zeros(6)                    # DOF order: P_x, P_y, Q_x, Q_y, R_x, R_y
f_toy[5] = -60e3                       # 60 kN down at R

# --- snippet element: One bar's stiffness matrix ---
def element_stiffness(xy_i, xy_j, EA):
    """4 × 4 stiffness of one bar from node i to node j, its length, and g with δ = g · u_e."""
    d = np.asarray(xy_j, float) - np.asarray(xy_i, float)
    L = np.hypot(d[0], d[1])
    c, s = d / L                       # direction cosines
    g = np.array([-c, -s, c, s])       # elongation δ = c (u_jx − u_ix) + s (u_jy − u_iy)
    return (EA / L) * np.outer(g, g), L, g

k_PR, L_PR, g_PR = element_stiffness(nodes_toy[0], nodes_toy[2], EA_toy)
assert np.isclose(L_PR, 5.0)
assert np.allclose(k_PR / 1e6, [[ 5.12,  3.84, -5.12, -3.84],
                                [ 3.84,  2.88, -3.84, -2.88],
                                [-5.12, -3.84,  5.12,  3.84],
                                [-3.84, -2.88,  3.84,  2.88]])   # MN/m

# --- snippet assemble: Assemble K ---
def dofs(i, j):
    """Global DOF indices of a bar's two ends: x and y of node i, then of node j."""
    return [2 * i, 2 * i + 1, 2 * j, 2 * j + 1]

def assemble(nodes, bars, EA):
    """Global stiffness matrix: add each bar's 4 × 4 block at its four DOFs."""
    EA = np.broadcast_to(EA, (len(bars),))
    K = np.zeros((2 * len(nodes), 2 * len(nodes)))
    for b, (i, j) in enumerate(bars):
        k_e, _, _ = element_stiffness(nodes[i], nodes[j], EA[b])
        K[np.ix_(dofs(i, j), dofs(i, j))] += k_e
    return K

K_toy = assemble(nodes_toy, bars_toy, EA_toy)
assert np.allclose(K_toy, K_toy.T)
print("K_toy (MN/m) =", K_toy / 1e6, sep="\n")

# --- snippet solve: Apply supports and solve K u = f ---
fixed_toy = [0, 1, 3]                  # P_x, P_y (pin) and Q_y (roller)
free_toy = [2, 4, 5]                   # Q_x, R_x, R_y
K_ff_toy = K_toy[np.ix_(free_toy, free_toy)]
assert np.allclose(K_ff_toy / 1e6, [[10.12, -5.12, 3.84],
                                    [-5.12, 10.24, 0.00],
                                    [ 3.84,  0.00, 5.76]])
u_toy = np.zeros(6)
u_toy[free_toy] = np.linalg.solve(K_ff_toy, f_toy[free_toy])
assert np.allclose(u_toy[free_toy] * 1e3, [8.0, 4.0, -15.75])   # mm
print("u_toy (mm) =", u_toy * 1e3)

# --- snippet forces: Bar forces, reactions, equilibrium ---
def bar_forces(nodes, bars, EA, u):
    """Axial force in each bar, N = (EA / L) δ: positive in tension."""
    EA = np.broadcast_to(EA, (len(bars),))
    N = np.zeros(len(bars))
    for b, (i, j) in enumerate(bars):
        _, L, g = element_stiffness(nodes[i], nodes[j], 1.0)
        N[b] = EA[b] / L * (g @ u[dofs(i, j)])
    return N

N_toy = bar_forces(nodes_toy, bars_toy, EA_toy, u_toy)
r_toy = K_toy @ u_toy - f_toy          # support reactions; zero at free DOFs
assert np.allclose(N_toy / 1e3, [40.0, -50.0, -50.0])           # kN: PQ tension, PR and QR compression
assert np.allclose(r_toy / 1e3, [0, 30, 0, 30, 0, 0], atol=1e-9)
assert np.isclose((r_toy + f_toy)[1::2].sum(), 0)               # vertical forces balance
print("N_toy (kN) =", N_toy / 1e3)

# --- snippet mechanism: Too few supports: K is singular ---
lam_toy = np.linalg.eigvalsh(K_toy)    # no supports at all
assert np.sum(lam_toy < 1e-6 * lam_toy.max()) == 3              # two translations, one rotation
rotation_toy = np.column_stack([-nodes_toy[:, 1], nodes_toy[:, 0]]).ravel()   # spin about P
assert np.allclose(K_toy @ rotation_toy, 0, atol=1e-6)
free_pin = [2, 3, 4, 5]                # pin at P only, roller removed
lam_pin = np.linalg.eigvalsh(K_toy[np.ix_(free_pin, free_pin)])
assert np.sum(lam_pin < 1e-6 * lam_pin.max()) == 1               # the truss can still spin about P
print("eigenvalues with no supports (MN/m):", np.round(lam_toy / 1e6, 4))

# --- snippet bridge: A Pratt truss bridge ---
def pratt_truss(n_panels, panel, height):
    """Nodes numbered along the span (bottom, then top, panel by panel) and the bars."""
    nodes, bot, top = [], {}, {}
    for k in range(n_panels + 1):
        bot[k] = len(nodes)
        nodes.append((k * panel, 0.0))
        if 0 < k < n_panels:
            top[k] = len(nodes)
            nodes.append((k * panel, height))
    half = n_panels // 2
    members = [(bot[k], bot[k + 1], "bottom chord") for k in range(n_panels)]
    members += [(top[k], top[k + 1], "top chord") for k in range(1, n_panels - 1)]
    members += [(bot[k], top[k], "vertical") for k in range(1, n_panels)]
    members += [(bot[0], top[1], "end post"), (bot[n_panels], top[n_panels - 1], "end post")]
    members += [(top[k], bot[k + 1], "diagonal") for k in range(1, half)]
    members += [(top[k], bot[k - 1], "diagonal") for k in range(half + 1, n_panels)]
    bars = [(i, j) for i, j, _ in members]
    kinds = [kind for _, _, kind in members]
    return np.array(nodes), bars, kinds, bot, top

n_panels, panel, height = 12, 6.0, 8.0        # 72 m span, 8 m deep
E_steel, rho_steel, g_grav = 200e9, 7850.0, 9.81
area_by_kind = {"bottom chord": 0.024, "top chord": 0.026, "end post": 0.026,
                "vertical": 0.010, "diagonal": 0.014}  # m²
w_deck = 40e3                                 # N/m carried by this truss: deck plus traffic
m_deck = 2500.0                               # kg/m of deck mass carried by this truss
nodes_br, bars_br, kinds_br, bot_br, top_br = pratt_truss(n_panels, panel, height)
span = n_panels * panel
assert len(nodes_br) == 24 and len(bars_br) == 45
assert len(bars_br) + 3 == 2 * len(nodes_br)  # statically determinate: bars + reactions = 2 × joints

# --- snippet stiffness: Assemble the sparse stiffness matrix ---
A_br = np.array([area_by_kind[kind] for kind in kinds_br])
EA_br = E_steel * A_br
K_br = assemble(nodes_br, bars_br, EA_br)
fixed_br = [2 * bot_br[0], 2 * bot_br[0] + 1, 2 * bot_br[n_panels] + 1]   # pin left, roller right
free_br = [d for d in range(K_br.shape[0]) if d not in fixed_br]
K_ff = K_br[np.ix_(free_br, free_br)]
L_K = np.linalg.cholesky(K_ff)                # succeeds only if K_ff is positive definite
assert np.allclose(K_ff, K_ff.T)
nnz_fraction = np.count_nonzero(K_ff) / K_ff.size
bandwidth = max(abs(i - j) for i, j in zip(*np.nonzero(K_ff)))
assert nnz_fraction < 0.15
print(f"{len(free_br)} free DOFs, {100 * nnz_fraction:.1f}% nonzero, half-bandwidth {bandwidth}")

# --- snippet static: Static solve by Cholesky ---
L_bar = np.array([element_stiffness(nodes_br[i], nodes_br[j], 1.0)[1] for i, j in bars_br])
m_bar = rho_steel * A_br * L_bar              # kg per bar
f_br = np.zeros(K_br.shape[0])
f_br[[2 * bot_br[k] + 1 for k in range(1, n_panels)]] -= w_deck * panel   # deck load, interior bottom joints
ends_y = np.array([[2 * i + 1, 2 * j + 1] for i, j in bars_br])
np.add.at(f_br, ends_y, -m_bar[:, None] * g_grav / 2)   # half of each bar's weight at each end
z_br = np.linalg.solve(L_K, f_br[free_br])    # forward substitution:  L z = f
u_br = np.zeros(K_br.shape[0])
u_br[free_br] = np.linalg.solve(L_K.T, z_br)  # back substitution:     Lᵀ u = z
residual_br = np.linalg.norm(K_ff @ u_br[free_br] - f_br[free_br]) / np.linalg.norm(f_br)
N_br = bar_forces(nodes_br, bars_br, EA_br, u_br)
sigma_br = N_br / A_br                        # Pa
r_br = K_br @ u_br - f_br                     # reactions
assert residual_br < 1e-10
assert np.isclose(r_br[1::2].sum(), -f_br[1::2].sum())    # supports carry the whole load
mid_top = bars_br.index((top_br[n_panels // 2 - 1], top_br[n_panels // 2]))
x_mid = n_panels // 2 * panel                 # beam check: N_top = −M / h at midspan
R_left = -sum(f_br[2 * n + 1] * (span - nodes_br[n, 0]) for n in range(len(nodes_br))) / span
M_mid = R_left * x_mid + sum(f_br[2 * n + 1] * (x_mid - nodes_br[n, 0])
                             for n in range(len(nodes_br)) if nodes_br[n, 0] < x_mid)
assert np.isclose(N_br[mid_top], -M_mid / height)
print(f"midspan deflection {-u_br[1::2].min() * 1e3:.1f} mm = span/{span / -u_br[1::2].min():.0f}")
print(f"stress from {sigma_br.min() / 1e6:.0f} to {sigma_br.max() / 1e6:.0f} MPa")

# --- snippet modes: Natural frequencies: K φ = λ M φ ---
def assemble_mass(nodes, bars, m_bar):
    """Consistent mass matrix of the bars: (m / 6) [2 1; 1 2] in each direction."""
    M = np.zeros((2 * len(nodes), 2 * len(nodes)))
    for b, (i, j) in enumerate(bars):
        M[np.ix_(dofs(i, j), dofs(i, j))] += m_bar[b] / 6 * np.kron([[2, 1], [1, 2]], np.eye(2))
    return M

M_br = assemble_mass(nodes_br, bars_br, m_bar)
deck_dofs = np.array([[2 * bot_br[k], 2 * bot_br[k] + 1] for k in range(n_panels + 1)])
deck_mass = m_deck * panel * np.array([0.5 if k in (0, n_panels) else 1.0 for k in range(n_panels + 1)])
M_br[deck_dofs, deck_dofs] += deck_mass[:, None]   # deck mass lumped at the bottom joints, x and y
M_ff = M_br[np.ix_(free_br, free_br)]
L_M = np.linalg.cholesky(M_ff)                # M = L_M L_Mᵀ
Li_M = np.linalg.inv(L_M)
C_br = Li_M @ K_ff @ Li_M.T                   # K φ = λ M φ  becomes  C y = λ y,  φ = L_M⁻ᵀ y
lam_br, y_br = np.linalg.eigh(C_br)
phi_br = Li_M.T @ y_br
freq_hz = np.sqrt(lam_br) / (2 * np.pi)
assert np.all(lam_br > 0) and np.all(np.diff(lam_br) >= 0)
assert np.allclose(phi_br.T @ M_ff @ phi_br, np.eye(len(free_br)), atol=1e-9)
assert np.allclose(K_ff @ phi_br, M_ff @ phi_br * lam_br, rtol=1e-8, atol=1e-6 * lam_br.max())
assert 1.0 < freq_hz[0] < 3.0
print("lowest natural frequencies (Hz):", np.round(freq_hz[:6], 2))
