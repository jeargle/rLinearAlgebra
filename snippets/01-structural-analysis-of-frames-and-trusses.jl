# Julia version of notebooks/01-structural-analysis-of-frames-and-trusses.py: a three-bar
# triangle truss worked by hand, then a 12-panel Pratt truss bridge, using the notebook's
# variable names. Runs as it stands, with only the LinearAlgebra standard library:
#
#     julia 01-structural-analysis-of-frames-and-trusses.jl
#
# Each section is shown on the entry page next to its Python twin. The @assert lines check the
# results: the toy against the numbers worked by hand, the bridge against properties any correct
# analysis must have (symmetry, positive definiteness, equilibrium, M-orthogonal modes). Julia
# counts from 1, so node and DOF indices are one larger than in the Python file (panel numbers
# k, the keys of bot_br and top_br, still start at 0). Units are SI: metres, newtons, kilograms.
# Lines ending in #hide run but are not shown.

# --- snippet setup: The toy truss ---
using LinearAlgebra
names_toy = ["P", "Q", "R"]
nodes_toy = [0.0 0.0      # P: pinned support
             8.0 0.0      # Q: roller support (free to slide in x)
             4.0 3.0]     # R: loaded joint
bars_toy = [(1, 2), (1, 3), (2, 3)]    # PQ, PR, QR
EA_toy = 4.0e7                         # N: steel, E = 200 GPa, A = 200 mm²
f_toy = zeros(6)                       # DOF order: P_x, P_y, Q_x, Q_y, R_x, R_y
f_toy[6] = -60e3                       # 60 kN down at R

# --- snippet element: One bar's stiffness matrix ---
"4 × 4 stiffness of one bar from node i to node j, its length, and g with δ = g ⋅ u_e."
function element_stiffness(xy_i, xy_j, EA)
    d = xy_j .- xy_i
    L = hypot(d[1], d[2])
    c, s = d ./ L                      # direction cosines
    g = [-c, -s, c, s]                 # elongation δ = c (u_jx − u_ix) + s (u_jy − u_iy)
    return (EA / L) * g * g', L, g
end

k_PR, L_PR, g_PR = element_stiffness(nodes_toy[1, :], nodes_toy[3, :], EA_toy)
@assert L_PR ≈ 5.0
@assert k_PR / 1e6 ≈ [ 5.12  3.84 -5.12 -3.84
                       3.84  2.88 -3.84 -2.88
                      -5.12 -3.84  5.12  3.84
                      -3.84 -2.88  3.84  2.88]   # MN/m

# --- snippet assemble: Assemble K ---
"Global DOF indices of a bar's two ends: x and y of node i, then of node j."
dofs(i, j) = [2i - 1, 2i, 2j - 1, 2j]

"Global stiffness matrix: add each bar's 4 × 4 block at its four DOFs."
function assemble(nodes, bars, EA)
    EA = EA isa Number ? fill(EA, length(bars)) : EA
    K = zeros(2 * size(nodes, 1), 2 * size(nodes, 1))
    for (b, (i, j)) in enumerate(bars)
        k_e, _, _ = element_stiffness(nodes[i, :], nodes[j, :], EA[b])
        K[dofs(i, j), dofs(i, j)] .+= k_e
    end
    return K
end

K_toy = assemble(nodes_toy, bars_toy, EA_toy)
@assert issymmetric(K_toy)
println("K_toy (MN/m) ="); display(K_toy / 1e6)

# --- snippet solve: Apply supports and solve K u = f ---
fixed_toy = [1, 2, 4]                  # P_x, P_y (pin) and Q_y (roller)
free_toy = [3, 5, 6]                   # Q_x, R_x, R_y
K_ff_toy = K_toy[free_toy, free_toy]
@assert K_ff_toy / 1e6 ≈ [10.12 -5.12 3.84
                          -5.12 10.24 0.00
                           3.84  0.00 5.76]
u_toy = zeros(6)
u_toy[free_toy] = K_ff_toy \ f_toy[free_toy]
@assert u_toy[free_toy] * 1e3 ≈ [8.0, 4.0, -15.75]       # mm
@show u_toy * 1e3

# --- snippet forces: Bar forces, reactions, equilibrium ---
"Axial force in each bar, N = (EA / L) δ: positive in tension."
function bar_forces(nodes, bars, EA, u)
    EA = EA isa Number ? fill(EA, length(bars)) : EA
    N = zeros(length(bars))
    for (b, (i, j)) in enumerate(bars)
        _, L, g = element_stiffness(nodes[i, :], nodes[j, :], 1.0)
        N[b] = EA[b] / L * dot(g, u[dofs(i, j)])
    end
    return N
