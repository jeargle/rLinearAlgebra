# Consensus and opinion dynamics: repeated averaging with a row-stochastic matrix

### Start here

A group of people each hold an opinion that can be written as a number: an estimate of a price or the
probability that it will rain tomorrow. They talk. After each round of
conversation, everyone revises their estimate toward the estimates of the people they listen to, giving
more weight to some voices than to others.

Two questions follow. Does the group ever agree? And if it does, on what number? It is tempting to guess
the plain average of where everyone started, but that is usually wrong. People who are listened to by
people who are themselves listened to pull the final answer toward their own starting view.

The same arithmetic runs inside machines. Sensors in a field, drones in a swarm or computers in a data
center can each hold a reading and repeatedly average with their neighbors, with no central computer,
until all of them hold the same value.

**Field:** Network science, social network analysis, distributed computing, sensor networks, multi-agent control  
**Tier:** 2 — the agreed value is set by the left Perron [eigenvector](https://en.wikipedia.org/wiki/Eigenvalues_and_eigenvectors) of the trust matrix and the speed of agreement by its second-largest eigenvalue modulus, so the entry needs eigenvalues and [Perron–Frobenius](https://en.wikipedia.org/wiki/Perron%E2%80%93Frobenius_theorem). The continuous-time model, named in Extensions, is an [ordinary differential equation](https://en.wikipedia.org/wiki/Ordinary_differential_equation) and raises the ceiling to Tier 3.  
**Scalar field:** R  
**Vectors:** R^n over agents: x(t) holds one opinion per person. The influence weights π live in the probability simplex (nonnegative, summing to 1), which is not a subspace  
**Underlying equations:** A linear [difference equation](https://en.wikipedia.org/wiki/Recurrence_relation) x(t+1) = W x(t), with W [row-stochastic](https://en.wikipedia.org/wiki/Stochastic_matrix), so that each new opinion is a [weighted average](https://en.wikipedia.org/wiki/Weighted_arithmetic_mean) of current opinions

### The problem

The setting has three core nouns. An agent is one participant: a person, a sensor or a computer. An
opinion is the single real number an agent holds at a given time, for example an estimated price in
dollars. The trust graph records who listens to whom: an arrow from agent i to agent j means that i
gives j's opinion some weight, and every agent may also give weight to their own opinion. For example,
in a committee of three, P may listen only to their own opinion and Q's, while Q listens to everyone.

Time is counted in rounds t = 0, 1, 2, …, and in each round every agent replaces their opinion by a
fixed weighted average of the current opinions they listen to. The weights are given; the starting
opinions are given. The unknowns are the long-run behavior: whether all opinions converge to one
common value (consensus), what that value is, and how many rounds it takes to get close.

The motivating contrast is between the plain average of the starting opinions and the value the group
actually reaches. The two coincide only in special networks. In general the group lands on a
weighted average whose weights measure each agent's influence in the network, and that weighting, not the
individual trust weights, is what the field means by social power.

### Variables

| Symbol | Name | What it holds | Shape | Units |
|---|---|---|---|---|
| n | number of agents | people, sensors or computers in the network | integer | — |
| i, j | agent indices | i is the listener, j the agent listened to | integers 1 … n | — |
| t | round | number of averaging rounds so far | integer | — |
| x_i(t) | opinion | agent i's opinion after t rounds | scalar | units of the opinion (for example dollars) |
| x(t) | opinion vector | the opinions x_i(t) stacked | n × 1 | units of the opinion |
| w_ij | trust weight | weight agent i gives to agent j's opinion; w_ij ≥ 0 and Σ_j w_ij = 1 | scalar | dimensionless |
| W | trust (influence) matrix | the weights w_ij; row i is agent i's averaging rule | n × n | dimensionless |
| 1 | all-ones vector | | n × 1 | — |
| π | influence weights (social power) | left eigenvector of W for eigenvalue 1, scaled so 1ᵀ π = 1 | n × 1 | dimensionless |
| c | consensus value | the common limit of every x_i(t) | scalar | units of the opinion |
| λ_k | eigenvalues of W | ordered so 1 = λ_1 ≥ |λ_2| ≥ … ≥ |λ_n| | scalar, possibly complex | dimensionless |

### Formulation

**Where the equations come from.** The model is a linear difference equation: opinions at round t+1
are computed from opinions at round t by a fixed rule, with nothing happening between rounds.

**The familiar formula.** A weighted average of numbers y_1, …, y_m with weights a_1, …, a_m that are
nonnegative and sum to 1 is a_1 y_1 + … + a_m y_m. A course grade that counts homework at 0.4 and
exams at 0.6 is one example: homework 80 and exams 90 give 0.4 × 80 + 0.6 × 90 = 86. A weighted average
always lies between the smallest and the largest of the y's.

**One agent.** Agent i's update is that weighted average, with the trust weights w_ij as the a's and
the current opinions x_j(t) as the y's:

```
x_i(t+1) = w_i1 x_1(t) + w_i2 x_2(t) + … + w_in x_n(t)
```

**All agents at once.** Stacking the n updates gives the [DeGroot model](https://en.wikipedia.org/wiki/DeGroot_learning):

```
x(t+1) = W x(t),   so   x(t) = W^t x(0)
```

W is nonnegative and every row sums to 1, W 1 = 1, which is what row-stochastic means. So 1 is a right
eigenvector with eigenvalue 1: if everyone already agrees, nobody moves.

**The limit.** Suppose the trust graph is [strongly connected](https://en.wikipedia.org/wiki/Strongly_connected_component) (every agent's opinion reaches every other
agent through some chain of arrows) and [aperiodic](https://en.wikipedia.org/wiki/Aperiodic_graph). Aperiodic means that the [greatest common divisor](https://en.wikipedia.org/wiki/Greatest_common_divisor)
(gcd) of the lengths of the graph's cycles is 1; the gcd is the largest whole number dividing all of
them, so cycles of lengths 2 and 3 have gcd 1. A single positive self-weight w_ii gives a cycle of
length 1 and is enough. Under these conditions the Perron–Frobenius theorem says that 1 is a simple
eigenvalue, every other eigenvalue has |λ_k| < 1, and the matching left eigenvector π, with πᵀ W = πᵀ,
can be taken with every entry positive. Then

```
W^t → 1 πᵀ,   so   x(t) → 1 (πᵀ x(0)),   c = πᵀ x(0) = π_1 x_1(0) + … + π_n x_n(0)
```

Everyone agrees, and the consensus value is the π-weighted average of the starting opinions. The
quantity πᵀ x(t) is the same at every round, because πᵀ x(t+1) = πᵀ W x(t) = πᵀ x(t); it is the one
thing averaging never changes. The distance to consensus shrinks roughly like |λ_2|^t, where |λ_2| is
the modulus, or absolute value, of the second-largest eigenvalue. Eigenvalues of a nonsymmetric W can
be complex, and the modulus of a + bi is √(a² + b²); for example, 0.3 + 0.4i has modulus 0.5.

**Known and unknown.** W and x(0) are given. The unknowns are π (a linear system: πᵀ (W − I) = 0
together with 1ᵀ π = 1), then c, and |λ_2| for the speed.

**Worked case: three people.** P keeps half their own opinion and takes half from Q. Q keeps half and
takes a quarter each from P and R. R keeps half and takes half from Q. As scalar equations:

```
x_P(t+1) = 1/2 x_P(t) + 1/2 x_Q(t)
x_Q(t+1) = 1/4 x_P(t) + 1/2 x_Q(t) + 1/4 x_R(t)
x_R(t+1) =              1/2 x_Q(t) + 1/2 x_R(t)
```

Row by row, with the columns labeled by whose opinion is being weighted:

```
      P    Q    R
W = [ 1/2  1/2  0   ]    P
    [ 1/4  1/2  1/4 ]    Q
    [ 0    1/2  1/2 ]    R
```

The starting opinions are x(0) = (8, 0, 4), with plain average 4. Iterating by hand:

```
x(0) = (8,    0, 4   )
x(1) = (4,    3, 2   )
x(2) = (3.5,  3, 2.5 )
x(3) = (3.25, 3, 2.75)
x(4) = (3.125, 3, 2.875)
```

The opinions close in on 3, not on 4. To predict the 3, solve πᵀ W = πᵀ. Its first entry reads
π_P = 1/2 π_P + 1/4 π_Q, so π_Q = 2 π_P; its third reads π_R = 1/4 π_Q + 1/2 π_R, so π_Q = 2 π_R.
With π_P + π_Q + π_R = 1 this gives π = (1/4, 1/2, 1/4). Q has the most social power, because both
other people listen to Q. The consensus value is

```
c = πᵀ x(0) = 1/4 × 8 + 1/2 × 0 + 1/4 × 4 = 3
```

which matches the iteration. Every row of W^t tends to πᵀ = (1/4, 1/2, 1/4). The eigenvalues of W are
1, 1/2 and 0, with right eigenvectors 1, (1, 0, −1) and (1, −1, 1). Writing x(0) in that basis,

```
x(0) = 3 (1, 1, 1) + 2 (1, 0, −1) + 3 (1, −1, 1)
```

so for t ≥ 1 the third term is gone and x(t) = 3 1 + 2 (1/2)^t (1, 0, −1): the disagreement halves
every round, exactly |λ_2| = 1/2, as the table shows.

### Matrix structure

W is nonnegative, row-stochastic and [sparse](https://en.wikipedia.org/wiki/Sparse_matrix): each agent listens to a handful of others. It is usually
not [symmetric](https://en.wikipedia.org/wiki/Symmetric_matrix), because trust need not be mutual, so its eigenvalues can be complex and its left and
right eigenvectors differ.

### What is computed

Running the model is [power iteration](https://en.wikipedia.org/wiki/Power_iteration) in the row-stochastic convention: one sparse matrix–vector product
per round.
The influence weights π are computed as the dominant left eigenvector, by power iteration on Wᵀ or a
sparse eigensolver, for example scipy.sparse.linalg.eigs, and |λ_2| by the same solver.

### Why linear algebra is the right tool

Each round is a linear map, so t rounds are the matrix power W^t, and its long-run behavior is read off
the eigenvalues. Perron–Frobenius turns "does the group agree?" into a condition on the graph, and the
left eigenvector gives the agreed value without running a single round.

### Pitfall worth teaching

Strong connectivity alone is not enough. Two people who each listen only to the other swap opinions
forever:

```
W = [ 0  1 ]
    [ 1  0 ]
```

The graph has only cycles of length 2, and W has eigenvalue −1 with modulus 1. Any positive self-weight
removes the oscillation.

A stubborn agent changes the answer completely. If P stops listening, with row P of W set to (1, 0, 0)
and w_PP = 1, then π = (1, 0, 0) and the group converges to P's starting opinion 8, whatever Q and R
think: x(4) = (8, 5.125, 3.9375). It is also slower, because |λ_2| rises to (2 + √2)/4 ≈ 0.854.
Finally, if the trust graph splits into groups that never listen outside themselves, eigenvalue 1 is
repeated, and each group reaches its own consensus.

### Extensions

The [PageRank](https://en.wikipedia.org/wiki/PageRank) entry uses the same Perron vector with the convention transposed: there the matrix is
column-stochastic and the [stationary distribution](https://en.wikipedia.org/wiki/Stationary_distribution) is a right eigenvector, G r = r. Here W is
row-stochastic, and π is a left eigenvector. Read as the transition matrix of a [Markov chain](https://en.wikipedia.org/wiki/Markov_chain), W
moves a walker from agent i to agent j with probability w_ij, and π is its stationary distribution.
The Markov decision processes entry builds on the same row-stochastic transition matrices. When W is also [doubly stochastic](https://en.wikipedia.org/wiki/Doubly_stochastic_matrix), with
columns summing to 1, π = (1/n) 1 and the group reaches the plain mean; this is average consensus, used
in sensor networks. For a symmetric network with graph [Laplacian](https://en.wikipedia.org/wiki/Laplacian_matrix) L (degree matrix minus adjacency
matrix), W = I − ε L with a small enough step ε > 0 is such a matrix, and its |λ_2| is 1 − ε times the
second-smallest eigenvalue of L, the [algebraic connectivity](https://en.wikipedia.org/wiki/Algebraic_connectivity) met in the spectral clustering entry. The
Laplacian also ranks teams in the Massey and Colley entry. Letting the step size shrink to zero gives
continuous-time consensus, the linear ordinary differential equation dx/dt = −L x, which is Tier 3. The
Friedkin–Johnsen model, x(t+1) = Λ W x(t) + (I − Λ) x(0) with Λ a diagonal matrix of susceptibilities
between 0 and 1, keeps each agent partly anchored to their initial view, so disagreement can persist at
equilibrium.

### Terminology

How this field's vocabulary reads as linear algebra.

| Domain term | In linear algebra |
|---|---|
| DeGroot model | the difference equation x(t+1) = W x(t) with W row-stochastic |
| trust (influence) matrix W | row i holds the weights person i gives to each opinion; nonnegative, rows sum to 1 |
| self-weight w_ii | how much person i keeps of their own opinion; a diagonal entry of W |
| consensus | x(t) → c 1, every entry of the opinion vector equal |
| social power (influence weight) π_i | entry i of the left Perron eigenvector, πᵀ W = πᵀ, 1ᵀ π = 1 |
| consensus value c | πᵀ x(0), the π-weighted average of the starting opinions |
| strongly connected trust graph | W irreducible |
| aperiodic | the gcd of the graph's cycle lengths is 1; with strong connectivity, W primitive |
| convergence rate | the second-largest eigenvalue modulus \|λ_2\| of W |
| stubborn agent | a row of W equal to a standard basis vector, w_ii = 1 |
| average consensus | W doubly stochastic (columns also sum to 1), so π = 1/n and c is the plain mean |

---

[Back to the index](/r/LinearAlgebra/wiki/applications)
