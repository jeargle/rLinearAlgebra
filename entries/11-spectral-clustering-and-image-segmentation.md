---
id: 11
slug: spectral-clustering-and-image-segmentation
status: written
title: 'Spectral clustering: cutting a similarity graph with the eigenvectors of its Laplacian'
short_title: Spectral clustering and image segmentation
field_label: Machine learning, data clustering, computer vision, image segmentation, network community detection
tier_note: 'the clusters are read off the signs of an eigenvector of the graph Laplacian, a symmetric
  positive semidefinite matrix, so the entry needs the spectral theorem. Why that eigenvector
  approximates the best cut, the Cheeger inequality, is named in Extensions.'
nav_field: Machine Learning & Data
field: Computer Science
subfield: Machine learning/vision
tier: 2
tier_ceiling: 3
prereq_beyond_la: spectral graph theory; Cheeger inequality
scalar_field: R
vector_space: 'R^n over graph nodes: a vector x assigns one real number to every data point or pixel.
  A two-way split is a vector of ±1 entries, which is not a subspace; the relaxation drops that
  constraint and keeps only x ⊥ 1 and a fixed length'
underlying_equations: 'A graph model: data points joined by edges with similarity weights w_ij, and the
  quadratic form xᵀ L x = Σ over edges w_ij (x_i − x_j)², minimized over unit vectors orthogonal to 1'
core_la_object: Graph Laplacian eigenvectors
la_concepts: Laplacian; Fiedler vector; normalized cuts
primary_method: Sparse symmetric eigensolve
matrix_structure: sparse symmetric PSD
typical_size: 1e4-1e7
worked_example_size: 4-node weighted path (a 1 × 4 strip of pixels) with integer eigenvalues by hand
terminology:
  similarity graph: nodes for data points, edge weights w_ij for how alike points i and j are
  affinity matrix W: the symmetric n × n matrix of weights w_ij, zero diagonal
  degree d_i: row sum of W; D = diag(d_1, …, d_n)
  graph Laplacian L: L = D − W, symmetric positive semidefinite, rows summing to 0
  cut: total weight of the edges crossing a split into two groups, cut = xᵀ L x / 4 for a ±1 vector x
  algebraic connectivity: λ_2, the second-smallest eigenvalue of L; zero exactly when the graph is disconnected
  Fiedler vector: v_2, the eigenvector of λ_2; its signs give the two-way split
  connected component: a group of nodes reachable from each other; each one adds a zero eigenvalue of L
  normalized cut (Ncut): cut weighted by the total degree of each side, relaxed to L x = λ D x
  normalized Laplacian L_sym: D^(−1/2) L D^(−1/2), with the same zero pattern as L
  spectral embedding: row i of [v_2 … v_k], the coordinates of point i passed to k-means
---

## Start here

Sorting points into groups is easy when each group is a compact blob: pick a center for each group
and give every point to the nearest center. It fails when a group has a shape, such as a ring around
another ring, or a winding road in a photograph, because points on opposite sides of a ring are far
apart but still belong together.

Spectral clustering looks at a different thing: who is close to whom. Join each point to its near
neighbors with a link whose strength says how alike they are. A good split cuts the network where it
is weakest, through a few weak links rather than many strong ones.

Finding the weakest cut exactly is a hopeless search over all possible splits. A relaxed version is
an eigenvalue problem, and the signs of a single eigenvector give the split. In a photograph the
points are pixels, linked to nearby pixels of similar color, and the split separates an object from
its background.

## The problem

Some vocabulary first. A **data point** is one item to be grouped: for example a customer, a gene, or
a pixel in an image. A **similarity** w_ij ≥ 0 says how alike points i and j are; 0 means unrelated.
The points and the nonzero similarities form a **similarity graph**: points are nodes, and each pair
with w_ij > 0 is an edge of weight w_ij. Splitting the nodes into two groups, a **cut**, costs the total
weight of the edges that cross between the groups. In **image segmentation** the points are pixels,
for example a 640 × 480 photograph gives 307,200 nodes, and edges join pixels that are near each other
and similar in brightness or color.

The motivating contrast is between distance to a center and connectedness. k-means clustering, the
standard method, alternates two steps: assign every point to the nearest of k centers, then move each
center to the mean of its points. It can only produce groups separated by straight boundaries, so it
cuts a ring in half. Spectral clustering instead asks which groups are connected internally by strong
edges and to each other only by weak ones.

Given the weights w_ij, find a split of the nodes into two groups with a small cut and neither group
trivially small.

## Variables

