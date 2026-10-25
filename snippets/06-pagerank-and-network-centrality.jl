# Julia version of notebooks/06-pagerank-and-network-centrality.py: a four-page toy web, then
# 137 linear-algebra articles on Wikipedia, using the notebook's variable names. Runs as it
# stands, with only the LinearAlgebra standard library:
#
#     julia 06-pagerank-and-network-centrality.jl
#
# Each section is shown on the entry page (except the data) next to its Python twin. The
# @assert lines check the results: the toy against the numbers worked by hand, the Wikipedia
# network against properties that any version of it must have. Julia counts from 1, so page
# and article indices are one larger than in the Python file. Lines ending in #hide run but
# are not shown.

# --- snippet setup: The toy web ---
using LinearAlgebra
pages_toy = ["A", "B", "C", "D"]
# column j: where a surfer on page j goes next. A links to B and C; B to C; C to A; D to C.
P_toy = [0   0 1 0
         0.5 0 0 0
         0.5 1 0 1
         0   0 0 0]
@assert all(sum(P_toy, dims=1) .≈ 1)       # column-stochastic: every column sums to 1

# --- snippet by_hand: Without damping: the eigenvector for eigenvalue 1 ---
eigenvalues, eigenvectors = eigen(P_toy)
k1 = argmin(abs.(eigenvalues .- 1))
r_hand = real(eigenvectors[:, k1])
r_hand = r_hand / sum(r_hand)               # scale so the entries sum to 1
@assert isapprox(r_hand, [0.4, 0.2, 0.4, 0], atol=1e-12)
@show r_hand

# --- snippet damped: With damping: solve (I − α P) r = (1 − α)/n 1 ---
alpha = 0.85                                # the slider
n_toy = length(pages_toy)
G_toy = alpha * P_toy .+ (1 - alpha) / n_toy   # the Google matrix
r_toy = (I - alpha * P_toy) \ fill((1 - alpha) / n_toy, n_toy)
@assert G_toy * r_toy ≈ r_toy && sum(r_toy) ≈ 1
@assert r_toy[4] ≈ (1 - alpha) / n_toy      # nobody links to D: it gets only random jumps
@show r_toy

# --- snippet power: Power iteration ---
r = fill(1 / n_toy, n_toy)                  # start from the uniform distribution
history = [r]
for _ in 1:40
    global r = G_toy * r                    # one round of clicking
    push!(history, r)
end
errors = [sum(abs, h - r_toy) for h in history]
lambda2_toy = sort(abs.(eigvals(G_toy)))[end-1]   # second-largest |eigenvalue|
@assert lambda2_toy ≈ alpha * sqrt(0.5)     # α times |−½ ± ½i| for P_toy
@assert errors[end] < 1e-8
@show lambda2_toy

# --- snippet periodic: A web that goes round in a circle ---
P_cycle = copy(P_toy)
P_cycle[:, 1] = [0, 1, 0, 0]                # delete the link A → C: now A → B → C → A
r_cycle = [1.0, 0, 0, 0]                          # start on page A
cycle_undamped = [r_cycle]
for _ in 1:30
    global r_cycle = P_cycle * r_cycle                  # no damping: the surfer never settles
    push!(cycle_undamped, r_cycle)
end
@assert cycle_undamped[31] ≈ cycle_undamped[28]   # period 3, forever
eigenvalues_cycle = eigvals(P_cycle)
@assert all(sort(abs.(eigenvalues_cycle))[end-2:end] .≈ 1)   # three eigenvalues on |λ| = 1

# --- snippet dangling: A page with no links ---
P_dang = copy(P_toy)
P_dang[:, 4] .= 0                           # delete D's link: column D is now all zeros
r_naive = fill(1 / n_toy, n_toy)
for _ in 1:200
    global r_naive = alpha * (P_dang * r_naive) .+ (1 - alpha) / n_toy   # unpatched: probability leaks away
