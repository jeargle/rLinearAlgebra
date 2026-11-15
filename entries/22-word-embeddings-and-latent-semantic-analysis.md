---
id: 22
slug: word-embeddings-and-latent-semantic-analysis
status: written
title: 'Latent semantic analysis: word meanings from a truncated SVD of word counts'
short_title: Word embeddings and latent semantic analysis
field_label: Natural language processing, information retrieval, search engines, text mining
tier_note: 'word and document vectors are read off a truncated SVD of a count matrix, and the Eckart–Young
  theorem says why truncation is the right step, so the entry needs the SVD. Word2vec and GloVe, named in
  Extensions, fit closely related factorizations by gradient descent.'
nav_field: Machine Learning & Data
field: Computer Science
subfield: NLP
tier: 2
tier_ceiling: 2
prereq_beyond_la: ''
scalar_field: R
vector_space: 'two count spaces: a document is a vector in R^m (one coordinate per vocabulary word) and a
  word is a vector in R^n (one coordinate per document). After truncation, words and documents both get
  coordinates in the same small space R^k, the latent space'
underlying_equations: 'A statistical model: a table of word counts approximated by a low-rank matrix,
  A ≈ U_k Σ_k V_kᵀ, chosen to minimize the sum of squared errors'
core_la_object: Factorization of a co-occurrence matrix
la_concepts: SVD; implicit matrix factorization
primary_method: Truncated SVD; SGD factorization
matrix_structure: sparse counts, low-rank structure
typical_size: 1e5 x 1e5
worked_example_size: 5 words x 4 documents by hand, rank-2 truncation
terminology:
  term-document matrix A: the m × n count matrix, one row per word and one column per document
  word-context (co-occurrence) matrix: the same idea with nearby words as the columns instead of documents
  latent semantic analysis (LSA, LSI): the truncated SVD A_k = U_k Σ_k V_kᵀ of the (weighted) count matrix
  topic or latent dimension: one singular triple (σ_j, u_j, v_j)
  word embedding w_i: row i of U_k Σ_k, the word's coordinates in the latent space
  document vector: row j of V_k Σ_k, the document's coordinates in the same space
  cosine similarity: the cosine of the angle between two vectors, x·y / (‖x‖ ‖y‖)
  folding-in: mapping a new document or query into the latent space, q̂ = Σ_k⁻¹ U_kᵀ q
  tf-idf weighting: rescaling the counts before the SVD so that common words count less
  PPMI: positive pointwise mutual information, a log-ratio reweighting of co-occurrence counts
  embedding dimension: k, the rank of the truncation
---

## Start here

A search engine that matches only exact words misses every page that says car when asked about an
automobile. People know these words are related because they see them used next to the same other words.

Latent semantic analysis turns that observation into arithmetic. Count how often every word appears
in every document of a large collection and arrange the counts in a table. Much of its detail is accidental,
such as which of two equivalent words an author chose; underneath are a few themes, each with typical
words and documents.

A standard tool from linear algebra finds the table with only a few themes that stays closest to the
real one. In it, a word is described by how strongly it belongs to each theme, so two words used in
similar company get similar descriptions even if they never share a document. Refined versions of the
idea give the word embeddings of modern language software.

## The problem

A collection of text is split into documents: a web page, a paragraph or an abstract. Each document is
a sequence of words, and the vocabulary is the list of distinct words in the whole collection, often
tens or hundreds of thousands of them after rare words are dropped. Counting each word in each document,
ignoring order, gives a term-document matrix: the document "the car needs a new engine" contributes
a 1 to the rows for car and engine in its column.

The motivating contrast is lexical against semantic matching. Lexical matching compares the words
themselves, so two documents are similar only if they share words. Semantic matching should compare
what the words mean. Given the count matrix, find a short vector for every word and every document so
that words used in similar contexts get nearby vectors, including synonyms such as car and automobile
that may never occur together.

## Variables

