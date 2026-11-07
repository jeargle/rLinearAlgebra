# Julia version of notebooks/09-empirical-orthogonal-functions-in-climate-data.py: a 4-site,
# 6-month toy field, then a synthetic Pacific sea-surface temperature field with two planted
# modes, using the notebook's variable names. Runs as it stands, with only Julia's standard
# library:
#
#     julia 09-empirical-orthogonal-functions-in-climate-data.jl
#
# Each section is shown in the notebook and on the entry page. The @assert lines check the
# results: the toy against the numbers worked by hand, the synthetic field against properties
# that hold for any random draw (Julia and Python use different random numbers).
# Lines ending in #hide run but are not shown.

# --- snippet setup: The toy field ---
using LinearAlgebra, Statistics, Random, Printf
toy_sites = ["g1", "g2", "g3", "g4"]
T_toy = [28.0 26 27 24 22 23     # g1: temperature (°C), months 1-6
         27   25 26 23 21 22     # g2
         27   29 28 23 25 24     # g3
         26   28 27 22 24 23]    # g4
s_toy, t_toy = size(T_toy)

# --- snippet anomaly: Remove each site's average ---
X_toy = T_toy .- mean(T_toy, dims=2)                 # x_gk = T_gk - (mean of row g)
@assert X_toy ≈ [3 1 2 -1 -3 -2
                 3 1 2 -1 -3 -2
                 1 3 2 -3 -1 -2
                 1 3 2 -3 -1 -2]

