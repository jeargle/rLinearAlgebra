# The fast Fourier transform: the DFT matrix as a product of sparse factors

### Start here

The [discrete Fourier transform](https://en.wikipedia.org/wiki/Discrete_Fourier_transform) turns a block of signal samples into a list of frequency amounts. Done
the obvious way, each of the amounts needs every sample, so the work grows with the square of the block
length. A block of a million samples would take about a trillion multiplications.

The [fast Fourier transform](https://en.wikipedia.org/wiki/Fast_Fourier_transform) gets exactly the same answer with about ten million. It is not an
approximation and not a different transform. It is a smarter order of operations: the waves being
compared against are made of the same few numbers over and over, so most of the products are repeats.

In matrix language, the transform is multiplication by one dense matrix, and the fast algorithm writes
that matrix as a product of a handful of very [sparse](https://en.wikipedia.org/wiki/Sparse_matrix) ones. This is why audio software, phone networks,
medical scanners and weather models can afford Fourier analysis at all.

**Field:** Signal processing, audio, communications, image processing, scientific computing  
**Tier:** 2 — the factorization itself is matrix multiplication, but the entry rests on each scaled factor being a [unitary](https://en.wikipedia.org/wiki/Unitary_matrix) matrix, which explains the numerical stability, and its main application, fast convolution, rests on the DFT diagonalizing [circulant](https://en.wikipedia.org/wiki/Circulant_matrix) matrices, an [eigenvector](https://en.wikipedia.org/wiki/Eigenvalues_and_eigenvectors) statement. That makes it Tier 2. [Rader's algorithm](https://en.wikipedia.org/wiki/Rader's_FFT_algorithm) for prime N uses the group structure of the integers modulo a prime, and the quantum Fourier transform needs quantum mechanics; both are Tier 3.  
**Scalar field:** C, the complex numbers: the [twiddle factors](https://en.wikipedia.org/wiki/Twiddle_factor) are complex roots of unity even when the signal is real  
**Vectors:** C^N for a block of N samples, with N a power of 2 in the radix-2 form. Every stage maps C^N to C^N; the two half-length transforms act separately on the even-indexed and the odd-indexed samples, two copies of C^(N/2)  
**Underlying equations:** A change of basis on a finite block of samples, X = F_N x, computed through the factorization F_N = B_N (F_(N/2) ⊕ F_(N/2)) P_N applied recursively

### The problem

Some vocabulary first. A signal is recorded as samples: its values at equally spaced moments, for
example 44,100 per second for audio. A block is a run of consecutive samples, stored as one vector. The
discrete Fourier transform (DFT) of the block is its spectrum: the coordinates of the block in a basis
of complex waves (the small DFT entry). An operation count is the number of complex multiplications and
additions an algorithm uses.

The motivating contrast is between a transform and an algorithm. The DFT is one fixed linear map; the
fast Fourier transform (FFT) is a way of computing it, and returns the same spectrum, up to rounding,
as the direct product. The difference is cost: for a block of N samples, N squared multiplications
directly, against about N/2 times log₂ N, where log₂ N is the number of times N can be halved before
reaching 1.

Given: the block of samples and its length, a power of 2 here. Unknown: the spectrum. The question is
why the spectrum is so cheap to compute. The answer is that the DFT matrix factors into about log₂ N
sparse matrices, each with two nonzero entries per row: the speed of the FFT is a statement about
structure.

### Variables

| Symbol | Name | What it holds | Shape | Units |
|---|---|---|---|---|
| N | block length | number of samples, a power of 2 | integer | — |
| n, k | time index, frequency index | 0, …, N − 1 | integer | — |
| m | half-block index | 0, …, N/2 − 1; sample 2m is even, 2m + 1 odd | integer | — |
| x | signal | samples x_0, …, x_(N−1) | N × 1 complex (often real) | signal units |
| X | spectrum | X = F_N x | N × 1 complex | signal units |
| ω_N | root of unity | e^(−2πi/N); ω_4 = −i and ω_2 = −1 | complex scalar | dimensionless |
| F_N | DFT matrix | entry (k, n) is ω_N^(kn) | N × N complex | dimensionless |
| E_k, O_k | even and odd half-spectra | entry k of the length-N/2 DFTs of (x_0, x_2, …) and of (x_1, x_3, …) | N/2 × 1 each | signal units |
| P_N | even/odd permutation | reorders x to (x_0, x_2, …, x_1, x_3, …) | N × N, entries 0 and 1 | dimensionless |
| I_(N/2) | identity matrix | | N/2 × N/2 | — |
| D_(N/2) | twiddle matrix | diagonal, entries ω_N^0, ω_N^1, …, ω_N^(N/2−1) | N/2 × N/2 | dimensionless |
| B_N | butterfly matrix | one stage of N/2 butterflies | N × N, 2 nonzeros per row | dimensionless |
| L | number of stages | L = log₂ N | integer | — |
| S_j | stage j | the j-th sparse factor, j = 1, …, L | N × N, 2 nonzeros per row | dimensionless |
| R_N | bit-reversal permutation | the product of all the even/odd permutations | N × N, entries 0 and 1 | dimensionless |
| U_N | unitary DFT | F_N / √N | N × N complex | dimensionless |
| M(N) | multiplication count | complex multiplications the FFT uses | integer | — |
| C | circulant matrix | each row is the row above shifted one place right, wrapping around | N × N | depends on use |
| c | generating vector | the first column of C | N × 1 | depends on use |

### Formulation

**Where the equations come from.** The model is the same change of basis as in the small DFT entry,
X = F_N x. Nothing new is modeled; the content is a factorization of a known matrix.

**The familiar formula.** Texts usually derive the FFT by the [Cooley–Tukey](https://en.wikipedia.org/wiki/Cooley%E2%80%93Tukey_FFT_algorithm) split of the DFT sum
X_k = Σ_(n=0)^(N−1) x_n ω_N^(kn) into even-indexed samples (n = 2m) and odd-indexed ones (n = 2m + 1):

```
X_k = Σ_(m=0)^(N/2−1) x_(2m) ω_N^(2mk)  +  ω_N^k · Σ_(m=0)^(N/2−1) x_(2m+1) ω_N^(2mk)
```

Squaring ω_N = e^(−2πi/N) gives e^(−2πi/(N/2)) = ω_(N/2), so ω_N^(2mk) = ω_(N/2)^(mk), and each sum is
a DFT of length N/2. The first is E_k, from the even samples; the second is O_k, from the odd ones.
Both repeat with period N/2 in k, and ω_N^(N/2) = e^(−πi) = −1, so ω_N^(k+N/2) = −ω_N^k. Hence:

```
X_k       = E_k + ω_N^k O_k
X_(k+N/2) = E_k − ω_N^k O_k,        k = 0, …, N/2 − 1
```

**One [butterfly](https://en.wikipedia.org/wiki/Butterfly_diagram).** For one k, the pair (E_k, O_k) becomes the pair (X_k, X_(k+N/2)):

```
[ X_k       ]   [ 1    ω_N^k ]   [ E_k ]
[ X_(k+N/2) ] = [ 1   −ω_N^k ] × [ O_k ]
```

This 2 × 2 map is called a butterfly because, drawn as a signal-flow diagram, its crossing lines look
like a butterfly's wings. The number ω_N^k is called a twiddle factor because it twiddles, that is
rotates, O_k around the unit circle before the sum and difference are taken. The product ω_N^k O_k is
computed once and used twice.

**All butterflies at once.** Stacking the N/2 butterflies, with the twiddle factors on the diagonal of
D_(N/2), gives the butterfly matrix

```
B_N = [ I_(N/2)    D_(N/2) ]
      [ I_(N/2)   −D_(N/2) ]
```

To get E and O, the permutation P_N lists the even samples, then the odd ones, and the
[block-diagonal](https://en.wikipedia.org/wiki/Block_matrix) matrix F_(N/2) ⊕ F_(N/2) transforms each half. The symbol ⊕ (direct sum) means the
matrix with the two blocks on its diagonal and zeros elsewhere: for example, [1] ⊕ [2] is the 2 × 2
matrix with rows (1, 0) and (0, 2). Together:

```
F_N = B_N (F_(N/2) ⊕ F_(N/2)) P_N
```

**Worked case: N = 4.** This extends the small DFT entry's 4-point example. Here ω_4 = −i, ω_2 = −1,
and the twiddle factors are ω_4^0 = 1 and ω_4^1 = −i. As scalar equations in x_0, …, x_3, the two
2-point transforms are

```
E_0 = x_0 + x_2        O_0 = x_1 + x_3
E_1 = x_0 − x_2        O_1 = x_1 − x_3
```

and the butterflies combine them:

```
X_0 = E_0 + O_0        X_2 = E_0 − O_0
X_1 = E_1 − i O_1      X_3 = E_1 + i O_1
```

As matrices, row by row: the permutation P_4, the two copies of F_2 = [1 1; 1 −1], and the butterfly
B_4 with D_2 = diag(1, −i), the diagonal matrix with 1 and −i on its diagonal:

```
P_4 = [ 1  0  0  0 ]     F_2 ⊕ F_2 = [ 1   1   0   0 ]     B_4 = [ 1  0   1   0 ]
      [ 0  0  1  0 ]                 [ 1  −1   0   0 ]           [ 0  1   0  −i ]
      [ 0  1  0  0 ]                 [ 0   0   1   1 ]           [ 1  0  −1   0 ]
      [ 0  0  0  1 ]                 [ 0   0   1  −1 ]           [ 0  1   0   i ]
```

The product B_4 (F_2 ⊕ F_2) is F_4 with its middle columns swapped, because the inputs sit in the order
(x_0, x_2, x_1, x_3); P_4 swaps them back:

```
B_4 (F_2 ⊕ F_2) = [ 1   1   1   1 ]        B_4 (F_2 ⊕ F_2) P_4 = [ 1   1   1   1 ] = F_4
                  [ 1  −1  −i   i ]                              [ 1  −i  −1   i ]
                  [ 1   1  −1  −1 ]                              [ 1  −1   1  −1 ]
                  [ 1  −1   i  −i ]                              [ 1   i  −1  −i ]
```

One signal through the factored route: the known input is x = (1, 2, 3, 4), as in the small DFT entry,
and X is unknown:

```
P_4 x                     = (1, 3, 2, 4)
(F_2 ⊕ F_2) P_4 x         = (4, −2, 6, −2)          so E = (4, −2), O = (6, −2)
twiddled odd half         = (1 · 6, −i · (−2))      = (6, 2i)
X = B_4 (F_2 ⊕ F_2) P_4 x = (4 + 6, −2 + 2i, 4 − 6, −2 − 2i) = (10, −2 + 2i, −2, −2 − 2i)
```

This matches the direct product, which used 16 multiplications by entries of F_4 and 12 additions. The
factored route used 4 twiddle multiplications (one per butterfly, counting the trivial ones by 1) and 8
additions. Only one of them, by −i, is not by 1, and it only swaps real and imaginary parts and changes
a sign.

**The general recursion.** Each F_(N/2) splits the same way, down to F_2, itself a butterfly with
twiddle factor 1. After L = log₂ N levels the DFT matrix is a product of L sparse stages and one
permutation:

```
F_N = S_1 S_2 ⋯ S_L R_N
```

Stage S_1 is B_N, stage S_2 is B_(N/2) ⊕ B_(N/2), and the last stage is N/2 copies of F_2 on the
diagonal. The permutations from every level combine into R_N, the [bit-reversal permutation](https://en.wikipedia.org/wiki/Bit-reversal_permutation): it puts
sample n at the position whose binary digits are those of n written backwards. For N = 8 the input
order is (x_0, x_4, x_2, x_6, x_1, x_5, x_3, x_7); for example,
position 3 (011 in binary) holds x_6 (110). For N = 4, R_4 is the P_4 above.

**The operation count.** Each stage holds N/2 butterflies, and each butterfly costs one multiplication
and two additions, so

```
M(N) = (N/2) log₂ N multiplications,     N log₂ N additions
```

against N² multiplications for the direct product. In [big-O notation](https://en.wikipedia.org/wiki/Big_O_notation) the FFT is O(N log N) and the
direct product O(N²). O(f(N)) means growing no faster than a constant times f(N); for example, 3N² + 5N
is O(N²).

| N | direct product, N² | FFT, (N/2) log₂ N | ratio |
|---|---|---|---|
| 4 | 16 | 4 | 4 |
| 8 | 64 | 12 | 5.3 |
| 1,024 | 1,048,576 | 5,120 | 205 |
| 1,048,576 | about 1.1 × 10^12 | 10,485,760 | about 104,858 |

**Unitarity of every stage.** The [conjugate transpose](https://en.wikipedia.org/wiki/Conjugate_transpose) of a matrix, marked with a superscript ᴴ, is its
transpose with every entry replaced by its complex conjugate; for example, the conjugate transpose of
the row (1, −i) is the column with entries 1 and i. For the butterfly matrix, writing I and D for
I_(N/2) and D_(N/2),

```
B_Nᴴ B_N = [ I + I        D − D     ]  =  2 I
           [ Dᴴ − Dᴴ      DᴴD + DᴴD ]
```

because every twiddle factor has absolute value 1, so DᴴD = I. Thus B_N / √2 is unitary, and so is
F_2 / √2. [Permutation matrices](https://en.wikipedia.org/wiki/Permutation_matrix) are unitary too, and (1/√2)^L = 1/√N, so U_N = F_N / √N is a product of
L unitary sparse factors and a permutation. A unitary factor preserves length, so a [rounding error](https://en.wikipedia.org/wiki/Round-off_error) made
at one stage is not amplified by the stages after it, which is why the rounding error of the FFT grows
only slowly with N, typically more slowly than that of the direct sum.

### Matrix structure

F_N is dense: all N² entries are nonzero and have absolute value 1. Each stage S_j has exactly two
nonzeros per row, 2N in all, so the factors hold 2N log₂ N nonzeros against N² for F_N. The sparsity is
not in the matrix but in its factors. A generic dense matrix has no such factorization; F_N has one
because its entries are powers of one root of unity, and ω_N² = ω_(N/2) makes its diagonal blocks
smaller DFT matrices. Because F_N and R_N are both symmetric, transposing gives a second factorization,
F_N = R_N S_Lᵀ ⋯ S_1ᵀ.

### What is computed

The spectrum X, in L passes over one array of length N. Each pass applies one stage, and each butterfly
reads two array slots and overwrites the same two, so the FFT runs in place. Decimation in time is the
factorization above: reorder the input by bit reversal, then apply the stages. Decimation in frequency
is the transposed factorization: natural-order input, bit-reversed output. The inverse transform uses
the same factors conjugated, because F_N⁻¹ = (1/N) F_Nᴴ. Libraries such as FFTW, numpy.fft and Julia's
FFTW.jl handle any N by mixing radices; FFTW times equivalent factorizations on the machine and keeps
the fastest as a plan. On graphics processors, NVIDIA's cuFFT plays the same role.

### Why linear algebra is the right tool

The recursive code and the matrix identity F_N = B_N (F_(N/2) ⊕ F_(N/2)) P_N say the same thing, but
the identity makes the cost visible: L factors with 2N nonzeros each. Variants that look different in
code, for example decimation in time or in frequency, or orderings that avoid the bit-reversal pass,
are different factorizations of the same matrix. Unitarity of the scaled stages explains stability
without analyzing the code. The speed-up is a property of the matrix, not of clever programming.

### Pitfall worth teaching

Zero padding a block to a power of 2 does not compute the same transform faster. It computes a
different one. For x = (1, 2, 3), the 3-point DFT is (6, −1.5 + 0.866i, −1.5 − 0.866i), with frequency
bins at 1/3 and 2/3 of a cycle per sample. Padding to (1, 2, 3, 0) and using F_4 gives
(6, −2 − 2i, 2, −2 + 2i), with bins at 1/4, 1/2 and 3/4. Both are correct answers to different
questions. Padding suits a finer frequency grid or fast convolution (below), not speeding up a
fixed-length transform. Modern libraries are fast for any N, including primes. A second trap: a
hand-written radix-2 FFT that skips the reordering returns a plausible-looking but bit-reversed
spectrum.

### Extensions

Splitting by 4 instead of 2 (radix-4), or by 2 and 4 together ([split-radix](https://en.wikipedia.org/wiki/Split-radix_FFT_algorithm)), regroups the stages so
more twiddle factors are ±1 or ±i. The general Cooley–Tukey algorithm splits any composite N the same
way. For prime N, [Bluestein](https://en.wikipedia.org/wiki/Chirp_Z-transform)'s chirp-z algorithm rewrites kn = (k² + n² − (k − n)²)/2, turning the DFT
into a convolution that a power-of-2 FFT computes; Rader's algorithm uses the integers modulo a prime
instead (Tier 3).

Fast convolution is the main application. A convolution is a sliding weighted sum, the operation every
linear filter performs, and on a block that wraps around it is multiplication by a circulant matrix C.
The DFT diagonalizes every circulant matrix: C = F_N⁻¹ diag(F_N c) F_N, where diag(F_N c) is the
diagonal matrix holding the entries of F_N c. This eigenvector statement is the matrix form of the
[convolution theorem](https://en.wikipedia.org/wiki/Convolution_theorem), and it makes a length-N convolution cost three FFTs instead of N² multiplications;
see the small DFT entry. The two-dimensional (2D) FFT of an image applies F_N to every row and then to
every column. The [discrete cosine transform](https://en.wikipedia.org/wiki/Discrete_cosine_transform) of [JPEG](https://en.wikipedia.org/wiki/JPEG) (Joint Photographic Experts Group) image
compression has a butterfly factorization of the same kind (the JPEG entry). In the
beamforming and MUSIC (multiple signal classification) entry, an FFT across a uniform line of sensors
forms beams in N directions at once.

The quantum Fourier transform is U_N, with the opposite sign in the exponent, acting on L = log₂ N
[qubits](https://en.wikipedia.org/wiki/Qubit) (the quantum computing entry). Its circuit of about L²/2 gates is the same factorization written
with [Kronecker products](https://en.wikipedia.org/wiki/Kronecker_product): Hadamard gates (F_2 / √2), controlled phase rotations (the twiddle factors)
and final swap gates (the bit reversal). The Kronecker product of two matrices replaces each entry of
the first by that entry times the whole second matrix; for example, the Kronecker product of the 2 × 2
identity with F_2 is F_2 ⊕ F_2.

### Terminology

How this field's vocabulary reads as linear algebra.

| Domain term | In linear algebra |
|---|---|
| DFT matrix F_N | the dense matrix with entries ω_N^(kn) that the FFT factors |
| fast Fourier transform (FFT) | any algorithm that computes F_N x through a sparse factorization of F_N; the same transform as the DFT, not an approximation |
| Cooley–Tukey algorithm | the split F_N = B_N (F_(N/2) ⊕ F_(N/2)) P_N, applied recursively |
| radix-2 | splitting in two at every level, so N must be a power of 2 |
| decimation in time | splitting the input into even- and odd-indexed samples, the permutation P_N on the right |
| decimation in frequency | the transposed factorization, with the permutation on the output side |
| butterfly | the 2 × 2 map taking (E_k, O_k) to (E_k + ω_N^k O_k, E_k − ω_N^k O_k) |
| butterfly matrix B_N | [I D; I −D], one stage of N/2 butterflies |
| twiddle factor ω_N^k | a diagonal entry of D_(N/2), the rotation applied to O_k |
| stage S_j | one sparse factor, with 2 nonzeros per row; there are L = log₂ N of them |
| bit-reversal permutation R_N | the product of all the even/odd permutations; it moves sample n to the position whose binary digits are those of n reversed |
| in-place FFT | each butterfly reads and overwrites the same two array slots, so no second array is needed |
| O(N log N) | the operation count M(N) = (N/2) log₂ N multiplications and N log₂ N additions |
| zero padding | appending zeros to reach a convenient N, which computes a different transform |
| plan | a library's precomputed choice of factorization for one N |

---

[Back to the index](/r/LinearAlgebra/wiki/applications)