| Symbol | Name | What it holds | Shape | Units |
|---|---|---|---|---|
| m | vocabulary size | number of distinct words | integer | — |
| n | number of documents | documents in the collection | integer | — |
| a_ij | count | number of times word i occurs in document j | scalar | occurrences |
| A | term-document matrix | the counts a_ij; row i is word i's count vector, column j is document j's | m × n | occurrences |
| U, Σ, V | SVD factors | A = U Σ Vᵀ; U and V have orthonormal columns u_j and v_j, Σ is diagonal | m × r, r × r, n × r | U, V dimensionless; Σ in occurrences |
| σ_j | singular value | strength of latent dimension j, with σ_1 ≥ σ_2 ≥ … ≥ 0 | scalar | occurrences |
| r | rank | number of nonzero singular values | integer | — |
| k | embedding dimension | number of latent dimensions kept | integer, k < r | — |
| U_k, Σ_k, V_k | truncated factors | the first k columns of U and V, the first k singular values | m × k, k × k, n × k | as U, Σ, V |
| A_k | rank-k approximation | A_k = U_k Σ_k V_kᵀ | m × n | occurrences |
| w_i | word vector | row i of U_k Σ_k | 1 × k | occurrences |
| d_j | document vector | row j of V_k Σ_k | 1 × k | occurrences |
| q | query | word counts of a new document or search query | m × 1 | occurrences |
| q̂ | folded-in query | q̂ = Σ_k⁻¹ U_kᵀ q, the query's coordinates in the latent space | k × 1 | dimensionless |

## Formulation

**Where the equations come from.** The model is statistical: the observed counts are treated as a
low-rank matrix plus noise, where the noise is the individual author's choice among related words.
The low-rank part is the one closest to A in squared error.

**The familiar formula.** Everyone in search and text mining compares two vectors x and y by
cosine similarity, cos θ = x·y / (‖x‖ ‖y‖), where θ is the angle between them. It is 1 for vectors pointing the
same way and 0 for perpendicular ones. Applied to the raw rows of A, it fails for synonyms: if car and
automobile never share a document, their rows have no nonzero entry in common and their cosine is 0.

**One latent dimension.** Let v_j be a unit vector in ℝ^n, a weighting of the documents. The
coordinate of word i along it is the inner product of the word's count row with v_j, Σ_l a_il v_lj.
For the right singular vectors this inner product is A v_j = σ_j u_j, so word i's coordinate on
dimension j is σ_j u_ij. A word scores high on a dimension when it occurs in the documents that the
dimension weights heavily, whether or not it ever meets the other words that do.

**All dimensions at once.** Stacking every dimension gives the singular value decomposition, a sum of
rank-one pieces:

```
A = U Σ Vᵀ = Σ_j σ_j u_j v_jᵀ
```

Keeping the first k pieces gives the truncation A_k = U_k Σ_k V_kᵀ. By the Eckart–Young theorem, no
other matrix of rank k is closer to A, either in the sum of squared entry differences or in the
spectral norm, and the squared error is σ_(k+1)² + … + σ_r². The word vectors and document vectors
are the rows of

```
U_k Σ_k = A V_k        (word vectors w_i)
V_k Σ_k = Aᵀ U_k       (document vectors d_j)
```

A new query is placed in the space by folding-in, q̂ = Σ_k⁻¹ U_kᵀ q, which treats q as one more column
of A. The known quantity is A, counted from the text; the unknowns are U_k, Σ_k and V_k, and from them
the vectors.

**Worked case: 5 words, 4 documents.** The words are car, automobile, engine, fruit and apple, and the
documents are

- document 1: car, engine
- document 2: automobile, engine
- document 3: fruit, apple
- document 4: fruit, apple

so the nonzero counts are a_11 = 1, a_31 = 1, a_22 = 1, a_32 = 1, a_43 = 1, a_53 = 1, a_44 = 1 and
a_54 = 1, and every other a_ij is 0. Row by row:

```
      d1  d2  d3  d4
A = [ 1   0   0   0 ]    car
    [ 0   1   0   0 ]    automobile
    [ 1   1   0   0 ]    engine
    [ 0   0   1   1 ]    fruit
    [ 0   0   1   1 ]    apple
```

The raw cosine of car and automobile is 0. The squared singular values are the eigenvalues of AᵀA,
whose entries are inner products of document columns:

```
AᵀA = [ 2  1  0  0 ]
      [ 1  2  0  0 ]
      [ 0  0  2  2 ]
      [ 0  0  2  2 ]
```

