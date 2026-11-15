# Markov decision processes: valuing a policy with one linear solve

### Start here

A machine earns money while it runs, sometimes breaks down, and costs money to repair. Is a repair
worth paying for? The answer depends on what the machine will earn afterward, and that depends on
how it will be handled later, including what happens the next time it breaks.

Problems of this shape, where each choice changes what can happen next, are planned
with [Markov decision processes](https://en.wikipedia.org/wiki/Markov_decision_process). They describe a robot moving through a building, a game-playing program, an
inventory manager or a medical treatment plan, and they are the setting of [reinforcement learning](https://en.wikipedia.org/wiki/Reinforcement_learning).

The central question is how much a fixed rule for choosing ("always repair") is worth from each
starting situation. Money now counts for more than money later, and with that one assumption the
question has an exact answer: one system of linear equations. Finding the best rule then alternates
two steps: work out what the current rule is worth, then switch, wherever it helps, to a better choice.

**Field:** Reinforcement learning, operations research, sequential decision-making  
**Tier:** 2 — the value of a fixed policy solves (I − γ P_π) v = r_π, whose matrix is invertible because γ P_π has [spectral radius](https://en.wikipedia.org/wiki/Spectral_radius) γ < 1. That is a statement about the [eigenvalues](https://en.wikipedia.org/wiki/Eigenvalues_and_eigenvectors) of a [stochastic matrix](https://en.wikipedia.org/wiki/Stochastic_matrix), so the entry is Tier 2. [Contraction](https://en.wikipedia.org/wiki/Contraction_mapping)-mapping proofs, stochastic-process theory and the convergence of [Q-learning](https://en.wikipedia.org/wiki/Q-learning) are Tier 3.  
**Scalar field:** R  
**Vectors:** R^n, one coordinate per state: a value function v is a vector in R^n. A policy is not a vector but a choice of action in each state, so the deterministic policies form a finite set, not a subspace. Each row of P_π is a probability distribution over next states and lies in the probability simplex, which is not a subspace either  
**Underlying equations:** A linear recurrence on expected rewards for a controlled discrete-time Markov chain: the [Bellman expectation equation](https://en.wikipedia.org/wiki/Bellman_equation) v_π = r_π + γ P_π v_π for a fixed policy, and the Bellman optimality equation v∗(s) = max_a [ r(s, a) + γ Σ_s' p(s'|s, a) v∗(s') ], which has a max and is not linear

### The problem

A Markov decision process (MDP) is a model of repeated decisions under uncertainty. At each time step
the system is in one of n states, for example "working" or "broken". The decision-maker, called the
agent, picks an action available in that state, for example "repair" or "wait". The action earns an
immediate reward, possibly negative (a cost), and the system moves to a random next state with
probabilities that depend only on the current state and action. That last property is
the [Markov property](https://en.wikipedia.org/wiki/Markov_property): the past matters only through the present state.

A policy is a rule giving one action for each state. The motivating contrast is between immediate and
long-run reward: a greedy agent picks the largest reward now, while a planning agent accepts a cost now
(a repair) for larger rewards later. Two problems follow. Policy evaluation: given a policy, compute
its value in each state, the expected total of discounted future rewards. Policy optimization: find the
policy whose value is largest in every state. The rewards, probabilities and discount factor are
known; the values are the unknowns.

### Variables

| Symbol | Name | What it holds | Shape | Units |
|---|---|---|---|---|
| n | number of states | how many situations the system can be in | integer | — |
| s, s' | state, next state | indices 1, …, n | integer | — |
| a | action | a choice available in state s | label | — |
| p(s'\|s, a) | transition probability | probability of moving to s' after action a in state s | scalar in [0, 1] | dimensionless |
| r(s, a) | reward | immediate payoff of action a in state s | scalar | reward units (e.g. dollars per step) |
| γ | discount factor | weight on the next step's value, 0 < γ < 1 | scalar | dimensionless |
| π | policy | the action π(s) chosen in each state | list of n actions | — |
| P_π | transition matrix of π | entry (s, s') is p(s'\|s, π(s)); each row sums to 1 | n × n | dimensionless |
| r_π | reward vector of π | entry s is r(s, π(s)) | n × 1 | reward units |
| v_π | value function of π | entry s is the expected discounted total reward starting from s | n × 1 | reward units |
| I | identity matrix | | n × n | — |
| t | time step | steps since the start | integer | — |
| q(s, a) | action value | value of taking a in s once, then following the current policy | scalar | reward units |
| v∗ | optimal value function | the largest achievable value in each state | n × 1 | reward units |
| v_k | value-iteration iterate | estimate of v∗ after k sweeps, with v_0 = 0 | n × 1 | reward units |

### Formulation

**Where the equations come from.** The model is a Markov chain whose transitions the agent controls.
Fixing a policy removes the choices and leaves an ordinary Markov chain with stochastic matrix P_π,
the row-stochastic version of the matrix in the [PageRank](https://en.wikipedia.org/wiki/PageRank) entry. The equations are accounting
identities for expected rewards.

**The familiar formula.** Anyone who has compared loans knows [present value](https://en.wikipedia.org/wiki/Present_value): a payment c_t received t
years from now, at interest rate i per year, is worth c_t / (1 + i)^t today. Writing γ = 1 / (1 + i),
the present value of a stream of payments is Σ_t γ^t c_t. The discount factor γ plays exactly this
role, with rewards in place of payments: γ = 0.9 corresponds to i ≈ 11% per step. An equivalent
reading is that the process ends after each step with probability 1 − γ.

**One state.** In state s, the policy takes action π(s), earns r(s, π(s)) now, and moves to state s'
with probability p(s'|s, π(s)). Everything after that is worth v_π(s') from the next step on, discounted
once by γ:

```
v_π(s) = r(s, π(s)) + γ Σ_s' p(s'|s, π(s)) v_π(s')
```

This is the Bellman expectation equation for one state: value now equals reward now plus the
discounted expected value of where the system goes.

**All states at once.** Stacking the n equations gives one linear system:

```
v_π = r_π + γ P_π v_π,    or    (I − γ P_π) v_π = r_π
```

The known quantities are P_π and r_π, read off the model once the policy is fixed; v_π is solved for.
The matrix is always invertible. Every row of P_π is a probability distribution, so P_π has eigenvalue
1 (with the all-ones vector) and, because no eigenvalue can exceed the largest row sum, none larger
than 1 in absolute value. The spectral radius of γ P_π is therefore γ < 1, so 1 is not an
eigenvalue of γ P_π, and the [Neumann series](https://en.wikipedia.org/wiki/Neumann_series) converges:

```
v_π = (I − γ P_π)⁻¹ r_π = r_π + γ P_π r_π + γ² P_π² r_π + …
```

Row s of P_π^t is the distribution of the state t steps after starting in s, so term t is the expected
reward at step t, discounted t times. The series restates the definition of value: the expected
discounted sum of rewards.

**Improvement, the one nonlinear step.** Given v_π, the action value of each action a in state s is

```
q(s, a) = r(s, a) + γ Σ_s' p(s'|s, a) v_π(s')
```

The improved policy picks, in each state, the action with the largest q(s, a). The max of a list is its
largest entry, and the argmax is the position where it occurs: for the list (repair: 1/3, wait: 0) the
max is 1/3 and the argmax is repair. Policy iteration alternates evaluation (a linear solve) and
improvement (an argmax per state) until the policy stops changing. Each improved policy is at least as
good in every state, and with finitely many policies the loop ends.

**The optimal value.** At that point v∗ satisfies the Bellman optimality equation, stated here but
not solved as a linear system, because the max makes it nonlinear:

```
v∗(s) = max_a [ r(s, a) + γ Σ_s' p(s'|s, a) v∗(s') ]
```

**Worked case: a machine.** Let state 1 be working and state 2 be broken, with γ = 1/2. A working
machine has one action, run: reward 2, and next step it is working or broken with probability 1/2 each.
A broken machine has two actions: repair, reward −1 (a cost), after which it is working; or wait,
reward 0, after which it is still broken. There are two policies, "wait" and "repair", named by the
choice in the broken state.

For the repair policy, the two Bellman equations in v_1 and v_2 are

```
v_1 = 2 + (1/2)(1/2 v_1 + 1/2 v_2)
v_2 = −1 + (1/2)(v_1)
```

with the transition matrix and reward vector

```
                 working  broken
P_repair     = [ 1/2      1/2 ]    working
               [ 1        0   ]    broken

r_repair     = [ 2  ]
               [ −1 ]
```

so (I − γ P_π) v = r_π reads

```
[ 3/4    −1/4 ]   [ v_1 ]   [ 2  ]
[ −1/2   1    ] × [ v_2 ] = [ −1 ]
```

The [determinant](https://en.wikipedia.org/wiki/Determinant) is 3/4 − 1/8 = 5/8, and v_repair = (14/5, 2/5) = (2.8, 0.4). The eigenvalues of
γ P_repair are 1/2 and −1/4, so the spectral radius is γ, as promised. The first Neumann partial sums
are (2, −1), then (2.25, 0), then (2.5625, 0.125), approaching (2.8, 0.4).

For the wait policy, P_wait has rows (1/2, 1/2) and (0, 1), and r_wait = (2, 0). The system is

```
[ 3/4   −1/4 ]   [ v_1 ]   [ 2 ]
[ 0     1/2  ] × [ v_2 ] = [ 0 ]
```

so v_2 = 0 and v_wait = (8/3, 0) ≈ (2.667, 0). Starting policy iteration from wait, the improvement
step compares the two actions in the broken state using v_wait:

```
q(broken, repair) = −1 + (1/2)(8/3) = 1/3
q(broken, wait)   =  0 + (1/2)(0)   = 0
```

The argmax is repair. Evaluating repair gives (2.8, 0.4), larger in both states. Improving again
gives q(broken, repair) = −1 + (1/2)(2.8) = 0.4 against q(broken, wait) = (1/2)(0.4) = 0.2, so repair
stays and policy iteration stops: v∗ = (2.8, 0.4).

**Value iteration.** Instead of solving, repeat
v_(k+1)(s) = max_a [ r(s, a) + γ Σ_s' p(s'|s, a) v_k(s') ] from v_0 = 0. Each sweep is a multiplication
by γ times a stochastic matrix plus a max per row, like the [power iteration](https://en.wikipedia.org/wiki/Power_iteration) of the PageRank entry.
For the machine, v_1 = (2, 0), v_2 = (2.5, 0), v_3 = (2.625, 0.25)
and v_8 ≈ (2.795, 0.395). The largest error at least halves each sweep, a factor of γ.

### Matrix structure

P_π is row-stochastic and [sparse](https://en.wikipedia.org/wiki/Sparse_matrix): from any state only a few next states are possible. I − γ P_π is
strictly [diagonally dominant](https://en.wikipedia.org/wiki/Diagonally_dominant_matrix) by rows (its diagonal entry 1 − γ p(s|s, π(s)) exceeds the sum of the
other entries' sizes), so [Jacobi](https://en.wikipedia.org/wiki/Jacobi_method) and [Gauss–Seidel](https://en.wikipedia.org/wiki/Gauss%E2%80%93Seidel_method) iterations converge on it. Its inverse is entrywise
nonnegative, so larger rewards never lower any value.

### What is computed

For up to about 10⁴ states, policy evaluation is a sparse direct solve. For more, it is iterative:
repeated application of v ← r_π + γ P_π v, a few sweeps per evaluation (modified policy iteration),
or value iteration throughout. Policy iteration typically stops after a handful of improvements;
value iteration needs about log(10) / log(1/γ) sweeps per extra decimal digit of accuracy, about 22
at γ = 0.9, so γ near 1 is slow, just as a damping factor near 1 slows PageRank.

### Why linear algebra is the right tool

Once a policy is fixed, value is a linear function of the rewards: v_π = (I − γ P_π)⁻¹ r_π. Its
existence, uniqueness and series form all come from one spectral fact, that γ P_π has spectral radius
γ < 1. The only nonlinearity in planning is the per-state argmax, and policy iteration isolates it
between exact linear solves.

### Pitfall worth teaching

The discount factor is a modeling choice, not a numerical detail, and it can change the decision. In
the machine example with γ = 1/4, v_wait = (16/7, 0) and q(broken, repair) = −1 + (1/4)(16/7) = −3/7,
which is less than 0, so waiting, that is abandoning the machine, is optimal. At γ = 9/10, repair wins
by a wide margin, with v_repair = (310/29, 250/29) ≈ (10.69, 8.62). A second trap is setting γ = 1 for
a task that never ends: I − P_π is then singular, since P_π has eigenvalue 1, and the value is
infinite or undefined.

### Extensions

Q-learning estimates the action values q(s, a) from observed transitions without knowing p or r; it is
the basic method of reinforcement learning, and its convergence proof uses stochastic approximation,
which is Tier 3. Value iteration converges because the Bellman optimality map is a contraction mapping
in the max norm with constant γ, which the [Banach fixed-point theorem](https://en.wikipedia.org/wiki/Banach_fixed-point_theorem) turns into existence and
uniqueness of v∗. The optimal value is also the solution of a [linear program](https://en.wikipedia.org/wiki/Linear_programming): minimize Σ_s v(s)
subject to v(s) ≥ r(s, a) + γ Σ_s' p(s'|s, a) v(s') for every state and action, and the dual
variables are discounted state-action visit frequencies. For huge state spaces, v is approximated by
a weighted sum of a few chosen features of the state; [least-squares](https://en.wikipedia.org/wiki/Least_squares) [temporal-difference learning](https://en.wikipedia.org/wiki/Temporal_difference_learning)
(LSTD) then solves a small linear system for the weights, and deep reinforcement learning replaces
the weighted sum by a neural network.
Average-reward MDPs drop the discount and use the [stationary distribution](https://en.wikipedia.org/wiki/Stationary_distribution) of P_π, the Perron vector
of the PageRank entry. The consensus and opinion dynamics entry iterates a row-stochastic matrix with
no rewards, and the spectral clustering entry reads structure from the eigenvectors of a related
graph matrix.

### Terminology

How this field's vocabulary reads as linear algebra.

| Domain term | In linear algebra |
|---|---|
| state s | one of the n situations the system can be in, an index into R^n |
| action a | a choice available in a state |
| transition probability p(s'\|s, a) | entry of the stochastic matrix for action a |
| reward r(s, a) | the immediate payoff, one entry of the vector r_π once a policy is fixed |
| discount factor γ | the weight on the next step's value; it scales P_π and sets the spectral radius |
| policy π | a choice of one action per state, which picks one row of P and r for each state |
| transition matrix P_π | the n × n row-stochastic matrix of the Markov chain the policy induces |
| value function v_π | the solution of (I − γ P_π) v = r_π |
| Bellman expectation equation | the fixed-point form v = r_π + γ P_π v of that linear system |
| policy evaluation | solving the linear system, directly or by iteration |
| policy improvement | the argmax over actions, row by row; the one nonlinear step |
| action value q(s, a) | r(s, a) + γ (row of P for action a) · v |
| value iteration | repeated multiplication by γ P with a max per row, like power iteration |
| Bellman optimality equation | v∗ = max over actions of the same affine map; a fixed point, not a linear system |

---

[Back to the index](/r/LinearAlgebra/wiki/applications)
