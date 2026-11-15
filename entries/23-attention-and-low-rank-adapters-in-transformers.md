---
id: 23
slug: attention-and-low-rank-adapters-in-transformers
status: written
title: 'Attention and low-rank adapters: learned bilinear forms and rank-limited updates in transformers'
short_title: Attention and low-rank adapters in transformers
field_label: Machine learning, natural language processing, large language models
tier_note: 'attention scores are a bilinear form of rank at most d_k, and a low-rank adapter is a
  product of two thin matrices, so posing both needs only matrix products and rank. The best rank-r
  update comes from the SVD (Eckart–Young), which makes the entry Tier 2. How the weights are learned,
  by gradient-based optimization of a deep network, is Tier 3.'
nav_field: Machine Learning & Data
field: Computer Science
subfield: Deep learning
tier: 2
tier_ceiling: 3
prereq_beyond_la: deep learning; optimization
scalar_field: R
vector_space: 'R^d token embeddings, one row vector per token. Queries and keys live in a smaller space
  R^(d_k) and values in R^(d_v). A weight matrix W of size d × m is a point in the space of d × m matrices,
  and a low-rank adapter restricts its change to the matrices of rank at most r, which is not a subspace'
underlying_equations: 'A parameterized model whose weights are fixed by training: Y = softmax(X W_Q W_Kᵀ
  Xᵀ / √d_k) X W_V, with the softmax applied row by row, and a fine-tuned weight W_0 + B A'
core_la_object: Learned bilinear forms and rank-constrained updates
la_concepts: bilinear forms; rank of a product; low-rank parameterization; row-stochastic matrices;
  SVD and Eckart-Young; associativity of matrix products
primary_method: Dense GEMM
matrix_structure: dense; W_Q W_Kᵀ has rank at most d_k; the adapter B A has rank at most r; the
  attention-weight matrix is row-stochastic
typical_size: 1e3-1e4 per head
worked_example_size: 3 tokens in R^3 with one 2-dimensional head and a rank-1 adapter by hand; adapter counts for a 4096 × 4096 weight
terminology:
  token: one row x_i of X, the vector representing one word or word-piece
  embedding dimension d: the length of each token vector
  query, key, value: the rows of Q = X W_Q, K = X W_K and V = X W_V, three linear images of each token
  attention score s_ij: the bilinear form x_i W_Q W_Kᵀ x_jᵀ, equal to the dot product q_i · k_j
  head dimension d_k: the inner dimension of W_Q W_Kᵀ, so the rank cap of the score form
  scaled dot-product attention: softmax(Q Kᵀ / √d_k) V, a row-stochastic matrix times V
  attention weights P: the row-stochastic matrix; row i holds the mixing proportions for token i
  softmax: the row-by-row map e^(z_j) / Σ_l e^(z_l), the one nonlinear step
  attention head: one triple (W_Q, W_K, W_V); several heads run in parallel and are concatenated
  fine-tuning: changing pretrained weights W_0 to W_0 + ΔW for a new task
  LoRA rank r: the inner dimension of ΔW = B A, an upper bound on rank(ΔW)
  adapter merging: forming W_0 + B A once, so inference costs nothing extra
---

## Start here

A large language model reads text as a sequence of tokens, each turned into a list of a few thousand
numbers. To understand a word it has to look at the other words around it: in "the bank of the
river", the meaning of "bank" depends on "river". The mechanism that does this is called attention.
Each word scores every other word for relevance, the scores are turned into proportions, and the word's
new representation is the corresponding blend of the others.

Almost all of this is matrix multiplication. The relevance score between two words is a fixed recipe
applied to their two lists of numbers, and that recipe is a matrix. A surprising property is that the
matrix is deliberately low-rank: it can only compare words along a limited number of directions.

The same idea, used on purpose, makes it cheap to adapt a model to a new task. Instead of retraining
millions of numbers in a weight matrix, one learns a change to it that is the product of two thin
matrices. That change has low rank and costs a tiny fraction of the storage, and for many tasks it is
enough.

## The problem

A token is a unit of text, such as a word or part of a word, and its embedding is the list of real
numbers, a vector, that represents it. A transformer layer receives n tokens as the rows of a matrix and must produce n new
vectors, each a context-dependent mixture of the others. The contrast with older models is between a
fixed representation, where "bank" always has the same vector, and a contextual one, where its vector
depends on the sentence. A weight matrix is a matrix of numbers fixed by training, and an attention
head is one set of three of them (query, key and value weights). Given the weights, compute the
attention scores, the mixing proportions, and the output.

The second problem is fine-tuning: a pretrained weight matrix is known, and a change to it is wanted
that adapts the model to a new task. An adapter is a small set of extra parameters that produces that
change. The question is how many numbers the change needs, and what is lost by restricting its rank.

## Variables

