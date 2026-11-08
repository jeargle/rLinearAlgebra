# Domain terminology, translated

One unfamiliar word from a question, and what it means mathematically.

### Two general terms

A **field** is a number system in which addition, subtraction, multiplication, and division by any nonzero number all behave the way they do for ordinary numbers. The rational numbers ℚ, the real numbers ℝ, the complex numbers ℂ, and the integers [modulo](https://en.wikipedia.org/wiki/Modular_arithmetic) a prime p all qualify. The integers modulo 6 do not: there 2 × 3 = 0, so 2 has no reciprocal and nothing can be divided by 2. The scalars of every vector space come from a field, which is why each entry names its scalar field.

**[GF(2)](https://en.wikipedia.org/wiki/GF%282%29)** is the smallest field: just the two numbers 0 and 1, added and multiplied modulo 2, so 1 + 1 = 0. Addition is the same as [XOR](https://en.wikipedia.org/wiki/Exclusive_or), and multiplication is the same as AND. GF(p) is the same construction using the integers modulo a prime p.

### By field

| Domain term | In linear algebra | Entry |
|---|---|---|
| (k, n) scheme | a polynomial in a k-dimensional space evaluated at n distinct points | [Shamir secret sharing](applications/shamir-secret-sharing) |
| adjustment | least-squares estimation of the coordinates from redundant, inconsistent observations | [Geodetic network adjustment](applications/geodetic-network-adjustment) |
| affine combination | a weighted sum whose weights add up to 1 | [Barycentric coordinates and triangle rasterization](applications/barycentric-coordinates-and-triangle-rasterization) |
| affine invariance | transforming the control points transforms the curve, because the basis sums to 1 | [Bezier curves and font rendering](applications/bezier-curves-and-font-rendering) |
| anomaly field | the mean-centered data matrix | [Empirical orthogonal functions in climate data](applications/empirical-orthogonal-functions-in-climate-data) |
| ART / SIRT | Kaczmarz row-action and related simultaneous iterations | [Computed tomography reconstruction](applications/computed-tomography-reconstruction) |
| assembly | summing small element matrices into the global matrix at shared DOF indices | [Structural analysis of frames and trusses](applications/structural-analysis-of-frames-and-trusses) |
| attenuation coefficient | the unknown x, one value per voxel | [Computed tomography reconstruction](applications/computed-tomography-reconstruction) |
| attitude / orientation | a rotation matrix R relating a body frame to a reference frame | [3D rotations and rigid-body pose](applications/3d-rotations-and-rigid-body-pose) |
| attribute | a value stored at each corner (colour, depth, texture coordinate) and blended across the triangle | [Barycentric coordinates and triangle rasterization](applications/barycentric-coordinates-and-triangle-rasterization) |
| B-splines and knots | piecewise-cubic basis functions joined smoothly at chosen points called knots, each nonzero over only a few intervals | [Least-squares fitting in a chosen function basis](applications/least-squares-fitting-in-a-chosen-function-basis) |
| backprojection | applying A transpose to the data | [Computed tomography reconstruction](applications/computed-tomography-reconstruction) |
| balancing an equation | finding an integer null vector of the element-by-species matrix | [Stoichiometric matrices of reaction networks](applications/stoichiometric-matrices-of-reaction-networks) |
| bandwidth / skyline | the sparsity pattern induced by node numbering | [Structural analysis of frames and trusses](applications/structural-analysis-of-frames-and-trusses) |
| barycentric coordinates | the weights (α, β, γ) that write a point as a weighted average of the three corners | [Barycentric coordinates and triangle rasterization](applications/barycentric-coordinates-and-triangle-rasterization) |
| barycentric formula | a stable way to evaluate the Lagrange form | [Polynomial interpolation and change of basis](applications/polynomial-interpolation-and-change-of-basis) |
| basis functions | fixed functions of t, chosen before seeing the coefficients, whose combinations are the candidate curves | [Least-squares fitting in a chosen function basis](applications/least-squares-fitting-in-a-chosen-function-basis) |
| basis image | one of the 64 cosine patterns an 8 × 8 block is built from | [JPEG and video compression](applications/jpeg-and-video-compression) |
| basis set (quantum chemistry) | the chosen basis in which H is expressed | [Quantum mechanics and quantum computing](applications/quantum-mechanics-and-quantum-computing) |
| benchmark (station, control point) | a surveyed point; its coordinates are unknowns | [Geodetic network adjustment](applications/geodetic-network-adjustment) |
| Bernstein polynomials | a basis of P_3 consisting of nonnegative functions that sum to 1 | [Bezier curves and font rendering](applications/bezier-curves-and-font-rendering) |
| block | an 8 × 8 tile of pixels, the unit JPEG transforms and codes separately | [JPEG and video compression](applications/jpeg-and-video-compression) |
| blocking artifact | visible steps at block boundaries at high compression | [JPEG and video compression](applications/jpeg-and-video-compression) |
| body frame vs world frame | two orthonormal bases; R changes coordinates from one to the other | [3D rotations and rigid-body pose](applications/3d-rotations-and-rigid-body-pose) |
| boundary (cordon) counts | known traffic entering and leaving at the district's edge, summarized in b | [Traffic flow conservation at intersections](applications/traffic-flow-conservation-at-intersections) |
| Bradford transform | a standard chromatic adaptation matrix built on a cone-like basis | [Color spaces as change of basis](applications/color-spaces-as-change-of-basis) |
| bridge balance | a choice of resistances that puts one edge current at zero | [Resistor networks and Kirchhoff's laws](applications/resistor-networks-and-kirchhoff-s-laws) |
| bundle adjustment | sparse nonlinear least squares over all cameras and points at once | [Multiple-view geometry and structure from motion](applications/multiple-view-geometry-and-structure-from-motion) |
| burst error | errors confined to a run of consecutive bits | [CRC checksums as polynomial arithmetic modulo 2](applications/crc-checksums-as-polynomial-arithmetic-over-gf-2) |
| central, forward and one-sided differences | stencils whose offsets are symmetric about x, start at x, or lie on one side of it | [Finite-difference stencils by undetermined coefficients](applications/finite-difference-stencils-by-undetermined-coefficients) |
| centrality | a score defined as an eigenvector, or a function, of the graph matrix | [PageRank and network centrality](applications/pagerank-and-network-centrality) |
| Chebyshev polynomials and nodes | a basis and a set of nodes for which the interpolation problem is well conditioned | [Polynomial interpolation and change of basis](applications/polynomial-interpolation-and-change-of-basis) |
| check bits (checksum) | the r bits appended to a message so the receiver can test it | [CRC checksums as polynomial arithmetic modulo 2](applications/crc-checksums-as-polynomial-arithmetic-over-gf-2) |
| chromatic adaptation | the eye's adjustment to the colour of the illumination, and its modelling by a matrix | [Color spaces as change of basis](applications/color-spaces-as-change-of-basis) |
| chromaticity (x, y) | x = X/(X + Y + Z) and y = Y/(X + Y + Z), the colour with its brightness divided out | [Color spaces as change of basis](applications/color-spaces-as-change-of-basis) |
| circulation | traffic going round a closed loop, a vector in the null space of A | [Traffic flow conservation at intersections](applications/traffic-flow-conservation-at-intersections) |
| clip coordinates | the homogeneous 4-vector after the projection matrix, before division | [3D viewing and perspective projection pipeline](applications/3d-viewing-and-perspective-projection-pipeline) |
| code rate | k/n, the subspace dimension over the ambient dimension | [Linear error-correcting codes](applications/linear-error-correcting-codes) |
| codeword | an element of the k-dimensional subspace of GF(2)^n | [Linear error-correcting codes](applications/linear-error-correcting-codes) |
| codeword | a message with its check bits appended; always a multiple of G(x) | [CRC checksums as polynomial arithmetic modulo 2](applications/crc-checksums-as-polynomial-arithmetic-over-gf-2) |
| Colley matrix | 2I plus the Massey matrix | [Sports and citation ranking (Massey/Colley)](applications/sports-and-citation-ranking-massey-colley) |
| component balance | one row of the system, for one component around one unit | [Mass balance in a chemical process flowsheet](applications/mass-balance-in-a-chemical-process-flowsheet) |
| cones | the three kinds of colour receptor in the eye, most sensitive to long, medium and short wavelengths (L, M, S) | [Color spaces as change of basis](applications/color-spaces-as-change-of-basis) |
| connected schedule | one in which every team is linked to every other by a chain of games | [Sports and citation ranking (Massey/Colley)](applications/sports-and-citation-ranking-massey-colley) |
| conservation of flow (continuity) | A x = b, one equation per intersection | [Traffic flow conservation at intersections](applications/traffic-flow-conservation-at-intersections) |
| conserved moiety | a left null vector y; y^T c is constant for all time | [Stoichiometric matrices of reaction networks](applications/stoichiometric-matrices-of-reaction-networks) |
| control points | coordinates of the curve in the Bernstein basis, one point in the plane per basis polynomial | [Bezier curves and font rendering](applications/bezier-curves-and-font-rendering) |
| control polygon | the broken line through the control points; the curve lies in its convex hull | [Bezier curves and font rendering](applications/bezier-curves-and-font-rendering) |
| convex combination | an affine combination with no negative weights; these fill the triangle | [Barycentric coordinates and triangle rasterization](applications/barycentric-coordinates-and-triangle-rasterization) |
| corrupted share | an error in a Reed-Solomon codeword | [Shamir secret sharing](applications/shamir-secret-sharing) |
| covariance matrix P | the uncertainty ellipsoid; symmetric positive semidefinite | [Kalman filtering for navigation](applications/kalman-filtering-for-navigation) |
| CRC-r | a cyclic redundancy check with r check bits, such as CRC-8 or CRC-32 | [CRC checksums as polynomial arithmetic modulo 2](applications/crc-checksums-as-polynomial-arithmetic-over-gf-2) |
| cubic vs quadratic outlines (CFF/PostScript vs TrueType) | curves in P_3 vs curves in P_2 | [Bezier curves and font rendering](applications/bezier-curves-and-font-rendering) |
| current transformation matrix (CTM) | the product of every transform in effect for an element | [2D affine transforms in vector graphics](applications/2d-affine-transforms-in-vector-graphics) |
| damping factor (alpha) | the weight on P versus the uniform teleportation term | [PageRank and network centrality](applications/pagerank-and-network-centrality) |
| dangling node | a zero column, which breaks stochasticity | [PageRank and network centrality](applications/pagerank-and-network-centrality) |
| datum | the choice that fixes the null space, such as a benchmark held at a known height | [Geodetic network adjustment](applications/geodetic-network-adjustment) |
| datum defect | the dimension of the null space of the design matrix | [Geodetic network adjustment](applications/geodetic-network-adjustment) |
| DC and AC coefficients | the coefficient of the constant pattern, and those of the oscillating ones | [JPEG and video compression](applications/jpeg-and-video-compression) |
| DC component | bin 0, the coefficient of the constant vector, N times the mean | [The small DFT as a complex unitary matrix](applications/the-small-dft-as-a-complex-unitary-matrix) |
| de Casteljau algorithm | evaluation by repeated linear interpolation | [Bezier curves and font rendering](applications/bezier-curves-and-font-rendering) |
| dealer | whoever chooses the polynomial and hands out the shares | [Shamir secret sharing](applications/shamir-secret-sharing) |
| degenerate configuration | point placement that makes A rank-deficient, so the solution is not unique | [Multiple-view geometry and structure from motion](applications/multiple-view-geometry-and-structure-from-motion) |
| degraded mode | one block of each stripe unknown, recovered on every read by solving the equation | [RAID-5 parity and XOR recovery](applications/raid-5-parity-and-xor-recovery) |
| degree elevation | the inclusion P_2 → P_3, written in Bernstein coordinates | [Bezier curves and font rendering](applications/bezier-curves-and-font-rendering) |
| degree of freedom (DOF) | one scalar unknown — one component of the displacement vector | [Structural analysis of frames and trusses](applications/structural-analysis-of-frames-and-trusses) |
| degrees of freedom | dimensions; k for the model (the trace of H) and n − k for the residuals | [Least squares regression and the hat matrix](applications/least-squares-regression-and-the-hat-matrix) |
| degrees of freedom | unknowns minus independent equations; it must be zero for a unique answer | [Mass balance in a chemical process flowsheet](applications/mass-balance-in-a-chemical-process-flowsheet) |
| degrees of freedom of the network | the nullity of S | [Stoichiometric matrices of reaction networks](applications/stoichiometric-matrices-of-reaction-networks) |
| density matrix | a positive semidefinite matrix with trace 1 | [Quantum mechanics and quantum computing](applications/quantum-mechanics-and-quantum-computing) |
| depth buffer (z-buffer) | the per-pixel record of the nearest depth drawn so far | [3D viewing and perspective projection pipeline](applications/3d-viewing-and-perspective-projection-pipeline) |
| design matrix | the matrix whose column j is basis function j evaluated at every data point | [Least-squares fitting in a chosen function basis](applications/least-squares-fitting-in-a-chosen-function-basis) |
| design matrix (model matrix) X | the n × k matrix whose columns are the predictors, including a column of 1s for the intercept | [Least squares regression and the hat matrix](applications/least-squares-regression-and-the-hat-matrix) |
| direct vs indirect requirements | the successive terms A, A^2, A^3 of the Neumann series | [Leontief input-output economics](applications/leontief-input-output-economics) |
| direction cosine matrix (DCM) | the rotation matrix; its entries are cosines of angles between axes | [3D rotations and rigid-body pose](applications/3d-rotations-and-rigid-body-pose) |
| discrete cosine transform (DCT) | the change of basis from pixel values to amounts of sampled cosine waves | [JPEG and video compression](applications/jpeg-and-video-compression) |
| DLT (direct linear transform) | stacking constraints into A and taking the smallest right singular vector | [Multiple-view geometry and structure from motion](applications/multiple-view-geometry-and-structure-from-motion) |
| dummy variable trap | an exactly dependent set of indicator columns, which makes X rank-deficient | [Least squares regression and the hat matrix](applications/least-squares-regression-and-the-hat-matrix) |
| easing curve (CSS cubic-bezier) | a cubic in the same basis, used for timing instead of shape | [Bezier curves and font rendering](applications/bezier-curves-and-font-rendering) |
| edge function | a barycentric coordinate written as a linear function of the pixel position | [Barycentric coordinates and triangle rasterization](applications/barycentric-coordinates-and-triangle-rasterization) |
| effective (Thevenin) resistance | (e_a - e_b)^T L^+ (e_a - e_b), a quadratic form in the pseudoinverse | [Resistor networks and Kirchhoff's laws](applications/resistor-networks-and-kirchhoff-s-laws) |
| eigenstate / energy level | eigenvector and eigenvalue of the Hamiltonian | [Quantum mechanics and quantum computing](applications/quantum-mechanics-and-quantum-computing) |
| elementary flux mode | an extreme ray of the nonnegative part of the null space | [Stoichiometric matrices of reaction networks](applications/stoichiometric-matrices-of-reaction-networks) |
| embodied / Scope 3 emissions | an appended satellite row multiplied through the same inverse | [Leontief input-output economics](applications/leontief-input-output-economics) |
| energy compaction | concentrating most of a signal's energy in a few coordinates | [JPEG and video compression](applications/jpeg-and-video-compression) |
| entangled state | a vector that does not factor as a tensor product | [Quantum mechanics and quantum computing](applications/quantum-mechanics-and-quantum-computing) |
| EOF | a left singular vector — one spatial pattern | [Empirical orthogonal functions in climate data](applications/empirical-orthogonal-functions-in-climate-data) |
| epipolar constraint | the bilinear equation relating corresponding points in two views | [Multiple-view geometry and structure from motion](applications/multiple-view-geometry-and-structure-from-motion) |
| erasure vs error | known vs unknown error position — a column selection vs a search | [Linear error-correcting codes](applications/linear-error-correcting-codes) |
| erasure vs error | a lost block at a known position (solvable) vs a wrong block at an unknown position (only detectable) | [RAID-5 parity and XOR recovery](applications/raid-5-parity-and-xor-recovery) |
| error detection vs error correction | noticing that bits changed, versus also knowing which ones | [CRC checksums as polynomial arithmetic modulo 2](applications/crc-checksums-as-polynomial-arithmetic-over-gf-2) |
| essential / fundamental matrix | the rank-2 bilinear form satisfying x'^T E x = 0 | [Multiple-view geometry and structure from motion](applications/multiple-view-geometry-and-structure-from-motion) |
| estimable quantity | a function of the coordinates that does not depend on the datum, such as a height difference | [Geodetic network adjustment](applications/geodetic-network-adjustment) |
| expectation value | the quadratic form psi^* A psi | [Quantum mechanics and quantum computing](applications/quantum-mechanics-and-quantum-computing) |
| explained variance | sigma_i^2 as a fraction of the total | [Empirical orthogonal functions in climate data](applications/empirical-orthogonal-functions-in-climate-data) |
| extrapolation | using a fitted curve outside the range of the data | [Least-squares fitting in a chosen function basis](applications/least-squares-fitting-in-a-chosen-function-basis) |
| extrinsic parameters [R\|t] | the rigid transform from world to camera frame | [Multiple-view geometry and structure from motion](applications/multiple-view-geometry-and-structure-from-motion) |
| FFT | a factorization of the DFT matrix into sparse factors, not a different transform | [The small DFT as a complex unitary matrix](applications/the-small-dft-as-a-complex-unitary-matrix) |
| field of view | the angle the camera sees, top to bottom | [3D viewing and perspective projection pipeline](applications/3d-viewing-and-perspective-projection-pipeline) |
| filter divergence | P losing positive definiteness in finite precision, or an unobservable direction growing without bound | [Kalman filtering for navigation](applications/kalman-filtering-for-navigation) |
| filtered backprojection (FBP) | an analytic spectral inverse of the forward operator | [Computed tomography reconstruction](applications/computed-tomography-reconstruction) |
| final demand | the right-hand side d | [Leontief input-output economics](applications/leontief-input-output-economics) |
| fitted values ŷ | the orthogonal projection of y onto the column space of X | [Least squares regression and the hat matrix](applications/least-squares-regression-and-the-hat-matrix) |
| flow (volume) | cars per hour on a segment, an entry of x | [Traffic flow conservation at intersections](applications/traffic-flow-conservation-at-intersections) |
| flux | v, the vector of reaction rates | [Stoichiometric matrices of reaction networks](applications/stoichiometric-matrices-of-reaction-networks) |
| Fornberg's algorithm | a recursion that produces the weights for any offsets and derivative orders without forming the matrix | [Finite-difference stencils by undetermined coefficients](applications/finite-difference-stencils-by-undetermined-coefficients) |
| forward kinematics | the product of the joint transforms along a robot arm | [3D rotations and rigid-body pose](applications/3d-rotations-and-rigid-body-pose) |
| Fourier basis | a constant together with sines and cosines of whole-number multiples of a fundamental frequency | [Least-squares fitting in a chosen function basis](applications/least-squares-fitting-in-a-chosen-function-basis) |
| Fourier coefficients a_n, b_n | the amounts of cos nx and sin nx in the function | [Fourier series as orthogonal projection](applications/fourier-series-as-orthogonal-projection) |
| free network | a minimum-norm solution, with no point held fixed | [Geodetic network adjustment](applications/geodetic-network-adjustment) |
| frequency bin k | the coefficient of the k-th complex wave in the Fourier basis | [The small DFT as a complex unitary matrix](applications/the-small-dft-as-a-complex-unitary-matrix) |
| gamut | the set of colours a device can produce | [Color spaces as change of basis](applications/color-spaces-as-change-of-basis) |
| generator matrix G | a basis of the code, written as rows | [Linear error-correcting codes](applications/linear-error-correcting-codes) |
| generator polynomial G(x) | the fixed divisor of degree r that both ends agree on | [CRC checksums as polynomial arithmetic modulo 2](applications/crc-checksums-as-polynomial-arithmetic-over-gf-2) |
| Gibbs phenomenon | the overshoot of partial sums next to a jump, which does not shrink as N grows | [Fourier series as orthogonal projection](applications/fourier-series-as-orthogonal-projection) |
| gimbal lock | Euler angles at which two of the three angles turn about the same axis | [3D rotations and rigid-body pose](applications/3d-rotations-and-rigid-body-pose) |
| Gouraud shading | colouring a triangle by blending its corner colours | [Barycentric coordinates and triangle rasterization](applications/barycentric-coordinates-and-triangle-rasterization) |
| Gram matrix | the matrix of inner products of the basis functions | [Fourier series as orthogonal projection](applications/fourier-series-as-orthogonal-projection) |
| grid and grid spacing h | equally spaced points x + s h at which the function is known | [Finite-difference stencils by undetermined coefficients](applications/finite-difference-stencils-by-undetermined-coefficients) |
| gross / total output | the unknown x | [Leontief input-output economics](applications/leontief-input-output-economics) |
| ground (reference node) | the node whose potential is fixed at 0, removing the null space spanned by the all-ones vector | [Resistor networks and Kirchhoff's laws](applications/resistor-networks-and-kirchhoff-s-laws) |
| Hamiltonian | the Hermitian matrix H in H psi = E psi | [Quantum mechanics and quantum computing](applications/quantum-mechanics-and-quantum-computing) |
| handedness | the sign of the determinant; +1 for rotations, −1 for reflections | [3D rotations and rigid-body pose](applications/3d-rotations-and-rigid-body-pose) |
| harmonic | sin nx or cos nx, oscillating n times per period | [Fourier series as orthogonal projection](applications/fourier-series-as-orthogonal-projection) |
| hat matrix H | the projection matrix X (XᵀX)⁻¹ Xᵀ, so ŷ = H y | [Least squares regression and the hat matrix](applications/least-squares-regression-and-the-hat-matrix) |
| homogeneous coordinates | an added coordinate that turns perspective division into a linear map plus a normalization | [Multiple-view geometry and structure from motion](applications/multiple-view-geometry-and-structure-from-motion) |
| homogeneous transformation | the 4 × 4 matrix [R t; 0 1] | [3D rotations and rigid-body pose](applications/3d-rotations-and-rigid-body-pose) |
| identity transform | the 3 × 3 identity, matrix(1, 0, 0, 1, 0, 0) | [2D affine transforms in vector graphics](applications/2d-affine-transforms-in-vector-graphics) |
| initial value and final XOR | constants added in standard CRCs, which make the map affine | [CRC checksums as polynomial arithmetic modulo 2](applications/crc-checksums-as-polynomial-arithmetic-over-gf-2) |
| inner product of functions | ⟨f, g⟩ = ∫ f g dx, the continuous analogue of the dot product | [Fourier series as orthogonal projection](applications/fourier-series-as-orthogonal-projection) |
| innovation / residual | z - Hx, the part of the measurement the prediction did not explain | [Kalman filtering for navigation](applications/kalman-filtering-for-navigation) |
| interpolant | the unique element of P_d with the prescribed values at the nodes | [Polynomial interpolation and change of basis](applications/polynomial-interpolation-and-change-of-basis) |
| intrinsic matrix K | the camera's internal calibration, an upper-triangular 3x3 | [Multiple-view geometry and structure from motion](applications/multiple-view-geometry-and-structure-from-motion) |
| inverse DFT | the change of basis back, using the conjugate transpose | [The small DFT as a complex unitary matrix](applications/the-small-dft-as-a-complex-unitary-matrix) |
| Kalman gain | the projection weight matrix that blends prediction and measurement | [Kalman filtering for navigation](applications/kalman-filtering-for-navigation) |
| ket / state vector | a unit vector in a complex inner-product space | [Quantum mechanics and quantum computing](applications/quantum-mechanics-and-quantum-computing) |
| Kirchhoff's current law (KCL) | A^T I = s, a statement about the left null space of A | [Resistor networks and Kirchhoff's laws](applications/resistor-networks-and-kirchhoff-s-laws) |
| Kirchhoff's voltage law (KVL) | voltage drops lie in the column space of A, so they sum to zero around every loop | [Resistor networks and Kirchhoff's laws](applications/resistor-networks-and-kirchhoff-s-laws) |
| Lagrange coefficients | the weights λ_i, which depend only on which parties are present | [Shamir secret sharing](applications/shamir-secret-sharing) |
| Lagrange form | coordinates in the basis that is dual to evaluation at the nodes, so the coordinates are the data values themselves | [Polynomial interpolation and change of basis](applications/polynomial-interpolation-and-change-of-basis) |
| Lebesgue constant | how much the interpolation map can amplify errors in the data | [Polynomial interpolation and change of basis](applications/polynomial-interpolation-and-change-of-basis) |
| Leontief inverse | (I - A)^-1 | [Leontief input-output economics](applications/leontief-input-output-economics) |
| levelling (spirit levelling) | measuring height differences between benchmarks | [Geodetic network adjustment](applications/geodetic-network-adjustment) |
| leverage h_ii | the i-th diagonal entry of H; how strongly observation i pulls its own fitted value | [Least squares regression and the hat matrix](applications/least-squares-regression-and-the-hat-matrix) |
| linear and encoded RGB | light intensities, versus the values stored in files after the transfer function (often loosely called gamma) | [Color spaces as change of basis](applications/color-spaces-as-change-of-basis) |
| linear least squares | least squares in which the coefficients enter linearly, whatever the shape of the basis functions | [Least-squares fitting in a chosen function basis](applications/least-squares-fitting-in-a-chosen-function-basis) |
| link (road segment) | one coordinate of the flow vector | [Traffic flow conservation at intersections](applications/traffic-flow-conservation-at-intersections) |
| link closure | forcing a coordinate of x to zero, which may leave no admissible solution | [Traffic flow conservation at intersections](applications/traffic-flow-conservation-at-intersections) |
| link matrix | the column-stochastic matrix P built from the graph | [PageRank and network centrality](applications/pagerank-and-network-centrality) |
| load vector | the right-hand side f | [Structural analysis of frames and trusses](applications/structural-analysis-of-frames-and-trusses) |
| loading | one entry of an EOF, i.e. one grid point's weight in that pattern | [Empirical orthogonal functions in climate data](applications/empirical-orthogonal-functions-in-climate-data) |
| local vs global coordinates | reading a product right to left (each step in the parent's frame) or left to right (each step in the newly moved frame) | [2D affine transforms in vector graphics](applications/2d-affine-transforms-in-vector-graphics) |
| lookup table | precomputed CRCs of all 256 byte values, for software that works a byte at a time | [CRC checksums as polynomial arithmetic modulo 2](applications/crc-checksums-as-polynomial-arithmetic-over-gf-2) |
| loop (mesh) currents | coordinates in a basis of the cycle space, the null space of A^T, dimension m - n + 1 | [Resistor networks and Kirchhoff's laws](applications/resistor-networks-and-kirchhoff-s-laws) |
| luminance Y | the brightness coordinate of XYZ | [Color spaces as change of basis](applications/color-spaces-as-change-of-basis) |
| margin of victory | the winner's points minus the loser's points in one game | [Sports and citation ranking (Massey/Colley)](applications/sports-and-citation-ranking-massey-colley) |
| Massey matrix | the T × T normal-equations matrix, games played on the diagonal and minus the number of meetings off it | [Sports and citation ranking (Massey/Colley)](applications/sports-and-citation-ranking-massey-colley) |
| matrix(a, b, c, d, e, f) | the SVG/CSS notation for the 3 × 3 matrix with columns (a, b, 0), (c, d, 0), (e, f, 1) | [2D affine transforms in vector graphics](applications/2d-affine-transforms-in-vector-graphics) |
| mechanism | a nontrivial null space of K — the structure can move with no restoring force | [Structural analysis of frames and trusses](applications/structural-analysis-of-frames-and-trusses) |
| message authentication code (MAC) | a keyed check that, unlike a CRC, an attacker cannot recompute | [CRC checksums as polynomial arithmetic modulo 2](applications/crc-checksums-as-polynomial-arithmetic-over-gf-2) |
| metamers | different spectra that look the same colour | [Color spaces as change of basis](applications/color-spaces-as-change-of-basis) |
| method of undetermined coefficients | writing the weights as unknowns and solving the conditions they must satisfy | [Finite-difference stencils by undetermined coefficients](applications/finite-difference-stencils-by-undetermined-coefficients) |
| minimally constrained vs overconstrained adjustment | removing exactly the null space vs also forcing the network to fit fixed points | [Geodetic network adjustment](applications/geodetic-network-adjustment) |
| minimum distance | the smallest weight of a nonzero codeword | [Linear error-correcting codes](applications/linear-error-correcting-codes) |
| misclosure | the amount by which observations around a loop fail to add up to zero | [Geodetic network adjustment](applications/geodetic-network-adjustment) |
| mode shape | an eigenvector of K phi = lambda M phi | [Structural analysis of frames and trusses](applications/structural-analysis-of-frames-and-trusses) |
| model matrix | places an object in the world (object to world coordinates) | [3D viewing and perspective projection pipeline](applications/3d-viewing-and-perspective-projection-pipeline) |
| model space | the span of the basis functions, every curve the fit could produce | [Least-squares fitting in a chosen function basis](applications/least-squares-fitting-in-a-chosen-function-basis) |
| monomial (power) form | coordinates in the basis 1, x, x², …, x^d | [Polynomial interpolation and change of basis](applications/polynomial-interpolation-and-change-of-basis) |
| motion compensation | predicting a video block from the previous frame and coding only the difference | [JPEG and video compression](applications/jpeg-and-video-compression) |
| multicollinearity | columns of X that are nearly linearly dependent, so β is poorly determined | [Least squares regression and the hat matrix](applications/least-squares-regression-and-the-hat-matrix) |
| multiplier | a single entry of the Leontief inverse | [Leontief input-output economics](applications/leontief-input-output-economics) |
| natural frequency | square root of the corresponding eigenvalue | [Structural analysis of frames and trusses](applications/structural-analysis-of-frames-and-trusses) |
| near and far planes | the closest and farthest distances that are drawn | [3D viewing and perspective projection pipeline](applications/3d-viewing-and-perspective-projection-pipeline) |
| negative frequencies | bins N/2 + 1 to N − 1, the complex conjugates of positive ones for a real signal | [The small DFT as a complex unitary matrix](applications/the-small-dft-as-a-complex-unitary-matrix) |
| network flow problem | choosing among the admissible x by minimizing a cost, a linear program | [Traffic flow conservation at intersections](applications/traffic-flow-conservation-at-intersections) |
| Newton form and divided differences | coordinates in the basis 1, (x − x_0), (x − x_0)(x − x_1), …, computed by a triangular solve | [Polynomial interpolation and change of basis](applications/polynomial-interpolation-and-change-of-basis) |
| nodal analysis vs mesh analysis | solving in potential space (dimension n - 1) vs in cycle space (dimension m - n + 1) | [Resistor networks and Kirchhoff's laws](applications/resistor-networks-and-kirchhoff-s-laws) |
| nodal conductance (admittance) matrix | the weighted graph Laplacian L = A^T C A | [Resistor networks and Kirchhoff's laws](applications/resistor-networks-and-kirchhoff-s-laws) |
| node (intersection) | one row of the conservation system | [Traffic flow conservation at intersections](applications/traffic-flow-conservation-at-intersections) |
| node voltage (potential) | one entry of the vector φ in R^n | [Resistor networks and Kirchhoff's laws](applications/resistor-networks-and-kirchhoff-s-laws) |
| nodes (interpolation points) | the d + 1 distinct x-values where the polynomial must match the data | [Polynomial interpolation and change of basis](applications/polynomial-interpolation-and-change-of-basis) |
| norm and energy | ‖f‖² = ⟨f, f⟩, the integral of the square of f | [Fourier series as orthogonal projection](applications/fourier-series-as-orthogonal-projection) |
| normal equations | Xᵀ X β = Xᵀ y, the statement that the residual is orthogonal to every column of X | [Least squares regression and the hat matrix](applications/least-squares-regression-and-the-hat-matrix) |
| normalized device coordinates (NDC) | the cube −1 ≤ x, y, z ≤ 1 that the visible region lands in | [3D viewing and perspective projection pipeline](applications/3d-viewing-and-perspective-projection-pipeline) |
| North's rule of thumb | a test for whether two singular values are too close to separate the modes | [Empirical orthogonal functions in climate data](applications/empirical-orthogonal-functions-in-climate-data) |
| Nyquist bin | bin N/2, the fastest wave a block of N samples can represent | [The small DFT as a complex unitary matrix](applications/the-small-dft-as-a-complex-unitary-matrix) |
| object, world and camera coordinates | the frames attached to a model, to the scene, and to the eye | [3D viewing and perspective projection pipeline](applications/3d-viewing-and-perspective-projection-pipeline) |
| observability | rank of the stacked matrix [H; HF; HF^2; ...] | [Kalman filtering for navigation](applications/kalman-filtering-for-navigation) |
| observable | a Hermitian operator; its eigenvalues are the measurable values | [Quantum mechanics and quantum computing](applications/quantum-mechanics-and-quantum-computing) |
| observation equation | one row of the system, an observation written in terms of the unknowns | [Geodetic network adjustment](applications/geodetic-network-adjustment) |
| observation model H | the linear map from state space to measurement space | [Kalman filtering for navigation](applications/kalman-filtering-for-navigation) |
| offset s_j | the position of a sample, counted in grid steps from the point x where the derivative is wanted | [Finite-difference stencils by undetermined coefficients](applications/finite-difference-stencils-by-undetermined-coefficients) |
| on-curve and off-curve points (font editors) | the end control points, which the curve passes through, and the inner control points, which it generally does not | [Bezier curves and font rendering](applications/bezier-curves-and-font-rendering) |
| order of accuracy | the power p in an error proportional to h^p | [Finite-difference stencils by undetermined coefficients](applications/finite-difference-stencils-by-undetermined-coefficients) |
| origin and destination volumes | the entries of b, net traffic entering the network at each node | [Traffic flow conservation at intersections](applications/traffic-flow-conservation-at-intersections) |
| orthogonal functions | functions whose inner product is zero | [Fourier series as orthogonal projection](applications/fourier-series-as-orthogonal-projection) |
| orthogonal polynomials (for a set of points) | polynomials whose sampled values are orthogonal, so that the design matrix has orthogonal columns | [Least-squares fitting in a chosen function basis](applications/least-squares-fitting-in-a-chosen-function-basis) |
| overall (total) balance | the sum of the component balances, a linearly dependent row | [Mass balance in a chemical process flowsheet](applications/mass-balance-in-a-chemical-process-flowsheet) |
| overfitting | fitting the noise in the data by using too many basis functions | [Least-squares fitting in a chosen function basis](applications/least-squares-fitting-in-a-chosen-function-basis) |
| parity block | the block chosen so that every stripe satisfies d_1 + ⋯ + d_(n−1) + p = 0 | [RAID-5 parity and XOR recovery](applications/raid-5-parity-and-xor-recovery) |
| parity-check matrix H | a basis of the code's orthogonal complement; codewords are its null space | [Linear error-correcting codes](applications/linear-error-correcting-codes) |
| Parseval's identity | the energy of f is the sum of the energies of its components | [Fourier series as orthogonal projection](applications/fourier-series-as-orthogonal-projection) |
| Parseval's theorem | the change of basis preserves length (energy), up to the factor N | [The small DFT as a complex unitary matrix](applications/the-small-dft-as-a-complex-unitary-matrix) |
| partial sum S_N | the series cut off after the N-th harmonic | [Fourier series as orthogonal projection](applications/fourier-series-as-orthogonal-projection) |
| perfect (information-theoretic) secrecy | every candidate secret is consistent with the same number of polynomials through any k − 1 shares | [Shamir secret sharing](applications/shamir-secret-sharing) |
| period and fundamental | the length after which the signal repeats (2π here), and the sine or cosine that repeats exactly once in it | [Fourier series as orthogonal projection](applications/fourier-series-as-orthogonal-projection) |
| perspective division | dividing by w, the step that makes distant objects smaller | [3D viewing and perspective projection pipeline](applications/3d-viewing-and-perspective-projection-pipeline) |
| perspective-correct interpolation | blending attributes using the 3D weights rather than the screen weights | [Barycentric coordinates and triangle rasterization](applications/barycentric-coordinates-and-triangle-rasterization) |
| pixel centre | the point in the middle of a pixel; a pixel is drawn when its centre is covered | [Barycentric coordinates and triangle rasterization](applications/barycentric-coordinates-and-triangle-rasterization) |
| point differential | a team's total points scored minus points allowed | [Sports and citation ranking (Massey/Colley)](applications/sports-and-citation-ranking-massey-colley) |
| pose (frame, transform) | a rotation and a translation together, a 4 × 4 matrix in SE(3) | [3D rotations and rigid-body pose](applications/3d-rotations-and-rigid-body-pose) |
| power iteration | repeated multiplication by the matrix | [PageRank and network centrality](applications/pagerank-and-network-centrality) |
| primaries | the three lights a display mixes; each RGB space has its own | [Color spaces as change of basis](applications/color-spaces-as-change-of-basis) |
| principal component time series | the corresponding right singular vector, scaled | [Empirical orthogonal functions in climate data](applications/empirical-orthogonal-functions-in-climate-data) |
| process noise / measurement noise | the covariance matrices Q and R | [Kalman filtering for navigation](applications/kalman-filtering-for-navigation) |
| productive economy | spectral radius of A below 1, so the Neumann series converges | [Leontief input-output economics](applications/leontief-input-output-economics) |
| projection / ray sum | one row of A applied to x — a line integral through the object | [Computed tomography reconstruction](applications/computed-tomography-reconstruction) |
| projection matrix | maps the visible region to clip coordinates and puts the depth into w | [3D viewing and perspective projection pipeline](applications/3d-viewing-and-perspective-projection-pipeline) |
| purge stream | a small bleed that keeps an inert component from accumulating in the loop | [Mass balance in a chemical process flowsheet](applications/mass-balance-in-a-chemical-process-flowsheet) |
| quantization | dividing each coefficient by a step size and rounding to a whole number | [JPEG and video compression](applications/jpeg-and-video-compression) |
| quantization table | the 64 step sizes, larger for higher frequencies | [JPEG and video compression](applications/jpeg-and-video-compression) |
| RAID-6 | a second, independent equation over GF(2^8), so two erasures can be solved | [RAID-5 parity and XOR recovery](applications/raid-5-parity-and-xor-recovery) |
| raster image (bitmap) | a vector in R^(width × height), one coordinate per pixel, so its resolution is fixed by the dimension | [Bezier curves and font rendering](applications/bezier-curves-and-font-rendering) |
| rasterization | deciding which pixel centres a shape covers, turning a vector description into pixels | [Barycentric coordinates and triangle rasterization](applications/barycentric-coordinates-and-triangle-rasterization) |
| rasterization | sampling the curves onto a pixel grid, a map from the polynomial space into R^(width × height) | [Bezier curves and font rendering](applications/bezier-curves-and-font-rendering) |
| rating | a number per team whose differences predict results | [Sports and citation ranking (Massey/Colley)](applications/sports-and-citation-ranking-massey-colley) |
| re-orthonormalization | projecting a drifted matrix back onto the orthogonal matrices | [3D rotations and rigid-body pose](applications/3d-rotations-and-rigid-body-pose) |
| read-modify-write (small write) | updating parity by p_new = p_old + d_old + d_new, which uses linearity | [RAID-5 parity and XOR recovery](applications/raid-5-parity-and-xor-recovery) |
| rebuild (resilvering) | solving the equation for the failed disk's block in every stripe | [RAID-5 parity and XOR recovery](applications/raid-5-parity-and-xor-recovery) |
| reciprocity | symmetry of L, so the potential at b due to a source at a equals the potential at a due to the same source at b | [Resistor networks and Kirchhoff's laws](applications/resistor-networks-and-kirchhoff-s-laws) |
| reconstruction | Lagrange interpolation evaluated at x = 0, a fixed linear combination of the shares | [Shamir secret sharing](applications/shamir-secret-sharing) |
| recycle stream | the coupling that turns a triangular system into a genuinely simultaneous one | [Mass balance in a chemical process flowsheet](applications/mass-balance-in-a-chemical-process-flowsheet) |
| reference direction | the arrow chosen for a segment; a negative flow means net traffic against it | [Traffic flow conservation at intersections](applications/traffic-flow-conservation-at-intersections) |
| regression coefficients β | coordinates of the fitted vector in the basis given by the columns of X | [Least squares regression and the hat matrix](applications/least-squares-regression-and-the-hat-matrix) |
| regularization strength | the Tikhonov parameter lambda trading data fit against smoothness | [Computed tomography reconstruction](applications/computed-tomography-reconstruction) |
| reprojection error | the nonlinear least-squares objective minimized in refinement | [Multiple-view geometry and structure from motion](applications/multiple-view-geometry-and-structure-from-motion) |
| residual (correction) v | the change to each observation that makes the set consistent | [Geodetic network adjustment](applications/geodetic-network-adjustment) |
| residuals | the component of y in the orthogonal complement of the column space | [Least squares regression and the hat matrix](applications/least-squares-regression-and-the-hat-matrix) |
| restraint / boundary condition | deleting the corresponding rows and columns, or adding constraint rows | [Structural analysis of frames and trusses](applications/structural-analysis-of-frames-and-trusses) |
| rotated EOF (varimax) | a deliberately non-orthogonal re-basis of the leading subspace | [Empirical orthogonal functions in climate data](applications/empirical-orthogonal-functions-in-climate-data) |
| rounding (cancellation) error | the loss of digits when nearly equal sample values are subtracted | [Finite-difference stencils by undetermined coefficients](applications/finite-difference-stencils-by-undetermined-coefficients) |
| Runge phenomenon | large oscillations of high-degree interpolants at equally spaced nodes | [Polynomial interpolation and change of basis](applications/polynomial-interpolation-and-change-of-basis) |
| R² | the squared length of the centered fitted vector over that of the centered data vector | [Least squares regression and the hat matrix](applications/least-squares-regression-and-the-hat-matrix) |
| samples | the coordinates of the signal in the standard basis (one per time step) | [The small DFT as a complex unitary matrix](applications/the-small-dft-as-a-complex-unitary-matrix) |
| SCF iteration | fixed-point iteration on an eigenproblem whose matrix depends on its own solution | [Quantum mechanics and quantum computing](applications/quantum-mechanics-and-quantum-computing) |
| schedule graph | teams as nodes and games as edges | [Sports and citation ranking (Massey/Colley)](applications/sports-and-citation-ranking-massey-colley) |
| sequential modular vs equation-oriented simulation | fixed-point iteration around loops vs solving the whole linear system at once | [Mass balance in a chemical process flowsheet](applications/mass-balance-in-a-chemical-process-flowsheet) |
| share | a point (x_i, f(x_i)), one coordinate of the evaluation map's output | [Shamir secret sharing](applications/shamir-secret-sharing) |
| share refresh (proactive sharing) | adding a sharing of 0, a polynomial from the subspace with f(0) = 0 | [Shamir secret sharing](applications/shamir-secret-sharing) |
| shift register (LFSR) | the hardware that computes a CRC one bit per clock | [CRC checksums as polynomial arithmetic modulo 2](applications/crc-checksums-as-polynomial-arithmetic-over-gf-2) |
| single-pass conversion | the fraction of the reactant entering the reactor that reacts, a fixed coefficient | [Mass balance in a chemical process flowsheet](applications/mass-balance-in-a-chemical-process-flowsheet) |
| sinogram | the measurement vector b, arranged by angle and detector position | [Computed tomography reconstruction](applications/computed-tomography-reconstruction) |
| spectral leakage | energy of a wave that is not one of the N basis waves, spread across many coordinates | [The small DFT as a complex unitary matrix](applications/the-small-dft-as-a-complex-unitary-matrix) |
| spectrum | the coordinate vector in the Fourier basis; its magnitudes are what a spectrum analyzer shows | [The small DFT as a complex unitary matrix](applications/the-small-dft-as-a-complex-unitary-matrix) |
| spectrum (spectral power distribution) | how much power a light carries at each wavelength | [Color spaces as change of basis](applications/color-spaces-as-change-of-basis) |
| split fraction | the fraction of a component a separator sends to a given outlet, a fixed coefficient | [Mass balance in a chemical process flowsheet](applications/mass-balance-in-a-chemical-process-flowsheet) |
| square-root filter | propagating a Cholesky factor of P instead of P | [Kalman filtering for navigation](applications/kalman-filtering-for-navigation) |
| state vector | the unknown x being estimated | [Kalman filtering for navigation](applications/kalman-filtering-for-navigation) |
| stationary distribution | the dominant eigenvector, normalized | [PageRank and network centrality](applications/pagerank-and-network-centrality) |
| steady state | Sv = 0 — v lies in the right null space | [Stoichiometric matrices of reaction networks](applications/stoichiometric-matrices-of-reaction-networks) |
| stencil | a list of offsets and weights; the estimate is the weighted sum of the samples | [Finite-difference stencils by undetermined coefficients](applications/finite-difference-stencils-by-undetermined-coefficients) |
| stiffness matrix | the coefficient matrix K; symmetric positive definite once restraints are applied | [Structural analysis of frames and trusses](applications/structural-analysis-of-frames-and-trusses) |
| stoichiometric matrix S | species by reactions, signed integer coefficients | [Stoichiometric matrices of reaction networks](applications/stoichiometric-matrices-of-reaction-networks) |
| streak artifact | the visible signature of undersampling — energy in the near-null space | [Computed tomography reconstruction](applications/computed-tomography-reconstruction) |
| stream | a pipe between units; contributes one unknown per component it carries | [Mass balance in a chemical process flowsheet](applications/mass-balance-in-a-chemical-process-flowsheet) |
| strength of schedule | how good a team's opponents were; built into both methods | [Sports and citation ranking (Massey/Colley)](applications/sports-and-citation-ranking-massey-colley) |
| stripe | one block from each disk at the same position, the unknowns of one parity equation | [RAID-5 parity and XOR recovery](applications/raid-5-parity-and-xor-recovery) |
| stripe unit (chunk) | one block of a stripe, a vector in GF(2)^w | [RAID-5 parity and XOR recovery](applications/raid-5-parity-and-xor-recovery) |
| subdivision (splitting a curve) | change of basis to the Bernstein basis of a subinterval | [Bezier curves and font rendering](applications/bezier-curves-and-font-rendering) |
| superposition | linearity of the solution map s -> φ | [Resistor networks and Kirchhoff's laws](applications/resistor-networks-and-kirchhoff-s-laws) |
| syndrome | H y^T — depends only on the error, not the message | [Linear error-correcting codes](applications/linear-error-correcting-codes) |
| system matrix / forward projector | A, the discretized Radon transform | [Computed tomography reconstruction](applications/computed-tomography-reconstruction) |
| systematic form | G = [I \| P], so the message appears verbatim in the codeword | [Linear error-correcting codes](applications/linear-error-correcting-codes) |
| tear stream | the unknown guessed to start the unit-by-unit iteration around a loop | [Mass balance in a chemical process flowsheet](applications/mass-balance-in-a-chemical-process-flowsheet) |
| technical coefficient matrix A | input from sector i per unit output of sector j | [Leontief input-output economics](applications/leontief-input-output-economics) |
| teleportation | the rank-one correction that makes the chain irreducible | [PageRank and network centrality](applications/pagerank-and-network-centrality) |
| tensor product | the Kronecker product; why n qubits need dimension 2^n | [Quantum mechanics and quantum computing](applications/quantum-mechanics-and-quantum-computing) |
| texture coordinates | the position in an image (a texture) that each corner is mapped to | [Barycentric coordinates and triangle rasterization](applications/barycentric-coordinates-and-triangle-rasterization) |
| threshold k | the dimension of the polynomial space, deg f + 1 | [Shamir secret sharing](applications/shamir-secret-sharing) |
| top-left rule | the tie-break that assigns a pixel exactly on a shared edge to just one triangle | [Barycentric coordinates and triangle rasterization](applications/barycentric-coordinates-and-triangle-rasterization) |
| traffic counts (detector or loop counts) | measured coordinates of x, used to pin down the free variables | [Traffic flow conservation at intersections](applications/traffic-flow-conservation-at-intersections) |
| transform attribute / CSS transform property | a list of elementary transforms whose matrices are multiplied in the order written | [2D affine transforms in vector graphics](applications/2d-affine-transforms-in-vector-graphics) |
| transform-origin | the point about which rotation and scaling happen, a conjugation T(c) M T(−c) | [2D affine transforms in vector graphics](applications/2d-affine-transforms-in-vector-graphics) |
| translate, rotate, scale, skew | the elementary matrices of the stack | [2D affine transforms in vector graphics](applications/2d-affine-transforms-in-vector-graphics) |
| tristimulus values | three numbers that determine a colour; CIE XYZ is the standard set | [Color spaces as change of basis](applications/color-spaces-as-change-of-basis) |
| truncation error | the error from cutting off the Taylor series, present even in exact arithmetic | [Finite-difference stencils by undetermined coefficients](applications/finite-difference-stencils-by-undetermined-coefficients) |
| twiddle factor ω^(kn) | an entry of the DFT matrix | [The small DFT as a complex unitary matrix](applications/the-small-dft-as-a-complex-unitary-matrix) |
| unitary gate | a norm-preserving complex linear map — the complex analogue of an orthogonal matrix | [Quantum mechanics and quantum computing](applications/quantum-mechanics-and-quantum-computing) |
| user space vs viewport space | two coordinate systems related by the CTM | [2D affine transforms in vector graphics](applications/2d-affine-transforms-in-vector-graphics) |
| vector graphics | shapes stored as coordinates in a polynomial space, evaluated at whatever resolution the output needs | [Bezier curves and font rendering](applications/bezier-curves-and-font-rendering) |
| vertex | a corner of a triangle; the pipeline moves vertices, and the triangles follow | [3D viewing and perspective projection pipeline](applications/3d-viewing-and-perspective-projection-pipeline) |
| view frustum | the truncated pyramid between the near and far planes that the camera sees | [3D viewing and perspective projection pipeline](applications/3d-viewing-and-perspective-projection-pipeline) |
| view matrix | re-expresses the world relative to the camera (world to camera coordinates) | [3D viewing and perspective projection pipeline](applications/3d-viewing-and-perspective-projection-pipeline) |
| viewport transform | the final scaling from NDC to pixels | [3D viewing and perspective projection pipeline](applications/3d-viewing-and-perspective-projection-pipeline) |
| weight | the inverse of an observation's variance; longer levelling lines get smaller weights | [Geodetic network adjustment](applications/geodetic-network-adjustment) |
| white point | the colour of R = G = B = 1; D65 (daylight, about 6500 K) for sRGB, D50 for print | [Color spaces as change of basis](applications/color-spaces-as-change-of-basis) |
| write hole | a crash between writing data and parity, which leaves a stripe that violates its equation | [RAID-5 parity and XOR recovery](applications/raid-5-parity-and-xor-recovery) |
| XOR | addition in GF(2), applied bit by bit | [RAID-5 parity and XOR recovery](applications/raid-5-parity-and-xor-recovery) |
| yaw, pitch, roll (Euler angles) | coordinates on the set of rotations, R = R_z(ψ) R_y(θ) R_x(φ) | [3D rotations and rigid-body pose](applications/3d-rotations-and-rigid-body-pose) |
| YCbCr and chroma subsampling | brightness and two colour-difference channels, with the colour stored at lower resolution | [JPEG and video compression](applications/jpeg-and-video-compression) |
| z-fighting | flickering between surfaces whose depths the depth buffer cannot tell apart | [3D viewing and perspective projection pipeline](applications/3d-viewing-and-perspective-projection-pipeline) |
| zigzag order and entropy coding | listing coefficients from low to high frequency so the zeros come in long runs, then coding the result compactly | [JPEG and video compression](applications/jpeg-and-video-compression) |
