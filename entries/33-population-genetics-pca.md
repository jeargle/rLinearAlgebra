---
id: 33
slug: population-genetics-pca
status: written
title: 'Principal components of a genotype matrix: what PCA plots of human genetic variation show'
short_title: Population genetics PCA
field_label: Population genetics, human genetics, genomics, evolutionary and conservation biology
tier_note: 'the principal components are the leading singular vectors of a centered genotype matrix,
  equivalently eigenvectors of a genetic relationship matrix. Reading them in terms of ancestry and
  genealogy rests on population-genetic models that the entry states but does not derive.'
nav_field: Life Sciences
field: Biology
subfield: Genomics
tier: 2
tier_ceiling: 2
prereq_beyond_la: ''
scalar_field: R
vector_space: 'two spaces: each individual is a vector in R^M (one coordinate per SNP), and each SNP is
  a vector in R^N (one coordinate per individual). SNP loadings live in R^M and individuals'' PC scores
  in R^N. Raw genotypes are integer counts 0, 1, 2, but after centering they are real numbers'
underlying_equations: 'A statistical decomposition of observed genotypes, X = U Σ Vᵀ, where X is the genotype matrix with each SNP''s mean subtracted'
core_la_object: Low-rank structure in a genotype matrix
la_concepts: SVD; interpretability limits; ascertainment bias
primary_method: Randomized SVD
matrix_structure: dense or sparse 0/1/2 genotype matrix
typical_size: 1e4 x 1e6
worked_example_size: 6 individuals from two populations x 5 SNPs by hand
terminology:
  SNP (single-nucleotide polymorphism): one column of G; a coordinate of R^M
  genotype g_ij: one entry of G, a count 0, 1 or 2 of the counted allele
  allele frequency p_j: half the mean of column j of G
  mean-centering: subtracting each column's mean, 2 p_j, to give X
  principal component (PC) axis v_k: a right singular vector of X, a direction in SNP space
  SNP loadings: the entries of v_k, one weight per SNP
  PC scores t_k: X v_k = σ_k u_k, each individual's coordinate along axis k
  PC plot: the individuals plotted at their coordinates (t_1, t_2)
  genetic relationship matrix (GRM) K: X Xᵀ / M, the N × N Gram matrix of the individuals' centered genotype rows
  proportion of variance explained: σ_k² / Σ σ_l²
  LD pruning: deleting SNPs that are nearly collinear with nearby SNPs before the SVD
  projecting new samples: computing x v_k for a new row x on axes fitted without it
---

## Start here

Every person carries two copies of the genome, one from each parent, and at a few million positions
the DNA letter differs from person to person. Genotyping chips read hundreds of thousands of those
positions at once, so a study of ten thousand people produces a table with ten thousand rows and
hundreds of thousands of columns.

Population geneticists want a picture of who is related to whom from that table. The standard
first step squeezes it down to two numbers per person and plots one dot per person. People whose
ancestors lived in the same place for many generations share many small differences in letter
frequency, so their dots land near each other. In the best-known example, Europeans plotted this way
form a picture that looks like a map of Europe.

The method is principal component analysis, which finds the directions along which people differ
most. It needs no labels: nobody tells it which person came from where. That is its strength, and
it is also why its pictures are easy to over-read. The axes are whatever directions explain the most
variation in this particular sample, and they need not correspond to populations, migrations or
history.

## The problem

Some vocabulary first. A **SNP** (single-nucleotide polymorphism) is a position in the genome where the
DNA letter varies between people: for example, at one position some chromosomes carry an A and others a
G. The two versions are the SNP's two **alleles**. An **individual** is one sampled person (or animal,
or plant) with two copies of each chromosome. The individual's **genotype** at a SNP is the number of
copies of one chosen allele that it carries: 0, 1 or 2. At the A/G SNP, counting G, a person with two As
has genotype 0, an A/G person has 1, and a G/G person has 2. A **population** is a group of individuals
who share ancestry because their ancestors mated mostly with each other. Allele frequencies drift apart
between populations, so the same SNP can be 90% G in one population and 40% G in another.

The motivating contrast is between labels and data. Researchers record labels such as birthplace or
self-reported ancestry. Principal component analysis (PCA) instead asks which directions in the
genotypes themselves carry the most variation, and only afterwards are the labels used to color the
dots.

Given the genotypes of N individuals at M SNPs, find each individual's coordinates along the few
directions of greatest genetic variation.

## Variables

