# Distance geometry for NMR structures: coordinates from distances through the Gram matrix

### Start here

A ruler cannot reach inside a protein, but a magnet can sense which atoms are near which. A protein
measured this way yields a list of statements such as "these two hydrogen atoms are less than 5 Å
apart", where 1 Å (ångström) is 10⁻¹⁰ m, about the size of one atom, plus the bond lengths and angles that
chemistry fixes. The task is to turn that list of distances into a three-dimensional shape.

If every distance were known exactly, one [eigenvalue](https://en.wikipedia.org/wiki/Eigenvalues_and_eigenvectors) computation would give the shape, up to moving,
turning and mirroring it. Real data give only some distances, and only as ranges, so practice adds an
optimization on top.

**Field:** Structural biology, protein NMR, molecular modeling, sensor network localization, [multidimensional scaling](https://en.wikipedia.org/wiki/Multidimensional_scaling)  
**Tier:** 2 — complete distances become coordinates through the eigenvectors of a [symmetric](https://en.wikipedia.org/wiki/Symmetric_matrix) [positive semidefinite](https://en.wikipedia.org/wiki/Definite_matrix) [Gram matrix](https://en.wikipedia.org/wiki/Gram_matrix), so the entry needs the [spectral theorem](https://en.wikipedia.org/wiki/Spectral_theorem). Fitting incomplete distance bounds as a [semidefinite program](https://en.wikipedia.org/wiki/Semidefinite_programming) needs convex analysis and duality and is named in Extensions (Tier 3).  
**Scalar field:** R  
**Vectors:** R^3n coordinates, one point x_i in R^3 per atom; the Gram matrix G lives in Sym_n, the space of symmetric n × n matrices. The matrices that are Gram matrices of real points form the positive semidefinite cone, which is closed under sums and positive scaling but is not a subspace  
**Underlying equations:** Euclidean geometry: d_ij² = ‖x_i − x_j‖², which expands by the [law of cosines](https://en.wikipedia.org/wiki/Law_of_cosines) into [inner products](https://en.wikipedia.org/wiki/Inner_product_space), so that the centered Gram matrix is G = −½ J D^(2) J with J = I − (1/n) 1 1ᵀ

### The problem

Some vocabulary first. A **conformation** is one three-dimensional arrangement of a molecule's atoms,
described by the coordinates of every atom. **[Nuclear magnetic resonance](https://en.wikipedia.org/wiki/Nuclear_magnetic_resonance_spectroscopy_of_proteins) (NMR)** spectroscopy places
the sample in a strong magnetic field and records radio-frequency signals from atomic nuclei, mainly
the protons of hydrogen atoms. The **[nuclear Overhauser effect](https://en.wikipedia.org/wiki/Nuclear_Overhauser_effect) (NOE)** is a transfer of magnetization
between two protons through space; its strength falls off as the inverse sixth power of their distance,
so a peak appears only for proton pairs closer than roughly 5 to 6 Å, where 1 Å (ångström) is 10⁻¹⁰ m.
For example, an NOE between protons on two residues far apart in sequence says the chain folds back. An
NOE peak is converted into an **upper bound** on a distance, not a value, because its intensity also
depends on motion and relaxation. Covalent geometry (bond lengths and bond angles) fixes other
distances almost exactly, and the sum of two atoms' [van der Waals radii](https://en.wikipedia.org/wiki/Van_der_Waals_radius) gives a **lower bound** for
every pair, since atoms cannot overlap.

The motivating contrast is between coordinates and distances. [X-ray crystallography](https://en.wikipedia.org/wiki/X-ray_crystallography) produces an
electron density map in which the atoms can be placed at coordinates. NMR produces relations between
pairs of atoms, which do not depend on where the molecule is or how it is turned. **[Distance geometry](https://en.wikipedia.org/wiki/Distance_geometry)**
is the mathematics of going from such pairwise distances to coordinates.

The core of it, posed here, is the exact version: given all pairwise distances among n points, find
coordinates that reproduce them, and say when no such coordinates exist. The same computation, known
in statistics as **classical multidimensional scaling (MDS)**, draws maps from tables of dissimilarities.

### Variables

| Symbol | Name | What it holds | Shape | Units |
|---|---|---|---|---|
| n | number of points | atoms (or protons) in the model | integer | — |
| x_i | position of point i | its Cartesian coordinates | 3 × 1 | Å |
| X | coordinate matrix | row i is x_iᵀ | n × 3 | Å |
| d_ij | distance | ‖x_i − x_j‖ between points i and j, e.g. d_PQ | scalar ≥ 0 | Å |
| l_ij, u_ij | distance bounds | lower bound (contact, covalent) and upper bound (NOE, covalent) | scalars | Å |
| D^(2) | squared-distance matrix | entry (i, j) is d_ij² | n × n | Å² |
| I | identity matrix | ones on the diagonal | n × n | dimensionless |
| 1 | all-ones vector | (1, 1, …, 1) | n × 1 | dimensionless |
| J | centering matrix | I − (1/n) 1 1ᵀ | n × n | dimensionless |
| G | Gram matrix (metric matrix) | entry g_ij = x_i · x_j, coordinates measured from the centroid | n × n | Å² |
| λ_k, v_k | eigenpairs of G | G v_k = λ_k v_k, with λ_1 ≥ λ_2 ≥ … ≥ λ_n and ‖v_k‖ = 1 | scalar, n × 1 | Å², dimensionless |
| Λ_3, V_3 | top three eigenpairs | diag(λ_1, λ_2, λ_3) and the columns [v_1 v_2 v_3] | 3 × 3, n × 3 | Å², dimensionless |
| U | orthogonal matrix | a rotation (det U = 1) or a rotation with a mirror (det U = −1) | 3 × 3 | dimensionless |
| t | translation | a shift applied to every point | 3 × 1 | Å |

### Formulation

**Where the equations come from.** The model is Euclidean geometry: d_ij² = ‖x_i − x_j‖². What is
known is the matrix of distances d_ij (in the exact case, all of them). What is solved for is X. The
equation is quadratic in X, and the step that makes it linear algebra is to solve for the inner products
x_i · x_j first.

**The familiar formula.** The law of cosines says that a triangle with sides a, b and c, and angle θ
between a and b, has c² = a² + b² − 2ab cos θ. Put point 0 at the origin and take a = d_0i, b = d_0j,
c = d_ij. Since ab cos θ is the dot product x_i · x_j,

```
x_i · x_j = (d_0i² + d_0j² − d_ij²) / 2
```

So distances determine all the inner products of the points measured from point 0, and the inner
products determine the shape.

**One entry, centered.** Using one atom as the origin favors it. Classical MDS instead puts the origin at
the centroid, the average of all the points. Expanding d_ij² = ‖x_i‖² + ‖x_j‖² − 2 x_i · x_j and
averaging over i, over j, and over both gives, when the points are centered and the means are taken
over the entries of D^(2),

```
g_ij = x_i · x_j = −½ ( d_ij² − (mean of row i) − (mean of column j) + (mean of all entries) )
```

Here D^(2) is the entrywise square of the distance matrix: each entry d_ij is squared on its own, so a
distance √2 becomes 2. It is not the matrix product of the distance matrix with itself.

**All entries at once.** Subtracting row and column means is what J does. J times a vector subtracts the
vector's mean from every entry: for example, with n = 4, J (1, 2, 3, 6) = (−2, −1, 0, 3), since the mean
is 3. Multiplying by J on both sides centers rows and columns, so

```
G = −½ J D^(2) J        and        G = X Xᵀ
```

The second equation says G is symmetric positive semidefinite (vᵀ G v = ‖Xᵀ v‖² ≥ 0 for every v) with
rank at most 3. By the spectral theorem G = V Λ Vᵀ, and keeping the three nonzero eigenvalues gives

```
X = V_3 Λ_3^(1/2)
```

where Λ_3^(1/2) is diagonal with entries √λ_1, √λ_2, √λ_3. The **embedding dimension**, the
smallest dimension in which the points fit, is the number of positive eigenvalues. A negative eigenvalue
proves that no points in any dimension have the given distances.

The answer is unique only up to X U + 1 tᵀ, a rotation or reflection U followed by a shift t, since both
leave every distance unchanged. Centering removes t. U remains, and it includes det U = −1, the mirror
image.

**Worked case: a unit square.** Take four points P, Q, R, S at the corners of a square with side 1, in
that order around the square. The four sides have d² = 1 and the two diagonals have d_PR² = d_QS² = 2.
Written as scalar facts about unknown positions,

```
‖x_P − x_Q‖² = 1    ‖x_Q − x_R‖² = 1    ‖x_R − x_S‖² = 1    ‖x_S − x_P‖² = 1
‖x_P − x_R‖² = 2    ‖x_Q − x_S‖² = 2
```

The known matrices, row by row:

```
          P  Q  R  S
D^(2) = [ 0  1  2  1 ]   P
        [ 1  0  1  2 ]   Q
        [ 2  1  0  1 ]   R
        [ 1  2  1  0 ]   S

      P     Q     R     S
J = [ 3/4   −1/4  −1/4  −1/4 ]   P
    [ −1/4  3/4   −1/4  −1/4 ]   Q
    [ −1/4  −1/4  3/4   −1/4 ]   R
    [ −1/4  −1/4  −1/4  3/4  ]   S
```

Every row and column of D^(2) has mean 1, and so does the whole matrix, so the component formula gives
g_ij = −½ (d_ij² − 1). For example, g_PP = −½ (0 − 1) = 1/2, g_PQ = −½ (1 − 1) = 0 and
g_PR = −½ (2 − 1) = −1/2:

```
      P     Q     R     S
G = [ 1/2   0     −1/2  0    ]   P
    [ 0     1/2   0     −1/2 ]   Q
    [ −1/2  0     1/2   0    ]   R
    [ 0     −1/2  0     1/2  ]   S
```

The eigenvalues of G are 1, 1, 0 and 0. Two positive eigenvalues say the four points lie in a plane.
Checking one eigenvector:

```
[ 1/2   0     −1/2  0    ]   [ 1  ]   [ 1  ]       [ 1  ]
[ 0     1/2   0     −1/2 ]   [ 0  ]   [ 0  ]       [ 0  ]
[ −1/2  0     1/2   0    ] × [ −1 ] = [ −1 ] = 1 × [ −1 ]
[ 0     −1/2  0     1/2  ]   [ 0  ]   [ 0  ]       [ 0  ]
```

and (0, 1, 0, −1) works the same way. Normalizing each to length 1 (dividing by √2) and multiplying by
√1 gives the coordinates:

```
      x       y
X = [ 0.707   0      ]   P
    [ 0       0.707  ]   Q
    [ −0.707  0      ]   R
    [ 0       −0.707 ]   S
```

Every distance checks: d_PQ = √(0.5 + 0.5) = 1 and d_PR = 1.414 = √2. This is the original square with
its center at the origin, turned by 135°. The eigenvalue 1 is repeated, so an eigensolver may return any
orthonormal pair from its eigenspace, which is the same square at another angle.

**Changing the diagonals.** Keep the four sides at 1 and set both diagonals to d² = c. For c = 1 all six
distances are 1, and G has eigenvalues 1/2, 1/2, 1/2 and 0: three positive, the regular tetrahedron,
which needs three dimensions. For c = 3 the computation gives

```
              P   Q   R   S
G = 1/8 × [ 5   1   −7  1  ]   P
            [ 1   5   1   −7 ]   Q
            [ −7  1   5   1  ]   R
            [ 1   −7  1   5  ]   S
```

with eigenvalues 1.5, 1.5, 0 and −0.5; the last belongs to (1, −1, 1, −1). The negative eigenvalue says
no such points exist in any dimension. A direct check is [Euler's quadrilateral theorem](https://en.wikipedia.org/wiki/Euler's_quadrilateral_theorem): the four squared
sides of a quadrilateral, flat or not, add up to at least the two squared diagonals, here 4 < 3 + 3.
Keeping only the positive eigenvalues gives the nearest planar answer, a square with sides 1.225 and
diagonals 1.732: the diagonals survive and the sides stretch.

### Matrix structure

G is dense, symmetric and positive semidefinite in the exact case, with every row summing to zero
(G 1 = 0, because the points are centered) and [rank](https://en.wikipedia.org/wiki/Rank_%28linear_algebra%29) 3 for a molecule. D^(2) is dense too, but in NMR
most of its entries are unknown: of the roughly n²/2 pairs, only bonded neighbors and protons within
5 to 6 Å are constrained, a small fraction for a protein of 100 residues.

### What is computed

Only the three largest eigenpairs of G, from a dense symmetric eigensolver (numpy.linalg.eigh, or
scipy.linalg.eigh with subset_by_index) or [Lanczos](https://en.wikipedia.org/wiki/Lanczos_algorithm) for large n. The classical
NMR pipeline, from Crippen and Havel, works around the missing data: bound smoothing tightens each
interval [l_ij, u_ij] with the [triangle inequality](https://en.wikipedia.org/wiki/Triangle_inequality), metrization picks one distance from each interval,
classical MDS embeds the result, and [simulated annealing](https://en.wikipedia.org/wiki/Simulated_annealing) then refines the coordinates against the
original bounds and the covalent geometry. Programs in use include XPLOR-NIH and CYANA (whose
predecessor DIANA works in torsion-angle space rather than through G). Each run starts from different
random choices, and the ensemble of 20 or so structures that satisfy the bounds is deposited together.

### Why linear algebra is the right tool

Distances are quadratic in the coordinates, but inner products are linear in G, and the law of cosines
turns one into the other. In terms of G the problem is a symmetric matrix with known rank, and the
spectral theorem gives both the coordinates and a test of consistency: the dimension is the count of
positive eigenvalues, and impossible data show up as negative ones.

### Pitfall worth teaching

Distances cannot tell a molecule from its mirror image. X U with det U = −1 fits every distance, and for a
protein it is the version built from D-amino acids, with left-handed helices. The hand must be fixed by
other data. The sign of a [determinant](https://en.wikipedia.org/wiki/Determinant) does it: for four atoms, det [x_Q − x_P, x_R − x_P, x_S − x_P] is
six times their signed volume, and a [chirality](https://en.wikipedia.org/wiki/Chirality_%28chemistry%29) restraint on the four atoms around each α-carbon fixes the
sign. A second trap is filling missing distances with the upper bound or the middle of the interval:
the matrix is then rarely a [Euclidean distance matrix](https://en.wikipedia.org/wiki/Euclidean_distance_matrix), G gets large negative eigenvalues, and dropping
them tends to compress or distort the fold.

### Extensions

With bounds instead of distances, the question becomes: find a positive semidefinite G, with G 1 = 0,
whose implied distances g_ii + g_jj − 2 g_ij fall between l_ij² and u_ij². The constraints are linear
in G, so this is a semidefinite program (SDP), a linear objective over symmetric matrices required to
be positive semidefinite, and the next rung of the ladder that the [linear programming](https://en.wikipedia.org/wiki/Linear_programming) entry and the
portfolio optimization entry begin: a linear program optimizes over a polyhedron, a quadratic program
adds a quadratic objective, and an SDP replaces the nonnegative vector by a positive semidefinite
matrix. Its theory needs convex analysis and duality (Tier 3). The same relaxation is used for
sensor network localization, where radios estimate distances to neighbors and a few anchors
have known positions. Classical MDS of Euclidean distances is [principal component analysis](https://en.wikipedia.org/wiki/Principal_component_analysis) (PCA) of the centered
coordinates: G = X Xᵀ and Xᵀ X share their nonzero eigenvalues, and the embedding is the PCA score
matrix, as in the population genetics entry. The geodetic network adjustment entry also turns distances
into positions, and its datum defect is the same rotation and translation freedom seen here. The 3D
rotations entry describes U and the difference between det U = 1 and det U = −1. The older test of
whether distances fit in a given dimension uses [Cayley–Menger](https://en.wikipedia.org/wiki/Cayley%E2%80%93Menger_determinant) determinants, bordered determinants of
D^(2) that give squared volumes of triangles and tetrahedra.

### Terminology

How this field's vocabulary reads as linear algebra.

| Domain term | In linear algebra |
|---|---|
| distance geometry | recovering point coordinates from some or all of their pairwise distances |
| NOE restraint | an upper bound u_ij on the distance between two protons, from a nuclear Overhauser effect peak |
| distance bounds l_ij, u_ij | lower and upper limits on d_ij; equal when the distance is fixed by covalent geometry |
| squared-distance matrix D^(2) | the n × n matrix of d_ij², symmetric with zero diagonal |
| centering matrix J | I − (1/n) 1 1ᵀ, the projection that subtracts the mean |
| metric matrix (Gram matrix) G | G = X Xᵀ = −½ J D^(2) J, entries g_ij = x_i · x_j about the centroid |
| embedding | coordinates X = V_3 Λ_3^(1/2) from the three largest eigenpairs of G |
| embedding dimension | the number of positive eigenvalues of G, rank(G) |
| classical multidimensional scaling (MDS) | the same eigendecomposition used to draw data from dissimilarities |
| mirror image (enantiomer) | X U with det U = −1; it fits every distance equally well |
| chirality restraint | the sign of a determinant (signed volume) of four atoms, which fixes the hand |

---

[Back to the index](/r/LinearAlgebra/wiki/applications)