# --- snippet svd: EOFs from the SVD of X ---
F_toy = svd(X_toy)
U_toy, S_toy, Vt_toy = F_toy.U, F_toy.S, F_toy.Vt
V_toy = Matrix(Vt_toy')
sign_toy = [u < 0 ? -1 : 1 for u in U_toy[1, :]]'   # fix each pattern's sign: g1 loading > 0
U_toy, V_toy = U_toy .* sign_toy, V_toy .* sign_toy
pc_toy = V_toy .* S_toy'                             # a_i = sigma_i v_i, one column per mode
frac_toy = S_toy .^ 2 ./ sum(S_toy .^ 2)             # explained variance
@assert S_toy[1:2] ≈ [4sqrt(6), 4] && all(abs.(S_toy[3:end]) .< 1e-10)
@assert U_toy[:, 1:2] ≈ [0.5 0.5; 0.5 0.5; 0.5 -0.5; 0.5 -0.5]
@assert frac_toy[1:2] ≈ [6/7, 1/7]
println("sigma = ", round.(S_toy, digits=3), "  explained variance = ", round.(frac_toy, digits=3))

# --- snippet covariance: The same EOFs from the covariance matrix ---
C_toy = X_toy * X_toy' / (t_toy - 1)
@assert C_toy ≈ [28 28 20 20
                 28 28 20 20
                 20 20 28 28
                 20 20 28 28] / 5
E = eigen(Symmetric(C_toy), sortby = λ -> -λ)        # descending order
lam_toy, E_toy = E.values, E.vectors
@assert isapprox(lam_toy, S_toy .^ 2 / (t_toy - 1), atol=1e-10)   # 19.2, 3.2, 0, 0
@assert abs.(E_toy[:, 1:2]' * U_toy[:, 1:2]) ≈ I(2)  # same patterns, up to sign

# --- snippet truncate: The best rank-1 approximation ---
X1_toy = S_toy[1] * U_toy[:, 1] * V_toy[:, 1]'
err1_toy = norm(X_toy - X1_toy)                      # Frobenius norm
@assert err1_toy^2 ≈ S_toy[2]^2                      # Eckart-Young: error^2 = 16
println("rank-1 error = ", round(err1_toy, digits=6))

# --- snippet field: A synthetic Pacific temperature field ---
rng = Xoshiro(9)
lats = collect(-40.0:4.0:40.0)                       # 21 latitudes
lons = collect(130.0:5.0:280.0)                      # 31 longitudes (130°E to 80°W)
lat_g = vec([la for lo in lons, la in lats])         # one entry per grid point, latitude-major
lon_g = vec([lo for lo in lons, la in lats])         # (same order as the Python version)
s_sst, t_sst = length(lat_g), 480                    # 651 points, 40 years of months
month = (0:t_sst-1) .% 12
# planted pattern 1: an ENSO-like dipole, warm east and cool west along the equator
p_enso = (exp.(-(lat_g / 10) .^ 2 .- ((lon_g .- 240) / 30) .^ 2)
          .- 0.6 * exp.(-(lat_g / 12) .^ 2 .- ((lon_g .- 160) / 20) .^ 2))
# planted pattern 2: basin-wide warming, stronger in the north
p_trend = 0.4 .+ 0.6 * (lat_g .+ 40) / 80
w_sst = sqrt.(cosd.(lat_g))                          # area weights, the diagonal of W
# planted time series: red noise (AR(1)) for ENSO, a linear trend for warming; unit variance
a_enso = zeros(t_sst)
for k in 2:t_sst
    a_enso[k] = 0.9 * a_enso[k-1] + randn(rng)
end
a_trend = collect(range(-1, 1, length=t_sst))
a_trend = a_trend / std(a_trend, corrected=false)
a_enso = a_enso .- mean(a_enso)
a_enso = a_enso - (a_enso ⋅ a_trend) / (a_trend ⋅ a_trend) * a_trend   # uncorrelated with the trend
a_enso = a_enso / std(a_enso, corrected=false)
ratio = 0.3                                          # planted variance of mode 2 / mode 1
amp_enso = 1.0                                       # K
amp_trend = amp_enso * sqrt(ratio) * norm(w_sst .* p_enso) / norm(w_sst .* p_trend)
T_clim = 26 .- 0.004 * lat_g .^ 2 .+ 3 * (lat_g / 40) .* cos.(2pi * month' / 12)
noise_sst = 0.4 * randn(rng, s_sst, t_sst)           # white noise, K
T_sst = (T_clim + amp_enso * p_enso * a_enso'
         + amp_trend * p_trend * a_trend' + noise_sst)

# --- snippet weights: Anomalies and area weights ---
clim_sst = hcat([mean(T_sst[:, month .== m], dims=2) for m in 0:11]...)
X_sst = T_sst - clim_sst[:, month .+ 1]              # subtract each calendar month's average
WX_sst = w_sst .* X_sst                              # W X, without forming the s x s matrix W
@assert size(X_sst) == (651, 480) && all(abs.(mean(X_sst[:, month .== 0], dims=2)) .< 1e-10)

# --- snippet eofs: Truncated SVD ---
F_sst = svd(WX_sst)
U_sst, S_sst, Vt_sst = F_sst.U, F_sst.S, F_sst.Vt
q = 2                                                # modes retained
sign_sst = sign.([U_sst[:, 1] ⋅ (w_sst .* p_enso), U_sst[:, 2] ⋅ (w_sst .* p_trend)])
U_sst[:, 1:q] .*= sign_sst'                          # the SVD fixes each pattern only up to sign
Vt_sst[1:q, :] .*= sign_sst
eof_maps = U_sst[:, 1:q] ./ w_sst                    # undo the weighting before plotting
pc_sst = Vt_sst[1:q, :]' .* S_sst[1:q]'              # PC time series a_i = sigma_i v_i
frac_sst = S_sst .^ 2 ./ sum(S_sst .^ 2)
WX_q = U_sst[:, 1:q] * Diagonal(S_sst[1:q]) * Vt_sst[1:q, :]
err_q = norm(WX_sst - WX_q)
@assert err_q^2 ≈ sum(S_sst[q+1:end] .^ 2)          # Eckart-Young: error^2 = discarded sigma^2
println("explained variance of modes 1-4: ", round.(frac_sst[1:4], digits=3))

# --- snippet north: North's rule of thumb ---
lam_sst = S_sst .^ 2 / (t_sst - 1)                   # eigenvalues of the weighted covariance
dlam_sst = lam_sst * sqrt(2 / t_sst)                 # sampling error, if months were independent
separated = lam_sst[1:end-1] - lam_sst[2:end] .> dlam_sst[1:end-1]
@assert separated[1] && separated[2]                 # modes 1 and 2 stand clear of their neighbours
@assert frac_sst[3] < 0.01                           # mode 3 onward is noise

# --- snippet recover: Recovered versus planted patterns ---
"""|cosine| between an EOF (weighted space) and a planted map, in the area-weighted metric."""
function pattern_corr(u, p, w)
    wp = w .* p
    return abs(u ⋅ wp) / (norm(u) * norm(wp))
end

corr_enso = pattern_corr(U_sst[:, 1], p_enso, w_sst)
corr_trend = pattern_corr(U_sst[:, 2], p_trend, w_sst)
overlap = pattern_corr(w_sst .* p_enso, p_trend, w_sst)   # the planted patterns are not orthogonal
@assert corr_enso > 0.95 && corr_trend > 0.9
@assert abs(cor(pc_sst[:, 1], a_enso)) > 0.95
@printf("pattern correlations: %.3f, %.3f; planted overlap %.3f\n", corr_enso, corr_trend, overlap)

# --- snippet mixing: Equal variances blend the modes ---
amp_eq = amp_enso * norm(w_sst .* p_enso) / norm(w_sst .* p_trend)   # ratio = 1
X_eq = amp_enso * p_enso * a_enso' + amp_eq * p_trend * a_trend' + noise_sst
U_eq = svd(w_sst .* X_eq).U
corr_eq = pattern_corr(U_eq[:, 1], p_enso, w_sst)
blend = p_enso / norm(w_sst .* p_enso) + p_trend / norm(w_sst .* p_trend)
corr_blend = pattern_corr(U_eq[:, 1], blend, w_sst)
@assert corr_eq < corr_enso && corr_blend > corr_eq  # EOF 1 is now a mixture of both mechanisms
@printf("EOF 1 vs ENSO: %.3f; vs ENSO + warming blend: %.3f\n", corr_eq, corr_blend)
