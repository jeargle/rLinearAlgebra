# Python version of notebooks/09-empirical-orthogonal-functions-in-climate-data.py: a 4-site,
# 6-month toy field, then a synthetic Pacific sea-surface temperature field with two planted
# modes, using the notebook's variable names. Runs as it stands, with only numpy:
#
#     python 09-empirical-orthogonal-functions-in-climate-data.py
#
# Each section is shown on the entry page next to its Julia twin. The assert lines check the
# results: the toy against the numbers worked by hand, the synthetic field against properties
# that hold for any random draw (Python and Julia use different random numbers).
# Lines ending in #hide run but are not shown.

# --- snippet setup: The toy field ---
import numpy as np
toy_sites = ["g1", "g2", "g3", "g4"]
T_toy = np.array([[28., 26., 27., 24., 22., 23.],    # g1: temperature (°C), months 1-6
                  [27., 25., 26., 23., 21., 22.],    # g2
                  [27., 29., 28., 23., 25., 24.],    # g3
                  [26., 28., 27., 22., 24., 23.]])   # g4
s_toy, t_toy = T_toy.shape

# --- snippet anomaly: Remove each site's average ---
X_toy = T_toy - T_toy.mean(axis=1, keepdims=True)    # x_gk = T_gk - (mean of row g)
assert np.allclose(X_toy, [[3, 1, 2, -1, -3, -2],
                           [3, 1, 2, -1, -3, -2],
                           [1, 3, 2, -3, -1, -2],
                           [1, 3, 2, -3, -1, -2]])

# --- snippet svd: EOFs from the SVD of X ---
U_toy, S_toy, Vt_toy = np.linalg.svd(X_toy, full_matrices=False)
V_toy = Vt_toy.T
sign_toy = np.where(U_toy[0] < 0, -1, 1)                       # fix each pattern's sign: g1 loading > 0
U_toy, V_toy = U_toy * sign_toy, V_toy * sign_toy
pc_toy = V_toy * S_toy                               # a_i = sigma_i v_i, one column per mode
frac_toy = S_toy**2 / np.sum(S_toy**2)               # explained variance
assert np.allclose(S_toy[:2], [4 * np.sqrt(6), 4]) and np.allclose(S_toy[2:], 0)
assert np.allclose(U_toy[:, :2], [[0.5, 0.5], [0.5, 0.5], [0.5, -0.5], [0.5, -0.5]])
assert np.allclose(frac_toy[:2], [6 / 7, 1 / 7])
print("sigma =", S_toy.round(3), " explained variance =", frac_toy.round(3))

# --- snippet covariance: The same EOFs from the covariance matrix ---
C_toy = X_toy @ X_toy.T / (t_toy - 1)
assert np.allclose(C_toy, np.array([[28, 28, 20, 20],
                                    [28, 28, 20, 20],
                                    [20, 20, 28, 28],
                                    [20, 20, 28, 28]]) / 5)
lam_toy, E_toy = np.linalg.eigh(C_toy)               # ascending order
lam_toy, E_toy = lam_toy[::-1], E_toy[:, ::-1]
assert np.allclose(lam_toy, S_toy**2 / (t_toy - 1))  # 19.2, 3.2, 0, 0
assert np.allclose(np.abs(E_toy[:, :2].T @ U_toy[:, :2]), np.eye(2))  # same patterns, up to sign

# --- snippet truncate: The best rank-1 approximation ---
X1_toy = S_toy[0] * np.outer(U_toy[:, 0], V_toy[:, 0])
err1_toy = np.linalg.norm(X_toy - X1_toy)            # Frobenius norm
assert np.isclose(err1_toy**2, S_toy[1]**2)          # Eckart-Young: error^2 = 16
print("rank-1 error =", round(err1_toy, 6))

# --- snippet field: A synthetic Pacific temperature field ---
rng = np.random.default_rng(9)
lats = np.arange(-40.0, 41.0, 4.0)                   # 21 latitudes
lons = np.arange(130.0, 281.0, 5.0)                  # 31 longitudes (130°E to 80°W)
LAT, LON = np.meshgrid(lats, lons, indexing="ij")
lat_g, lon_g = LAT.ravel(), LON.ravel()              # one entry per grid point
s_sst, t_sst = lat_g.size, 480                       # 651 points, 40 years of months
month = np.arange(t_sst) % 12
# planted pattern 1: an ENSO-like dipole, warm east and cool west along the equator
p_enso = (np.exp(-(lat_g / 10)**2 - ((lon_g - 240) / 30)**2)
          - 0.6 * np.exp(-(lat_g / 12)**2 - ((lon_g - 160) / 20)**2))
# planted pattern 2: basin-wide warming, stronger in the north
p_trend = 0.4 + 0.6 * (lat_g + 40) / 80
w_sst = np.sqrt(np.cos(np.radians(lat_g)))          # area weights, the diagonal of W
# planted time series: red noise (AR(1)) for ENSO, a linear trend for warming; unit variance
a_enso = np.zeros(t_sst)
for k in range(1, t_sst):
    a_enso[k] = 0.9 * a_enso[k - 1] + rng.standard_normal()
