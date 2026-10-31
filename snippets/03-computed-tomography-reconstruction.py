# Python version of notebooks/03-computed-tomography-reconstruction.py: a four-pixel toy scan
# worked by hand, then a 32 × 32 Shepp–Logan phantom scanned at 24 angles, using the notebook's
# variable names. Runs as it stands, with numpy and scipy:
#
#     python 03-computed-tomography-reconstruction.py
#
# Each section is shown on the entry page next to its Julia twin. The assert lines check the
# results: the toy against the numbers worked by hand, the phantom against properties that any
# run must have (the Julia file draws different random noise). Python counts from 0, so pixel j
# and ray i are one smaller than in the Julia file. Lines ending in #hide run but are not shown.

# --- snippet setup: The toy scan: four pixels, five rays ---
import numpy as np
# pixels P Q (top row) and R S (bottom row), each 1 cm wide; x lists them in the order P, Q, R, S
x_toy = np.array([0.2, 0.2, 0.2, 0.5])     # attenuation μ in cm⁻¹: soft tissue, and bone in S
A_toy = np.array([[1.0, 1.0, 0.0, 0.0],    # ray 1: across the top row (P, Q)
                  [0.0, 0.0, 1.0, 1.0],    # ray 2: across the bottom row (R, S)
                  [1.0, 0.0, 1.0, 0.0],    # ray 3: down the left column (P, R)
                  [0.0, 1.0, 0.0, 1.0],    # ray 4: down the right column (Q, S)
                  [0.2, 0.0, 0.0, 0.0]])   # ray 5: clips the corner of P, 0.2 cm inside it
b_toy = A_toy @ x_toy                      # total attenuation along each ray
assert np.allclose(b_toy, [0.4, 0.7, 0.4, 0.7, 0.04])
print("b_toy =", b_toy)

# --- snippet beer_lambert: Beer–Lambert: fractions multiply, logarithms add ---
I0 = 1.0e5                                 # photons sent along each ray
I_toy = I0 * np.exp(-b_toy)                # what the detectors count (no noise yet)
# ray 2 crosses R then S: the surviving fractions multiply ...
assert np.isclose(I_toy[1] / I0, np.exp(-0.2) * np.exp(-0.5))
# ... so their logarithms add, and −ln(I/I0) is linear in μ
assert np.allclose(-np.log(I_toy / I0), A_toy @ x_toy)
print("I_toy / I0 =", I_toy / I0)

# --- snippet svd: The SVD of the toy A ---
U_toy, s_toy, Vt_toy = np.linalg.svd(A_toy, full_matrices=False)
checker = np.array([1, -1, -1, 1]) / 2     # the checkerboard pattern, length 1
assert np.allclose(A_toy[:4] @ checker, 0)          # rows and columns cannot see it
assert np.allclose(A_toy @ checker, [0, 0, 0, 0, 0.1])  # only ray 5 can, weakly
assert abs(abs(Vt_toy[-1] @ checker) - 1) < 1e-4    # it is (almost exactly) the last v
assert 0.09 < s_toy[-1] < 0.1
print("singular values:", s_toy)

# --- snippet noise: One reading off by 0.01, image off by 0.1 ---
b_noisy_toy = b_toy + np.array([0, 0, 0, 0, 0.01])  # ray 5 reads 0.05 instead of 0.04
x_naive_toy = np.linalg.lstsq(A_toy, b_noisy_toy, rcond=None)[0]
assert np.allclose(x_naive_toy, [0.25, 0.15, 0.15, 0.55])   # P = 0.05/0.2, then rows and columns
assert np.allclose(x_naive_toy - x_toy, 0.1 * checker)      # the error is the checkerboard
print("x_naive_toy =", x_naive_toy)

# --- snippet tikhonov_toy: Tikhonov regularization on the toy ---
lam_toy = 0.01                             # λ, with L = I: prefer the smallest image that fits
x_tik_toy = np.linalg.solve(A_toy.T @ A_toy + lam_toy * np.eye(4), A_toy.T @ b_noisy_toy)
filter_toy = s_toy**2 / (s_toy**2 + lam_toy)   # how much of each singular direction survives
assert np.linalg.norm(x_tik_toy - x_toy) < np.linalg.norm(x_naive_toy - x_toy) / 3
assert filter_toy[:3].min() > 0.99 and 0.4 < filter_toy[-1] < 0.6
print("x_tik_toy =", x_tik_toy.round(3), " filter factors:", filter_toy.round(3))

