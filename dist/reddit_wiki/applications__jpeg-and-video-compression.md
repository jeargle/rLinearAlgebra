# JPEG compression: change to a cosine basis, then keep only a few coordinates

### Start here

A photograph from a phone has millions of pixels, each with three colour values, yet the [JPEG](https://en.wikipedia.org/wiki/JPEG) file is
usually a tenth of the raw size or less, and the difference is hard to see. The saving comes from a
simple observation: neighbouring pixels in a photograph are usually close in value. A patch of sky or
skin changes slowly. Listing every pixel value separately wastes space on information that is nearly
the same from one pixel to the next.

JPEG cuts the image into 8 × 8 blocks and rewrites each block in a different basis. Instead of 64 pixel
values, it records how much of each of 64 cosine patterns the block contains, from flat to rapidly
striped. For a smooth block, almost everything is in the first few patterns, and the amounts of the
rest are close to zero. Rounding those small amounts to exactly zero is where the compression happens.

The rewriting is a [change of basis](https://en.wikipedia.org/wiki/Change_of_basis) with an [orthogonal matrix](https://en.wikipedia.org/wiki/Orthogonal_matrix), so it loses nothing and is undone by the
transpose. Only the rounding loses information, and the orthogonality keeps the loss under control.
Video compression uses the same idea on the differences between one frame and the next.

**Field:** Image and video compression, digital photography, streaming video, multimedia standards  
**Tier:** 1 — the [discrete cosine transform](https://en.wikipedia.org/wiki/Discrete_cosine_transform) is an orthogonal change of basis for each block of pixels, and compression is rounding the new coordinates, most of them to zero. Why cosines are close to the best possible basis is an [eigenvector](https://en.wikipedia.org/wiki/Eigenvalues_and_eigenvectors) statement, which is Tier 2.  
**Scalar field:** R  
**Vectors:** R^64 for an 8 × 8 block of pixel values (R^4 for one row of four pixels in the toy). The discrete cosine transform is an orthogonal change of basis in that space, and compression stores the coordinates in the new basis coarsely  
**Underlying equations:** Change of basis: X = C x for a row of samples and F = C B Cᵀ for a block, where C is the orthogonal DCT matrix; [quantization](https://en.wikipedia.org/wiki/Quantization_%28image_processing%29) then rounds each coordinate to a multiple of a step size

### The problem

A grey-level image is a grid of numbers from 0 (black) to 255 (white). JPEG splits it into **blocks**
of 8 × 8 pixels and treats each block as a vector in ℝ⁶⁴. A colour image is first converted to a
brightness channel and two colour-difference channels (**[YCbCr](https://en.wikipedia.org/wiki/YCbCr)**), and the colour channels are usually
stored at half resolution in each direction, because the eye is less sensitive to fine colour detail
than to fine brightness detail. Each channel is then coded block by block.

The everyday contrast is between **lossless** and **[lossy](https://en.wikipedia.org/wiki/Lossy_compression)** compression. A ZIP file must give back
every bit; a JPEG only has to look the same. JPEG may change pixel values, as long as the changes are
small where the eye would notice.

Find a basis in which typical blocks have only a few large coordinates, round the coordinates so that
most become zero, and do it so that the error in the pixels stays small and predictable.

### Variables

| Symbol | Name | What it holds | Shape | Units |
|---|---|---|---|---|
| N | transform size | 8 in JPEG, 4 in the toy | integer | — |
| n | sample index | position of a pixel in a row, 0 to N − 1 | integer | — |
| k | frequency index | which cosine pattern, 0 to N − 1 | integer | — |
| x | row of pixels | x_0, …, x_(N−1) | N × 1 | grey levels |
| w_k | cosine basis vector | the k-th sampled cosine, scaled to length 1 | N × 1 | dimensionless |
| C | DCT matrix | row k is w_k | N × N, orthogonal | dimensionless |
| X | coefficients | X = C x, the coordinates of x in the cosine basis | N × 1 | grey levels |
| B | pixel block | the 8 × 8 block, after subtracting 128 | 8 × 8 | grey levels |
| F | block coefficients | F = C B Cᵀ | 8 × 8 | grey levels |
| Δ_k | quantization step | step size for coefficient k | number | grey levels |
| q_k | quantized coefficient | round(X_k / Δ_k), the whole number stored in the file | integer | — |

### Formulation

**Where the equations come from.** There is no physical model. The method is a change of basis
followed by rounding, chosen because photographs are smooth almost everywhere.

**The familiar formula.** The JPEG standard defines the forward transform of a block f(i, j), with
pixel row and column i, j and frequencies u, v all running from 0 to 7, as

```
F(u, v)  =  ¼ a(u) a(v)  Σ_i Σ_j  f(i, j) cos((2i + 1)uπ/16) cos((2j + 1)vπ/16)
```

where a(0) = 1/√2 and a(u) = 1 otherwise. (The standard writes x, y for the pixel position and C(u) for
a(u); here x is a row of pixels and C is the matrix.) The rest of this section shows that this formula
is a matrix product on each side of the block.

**One coefficient first.** For a row of N pixels, the k-th basis vector samples a cosine with k half
periods across the row:

```
w_k(n)  =  s_k cos( π (2n + 1) k / (2N) ),       s_0 = √(1/N),   s_k = √(2/N) for k ≥ 1
```

The scale factors make every w_k a unit vector, and the vectors are mutually orthogonal. The coordinate
of x along w_k is the dot product X_k = w_k · x. For N = 4,

```
w_0 = ( 0.5,     0.5,     0.5,     0.5    )
w_1 = ( 0.6533,  0.2706, −0.2706, −0.6533 )
w_2 = ( 0.5,    −0.5,    −0.5,     0.5    )
w_3 = ( 0.2706, −0.6533,  0.6533, −0.2706 )
```

Take the smooth row x = (100, 110, 120, 130). Then X_0 = w_0 · x = 230, twice the average, and

```
X_1  =  0.6533·100 + 0.2706·110 − 0.2706·120 − 0.6533·130  =  −22.30
```

which measures the slope: w_1 runs from high to low, so a rising row has a negative X_1.

**Stacking the coefficients.** With the w_k as rows, X = C x:

```
[  0.5      0.5      0.5      0.5    ] [ 100 ]   [ 230    ]
[  0.6533   0.2706  −0.2706  −0.6533 ] [ 110 ] = [ −22.30 ]
[  0.5     −0.5     −0.5      0.5    ] [ 120 ]   [   0    ]
[  0.2706  −0.6533   0.6533  −0.2706 ] [ 130 ]   [ −1.59  ]
```

C is orthogonal, so C⁻¹ = Cᵀ and x = Cᵀ X. It also preserves length: ‖X‖² = ‖x‖² = 53,400. Of that energy,
X_0 carries 99.06% and X_1 carries 0.93%, leaving under 0.01% for the last two. That is **energy
compaction**.

**Quantization.** Divide each coefficient by a step Δ_k and round: q_k = round(X_k / Δ_k). With every
step equal to 10, the toy row is stored as (23, −2, 0, 0) and decodes to
Cᵀ (230, −20, 0, 0) = (101.9, 109.6, 120.4, 128.1). Two whole numbers replace four pixel values, and no
pixel is off by more than 2. Because C is orthogonal, the [rounding error](https://en.wikipedia.org/wiki/Round-off_error) has the same length in pixels
as in coefficients, so an encoder that controls one controls the other.

**Two dimensions.** A block is transformed along its rows and then along its columns, which is one
matrix product on each side:

```
F  =  C B Cᵀ,        B  =  Cᵀ F C
```

Entry F(k, l) is the coordinate of B along the **basis image** w_k w_lᵀ, the outer product of two
cosine vectors. Multiplied out, this is the formula from the standard.

**Worked case: one 8 × 8 block.** Take a block that brightens smoothly downwards and to the right, with
a soft vertical edge in the middle (pixel values 100 + 5i + 3j + 40/(1 + e^(−1.5(j − 4.5))) in row i and
column j, rounded), subtract 128, and transform. Three of the 64 coefficients carry 97.7% of the energy.
Quantizing all 64 with a step of 16 leaves 6 of them nonzero. The decoded block has a [root-mean-square](https://en.wikipedia.org/wiki/Root_mean_square)
error of 1.8 grey levels and no pixel off by more than 4.

### Matrix structure

C is a dense orthogonal matrix, and like the DFT it has fast factorizations, so an 8-point transform
takes far fewer than 64 multiplications. Video codecs use integer approximations. The 4 × 4 core
transform of [H.264](https://en.wikipedia.org/wiki/Advanced_Video_Coding) has rows (1, 1, 1, 1), (2, 1, −1, −2), (1, −1, −1, 1) and (1, −2, 2, −1). These have
the sign patterns of the rows of the 4-point C above, with the ratio 2 between large and small entries
in place of 0.6533/0.2706 ≈ 2.414. The rows are orthogonal but not of equal length, and the codec folds
the different lengths into its quantization steps, so the transform runs in exact integer arithmetic.

### What is computed

A JPEG encoder converts RGB to YCbCr, subsamples the colour channels, cuts each channel into blocks,
subtracts 128, applies the 8 × 8 DCT, and divides by a **quantization table** of 64 step sizes. The
steps are larger for high frequencies, where the eye is less sensitive, and the quality setting scales
the whole table. The quantized coefficients are listed in zigzag order from low to high frequency, so
the zeros come in long runs, and are [entropy coded](https://en.wikipedia.org/wiki/Entropy_coding). The decoder runs the steps backwards. Video codecs
such as H.264 and [HEVC](https://en.wikipedia.org/wiki/High_Efficiency_Video_Coding) predict each block from earlier frames ([motion compensation](https://en.wikipedia.org/wiki/Motion_compensation)) and transform only
the prediction error. The libjpeg-turbo library is the common implementation of JPEG.

### Why linear algebra is the right tool

Compression is a change of basis into one where typical data have few large coordinates. Orthogonality
makes the change free to undo (the inverse is the transpose), keeps the energy unchanged, and makes the
error from rounding the coordinates equal to the error in the pixels. The two-dimensional transform is
a matrix product on both sides. The choice of cosines is itself a basis argument. The DFT of the
small-DFT entry treats a block as one period of a repeating signal, so the jump from the last pixel
back to the first acts like an edge. For the toy row, the DFT spreads the non-constant energy over three
coefficients in the proportions 40%, 40% and 20%, while the DCT puts 99.5% of it in X_1. The cosine
basis corresponds to reflecting the block in a mirror instead, which has no jump, so its coefficients
fall off faster, for the same reason as in the Gibbs pitfall of the [Fourier series](https://en.wikipedia.org/wiki/Fourier_series) entry.

### Pitfall worth teaching

Every block is coded on its own, so errors do not match across block boundaries. Take two neighbouring
4-pixel blocks from a smooth ramp, (100, 110, 120, 130) and (140, 150, 160, 170). Quantize them as JPEG
tables do, finely for the constant coefficient (step 10) and coarsely for the rest (step 50). The
coefficients X_1 = −22.30 and X_3 = −1.59 of both blocks round to zero, and the blocks decode as flat
rows, (115, 115, 115, 115) and (155, 155, 155, 155). The ramp becomes a staircase, with a jump of 40 at the
block boundary where the original stepped by 10.

These **[blocking artifacts](https://en.wikipedia.org/wiki/Compression_artifact)** are the 8 × 8 grid visible in heavily compressed images, and the same
rounding produces ringing next to sharp edges, as in the [Gibbs phenomenon](https://en.wikipedia.org/wiki/Gibbs_phenomenon). Video codecs run a
[deblocking filter](https://en.wikipedia.org/wiki/Deblocking_filter) across block boundaries, and H.264 includes one inside the prediction loop. Newer
image formats use transforms that overlap from block to block, or [wavelets](https://en.wikipedia.org/wiki/Wavelet), to avoid hard boundaries.

### Extensions

For data with known correlations, the best possible basis for compaction comes from the eigenvectors of
the [covariance](https://en.wikipedia.org/wiki/Covariance_matrix) matrix (the [Karhunen–Loève](https://en.wikipedia.org/wiki/Kosambi%E2%80%93Karhunen%E2%80%93Lo%C3%A8ve_theorem) transform, or [principal component](https://en.wikipedia.org/wiki/Principal_component_analysis) analysis, Tier 2). The DCT
was introduced in 1974 as a fixed approximation to it for highly correlated signals. The DCT basis
vectors are also the eigenvectors of the second-difference matrix of the [finite-difference](https://en.wikipedia.org/wiki/Finite_difference) entry with
mirror-image boundary conditions (Tier 2). [JPEG 2000](https://en.wikipedia.org/wiki/JPEG_2000) replaces the DCT with wavelets. [MP3](https://en.wikipedia.org/wiki/MP3) and AAC audio
use the [modified DCT](https://en.wikipedia.org/wiki/Modified_discrete_cosine_transform) on overlapping blocks. The colour conversion to YCbCr is the colour-spaces entry,
the continuous version of the cosine basis is the Fourier series entry, and choosing a basis to fit
data is the basis-fitting entry.

### Terminology

How this field's vocabulary reads as linear algebra.

| Domain term | In linear algebra |
|---|---|
| block | an 8 × 8 tile of pixels, the unit JPEG transforms and codes separately |
| discrete cosine transform (DCT) | the change of basis from pixel values to amounts of sampled cosine waves |
| basis image | one of the 64 cosine patterns an 8 × 8 block is built from |
| DC and AC coefficients | the coefficient of the constant pattern, and those of the oscillating ones |
| energy compaction | concentrating most of a signal's energy in a few coordinates |
| quantization | dividing each coefficient by a step size and rounding to a whole number |
| quantization table | the 64 step sizes, larger for higher frequencies |
| zigzag order and entropy coding | listing coefficients from low to high frequency so the zeros come in long runs, then coding the result compactly |
| YCbCr and chroma subsampling | brightness and two colour-difference channels, with the colour stored at lower resolution |
| blocking artifact | visible steps at block boundaries at high compression |
| motion compensation | predicting a video block from the previous frame and coding only the difference |

---

[Back to the index](/r/LinearAlgebra/wiki/applications)
