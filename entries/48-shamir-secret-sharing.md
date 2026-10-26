---
id: 48
slug: shamir-secret-sharing
status: written
title: 'Shamir secret sharing: a threshold is a theorem about interpolation'
short_title: Shamir secret sharing
field_label: Cryptography, key management, distributed systems security
tier_note: 'everything is polynomial interpolation, a Vandermonde solve, done in the integers modulo a
  prime p. Arithmetic modulo a prime obeys the usual rules of algebra, including division by any nonzero
  number, and nothing more from abstract algebra is needed. The byte-wise version used in practice works
  in GF(2^8), which is Tier 3.'
nav_field: Cryptography & Security
field: Computer Science
subfield: Cryptography
tier: 1
tier_ceiling: 3
prereq_beyond_la: modular arithmetic; field extensions GF(2^m) for byte-wise implementations
scalar_field: GF(p), the integers 0 to p − 1 with arithmetic modulo a prime p (in practice p is a prime
  larger than any possible secret, often 127 or more bits)
vector_space: P_(k−1)(GF(p)), the polynomials of degree at most k − 1 with coefficients in GF(p), a
  k-dimensional space; the n shares are a vector in GF(p)^n, the image of a polynomial under the evaluation
  map
underlying_equations: 'Polynomial evaluation and interpolation over the finite field GF(p)'
core_la_object: Polynomial interpolation over GF(p)
la_concepts: vector spaces over a finite field; evaluation map; Vandermonde matrix; Lagrange basis;
  uniqueness from rank; affine solution sets
primary_method: Lagrange interpolation at x = 0 over GF(p)
matrix_structure: small dense Vandermonde over GF(p)
typical_size: k up to tens; secrets of 128-256 bits
worked_example_size: 3-of-5 split of a secret over GF(13), reconstructed by hand
terminology:
  dealer: whoever chooses the polynomial and hands out the shares
  share: a point (x_i, f(x_i)), one coordinate of the evaluation map's output
  threshold k: the dimension of the polynomial space, deg f + 1
  (k, n) scheme: a polynomial in a k-dimensional space evaluated at n distinct points
  reconstruction: Lagrange interpolation evaluated at x = 0, a fixed linear combination of the shares
  Lagrange coefficients: the weights λ_i, which depend only on which parties are present
  perfect (information-theoretic) secrecy: every candidate secret is consistent with the same number of
    polynomials through any k − 1 shares
  share refresh (proactive sharing): adding a sharing of 0, a polynomial from the subspace with f(0) = 0
  corrupted share: an error in a Reed-Solomon codeword
---

## Start here

Suppose a company's master password must never be in one person's hands, but any three of its five
directors acting together should be able to recover it. Splitting the password into five pieces does not
work: each piece gives part of the password away, and losing one piece loses the password.

The trick uses a fact from school algebra: two points determine a line, three points determine a
parabola, and in general k points determine a polynomial of degree k − 1. Hide the password as the
height of a parabola where it crosses the vertical axis, choose the rest of the parabola at random, and
give each director one point on it. Any three directors can rebuild the parabola and read off the
password. Any two cannot, and this is the surprising part: through two points there is a parabola
crossing the axis at every possible height, all equally likely, so two points reveal nothing at all.

For this to be exact, the arithmetic is done with whole numbers that wrap around at a fixed prime, like
the hours on a clock. That number system still allows division, which interpolation needs, and it has no
rounding and no sizes that leak information.

## The problem

Split a secret s into n shares so that any k of them determine s, while any k − 1 of them give no
information about s whatsoever.

## Variables

| Symbol | Name | What it holds | Shape | Units |
|---|---|---|---|---|
| p | modulus | a prime larger than the secret and than n | integer | — |
| s | secret | the value to be protected, an element of GF(p) | scalar | — |
| k | threshold | number of shares needed to reconstruct | integer | — |
| n | number of shares | number of parties | integer | — |
| a_1, …, a_(k−1) | random coefficients | chosen uniformly at random from GF(p) by the dealer | scalars | — |
| f | sharing polynomial | f(x) = s + a_1 x + … + a_(k−1) x^(k−1), so f(0) = s | element of P_(k−1) | — |
| x_i | evaluation point | the public label of party i; distinct and nonzero | scalar per party | — |
| y_i | share value | y_i = f(x_i), kept secret by party i | scalar per party | — |
| V | Vandermonde matrix | row i is (1, x_i, x_i², …, x_i^(k−1)) | k × k for k parties | — |
| c | coefficient vector | (s, a_1, …, a_(k−1)), the coordinates of f in the basis 1, x, …, x^(k−1) | k × 1 | — |
| λ_i | Lagrange coefficients | weights such that s = Σ λ_i y_i | one per participating party | — |

Every quantity is an element of GF(p), the integers 0, 1, …, p − 1 with addition and multiplication
modulo p, so there are no physical units. Because p is prime, every nonzero element has a reciprocal:
in GF(13), for example, 1/2 = 7, since 2 × 7 = 14 = 1 modulo 13.

## Formulation

**Where the equations come from.** The model is polynomial evaluation
over the finite field GF(p).

