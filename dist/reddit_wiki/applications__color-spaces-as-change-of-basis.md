# Colour spaces: three numbers per colour, and every conversion is a change of basis

### Start here

A screen makes every colour it shows from three small lights: a red, a green and a blue. That this
works at all is a fact about the eye, not about light. Light carries a whole [spectrum](https://en.wikipedia.org/wiki/Spectral_power_distribution), a different
amount of power at every wavelength. The eye has only three kinds of colour receptor, [the cones](https://en.wikipedia.org/wiki/Cone_cell), and
each reports a single number. Two lights with completely different spectra that produce the same
three numbers look identical.

So a colour, as people see it, is three numbers, and colours behave like vectors in a
three-dimensional space: mixing two lights adds their vectors, and dimming a light scales it. Every
device picks its own three lights, so the same colour gets different coordinates on different devices.
Converting between them is a [change of basis](https://en.wikipedia.org/wiki/Change_of_basis), a 3 × 3 matrix.

The same matrices are behind every colour-managed web page, photo editor and printer. They also
explain the white-balance setting on a camera, and why a widely used shortcut for blending colours
gives the wrong answer.

**Field:** Colour science, displays and photography, image processing, colour management for web and print  
**Tier:** 1 — the eye reduces a spectrum to three numbers by a linear map, so colours form a three-dimensional vector space, and moving between RGB, XYZ and cone coordinates is a 3 × 3 change of basis. Analysing spectra or camera responses with the [SVD](https://en.wikipedia.org/wiki/Singular_value_decomposition) is Tier 2.  
**Scalar field:** R  
**Vectors:** R^3 of [tristimulus values](https://en.wikipedia.org/wiki/CIE_1931_color_space). Light is a spectrum, a function of wavelength in an infinite-dimensional space; colour matching maps it linearly onto R^3, and every RGB, XYZ or cone-response space is a choice of basis for that R^3  
**Underlying equations:** Change of basis: (X, Y, Z) = M (R, G, B) for linear RGB values, where the columns of M are the XYZ values of the display's three [primaries](https://en.wikipedia.org/wiki/Primary_color) at full strength; [Grassmann's laws](https://en.wikipedia.org/wiki/Grassmann's_laws_%28color_science%29) of colour matching make the map linear

### The problem

The everyday contrast is between the physics and the perception. Physically, a light is its
**spectrum**: a function of wavelength across the visible range, so infinitely many numbers.
Perceptually it is three numbers. The international standard set of three, defined by the CIE in 1931
from colour-matching experiments, is the **tristimulus values** X, Y and Z, where Y is the
**[luminance](https://en.wikipedia.org/wiki/Luminance)**, the perceived brightness. Dividing out the brightness gives the **[chromaticity](https://en.wikipedia.org/wiki/Chromaticity)**
x = X/(X + Y + Z) and y = Y/(X + Y + Z), which says only what colour a light is.

A display is described by its three **primaries**, given as chromaticities, and its **[white point](https://en.wikipedia.org/wiki/White_point)**,
the colour it shows when all three are fully on. For the [sRGB](https://en.wikipedia.org/wiki/SRGB) standard used by the web, the red
primary has chromaticity (0.64, 0.33), green (0.30, 0.60), blue (0.15, 0.06), and the white point is
the daylight white [D65](https://en.wikipedia.org/wiki/Standard_illuminant#Illuminant_series_D) at (0.3127, 0.3290). The [Display P3](https://en.wikipedia.org/wiki/DCI-P3) standard of many recent phones and laptops
keeps the same blue and white but uses a deeper red (0.680, 0.320) and green (0.265, 0.690).

Given those numbers, find the matrix that turns a display's linear RGB values into XYZ, convert colours
from one display to another, say which colours a display cannot show, and adjust colours for a change
of white.

### Variables

| Symbol | Name | What it holds | Shape | Units |
|---|---|---|---|---|
| v | tristimulus vector | (X, Y, Z) | 3 × 1 | relative, with Y = 1 for white |
| (x, y) | chromaticity | the colour with brightness divided out | 2 numbers | dimensionless |
| (R, G, B) | linear RGB | how strongly each primary is driven | 3 × 1, each from 0 to 1 | dimensionless |
| p_R, p_G, p_B | primary directions | XYZ of each primary per unit luminance, (x/y, 1, (1 − x − y)/y) | 3 × 1 each | relative |
| K | direction matrix | columns p_R, p_G, p_B | 3 × 3 | relative |
| s | primary luminances | (s_R, s_G, s_B), the luminance of each primary at full strength | 3 × 1 | relative |
| w | white point | XYZ of R = G = B = 1 | 3 × 1 | relative |
| M | RGB-to-XYZ matrix | v = M (R, G, B) for sRGB | 3 × 3 | relative |
| M_3 | RGB-to-XYZ matrix | the same for Display P3 | 3 × 3 | relative |
| C | display-to-display matrix | sRGB coordinates to Display P3 coordinates | 3 × 3 | dimensionless |
| B | Bradford matrix | XYZ to cone-like responses | 3 × 3 | dimensionless |
| D | adaptation scaling | diagonal ratios of the two whites' cone-like responses | 3 × 3 diagonal | dimensionless |
| A | adaptation matrix | XYZ under one white to XYZ under another | 3 × 3 | dimensionless |
| ℓ, e | linear and encoded channel values | one of R, G, B as light intensity, and as stored in a file | numbers from 0 to 1 | dimensionless |

The Bradford matrix is named B by convention. It is unrelated to the blue value B, which always appears
inside (R, G, B).

### Formulation

**Where the equations come from.** Colour matching obeys Grassmann's laws: if two lights match two
others, their sums match, and scaling both members of a match keeps the match. So the map from
spectra to tristimulus values is linear. Each of X, Y and Z is the integral of the spectrum against a
fixed weighting curve, a [linear functional](https://en.wikipedia.org/wiki/Linear_form) on spectra. The map goes from an infinite-dimensional space
of spectra onto ℝ³, so it has an enormous [null space](https://en.wikipedia.org/wiki/Kernel_%28linear_algebra%29). Two spectra whose difference lies in that null
space are **[metamers](https://en.wikipedia.org/wiki/Metamerism_%28color%29)**: different light, the same colour.

**The familiar formula.** Image-processing courses teach that the brightness of a linear sRGB colour is

```
Y  =  0.2126 R  +  0.7152 G  +  0.0722 B
```

with green counting ten times as much as blue. These weights are not chosen by hand. They are the
middle row of the matrix built below.

**One primary first.** The red primary has chromaticity (x, y) = (0.64, 0.33). Its XYZ direction with
luminance 1 is

```
p_R  =  (x/y,  1,  (1 − x − y)/y)  =  (0.64/0.33,  1,  0.03/0.33)  =  (1.9394,  1,  0.0909)
```

At full strength red gives s_R p_R, where its luminance s_R is not yet known. Driving it at strength R
gives R s_R p_R. In the same way the green and blue directions are p_G = (0.5, 1, 0.1667) and
p_B = (2.5, 1, 13.1667).

**Stacking the primaries.** Light from the three primaries adds, so

```
v  =  R s_R p_R  +  G s_G p_G  +  B s_B p_B  =  M (R, G, B),      M  =  K diag(s_R, s_G, s_B)
```

The columns of M are the primaries at full strength, which is the change-of-basis matrix from RGB
coordinates to XYZ coordinates. The luminances s come from the white point. Full drive (1, 1, 1) must
give white, w = (0.3127/0.3290, 1, 0.3583/0.3290) = (0.9505, 1, 1.0891), so K s = w:

```
[ 1.9394   0.5      2.5     ] [ s_R ]   [ 0.9505 ]
[ 1        1        1       ] [ s_G ] = [ 1      ]
[ 0.0909   0.1667  13.1667  ] [ s_B ]   [ 1.0891 ]
```

Its solution is s = (0.2126, 0.7152, 0.0722), the luminance weights of the familiar formula, and the
sRGB matrix is

```
    [ 0.4124   0.3576   0.1805 ]
M = [ 0.2126   0.7152   0.0722 ]
    [ 0.0193   0.1192   0.9505 ]
```

the standard sRGB-to-XYZ matrix; the sRGB specification publishes its inverse, for converting XYZ
to sRGB.

**From one display to another.** Build M_3 the same way for Display P3. A colour with sRGB
coordinates (R, G, B) has XYZ value M (R, G, B) and Display P3 coordinates M_3⁻¹ M (R, G, B), so the
conversion is one matrix:

```
                    [ 0.8225   0.1775   0      ]
C  =  M_3⁻¹ M  =    [ 0.0332   0.9668   0      ]
                    [ 0.0171   0.0724   0.9105 ]
```

Its last column says that sRGB blue is exactly Display P3 blue at 91% strength, because the two
standards use the same blue chromaticity.

**[Gamut](https://en.wikipedia.org/wiki/Gamut).** The colours a display can make are the combinations with every coordinate between 0 and 1.
Their directions form a **[convex cone](https://en.wikipedia.org/wiki/Convex_cone)**: the nonnegative combinations of the three primaries. Every
entry of C is nonnegative, so every sRGB colour has nonnegative Display P3 coordinates, and the sRGB
gamut lies inside the Display P3 gamut. The reverse fails. Pure Display P3 red, (1, 0, 0), has sRGB
coordinates C⁻¹ (1, 0, 0) = (1.2249, −0.0421, −0.0196). The negative entries mean that sRGB would have
to subtract green and blue light to make it, so no sRGB screen can show that red.

**Adapting to a different white.** A white sheet of paper looks white under daylight and under a warm
lamp, because the eye rescales each cone's response to the light it is adapted to. That is von Kries's
hypothesis, and it is diagonal in a basis of cone responses. The Bradford transform, the standard
choice in colour management, uses the cone-like basis given by the matrix

```
    [  0.8951   0.2664  −0.1614 ]
B = [ −0.7502   1.7135   0.0367 ]
    [  0.0389  −0.0685   1.0296 ]
```

To move from D65 to the print standard D50, whose white is about (0.9643, 1, 0.8251), compute both
whites' responses B w, and let D be the diagonal matrix of their ratios, here diag(1.0584, 0.9807,
0.7511). The adaptation is: change to the cone-like basis, scale, change back.

```
                     [  1.0479   0.0229  −0.0502 ]
A  =  B⁻¹ D B  =     [  0.0296   0.9904  −0.0171 ]
                     [ −0.0092   0.0151   0.7519 ]
```

A sends the D65 white exactly to the D50 white. It is a dense matrix in XYZ, but it is the same map as
the diagonal D, written in a different basis.

### Matrix structure

All the matrices are 3 × 3 and dense. Because the conversions are linear, a whole chain, such as
camera RGB to XYZ, adaptation, then XYZ to display RGB, multiplies out to a single 3 × 3 matrix
applied to each pixel. The [condition number](https://en.wikipedia.org/wiki/Condition_number) of M is about 4.3. It grows when the primaries are close
together in chromaticity, and then small errors in RGB become large errors in XYZ. The negative
entries of inverse matrices are the algebraic sign of gamut limits.

### What is computed

Display [ICC profiles](https://en.wikipedia.org/wiki/ICC_profile) are often stored as exactly these parts: a 3 × 3 matrix and three tone curves,
applied by colour-management engines such as Little CMS. [CSS](https://en.wikipedia.org/wiki/CSS) Color Level 4 lets web pages write
color(display-p3 1 0 0) and specifies the conversion matrices in its sample code. Raw photo formats
such as [DNG](https://en.wikipedia.org/wiki/Digital_Negative) store colour matrices that relate the camera's own RGB to XYZ. In Python, the
colour-science package implements these spaces and [chromatic adaptation](https://en.wikipedia.org/wiki/Chromatic_adaptation) transforms, including
Bradford.

### Why linear algebra is the right tool

Grassmann's laws make colour linear, and three kinds of cone make it three-dimensional. Any three
independent primaries are then a basis, an RGB value is a coordinate vector, and converting between
devices is a change of basis. Metamerism is a null space. A gamut is a convex cone cut off by the unit
cube. White balance is a scaling that is diagonal in one basis and looks complicated in another. Each
fact that colour science states in its own vocabulary is a standard fact about ℝ³.

### Pitfall worth teaching

The matrices act on linear light, but image files store encoded values. sRGB files store each channel
after a [transfer function](https://en.wikipedia.org/wiki/Gamma_correction): e = 12.92 ℓ for ℓ up to 0.0031308, and e = 1.055 ℓ^(1/2.4) − 0.055 above
it, where ℓ is the linear value and e the stored one. The encoding spends more of the available numbers on
dark tones, where the eye is more sensitive. The colour matrices must be applied after decoding, and
so must any averaging.

Averaging encoded values is a common mistake. Blend a black pixel and a white pixel half and half, as
resizing or blurring an image does. Averaging the stored values gives 0.5, which decodes to a linear
intensity of only 0.214, so the result carries about 21% of white's light instead of 50%. The correct
average is linear 0.5, which is stored as 0.735. Programs that blend stored values make fine
light-and-dark detail darker when an image is shrunk, and colour gradients between saturated colours
dip through muddy, darker tones.

### Extensions

Perceptual spaces such as [CIELAB](https://en.wikipedia.org/wiki/CIELAB_color_space) apply cube roots to XYZ, so that distances in them roughly match how
different colours look. They are nonlinear, and the matrices above are only their first step. Camera
colour matrices are fitted by [least squares](https://en.wikipedia.org/wiki/Least_squares) to photographs of colour charts, as in the regression and
basis-fitting entries. The reflectance spectra of natural surfaces are well approximated by a few basis
functions found by [principal component](https://en.wikipedia.org/wiki/Principal_component_analysis) analysis (Tier 2), the same idea as the [empirical orthogonal](https://en.wikipedia.org/wiki/Empirical_orthogonal_functions)
functions entry. JPEG converts RGB to [YCbCr](https://en.wikipedia.org/wiki/YCbCr), another 3 × 3 change of basis that separates brightness
from colour, before its cosine transform (the JPEG entry). People with two types of cone see a
two-dimensional colour space, and [colour-blindness](https://en.wikipedia.org/wiki/Color_blindness) simulators apply a rank-2 matrix that projects onto
it. The barycentric-coordinates entry blends colours with the same kind of weights, and for the reason
in the pitfall above, the blend is physically correct only in linear RGB.

### Terminology

How this field's vocabulary reads as linear algebra.

| Domain term | In linear algebra |
|---|---|
| spectrum (spectral power distribution) | how much power a light carries at each wavelength |
| cones | the three kinds of colour receptor in the eye, most sensitive to long, medium and short wavelengths (L, M, S) |
| tristimulus values | three numbers that determine a colour; CIE XYZ is the standard set |
| luminance Y | the brightness coordinate of XYZ |
| chromaticity (x, y) | x = X/(X + Y + Z) and y = Y/(X + Y + Z), the colour with its brightness divided out |
| primaries | the three lights a display mixes; each RGB space has its own |
| white point | the colour of R = G = B = 1; D65 (daylight, about 6500 K) for sRGB, D50 for print |
| linear and encoded RGB | light intensities, versus the values stored in files after the transfer function (often loosely called gamma) |
| gamut | the set of colours a device can produce |
| metamers | different spectra that look the same colour |
| chromatic adaptation | the eye's adjustment to the colour of the illumination, and its modelling by a matrix |
| Bradford transform | a standard chromatic adaptation matrix built on a cone-like basis |

---

[Back to the index](/r/LinearAlgebra/wiki/applications)