| Symbol | Name | What it holds | Shape | Units |
|---|---|---|---|---|
| n | number of nodes | data points or pixels | integer | — |
| w_ij | similarity (edge weight) | how alike nodes i and j are; w_ij = w_ji, w_ii = 0 | scalar ≥ 0 | dimensionless |
| W | affinity matrix | the weights w_ij | n × n | dimensionless |
| d_i | degree | d_i = Σ_j w_ij, total weight at node i | scalar | dimensionless |
| D | degree matrix | diag(d_1, …, d_n) | n × n | dimensionless |
| L | graph Laplacian | L = D − W | n × n | dimensionless |
| x | node labeling | one number x_i per node; ±1 for a split, real after relaxation | n × 1 | dimensionless |
| 1 | all-ones vector | (1, 1, …, 1) | n × 1 | dimensionless |
| λ_k, v_k | eigenpairs of L | L v_k = λ_k v_k, with 0 = λ_1 ≤ λ_2 ≤ … ≤ λ_n | scalar, n × 1 | dimensionless |
| T_1, T_2 | the two groups | a split of the nodes | sets | — |
| k | number of clusters | groups wanted | integer | — |
| I_i, X_i | pixel data | intensity (gray level) and position of pixel i | scalar, 2 × 1 | gray level, pixels |
| σ_I, σ_X, r | scale parameters | intensity and distance scales; neighborhood radius | scalars | gray level, pixels, pixels |

## Formulation

**Where the equations come from.** The model is a graph: the weights are chosen from the data, and the
question is posed as minimizing a quadratic form over node labelings. No dynamics are involved.

**The familiar formula.** Every practitioner knows the cut: with the groups labeled x_i = +1 in T_1 and
x_i = −1 in T_2, an edge crossing the cut has (x_i − x_j)² = 4 and any other edge has 0, so

```
cut(T_1, T_2) = Σ over edges w_ij  =  (1/4) Σ over edges w_ij (x_i − x_j)²
```

**One node's row.** Expand the sum. Node i appears in the edges to all its neighbors, so the terms with
x_i² add up to d_i x_i², and each edge contributes a cross term −2 w_ij x_i x_j. That is row i of a
matrix: (L x)_i = d_i x_i − Σ_j w_ij x_j. The diagonal of L holds the degrees, the off-diagonal entries
are −w_ij, and every row sums to 0.

**All nodes at once.** Stacking the rows gives the graph Laplacian and its quadratic form:

```
L = D − W
xᵀ L x = Σ over edges w_ij (x_i − x_j)²  ≥  0
```

So L is symmetric positive semidefinite. Since L 1 = 0, the smallest eigenvalue is λ_1 = 0 with
eigenvector 1, the labeling that puts every node in one group. If the graph falls into separate
connected components, the indicator vector of each component is also in the null space, so the
number of zero eigenvalues equals the number of components.

Minimizing the cut over ±1 vectors is a combinatorial search. The relaxation allows any real x, but
requires x ⊥ 1, so that x cannot be the constant labeling, and fixes xᵀx so that x cannot shrink to 0.
The symbol ⊥ means "is orthogonal to": x ⊥ 1 says xᵀ1 = x_1 + x_2 + … + x_n = 0, so the entries of x
sum to zero and x must give some nodes positive values and others negative ones. By the spectral theorem the minimum of xᵀ L x / xᵀ x over x ⊥ 1 is λ_2, reached at v_2. λ_2 is called
the algebraic connectivity because it is zero exactly when the graph is disconnected and small when
the graph is nearly so. Its eigenvector v_2 is called the Fiedler vector after Miroslav Fiedler, who
studied it, and the split puts node i in T_1 when the i-th entry of v_2 is positive and in T_2
otherwise.

What is known is W, built from the data. What is solved for is v_2, and from its signs the groups.

**Worked case: a strip of four pixels.** Pixels P, Q, R, S sit in a row; P and Q are dark, R and S are
light. Similar neighbors get weight 12 and the dark-light pair Q, R gets weight 5, so the scalar
equations for (L x) are

```
(L x)_P = 12 x_P − 12 x_Q
(L x)_Q = −12 x_P + 17 x_Q − 5 x_R
(L x)_R = −5 x_Q + 17 x_R − 12 x_S
(L x)_S = −12 x_R + 12 x_S
```

and row by row:

```
      P   Q   R   S
W = [ 0   12  0   0  ]   P
    [ 12  0   5   0  ]   Q
    [ 0   5   0   12 ]   R
    [ 0   0   12  0  ]   S

D = diag(12, 17, 17, 12)

      P    Q    R    S
L = [ 12   −12  0    0   ]   P
    [ −12  17   −5   0   ]   Q
    [ 0    −5   17   −12 ]   R
    [ 0    0    −12  12  ]   S
```

The eigenvalues are 0, 4, 24 and 30, with eigenvectors (1, 1, 1, 1), (3, 2, −2, −3), (1, −1, −1, 1)
and (2, −3, 3, −2). Checking the Fiedler vector:

```
[ 12   −12  0    0   ]   [ 3  ]   [ 12  ]       [ 3  ]
[ −12  17   −5   0   ]   [ 2  ]   [ 8   ]       [ 2  ]
[ 0    −5   17   −12 ] × [ −2 ] = [ −8  ] = 4 × [ −2 ]
[ 0    0    −12  12  ]   [ −3 ]   [ −12 ]       [ −3 ]
```

