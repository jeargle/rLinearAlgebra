---
id: 18
slug: beamforming-and-music-direction-finding
status: written
title: 'Beamforming and MUSIC: finding directions from the eigenvectors of an array covariance'
short_title: Beamforming and MUSIC direction finding
field_label: Radar, sonar, wireless communications, microphone arrays, radio astronomy, seismology
tier_note: 'the directions are read off the eigenvectors of a Hermitian covariance matrix: the ones with
  the largest eigenvalues span the signal subspace, and the steering vectors of the true directions are
  orthogonal to the rest. That is the spectral theorem, so the entry is Tier 2. Random-process theory,
  statistical consistency and the Cramér–Rao bound are Tier 3 and appear only in Extensions.'
nav_field: Signal Processing
field: Engineering
subfield: Radar/sonar/wireless
tier: 2
tier_ceiling: 3
prereq_beyond_la: random processes; estimation theory
scalar_field: 'C, the complex numbers: each sensor sample is an amplitude and a phase, recorded as one
  complex number'
vector_space: 'C^M, one coordinate per sensor: a snapshot x(t) is a vector in C^M. The steering vectors
  a(θ) form a curve in C^M (the array manifold), not a subspace; the signal subspace is the span of the
  d steering vectors of the actual sources, and the covariance R is a Hermitian M × M matrix'
underlying_equations: 'A statistical model of plane waves plus noise: snapshots x(t) = A s(t) + n(t),
  with spatial covariance R = A R_ss Aᴴ + σ² I'
core_la_object: Signal and noise subspaces
la_concepts: eigendecomposition of covariance; subspace separation; Hermitian matrices; orthogonal
  complement; conjugate transpose
primary_method: Eigendecomposition
matrix_structure: small dense Hermitian positive semidefinite; Toeplitz for a uniform array and
  uncorrelated sources
typical_size: 1e1-1e2 sensors
worked_example_size: 3-sensor array with one source at 30° by hand; 8-sensor array with two sources 10° apart simulated
terminology:
  sensor (array element): one antenna, hydrophone or microphone; one coordinate of C^M
  snapshot x(t): the M complex sensor samples at one instant, a vector in C^M
  direction of arrival θ: the angle of a source from broadside (straight ahead of the array)
  steering vector a(θ): the snapshot a unit plane wave from angle θ would produce, entries e^(−iπ m sin θ)
  array manifold: the curve of all steering vectors a(θ) as θ varies
  spatial covariance matrix R: E[x xᴴ], Hermitian positive semidefinite, M × M
  sample covariance R̂: (1/N) Σ x(t) x(t)ᴴ over N snapshots, the estimate of R actually computed
  beamformer weights w: a vector in C^M; the output is the inner product wᴴ x
  delay-and-sum beamformer: weights w = a(θ); output power a(θ)ᴴ R a(θ)
  beam pattern: 'the response |a(θ_0)ᴴ a(θ)|² of a beam aimed at θ_0, as θ varies'
  aperture: the length of the array; it sets the beamwidth, about 2/M in sin θ
  signal subspace: span of the d eigenvectors of R with the largest eigenvalues, equal to the column space of A
  noise subspace E_n: the orthogonal complement, spanned by the M − d eigenvectors with eigenvalue σ²
  MUSIC pseudospectrum: 1 / ‖E_nᴴ a(θ)‖², infinite where a(θ) is orthogonal to the noise subspace
  model order d: the number of sources, the number of eigenvalues above the noise floor
  coherent sources: delayed copies of one signal (multipath) that make R_ss singular
  spatial smoothing: averaging covariances of overlapping subarrays to restore the rank of R_ss
---

## Start here

A row of antennas, underwater microphones or ordinary microphones listens to a sound or radio wave
arriving from some direction. The wave reaches the near end of the row a little before the far end,
so each sensor hears the same signal with a slightly different delay. The pattern of delays across
the row says which way the wave came from.

The traditional way to read that pattern is to "point" the row electronically: for each candidate
direction, undo the delays that direction would cause and add the sensor outputs. Waves from that
direction add up strongly, others partly cancel. Pointing everywhere and listening for the loudest
direction works, but two sources close together blur into one, because a short row cannot point
sharply.