| Symbol | Name | What it holds | Shape | Units |
|---|---|---|---|---|
| n | sequence length | number of tokens | integer | — |
| d | embedding dimension | length of each token vector | integer | — |
| d_k, d_v | head dimensions | length of each query/key and each value | integers | — |
| x_i | token embedding | the vector for token i | 1 × d (row) | dimensionless |
| X | token matrix | row i is x_i | n × d | dimensionless |
| W_Q, W_K, W_V | query, key, value weights | learned linear maps | d × d_k, d × d_k, d × d_v | dimensionless |
| Q, K, V | queries, keys, values | Q = X W_Q, K = X W_K, V = X W_V; rows q_i, k_j, v_j | n × d_k, n × d_k, n × d_v | dimensionless |
| M | score matrix of the bilinear form | M = W_Q W_Kᵀ | d × d | dimensionless |
| S | attention scores | S = Q Kᵀ, entries s_ij | n × n | dimensionless |
| P | attention weights | softmax of S / √d_k, row by row | n × n | dimensionless |
| Y | head output | Y = P V | n × d_v | dimensionless |
| W_0 | pretrained weight | a frozen weight matrix | d × m | dimensionless |
| m | output width of W_0 | number of columns of W_0 | integer | — |
| ΔW | fine-tuning update | the change added to W_0 | d × m | dimensionless |
| r | adapter rank | inner dimension of the adapter | integer, r ≪ min(d, m) | — |
| B, A | adapter factors | ΔW = B A | d × r and r × m | dimensionless |

## Formulation

**Where the equations come from.** The model is a parameterized function. Its weights are numbers
found by training, which this entry takes as given.

**The familiar formula.** Practitioners know attention as

```
Attention(Q, K, V) = softmax(Q Kᵀ / √d_k) V
```

with Q, K, V the queries, keys and values above. Everything except the softmax is matrix
multiplication.

**One score.** Token i asks a question, its query q_i = x_i W_Q, and token j offers a label, its key
k_j = x_j W_K. The query is so called because it is what token i is looking for, and the key because
it is what other tokens are matched against. The score is their dot product:

```
s_ij = q_i · k_j = x_i W_Q W_Kᵀ x_jᵀ = x_i M x_jᵀ
```

So the score is a bilinear form in the two token vectors, with matrix M = W_Q W_Kᵀ. M is d × d but is a
product through a d_k-dimensional middle, so rank(M) ≤ d_k. When d_k < d, the form ignores every
direction of x_j in the null space of M: a head can compare tokens along at most d_k directions.

**All scores at once.** Stacking the queries and keys as rows,

```
S = Q Kᵀ = X M Xᵀ
```

**Softmax, the one nonlinear step.** The softmax turns a list of scores into weights that are positive
and sum to 1: exponentiate each score, then divide by the total. It is called the softmax because it is
a soft version of picking the maximum. The largest score gets the largest weight without taking all of
it: scores (2, 1, 0) become weights (0.665, 0.245, 0.090), while scores (20, 10, 0), spread ten times
wider, give almost exactly (1, 0, 0). Each row of S is divided by √d_k and passed through the softmax,
separately row by row:

```
P_ij = e^(s_ij / √d_k) / Σ_l e^(s_il / √d_k)
```

Every entry of P is positive and each row sums to 1, so P is row-stochastic. The softmax is what makes
attention nonlinear in X; every other step is linear.

**The output.** Y = P V, so row i of Y is the weighted average Σ_j P_ij v_j of the value vectors.

**Worked case: three tokens, one head.** Take n = 3, d = 3, d_k = d_v = 2, with tokens
x_1 = (1, 0, 1), x_2 = (0, 1, 0), x_3 = (1, 1, 0):

```
X = [ 1  0  1 ]      W_Q = [ 1  0 ]      W_K = [ 1  0 ]      W_V = [ 0  1 ]
    [ 0  1  0 ]            [ 0  1 ]            [ 0  1 ]            [ 1  0 ]
    [ 1  1  0 ]            [ 1  0 ]            [ 0  0 ]            [ 1  1 ]
```

One component first: q_1 = x_1 W_Q = (1 + 1, 0) = (2, 0) and k_3 = x_3 W_K = (1, 1), so
s_13 = 2·1 + 0·1 = 2. Doing every row gives

```
Q = [ 2  0 ]      K = [ 1  0 ]      V = [ 1  2 ]
    [ 0  1 ]          [ 0  1 ]          [ 1  0 ]
    [ 1  1 ]          [ 1  1 ]          [ 1  1 ]
```

and the scores, as Q × Kᵀ = S:

```
S = [ 2  0  2 ]
    [ 0  1  1 ]
    [ 1  1  2 ]
```

The matrix of the bilinear form is

```
M = W_Q W_Kᵀ = [ 1  0  0 ]
               [ 0  1  0 ]
               [ 1  0  0 ]
```

It has rank 2, and its third column is zero, so the third coordinate of the key token never affects a
score; X M Xᵀ reproduces S. M is not symmetric, and neither is S: s_13 = 2 but s_31 = 1.