end

N_toy = bar_forces(nodes_toy, bars_toy, EA_toy, u_toy)
r_toy = K_toy * u_toy - f_toy          # support reactions; zero at free DOFs
@assert N_toy / 1e3 ≈ [40.0, -50.0, -50.0]                # kN: PQ tension, PR and QR compression
@assert isapprox(r_toy / 1e3, [0, 30, 0, 30, 0, 0], atol=1e-9)
@assert isapprox(sum((r_toy + f_toy)[2:2:end]), 0, atol=1e-6)   # vertical forces balance
@show N_toy / 1e3

# --- snippet mechanism: Too few supports: K is singular ---
lam_toy = eigvals(Symmetric(K_toy))    # no supports at all
@assert count(<(1e-6 * maximum(lam_toy)), lam_toy) == 3  # two translations, one rotation
rotation_toy = vec([-nodes_toy[:, 2] nodes_toy[:, 1]]')   # spin about P
@assert isapprox(K_toy * rotation_toy, zeros(6), atol=1e-6)
free_pin = [3, 4, 5, 6]                # pin at P only, roller removed
lam_pin = eigvals(Symmetric(K_toy[free_pin, free_pin]))
@assert count(<(1e-6 * maximum(lam_pin)), lam_pin) == 1  # the truss can still spin about P
println("eigenvalues with no supports (MN/m): ", round.(lam_toy / 1e6, digits=4))

# --- snippet bridge: A Pratt truss bridge ---
"Nodes numbered along the span (bottom, then top, panel by panel) and the bars."
function pratt_truss(n_panels, panel, height)
    nodes, bot, top = Vector{Vector{Float64}}(), Dict{Int,Int}(), Dict{Int,Int}()
    for k in 0:n_panels
        push!(nodes, [k * panel, 0.0]); bot[k] = length(nodes)
        if 0 < k < n_panels
            push!(nodes, [k * panel, height]); top[k] = length(nodes)
        end
    end
    half = n_panels ÷ 2
    members = [(bot[k], bot[k + 1], "bottom chord") for k in 0:n_panels-1]
    append!(members, [(top[k], top[k + 1], "top chord") for k in 1:n_panels-2])
    append!(members, [(bot[k], top[k], "vertical") for k in 1:n_panels-1])
    append!(members, [(bot[0], top[1], "end post"), (bot[n_panels], top[n_panels - 1], "end post")])
    append!(members, [(top[k], bot[k + 1], "diagonal") for k in 1:half-1])
    append!(members, [(top[k], bot[k - 1], "diagonal") for k in half+1:n_panels-1])
    bars = [(i, j) for (i, j, _) in members]
    kinds = [kind for (_, _, kind) in members]
    return permutedims(reduce(hcat, nodes)), bars, kinds, bot, top
end

n_panels, panel, height = 12, 6.0, 8.0        # 72 m span, 8 m deep
E_steel, rho_steel, g_grav = 200e9, 7850.0, 9.81
area_by_kind = Dict("bottom chord" => 0.024, "top chord" => 0.026, "end post" => 0.026,
                    "vertical" => 0.010, "diagonal" => 0.014)    # m²
w_deck = 40e3                                 # N/m carried by this truss: deck plus traffic
m_deck = 2500.0                               # kg/m of deck mass carried by this truss
nodes_br, bars_br, kinds_br, bot_br, top_br = pratt_truss(n_panels, panel, height)
span = n_panels * panel
@assert size(nodes_br, 1) == 24 && length(bars_br) == 45
@assert length(bars_br) + 3 == 2 * size(nodes_br, 1)  # statically determinate: bars + reactions = 2 × joints

# --- snippet stiffness: Assemble the sparse stiffness matrix ---
A_br = [area_by_kind[kind] for kind in kinds_br]
EA_br = E_steel * A_br
K_br = assemble(nodes_br, bars_br, EA_br)
fixed_br = [2 * bot_br[0] - 1, 2 * bot_br[0], 2 * bot_br[n_panels]]   # pin left, roller right
free_br = setdiff(1:size(K_br, 1), fixed_br)
K_ff = K_br[free_br, free_br]
L_K = cholesky(Symmetric(K_ff)).L             # succeeds only if K_ff is positive definite
@assert issymmetric(K_ff)
nnz_fraction = count(!iszero, K_ff) / length(K_ff)
bandwidth = maximum(abs(I[1] - I[2]) for I in findall(!iszero, K_ff))
@assert nnz_fraction < 0.15
println("$(length(free_br)) free DOFs, $(round(100 * nnz_fraction, digits=1))% nonzero, half-bandwidth $bandwidth")

# --- snippet static: Static solve by Cholesky ---
L_bar = [element_stiffness(nodes_br[i, :], nodes_br[j, :], 1.0)[2] for (i, j) in bars_br]
m_bar = rho_steel * A_br .* L_bar             # kg per bar
f_br = zeros(size(K_br, 1))
f_br[[2 * bot_br[k] for k in 1:n_panels-1]] .-= w_deck * panel   # deck load, interior bottom joints
ends_y = [(2i, 2j) for (i, j) in bars_br]
for (b, (iy, jy)) in enumerate(ends_y)        # half of each bar's weight at each end
    f_br[iy] -= m_bar[b] * g_grav / 2
    f_br[jy] -= m_bar[b] * g_grav / 2
end
z_br = LowerTriangular(L_K) \ f_br[free_br]   # forward substitution:  L z = f
u_br = zeros(size(K_br, 1))
u_br[free_br] = LowerTriangular(L_K)' \ z_br  # back substitution:     Lᵀ u = z
residual_br = norm(K_ff * u_br[free_br] - f_br[free_br]) / norm(f_br)
N_br = bar_forces(nodes_br, bars_br, EA_br, u_br)
sigma_br = N_br ./ A_br                       # Pa
r_br = K_br * u_br - f_br                     # reactions
@assert residual_br < 1e-10
@assert sum(r_br[2:2:end]) ≈ -sum(f_br[2:2:end])     # supports carry the whole load
mid_top = findfirst(==((top_br[n_panels ÷ 2 - 1], top_br[n_panels ÷ 2])), bars_br)
x_mid = n_panels ÷ 2 * panel                  # beam check: N_top = −M / h at midspan
R_left = -sum(f_br[2n] * (span - nodes_br[n, 1]) for n in 1:size(nodes_br, 1)) / span
M_mid = R_left * x_mid + sum(f_br[2n] * (x_mid - nodes_br[n, 1])
                             for n in 1:size(nodes_br, 1) if nodes_br[n, 1] < x_mid)
@assert N_br[mid_top] ≈ -M_mid / height
println("midspan deflection $(round(-minimum(u_br[2:2:end]) * 1e3, digits=1)) mm")
println("stress from $(round(minimum(sigma_br) / 1e6)) to $(round(maximum(sigma_br) / 1e6)) MPa")

# --- snippet modes: Natural frequencies: K φ = λ M φ ---
"Consistent mass matrix of the bars: (m / 6) [2 1; 1 2] in each direction."
function assemble_mass(nodes, bars, m_bar)
    M = zeros(2 * size(nodes, 1), 2 * size(nodes, 1))
    for (b, (i, j)) in enumerate(bars)
        M[dofs(i, j), dofs(i, j)] .+= m_bar[b] / 6 * kron([2 1; 1 2], Matrix(1.0I, 2, 2))
    end
    return M
end

M_br = assemble_mass(nodes_br, bars_br, m_bar)
deck_dofs = [2 * bot_br[k] + d for k in 0:n_panels, d in (-1, 0)]   # x and y DOFs of bottom joints
deck_mass = m_deck * panel * [k in (0, n_panels) ? 0.5 : 1.0 for k in 0:n_panels]
for (row, m) in enumerate(deck_mass), d in deck_dofs[row, :]   # deck mass lumped at the bottom joints
    M_br[d, d] += m
end
M_ff = M_br[free_br, free_br]
L_M = cholesky(Symmetric(M_ff)).L             # M = L_M L_Mᵀ
Li_M = inv(LowerTriangular(L_M))
C_br = Symmetric(Li_M * K_ff * Li_M')         # K φ = λ M φ  becomes  C y = λ y,  φ = L_M⁻ᵀ y
lam_br, y_br = eigen(C_br)
phi_br = Li_M' * y_br
freq_hz = sqrt.(lam_br) / (2π)
@assert all(lam_br .> 0) && issorted(lam_br)
@assert isapprox(phi_br' * M_ff * phi_br, I, atol=1e-9)
@assert isapprox(K_ff * phi_br, M_ff * phi_br * Diagonal(lam_br), rtol=1e-8)
@assert 1.0 < freq_hz[1] < 3.0
println("lowest natural frequencies (Hz): ", round.(freq_hz[1:6], digits=2))