A second method, MUSIC, uses linear algebra instead. It collects many recordings, builds a matrix
that says how the sensors vary together, and splits the space of possible recordings into a part
the sources can reach and a part only noise reaches. The true directions are exactly those whose
delay patterns have nothing in the noise-only part, and that test can separate sources that pointing
cannot.

## The problem

A **sensor array** is a set of M sensors, for example 8 antennas on a radar mast or 4 microphones in a
smart speaker. Here the sensors stand in a straight line, equally spaced, half a wavelength apart: a
uniform linear array. A **source** is a distant emitter, for example an aircraft or a talker, whose
wave arrives as a plane wave from a **direction of arrival** θ, measured from broadside (the direction
straight ahead of the line). A **snapshot** is the set of M complex samples taken at one instant: each
sample records the amplitude and the phase of the wave at one sensor. Direction finding means: from N
snapshots, estimate the directions of d sources.

The motivating contrast is between steering and subspace methods. Steering (beamforming) scans a
beam across all angles and reports where the received power is high; its sharpness is fixed by the
length of the array, the aperture. A subspace method fits a model of the covariance and reports the
angles the model says are occupied, which can resolve sources closer than one beamwidth. The subspace
method in this entry is multiple signal classification (MUSIC).

## Variables

| Symbol | Name | What it holds | Shape | Units |
|---|---|---|---|---|
| M | number of sensors | array elements, indexed m = 0, …, M − 1 | integer | — |
| θ | direction of arrival | angle of a source from broadside | scalar | degrees |
| d | number of sources | the model order; d < M | integer | — |
| a(θ) | steering vector | entries a_m(θ) = e^(−iπ m sin θ) | M × 1 complex | dimensionless |
| A | array response matrix | columns a(θ_1), …, a(θ_d) | M × d complex | dimensionless |
| s(t) | source signals | complex amplitude of each source at time t | d × 1 complex | signal units |
| n(t) | sensor noise | independent noise at each sensor | M × 1 complex | signal units |
| x(t) | snapshot | x(t) = A s(t) + n(t) | M × 1 complex | signal units |
| N | number of snapshots | times t = 1, …, N | integer | — |
| R_ss | source covariance | E[s sᴴ]; diag(σ_s², …) for uncorrelated sources | d × d | signal units² |
| σ_s², σ² | source and noise power | variance of one source; of the noise at each sensor | scalars | signal units² |
| R | spatial covariance | R = E[x xᴴ] | M × M Hermitian | signal units² |
| R̂ | sample covariance | (1/N) Σ x(t) x(t)ᴴ | M × M Hermitian | signal units² |
| P(θ) | delay-and-sum power | a(θ)ᴴ R a(θ) | scalar | signal units² |
| λ_k, u_k | eigenpairs of R | R u_k = λ_k u_k, λ_1 ≥ … ≥ λ_M | scalar, M × 1 | signal units², dimensionless |
| E_s, E_n | subspace bases | E_s = [u_1 … u_d], E_n = [u_(d+1) … u_M] | M × d, M × (M − d) | dimensionless |
| P_MU(θ) | MUSIC pseudospectrum | 1 / ‖E_nᴴ a(θ)‖² | scalar | dimensionless |

## Formulation

**Where the equations come from.** The model is statistical: plane waves plus independent noise,
summarized by second moments. No equation of motion is solved.

**One sensor.** The familiar formula is the path difference: a plane wave from angle θ travels an
extra distance (spacing) × sin θ to reach each next sensor. With spacing half a wavelength, that is
half a cycle times sin θ, a phase lag of π sin θ per sensor. Sensor m therefore sees the source
amplitude s multiplied by e^(−iπ m sin θ). For example, at θ = 30°, sin θ = 1/2 and the factors for
m = 0, 1, 2 are e^0 = 1, e^(−iπ/2) = −i and e^(−iπ) = −1.

**All sensors.** Stacking the M factors gives the steering vector a(θ), and stacking one steering
vector per source gives A. One snapshot is then

```
x(t) = A s(t) + n(t)
```

The noisy snapshot is known; A (through the angles θ_k) and s(t) are unknown.

