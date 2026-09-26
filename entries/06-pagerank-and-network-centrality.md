---
id: 6
slug: pagerank-and-network-centrality
status: seed
title: 'PageRank: ranking by the structure of a network'
short_title: PageRank and network centrality
field_label: Computer science, network science
tier_note: a dominant-eigenvector problem by construction.
nav_field: Computer Science & Networks
field: Computer Science
subfield: Network science
tier: 2
tier_ceiling: 2
prereq_beyond_la: ''
scalar_field: R
vector_space: R^n over pages, but the solution is constrained to the probability simplex (nonnegative,
  entries summing to 1), which is NOT a subspace
core_la_object: Stochastic matrix and dominant eigenvector
la_concepts: Perron-Frobenius; power iteration; rank-one update; stationary distribution
primary_method: Power iteration
matrix_structure: sparse column-stochastic plus rank-one
typical_size: 1e9 nodes
worked_example_size: 50-node synthetic web graph
terminology:
  link matrix: the column-stochastic matrix P built from the graph
  dangling node: a zero column, which breaks stochasticity
  damping factor (alpha): the weight on P versus the uniform teleportation term
  teleportation: the rank-one correction that makes the chain irreducible
  stationary distribution: the dominant eigenvector, normalized
  power iteration: repeated multiplication by the matrix
  centrality: a score defined as an eigenvector, or a function, of the graph matrix
---

## Start here

How do you rank web pages by importance when importance is circular? A page matters if important pages
link to it — but that definition refers to itself.

Picture someone clicking links at random forever. From whatever page they are on, they pick an outgoing
link at random and follow it. Occasionally, out of boredom, they jump to a completely random page
instead. Over a very long time, what fraction of their clicks land on each page?

That fraction is the ranking. Pages with many incoming links get visited often; pages linked from
frequently-visited pages get visited often too, which is exactly the circular definition, now made
precise as a statement about long-run behaviour.

The computation is remarkably simple: guess a distribution, push it through one round of clicking, and
repeat. It converges quickly, and the boredom-jump is not a detail — without it the process can get
permanently stuck in a corner of the web, and the whole thing falls apart.

## The problem

Order the pages of the web (or papers in a citation graph, or proteins in an interaction network) by importance, where importance is recursive: a page is important if important pages link to it.

## Formulation

Let `P` be the column-stochastic link matrix. PageRank is the stationary distribution

```
r = α P r + (1 − α)/n · 1,      equivalently     G r = r
```

with `G = α P + (1 − α)/n · 11ᵀ` the Google matrix and `α ≈ 0.85`.

## Matrix structure

`P` is sparse (average out-degree in the tens) and stochastic; `G` is dense but never formed — the damping term is a rank-one update applied on the fly, so each matrix–vector product still costs O(nnz).

## What is computed

Power iteration. Convergence rate is governed by `|λ₂/λ₁| ≤ α`, so the damping factor directly sets the iteration count: roughly 50–100 iterations at α = 0.85 regardless of graph size.

## Why linear algebra is the right tool

The circular definition of importance is a fixed-point equation, and Perron–Frobenius guarantees for an irreducible aperiodic nonnegative matrix that the fixed point exists, is unique, and is positive. The damping factor is what buys irreducibility — a modeling choice made to secure a theorem.

## Pitfall worth teaching

Dangling nodes (no outlinks) break stochasticity, and the standard patch — treating them as linking to everything — is a modeling decision with real effects on the ranking. Every "algorithm detail" here is a mathematical requirement in disguise.

## Extensions

Leslie matrices in population ecology (same dominant-eigenvector structure, eigenvalue = population growth rate); the next-generation matrix in epidemiology, whose spectral radius *is* R₀; Katz centrality and hub/authority (HITS) scores; personalized PageRank as a graph kernel in ML.