The upper block has eigenvalues 3 and 1, the lower block 4 and 0, so σ_1 = 2, σ_2 = √3 ≈ 1.732,
σ_3 = 1 and σ_4 = 0. The first two right singular vectors are v_1 = (0, 0, 1, 1)/√2, the fruit
documents, and v_2 = (1, 1, 0, 0)/√2, the vehicle documents. Each word's coordinates are its row of A
times these two vectors:

```
U_2 Σ_2 = A V_2 = [ 0      0.707 ]    car
                  [ 0      0.707 ]    automobile
                  [ 0      1.414 ]    engine
                  [ 1.414  0     ]    fruit
                  [ 1.414  0     ]    apple
```

Car and automobile now have cosine 1, and car against fruit still has cosine 0. The dimension that was
dropped, σ_3 = 1 with u_3 = (1, −1, 0, 0, 0)/√2, is exactly the contrast "car, not automobile": the
detail of which synonym an author chose. The truncation itself fills in the missing synonym:

```
A_2 = [ 0.5  0.5  0  0 ]
      [ 0.5  0.5  0  0 ]
      [ 1    1    0  0 ]
      [ 0    0    1  1 ]
      [ 0    0    1  1 ]
```

so car now has weight 0.5 in document 2, which never mentions it. The error is ‖A − A_2‖ = σ_3 = 1 in
both norms, as Eckart–Young predicts. Folding in the one-word query automobile gives
q̂ = (0, 1/(3√2)) ≈ (0, 0.236), which has cosine 1 with document 1's vector d_1 = (0, √3/√2) ≈ (0, 1.225),
even though document 1 does not contain the word.

## Matrix structure

A is very sparse and nonnegative, with heavily skewed word frequencies. The useful structure is low
rank: a few hundred dimensions usually capture what matters, while the full rank is close to min(m, n).

## What is computed

Only the leading k singular triples are computed, with k typically 100 to 300, by Lanczos-type methods
(ARPACK's svds) or randomized SVD, which need only products of the sparse A and Aᵀ with vectors. Libraries include scikit-learn's TruncatedSVD and gensim's LsiModel.
The counts are reweighted first, usually by tf-idf for term-document matrices or PPMI for
word-context matrices.

## Why linear algebra is the right tool

Eckart–Young turns "keep the main themes, discard the noise" into an optimization with an exact
solution. Merging synonyms follows from the rank limit, not from any rule: with only k dimensions,
words with similar rows of A are not kept apart, because the directions separating them carry little
of the squared error.

## Pitfall worth teaching

Nearby in the latent space means "used in the same contexts", not "means the same". In the worked
case, engine has cosine 1 with car as well; it is merely longer. Related words (car, engine, road) cluster as
readily as synonyms, and antonyms such as hot and cold often end up close. A second trap is skipping the weighting: with raw counts, the leading
singular vectors describe the most frequent words, such as the and of, rather than any topic. The axes carry no fixed
meaning either: singular vectors are defined only up to sign.

## Extensions

The same truncated SVD is the empirical orthogonal functions entry in climate science and the
population-genetics PCA entry in genomics, where the rows are genetic markers rather than words. PPMI
replaces counts by log(P(word, context) / (P(word) P(context))), where P is a probability estimated from the counts and negative values are set to 0. Word2vec's
skip-gram with negative sampling has been shown to factorize, implicitly, a PMI matrix shifted by the
logarithm of the number of negative samples (Levy and Goldberg, 2014), and GloVe fits word vectors whose
inner products approximate the logarithms of co-occurrence counts, so both are low-rank factorizations
found by gradient descent instead of an SVD. The attention and low-rank adapters entry uses these
embeddings as inputs and low-rank matrices of its own. Ranking documents by a dominant eigenvector of a
link graph is the PageRank entry. Folding-in is a least-squares fit of q by the columns of U_k Σ_k,
the projection of the least-squares regression entry and the basis-fitting entry. At 10⁵ × 10⁵, randomized SVD multiplies A by a
few hundred random vectors, orthonormalizes the result, and takes an exact SVD of the small projected matrix.
