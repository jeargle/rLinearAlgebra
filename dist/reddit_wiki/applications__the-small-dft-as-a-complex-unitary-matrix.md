# The discrete Fourier transform: a change to a basis of complex waves

### Start here

Any sound, radio signal or row of pixels can be recorded as a list of numbers: the signal's value at
equally spaced moments. For many purposes that list is the wrong description. A musician wants to know
which notes are present, an engineer which frequencies carry interference, and a compression program
which parts can be thrown away without anyone noticing.

The [discrete Fourier transform](https://en.wikipedia.org/wiki/Discrete_Fourier_transform) answers by rewriting the list as a combination of pure waves: a
constant, a wave that goes up and down once over the block of samples, one that goes twice, and so on.
Each wave gets one coefficient, telling how much of it is present and where in its cycle it starts.
The list of coefficients is the signal's spectrum.

That rewriting is a change of coordinates, from "value at each moment" to "amount of each wave". The
waves are perpendicular to each other, which makes the change easy to undo and means it preserves the
total energy of the signal. To describe both how much of a wave is present and where it starts with a
single number, the coordinates are complex numbers, so this is linear algebra over the complex numbers
instead of the real ones.

**Field:** Signal processing, audio, communications, image processing, spectroscopy  
**Tier:** 1 — the DFT is multiplication by one explicit complex matrix whose columns form an orthogonal basis, so it needs complex numbers but no [eigenvalues](https://en.wikipedia.org/wiki/Eigenvalues_and_eigenvectors). That the DFT diagonalizes every [circulant](https://en.wikipedia.org/wiki/Circulant_matrix) matrix, the reason convolution becomes multiplication, is an eigenvector statement and Tier 2.  
**Scalar field:** C, the complex numbers, even when the signal itself is real: the basis vectors are complex waves, so the coordinates are complex  
**Vectors:** C^N for a block of N samples, with the complex inner product ⟨u, v⟩ = Σ conj(u_n) v_n. A real signal lies in the real subset R^N, which is not a complex subspace, and its transform has the conjugate symmetry X_(N−k) = conj(X_k)  
**Underlying equations:** A [change of basis](https://en.wikipedia.org/wiki/Change_of_basis) on a finite block of samples, X = F x

### The problem

Given a block of N equally spaced samples of a signal, find how much of each of the N basic
frequencies it contains, and be able to rebuild the samples exactly from those amounts.

### Variables

| Symbol | Name | What it holds | Shape | Units |
|---|---|---|---|---|
| N | block length | number of samples | integer | — |
| x | signal | samples x_0, …, x_(N−1) | N × 1, complex in general (often real) | signal units (volts, pressure, brightness) |
| ω | root of unity | ω = e^(−2πi/N), so ω^N = 1 | complex scalar | dimensionless |
| w_k | wave of frequency k | (w_k)_n = e^(2πi kn/N): k complete cycles over the block | N × 1 complex | dimensionless |
| F | DFT matrix | F_kn = ω^(kn), for k, n = 0, …, N − 1; row k is the conjugated wave w_k | N × N complex | dimensionless |
| X | spectrum | X = F x; X_k is the coefficient of frequency k | N × 1 complex | signal units |
| U | unitary DFT | U = F / √N | N × N complex | dimensionless |
| Fᴴ | conjugate transpose | the transpose with every entry replaced by its complex conjugate | N × N | dimensionless |

Bin k corresponds to k cycles per block, which is k / (N Δt) cycles per second if the samples are Δt
seconds apart.

### Formulation

**Where the equations come from.** The model is a choice of basis
for the space of length-N blocks of samples.

**One frequency at a time.** The wave of frequency k is the vector w_k whose n-th entry is

```
(w_k)_n = e^(2πi kn/N) = cos(2π kn/N) + i sin(2π kn/N),     n = 0, …, N − 1
```

As n runs through the block, its angle 2π kn/N goes round the unit circle exactly k times, so w_k
makes k complete cycles: w_0 is the constant vector, w_1 one slow cycle, and so on. To measure how much
of this wave the signal contains, multiply each sample by the complex conjugate of the wave's value at
that moment and add the results:

```
X_k = Σ_(n=0)^(N−1) x_n · conj((w_k)_n) = Σ_(n=0)^(N−1) x_n e^(−2πi kn/N)
```

This is the familiar DFT formula from signal processing. It is the complex inner product of the wave
with the signal, X_k = ⟨w_k, x⟩, where the inner product on ℂ^N conjugates its first argument,
⟨u, v⟩ = Σ conj(u_n) v_n, so that ⟨v, v⟩ = Σ |v_n|² is a length squared. Splitting the exponential
into its cosine and sine parts shows what the number means. The real part of X_k is Σ x_n cos(2π kn/N),
the correlation of the signal with a cosine of frequency k, and the imaginary part is
−Σ x_n sin(2π kn/N), the correlation with a sine. Together they say how large the frequency-k
component is, |X_k|, and where in its cycle it starts, the angle of X_k.

**All frequencies at once.** Doing this for every k = 0, …, N − 1 gives N inner products, one per
frequency. Stacking them, row k of a matrix holds the conjugated wave, e^(−2πi kn/N) = ω^(kn) in
column n, and the whole spectrum is one matrix-vector product:

```
X = F x,     F_kn = ω^(kn)
```

**Orthogonality, and the inverse.** With the complex inner product, the N waves w_0, …, w_(N−1) are
mutually orthogonal and each has squared length N:

```
Fᴴ F = N I
```

So the inverse is just the [conjugate transpose](https://en.wikipedia.org/wiki/Conjugate_transpose), scaled: x = (1/N) Fᴴ X, which is the inverse DFT
formula x_n = (1/N) Σ X_k e^(2πi kn/N). Scaled to U = F/√N, the matrix is [unitary](https://en.wikipedia.org/wiki/Unitary_matrix), Uᴴ U = I: the
complex version of an [orthogonal matrix](https://en.wikipedia.org/wiki/Orthogonal_matrix), a rotation of ℂ^N.

**[Parseval](https://en.wikipedia.org/wiki/Parseval's_theorem)'s identity.** A unitary change of basis preserves length, so Σ |x_n|² = (1/N) Σ |X_k|²:
the energy of the signal can be added up over time or over frequency.

**Worked case: N = 4.** Here ω = e^(−2πi/4) = −i, so every entry of F is 1, −i, −1 or i:

```
F = [ 1    1    1    1 ]
    [ 1   −i   −1    i ]
    [ 1   −1    1   −1 ]
    [ 1    i   −1   −i ]
```

For x = (1, 2, 3, 4), one coefficient at a time, X_1 multiplies the samples by the row
(1, −i, −1, i) and adds them:

```
X_1 = 1·1 + 2·(−i) + 3·(−1) + 4·(i) = −2 + 2i
```

and doing the same with every row gives the whole spectrum:

```
X = F x = (10,  −2 + 2i,  −2,  −2 − 2i)
```

X_0 = 10 is the sum, four times the mean (the DC component). X_2 = −2 is the alternating pattern
+ − + −, the fastest wave four samples can hold. X_3 is the complex conjugate of X_1, as it must be for
a real signal. Parseval checks: 1 + 4 + 9 + 16 = 30, and (100 + 8 + 4 + 8)/4 = 30. Multiplying X by
Fᴴ/4 returns (1, 2, 3, 4).

### Matrix structure

`F` is dense, complex and [symmetric](https://en.wikipedia.org/wiki/Symmetric_matrix) (F_kn = F_nk), but it is not [Hermitian](https://en.wikipedia.org/wiki/Hermitian_matrix), because the conjugate of
its transpose is a different matrix. Scaled by 1/√N it is unitary. All its entries are powers of a
single number ω, which lie on the unit circle, and that repetition is what lets the matrix be factored
into about log₂ N [sparse](https://en.wikipedia.org/wiki/Sparse_matrix) factors.

### What is computed

For small N, or a handful of frequencies, the transform is computed directly as a matrix-vector
product. For anything larger, the [fast Fourier transform](https://en.wikipedia.org/wiki/Fast_Fourier_transform) computes exactly the same product in
O(N log N) operations instead of O(N²) by factoring F into sparse matrices (the FFT entry). Libraries
such as FFTW, numpy.fft and Julia's FFTW.jl differ in scaling conventions, which the pitfall
discusses.

### Why linear algebra is the right tool

Seeing the DFT as a change of basis explains its properties without computation. It is invertible
because the waves are a basis. The inverse is cheap because the basis is orthogonal, and energy is
preserved because the change is unitary. Filtering is "change basis, scale some coordinates, change
back". [Leakage](https://en.wikipedia.org/wiki/Spectral_leakage), the spreading of a pure tone across many bins, happens because a wave whose frequency
is not a whole number of cycles per block is not one of the N basis vectors, so its coordinates in that
basis are spread out. Compression works because many real signals have most of their length in a few
coordinates of a well-chosen basis.

### Pitfall worth teaching

In ℂ^N, the transpose is not the inverse of a unitary matrix; the conjugate transpose is. Using the
plain transpose, as one would for a real orthogonal matrix, is a common bug: Uᵀ U is not the identity.
For N = 4 it is the matrix that reverses the order of bins 1 to 3, so "inverting" with the transpose
returns the signal with time running backwards (x_0, x_3, x_2, x_1) instead of an error message. In
NumPy, `U.T` is the transpose and `U.conj().T` the conjugate transpose; in MATLAB and Julia, `'`
conjugates and `.'` or `transpose` does not. The same bug appears as forgetting to conjugate when
computing a complex inner product. A second source of disagreement is convention: libraries put the
1/N on the inverse (NumPy, MATLAB), split it as 1/√N on both sides (the unitary convention), or
leave it to the user (FFTW), and some fields use e^(+2πi kn/N) in the forward transform. All of them
are the same change of basis with differently scaled or conjugated basis vectors.

### Extensions

The DFT matrix diagonalizes every circulant matrix, which is why convolution in time becomes
multiplication in frequency; that is an eigenvector statement (Tier 2). The FFT as a matrix
factorization is its own entry. The [discrete cosine transform](https://en.wikipedia.org/wiki/Discrete_cosine_transform) of JPEG compression is a real orthogonal
cousin (the JPEG entry), and Fourier series are the same idea for functions on an interval rather than
finite blocks (the Fourier series entry). Orthogonal [frequency-division multiplexing](https://en.wikipedia.org/wiki/Orthogonal_frequency-division_multiplexing) (OFDM), used in
Wi-Fi, 4G and 5G, transmits data directly as DFT coordinates. Quantum computing's quantum Fourier
transform is this unitary matrix acting on the amplitudes of n [qubits](https://en.wikipedia.org/wiki/Qubit), with N = 2^n.

### Terminology

How this field's vocabulary reads as linear algebra.

| Domain term | In linear algebra |
|---|---|
| samples | the coordinates of the signal in the standard basis (one per time step) |
| frequency bin k | the coefficient of the k-th complex wave in the Fourier basis |
| spectrum | the coordinate vector in the Fourier basis; its magnitudes are what a spectrum analyzer shows |
| inverse DFT | the change of basis back, using the conjugate transpose |
| twiddle factor ω^(kn) | an entry of the DFT matrix |
| DC component | bin 0, the coefficient of the constant vector, N times the mean |
| Nyquist bin | bin N/2, the fastest wave a block of N samples can represent |
| negative frequencies | bins N/2 + 1 to N − 1, the complex conjugates of positive ones for a real signal |
| Parseval's theorem | the change of basis preserves length (energy), up to the factor N |
| spectral leakage | energy of a wave that is not one of the N basis waves, spread across many coordinates |
| FFT | a factorization of the DFT matrix into sparse factors, not a different transform |

---

[Back to the index](/r/LinearAlgebra/wiki/applications)