| Symbol | Name | What it holds | Shape | Units |
|---|---|---|---|---|
| N | sample size | number of individuals | integer | — |
| M | number of SNPs | number of genotyped positions | integer | — |
| g_ij | genotype | copies of the counted allele carried by individual i at SNP j | scalar in {0, 1, 2} | allele copies |
| G | genotype matrix | row i is individual i, column j is SNP j | N × M | allele copies |
| p_j | allele frequency | fraction of all 2N copies at SNP j that are the counted allele | scalar | dimensionless |
| X | centered genotype matrix | x_ij = g_ij − 2 p_j, optionally divided by √(p_j (1 − p_j)) | N × M | allele copies (dimensionless if scaled) |
| x_i | individual's row | row i of X | 1 × M | as X |
| U | left singular vectors | columns u_k of unit length, one coordinate per individual | N × ρ | dimensionless |
| Σ | singular values | diagonal σ_1 ≥ σ_2 ≥ … > 0 | ρ × ρ | as X |
| V | right singular vectors | columns v_k of unit length: the PC axes, one loading per SNP | M × ρ | dimensionless |
| t_k | PC scores | t_k = X v_k = σ_k u_k, every individual's coordinate on axis k | N × 1 | as X |
| K | genetic relationship matrix | K = X Xᵀ / M, the average product of two individuals' centered genotypes | N × N | (as X)² |
| ρ | rank | number of nonzero singular values, at most min(N − 1, M) | integer | — |
| q | PCs retained | how many axes are plotted or kept | integer | — |

## Formulation

**Where the equations come from.** The model is a statistical decomposition of observed genotypes. No
model of ancestry is assumed; the population-genetic reading of the result comes afterwards.

**The familiar formulas.** Geneticists start from the allele frequency and the relationship matrix:

```
p_j = (g_1j + g_2j + … + g_Nj) / (2N)
K = X Xᵀ / M
```

Entry K_il is large and positive when individuals i and l tend to carry the same rare alleles. PCA in
genetics is usually described as taking the top eigenvectors of K. Centering matters: the mean genotype
at SNP j is 2 p_j, and subtracting it makes x_ij measure how far individual i departs from the sample
at that SNP. Dividing by √(p_j (1 − p_j)) gives rare and common SNPs comparable weight (EIGENSOFT's
choice). Under Hardy–Weinberg proportions the variance of g_ij is 2 p_j (1 − p_j), so this scaling
differs from standardizing only by a constant factor √2, which does not change the axes.

**One axis, one individual.** Pick a unit vector v in ℝ^M, one weight per SNP. Individual i's
coordinate along v is an inner product:

```
t_i = x_i · v = x_i1 v_1 + x_i2 v_2 + … + x_iM v_M
```

Doing this for every individual gives the vector t = X v. PCA chooses v to make the spread of the
coordinates, ‖X v‖², as large as possible. The maximizer is v_1, the top right singular vector of X,
and the maximum is σ_1².

**All axes at once.** The SVD

```
X = U Σ Vᵀ = σ_1 u_1 v_1ᵀ + σ_2 u_2 v_2ᵀ + …
```

gives every axis. v_k is the PC axis in SNP space, its entries are the SNP loadings, and t_k = X v_k
= σ_k u_k holds every individual's score on PC k. Since K = U (Σ² / M) Uᵀ, the left singular vectors u_k
are the eigenvectors of the relationship matrix, with eigenvalues σ_k² / M. The fraction σ_k² / Σ_l σ_l²
is the proportion of variance explained by PC k.

What is known is G, and therefore X. What is solved for is V (the axes), Σ and the scores t_k.
Population labels are not inputs.

**Worked case: two populations, five SNPs.** Individuals 1–3 come from one population and 4–6 from
another. Population 1 carries two copies of the counted allele at SNPs 1 and 5 and none at SNP 2, while
everyone in population 2 carries one copy at SNPs 2 and 5. SNPs 3 and 4 have allele frequency 0.5 in
both populations, and individuals 1 and 2 differ there.

```
G = [ 2  0  2  0  2 ]
    [ 2  0  0  2  2 ]
    [ 2  0  1  1  2 ]
    [ 0  1  1  1  1 ]
    [ 0  1  1  1  1 ]
    [ 0  1  1  1  1 ]
```

The column means 2 p_j are (1, 0.5, 1, 1, 1.5), so p = (0.5, 0.25, 0.5, 0.5, 0.75). Subtracting them
from every row:

```
X = [  1   −0.5   1   −1    0.5 ]
    [  1   −0.5  −1    1    0.5 ]
    [  1   −0.5   0    0    0.5 ]
    [ −1    0.5   0    0   −0.5 ]
    [ −1    0.5   0    0   −0.5 ]
    [ −1    0.5   0    0   −0.5 ]
```

X has rank 2, and its SVD can be read off by inspection:

```
u_1 = (1, 1, 1, −1, −1, −1) / √6     v_1 = (2, −1, 0, 0, 1) / √6     σ_1 = 3
u_2 = (1, −1, 0, 0, 0, 0) / √2       v_2 = (0, 0, 1, −1, 0) / √2     σ_2 = 2
```

