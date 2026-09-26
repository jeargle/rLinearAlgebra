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
**Tier:** 1 — rank and null space over GF(2), using the finite-field material this collection wants at Tier 1. Reed–Solomon over GF(2^m) is Tier 3.  
**Scalar field:** GF(2) = {0,1} with XOR as addition; GF(2^m) for Reed-Solomon  
**Vectors:** GF(2)^n; the code is a k-dimensional subspace of it. There is no Euclidean length here - Hamming weight is a metric, not a norm from an inner product

### The problem

Send bits over a channel that flips some of them. Detect and correct the errors without retransmission.

### Formulation

Work over the field GF(2), where arithmetic is XOR. A linear `[n, k]` code is a `k`-dimensional subspace of GF(2)ⁿ. Encoding is

```
c = G m        (G: k × n generator matrix)
```

Every valid codeword lies in the null space of the parity-check matrix `H`:

```
H cᵀ = 0
```

A received word `y = c + e` gives the syndrome

```
s = H yᵀ = H eᵀ
```

which depends only on the error pattern, not on the message.

### Matrix structure

Entries in GF(2); LDPC codes use very sparse `H`; Reed–Solomon works over GF(2^m) with a Vandermonde-structured generator.

### What is computed

Syndrome decoding: look up or infer the minimum-weight `e` consistent with `s`. For LDPC codes, belief propagation on the bipartite graph of `H`. For Reed–Solomon, polynomial interpolation, which is a structured linear solve.

### Why linear algebra is the right tool

Distance properties — the whole point of a code — become rank conditions. A code corrects `t` errors if and only if every `2t` columns of `H` are linearly independent. Searching an exponentially large space of codewords collapses to a statement about column ranks.

### Pitfall worth teaching

This is where the abstraction of "field" earns its keep. Everything from linear algebra (rank, null space, dimension, bases) carries over unchanged; everything from geometry (angles, lengths, positive-definiteness, least squares) does not. A good exercise in what the axioms actually buy.

### Extensions

Reed–Solomon in QR codes, CDs, and RAID-6; LDPC in 5G and Wi-Fi 6; polar codes in 5G control channels. Separately, the same GF(2) linear algebra at massive scale — sparse nullspace via block Lanczos or Wiedemann — is the final stage of the number field sieve used to factor RSA moduli.

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