end
mass_naive = sum(r_naive)
dangling_toy = vec(sum(P_dang, dims=1) .== 0)
P_patched = P_dang + ones(n_toy) * dangling_toy' / n_toy   # D now links to every page
r_dang = (I - alpha * P_patched) \ fill((1 - alpha) / n_toy, n_toy)
@assert mass_naive < 0.8 && sum(r_dang) ≈ 1
@show mass_naive r_dang

# --- snippet data: The Wikipedia network ---
# BEGIN WIKIPEDIA DATA: Wikipedia, revisions as of 2026-10-01; 137 articles, 2120 links (written by data/prepare_wikipedia_links.py)
titles = [
    "Adjugate matrix", "Affine geometry", "Affine group", "Affine space", "Affine transformation",
    "Basic Linear Algebra Subprograms", "Basis (linear algebra)", "Bivector", "Block matrix",
    "Cartesian coordinate system", "Category of modules", "Cauchy–Binet formula",
    "Cayley–Hamilton theorem", "Change of basis", "Characteristic polynomial",
    "Cholesky decomposition", "Circulant matrix", "Clifford algebra", "Coordinate vector",
    "Cramer's rule", "Cyclic subspace", "Definite matrix", "Determinant", "Diagonal matrix",
    "Dimension (vector space)", "Dimension theorem for vector spaces", "Dot product", "Dual space",
    "Eigenvalues and eigenvectors", "Elementary matrix", "Euclidean group", "Euclidean space",
    "Examples of vector spaces", "Exterior algebra", "Flat (geometry)",
    "Floating-point arithmetic", "Galilean transformation", "Gamas's theorem",
    "Gaussian elimination", "Geometric algebra", "Gram–Schmidt process", "Hankel matrix",
    "Haynsworth inertia additivity formula", "Hermitian matrix", "Hessenberg matrix",
    "Hessian matrix", "Higher-order singular value decomposition", "Homography",
    "Householder transformation", "Improper rotation", "Indefinite orthogonal group",
    "Inner product space", "Invertible matrix", "Jordan normal form", "Kernel (linear algebra)",
    "LU decomposition", "Least squares", "Linear algebra", "Linear combination", "Linear equation",
    "Linear form", "Linear independence", "Linear least squares", "Linear map", "Linear span",
    "Linear subspace", "Logical matrix", "Matrix (mathematics)", "Matrix addition",
    "Matrix congruence", "Matrix consimilarity", "Matrix decomposition", "Matrix equivalence",
    "Matrix multiplication", "Matrix similarity", "Minor (linear algebra)",
    "Moore–Penrose inverse", "Multilinear algebra", "Multivector", "Normed vector space",
    "Null vector", "Nullity theorem", "Numerical linear algebra", "Numerical stability",
    "Orientation (geometry)", "Orthogonal complement", "Orthogonal group", "Orthogonal matrix",
    "Orthogonality", "Outer product", "Overcompleteness", "Perron–Frobenius theorem", "Pfaffian",
    "Poincaré group", "Polar decomposition", "Projection (linear algebra)", "Projective geometry",
    "Projective linear group", "Projective space", "Pseudo-Euclidean space", "QR decomposition",
    "Quadric", "Rank (linear algebra)", "Rank–nullity theorem", "Reducing subspace",
    "Row and column spaces", "Row equivalence", "Schur complement", "Schur decomposition",
    "Shear mapping", "Singular value decomposition", "Skew-Hermitian matrix",
    "Skew-symmetric matrix", "Sparse matrix", "Spectral theorem", "Spectrum of a matrix",
    "Squeeze mapping", "Stochastic matrix", "Strassen algorithm", "Symmetric algebra",
    "Symmetric matrix", "Symplectic geometry", "System of linear equations", "Tensor",
    "Tensor (intrinsic definition)", "Tensor algebra", "Toeplitz matrix",
    "Topological vector space", "Trace (linear algebra)", "Transpose", "Triangular matrix",
    "Tridiagonal matrix", "Unitary matrix", "Vandermonde matrix", "Vector space",
    "Weyr canonical form", "Woodbury matrix identity",
]
links = [   # links[j]: indices of the articles that article j links to (1-based)
    [7, 12, 13, 15, 20, 23, 24, 25, 34, 44, 52, 53, 55, 58, 64, 68, 76, 88, 103, 112, 113, 121, 123, 129, 130, 131, 133, 135],
    [3, 4, 5, 48, 58, 81, 97, 99, 110, 117, 135],
    [4, 5, 9, 29, 32, 48, 54, 74, 75, 87, 94, 97, 110, 135],
    [2, 3, 5, 7, 10, 25, 32, 35, 48, 52, 59, 65, 66, 68, 98, 99, 106, 123, 135],
    [2, 3, 4, 10, 23, 32, 35, 48, 50, 53, 64, 68, 74, 88, 99, 103, 110, 117, 135],
    [9, 27, 58, 74, 83, 114, 119, 130, 131, 135],
    [4, 10, 19, 25, 26, 52, 59, 62, 64, 65, 68, 80, 99, 128, 135],
    [7, 10, 15, 18, 23, 27, 29, 32, 34, 40, 66, 78, 79, 85, 86, 88, 89, 97, 113, 124, 135],
    [15, 23, 24, 29, 53, 54, 56, 64, 68, 108, 119, 127, 129, 130, 132, 135],
    [4, 5, 7, 32, 52, 58, 88, 110, 130, 135],
    [26, 58, 64, 135],
    [23, 27, 34, 52, 58, 59, 68, 74, 76, 103, 126],
    [1, 7, 9, 15, 23, 25, 29, 34, 53, 54, 58, 59, 60, 64, 65, 76, 129, 130, 135],
    [7, 19, 23, 24, 25, 29, 32, 53, 59, 62, 64, 68, 75, 88, 102, 115, 121, 130, 135],
    [7, 13, 23, 29, 34, 53, 54, 58, 64, 75, 76, 109, 129, 130, 131, 135],
    [22, 24, 27, 39, 44, 46, 53, 56, 58, 63, 72, 74, 75, 76, 84, 88, 90, 101, 123, 131, 135],
    [15, 23, 25, 29, 39, 44, 53, 58, 60, 68, 77, 103, 121, 127, 130, 135],
    [7, 25, 34, 40, 64, 66, 87, 89, 120, 124, 126, 135],
    [7, 10, 14, 25, 29, 53, 58, 59, 64, 68, 130, 135],
    [1, 23, 32, 39, 53, 58, 68, 119, 123],
    [25, 29, 58, 64, 66, 128, 135],
    [9, 14, 15, 16, 23, 24, 27, 29, 30, 39, 44, 46, 52, 53, 56, 62, 65, 68, 70, 75, 76, 88, 108, 115, 121, 127, 129, 130, 131, 133, 135],
    [1, 9, 12, 15, 16, 17, 20, 22, 24, 25, 29, 30, 32, 34, 39, 44, 46, 52, 53, 56, 59, 62, 64, 65, 68, 75, 76, 83, 88, 93, 101, 104, 108, 111, 114, 123, 129, 130, 131, 135],
    [1, 6, 9, 15, 17, 23, 29, 30, 53, 54, 58, 62, 64, 68, 69, 74, 75, 111, 114, 115, 121, 127, 129, 131, 132, 133],
    [7, 26, 64, 66, 104, 129, 135],
    [7, 25, 59, 62, 64, 68, 104, 135],
    [6, 10, 19, 23, 32, 34, 52, 68, 74, 80, 89, 90, 100, 124, 130, 135],
    [7, 25, 32, 61, 62, 64, 66, 68, 74, 80, 86, 124, 128, 130, 135],
    [7, 15, 22, 23, 24, 25, 27, 36, 39, 44, 49, 53, 54, 55, 58, 59, 60, 64, 66, 68, 72, 75, 76, 88, 89, 92, 102, 103, 110, 113, 114, 116, 117, 121, 124, 129, 131, 133],
    [23, 24, 39, 56, 58, 68, 110, 123, 131],
    [2, 3, 5, 32, 50, 87, 88, 94],
    [4, 7, 10, 19, 25, 27, 41, 52, 58, 64, 65, 66, 87, 100, 135],
    [7, 25, 28, 55, 58, 64, 66, 68, 74, 135],
    [4, 7, 8, 12, 18, 23, 25, 28, 32, 40, 52, 58, 59, 61, 62, 64, 65, 66, 68, 76, 78, 79, 99, 100, 103, 113, 120, 125, 126, 135],
    [4, 32, 58, 62, 123],
    [29, 53, 83, 84],
    [58, 65, 74, 94, 110, 135],
    [62, 78, 124, 135],
    [9, 22, 23, 30, 36, 41, 53, 56, 62, 68, 72, 84, 103, 123, 124, 131, 135],
    [2, 4, 8, 9, 18, 24, 27, 28, 32, 34, 49, 50, 52, 66, 74, 79, 81, 88, 90, 93, 94, 96, 97, 99, 100, 115, 121, 122, 126],
    [16, 22, 23, 27, 30, 32, 39, 40, 44, 49, 52, 58, 62, 65, 68, 84, 88, 96, 101, 103, 131],
    [23, 29, 53, 58, 68, 103, 111, 121, 127, 134],
    [9, 29, 44, 53, 77, 108],
    [22, 24, 25, 29, 52, 53, 58, 64, 74, 89, 111, 112, 113, 115, 121, 130, 133, 135],
    [15, 29, 49, 58, 72, 101, 131, 132, 133, 134],
    [22, 23, 29, 55, 64, 76, 121, 124],
    [78, 96, 111, 124, 133],
    [4, 29, 32, 53, 58, 97, 98, 99, 129, 135],
    [6, 23, 44, 45, 52, 58, 64, 75, 83, 84, 88, 89, 90, 101, 130, 132, 133],
    [5, 31, 32, 64, 87, 88, 124],
    [9, 23, 24, 25, 29, 52, 64, 68, 87, 94, 117, 121, 130, 135],
    [5, 7, 10, 18, 22, 25, 27, 32, 34, 40, 41, 44, 58, 61, 62, 64, 66, 80, 86, 88, 89, 90, 115, 121, 125, 128, 129, 130, 133, 135],
    [1, 7, 23, 24, 27, 29, 30, 39, 41, 55, 56, 58, 59, 72, 74, 76, 77, 89, 103, 104, 106, 107, 111, 123, 130, 137],
    [7, 9, 13, 15, 25, 29, 44, 55, 58, 62, 64, 66, 72, 75, 104, 109, 115, 131, 135, 136],
    [7, 25, 27, 35, 36, 39, 52, 64, 65, 66, 74, 86, 89, 96, 103, 104, 106, 123, 128, 130, 135],
    [9, 16, 22, 23, 24, 39, 44, 49, 53, 58, 62, 68, 72, 74, 76, 84, 90, 101, 114, 123, 130, 131],
    [59, 63, 77, 96],
    [4, 6, 7, 10, 14, 15, 19, 20, 23, 24, 25, 26, 28, 29, 30, 32, 39, 40, 41, 48, 52, 53, 54, 55, 59, 60, 61, 62, 64, 65, 66, 68, 74, 75, 78, 80, 83, 99, 103, 121, 123, 130, 135],
    [4, 7, 32, 58, 62, 65, 66, 123, 128, 135],
    [4, 5, 10, 23, 32, 58, 62, 64, 99, 123],
    [5, 7, 27, 28, 32, 52, 55, 59, 64, 66, 74, 80, 89, 128, 129, 135],
    [7, 23, 39, 58, 59, 65, 68, 123, 135],
    [57, 72, 106, 130, 134],
    [5, 7, 24, 25, 32, 55, 58, 59, 61, 65, 66, 68, 69, 74, 80, 96, 103, 104, 110, 117, 124, 128, 135],
    [7, 59, 62, 66, 135],
    [4, 10, 21, 25, 28, 30, 35, 39, 52, 55, 58, 61, 65, 68, 81, 86, 100, 103, 106, 123, 128, 135],
    [68, 74, 90, 121, 130],
    [1, 7, 9, 13, 14, 15, 18, 20, 22, 23, 24, 25, 27, 28, 29, 30, 32, 39, 44, 46, 52, 53, 54, 55, 56, 58, 59, 60, 62, 63, 64, 67, 69, 73, 74, 76, 83, 84, 87, 88, 89, 103, 104, 109, 110, 111, 113, 114, 115, 117, 118, 119, 121, 123, 124, 129, 130, 131, 133, 135],
    [68, 74, 135],
    [7, 14, 25, 29, 52, 53, 73, 75, 121, 135],
    [44, 54, 58, 64, 68, 75, 130],
    [9, 16, 22, 24, 29, 36, 39, 44, 45, 54, 56, 58, 62, 68, 77, 84, 88, 101, 103, 109, 112, 113, 121, 123, 130, 131, 133],
    [7, 14, 30, 53, 58, 64, 68, 70, 75, 103, 107],
    [7, 9, 10, 15, 19, 23, 24, 27, 29, 53, 58, 64, 68, 69, 75, 83, 90, 119, 123, 129, 130, 135],
    [7, 14, 15, 23, 24, 29, 53, 54, 58, 64, 68, 70, 73, 103, 115, 129, 133],
    [1, 12, 20, 22, 23, 34, 44, 53, 58, 68, 74, 78, 103, 130],
    [15, 16, 17, 24, 28, 32, 36, 44, 53, 55, 58, 62, 63, 68, 86, 96, 101, 103, 106, 111, 121, 123, 131, 135, 137],
    [18, 20, 23, 28, 34, 40, 52, 64, 68, 79, 90, 120, 123, 124, 125, 126, 135],
    [4, 8, 18, 28, 34, 40, 52, 59, 78, 99, 124, 135],
    [28, 32, 52, 64, 128, 135],
    [7, 62, 89, 100, 135],
    [9, 53, 55],
    [6, 7, 24, 29, 36, 41, 49, 56, 58, 63, 68, 88, 101, 111, 114, 131, 133],
    [29, 83],
    [10, 29, 32, 40, 87, 88],
    [27, 28, 52, 55, 58, 64, 66, 89, 100, 106, 135],
    [8, 9, 18, 23, 24, 25, 27, 29, 31, 32, 34, 49, 51, 52, 53, 55, 64, 68, 70, 74, 86, 88, 113, 115, 121, 122, 130, 135],
    [9, 10, 14, 16, 18, 22, 23, 24, 25, 27, 29, 32, 36, 39, 41, 49, 50, 52, 53, 58, 60, 62, 63, 64, 65, 68, 72, 74, 77, 81, 83, 84, 87, 89, 95, 96, 101, 111, 113, 115, 121, 123, 130, 131, 133],
    [52],
    [9, 19, 23, 27, 28, 32, 34, 49, 52, 57, 58, 62, 67, 74, 81, 103, 111, 124, 126, 129, 130, 135],
    [7, 58, 59],
    [15, 29, 54, 66, 68, 75, 96, 115, 116, 118],
    [14, 23, 29, 34, 46, 53, 68, 76, 87, 88, 113, 130, 132],
    [3, 31, 37, 110],
    [10, 22, 23, 44, 53, 64, 68, 72, 88, 101, 111, 121, 133],
    [7, 22, 25, 27, 29, 41, 45, 49, 52, 55, 58, 61, 63, 64, 66, 68, 69, 74, 77, 80, 86, 89, 90, 101, 103, 111, 129, 130, 135],
    [2, 5, 32, 48, 58, 98, 99],
    [23, 24, 25, 48, 62, 74, 87, 97, 99, 135],
    [2, 4, 7, 10, 28, 32, 40, 48, 55, 58, 62, 64, 66, 97, 98, 128, 135],
    [2, 4, 7, 18, 25, 27, 32, 35, 50, 51, 52, 65, 66, 81, 85, 86, 89, 117, 124, 135],
    [16, 23, 32, 36, 39, 41, 49, 52, 53, 56, 58, 62, 63, 65, 68, 72, 76, 84, 88, 89, 95, 103, 106, 111, 131, 133],
    [4, 5, 10, 19, 25, 29, 32, 48, 53, 55, 60, 65, 68, 99, 103, 130, 131, 135],
    [7, 25, 30, 36, 39, 53, 55, 56, 58, 59, 62, 64, 65, 68, 76, 89, 101, 104, 106, 111, 123, 124, 125, 130, 135],
    [7, 25, 55, 58, 59, 62, 64, 66, 68, 103, 135],
    [7, 9, 14, 25, 58, 64, 66, 86, 96],
    [7, 10, 25, 27, 30, 33, 35, 39, 52, 55, 58, 59, 62, 64, 65, 66, 68, 74, 86, 89, 103, 104, 111, 123, 130, 135],
    [7, 30, 39, 53, 55, 58, 59, 68, 73, 86, 103, 106, 123],
    [9, 39, 43, 56, 58, 68, 103, 121, 123, 137],
    [15, 22, 24, 29, 45, 58, 64, 72, 75, 88, 111, 116, 131, 133],
    [5, 9, 10, 22, 23, 29, 30, 37, 53, 64, 66, 68, 74, 86, 103, 129, 130, 135],
    [7, 22, 24, 27, 29, 32, 44, 47, 49, 52, 55, 57, 58, 63, 64, 65, 68, 72, 77, 83, 88, 90, 95, 101, 103, 104, 106, 110, 115, 121, 123, 130, 133],
    [27, 44, 58, 64, 113, 121, 133, 135],
    [7, 8, 9, 22, 23, 24, 25, 29, 52, 53, 58, 64, 75, 88, 93, 112, 115, 121, 129, 130, 133, 135],
    [9, 16, 24, 67, 68, 132],
    [15, 23, 24, 25, 27, 29, 44, 52, 54, 58, 64, 68, 72, 86, 109, 111, 116, 121, 131, 133],
    [7, 15, 23, 25, 29, 64, 68, 72, 74, 129, 135],
    [10, 14, 51, 58, 64, 87, 89, 110],
    [29, 58, 92],
    [9, 28, 39, 53, 58, 68, 74, 84],
    [4, 18, 25, 34, 64, 126, 135],
    [7, 16, 17, 22, 24, 29, 42, 44, 46, 52, 53, 54, 58, 64, 70, 74, 88, 95, 113, 115, 127, 130, 133],
    Int[],
    [7, 10, 16, 22, 23, 25, 30, 35, 39, 53, 55, 56, 58, 59, 60, 62, 64, 65, 66, 68, 77, 83, 103, 114, 121, 127, 135],
    [7, 8, 14, 23, 25, 27, 28, 34, 52, 53, 61, 64, 68, 79, 90, 125, 126, 129, 135],
    [7, 25, 28, 39, 58, 61, 64, 68, 78, 90, 103, 106, 124, 135],
    [7, 11, 18, 28, 34, 64, 78, 120, 124, 135],
    [7, 17, 23, 42, 53, 56, 58, 64, 66, 68, 74, 84, 121, 123, 131, 135],
    [7, 25, 28, 32, 52, 59, 61, 64, 65, 66, 80, 135],
    [1, 7, 9, 15, 23, 24, 25, 27, 28, 29, 44, 52, 53, 54, 55, 58, 59, 61, 64, 68, 74, 75, 90, 96, 103, 121, 130, 131, 135],
    [1, 6, 7, 15, 22, 23, 25, 27, 28, 29, 44, 52, 53, 54, 58, 64, 68, 69, 74, 75, 76, 77, 87, 88, 96, 112, 113, 121, 128, 133, 135],
    [9, 13, 15, 16, 23, 24, 29, 39, 45, 53, 54, 56, 67, 74, 75, 76, 101, 109, 127, 130, 132, 133],
    [23, 29, 44, 45, 53, 58, 68, 75, 121, 127, 135],
    [23, 29, 44, 52, 53, 58, 68, 72, 75, 87, 88, 112, 115],
    [14, 23, 30, 34, 53, 56, 58, 64, 68, 103, 123, 130, 131, 135],
    [2, 4, 7, 10, 11, 15, 19, 23, 25, 26, 27, 28, 29, 32, 34, 41, 52, 54, 55, 58, 59, 62, 64, 65, 66, 68, 74, 78, 80, 85, 89, 104, 115, 120, 123, 124, 125, 126, 128],
    [7, 9, 24, 29, 30, 53, 54, 55, 58, 75, 103, 135],
    [22, 23, 53, 58, 68, 77, 83, 84, 108, 111, 135],
]
# END WIKIPEDIA DATA  #hide

