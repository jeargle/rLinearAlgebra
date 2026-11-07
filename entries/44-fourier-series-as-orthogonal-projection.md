---
id: 44
slug: fourier-series-as-orthogonal-projection
status: written
title: 'Fourier series: the best approximation by sines and cosines is an orthogonal projection'
short_title: Fourier series as orthogonal projection
field_label: Applied analysis, signal processing, acoustics, physics and engineering
tier_note: 'a truncated Fourier series is the orthogonal projection of a function onto the span of finitely
  many sines and cosines, in an inner product defined by an integral. Explaining why sines and cosines
  are the natural basis, as eigenfunctions of the second derivative, is Tier 2.'
nav_field: Mathematics & Numerical Analysis
field: Mathematics
subfield: Applied analysis
tier: 1
tier_ceiling: 2
prereq_beyond_la: integration
scalar_field: R
vector_space: 'piecewise continuous real functions on [−π, π], with inner product ⟨f, g⟩ = ∫ f(x) g(x) dx
  over [−π, π]. The space is infinite-dimensional; each approximation lives in the subspace T_N spanned
  by 1, cos x, sin x, …, cos Nx, sin Nx, of dimension 2N + 1'
underlying_equations: 'Best approximation in an integral (least-squares) sense: choose the coefficients
  of S_N to minimize ∫ (f(x) − S_N(x))² dx over [−π, π]'
core_la_object: Inner-product space of functions
la_concepts: inner products; orthogonality; orthogonal bases; orthogonal projection; best approximation;
  Pythagoras' theorem and Parseval's identity; Gram matrix
primary_method: Projection via orthogonality, one inner product per coefficient; computed from samples
  with the FFT in practice
matrix_structure: diagonal Gram matrix (2π for the constant, π for each sine and cosine); a non-orthogonal
  basis such as 1, x, x², … gives a dense, badly conditioned Gram matrix (the Hilbert matrix on [0, 1])
typical_size: 10-1e6 harmonics
worked_example_size: a square wave projected onto its first 8 harmonics
terminology:
  period and fundamental: the length after which the signal repeats (2π here), and the sine or cosine
    that repeats exactly once in it
  harmonic: sin nx or cos nx, oscillating n times per period
  Fourier coefficients a_n, b_n: the amounts of cos nx and sin nx in the function
  partial sum S_N: the series cut off after the N-th harmonic
  inner product of functions: ⟨f, g⟩ = ∫ f g dx, the continuous analogue of the dot product
  orthogonal functions: functions whose inner product is zero
  norm and energy: ‖f‖² = ⟨f, f⟩, the integral of the square of f
  Gram matrix: the matrix of inner products of the basis functions
  Parseval's identity: the energy of f is the sum of the energies of its components
  Gibbs phenomenon: the overshoot of partial sums next to a jump, which does not shrink as N grows
---

## Start here

A violin and a flute playing the same note sound different, yet both sounds repeat at the same rate.
The difference is in the mixture: each sound is a sum of sine waves, a fundamental that repeats once
per cycle plus harmonics that repeat two, three or more times, and the instruments mix them in
different proportions. Joseph Fourier claimed in his work on heat flow, in the early 1800s, that
almost any repeating function, even one with sudden jumps, can be built this way.

How much of each sine wave goes into the mixture? The textbook answer is an integral of the function
times that sine wave. It looks like calculus, but it is linear algebra. Functions can be added and
scaled like vectors. The integral of the product of two functions behaves like a dot product. Under
that dot product, different sine waves are perpendicular to each other. The coefficient formula is
then the same as the formula for the component of a vector along a perpendicular axis.

Seeing the series this way explains why it works and in what sense a truncated series is the best
approximation. It also explains why the approximation keeps overshooting next to a jump, however many
terms are used.

## The problem

A function f is given on the interval from −π to π and repeats with **period** 2π. The **fundamental**
is sin x or cos x, which repeat once per period. The n-th **harmonic** is sin nx or cos nx, which repeat
n times. A truncated Fourier series, or **partial sum**, of order N is a combination

```
S_N(x)  =  a_0  +  a_1 cos x  +  b_1 sin x  +  …  +  a_N cos Nx  +  b_N sin Nx
```

Given f and N, find the coefficients that make S_N as close as possible to f, say how close it is,
and say in what sense. The running example is the square wave that equals −1 on (−π, 0) and +1 on
(0, π), approximated by its first 8 harmonics: cos x, …, cos 8x and sin x, …, sin 8x, with the constant.

## Variables

