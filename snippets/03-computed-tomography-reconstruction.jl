# Julia version of notebooks/03-computed-tomography-reconstruction.py: a four-pixel toy scan
# worked by hand, then a 32 × 32 Shepp–Logan phantom scanned at 24 angles, using the notebook's
# variable names. Runs as it stands, with only standard libraries (LinearAlgebra, SparseArrays,
# Random):
#
#     julia 03-computed-tomography-reconstruction.jl
#
# Each section is shown on the entry page next to its Python twin. The @assert lines check the
# results: the toy against the numbers worked by hand, the phantom against properties that any
# run must have (Julia's random numbers differ from Python's). Julia counts from 1, so pixel j
# and ray i are one larger than in the Python file. Lines ending in #hide run but are not shown.

# --- snippet setup: The toy scan: four pixels, five rays ---
using LinearAlgebra
# pixels P Q (top row) and R S (bottom row), each 1 cm wide; x lists them in the order P, Q, R, S
x_toy = [0.2, 0.2, 0.2, 0.5]       # attenuation μ in cm⁻¹: soft tissue, and bone in S
A_toy = [1.0 1.0 0.0 0.0           # ray 1: across the top row (P, Q)
         0.0 0.0 1.0 1.0           # ray 2: across the bottom row (R, S)
         1.0 0.0 1.0 0.0           # ray 3: down the left column (P, R)
         0.0 1.0 0.0 1.0           # ray 4: down the right column (Q, S)
         0.2 0.0 0.0 0.0]          # ray 5: clips the corner of P, 0.2 cm inside it
b_toy = A_toy * x_toy              # total attenuation along each ray
@assert b_toy ≈ [0.4, 0.7, 0.4, 0.7, 0.04]
@show b_toy

# --- snippet beer_lambert: Beer–Lambert: fractions multiply, logarithms add ---
I0 = 1.0e5                         # photons sent along each ray
I_toy = I0 .* exp.(-b_toy)         # what the detectors count (no noise yet)
# ray 2 crosses R then S: the surviving fractions multiply ...
@assert I_toy[2] / I0 ≈ exp(-0.2) * exp(-0.5)
# ... so their logarithms add, and −ln(I/I0) is linear in μ
@assert -log.(I_toy ./ I0) ≈ A_toy * x_toy
@show I_toy ./ I0

# --- snippet svd: The SVD of the toy A ---
F_toy = svd(A_toy)
U_toy, s_toy, Vt_toy = F_toy.U, F_toy.S, F_toy.Vt
checker = [1, -1, -1, 1] / 2       # the checkerboard pattern, length 1
@assert isapprox(A_toy[1:4, :] * checker, zeros(4), atol=1e-12)   # rows and columns cannot see it
@assert A_toy * checker ≈ [0, 0, 0, 0, 0.1]                       # only ray 5 can, weakly
@assert abs(abs(dot(Vt_toy[end, :], checker)) - 1) < 1e-4         # it is (almost exactly) the last v
@assert 0.09 < s_toy[end] < 0.1
@show s_toy

# --- snippet noise: One reading off by 0.01, image off by 0.1 ---
b_noisy_toy = b_toy + [0, 0, 0, 0, 0.01]   # ray 5 reads 0.05 instead of 0.04
x_naive_toy = A_toy \ b_noisy_toy          # least squares (A has full column rank)
@assert x_naive_toy ≈ [0.25, 0.15, 0.15, 0.55]   # P = 0.05/0.2, then rows and columns
@assert x_naive_toy - x_toy ≈ 0.1 * checker      # the error is the checkerboard
@show x_naive_toy

# --- snippet tikhonov_toy: Tikhonov regularization on the toy ---
lam_toy = 0.01                     # λ, with L = I: prefer the smallest image that fits
x_tik_toy = (A_toy' * A_toy + lam_toy * I) \ (A_toy' * b_noisy_toy)
filter_toy = s_toy .^ 2 ./ (s_toy .^ 2 .+ lam_toy)   # how much of each singular direction survives
@assert norm(x_tik_toy - x_toy) < norm(x_naive_toy - x_toy) / 3
@assert minimum(filter_toy[1:3]) > 0.99 && 0.4 < filter_toy[end] < 0.6
@show round.(x_tik_toy, digits=3) round.(filter_toy, digits=3)