# --- snippet phantom: The Shepp–Logan phantom ---
# modified Shepp–Logan ellipses on the square [-1, 1]²: value added inside, semi-axes a and b,
# centre (x0, y0), rotation in degrees. The values are μ in cm⁻¹ for a 20 cm field of view.
ellipses = np.array([
    [ 1.0, 0.69,   0.92,    0.0,   0.0,      0],
    [-0.8, 0.6624, 0.8740,  0.0,  -0.0184,   0],
    [-0.2, 0.1100, 0.3100,  0.22,  0.0,    -18],
    [-0.2, 0.1600, 0.4100, -0.22,  0.0,     18],
    [ 0.1, 0.2100, 0.2500,  0.0,   0.35,     0],
    [ 0.1, 0.0460, 0.0460,  0.0,   0.1,      0],
    [ 0.1, 0.0460, 0.0460,  0.0,  -0.1,      0],
    [ 0.1, 0.0460, 0.0230, -0.08, -0.605,    0],
    [ 0.1, 0.0230, 0.0230,  0.0,  -0.606,    0],
    [ 0.1, 0.0230, 0.0460,  0.06, -0.605,    0]])


def shepp_logan(n, ss=4):
    """n × n image, row 0 at the top; each pixel averages ss × ss samples."""
    c = (np.arange(n * ss) + 0.5) / (n * ss) * 2 - 1
    X, Y = np.meshgrid(c, -c)
    img = np.zeros_like(X)
    for val, a, b, x0, y0, phi in ellipses:
        t = np.deg2rad(phi)
        xr = (X - x0) * np.cos(t) + (Y - y0) * np.sin(t)
        yr = -(X - x0) * np.sin(t) + (Y - y0) * np.cos(t)
        img += val * ((xr / a) ** 2 + (yr / b) ** 2 <= 1)
    return img.reshape(n, ss, n, ss).mean(axis=(1, 3))


n = 32                                     # 32 × 32 pixels
width = 20.0                               # field of view, cm
img_true = shepp_logan(n)
x_true = img_true.ravel()                  # pixel j = row * n + col
assert img_true.min() > -1e-9 and img_true.max() <= 1 + 1e-9   # air 0 up to skull 1 cm⁻¹
assert np.isclose(img_true[22, 16], 0.2)                         # brain, near water

# --- snippet projector: The ray-projection matrix A ---
import scipy.sparse as sp


def ray_pixels(p0, d, n, h):
    """Pixels crossed by the ray p0 + t d (d a unit vector), and the length inside each."""
    half = n * h / 2
    edges = -half + h * np.arange(n + 1)
    ts = [(edges - p0[k]) / d[k] for k in range(2) if abs(d[k]) > 1e-12]
    t = np.unique(np.concatenate(ts))      # every crossing of a grid line, in order
    mid = p0[:, None] + d[:, None] * (t[1:] + t[:-1]) / 2
    col = np.floor((mid[0] + half) / h).astype(int)
    row = np.floor((half - mid[1]) / h).astype(int)
    seg = np.diff(t)
    keep = (col >= 0) & (col < n) & (row >= 0) & (row < n) & (seg > 1e-12)
    return row[keep] * n + col[keep], seg[keep]


def projector(n, n_angles, width):
    """Parallel-beam system matrix: one row per (angle, detector) ray, entries in cm."""
    h = width / n
    n_det = int(np.ceil(n * np.sqrt(2)))   # enough detectors to cover the diagonal
    rows, cols, vals = [], [], []
    for k in range(n_angles):
        th = np.pi * k / n_angles
        d = np.array([np.cos(th), np.sin(th)])        # ray direction
        nrm = np.array([-np.sin(th), np.cos(th)])     # detector axis
        for m in range(n_det):
            s = (m - (n_det - 1) / 2) * h
            j, length = ray_pixels(s * nrm - width * d, d, n, h)
            rows += [k * n_det + m] * len(j)
            cols += list(j)
            vals += list(length)
    A = sp.csr_matrix((vals, (rows, cols)), shape=(n_angles * n_det, n * n))
    return A, n_det


n_angles = 24                              # one view every 7.5°
A_ct, n_det = projector(n, n_angles, width)
M_ct, N_ct = A_ct.shape
mid_ray = n_det // 2                       # through the centre at angle 0 (horizontal)
assert np.isclose(A_ct[mid_ray].sum(), width)          # crosses the full 20 cm
assert M_ct > N_ct and A_ct.nnz / (M_ct * N_ct) < 0.05  # more rays than pixels, very sparse
print(f"A is {M_ct} × {N_ct}, {100 * A_ct.nnz / (M_ct * N_ct):.1f}% nonzero")

