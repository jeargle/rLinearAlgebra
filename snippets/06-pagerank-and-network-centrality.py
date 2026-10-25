# Python version of notebooks/06-pagerank-and-network-centrality.py: a four-page toy web, then
# 137 linear-algebra articles on Wikipedia, using the notebook's variable names. Runs as it
# stands, with only numpy:
#
#     python 06-pagerank-and-network-centrality.py
#
# Each section is shown on the entry page (except the data) next to its Julia twin. The assert
# lines check the results: the toy against the numbers worked by hand, the Wikipedia network
# against properties that any version of it must have. Lines ending in #hide run but are not
# shown.

# --- snippet setup: The toy web ---
import numpy as np
pages_toy = ["A", "B", "C", "D"]
# column j: where a surfer on page j goes next. A links to B and C; B to C; C to A; D to C.
P_toy = np.array([[0,   0, 1, 0],
                  [0.5, 0, 0, 0],
                  [0.5, 1, 0, 1],
                  [0,   0, 0, 0]])
assert np.allclose(P_toy.sum(axis=0), 1)    # column-stochastic: every column sums to 1

# --- snippet by_hand: Without damping: the eigenvector for eigenvalue 1 ---
eigenvalues, eigenvectors = np.linalg.eig(P_toy)
k1 = np.argmin(abs(eigenvalues - 1))
r_hand = np.real(eigenvectors[:, k1])
r_hand = r_hand / r_hand.sum()              # scale so the entries sum to 1
assert np.allclose(r_hand, [0.4, 0.2, 0.4, 0])
print("r_hand =", r_hand)

# --- snippet damped: With damping: solve (I − α P) r = (1 − α)/n 1 ---
alpha = 0.85                                # the slider
n_toy = len(pages_toy)
G_toy = alpha * P_toy + (1 - alpha) / n_toy * np.ones((n_toy, n_toy))   # the Google matrix
r_toy = np.linalg.solve(np.eye(n_toy) - alpha * P_toy, (1 - alpha) / n_toy * np.ones(n_toy))
assert np.allclose(G_toy @ r_toy, r_toy) and np.isclose(r_toy.sum(), 1)
assert np.isclose(r_toy[3], (1 - alpha) / n_toy)   # nobody links to D: it gets only random jumps
print("r_toy =", r_toy)

# --- snippet power: Power iteration ---
r = np.full(n_toy, 1 / n_toy)               # start from the uniform distribution
history = [r]
for _ in range(40):
    r = G_toy @ r                           # one round of clicking
    history.append(r)
errors = [abs(h - r_toy).sum() for h in history]
lambda2_toy = sorted(abs(np.linalg.eigvals(G_toy)))[-2]   # second-largest |eigenvalue|
assert np.isclose(lambda2_toy, alpha * np.sqrt(0.5))       # α times |−½ ± ½i| for P_toy
assert errors[-1] < 1e-8
print("lambda2_toy =", lambda2_toy)

# --- snippet periodic: A web that goes round in a circle ---
P_cycle = P_toy.copy()
P_cycle[:, 0] = [0, 1, 0, 0]                # delete the link A → C: now A → B → C → A
r_cycle = np.array([1.0, 0, 0, 0])                # start on page A
cycle_undamped = [r_cycle]
for _ in range(30):
    r_cycle = P_cycle @ r_cycle                         # no damping: the surfer never settles
    cycle_undamped.append(r_cycle)
assert np.allclose(cycle_undamped[30], cycle_undamped[27])   # period 3, forever
eigenvalues_cycle = np.linalg.eigvals(P_cycle)
assert np.allclose(sorted(abs(eigenvalues_cycle))[-3:], 1)   # three eigenvalues on |λ| = 1

# --- snippet dangling: A page with no links ---
P_dang = P_toy.copy()
P_dang[:, 3] = 0                            # delete D's link: column D is now all zeros
r_naive = np.full(n_toy, 1 / n_toy)
for _ in range(200):
    r_naive = alpha * (P_dang @ r_naive) + (1 - alpha) / n_toy   # unpatched: probability leaks away