To check, 3 u_1 v_1ᵀ has row ±(1, −0.5, 0, 0, 0.5), plus for individuals 1–3 and minus for 4–6,
which is the population part of X. Then 2 u_2 v_2ᵀ adds (1, −1) and (−1, 1) in columns 3 and 4 of rows
1 and 2. One score by hand: individual 1 on PC1 is

```
x_1 · v_1 = (1 · 2 + (−0.5)(−1) + 1 · 0 + (−1) · 0 + 0.5 · 1) / √6 = 3 / √6 ≈ 1.22
```

and all of them together are

```
t_1 = X v_1 = (1.22, 1.22, 1.22, −1.22, −1.22, −1.22)
t_2 = X v_2 = (1.41, −1.41, 0, 0, 0, 0)
```

PC1 separates the two populations perfectly and explains 9/13 ≈ 69% of the variance. PC2 explains 4/13
≈ 31%, but it describes only individuals 1 and 2 and says nothing about populations. The eigenvalues of
K are 9/5 = 1.8 and 4/5 = 0.8. With the √(p_j (1 − p_j)) scaling, u_1, u_2 and v_2 are unchanged,
but SNPs 2 and 5 (p = 0.25 and 0.75) gain weight relative to SNP 1 (p = 0.5), so v_1 tilts to (√3, −1, 0, 0, 1) / √5. Then
σ_1 = √40 ≈ 6.32 and σ_2 = 4, and PC1's share rises to 40/56 ≈ 71%. The signs of u_k and v_k are
arbitrary: software may return −u_1 and −v_1, flipping the plot.

## Matrix structure

G is a dense integer matrix stored in 2 bits per entry, short and very wide (10⁴ individuals by 10⁶
SNPs is typical). Centering would destroy any sparsity, so large-scale codes multiply by G and correct
for the means on the fly instead of forming X. K is N × N, symmetric and positive semidefinite. Its
rank is at most N − 1, because centering makes every column of X orthogonal to the vector of 1s.

## What is computed

Only the top 10–20 singular triples are needed. For N up to a few thousand, tools form K and take its
leading eigenvectors (EIGENSOFT's smartpca). At biobank scale they use randomized SVD or Lanczos
iterations that touch G only through products G v and Gᵀ u (PLINK 2's approximate PCA, FlashPCA). New
individuals are often placed on axes fitted to a reference panel by computing x v_k.

## Why linear algebra is the right tool

Shared ancestry is shared covariance. Individuals from one population depart from the overall allele
frequencies in the same direction at thousands of SNPs at once. In the worked case that is the rank-one
piece σ_1 u_1 v_1ᵀ. The SVD finds such directions without being told which individuals belong together.
Its optimality is the Eckart–Young statement: no other q axes reconstruct X better in the
least-squares sense.

## Pitfall worth teaching

PCs are directions of maximal variance in one sample, not populations, migration routes or admixture
events. The worked case already shows a PC driven by two individuals. In real data, relatives, a batch
of samples genotyped in one laboratory, or a long stretch of SNPs in linkage disequilibrium
(neighboring SNPs inherited together, so their columns are nearly collinear) can each produce a PC of
its own. Pruning SNPs in LD before the SVD is standard for that reason.

Sample composition moves the axes. A population sampled 1,000 times pulls PC1 towards its internal
variation, while one sampled 10 times barely registers. Ascertainment bias has the same effect from the
SNP side: genotyping chips favor SNPs that were common in the populations used to design them, which
distorts distances for everyone else.

The geography is real but partial. Novembre and colleagues found that PC1 and PC2 of about 1,400
Europeans reproduce the map of Europe, because genetic similarity decays smoothly with distance. That
smooth decay also sets a trap: Novembre and Stephens showed that continuous spatial structure produces
sinusoidal PCs, gradients and saddles that resemble the traces of ancient migrations even when no
migration occurred. McVean showed that, under standard population-genetic models, an individual's
expected position on the PC plot is determined by its average genealogical relatedness to the rest of
the sample. Different histories can give the same plot.

## Extensions

The same SVD with a climate vocabulary is the EOF entry, which carries the same warning that optimal
axes need not be physical modes. The word-embedding entry applies a truncated SVD to a term–document
matrix, and the attention and LoRA entry exploits low rank in weight updates.
Genome-wide association studies include the top PCs as covariates in a regression to correct for
population structure (the regression entry), and placing new samples on existing axes is a least-squares
fit in an orthonormal basis (the basis-fitting entry). The sinusoids of Novembre and Stephens are
eigenvectors of a covariance that depends only on distance, the same sines that diagonalize the
second-difference matrix of the finite-difference entry. Randomized SVD at 10⁴ × 10⁶ sharpens its
subspace with a few steps of the power iteration from the PageRank entry. Admixture models such as
STRUCTURE and ADMIXTURE replace the SVD with a nonnegative factorization, G / 2 ≈ Q F, where row i of Q
holds individual i's ancestry proportions (nonnegative, summing to 1) and F holds each ancestral
population's allele frequencies (between 0 and 1).