For the softmax, divide by √2. Row 1 becomes (1.414, 0, 1.414), with exponentials (4.113, 1, 4.113)
summing to 9.227, so row 1 of P is (0.446, 0.108, 0.446). The full matrices are

```
P = [ 0.446  0.108  0.446 ]          Y = P V = [ 1.000  1.337 ]
    [ 0.198  0.401  0.401 ]                    [ 1.000  0.797 ]
    [ 0.248  0.248  0.503 ]                    [ 1.000  1.000 ]
```

The first column of Y is all 1s because every value vector has first entry 1 and each row of P sums
to 1, a quick check that P averages.

**Low-rank adapters.** The method is called LoRA, for low-rank adaptation. The pretrained W_0 is
frozen, and the update is constrained to the product

```
W = W_0 + ΔW,     ΔW = B A,     B is d × r, A is r × m
```

which forces rank(ΔW) ≤ r. During fine-tuning W_0 is known and B and A are the unknowns, found by
training; here they are taken as given, and the question is what the restriction costs and saves. Storing ΔW in full takes d m numbers; storing B and A takes r (d + m). With
d = m = 3 and r = 1, B = (1, 2, 0)ᵀ and A = (1, 0, −1) give the rank-1 update

```
ΔW = B A = [ 1  0  −1 ]
           [ 2  0  −2 ]
           [ 0  0   0 ]
```

from 6 numbers instead of 9. At realistic size, d = m = 4096 and r = 8, a full update has
16,777,216 numbers and the adapter 65,536, which is 0.39% of them, or 256 times fewer.

**Relation to the SVD.** By the Eckart–Young theorem, the closest rank-r matrix to any update ΔW, in
the Frobenius and spectral norms, is its SVD truncated to the r largest singular values. A rank-r
adapter can therefore represent exactly the updates that keep r singular values, and LoRA rests on
the observation that useful fine-tuning updates have most of their size in a few of them.

## Matrix structure

X, the weights, Q, K and V are dense. M = W_Q W_Kᵀ and ΔW = B A are dense but rank-limited, and they
are never formed during attention: the products are taken in factored form. S and P are n × n, so
their cost grows with the square of the sequence length. P is row-stochastic.

## What is computed

General matrix-matrix products (GEMM) on GPUs: X W_Q, X W_K, X W_V, Q Kᵀ and P V, with the softmax in
between. Fused kernels such as FlashAttention compute P V in tiles without ever storing the whole n × n
matrix P. With an adapter, x W_0 + (x B) A costs two thin products; after fine-tuning the adapter can be
merged into W_0 + B A once, so inference costs nothing extra.

## Why linear algebra is the right tool

Rank explains both halves. A head with d_k = 64 or 128 scores tokens through a form of rank at most
d_k, which is why models use many heads, each free to compare tokens along different directions.
Fine-tuning by low-rank update is the statement that the useful change lives in a small set of
directions, and the SVD says how much is lost by assuming so. Associativity explains costs: grouping
X (W_Q W_Kᵀ) Xᵀ or (X W_Q)(X W_K)ᵀ gives the same S at different prices.

## Pitfall worth teaching

An attention score is not a similarity. A similarity would be symmetric, like a dot product x_i · x_j,
but M = W_Q W_Kᵀ is generally not symmetric, so how much token i attends to token j differs from how
much j attends to i: in the worked case s_13 = 2 and s_31 = 1. M is also not positive definite, and of
rank at most d_k, so a token need not score itself highly and two different tokens can be
indistinguishable to a head. Reading attention weights as "which words are alike" misreads a learned
bilinear form as an inner product.

## Extensions

Multi-head attention runs h heads in parallel, each with d_k = d / h, concatenates their outputs and
applies one more d × d matrix. The low-rank bottleneck of a single head, and the related softmax
bottleneck of the output layer (a log-probability matrix of limited rank), are rank arguments. Linear
attention replaces the softmax with a feature map φ, so the product φ(Q) φ(K)ᵀ V can be grouped as
φ(Q) (φ(K)ᵀ V), and associativity drops the cost from n² to n. Rotary position embeddings rotate each
pair of query and key coordinates by an angle proportional to position, so a score depends on the
offset between positions through a product of 2 × 2 rotations (the 3D rotations entry treats the
rotation matrices themselves). Learning the weights by gradient descent on a loss function is deep
learning and optimization, which is why the ceiling is Tier 3.

The SVD and Eckart–Young appear in the empirical orthogonal functions entry, where the low-rank
approximation is of climate data rather than of a weight update. Word embeddings and latent semantic
analysis (the word embeddings entry) are where token vectors come from, and population-genetics PCA
(the population genetics entry) is the same truncated SVD in another vocabulary. The row-stochastic P
is the same kind of matrix as the PageRank entry's transition matrix. The Eckart–Young best rank-r
approximation minimizes a sum of squares, the matrix analog of the projections in the regression
entry and the basis-fitting entry.