# --- snippet matrix: The link matrix ---
n_wiki = length(titles)
outdeg = length.(links)
P_wiki = zeros(n_wiki, n_wiki)
for (j, row) in enumerate(links)
    P_wiki[row, j] .= 1 / max(length(row), 1)   # column j: 1/outdeg(j) on each article j links to
end
indeg = vec(sum(P_wiki .> 0, dims=2))       # number of articles that link to each article
dangling = outdeg .== 0
@assert all(sum(P_wiki, dims=1)[.!dangling] .≈ 1) && count(dangling) >= 1
println("articles: ", n_wiki, "  links: ", sum(outdeg), "  dangling: ", titles[dangling])

# --- snippet pagerank: PageRank without forming G ---
function pagerank(P, alpha; v=nothing, tol=1e-10, max_iter=1000)
    # Power iteration for r = α S r + (1 − α) v, never forming G or S. S is P with each
    # dangling (all-zero) column replaced by 1/n everywhere; v is where random jumps land,
    # uniform unless given. Returns (r, errors): the change made by each step.
    n = size(P, 1)
    v = isnothing(v) ? fill(1 / n, n) : v
    dangling = vec(sum(P, dims=1) .== 0)
    r, errors = fill(1 / n, n), Float64[]
    for _ in 1:max_iter
        r_next = alpha * (P * r) .+ alpha * sum(r[dangling]) / n + (1 - alpha) * v
        push!(errors, sum(abs, r_next - r))
        r = r_next
        errors[end] < tol && break
    end
    return r, errors