# --- snippet scan: Simulated scan with photon noise ---
b_ct = A_ct @ x_true                       # exact line integrals
rng = np.random.default_rng(3)
expected = I0 * np.exp(-b_ct)              # mean photon count at each detector
# photon counts are Poisson; with counts this large a normal with equal mean and variance fits
counts = expected + np.sqrt(expected) * rng.standard_normal(M_ct)
b_meas = -np.log(counts / I0)              # the sinogram, after the logarithm
sinogram = b_meas.reshape(n_angles, n_det)
assert 0.005 < np.std(b_meas - b_ct) < 0.05

# --- snippet spectrum: The singular-value spectrum ---
U_ct, s_ct, Vt_ct = np.linalg.svd(A_ct.toarray(), full_matrices=False)
tol_ct = s_ct[0] * max(M_ct, N_ct) * np.finfo(float).eps  # numpy's own rank cutoff
rank_ct = int((s_ct > tol_ct).sum())
assert rank_ct < N_ct                      # a null space, despite having more rays than pixels
assert s_ct[rank_ct - 1] / s_ct[0] < 1e-3  # and singular values far below the largest
print(f"rank {rank_ct} of {N_ct}; σ_max = {s_ct[0]:.2f}, smallest kept σ = {s_ct[rank_ct - 1]:.2e}")

# --- snippet naive: Naive least squares ---
def rel_error(x):
    return np.linalg.norm(x - x_true) / np.linalg.norm(x_true)


coef_ct = U_ct[:, :rank_ct].T @ b_meas / s_ct[:rank_ct]  # each component divided by its σ
x_naive = Vt_ct[:rank_ct].T @ coef_ct      # minimum-norm least-squares solution
x_clean = Vt_ct[:rank_ct].T @ (U_ct[:, :rank_ct].T @ b_ct / s_ct[:rank_ct])  # same, no noise
err_naive = rel_error(x_naive)
assert err_naive > 3 * rel_error(x_clean)  # the noise, not the null space, ruins it
print(f"naive relative error {err_naive:.2f} (noise-free data: {rel_error(x_clean):.2f})")

# --- snippet tikhonov: Tikhonov with a smoothness penalty ---
D1 = sp.diags([-np.ones(n), np.ones(n - 1)], [0, 1], shape=(n - 1, n))   # neighbour differences
L_ct = sp.vstack([sp.kron(sp.eye(n), D1), sp.kron(D1, sp.eye(n))])       # across, then down
AtA = (A_ct.T @ A_ct).toarray()
LtL = (L_ct.T @ L_ct).toarray()
Atb = A_ct.T @ b_meas
lams = np.logspace(-6, 1, 15)              # λ from 10⁻⁶ to 10, two steps per decade


def tikhonov(lam):
    """Minimize ‖A x − b‖² + λ ‖L x‖² via its normal equations."""
    return np.linalg.solve(AtA + lam * LtL, Atb)


tik_err = np.array([rel_error(tikhonov(lam)) for lam in lams])
lam_best = lams[np.argmin(tik_err)]
x_tik = tikhonov(lam_best)
assert tik_err.min() < err_naive / 3
assert tik_err[0] > tik_err.min() and tik_err[-1] > tik_err.min()   # too little and too much both hurt
print(f"Tikhonov: best λ = {lam_best:.3g}, relative error {tik_err.min():.3f}")

# --- snippet art: Kaczmarz / ART: one ray at a time ---
def art(A, b, sweeps, omega=1.0):
    """Kaczmarz sweeps: project x onto each ray's equation in turn; return x after each sweep."""
    A = A.tocsr()
    row_norm2 = np.asarray(A.multiply(A).sum(axis=1)).ravel()
    x = np.zeros(A.shape[1])
    history = []
    for _ in range(sweeps):
        for i in np.flatnonzero(row_norm2):
            cols, a = A.indices[A.indptr[i]:A.indptr[i + 1]], A.data[A.indptr[i]:A.indptr[i + 1]]
            x[cols] += omega * (b[i] - a @ x[cols]) / row_norm2[i] * a
        history.append(x.copy())
    return x, history


x_art, art_history = art(A_ct, b_meas, sweeps=30)
art_err = np.array([rel_error(v) for v in art_history])
assert art_err[0] > art_err[1] > art_err[2] > art_err[4]   # falls quickly at first
assert art_err.min() < err_naive / 3
print(f"ART: error {art_err[0]:.3f} after 1 sweep, {art_err[-1]:.3f} after {len(art_err)}")