# --- snippet phantom: The Shepp–Logan phantom ---
# modified Shepp–Logan ellipses on the square [-1, 1]²: value added inside, semi-axes a and b,
# centre (x0, y0), rotation in degrees. The values are μ in cm⁻¹ for a 20 cm field of view.
ellipses = [ 1.0 0.69   0.92    0.0   0.0      0
            -0.8 0.6624 0.8740  0.0  -0.0184   0
            -0.2 0.1100 0.3100  0.22  0.0    -18
            -0.2 0.1600 0.4100 -0.22  0.0     18
             0.1 0.2100 0.2500  0.0   0.35     0
             0.1 0.0460 0.0460  0.0   0.1      0
             0.1 0.0460 0.0460  0.0  -0.1      0
             0.1 0.0460 0.0230 -0.08 -0.605    0
             0.1 0.0230 0.0230  0.0  -0.606    0
             0.1 0.0230 0.0460  0.06 -0.605    0]

"n × n image, row 1 at the top; each pixel averages ss × ss samples."
function shepp_logan(n; ss=4)
    c = ((0:n*ss-1) .+ 0.5) ./ (n * ss) .* 2 .- 1
    X = [c[q] for p in eachindex(c), q in eachindex(c)]
    Y = [-c[p] for p in eachindex(c), q in eachindex(c)]
    img = zeros(size(X))
    for (val, a, b, x0, y0, phi) in eachrow(ellipses)
        t = deg2rad(phi)
        xr = (X .- x0) .* cos(t) .+ (Y .- y0) .* sin(t)
        yr = -(X .- x0) .* sin(t) .+ (Y .- y0) .* cos(t)
        img .+= val .* ((xr ./ a) .^ 2 .+ (yr ./ b) .^ 2 .<= 1)
    end
    return [sum(img[(r-1)*ss+1:r*ss, (q-1)*ss+1:q*ss]) / ss^2 for r in 1:n, q in 1:n]
end

n = 32                             # 32 × 32 pixels
width = 20.0                       # field of view, cm
img_true = shepp_logan(n)
x_true = vec(permutedims(img_true))   # pixel j = (row - 1) * n + col, the same order as Python
@assert minimum(img_true) > -1e-9 && maximum(img_true) <= 1 + 1e-9   # air 0 up to skull 1 cm⁻¹
@assert img_true[23, 17] ≈ 0.2                                       # brain, near water

# --- snippet projector: The ray-projection matrix A ---
using SparseArrays

"Pixels crossed by the ray p0 + t d (d a unit vector), and the length inside each."
function ray_pixels(p0, d, n, h)
    half = n * h / 2
    edges = -half .+ h .* (0:n)
    t = sort(unique(vcat([(edges .- p0[k]) ./ d[k] for k in 1:2 if abs(d[k]) > 1e-12]...)))
    tm = (t[2:end] .+ t[1:end-1]) ./ 2
    col = floor.(Int, (p0[1] .+ d[1] .* tm .+ half) ./ h)
    row = floor.(Int, (half .- (p0[2] .+ d[2] .* tm)) ./ h)
    seg = diff(t)
    keep = (0 .<= col .< n) .& (0 .<= row .< n) .& (seg .> 1e-12)
    return row[keep] .* n .+ col[keep] .+ 1, seg[keep]
end

"Parallel-beam system matrix: one row per (angle, detector) ray, entries in cm."
function projector(n, n_angles, width)
    h = width / n
    n_det = ceil(Int, n * sqrt(2))   # enough detectors to cover the diagonal
    rows, cols, vals = Int[], Int[], Float64[]
    for k in 0:n_angles-1
        th = pi * k / n_angles
        d = [cos(th), sin(th)]       # ray direction
        nrm = [-sin(th), cos(th)]    # detector axis
        for m in 0:n_det-1
            s = (m - (n_det - 1) / 2) * h
            j, len = ray_pixels(s .* nrm .- width .* d, d, n, h)
            append!(rows, fill(k * n_det + m + 1, length(j)))
            append!(cols, j)
            append!(vals, len)
        end
    end
    return sparse(rows, cols, vals, n_angles * n_det, n * n), n_det
end

n_angles = 24                      # one view every 7.5°
A_ct, n_det = projector(n, n_angles, width)
M_ct, N_ct = size(A_ct)
mid_ray = n_det ÷ 2 + 1            # through the centre at angle 0 (horizontal)
@assert sum(A_ct[mid_ray, :]) ≈ width                  # crosses the full 20 cm
@assert M_ct > N_ct && nnz(A_ct) / (M_ct * N_ct) < 0.05 # more rays than pixels, very sparse
println("A is $M_ct × $N_ct, ", round(100 * nnz(A_ct) / (M_ct * N_ct), digits=1), "% nonzero")

