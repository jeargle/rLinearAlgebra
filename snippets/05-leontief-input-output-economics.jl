# Julia versions of the core computations in notebooks/05-leontief-input-output-economics.py,
# using the notebook's variable names. Each section is shown on the entry page and in the
# notebook; the @assert lines check it against the two-sector toy worked by hand. Lines ending
# in #hide run but are not shown: they load the toy numbers under the notebook's Part 2 names.
# Standard library only:
#     julia snippets/05-leontief-input-output-economics.jl

# --- snippet setup: The toy economy ---
using LinearAlgebra
A_toy = [0.2 0.2
         0.4 0.1]      # column j: inputs per $1 of sector j's output
d_toy = [100.0, 50.0]  # final demand

# --- snippet solve: Solve (I − A) x = d ---
x_toy = (I - A_toy) \ d_toy    # I adapts its size; \ solves without forming an inverse
@assert x_toy ≈ [156.25, 125.0]

# --- snippet inverse: The Leontief inverse ---
@assert det(I - A_toy) ≈ 0.64
L_toy = inv(I - A_toy)         # entry (i, j): output of i needed per $1 of final demand for j
@assert L_toy ≈ [1.40625 0.3125
                 0.625   1.25]

# --- snippet rounds: Round by round: d + A d + A² d + ... ---
@assert sum(A_toy^k * d_toy for k in 0:30) ≈ x_toy

# --- snippet productive: Is the economy productive? ---
s = 1.0                                  # the slider: scale every input requirement by s
A_s = s * A_toy
colsums_s = sum(A_s, dims=1)             # quick test: every column sums below 1
rho_s = maximum(abs, eigvals(A_s))       # exact test: spectral radius below 1
@assert all(colsums_s .< 1) && rho_s < 1

# --- snippet coefficients: Coefficients from a flow table ---
Z_us, d_us, x_us = A_toy .* x_toy', d_toy, x_toy   #hide
# Z_us: flows between sectors; d_us: final demand; x_us: gross output
n_us = length(x_us)
A_us = Z_us ./ x_us'               # a_ij = z_ij / x_j  (x_us' is a row: column j divided by x_j)
L_us = inv(I - A_us)
x_solved = (I - A_us) \ d_us       # should recover the actual output x_us
@assert A_us ≈ A_toy && x_solved ≈ x_us   #hide

# --- snippet multipliers: Output multipliers ---
multipliers = vec(sum(L_us, dims=1))   # column sums of L
@assert multipliers ≈ [2.03125, 1.5625]   #hide

# --- snippet shock: A demand shock, round by round ---
dd = [10.0, 0.0]                   #hide
# dd: extra final demand, all of it for one sector
dx_total = L_us * dd               # total extra output
dx_first = A_us * dd               # first round of inputs
dx_later = dx_total - dd - dx_first
@assert dx_total ≈ [14.0625, 6.25] && dx_later ≈ [2.0625, 2.25]   #hide