**Covariance.** Two pieces of notation. The conjugate transpose vᴴ transposes v and conjugates every
entry: for v = (1, −i), vᴴ is the row (1, i), so vᴴ v = 1 + (i)(−i) = 2. The expected value E[·]
is the average over many repetitions of a random quantity; for example, a fair die has E[roll] = 3.5. The
spatial covariance R = E[x xᴴ] holds in entry (j, k) the average of x_j conj(x_k), how sensors j and
k vary together. With sources and noise uncorrelated,

```
R = A R_ss Aᴴ + σ² I
```

In practice R is estimated by the sample covariance R̂. R is Hermitian (Rᴴ = R), so by the spectral
theorem its eigenvalues are real, here nonnegative, and its eigenvectors can be chosen orthonormal.

**Delay-and-sum beamforming.** Weighting snapshot x by a candidate steering vector and adding,
a(θ)ᴴ x undoes the phase lags for direction θ, so a source there adds coherently. Its average power
is

```
P(θ) = E[ |a(θ)ᴴ x|² ] = a(θ)ᴴ R a(θ)
```

and the estimate is the set of peaks of P(θ). The peaks have width about 2/M in sin θ, so two
sources closer than that merge.

**MUSIC.** The name stands for MUltiple SIgnal Classification. A R_ss Aᴴ has rank d, so for any
vector v orthogonal to the d columns of A, R v = σ² v. Hence R has M − d eigenvalues equal to σ², and
d larger ones whose eigenvectors span the column space of A, the signal subspace. The remaining
eigenvectors, collected as columns of E_n, span the noise subspace. The symbol ⊥ means "is orthogonal
to": a ⊥ E_n says aᴴ u = 0 for every column u of E_n, as for (1, 1) ⊥ (1, −1) in R². Each true
steering vector lies in the signal subspace, so a(θ_k) ⊥ E_n, and E_nᴴ a(θ), the vector of its inner
products with the noise eigenvectors, vanishes exactly there. The pseudospectrum

```
P_MU(θ) = 1 / ‖E_nᴴ a(θ)‖²
```

where ‖v‖ is the length of a vector, ‖v‖² = vᴴ v. It is infinite at the true angles for the exact R,
and sharply peaked for R̂. It is called a pseudospectrum because its peaks mark directions but its
heights are not powers.

**Worked case: three sensors, one source at 30°.** Take σ_s² = 2 and σ² = 1. With
a(30°) = (1, −i, −1), the scalar equations for one snapshot are

```
x_0 = s + n_0
x_1 = −i s + n_1
x_2 = −s + n_2
```

and in matrix form

```
[ x_0 ]   [ 1  ]       [ n_0 ]
[ x_1 ] = [ −i ] s  +  [ n_1 ]
[ x_2 ]   [ −1 ]       [ n_2 ]
```

The covariance is R = 2 a aᴴ + I, with (a aᴴ)_jk = a_j conj(a_k):

```
         0    1    2
a aᴴ = [ 1    i    −1  ]   0
       [ −i   1    i   ]   1
       [ −1   −i   1   ]   2
```

so that

```
      0    1    2
R = [ 3    2i   −2  ]   0
    [ −2i  3    2i  ]   1
    [ −2   −2i  3   ]   2
```

Since a aᴴ a = 3a, R a = (2 × 3 + 1) a = 7a: the signal eigenvalue is M σ_s² + σ² = 7. Checking
row by row:

```
[ 3    2i   −2  ]   [ 1  ]   [ 3 + 2 + 2     ]   [ 7  ]
[ −2i  3    2i  ] × [ −i ] = [ −2i − 3i − 2i ] = [ −7i ] = 7 × a
[ −2   −2i  3   ]   [ −1 ]   [ −2 − 2 − 3    ]   [ −7 ]
```

Every vector orthogonal to a has eigenvalue σ² = 1, twice. An orthonormal basis of that noise
subspace is

```
u_2 = (1, 0, 1) / √2,     u_3 = (1, 2i, −1) / √6
```

