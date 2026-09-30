# PageRank: ranking by the structure of a network

### Start here

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

**Field:** Computer science, network science  
**Tier:** 2 — a dominant-eigenvector problem by construction.  
**Scalar field:** R  
**Vectors:** R^n over pages, but the solution is constrained to the probability simplex (nonnegative, entries summing to 1), which is NOT a subspace  
**Underlying equations:** None; a linear [difference equation](https://en.wikipedia.org/wiki/Recurrence_relation) π_{t+1} = G π_t, i.e. a discrete-time [Markov chain](https://en.wikipedia.org/wiki/Markov_chain)

### The problem

Order the pages of the web (or papers in a citation graph, or proteins in an interaction network) by importance, where importance is recursive: a page is important if important pages link to it.

### Variables

| Symbol | Name | What it holds | Shape | Units |
|---|---|---|---|---|
| n | number of pages |  | integer | — |
| outdeg(j) | out-degree | number of links on page j | integer | — |
| P | link (transition) matrix | p_ij = 1 / outdeg(j) if page j links to page i, else 0; column j says where a surfer on page j goes next | n × n | dimensionless (probabilities) |
| α | damping factor | probability that the surfer follows a link rather than jumping to a random page; conventionally 0.85 | scalar | dimensionless |
| 1 | all-ones vector |  | n × 1 | — |
| G | Google matrix | G = α P + ((1 − α)/n) 1 1ᵀ | n × n | dimensionless |
| t | step index | number of clicks so far | integer | — |
| π_t | distribution after t clicks | probability that the surfer is on each page after t clicks; entries are nonnegative and sum to 1 | n × 1 | dimensionless |
| r | PageRank vector | long-run fraction of time spent on each page | n × 1 | dimensionless; entries sum to 1 |

### Formulation

**Where the equations come from.** There is no differential equation, but there is a dynamical system in discrete time: a random surfer who, at each step, follows a random link from the current page with probability α and otherwise jumps to a page chosen uniformly at random. The distribution over pages evolves by a linear difference equation:

```
π_{t+1} = G π_t
```

Row i reads: the probability of being on page i next equals the sum over pages j of (probability of being on j now) × (probability of moving from j to i).

**What a solution means.** The difference equation's solution is π_t = Gᵗ π_0. Because α < 1 every entry of G is positive, and the [Perron–Frobenius theorem](https://en.wikipedia.org/wiki/Perron%E2%80%93Frobenius_theorem) then guarantees that π_t converges to the same limit r for every starting distribution π_0. That limit is the stationary distribution:

```
G r = r,     r ≥ 0,     1ᵀ r = 1
```

r is the [eigenvector](https://en.wikipedia.org/wiki/Eigenvalues_and_eigenvectors) of G with eigenvalue 1, scaled to sum to one. Using 1ᵀ r = 1, the same equation can be written without forming the dense matrix G:

```
r = α P r + ((1 − α)/n) 1
```

This models importance as long-run visit frequency: a page ranks highly if a surfer wandering indefinitely spends a large fraction of time there. P is stochastic only if every page has at least one outgoing link; pages without links (dangling nodes) must be patched first.

### Matrix structure

`P` is [sparse](https://en.wikipedia.org/wiki/Sparse_matrix) (average out-degree in the tens) and stochastic; `G` is dense but never formed — the damping term is a rank-one update applied on the fly, so each matrix–vector product still costs O(nnz).

### What is computed

[Power iteration](https://en.wikipedia.org/wiki/Power_iteration). Convergence rate is governed by `|λ₂/λ₁| ≤ α`, so the damping factor directly sets the iteration count: roughly 50–100 iterations at α = 0.85 regardless of graph size.

### Why linear algebra is the right tool

The circular definition of importance is a fixed-point equation, and Perron–Frobenius guarantees for an irreducible aperiodic nonnegative matrix that the fixed point exists, is unique, and is positive. The damping factor is what buys irreducibility — a modeling choice made to secure a theorem.

### Pitfall worth teaching

Dangling nodes (no outlinks) break [stochasticity](https://en.wikipedia.org/wiki/Stochastic_matrix), and the standard patch — treating them as linking to everything — is a modeling decision with real effects on the ranking. Every "algorithm detail" here is a mathematical requirement in disguise.

### Extensions

[Leslie matrices](https://en.wikipedia.org/wiki/Leslie_matrix) in population ecology (same dominant-eigenvector structure, eigenvalue = population growth rate); the [next-generation matrix](https://en.wikipedia.org/wiki/Next-generation_matrix) in epidemiology, whose [spectral radius](https://en.wikipedia.org/wiki/Spectral_radius) *is* [R₀](https://en.wikipedia.org/wiki/Basic_reproduction_number); [Katz centrality](https://en.wikipedia.org/wiki/Katz_centrality) and [hub/authority](https://en.wikipedia.org/wiki/HITS_algorithm) (HITS) scores; personalized [PageRank](https://en.wikipedia.org/wiki/PageRank) as a graph kernel in ML.

### Terminology

How this field's vocabulary reads as linear algebra.

| Domain term | In linear algebra |
|---|---|
| link matrix | the column-stochastic matrix P built from the graph |
| dangling node | a zero column, which breaks stochasticity |
| damping factor (alpha) | the weight on P versus the uniform teleportation term |
| teleportation | the rank-one correction that makes the chain irreducible |
| stationary distribution | the dominant eigenvector, normalized |
| power iteration | repeated multiplication by the matrix |
| centrality | a score defined as an eigenvector, or a function, of the graph matrix |

---

[Back to the index](/r/LinearAlgebra/wiki/applications)