**Sharing.** The dealer puts the secret in the constant term and picks the other k − 1 coefficients at
random:

```
f(x) = s + a_1 x + a_2 x² + … + a_(k−1) x^(k−1)
y_i = f(x_i)          for i = 1, …, n
```

The map that sends a polynomial to its values at x_1, …, x_n is linear, from the k-dimensional space
P_(k−1) to GF(p)^n. In coordinates it is the n × k Vandermonde matrix with rows (1, x_i, …, x_i^(k−1)).

**Reconstruction from k shares.** Any k parties hold k equations in the k unknown coefficients:

```
V c = y
```

A square Vandermonde matrix with distinct x_i has determinant Π_(i<j) (x_j − x_i), which is nonzero, so
the system has exactly one solution, and the secret is its first entry. Nobody needs the full solution.
Writing f in the Lagrange basis gives the secret directly as a fixed linear combination of the shares:

```
s = f(0) = Σ λ_i y_i,     λ_i = Π_(j ≠ i) x_j / (x_j − x_i)
```

The weights depend only on which parties are present, not on the secret.

**Secrecy against k − 1 shares.** With only k − 1 equations, V is (k − 1) × k and has a one-dimensional
null space. For every candidate secret s′, adding the equation f(0) = s′ gives a square Vandermonde
system (with the extra point x = 0), which has exactly one solution. So each of the p possible secrets is
consistent with exactly one polynomial, and since the dealer chose the coefficients uniformly, every
secret is equally likely given what the k − 1 parties see.

**Worked case: 3 of 5 over GF(13).** Take s = 7 and f(x) = 7 + 3x + 5x² modulo 13. The five shares are
(1, 2), (2, 7), (3, 9), (4, 8), (5, 4). Parties 1, 2 and 3 compute

```
λ_1 = (2·3)/((2−1)(3−1)) = 3
λ_2 = (1·3)/((1−2)(3−2)) = −3 = 10
λ_3 = (1·2)/((1−3)(2−3)) = 1
s = 3·2 + 10·7 + 1·9 = 85 = 7   (mod 13)
```

Parties 1 and 2 alone, holding (1, 2) and (2, 7), find that s = 0 fits f(x) = 7x + 8x², s = 1 fits
1 + 12x + 2x², s = 2 fits 2 + 4x + 9x², and so on through all thirteen values: one polynomial for each
possible secret.

## Matrix structure

A small dense k × k Vandermonde matrix over GF(p), never formed explicitly in practice: the Lagrange
weights are computed directly, at a cost of O(k²) multiplications and k modular inverses.

## What is computed

Sharing is k − 1 random draws and n polynomial evaluations by Horner's rule. Reconstruction is the
Lagrange combination at x = 0. Each reciprocal modulo p is computed with the extended Euclidean algorithm
or as a^(p−2) by Fermat's little theorem. Real tools, such as the unseal keys of HashiCorp Vault, split
a key byte by byte and do the same arithmetic in GF(2^8), a 256-element field.

## Why linear algebra is the right tool

The security claim is a rank statement. Reconstruction works because k distinct evaluation points give
an invertible Vandermonde matrix, and secrecy holds because k − 1 points leave a one-dimensional space
of polynomials, every point of which corresponds to a different secret. Both halves of the threshold
property are the single fact that the evaluation map from P_(k−1) to k distinct points is invertible.
The same fact also gives the extras for free: adding two sharings gives a sharing of the sum, which is
the starting point for computing on secrets without revealing them.

## Pitfall worth teaching

The arithmetic must be done in a field. Over the ordinary integers a single share already leaks: with
x_1 = 2, the share f(2) = s + 2a_1 + 4a_2 has the same parity as s, so the party holding it knows whether
the secret is even or odd. The secrecy argument needs every value of the free coefficient to be equally
likely, and there is no uniform choice of a whole number. Modulo a composite number such as 256 the
argument breaks differently: x_j − x_i can share a factor with the modulus, the reciprocal that the
Lagrange formula needs does not exist, and the Vandermonde determinant Π (x_j − x_i) can be 0 even
though the x_i are distinct. A byte-wise implementation that reduces "modulo 256" instead of working in
the field GF(2^8) is broken in exactly this way. Two further rules are easy to forget: x = 0 must never
be handed out as a share, because f(0) is the secret, and the coefficients a_i must be genuinely random.

## Extensions

The shares of one secret form a codeword of a Reed–Solomon code, so a corrupted or dishonest share is a
codeword error, and the Berlekamp–Welch decoder (one more linear solve) identifies and corrects it
(see the error-correcting codes entry). Verifiable secret sharing lets parties check their shares against
public commitments, which needs exponentiation in a cyclic group (Tier 3). Threshold signatures and
secure multiparty computation build on the linearity noted above. The same interpolation over the reals
is the polynomial interpolation entry, with conditioning problems that a finite field does not have, and
finite-difference stencils solve a similar small Vandermonde system. RAID-6 storage uses the same
Reed–Solomon arithmetic to survive two failed disks (compare the RAID-5 parity entry).