end

alpha_wiki = 0.85                           # the slider
r_wiki, errors_wiki = pagerank(P_wiki, alpha_wiki)
@assert sum(r_wiki) ≈ 1 && all(r_wiki .> 0) && length(errors_wiki) < 100
for j in sortperm(r_wiki, rev=true)[1:10]
    println(round(r_wiki[j], digits=4), "  ", lpad(indeg[j], 3), " in-links  ", titles[j])
end

# --- snippet convergence: How fast: the second eigenvalue ---
S_wiki = P_wiki + ones(n_wiki) * dangling' / n_wiki   # dangling columns patched
G_wiki = alpha_wiki * S_wiki .+ (1 - alpha_wiki) / n_wiki   # formed only to check
lambda2_S = sort(abs.(eigvals(S_wiki)))[end-1]
lambda2_G = sort(abs.(eigvals(G_wiki)))[end-1]
@assert lambda2_G ≈ alpha_wiki * lambda2_S && lambda2_G <= alpha_wiki
@show lambda2_S lambda2_G length(errors_wiki)

# --- snippet personalized: Personalized PageRank ---
target = findfirst(==("Singular value decomposition"), titles)   # the dropdown
v = zeros(n_wiki)
v[target] = 1                               # every random jump returns to one article
r_pers, _ = pagerank(P_wiki, alpha_wiki; v=v)
lift = r_pers ./ r_wiki                     # > 1: visited more because jumps return to target
@assert sum(r_pers) ≈ 1 && argmax(r_pers) == target
for j in filter(!=(target), sortperm(lift, rev=true))[1:8]
    println("lift ", round(lift[j], digits=1), "  ", titles[j])
end