mass_naive = r_naive.sum()
dangling_toy = P_dang.sum(axis=0) == 0
P_patched = P_dang + np.outer(np.ones(n_toy), dangling_toy) / n_toy   # D now links to every page
r_dang = np.linalg.solve(np.eye(n_toy) - alpha * P_patched, (1 - alpha) / n_toy * np.ones(n_toy))
assert mass_naive < 0.8 and np.isclose(r_dang.sum(), 1)
print("mass_naive =", mass_naive, " r_dang =", r_dang)

# --- snippet data: The Wikipedia network ---
# BEGIN WIKIPEDIA DATA: Wikipedia, revisions as of 2026-10-01; 137 articles, 2120 links (written by data/prepare_wikipedia_links.py)
titles = [
    'Adjugate matrix', 'Affine geometry', 'Affine group', 'Affine space', 'Affine transformation',
    'Basic Linear Algebra Subprograms', 'Basis (linear algebra)', 'Bivector', 'Block matrix',
    'Cartesian coordinate system', 'Category of modules', 'Cauchy–Binet formula',
    'Cayley–Hamilton theorem', 'Change of basis', 'Characteristic polynomial',
    'Cholesky decomposition', 'Circulant matrix', 'Clifford algebra', 'Coordinate vector',
    "Cramer's rule", 'Cyclic subspace', 'Definite matrix', 'Determinant', 'Diagonal matrix',
    'Dimension (vector space)', 'Dimension theorem for vector spaces', 'Dot product', 'Dual space',
    'Eigenvalues and eigenvectors', 'Elementary matrix', 'Euclidean group', 'Euclidean space',
    'Examples of vector spaces', 'Exterior algebra', 'Flat (geometry)',
    'Floating-point arithmetic', 'Galilean transformation', "Gamas's theorem",
    'Gaussian elimination', 'Geometric algebra', 'Gram–Schmidt process', 'Hankel matrix',
    'Haynsworth inertia additivity formula', 'Hermitian matrix', 'Hessenberg matrix',
    'Hessian matrix', 'Higher-order singular value decomposition', 'Homography',
    'Householder transformation', 'Improper rotation', 'Indefinite orthogonal group',
    'Inner product space', 'Invertible matrix', 'Jordan normal form', 'Kernel (linear algebra)',
    'LU decomposition', 'Least squares', 'Linear algebra', 'Linear combination', 'Linear equation',
    'Linear form', 'Linear independence', 'Linear least squares', 'Linear map', 'Linear span',
    'Linear subspace', 'Logical matrix', 'Matrix (mathematics)', 'Matrix addition',
    'Matrix congruence', 'Matrix consimilarity', 'Matrix decomposition', 'Matrix equivalence',
    'Matrix multiplication', 'Matrix similarity', 'Minor (linear algebra)',
    'Moore–Penrose inverse', 'Multilinear algebra', 'Multivector', 'Normed vector space',
    'Null vector', 'Nullity theorem', 'Numerical linear algebra', 'Numerical stability',
    'Orientation (geometry)', 'Orthogonal complement', 'Orthogonal group', 'Orthogonal matrix',
    'Orthogonality', 'Outer product', 'Overcompleteness', 'Perron–Frobenius theorem', 'Pfaffian',
    'Poincaré group', 'Polar decomposition', 'Projection (linear algebra)', 'Projective geometry',
    'Projective linear group', 'Projective space', 'Pseudo-Euclidean space', 'QR decomposition',
    'Quadric', 'Rank (linear algebra)', 'Rank–nullity theorem', 'Reducing subspace',
    'Row and column spaces', 'Row equivalence', 'Schur complement', 'Schur decomposition',
    'Shear mapping', 'Singular value decomposition', 'Skew-Hermitian matrix',
    'Skew-symmetric matrix', 'Sparse matrix', 'Spectral theorem', 'Spectrum of a matrix',
    'Squeeze mapping', 'Stochastic matrix', 'Strassen algorithm', 'Symmetric algebra',
    'Symmetric matrix', 'Symplectic geometry', 'System of linear equations', 'Tensor',
    'Tensor (intrinsic definition)', 'Tensor algebra', 'Toeplitz matrix',
    'Topological vector space', 'Trace (linear algebra)', 'Transpose', 'Triangular matrix',
    'Tridiagonal matrix', 'Unitary matrix', 'Vandermonde matrix', 'Vector space',
    'Weyr canonical form', 'Woodbury matrix identity',
]
links = [   # links[j]: indices of the articles that article j links to
    [6, 11, 12, 14, 19, 22, 23, 24, 33, 43, 51, 52, 54, 57, 63, 67, 75, 87, 102, 111, 112, 120, 122, 128, 129, 130, 132, 134],
    [2, 3, 4, 47, 57, 80, 96, 98, 109, 116, 134],
    [3, 4, 8, 28, 31, 47, 53, 73, 74, 86, 93, 96, 109, 134],
    [1, 2, 4, 6, 9, 24, 31, 34, 47, 51, 58, 64, 65, 67, 97, 98, 105, 122, 134],
    [1, 2, 3, 9, 22, 31, 34, 47, 49, 52, 63, 67, 73, 87, 98, 102, 109, 116, 134],
    [8, 26, 57, 73, 82, 113, 118, 129, 130, 134],
    [3, 9, 18, 24, 25, 51, 58, 61, 63, 64, 67, 79, 98, 127, 134],
    [6, 9, 14, 17, 22, 26, 28, 31, 33, 39, 65, 77, 78, 84, 85, 87, 88, 96, 112, 123, 134],
    [14, 22, 23, 28, 52, 53, 55, 63, 67, 107, 118, 126, 128, 129, 131, 134],
    [3, 4, 6, 31, 51, 57, 87, 109, 129, 134],
    [25, 57, 63, 134],
    [22, 26, 33, 51, 57, 58, 67, 73, 75, 102, 125],
    [0, 6, 8, 14, 22, 24, 28, 33, 52, 53, 57, 58, 59, 63, 64, 75, 128, 129, 134],
    [6, 18, 22, 23, 24, 28, 31, 52, 58, 61, 63, 67, 74, 87, 101, 114, 120, 129, 134],
    [6, 12, 22, 28, 33, 52, 53, 57, 63, 74, 75, 108, 128, 129, 130, 134],
    [21, 23, 26, 38, 43, 45, 52, 55, 57, 62, 71, 73, 74, 75, 83, 87, 89, 100, 122, 130, 134],
    [14, 22, 24, 28, 38, 43, 52, 57, 59, 67, 76, 102, 120, 126, 129, 134],
    [6, 24, 33, 39, 63, 65, 86, 88, 119, 123, 125, 134],
    [6, 9, 13, 24, 28, 52, 57, 58, 63, 67, 129, 134],
    [0, 22, 31, 38, 52, 57, 67, 118, 122],
    [24, 28, 57, 63, 65, 127, 134],
    [8, 13, 14, 15, 22, 23, 26, 28, 29, 38, 43, 45, 51, 52, 55, 61, 64, 67, 69, 74, 75, 87, 107, 114, 120, 126, 128, 129, 130, 132, 134],
    [0, 8, 11, 14, 15, 16, 19, 21, 23, 24, 28, 29, 31, 33, 38, 43, 45, 51, 52, 55, 58, 61, 63, 64, 67, 74, 75, 82, 87, 92, 100, 103, 107, 110, 113, 122, 128, 129, 130, 134],
    [0, 5, 8, 14, 16, 22, 28, 29, 52, 53, 57, 61, 63, 67, 68, 73, 74, 110, 113, 114, 120, 126, 128, 130, 131, 132],
    [6, 25, 63, 65, 103, 128, 134],
    [6, 24, 58, 61, 63, 67, 103, 134],
    [5, 9, 18, 22, 31, 33, 51, 67, 73, 79, 88, 89, 99, 123, 129, 134],
    [6, 24, 31, 60, 61, 63, 65, 67, 73, 79, 85, 123, 127, 129, 134],
    [6, 14, 21, 22, 23, 24, 26, 35, 38, 43, 48, 52, 53, 54, 57, 58, 59, 63, 65, 67, 71, 74, 75, 87, 88, 91, 101, 102, 109, 112, 113, 115, 116, 120, 123, 128, 130, 132],
    [22, 23, 38, 55, 57, 67, 109, 122, 130],
    [1, 2, 4, 31, 49, 86, 87, 93],
    [3, 6, 9, 18, 24, 26, 40, 51, 57, 63, 64, 65, 86, 99, 134],
    [6, 24, 27, 54, 57, 63, 65, 67, 73, 134],
    [3, 6, 7, 11, 17, 22, 24, 27, 31, 39, 51, 57, 58, 60, 61, 63, 64, 65, 67, 75, 77, 78, 98, 99, 102, 112, 119, 124, 125, 134],
    [3, 31, 57, 61, 122],
    [28, 52, 82, 83],
    [57, 64, 73, 93, 109, 134],
    [61, 77, 123, 134],
    [8, 21, 22, 29, 35, 40, 52, 55, 61, 67, 71, 83, 102, 122, 123, 130, 134],
    [1, 3, 7, 8, 17, 23, 26, 27, 31, 33, 48, 49, 51, 65, 73, 78, 80, 87, 89, 92, 93, 95, 96, 98, 99, 114, 120, 121, 125],
    [15, 21, 22, 26, 29, 31, 38, 39, 43, 48, 51, 57, 61, 64, 67, 83, 87, 95, 100, 102, 130],
    [22, 28, 52, 57, 67, 102, 110, 120, 126, 133],
    [8, 28, 43, 52, 76, 107],
    [21, 23, 24, 28, 51, 52, 57, 63, 73, 88, 110, 111, 112, 114, 120, 129, 132, 134],
    [14, 28, 48, 57, 71, 100, 130, 131, 132, 133],
    [21, 22, 28, 54, 63, 75, 120, 123],
    [77, 95, 110, 123, 132],
    [3, 28, 31, 52, 57, 96, 97, 98, 128, 134],
    [5, 22, 43, 44, 51, 57, 63, 74, 82, 83, 87, 88, 89, 100, 129, 131, 132],
    [4, 30, 31, 63, 86, 87, 123],
    [8, 22, 23, 24, 28, 51, 63, 67, 86, 93, 116, 120, 129, 134],
    [4, 6, 9, 17, 21, 24, 26, 31, 33, 39, 40, 43, 57, 60, 61, 63, 65, 79, 85, 87, 88, 89, 114, 120, 124, 127, 128, 129, 132, 134],
    [0, 6, 22, 23, 26, 28, 29, 38, 40, 54, 55, 57, 58, 71, 73, 75, 76, 88, 102, 103, 105, 106, 110, 122, 129, 136],
    [6, 8, 12, 14, 24, 28, 43, 54, 57, 61, 63, 65, 71, 74, 103, 108, 114, 130, 134, 135],
    [6, 24, 26, 34, 35, 38, 51, 63, 64, 65, 73, 85, 88, 95, 102, 103, 105, 122, 127, 129, 134],
    [8, 15, 21, 22, 23, 38, 43, 48, 52, 57, 61, 67, 71, 73, 75, 83, 89, 100, 113, 122, 129, 130],
    [58, 62, 76, 95],
    [3, 5, 6, 9, 13, 14, 18, 19, 22, 23, 24, 25, 27, 28, 29, 31, 38, 39, 40, 47, 51, 52, 53, 54, 58, 59, 60, 61, 63, 64, 65, 67, 73, 74, 77, 79, 82, 98, 102, 120, 122, 129, 134],
    [3, 6, 31, 57, 61, 64, 65, 122, 127, 134],
    [3, 4, 9, 22, 31, 57, 61, 63, 98, 122],
    [4, 6, 26, 27, 31, 51, 54, 58, 63, 65, 73, 79, 88, 127, 128, 134],
    [6, 22, 38, 57, 58, 64, 67, 122, 134],
    [56, 71, 105, 129, 133],
    [4, 6, 23, 24, 31, 54, 57, 58, 60, 64, 65, 67, 68, 73, 79, 95, 102, 103, 109, 116, 123, 127, 134],
    [6, 58, 61, 65, 134],
    [3, 9, 20, 24, 27, 29, 34, 38, 51, 54, 57, 60, 64, 67, 80, 85, 99, 102, 105, 122, 127, 134],
    [67, 73, 89, 120, 129],
    [0, 6, 8, 12, 13, 14, 17, 19, 21, 22, 23, 24, 26, 27, 28, 29, 31, 38, 43, 45, 51, 52, 53, 54, 55, 57, 58, 59, 61, 62, 63, 66, 68, 72, 73, 75, 82, 83, 86, 87, 88, 102, 103, 108, 109, 110, 112, 113, 114, 116, 117, 118, 120, 122, 123, 128, 129, 130, 132, 134],
    [67, 73, 134],
    [6, 13, 24, 28, 51, 52, 72, 74, 120, 134],
    [43, 53, 57, 63, 67, 74, 129],
    [8, 15, 21, 23, 28, 35, 38, 43, 44, 53, 55, 57, 61, 67, 76, 83, 87, 100, 102, 108, 111, 112, 120, 122, 129, 130, 132],
    [6, 13, 29, 52, 57, 63, 67, 69, 74, 102, 106],
    [6, 8, 9, 14, 18, 22, 23, 26, 28, 52, 57, 63, 67, 68, 74, 82, 89, 118, 122, 128, 129, 134],
    [6, 13, 14, 22, 23, 28, 52, 53, 57, 63, 67, 69, 72, 102, 114, 128, 132],
    [0, 11, 19, 21, 22, 33, 43, 52, 57, 67, 73, 77, 102, 129],
    [14, 15, 16, 23, 27, 31, 35, 43, 52, 54, 57, 61, 62, 67, 85, 95, 100, 102, 105, 110, 120, 122, 130, 134, 136],
    [17, 19, 22, 27, 33, 39, 51, 63, 67, 78, 89, 119, 122, 123, 124, 125, 134],
    [3, 7, 17, 27, 33, 39, 51, 58, 77, 98, 123, 134],
    [27, 31, 51, 63, 127, 134],
    [6, 61, 88, 99, 134],
    [8, 52, 54],
    [5, 6, 23, 28, 35, 40, 48, 55, 57, 62, 67, 87, 100, 110, 113, 130, 132],
    [28, 82],
    [9, 28, 31, 39, 86, 87],
    [26, 27, 51, 54, 57, 63, 65, 88, 99, 105, 134],
    [7, 8, 17, 22, 23, 24, 26, 28, 30, 31, 33, 48, 50, 51, 52, 54, 63, 67, 69, 73, 85, 87, 112, 114, 120, 121, 129, 134],
    [8, 9, 13, 15, 17, 21, 22, 23, 24, 26, 28, 31, 35, 38, 40, 48, 49, 51, 52, 57, 59, 61, 62, 63, 64, 67, 71, 73, 76, 80, 82, 83, 86, 88, 94, 95, 100, 110, 112, 114, 120, 122, 129, 130, 132],
    [51],
    [8, 18, 22, 26, 27, 31, 33, 48, 51, 56, 57, 61, 66, 73, 80, 102, 110, 123, 125, 128, 129, 134],
    [6, 57, 58],
    [14, 28, 53, 65, 67, 74, 95, 114, 115, 117],
    [13, 22, 28, 33, 45, 52, 67, 75, 86, 87, 112, 129, 131],
    [2, 30, 36, 109],
    [9, 21, 22, 43, 52, 63, 67, 71, 87, 100, 110, 120, 132],
    [6, 21, 24, 26, 28, 40, 44, 48, 51, 54, 57, 60, 62, 63, 65, 67, 68, 73, 76, 79, 85, 88, 89, 100, 102, 110, 128, 129, 134],
    [1, 4, 31, 47, 57, 97, 98],
    [22, 23, 24, 47, 61, 73, 86, 96, 98, 134],
    [1, 3, 6, 9, 27, 31, 39, 47, 54, 57, 61, 63, 65, 96, 97, 127, 134],
    [1, 3, 6, 17, 24, 26, 31, 34, 49, 50, 51, 64, 65, 80, 84, 85, 88, 116, 123, 134],
    [15, 22, 31, 35, 38, 40, 48, 51, 52, 55, 57, 61, 62, 64, 67, 71, 75, 83, 87, 88, 94, 102, 105, 110, 130, 132],
    [3, 4, 9, 18, 24, 28, 31, 47, 52, 54, 59, 64, 67, 98, 102, 129, 130, 134],
    [6, 24, 29, 35, 38, 52, 54, 55, 57, 58, 61, 63, 64, 67, 75, 88, 100, 103, 105, 110, 122, 123, 124, 129, 134],
    [6, 24, 54, 57, 58, 61, 63, 65, 67, 102, 134],
    [6, 8, 13, 24, 57, 63, 65, 85, 95],
    [6, 9, 24, 26, 29, 32, 34, 38, 51, 54, 57, 58, 61, 63, 64, 65, 67, 73, 85, 88, 102, 103, 110, 122, 129, 134],
    [6, 29, 38, 52, 54, 57, 58, 67, 72, 85, 102, 105, 122],
    [8, 38, 42, 55, 57, 67, 102, 120, 122, 136],
    [14, 21, 23, 28, 44, 57, 63, 71, 74, 87, 110, 115, 130, 132],
    [4, 8, 9, 21, 22, 28, 29, 36, 52, 63, 65, 67, 73, 85, 102, 128, 129, 134],
    [6, 21, 23, 26, 28, 31, 43, 46, 48, 51, 54, 56, 57, 62, 63, 64, 67, 71, 76, 82, 87, 89, 94, 100, 102, 103, 105, 109, 114, 120, 122, 129, 132],
    [26, 43, 57, 63, 112, 120, 132, 134],
    [6, 7, 8, 21, 22, 23, 24, 28, 51, 52, 57, 63, 74, 87, 92, 111, 114, 120, 128, 129, 132, 134],
    [8, 15, 23, 66, 67, 131],
    [14, 22, 23, 24, 26, 28, 43, 51, 53, 57, 63, 67, 71, 85, 108, 110, 115, 120, 130, 132],
    [6, 14, 22, 24, 28, 63, 67, 71, 73, 128, 134],
    [9, 13, 50, 57, 63, 86, 88, 109],
    [28, 57, 91],
    [8, 27, 38, 52, 57, 67, 73, 83],
    [3, 17, 24, 33, 63, 125, 134],
    [6, 15, 16, 21, 23, 28, 41, 43, 45, 51, 52, 53, 57, 63, 69, 73, 87, 94, 112, 114, 126, 129, 132],
    [],
    [6, 9, 15, 21, 22, 24, 29, 34, 38, 52, 54, 55, 57, 58, 59, 61, 63, 64, 65, 67, 76, 82, 102, 113, 120, 126, 134],
    [6, 7, 13, 22, 24, 26, 27, 33, 51, 52, 60, 63, 67, 78, 89, 124, 125, 128, 134],
    [6, 24, 27, 38, 57, 60, 63, 67, 77, 89, 102, 105, 123, 134],
    [6, 10, 17, 27, 33, 63, 77, 119, 123, 134],
    [6, 16, 22, 41, 52, 55, 57, 63, 65, 67, 73, 83, 120, 122, 130, 134],
    [6, 24, 27, 31, 51, 58, 60, 63, 64, 65, 79, 134],
    [0, 6, 8, 14, 22, 23, 24, 26, 27, 28, 43, 51, 52, 53, 54, 57, 58, 60, 63, 67, 73, 74, 89, 95, 102, 120, 129, 130, 134],
    [0, 5, 6, 14, 21, 22, 24, 26, 27, 28, 43, 51, 52, 53, 57, 63, 67, 68, 73, 74, 75, 76, 86, 87, 95, 111, 112, 120, 127, 132, 134],
    [8, 12, 14, 15, 22, 23, 28, 38, 44, 52, 53, 55, 66, 73, 74, 75, 100, 108, 126, 129, 131, 132],
    [22, 28, 43, 44, 52, 57, 67, 74, 120, 126, 134],
    [22, 28, 43, 51, 52, 57, 67, 71, 74, 86, 87, 111, 114],
    [13, 22, 29, 33, 52, 55, 57, 63, 67, 102, 122, 129, 130, 134],
    [1, 3, 6, 9, 10, 14, 18, 22, 24, 25, 26, 27, 28, 31, 33, 40, 51, 53, 54, 57, 58, 61, 63, 64, 65, 67, 73, 77, 79, 84, 88, 103, 114, 119, 122, 123, 124, 125, 127],
    [6, 8, 23, 28, 29, 52, 53, 54, 57, 74, 102, 134],
    [21, 22, 52, 57, 67, 76, 82, 83, 107, 110, 134],
]
# END WIKIPEDIA DATA  #hide

