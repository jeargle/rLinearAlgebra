# Python versions of the core computations in notebooks/05-leontief-input-output-economics.py,
# using the notebook's variable names. Each section is shown on the entry page next to its Julia
# twin; the assert lines check it against the two-sector toy worked by hand. Lines ending in
# #hide run but are not shown: they load the toy numbers under the notebook's Part 2 names.
# Needs only numpy:
#     uv run --group notebooks python snippets/05-leontief-input-output-economics.py

# --- snippet setup: The toy economy ---
import numpy as np
A_toy = np.array([[0.2, 0.2],
                  [0.4, 0.1]])   # column j: inputs per $1 of sector j's output
d_toy = np.array([100.0, 50.0])  # final demand

# --- snippet solve: Solve (I − A) x = d ---
x_toy = np.linalg.solve(np.eye(2) - A_toy, d_toy)   # solves without forming an inverse
assert np.allclose(x_toy, [156.25, 125.0])

# --- snippet inverse: The Leontief inverse ---
assert np.isclose(np.linalg.det(np.eye(2) - A_toy), 0.64)
L_toy = np.linalg.inv(np.eye(2) - A_toy)  # entry (i, j): output of i needed per $1 of final demand for j
assert np.allclose(L_toy, [[1.40625, 0.3125],
                           [0.625,   1.25]])

# --- snippet rounds: Round by round: d + A d + A² d + ... ---
assert np.allclose(sum(np.linalg.matrix_power(A_toy, k) @ d_toy for k in range(31)), x_toy)

# --- snippet productive: Is the economy productive? ---
s = 1.0                                  # the slider: scale every input requirement by s
A_s = s * A_toy
colsums_s = A_s.sum(axis=0)              # quick test: every column sums below 1
rho_s = max(abs(np.linalg.eigvals(A_s))) # exact test: spectral radius below 1
assert (colsums_s < 1).all() and rho_s < 1

# --- snippet coefficients: Coefficients from a flow table ---
Z_us, d_us, x_us = A_toy * x_toy, d_toy, x_toy   #hide
# Z_us: flows between sectors; d_us: final demand; x_us: gross output
n_us = len(x_us)
A_us = Z_us / x_us                 # a_ij = z_ij / x_j  (broadcasting divides column j by x_j)
L_us = np.linalg.inv(np.eye(n_us) - A_us)
x_solved = np.linalg.solve(np.eye(n_us) - A_us, d_us)   # should recover the actual output x_us
assert np.allclose(A_us, A_toy) and np.allclose(x_solved, x_us)   #hide

# --- snippet multipliers: Output multipliers ---
multipliers = L_us.sum(axis=0)     # column sums of L
assert np.allclose(multipliers, [2.03125, 1.5625])   #hide

# --- snippet shock: A demand shock, round by round ---
dd = np.array([10.0, 0.0])         #hide
# dd: extra final demand, all of it for one sector
dx_total = L_us @ dd               # total extra output
dx_first = A_us @ dd               # first round of inputs
dx_later = dx_total - dd - dx_first
assert np.allclose(dx_total, [14.0625, 6.25]) and np.allclose(dx_later, [2.0625, 2.25])   #hide