| Symbol | Name | What it holds | Shape | Units |
|---|---|---|---|---|
| x | position | point in one period, from −π to π | number | radians |
| f | function | the signal being approximated | function on [−π, π] | units of f |
| n | harmonic number | how many times the harmonic repeats per period | 1, 2, …, N | — |
| N | order | highest harmonic kept | integer | — |
| a_0 | mean | the constant term | number | units of f |
| a_n, b_n | Fourier coefficients | amounts of cos nx and sin nx | numbers | units of f |
| S_N | partial sum | the approximation of order N | function | units of f |
| ⟨f, g⟩ | inner product | ∫ f(x) g(x) dx over [−π, π] | number | units of f times units of g, times radians |
| ‖f‖ | norm | √⟨f, f⟩; its square is the energy | number | units of f times √radians |
| T_N | approximation space | span of 1, cos x, sin x, …, cos Nx, sin Nx | subspace of dimension 2N + 1 | — |
| φ_1, …, φ_K | basis functions | any basis of the approximation space | K functions | dimensionless |
| c | coefficients | S = c_1 φ_1 + … + c_K φ_K in a general basis | K × 1 | units of f |
| G | Gram matrix | G_ij = ⟨φ_i, φ_j⟩ | K × K | radians |
| d | projections | d_i = ⟨φ_i, f⟩ | K × 1 | units of f times radians |

## Formulation

**Where the equations come from.** The goal is a best approximation: among all functions in T_N, find
the S_N that minimizes ‖f − S_N‖² = ∫ (f(x) − S_N(x))² dx over [−π, π]. This is least squares, with the
sum over data points replaced by an integral over the interval.

**The familiar formula.** Textbooks give the coefficients as

```
a_0 = (1/2π) ∫ f(x) dx,      a_n = (1/π) ∫ f(x) cos nx dx,      b_n = (1/π) ∫ f(x) sin nx dx
```

with every integral over [−π, π]. Some books write the constant as a_0/2 with a_0 = (1/π) ∫ f(x) dx; the
partial sum is the same. The rest of this section derives these formulas as a projection.

**Functions as vectors.** Functions on [−π, π] can be added and multiplied by numbers, and the results
are again functions, so they form a vector space. The inner product

```
⟨f, g⟩  =  ∫ f(x) g(x) dx    over [−π, π]
```

has the properties of the dot product: it is symmetric, linear in each argument, and ⟨f, f⟩ is
positive unless f is zero. (Two functions that differ at only finitely many points, such as two
choices for the value of a square wave at its jump, have the same integrals and count as the same
vector.) The analogy is close. Sample f and g at many equally spaced points x_i with spacing Δx, and
Σ f(x_i) g(x_i) Δx is a dot product of two long vectors that tends to the integral as Δx shrinks.

**The harmonics are orthogonal.** For whole numbers m and n,

```
⟨sin mx, sin nx⟩ = ⟨cos mx, cos nx⟩ = 0   when m ≠ n,      ⟨sin mx, cos nx⟩ = 0   always
⟨sin nx, sin nx⟩ = ⟨cos nx, cos nx⟩ = π   for n ≥ 1,        ⟨1, 1⟩ = 2π
```

The reason is the product-to-sum identity, for example
sin mx sin nx = ½ ( cos (m − n)x − cos (m + n)x ), together with the fact that cos jx integrates to zero
over a full period for every whole number j other than 0.

**One coefficient at a time.** In ℝ^n, the component of a vector y along a single vector v is
(v · y / v · v) v. The same formula with the inner product gives the amount of sin nx in f:

```
b_n  =  ⟨f, sin nx⟩ / ⟨sin nx, sin nx⟩  =  (1/π) ∫ f(x) sin nx dx
```

This is the textbook formula, and the 1/π is the squared length of sin nx. For the square wave and
n = 1, the numerator splits at 0:

```
⟨f, sin x⟩  =  ∫_0^π sin x dx  −  ∫_(−π)^0 sin x dx  =  2 + 2  =  4,       b_1 = 4/π ≈ 1.273
```

So the single sine wave closest to the square wave has amplitude 1.273, taller than the wave itself.
It overshoots in the middle of each half-period to make up for being small near the ends.

**All the coefficients together.** For a general basis φ_1, …, φ_K of the approximation space,
minimizing ‖f − Σ c_i φ_i‖² gives the normal equations of the regression entry, with the columns of the
design matrix replaced by functions:

```
G c = d,      G_ij = ⟨φ_i, φ_j⟩,      d_i = ⟨φ_i, f⟩
```

For the basis 1, cos x, sin x, …, cos Nx, sin Nx, orthogonality makes G diagonal:

```
G = diag( 2π, π, π, …, π )
```

Each equation then involves a single coefficient, which gives exactly the formulas above. A
consequence is that adding a harmonic never changes the coefficients already computed.

**Worked case: a square wave and 8 harmonics.** The square wave is odd (f(−x) = −f(x)), and so is
f(x) cos nx, so every a_n is 0, including the mean. For the sines,
⟨f, sin nx⟩ = 2 ∫_0^π sin nx dx = 2(1 − cos nπ)/n, which is 4/n for odd n and 0 for even n. Therefore
b_n = 4/(nπ) for odd n, and the projection onto the first 8 harmonics is