a_trend = np.linspace(-1, 1, t_sst)
a_trend = a_trend / a_trend.std()
a_enso = a_enso - a_enso.mean()
a_enso = a_enso - (a_enso @ a_trend) / (a_trend @ a_trend) * a_trend   # uncorrelated with the trend
a_enso = a_enso / a_enso.std()
ratio = 0.3                                          # planted variance of mode 2 / mode 1
amp_enso = 1.0                                       # K
amp_trend = amp_enso * np.sqrt(ratio) * np.linalg.norm(w_sst * p_enso) / np.linalg.norm(w_sst * p_trend)
T_clim = 26 - 0.004 * lat_g[:, None]**2 + 3 * (lat_g[:, None] / 40) * np.cos(2 * np.pi * month / 12)
noise_sst = 0.4 * rng.standard_normal((s_sst, t_sst))   # white noise, K
T_sst = (T_clim + amp_enso * np.outer(p_enso, a_enso)
         + amp_trend * np.outer(p_trend, a_trend) + noise_sst)

# --- snippet weights: Anomalies and area weights ---
clim_sst = np.stack([T_sst[:, month == m].mean(axis=1) for m in range(12)], axis=1)
X_sst = T_sst - clim_sst[:, month]                   # subtract each calendar month's average
WX_sst = w_sst[:, None] * X_sst                      # W X, without forming the s x s matrix W
assert X_sst.shape == (651, 480) and np.allclose(X_sst[:, month == 0].mean(axis=1), 0)

# --- snippet eofs: Truncated SVD ---
U_sst, S_sst, Vt_sst = np.linalg.svd(WX_sst, full_matrices=False)
q = 2                                                # modes retained
sign_sst = np.sign(np.array([U_sst[:, 0] @ (w_sst * p_enso), U_sst[:, 1] @ (w_sst * p_trend)]))
U_sst[:, :q] *= sign_sst                             # the SVD fixes each pattern only up to sign
Vt_sst[:q] *= sign_sst[:, None]
eof_maps = U_sst[:, :q] / w_sst[:, None]             # undo the weighting before plotting
pc_sst = Vt_sst[:q].T * S_sst[:q]                    # PC time series a_i = sigma_i v_i
frac_sst = S_sst**2 / np.sum(S_sst**2)
WX_q = (U_sst[:, :q] * S_sst[:q]) @ Vt_sst[:q]
err_q = np.linalg.norm(WX_sst - WX_q)
assert np.isclose(err_q**2, np.sum(S_sst[q:]**2))   # Eckart-Young: error^2 = discarded sigma^2
print("explained variance of modes 1-4:", frac_sst[:4].round(3))

# --- snippet north: North's rule of thumb ---
lam_sst = S_sst**2 / (t_sst - 1)                     # eigenvalues of the weighted covariance
dlam_sst = lam_sst * np.sqrt(2 / t_sst)              # sampling error, if months were independent
separated = lam_sst[:-1] - lam_sst[1:] > dlam_sst[:-1]
assert separated[0] and separated[1]                 # modes 1 and 2 stand clear of their neighbours
assert frac_sst[2] < 0.01                            # mode 3 onward is noise

# --- snippet recover: Recovered versus planted patterns ---
def pattern_corr(u, p, w):
    """|cosine| between an EOF (weighted space) and a planted map, in the area-weighted metric."""
    wp = w * p
    return abs(u @ wp) / (np.linalg.norm(u) * np.linalg.norm(wp))

corr_enso = pattern_corr(U_sst[:, 0], p_enso, w_sst)
corr_trend = pattern_corr(U_sst[:, 1], p_trend, w_sst)
overlap = pattern_corr(w_sst * p_enso, p_trend, w_sst)   # the planted patterns are not orthogonal
assert corr_enso > 0.95 and corr_trend > 0.9
assert abs(np.corrcoef(pc_sst[:, 0], a_enso)[0, 1]) > 0.95
print(f"pattern correlations: {corr_enso:.3f}, {corr_trend:.3f}; planted overlap {overlap:.3f}")

# --- snippet mixing: Equal variances blend the modes ---
amp_eq = amp_enso * np.linalg.norm(w_sst * p_enso) / np.linalg.norm(w_sst * p_trend)  # ratio = 1
X_eq = amp_enso * np.outer(p_enso, a_enso) + amp_eq * np.outer(p_trend, a_trend) + noise_sst
U_eq, S_eq, _ = np.linalg.svd(w_sst[:, None] * X_eq, full_matrices=False)
corr_eq = pattern_corr(U_eq[:, 0], p_enso, w_sst)
blend = p_enso / np.linalg.norm(w_sst * p_enso) + p_trend / np.linalg.norm(w_sst * p_trend)
corr_blend = pattern_corr(U_eq[:, 0], blend, w_sst)
assert corr_eq < corr_enso and corr_blend > corr_eq  # EOF 1 is now a mixture of both mechanisms
print(f"EOF 1 vs ENSO: {corr_eq:.3f}; vs ENSO + warming blend: {corr_blend:.3f}")