At θ = 30°, u_2ᴴ a = (1 − 1)/√2 = 0 and u_3ᴴ a = (1 + (−2i)(−i) + 1)/√6 = (1 − 2 + 1)/√6 = 0, so
a(30°) ⊥ E_n and P_MU is infinite. At θ = 0°, a(0°) = (1, 1, 1) gives u_2ᴴ a = 2/√2 and
u_3ᴴ a = −2i/√6, so ‖E_nᴴ a‖² = 2 + 2/3 = 8/3 and P_MU(0°) = 3/8. Delay-and-sum gives
P(θ) = 2 |a(θ)ᴴ a(30°)|² + 3, so P(30°) = 2 × 9 + 3 = 21 and P(0°) = 2 × 1 + 3 = 5.

**A two-source case.** With M = 8, sources at 0° and 10°, σ_s² = 1, σ² = 0.1 and one simulated set
of N = 200 snapshots, R̂ has eigenvalues 11.318 and 4.721 followed by six between 0.074 and 0.130.
The two large ones give d = 2. The beamwidth is 2/M = 0.25 in sin θ, about 14.5°, so delay-and-sum
shows a single peak near 5.2° (power 87.27). MUSIC peaks at −0.06° and 9.93°, with pseudospectrum
367.4 and 306.9 against 3.5 at 5° between them.

## Matrix structure

R is small, dense, Hermitian and positive semidefinite. For a uniform linear array and uncorrelated
sources it is also Toeplitz: entry (j, k) depends only on j − k. A steering vector at
sin θ = −2k/M is column k of Fᴴ, where F is the M-point discrete Fourier transform (DFT) matrix, so
delay-and-sum at those angles is a spatial DFT of the snapshot. Spacing wider than half a wavelength
lets two different angles give the same steering vector, and the array cannot tell them apart.

## What is computed

R̂ is formed from the snapshots, a Hermitian eigensolver (numpy.linalg.eigh, LAPACK zheevd) splits it,
and P_MU is evaluated on a fine grid of angles. Equivalently, the singular value decomposition (SVD)
of the M × N snapshot matrix gives the same subspaces without forming R̂.

## Why linear algebra is the right tool

The geometry is the whole argument. Sources live in a d-dimensional subspace of ℂ^M, noise fills all
of ℂ^M equally, and the spectral theorem separates the two as orthogonal eigenspaces. Direction
finding becomes a search along the array manifold for points orthogonal to a subspace. Delay-and-sum
measures a projection onto one steering vector, which is limited by aperture. MUSIC measures distance
from the signal subspace, which is limited only by how well R̂ estimates R.

## Pitfall worth teaching

Coherent sources break MUSIC. Multipath, for example a radar echo arriving directly and again off
the sea, gives two directions carrying the same signal up to a factor, so R_ss is singular and the
signal part of R has rank 1 instead of 2. Only one large eigenvalue appears, the signal subspace
holds a mixture of the two steering vectors, and neither is orthogonal to E_n. Spatial smoothing
averages the covariances of overlapping subarrays, which restores the rank at the cost of aperture.
A second trap is the model order: d must be estimated, usually from the gap between large
eigenvalues and the noise floor, or by the Akaike information criterion (AIC) or
minimum description length (MDL). Choosing d too small drops a source; too large puts a signal eigenvector into E_n.

## Extensions

The minimum-variance distortionless response (MVDR) or Capon beamformer uses weights
w = R⁻¹ a / (aᴴ R⁻¹ a), which keep the gain toward θ at 1 and minimize everything else. ESPRIT
(estimation of signal parameters via rotational invariance techniques) uses the shift between two
overlapping subarrays to get the angles from a small eigenproblem with no grid search. Root-MUSIC
writes ‖E_nᴴ a‖² as a polynomial in z = e^(−iπ sin θ) and reads the angles from its roots. How
accurately any unbiased method can estimate θ is the Cramér–Rao bound, and showing that MUSIC
approaches it as N grows needs estimation theory and random processes (Tier 3). The steering vectors are columns of a DFT-like matrix (the small DFT entry), and fast scanning of a
uniform array uses the fast Fourier transform (FFT), itself a matrix factorization (the FFT entry).
The split of a covariance into a few large eigenvalues and a flat floor is the same move as
principal component analysis (PCA) in the population-genetics entry and latent semantic analysis in
the word-embeddings entry. In 5G (fifth-generation) wireless, multiple-input multiple-output (MIMO)
base stations apply the same beamforming with dozens of antennas, and microphone arrays in smart
speakers use it to pick out a talker.