```
S_8(x)  =  (4/π) ( sin x  +  sin 3x / 3  +  sin 5x / 5  +  sin 7x / 7 )
```

with coefficients 1.273, 0.424, 0.255 and 0.182. Of the 17 basis functions, only four are used.

**How close.** The error f − S_N is orthogonal to the whole space T_N, so Pythagoras' theorem holds:

```
‖f‖²  =  ‖S_N‖²  +  ‖f − S_N‖²,       ‖S_N‖²  =  2π a_0²  +  π Σ_n (a_n² + b_n²)
```

For the square wave ‖f‖² = 2π. The fundamental alone captures 8/π², about 81.1% of this energy. The
first 8 harmonics capture 95.0%, 16 harmonics 97.5% and 64 harmonics 99.4%. As N grows the error
energy goes to zero, and the energy of f is the sum of the energies of its components. That is
Parseval's identity, which for the square wave says that 1 + 1/9 + 1/25 + 1/49 + … = π²/8.

## Matrix structure

In the sine-and-cosine basis the Gram matrix is diagonal, and after dividing each basis function by its
length (√(2π) for the constant, √π for the others) it is the identity. Nothing needs to be solved.

A basis that is not orthogonal gives a dense Gram matrix, and it can be very badly conditioned. Project
onto the polynomials 1, x, x² on [0, 1] instead, and the Gram matrix has entries 1/(i + j + 1) for
i, j = 0, 1, 2:

```
[ 1    1/2  1/3 ]
[ 1/2  1/3  1/4 ]
[ 1/3  1/4  1/5 ]
```

This is the Hilbert matrix. Its condition number is about 1.6 × 10⁴ with 4 basis functions,
1.5 × 10¹⁰ with 8 and 1.6 × 10¹³ with 10. Making the polynomials orthogonal by the Gram–Schmidt process
produces the Legendre polynomials (shifted to [0, 1]) and restores a diagonal Gram matrix.

## What is computed

In practice f is known through samples, not as a formula. The integrals are approximated by sums at
equally spaced points, which is the trapezoidal rule, and those sums are exactly the discrete Fourier
transform of the small-DFT entry, computed by the FFT in a number of operations that grows only
slightly faster than the number of samples. For smooth periodic functions the trapezoidal rule is
extraordinarily accurate. Sampling too coarsely makes high harmonics indistinguishable from low ones
(aliasing). Audio coding, image compression and spectral methods for differential equations all rely
on these computed coefficients, often in a cosine-only variant.

## Why linear algebra is the right tool

Every property of Fourier series used in practice follows from orthogonal projection, and none of them
needs anything specific to sines except their orthogonality. The coefficient formula is a component
along an axis. The best-approximation property is the shortest distance from a point to a subspace.
That earlier coefficients do not change when terms are added is a diagonal Gram matrix. The energy
accounting is Pythagoras' theorem. The space of functions is infinite-dimensional, but every
calculation happens in a finite-dimensional subspace T_N, where all the facts from ℝ^n hold unchanged.

## Pitfall worth teaching

Best in the integral sense is not best at every point. Near the jump of the square wave, the partial
sums overshoot the value 1. S_8 peaks at about 1.184, at x = π/8. S_64 peaks at about 1.179, at x = π/64.
As N grows, the peak moves toward the jump but does not get lower: its limit is about 1.179, an
overshoot of about 9% of the jump from −1 to 1. This is the Gibbs phenomenon.

There is no contradiction with convergence. The projection minimizes the integral of the squared
error, and the region where the overshoot happens gets narrower as N grows, so the error energy still
goes to zero while the largest error does not. Smoothly tapering the high coefficients reduces the
overshoot, at the cost of blurring the jump. The same thing happens at the ends of the interval for a
function that is not periodic, such as e^x on [−π, π]: its periodic extension jumps from e^π back to
e^(−π), and the partial sums ring there.

## Extensions

The complex form uses the basis e^(inx) and the complex inner product, with the conjugate on the first
argument, exactly as in the small-DFT entry. Sines and cosines are eigenfunctions of the second
derivative, which is why they decouple linear problems with constant coefficients (Tier 2), and other
eigenvalue problems give other orthogonal families, such as Legendre polynomials and Bessel functions.
That the partial sums converge in norm for every function of finite energy is the completeness of the
basis, studied in Hilbert space theory. The JPEG entry uses a discrete cosine basis on 8-point blocks.
Fitting with basis functions that are not orthogonal is the basis-fitting entry, where the Gram matrix
becomes XᵀX. Wavelets are orthogonal bases whose functions are localized in time as well as frequency.
Empirical orthogonal functions in climate data are orthogonal bases chosen from the data instead of
fixed in advance.