# --- snippet scan: Simulated scan with photon noise ---
using Random
b_ct = A_ct * x_true               # exact line integrals
rng = Xoshiro(3)
expected = I0 .* exp.(-b_ct)       # mean photon count at each detector
# photon counts are Poisson; with counts this large a normal with equal mean and variance fits
counts = expected .+ sqrt.(expected) .* randn(rng, M_ct)
b_meas = -log.(counts ./ I0)       # the sinogram, after the logarithm
sinogram = permutedims(reshape(b_meas, n_det, n_angles))   # one row per angle
resid_ct = b_meas - b_ct #hide
@assert 0.005 < sqrt(sum(abs2, resid_ct .- sum(resid_ct) / M_ct) / M_ct) < 0.05   # noise level

# --- snippet spectrum: The singular-value spectrum ---
F_ct = svd(Matrix(A_ct))
U_ct, s_ct, Vt_ct = F_ct.U, F_ct.S, F_ct.Vt
tol_ct = s_ct[1] * max(M_ct, N_ct) * eps()   # numpy's rank cutoff, for comparison
rank_ct = count(>(tol_ct), s_ct)
@assert rank_ct < N_ct                       # a null space, despite having more rays than pixels
@assert s_ct[rank_ct] / s_ct[1] < 1e-3       # and singular values far below the largest
println("rank $rank_ct of $N_ct; σ_max = ", round(s_ct[1], digits=2),
        ", smallest kept σ = ", round(s_ct[rank_ct], sigdigits=3))

# --- snippet naive: Naive least squares ---
rel_error(x) = norm(x - x_true) / norm(x_true)

coef_ct = (U_ct[:, 1:rank_ct]' * b_meas) ./ s_ct[1:rank_ct]   # each component divided by its σ
x_naive = Vt_ct[1:rank_ct, :]' * coef_ct     # minimum-norm least-squares solution
x_clean = Vt_ct[1:rank_ct, :]' * ((U_ct[:, 1:rank_ct]' * b_ct) ./ s_ct[1:rank_ct])   # same, no noise
err_naive = rel_error(x_naive)
@assert err_naive > 3 * rel_error(x_clean)   # the noise, not the null space, ruins it
println("naive relative error ", round(err_naive, digits=2),
        " (noise-free data: ", round(rel_error(x_clean), digits=2), ")")

# --- snippet tikhonov: Tikhonov with a smoothness penalty ---
D1 = spdiagm(n - 1, n, 0 => -ones(n - 1), 1 => ones(n - 1))      # neighbour differences
L_ct = [kron(sparse(1.0I, n, n), D1); kron(D1, sparse(1.0I, n, n))]   # across, then down
AtA = Matrix(A_ct' * A_ct)
LtL = Matrix(L_ct' * L_ct)
Atb = A_ct' * b_meas
lams = 10 .^ range(-6, 1, length=15)   # λ from 10⁻⁶ to 10, two steps per decade

"Minimize ‖A x − b‖² + λ ‖L x‖² via its normal equations."
tikhonov(lam) = Symmetric(AtA + lam * LtL) \ Atb

tik_err = [rel_error(tikhonov(lam)) for lam in lams]
lam_best = lams[argmin(tik_err)]
x_tik = tikhonov(lam_best)
@assert minimum(tik_err) < err_naive / 3
@assert tik_err[1] > minimum(tik_err) && tik_err[end] > minimum(tik_err)   # too little and too much both hurt
println("Tikhonov: best λ = ", round(lam_best, sigdigits=3), ", relative error ",
        round(minimum(tik_err), digits=3))

# --- snippet art: Kaczmarz / ART: one ray at a time ---
"Kaczmarz sweeps: project x onto each ray's equation in turn; return x after each sweep."
function art(A, b, sweeps; omega=1.0)
    At = sparse(A')                  # column i of A' is ray i, stored contiguously
    row_norm2 = vec(sum(abs2, A, dims=2))
    x = zeros(size(A, 2))
    history = Vector{Vector{Float64}}()
    for _ in 1:sweeps
        for i in findall(>(0), row_norm2)
            r = nzrange(At, i)
            cols, a = rowvals(At)[r], nonzeros(At)[r]
            x[cols] .+= omega * (b[i] - dot(a, x[cols])) / row_norm2[i] .* a
        end
        push!(history, copy(x))
    end
    return x, history
end

x_art, art_history = art(A_ct, b_meas, 30)
art_err = [rel_error(v) for v in art_history]
@assert art_err[1] > art_err[2] > art_err[3] > art_err[5]   # falls quickly at first
@assert minimum(art_err) < err_naive / 3
println("ART: error ", round(art_err[1], digits=3), " after 1 sweep, ",
        round(art_err[end], digits=3), " after $(length(art_err))")