# --- snippet matrix: The link matrix ---
n_wiki = len(titles)
outdeg = np.array([len(row) for row in links])
P_wiki = np.zeros((n_wiki, n_wiki))
for j, row in enumerate(links):
    if row:
        P_wiki[row, j] = 1 / len(row)       # column j: 1/outdeg(j) on each article j links to
indeg = (P_wiki > 0).sum(axis=1)            # number of articles that link to each article
dangling = outdeg == 0
assert np.allclose(P_wiki.sum(axis=0)[~dangling], 1) and dangling.sum() >= 1
print("articles:", n_wiki, " links:", outdeg.sum(), " dangling:", [titles[j] for j in np.where(dangling)[0]])

# --- snippet pagerank: PageRank without forming G ---
def pagerank(P, alpha, v=None, tol=1e-10, max_iter=1000):
    """Power iteration for r = α S r + (1 − α) v, never forming G or S. S is P with each
    dangling (all-zero) column replaced by 1/n everywhere; v is where random jumps land,
    uniform unless given. Returns (r, errors): the change made by each step."""
    n = P.shape[0]
    v = np.full(n, 1 / n) if v is None else v
    dangling = P.sum(axis=0) == 0
    r, errors = np.full(n, 1 / n), []
    for _ in range(max_iter):
        r_next = alpha * (P @ r) + alpha * r[dangling].sum() / n + (1 - alpha) * v
        errors.append(abs(r_next - r).sum())
        r = r_next
        if errors[-1] < tol:
            break
    return r, errors