The quadratic form agrees: 12 (3 − 2)² + 5 (2 + 2)² + 12 (−2 + 3)² = 104, and xᵀx = 26, so the ratio
is 104 / 26 = 4 = λ_2. The signs put P, Q in T_1 and R, S in T_2: the cut runs through the weak edge.
The exact split (1, 1, −1, −1) has quadratic form 4 × 5 = 20 and ratio 20 / 4 = 5, a little above λ_2,
as it must be because the relaxation searches a larger set. The magnitudes say more than the signs:
Q and R, next to the cut, get 2 and −2, less committed than P and S. If the weak edge is removed,
L splits into two blocks and its eigenvalues become 0, 0, 24, 24, one zero per component.

## Matrix structure

L is sparse, symmetric, positive semidefinite, with nonpositive off-diagonal entries and zero row sums.
For an image, each pixel is joined only to pixels within radius r, so a row has a few dozen nonzeros
whatever the image size. For other data, a k-nearest-neighbor graph (each point joined to its, for
example, 10 closest points) keeps W sparse; a fully connected W is dense and limited to a few
thousand points.

## What is computed

Only the few smallest eigenpairs are needed, from a sparse symmetric eigensolver: Lanczos (ARPACK
through SciPy's eigsh, usually in shift-invert mode near 0), LOBPCG (locally optimal block
preconditioned conjugate gradient), or algebraic multigrid
preconditioning for images with millions of pixels. scikit-learn's SpectralClustering builds the
graph, takes the eigenvectors and runs k-means on them. For images, the weight of Shi and Malik's
normalized cuts paper is

```
w_ij = exp(−(I_i − I_j)² / σ_I²) · exp(−‖X_i − X_j‖² / σ_X²)   if ‖X_i − X_j‖ < r, else 0
```

The Gaussian factor exp(−t²) turns a difference into a similarity between 0 and 1. For example, with
σ_I = 0.1 on a 0-to-1 gray scale, gray levels 0.1 and 0.2 give exp(−1) ≈ 0.37, while 0.1 and 0.9 give
exp(−64) ≈ 1.6 × 10⁻²⁸, effectively no edge.

## Why linear algebra is the right tool

The cut is a quadratic form, and the spectral theorem turns minimizing a quadratic form over a sphere
into an eigenvalue problem. The search over 2^n splits becomes one sparse eigensolve, and the price is
only the rounding step at the end, reading signs. Connectivity itself is linear-algebraic: the
null space of L is spanned by the indicators of the connected components, and nearly separate groups
show up as nearly zero eigenvalues.

## Pitfall worth teaching

Minimizing the plain cut favors slicing off a few outlying nodes, since a single node with weak edges
is cheap to cut off. In the worked case the cut around P alone costs 12, and a stray pixel with one
edge of weight 0.5 would cost 0.5. The unnormalized relaxation is really that of the ratio cut,
cut × (1/|T_1| + 1/|T_2|), where |T| counts nodes, which charges small groups, but on real data it still
often isolates outliers. That is why practice uses the normalized
versions in Extensions, which charge each side for its own total degree. A second trap: the
eigenvalues near 0 can be nearly equal, and then the eigensolver may return any mixture of their
eigenvectors, so the signs of v_2 alone are unreliable. Taking several eigenvectors and clustering
their rows is more stable. Finally, everything depends on W: the scales σ_I, σ_X and the number of
neighbors decide what counts as connected, and no eigensolver can recover from a poor graph.

## Extensions

The normalized cut of Shi and Malik divides each side's cut by that side's total degree. Its
relaxation is the generalized eigenproblem L x = λ D x, equivalently the normalized Laplacian L_sym =
D^(−1/2) L D^(−1/2). In the worked case it gives λ_2 = 5/17 ≈ 0.294 with eigenvector (17, 12, −12,
−17), the same split. Rewritten, L x = λ D x is D^(−1) W x = (1 − λ) x, and D^(−1) W is the
row-stochastic transition matrix of a random walk on the graph, the object of the PageRank entry:
spectral clustering looks at its second eigenvector, where PageRank looks at its first. For k > 2
clusters, the rows of [v_1 … v_k] (or [v_2 … v_k]) give each point k coordinates, and k-means on those
rows finds the groups (Ng, Jordan and Weiss normalize the rows first). The same coordinates without
the clustering step are Laplacian eigenmaps, a nonlinear dimension reduction. The guarantee that the
relaxation is not far from the best cut is the Cheeger inequality, which bounds the graph's
conductance h, the smallest ratio of a cut to the total degree of its smaller side, by λ_2 / 2 ≤ h ≤
√(2 λ_2) for L_sym; proving it needs spectral graph theory (Tier 3). The same L appears elsewhere in
the collection: in the consensus and opinion dynamics entry, where λ_2 sets how fast agents agree; in
the Massey and Colley ranking entry, as the matrix of the schedule graph; and in the resistor-network
entry, with conductances as weights. The population-genetics entry plays the opposite role: its
singular value decomposition (SVD), used there for principal component analysis (PCA), keeps the
largest eigenvalues of a similarity-like matrix rather than the smallest of a Laplacian.