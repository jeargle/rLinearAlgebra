# Domain terminology, translated

One unfamiliar word from a question, and what it means mathematically.

### Two general terms

A **field** is a number system in which addition, subtraction, multiplication, and division by any nonzero number all behave the way they do for ordinary numbers. The rational numbers ℚ, the real numbers ℝ, the complex numbers ℂ, and the integers [modulo](https://en.wikipedia.org/wiki/Modular_arithmetic) a prime p all qualify. The integers modulo 6 do not: there 2 × 3 = 0, so 2 has no reciprocal and nothing can be divided by 2. The scalars of every vector space come from a field, which is why each entry names its scalar field.

**[GF(2)](https://en.wikipedia.org/wiki/GF%282%29)** is the smallest field: just the two numbers 0 and 1, added and multiplied modulo 2, so 1 + 1 = 0. Addition is the same as [XOR](https://en.wikipedia.org/wiki/Exclusive_or), and multiplication is the same as AND. GF(p) is the same construction using the integers modulo a prime p.

### By field

| Domain term | In linear algebra | Entry |
|---|---|---|
| (k, n) scheme | a polynomial in a k-dimensional space evaluated at n distinct points | [Shamir secret sharing](applications/shamir-secret-sharing) |
| affine invariance | transforming the control points transforms the curve, because the basis sums to 1 | [Bezier curves and font rendering](applications/bezier-curves-and-font-rendering) |
| anomaly field | the mean-centered data matrix | [Empirical orthogonal functions in climate data](applications/empirical-orthogonal-functions-in-climate-data) |
| ART / SIRT | Kaczmarz row-action and related simultaneous iterations | [Computed tomography reconstruction](applications/computed-tomography-reconstruction) |
| assembly | summing small element matrices into the global matrix at shared DOF indices | [Structural analysis of frames and trusses](applications/structural-analysis-of-frames-and-trusses) |
| attenuation coefficient | the unknown x, one value per voxel | [Computed tomography reconstruction](applications/computed-tomography-reconstruction) |
| backprojection | applying A transpose to the data | [Computed tomography reconstruction](applications/computed-tomography-reconstruction) |
| balancing an equation | finding an integer null vector of the element-by-species matrix | [Stoichiometric matrices of reaction networks](applications/stoichiometric-matrices-of-reaction-networks) |
| bandwidth / skyline | the sparsity pattern induced by node numbering | [Structural analysis of frames and trusses](applications/structural-analysis-of-frames-and-trusses) |
| barycentric formula | a stable way to evaluate the Lagrange form | [Polynomial interpolation and change of basis](applications/polynomial-interpolation-and-change-of-basis) |
| basis set (quantum chemistry) | the chosen basis in which H is expressed | [Quantum mechanics and quantum computing](applications/quantum-mechanics-and-quantum-computing) |
| Bernstein polynomials | a basis of P_3 consisting of nonnegative functions that sum to 1 | [Bezier curves and font rendering](applications/bezier-curves-and-font-rendering) |
| boundary (cordon) counts | known traffic entering and leaving at the district's edge, summarized in b | [Traffic flow conservation at intersections](applications/traffic-flow-conservation-at-intersections) |
| bridge balance | a choice of resistances that puts one edge current at zero | [Resistor networks and Kirchhoff's laws](applications/resistor-networks-and-kirchhoff-s-laws) |
| bundle adjustment | sparse nonlinear least squares over all cameras and points at once | [Multiple-view geometry and structure from motion](applications/multiple-view-geometry-and-structure-from-motion) |
| centrality | a score defined as an eigenvector, or a function, of the graph matrix | [PageRank and network centrality](applications/pagerank-and-network-centrality) |
| Chebyshev polynomials and nodes | a basis and a set of nodes for which the interpolation problem is well conditioned | [Polynomial interpolation and change of basis](applications/polynomial-interpolation-and-change-of-basis) |
| circulation | traffic going round a closed loop, a vector in the null space of A | [Traffic flow conservation at intersections](applications/traffic-flow-conservation-at-intersections) |
| code rate | k/n, the subspace dimension over the ambient dimension | [Linear error-correcting codes](applications/linear-error-correcting-codes) |
| codeword | an element of the k-dimensional subspace of GF(2)^n | [Linear error-correcting codes](applications/linear-error-correcting-codes) |
| component balance | one row of the system, for one component around one unit | [Mass balance in a chemical process flowsheet](applications/mass-balance-in-a-chemical-process-flowsheet) |
| conservation of flow (continuity) | A x = b, one equation per intersection | [Traffic flow conservation at intersections](applications/traffic-flow-conservation-at-intersections) |
| conserved moiety | a left null vector y; y^T c is constant for all time | [Stoichiometric matrices of reaction networks](applications/stoichiometric-matrices-of-reaction-networks) |
| control points | coordinates of the curve in the Bernstein basis, one point in the plane per basis polynomial | [Bezier curves and font rendering](applications/bezier-curves-and-font-rendering) |
| control polygon | the broken line through the control points; the curve lies in its convex hull | [Bezier curves and font rendering](applications/bezier-curves-and-font-rendering) |
| corrupted share | an error in a Reed-Solomon codeword | [Shamir secret sharing](applications/shamir-secret-sharing) |
| covariance matrix P | the uncertainty ellipsoid; symmetric positive semidefinite | [Kalman filtering for navigation](applications/kalman-filtering-for-navigation) |
| cubic vs quadratic outlines (CFF/PostScript vs TrueType) | curves in P_3 vs curves in P_2 | [Bezier curves and font rendering](applications/bezier-curves-and-font-rendering) |
| damping factor (alpha) | the weight on P versus the uniform teleportation term | [PageRank and network centrality](applications/pagerank-and-network-centrality) |
| dangling node | a zero column, which breaks stochasticity | [PageRank and network centrality](applications/pagerank-and-network-centrality) |
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
| design matrix (model matrix) X | the n × k matrix whose columns are the predictors, including a column of 1s for the intercept | [Least squares regression and the hat matrix](applications/least-squares-regression-and-the-hat-matrix) |
| direct vs indirect requirements | the successive terms A, A^2, A^3 of the Neumann series | [Leontief input-output economics](applications/leontief-input-output-economics) |
| DLT (direct linear transform) | stacking constraints into A and taking the smallest right singular vector | [Multiple-view geometry and structure from motion](applications/multiple-view-geometry-and-structure-from-motion) |
| dummy variable trap | an exactly dependent set of indicator columns, which makes X rank-deficient | [Least squares regression and the hat matrix](applications/least-squares-regression-and-the-hat-matrix) |
| easing curve (CSS cubic-bezier) | a cubic in the same basis, used for timing instead of shape | [Bezier curves and font rendering](applications/bezier-curves-and-font-rendering) |
| effective (Thevenin) resistance | (e_a - e_b)^T L^+ (e_a - e_b), a quadratic form in the pseudoinverse | [Resistor networks and Kirchhoff's laws](applications/resistor-networks-and-kirchhoff-s-laws) |
| eigenstate / energy level | eigenvector and eigenvalue of the Hamiltonian | [Quantum mechanics and quantum computing](applications/quantum-mechanics-and-quantum-computing) |
| elementary flux mode | an extreme ray of the nonnegative part of the null space | [Stoichiometric matrices of reaction networks](applications/stoichiometric-matrices-of-reaction-networks) |
| embodied / Scope 3 emissions | an appended satellite row multiplied through the same inverse | [Leontief input-output economics](applications/leontief-input-output-economics) |
| entangled state | a vector that does not factor as a tensor product | [Quantum mechanics and quantum computing](applications/quantum-mechanics-and-quantum-computing) |
| EOF | a left singular vector — one spatial pattern | [Empirical orthogonal functions in climate data](applications/empirical-orthogonal-functions-in-climate-data) |
| epipolar constraint | the bilinear equation relating corresponding points in two views | [Multiple-view geometry and structure from motion](applications/multiple-view-geometry-and-structure-from-motion) |
| erasure vs error | known vs unknown error position — a column selection vs a search | [Linear error-correcting codes](applications/linear-error-correcting-codes) |
| erasure vs error | a lost block at a known position (solvable) vs a wrong block at an unknown position (only detectable) | [RAID-5 parity and XOR recovery](applications/raid-5-parity-and-xor-recovery) |
| essential / fundamental matrix | the rank-2 bilinear form satisfying x'^T E x = 0 | [Multiple-view geometry and structure from motion](applications/multiple-view-geometry-and-structure-from-motion) |
| expectation value | the quadratic form psi^* A psi | [Quantum mechanics and quantum computing](applications/quantum-mechanics-and-quantum-computing) |
| explained variance | sigma_i^2 as a fraction of the total | [Empirical orthogonal functions in climate data](applications/empirical-orthogonal-functions-in-climate-data) |
| extrinsic parameters [R\|t] | the rigid transform from world to camera frame | [Multiple-view geometry and structure from motion](applications/multiple-view-geometry-and-structure-from-motion) |
| FFT | a factorization of the DFT matrix into sparse factors, not a different transform | [The small DFT as a complex unitary matrix](applications/the-small-dft-as-a-complex-unitary-matrix) |
| filter divergence | P losing positive definiteness in finite precision, or an unobservable direction growing without bound | [Kalman filtering for navigation](applications/kalman-filtering-for-navigation) |
| filtered backprojection (FBP) | an analytic spectral inverse of the forward operator | [Computed tomography reconstruction](applications/computed-tomography-reconstruction) |
| final demand | the right-hand side d | [Leontief input-output economics](applications/leontief-input-output-economics) |
| fitted values ŷ | the orthogonal projection of y onto the column space of X | [Least squares regression and the hat matrix](applications/least-squares-regression-and-the-hat-matrix) |
| flow (volume) | cars per hour on a segment, an entry of x | [Traffic flow conservation at intersections](applications/traffic-flow-conservation-at-intersections) |
| flux | v, the vector of reaction rates | [Stoichiometric matrices of reaction networks](applications/stoichiometric-matrices-of-reaction-networks) |
| frequency bin k | the coefficient of the k-th complex wave in the Fourier basis | [The small DFT as a complex unitary matrix](applications/the-small-dft-as-a-complex-unitary-matrix) |
| generator matrix G | a basis of the code, written as rows | [Linear error-correcting codes](applications/linear-error-correcting-codes) |
| gross / total output | the unknown x | [Leontief input-output economics](applications/leontief-input-output-economics) |
| ground (reference node) | the node whose potential is fixed at 0, removing the null space spanned by the all-ones vector | [Resistor networks and Kirchhoff's laws](applications/resistor-networks-and-kirchhoff-s-laws) |
| Hamiltonian | the Hermitian matrix H in H psi = E psi | [Quantum mechanics and quantum computing](applications/quantum-mechanics-and-quantum-computing) |
| hat matrix H | the projection matrix X (XᵀX)⁻¹ Xᵀ, so ŷ = H y | [Least squares regression and the hat matrix](applications/least-squares-regression-and-the-hat-matrix) |
| homogeneous coordinates | an added coordinate that turns perspective division into a linear map plus a normalization | [Multiple-view geometry and structure from motion](applications/multiple-view-geometry-and-structure-from-motion) |
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
| leverage h_ii | the i-th diagonal entry of H; how strongly observation i pulls its own fitted value | [Least squares regression and the hat matrix](applications/least-squares-regression-and-the-hat-matrix) |
| link (road segment) | one coordinate of the flow vector | [Traffic flow conservation at intersections](applications/traffic-flow-conservation-at-intersections) |
| link closure | forcing a coordinate of x to zero, which may leave no admissible solution | [Traffic flow conservation at intersections](applications/traffic-flow-conservation-at-intersections) |
| link matrix | the column-stochastic matrix P built from the graph | [PageRank and network centrality](applications/pagerank-and-network-centrality) |
| load vector | the right-hand side b | [Structural analysis of frames and trusses](applications/structural-analysis-of-frames-and-trusses) |
| loading | one entry of an EOF, i.e. one grid point's weight in that pattern | [Empirical orthogonal functions in climate data](applications/empirical-orthogonal-functions-in-climate-data) |
| loop (mesh) currents | coordinates in a basis of the cycle space, the null space of A^T, dimension m - n + 1 | [Resistor networks and Kirchhoff's laws](applications/resistor-networks-and-kirchhoff-s-laws) |
| mechanism | a nontrivial null space of K — the structure can move with no restoring force | [Structural analysis of frames and trusses](applications/structural-analysis-of-frames-and-trusses) |
| minimum distance | the smallest weight of a nonzero codeword | [Linear error-correcting codes](applications/linear-error-correcting-codes) |
| mode shape | an eigenvector of K phi = lambda M phi | [Structural analysis of frames and trusses](applications/structural-analysis-of-frames-and-trusses) |
| monomial (power) form | coordinates in the basis 1, x, x², …, x^d | [Polynomial interpolation and change of basis](applications/polynomial-interpolation-and-change-of-basis) |
| multicollinearity | columns of X that are nearly linearly dependent, so β is poorly determined | [Least squares regression and the hat matrix](applications/least-squares-regression-and-the-hat-matrix) |
| multiplier | a single entry of the Leontief inverse | [Leontief input-output economics](applications/leontief-input-output-economics) |
| natural frequency | square root of the corresponding eigenvalue | [Structural analysis of frames and trusses](applications/structural-analysis-of-frames-and-trusses) |
| negative frequencies | bins N/2 + 1 to N − 1, the complex conjugates of positive ones for a real signal | [The small DFT as a complex unitary matrix](applications/the-small-dft-as-a-complex-unitary-matrix) |
| network flow problem | choosing among the admissible x by minimizing a cost, a linear program | [Traffic flow conservation at intersections](applications/traffic-flow-conservation-at-intersections) |
| Newton form and divided differences | coordinates in the basis 1, (x − x_0), (x − x_0)(x − x_1), …, computed by a triangular solve | [Polynomial interpolation and change of basis](applications/polynomial-interpolation-and-change-of-basis) |
| nodal analysis vs mesh analysis | solving in potential space (dimension n - 1) vs in cycle space (dimension m - n + 1) | [Resistor networks and Kirchhoff's laws](applications/resistor-networks-and-kirchhoff-s-laws) |
| nodal conductance (admittance) matrix | the weighted graph Laplacian L = A^T C A | [Resistor networks and Kirchhoff's laws](applications/resistor-networks-and-kirchhoff-s-laws) |
| node (intersection) | one row of the conservation system | [Traffic flow conservation at intersections](applications/traffic-flow-conservation-at-intersections) |
| node voltage (potential) | one entry of the vector φ in R^n | [Resistor networks and Kirchhoff's laws](applications/resistor-networks-and-kirchhoff-s-laws) |
| nodes (interpolation points) | the d + 1 distinct x-values where the polynomial must match the data | [Polynomial interpolation and change of basis](applications/polynomial-interpolation-and-change-of-basis) |
| normal equations | Xᵀ X β = Xᵀ y, the statement that the residual is orthogonal to every column of X | [Least squares regression and the hat matrix](applications/least-squares-regression-and-the-hat-matrix) |
| North's rule of thumb | a test for whether two singular values are too close to separate the modes | [Empirical orthogonal functions in climate data](applications/empirical-orthogonal-functions-in-climate-data) |
| Nyquist bin | bin N/2, the fastest wave a block of N samples can represent | [The small DFT as a complex unitary matrix](applications/the-small-dft-as-a-complex-unitary-matrix) |
| observability | rank of the stacked matrix [H; HF; HF^2; ...] | [Kalman filtering for navigation](applications/kalman-filtering-for-navigation) |
| observable | a Hermitian operator; its eigenvalues are the measurable values | [Quantum mechanics and quantum computing](applications/quantum-mechanics-and-quantum-computing) |
| observation model H | the linear map from state space to measurement space | [Kalman filtering for navigation](applications/kalman-filtering-for-navigation) |
| on-curve and off-curve points (font editors) | the end control points, which the curve passes through, and the inner control points, which it generally does not | [Bezier curves and font rendering](applications/bezier-curves-and-font-rendering) |
| origin and destination volumes | the entries of b, net traffic entering the network at each node | [Traffic flow conservation at intersections](applications/traffic-flow-conservation-at-intersections) |
| overall (total) balance | the sum of the component balances, a linearly dependent row | [Mass balance in a chemical process flowsheet](applications/mass-balance-in-a-chemical-process-flowsheet) |
| parity block | the block chosen so that every stripe satisfies d_1 + ⋯ + d_(n−1) + p = 0 | [RAID-5 parity and XOR recovery](applications/raid-5-parity-and-xor-recovery) |
| parity-check matrix H | a basis of the code's orthogonal complement; codewords are its null space | [Linear error-correcting codes](applications/linear-error-correcting-codes) |
| Parseval's theorem | the change of basis preserves length (energy), up to the factor N | [The small DFT as a complex unitary matrix](applications/the-small-dft-as-a-complex-unitary-matrix) |
| perfect (information-theoretic) secrecy | every candidate secret is consistent with the same number of polynomials through any k − 1 shares | [Shamir secret sharing](applications/shamir-secret-sharing) |
| power iteration | repeated multiplication by the matrix | [PageRank and network centrality](applications/pagerank-and-network-centrality) |
| principal component time series | the corresponding right singular vector, scaled | [Empirical orthogonal functions in climate data](applications/empirical-orthogonal-functions-in-climate-data) |
| process noise / measurement noise | the covariance matrices Q and R | [Kalman filtering for navigation](applications/kalman-filtering-for-navigation) |
| productive economy | spectral radius of A below 1, so the Neumann series converges | [Leontief input-output economics](applications/leontief-input-output-economics) |
| projection / ray sum | one row of A applied to x — a line integral through the object | [Computed tomography reconstruction](applications/computed-tomography-reconstruction) |
| purge stream | a small bleed that keeps an inert component from accumulating in the loop | [Mass balance in a chemical process flowsheet](applications/mass-balance-in-a-chemical-process-flowsheet) |
| RAID-6 | a second, independent equation over GF(2^8), so two erasures can be solved | [RAID-5 parity and XOR recovery](applications/raid-5-parity-and-xor-recovery) |
| raster image (bitmap) | a vector in R^(width × height), one coordinate per pixel, so its resolution is fixed by the dimension | [Bezier curves and font rendering](applications/bezier-curves-and-font-rendering) |
| rasterization | sampling the curves onto a pixel grid, a map from the polynomial space into R^(width × height) | [Bezier curves and font rendering](applications/bezier-curves-and-font-rendering) |
| read-modify-write (small write) | updating parity by p_new = p_old + d_old + d_new, which uses linearity | [RAID-5 parity and XOR recovery](applications/raid-5-parity-and-xor-recovery) |
| rebuild (resilvering) | solving the equation for the failed disk's block in every stripe | [RAID-5 parity and XOR recovery](applications/raid-5-parity-and-xor-recovery) |
| reciprocity | symmetry of L, so the potential at b due to a source at a equals the potential at a due to the same source at b | [Resistor networks and Kirchhoff's laws](applications/resistor-networks-and-kirchhoff-s-laws) |
| reconstruction | Lagrange interpolation evaluated at x = 0, a fixed linear combination of the shares | [Shamir secret sharing](applications/shamir-secret-sharing) |
| recycle stream | the coupling that turns a triangular system into a genuinely simultaneous one | [Mass balance in a chemical process flowsheet](applications/mass-balance-in-a-chemical-process-flowsheet) |
| reference direction | the arrow chosen for a segment; a negative flow means net traffic against it | [Traffic flow conservation at intersections](applications/traffic-flow-conservation-at-intersections) |
| regression coefficients β | coordinates of the fitted vector in the basis given by the columns of X | [Least squares regression and the hat matrix](applications/least-squares-regression-and-the-hat-matrix) |
| regularization strength | the Tikhonov parameter lambda trading data fit against smoothness | [Computed tomography reconstruction](applications/computed-tomography-reconstruction) |
| reprojection error | the nonlinear least-squares objective minimized in refinement | [Multiple-view geometry and structure from motion](applications/multiple-view-geometry-and-structure-from-motion) |
| residuals | the component of y in the orthogonal complement of the column space | [Least squares regression and the hat matrix](applications/least-squares-regression-and-the-hat-matrix) |
| restraint / boundary condition | deleting the corresponding rows and columns, or adding constraint rows | [Structural analysis of frames and trusses](applications/structural-analysis-of-frames-and-trusses) |
| rotated EOF (varimax) | a deliberately non-orthogonal re-basis of the leading subspace | [Empirical orthogonal functions in climate data](applications/empirical-orthogonal-functions-in-climate-data) |
| Runge phenomenon | large oscillations of high-degree interpolants at equally spaced nodes | [Polynomial interpolation and change of basis](applications/polynomial-interpolation-and-change-of-basis) |
| R² | the squared length of the centered fitted vector over that of the centered data vector | [Least squares regression and the hat matrix](applications/least-squares-regression-and-the-hat-matrix) |
| samples | the coordinates of the signal in the standard basis (one per time step) | [The small DFT as a complex unitary matrix](applications/the-small-dft-as-a-complex-unitary-matrix) |
| SCF iteration | fixed-point iteration on an eigenproblem whose matrix depends on its own solution | [Quantum mechanics and quantum computing](applications/quantum-mechanics-and-quantum-computing) |
| sequential modular vs equation-oriented simulation | fixed-point iteration around loops vs solving the whole linear system at once | [Mass balance in a chemical process flowsheet](applications/mass-balance-in-a-chemical-process-flowsheet) |
| share | a point (x_i, f(x_i)), one coordinate of the evaluation map's output | [Shamir secret sharing](applications/shamir-secret-sharing) |
| share refresh (proactive sharing) | adding a sharing of 0, a polynomial from the subspace with f(0) = 0 | [Shamir secret sharing](applications/shamir-secret-sharing) |
| single-pass conversion | the fraction of the reactant entering the reactor that reacts, a fixed coefficient | [Mass balance in a chemical process flowsheet](applications/mass-balance-in-a-chemical-process-flowsheet) |
| sinogram | the measurement vector b, arranged by angle and detector position | [Computed tomography reconstruction](applications/computed-tomography-reconstruction) |
| spectral leakage | energy of a wave that is not one of the N basis waves, spread across many coordinates | [The small DFT as a complex unitary matrix](applications/the-small-dft-as-a-complex-unitary-matrix) |
| spectrum | the coordinate vector in the Fourier basis; its magnitudes are what a spectrum analyzer shows | [The small DFT as a complex unitary matrix](applications/the-small-dft-as-a-complex-unitary-matrix) |
| split fraction | the fraction of a component a separator sends to a given outlet, a fixed coefficient | [Mass balance in a chemical process flowsheet](applications/mass-balance-in-a-chemical-process-flowsheet) |
| square-root filter | propagating a Cholesky factor of P instead of P | [Kalman filtering for navigation](applications/kalman-filtering-for-navigation) |
| state vector | the unknown x being estimated | [Kalman filtering for navigation](applications/kalman-filtering-for-navigation) |
| stationary distribution | the dominant eigenvector, normalized | [PageRank and network centrality](applications/pagerank-and-network-centrality) |
| steady state | Sv = 0 — v lies in the right null space | [Stoichiometric matrices of reaction networks](applications/stoichiometric-matrices-of-reaction-networks) |
| stiffness matrix | the coefficient matrix K; symmetric positive definite once restraints are applied | [Structural analysis of frames and trusses](applications/structural-analysis-of-frames-and-trusses) |
| stoichiometric matrix S | species by reactions, signed integer coefficients | [Stoichiometric matrices of reaction networks](applications/stoichiometric-matrices-of-reaction-networks) |
| streak artifact | the visible signature of undersampling — energy in the near-null space | [Computed tomography reconstruction](applications/computed-tomography-reconstruction) |
| stream | a pipe between units; contributes one unknown per component it carries | [Mass balance in a chemical process flowsheet](applications/mass-balance-in-a-chemical-process-flowsheet) |
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
| threshold k | the dimension of the polynomial space, deg f + 1 | [Shamir secret sharing](applications/shamir-secret-sharing) |
| traffic counts (detector or loop counts) | measured coordinates of x, used to pin down the free variables | [Traffic flow conservation at intersections](applications/traffic-flow-conservation-at-intersections) |
| twiddle factor ω^(kn) | an entry of the DFT matrix | [The small DFT as a complex unitary matrix](applications/the-small-dft-as-a-complex-unitary-matrix) |
| unitary gate | a norm-preserving complex linear map — the complex analogue of an orthogonal matrix | [Quantum mechanics and quantum computing](applications/quantum-mechanics-and-quantum-computing) |
| vector graphics | shapes stored as coordinates in a polynomial space, evaluated at whatever resolution the output needs | [Bezier curves and font rendering](applications/bezier-curves-and-font-rendering) |
| write hole | a crash between writing data and parity, which leaves a stripe that violates its equation | [RAID-5 parity and XOR recovery](applications/raid-5-parity-and-xor-recovery) |
| XOR | addition in GF(2), applied bit by bit | [RAID-5 parity and XOR recovery](applications/raid-5-parity-and-xor-recovery) |