alpha_wiki = 0.85                           # the slider
r_wiki, errors_wiki = pagerank(P_wiki, alpha_wiki)
assert np.isclose(r_wiki.sum(), 1) and (r_wiki > 0).all() and len(errors_wiki) < 100
for j in np.argsort(-r_wiki)[:10]:
    print(f"{r_wiki[j]:.4f}  {indeg[j]:3d} in-links  {titles[j]}")

# --- snippet convergence: How fast: the second eigenvalue ---
S_wiki = P_wiki + np.outer(np.ones(n_wiki), dangling) / n_wiki   # dangling columns patched
G_wiki = alpha_wiki * S_wiki + (1 - alpha_wiki) / n_wiki         # formed only to check
lambda2_S = sorted(abs(np.linalg.eigvals(S_wiki)))[-2]
lambda2_G = sorted(abs(np.linalg.eigvals(G_wiki)))[-2]
assert np.isclose(lambda2_G, alpha_wiki * lambda2_S) and lambda2_G <= alpha_wiki
print("lambda2_S =", lambda2_S, " lambda2_G =", lambda2_G, " iterations:", len(errors_wiki))

# --- snippet personalized: Personalized PageRank ---
target = titles.index("Singular value decomposition")   # the dropdown
v = np.zeros(n_wiki)
v[target] = 1                               # every random jump returns to one article
r_pers, _ = pagerank(P_wiki, alpha_wiki, v=v)
lift = r_pers / r_wiki                      # > 1: visited more because jumps return to target
assert np.isclose(r_pers.sum(), 1) and np.argmax(r_pers) == target
for j in [j for j in np.argsort(-lift) if j != target][:8]:
    print(f"lift {lift[j]:.1f}  {titles[j]}")
