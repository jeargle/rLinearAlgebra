# Error-correcting codes: linear algebra over a finite field

### Start here

You want to send a string of bits over a connection that occasionally flips one. Repeating everything
three times would work, but it triples what you send.

Here is a better idea. Alongside your data bits, send some extra bits, each one computed as the parity
(the even-or-odd count) of a chosen subset of the data bits. The receiver recomputes those parities from
what it received. If everything matches, no error. If some of them disagree, the exact *pattern* of
disagreement identifies which bit flipped — different bit positions participate in different subsets, so
each one produces its own distinctive signature of failures.

The design problem is choosing the subsets so that every possible single error produces a unique
signature. That is a question about independence: no two error patterns may look alike.

One thing to adjust up front. The arithmetic here is not ordinary addition — it is parity, where
1 + 1 = 0. Everything about subspaces and independence still works, but nothing about lengths or angles
does.

**Field:** Communications, information theory, storage systems  
**Tier:** 1 — rank and [null space](https://en.wikipedia.org/wiki/Kernel_%28linear_algebra%29) over [GF(2)](https://en.wikipedia.org/wiki/GF%282%29), the smallest [finite field](https://en.wikipedia.org/wiki/Finite_field): just the numbers 0 and 1, added and multiplied modulo 2, so 1 + 1 = 0. Nothing from abstract algebra is needed beyond that. [Reed–Solomon](https://en.wikipedia.org/wiki/Reed%E2%80%93Solomon_error_correction) codes use the larger fields GF(2^m), which are Tier 3.  
**Scalar field:** GF(2), the numbers 0 and 1 with arithmetic modulo 2 (addition is XOR, multiplication is AND); Reed–Solomon codes use GF(2^m)  
**Vectors:** GF(2)^n; the code is a k-dimensional subspace of it. There is no Euclidean length here - [Hamming weight](https://en.wikipedia.org/wiki/Hamming_distance) is a metric, not a norm from an inner product  
**Underlying equations:** None: algebraic constraints over GF(2)

**[Run this example](https://jeargle.github.io/rLinearAlgebra/notebooks/07-linear-error-correcting-codes.html)** — an interactive notebook that runs in your browser, with nothing to install.

### The problem

Send bits over a channel that flips some of them. Detect and correct the errors without retransmission.

### Variables

| Symbol | Name | What it holds | Shape | Units |
|---|---|---|---|---|
| k | message length | information bits per block | integer | — |
| n | block length | bits actually transmitted per block | integer | — |
| m | message | the k data bits to send | 1 × k row vector over GF(2) | bits |
| G | generator matrix | its rows are a basis of the code | k × n | bits |
| c | codeword | the n bits transmitted, c = m G | 1 × n | bits |
| H | parity-check matrix | each row is one parity check; its rows span the code's orthogonal complement | (n − k) × n | bits |
| e | error pattern | 1 in each position the channel flipped | 1 × n | bits |
| y | received word | y = c + e | 1 × n | bits |
| s | syndrome | which parity checks fail | (n − k) × 1 | bits |
| d | minimum distance | fewest positions in which two distinct codewords differ | integer | — |
| t | correctable errors | t = ⌊(d − 1)/2⌋ | integer | — |

There are no physical units: every entry is a bit, and all arithmetic is modulo 2, so 1 + 1 = 0 and subtraction is the same as addition. Coding theory conventionally writes messages and codewords as row vectors; that convention is used throughout this entry.

### Formulation

**Where the equations come from.** There is no differential equation; the model is a set of linear constraints over the two-element field GF(2).

**Encoding.**

```
c = m G
```

This models the transmitted block as a combination of the rows of G, with the message bits choosing which rows to add. The dimensions are 1 × k times k × n, giving 1 × n. A common choice is systematic form, G = [I_k  B] with B a k × (n − k) matrix, so the first k bits of c are the message itself and the rest are check bits.

**Parity checks.** With H = [Bᵀ  I_{n−k}], every codeword satisfies

```
H cᵀ = 0
```

because G Hᵀ = B + B = 0 in GF(2). Each row of H is one parity check: the bits it selects must XOR to zero. The code is exactly the null space of H.

**Receiving and decoding.** If the channel flips the bits marked by e, the receiver gets y = c + e and computes

```
s = H yᵀ = H cᵀ + H eᵀ = H eᵀ
```

The [syndrome](https://en.wikipedia.org/wiki/Decoding_methods#Syndrome_decoding) depends only on the error pattern, not on the message. Decoding means finding the error pattern with the fewest 1s that satisfies H eᵀ = s, and then recovering c = y + e.

**Worked case: [Hamming(7,4)](https://en.wikipedia.org/wiki/Hamming%287,4%29).** Here k = 4, n = 7, d = 3, and t = 1. The seven columns of H are the seven nonzero 3-bit vectors. A single flipped bit in position i produces a syndrome equal to column i of H, so the syndrome directly names the position of the error.

### Matrix structure

Entries in GF(2); [LDPC](https://en.wikipedia.org/wiki/Low-density_parity-check_code) codes use very [sparse](https://en.wikipedia.org/wiki/Sparse_matrix) `H`; Reed–Solomon works over GF(2^m) with a [Vandermonde](https://en.wikipedia.org/wiki/Vandermonde_matrix)-structured generator.

### What is computed

Syndrome decoding: look up or infer the minimum-weight `e` consistent with `s`. For LDPC codes, [belief propagation](https://en.wikipedia.org/wiki/Belief_propagation) on the bipartite graph of `H`. For Reed–Solomon, polynomial interpolation, which is a structured linear solve.

### Why linear algebra is the right tool

Distance properties — the whole point of a code — become rank conditions. A code corrects `t` errors if and only if every `2t` columns of `H` are linearly independent. Searching an exponentially large space of codewords collapses to a statement about column ranks.

### Pitfall worth teaching

This is where the abstraction of "field" earns its keep. Everything from linear algebra ([rank](https://en.wikipedia.org/wiki/Rank_%28linear_algebra%29), null space, dimension, bases) carries over unchanged; everything from geometry (angles, lengths, [positive-definiteness](https://en.wikipedia.org/wiki/Definite_matrix), [least squares](https://en.wikipedia.org/wiki/Least_squares)) does not. A good exercise in what the axioms actually buy.

### Extensions

Reed–Solomon in [QR codes](https://en.wikipedia.org/wiki/QR_code), CDs, and [RAID](https://en.wikipedia.org/wiki/Standard_RAID_levels)-6; LDPC in 5G and Wi-Fi 6; [polar codes](https://en.wikipedia.org/wiki/Polar_code_%28coding_theory%29) in 5G control channels. Separately, the same GF(2) linear algebra at massive scale — sparse nullspace via [block Lanczos](https://en.wikipedia.org/wiki/Block_Lanczos_algorithm) or [Wiedemann](https://en.wikipedia.org/wiki/Block_Wiedemann_algorithm) — is the final stage of the [number field sieve](https://en.wikipedia.org/wiki/General_number_field_sieve) used to factor RSA moduli.

### Terminology

How this field's vocabulary reads as linear algebra.

| Domain term | In linear algebra |
|---|---|
| codeword | an element of the k-dimensional subspace of GF(2)^n |
| generator matrix G | a basis of the code, written as rows |
| parity-check matrix H | a basis of the code's orthogonal complement; codewords are its null space |
| syndrome | H y^T — depends only on the error, not the message |
| minimum distance | the smallest weight of a nonzero codeword |
| systematic form | G = [I \| P], so the message appears verbatim in the codeword |
| code rate | k/n, the subspace dimension over the ambient dimension |
| erasure vs error | known vs unknown error position — a column selection vs a search |

---

[Back to the index](/r/LinearAlgebra/wiki/applications)
