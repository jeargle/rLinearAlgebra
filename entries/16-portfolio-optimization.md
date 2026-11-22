---
id: 16
slug: portfolio-optimization
status: written
title: 'Portfolio optimization: minimum-variance weights from one symmetric linear solve'
short_title: Portfolio optimization
field_label: Quantitative finance, investment management, risk management
tier_note: 'risk is the quadratic form wᵀ Σ w of a symmetric positive definite covariance matrix, and
  with equality constraints only the optimal weights solve one linear system. Positive definiteness,
  eigenvectors and condition numbers make the entry Tier 2. A ban on short selling turns it into a
  quadratic program with inequality constraints, whose theory and duality are Tier 3.'
nav_field: Economics, Finance & Operations Research
field: Economics
subfield: Quantitative finance
tier: 2
tier_ceiling: 3
prereq_beyond_la: probability; convex optimization
scalar_field: R
vector_space: 'R^n, one coordinate per asset: a portfolio is a weight vector w, and the budget
  constraint 1ᵀ w = 1 makes the portfolios an affine hyperplane, not a subspace (0 is not a portfolio).
  Without short sales they form the probability simplex, which is not a subspace either. The covariance
  matrix lives in the space of symmetric n × n matrices, inside the cone of positive semidefinite ones'
underlying_equations: 'A statistical model with linear constraints: returns form a random vector with
  mean μ and covariance Σ, so a portfolio has expected return μᵀ w and variance wᵀ Σ w. Minimizing the
  variance subject to 1ᵀ w = 1 and μᵀ w = r gives the linear system 2Σ w + λ_1 1 + λ_2 μ = 0,
  1ᵀ w = 1, μᵀ w = r'
core_la_object: Covariance matrix
la_concepts: positive definiteness; conditioning; shrinkage estimation
primary_method: Quadratic programming
matrix_structure: dense symmetric PSD, ill-conditioned
typical_size: 1e2-1e3 assets
worked_example_size: 3 assets P Q R with Σ = 0.02 × [2 1 0; 1 2 0; 0 0 1] by hand; 2-asset correlation sensitivity and a simulated 50-asset sample covariance from 60 observations
terminology:
  asset: one coordinate of R^n
  weight w_i: fraction of the budget held in asset i, one entry of w
  budget constraint: 1ᵀ w = 1, an affine hyperplane in R^n
  short sale: a negative entry of w
  expected return μ: the mean vector; the portfolio's expected return μᵀ w is a linear function of w
  covariance matrix Σ: 'the symmetric positive semidefinite n × n matrix with entries Σ_ij = E[(x_i − μ_i)(x_j − μ_j)]'
  portfolio variance: the quadratic form wᵀ Σ w
  volatility σ_p: square root of the quadratic form wᵀ Σ w
  diversification: off-diagonal terms with ρ_ij < 1 that make wᵀ Σ w smaller than (w_1 σ_1 + … + w_n σ_n)²
  minimum-variance portfolio: Σ⁻¹ 1 / (1ᵀ Σ⁻¹ 1)
  Lagrange multiplier λ: 'coefficient of a constraint row in 2Σ w + λ_1 1 + λ_2 μ = 0; minus it is the price of the constraint'
  KKT system: 'the symmetric indefinite (n + 2) × (n + 2) block system [2Σ 1 μ; 1ᵀ 0 0; μᵀ 0 0]'
  two-fund theorem: every optimal w lies in the span of Σ⁻¹ 1 and Σ⁻¹ μ
  efficient frontier: minimum variance as a quadratic function of the target return r
  sample covariance S: 'average of outer products of centered return vectors; rank at most T − 1'
  error maximization: inverting the small, noisy eigenvalues of S into large long-short weights
  shrinkage: S + δ I or a blend with a multiple of I, which raises every eigenvalue
---
## Start here

"Don't put all your eggs in one basket." An investor who splits money between two stocks that do not
always move together gets a smoother ride than one who holds either stock alone: when one falls, the
other often does not. How much smoother depends on how the two move together, and the best split can
be calculated.

Portfolio optimization asks the same question for many investments at once: what fraction of the money
should go into each, so that the swings of the whole are as small as possible, either outright or for
a required average return?

When the only rule is that the fractions add up to one, the answer is a single system of linear
equations. The catch is that the inputs are estimated from a limited history, and a naive solve turns
small estimation errors into wild bets.

## The problem

Some vocabulary first. An **asset** is anything held for its changing value, for example a stock, a
bond or a fund. Its **return** over a period is its fractional change in value, for example 0.07 for a
7% gain in a year. Returns are random, and the **expected return** of an asset is E[x], where E[·]
denotes the expected value, the probability-weighted average: a return of 0.10 or 0 with probability
1/2 each has E[x] = 0.05. A **portfolio** splits a budget among n assets with **weights**, the
fractions in each asset, summing to 1; for example (0.5, 0.5) puts half in each of two assets. A
negative weight is a **short sale**: borrowing an asset and selling it, which gains when its price
falls.

**Risk** is measured by the variance of the portfolio's return, or by its square root, the
**volatility**. The **covariance** of two returns measures how they move together: it is the
expected value of the product of their deviations from their means, so it is positive when, for
example, both tend to be above average at the same time. Dividing a covariance by the two volatilities
gives the **correlation**, a number between −1 and 1. All the covariances together form the
**covariance matrix**.

The motivating contrast: a portfolio's return is the weighted average of the asset returns, but its
volatility is less than the weighted average of the volatilities unless the assets are perfectly
correlated. That gap is diversification. The mean-variance problem of modern portfolio theory, posed
by Harry Markowitz in 1952, is to choose the weights with the smallest variance, either under the
budget rule alone (the **minimum-variance portfolio**) or also at a required expected return r. The
expected returns, the covariance matrix and r are given; the weights are solved for. In practice the
covariance matrix is estimated, as the **sample covariance** of T past observations, and that estimate
is where the trouble starts.

## Variables

| Symbol | Name | What it holds | Shape | Units |
|---|---|---|---|---|
| n | number of assets | how many assets can be held | integer | — |
| i, j | asset indices | 1, …, n; in the worked case P, Q, R are assets 1, 2, 3 | integer | — |
| x | return vector | entry i is the random return x_i of asset i over one period | n × 1 | fraction per year |
| E[·] | expected value | probability-weighted average of a random quantity | operator | units of its argument |
| μ | expected-return vector | entry i is μ_i = E[x_i] | n × 1 | fraction per year |
| σ_i | volatility of asset i | standard deviation of x_i | scalar ≥ 0 | fraction per year |
| ρ_ij | correlation | how x_i and x_j move together, between −1 and 1 | scalar | dimensionless |
| Σ | covariance matrix | entry Σ_ij = E[(x_i − μ_i)(x_j − μ_j)] = ρ_ij σ_i σ_j; diagonal Σ_ii = σ_i² | n × n | (fraction per year)² |
| w | weight vector | entry w_i is the fraction of the budget in asset i; negative means short | n × 1 | dimensionless |
| 1 | all-ones vector | 1ᵀ w = w_1 + … + w_n | n × 1 | — |
| σ_p² | portfolio variance | variance of the portfolio return wᵀ x | scalar | (fraction per year)² |
| r | target return | required expected return of the portfolio | scalar | fraction per year |
| w_mv | minimum-variance weights | the weights with the smallest variance under the budget rule alone | n × 1 | dimensionless |
| λ_1, λ_2 | Lagrange multipliers | one number per constraint: budget, then target return | scalars | (fraction per year)² per unit of constraint |
| d | direction of change | a small change in the weights | n × 1 | dimensionless |
| M | constraint-augmented matrix | the block matrix of the linear system for w, λ_1 and λ_2 | (n + 2) × (n + 2) | mixed |
| T | number of observations | past periods of return data | integer | — |
| x_t, m | observed returns, sample mean | return vector in period t, and the average of x_1, …, x_T | n × 1 | fraction per year |
| S | sample covariance matrix | (1/(T − 1)) × sum over t of (x_t − m)(x_t − m)ᵀ | n × n | (fraction per year)² |
| δ | shrinkage amount | amount added to every eigenvalue of S | scalar ≥ 0 | (fraction per year)² |
| κ | condition number | largest eigenvalue divided by smallest, for a symmetric positive definite matrix | scalar ≥ 1 | dimensionless |
| I | identity matrix | | n × n | — |

## Formulation

**Where the equations come from.** A statistical model: the returns form a random vector x with mean μ
and covariance Σ, and nothing else about their distribution is used.

**The familiar formula.** For two assets, every finance course gives the portfolio variance as

```
σ_p² = w_1² σ_1² + w_2² σ_2² + 2 w_1 w_2 ρ_12 σ_1 σ_2
```

For example, with σ_1 = σ_2 = 0.20, ρ_12 = 0 and a half-and-half split,
σ_p² = 0.25 × 0.04 + 0.25 × 0.04 = 0.02, so the volatility falls from 0.20 to about 0.141. With
ρ_12 = 0.5 the last term adds 0.01 and σ_p ≈ 0.173.

**One entry, then the matrix.** Since σ_i² = Σ_ii and ρ_12 σ_1 σ_2 = Σ_12 = Σ_21, the formula reads
w_1 Σ_11 w_1 + w_1 Σ_12 w_2 + w_2 Σ_21 w_1 + w_2 Σ_22 w_2: each ordered pair of assets (i, j)
contributes w_i Σ_ij w_j. For n assets the variance is the sum of those n² terms, the quadratic form

```
σ_p² = wᵀ Σ w,    expected return = μᵀ w,    budget: 1ᵀ w = 1
```

**Why Σ is positive semidefinite.** For any vector w, wᵀ Σ w is the variance of the random number
wᵀ x, and a variance is never negative, so Σ is positive semidefinite. It is positive definite unless
some nonzero combination of assets has zero variance, for example the same fund listed twice, where
w = (1, −1) cancels exactly. Assume Σ is positive definite, so it is invertible.

**Minimum variance.** Minimize wᵀ Σ w subject to 1ᵀ w = 1. The gradient of wᵀ Σ w, its vector of
partial derivatives, is 2Σ w (for one asset, the derivative of σ² w² is 2σ² w). At the best w, no
small budget-keeping change d (one with 1ᵀ d = 0) can lower the variance to first order, so 2Σ w is
orthogonal to the null space of 1ᵀ and lies in its row space, the multiples of 1. Hence
2Σ w + λ_1 1 = 0 for some number λ_1, called a Lagrange multiplier. Minus λ_1 is how fast the smallest
achievable variance rises as the constraint's right-hand side rises, so it acts as the constraint's
price. Solving and scaling w to sum to 1 gives

```
w_mv = Σ⁻¹ 1 / (1ᵀ Σ⁻¹ 1),    minimum variance = 1 / (1ᵀ Σ⁻¹ 1)
```

**Adding a target return.** With the second constraint μᵀ w = r, the same argument gives
2Σ w + λ_1 1 + λ_2 μ = 0. Stacked with the two constraints, this is one square system,
M × unknowns = knowns:

```
[ 2Σ   1   μ ]   [ w   ]   [ 0 ]
[ 1ᵀ   0   0 ] × [ λ_1 ] = [ 1 ]
[ μᵀ   0   0 ]   [ λ_2 ]   [ r ]
```

It is called the Karush–Kuhn–Tucker (KKT) system, after the optimality conditions it expresses. Its
first block row says w = −(λ_1/2) Σ⁻¹ 1 − (λ_2/2) Σ⁻¹ μ, so every optimal portfolio is a combination
of Σ⁻¹ 1 and Σ⁻¹ μ: the two-fund theorem. The minimum variance is a quadratic function of r, and the
upper half of its curve, plotted as volatility against r, is the efficient frontier: no other
portfolio gives more return for its risk.

**Worked case: three assets.** Assets P and Q each have volatility 0.20 and correlation 0.5, so their
covariance is 0.5 × 0.20 × 0.20 = 0.02. Asset R has variance 0.02 (volatility ≈ 0.141) and is
uncorrelated with both. The expected returns are 0.09, 0.06 and 0.05. With weights w_1, w_2, w_3 on P,
Q, R, the variance is

```
σ_p² = 0.04 w_1² + 0.04 w_2² + 0.02 w_3² + 2 × 0.02 w_1 w_2
```

and the given data, in matrix form, are

```
      P      Q      R
Σ = [ 0.04   0.02   0    ]   P
    [ 0.02   0.04   0    ]   Q
    [ 0      0      0.02 ]   R

μ = [ 0.09 ]
    [ 0.06 ]
    [ 0.05 ]
```

so Σ = 0.02 × [2 1 0; 1 2 0; 0 0 1]. For the minimum-variance portfolio, solve Σ z = 1 for z = Σ⁻¹ 1
rather than inverting Σ:

```
0.04 z_1 + 0.02 z_2            = 1
0.02 z_1 + 0.04 z_2            = 1
                      0.02 z_3 = 1
```

so z_1 = z_2 = 50/3 and z_3 = 50. Their sum is 1ᵀ Σ⁻¹ 1 = 250/3, so w_mv = (0.2, 0.2, 0.6), with
variance 3/250 = 0.012 (check: 0.04 × 0.04 + 0.04 × 0.04 + 0.02 × 0.36 + 2 × 0.02 × 0.04 = 0.012),
volatility ≈ 0.110, below every single asset's, and expected return 0.06.

To require r = 0.07 instead, the five scalar equations in w_1, w_2, w_3, λ_1, λ_2 are

```
0.08 w_1 + 0.04 w_2            + λ_1 + 0.09 λ_2 = 0
0.04 w_1 + 0.08 w_2            + λ_1 + 0.06 λ_2 = 0
                      0.04 w_3 + λ_1 + 0.05 λ_2 = 0
     w_1 +      w_2 +      w_3                  = 1
0.09 w_1 + 0.06 w_2 + 0.05 w_3                  = 0.07
```

or M × unknowns = knowns:

```
[ 0.08   0.04   0      1   0.09 ]   [ w_1 ]   [ 0    ]
[ 0.04   0.08   0      1   0.06 ]   [ w_2 ]   [ 0    ]
[ 0      0      0.04   1   0.05 ] × [ w_3 ] = [ 0    ]
[ 1      1      1      0   0    ]   [ λ_1 ]   [ 1    ]
[ 0.09   0.06   0.05   0   0    ]   [ λ_2 ]   [ 0.07 ]
```

The solution is w = (17/35, 2/35, 16/35) ≈ (0.486, 0.057, 0.457), λ_1 = 9/875 ≈ 0.0103 and
λ_2 = −4/7 ≈ −0.571. The weights sum to 1, the return is (9 × 17 + 6 × 2 + 5 × 16)/3500 = 0.07, and
the variance is 13/875 ≈ 0.0149. With Σ⁻¹ μ = (2, 1/2, 5/2), w = −(9/1750) Σ⁻¹ 1 + (2/7) Σ⁻¹ μ, as the
two-fund theorem promises. The minimum variance is (200/7) r² − (24/7) r + 201/1750, lowest at
r = 0.06, with slope 4/7 = −λ_2 at r = 0.07: there each extra 0.01 of return costs about 0.0057 of
variance.

## Matrix structure

Σ is dense, symmetric and positive definite: every pair of assets has a covariance. M is symmetric but
indefinite, with n positive and 2 negative eigenvalues (3 and 2 in the worked case), the pattern of a
saddle-point matrix. Cholesky factorization therefore applies to Σ but not to M. Estimated covariance
matrices of many assets are badly conditioned.

## What is computed

Factor Σ = L Lᵀ by Cholesky (L lower triangular) and get Σ⁻¹ 1 and Σ⁻¹ μ by triangular solves; Σ⁻¹ is
never formed. The whole frontier then depends on three numbers, 1ᵀ Σ⁻¹ 1, 1ᵀ Σ⁻¹ μ and μᵀ Σ⁻¹ μ
(250/3, 5 and 67/200 in the worked case). Production problems add inequality constraints and are
solved by active-set or interior-point methods, which solve a system like M at every step.

## Why linear algebra is the right tool

Variance is a quadratic form and the constraints are linear, so the optimality conditions are a linear
system. The spectral theorem shows what the solution does. Writing Σ through its eigenvectors,
Σ⁻¹ divides the component of 1 along each eigenvector by that eigenvalue, so the
minimum-variance portfolio leans hardest on the quietest directions. In the worked case,
1 = (1, 1, 0) + (0, 0, 1) splits into an eigenvector of Σ with eigenvalue 0.06 and one with eigenvalue
0.02, so R's weight is 0.06/0.02 = 3 times that of P or Q: 0.6 against 0.2.

## Pitfall worth teaching

The same division by small eigenvalues goes wrong in practice. Take two assets with volatilities 0.20
and 0.25. The minimum-variance weight on the first is
(σ_2² − ρ_12 σ_1 σ_2)/(σ_1² + σ_2² − 2ρ_12 σ_1 σ_2). At ρ_12 = 0.90 the weights are (1.4, −0.4); at
ρ_12 = 0.95 they are (0.015/0.0075, −1) = (2, −1). A change in correlation too small for a realistic
sample to resolve moves 60% of the budget. The smallest eigenvalue of Σ at ρ_12 = 0.95 is about
0.0024, with eigenvector ≈ (−0.78, 0.62), a long-short spread between the two assets, and the
condition number κ rises from about 20 to 41.

With many assets the sample covariance S is the culprit. It is a sum of T outer products of the
centered vectors x_t − m, which sum to zero, so its rank is at most T − 1, and for n ≥ T it is
singular. In one simulation with n = 50 independent assets of volatility 0.20 and T = 60 observations,
the true optimum is equal weights of 0.02, with variance 0.0008. The eigenvalues of S, all 0.04 in
truth, ranged from about 0.00022 to 0.147, so κ ≈ 680. The weights computed from S ranged from −0.127
to 0.169, and the cosine of the angle between them and the eigenvector of the smallest eigenvalue was
0.84. Their variance was 0.00013 on the sample but 0.0073 on the true Σ, about 9 times the optimum.
The optimizer seeks out the directions where the estimate is most wrong, so Richard Michaud called
mean-variance optimization "error maximization".

The fix is shrinkage: replace S by S + δ I, which adds δ to every eigenvalue and leaves the
eigenvectors alone. With δ = 0.04 in the simulation, κ fell to 4.6, the weights ranged from 0.003 to
0.037, and the true variance was 0.00093, within 17% of the optimum. The Ledoit–Wolf estimator blends
S with a multiple of I, choosing the blend weight from the data.

## Extensions

Banning short sales adds the constraint w ≥ 0, where ≥ between vectors means entrywise:
(0.2, 0, 0.8) ≥ 0, but (1.4, −0.4) is not. The problem becomes a quadratic program with
inequality constraints, whose theory, with duality, is Tier 3. On that optimization ladder the
linear programming entry is the rung below, and the distance geometry entry, for NMR
(nuclear magnetic resonance) structures, the rung above, optimizing over positive semidefinite
matrices. Adding a risk-free asset turns the frontier into a straight line through the portfolio with
the largest Sharpe ratio, which leads to the capital asset pricing model.

Factor models write Σ as a low-rank matrix plus a diagonal one, which cuts the number of estimated
entries. The leading eigenvector of a stock covariance matrix is usually close to equal weights, the
market as a whole, the same covariance eigenstructure read in the population genetics PCA
(principal component analysis) entry and the latent semantic analysis entry. The minimum-variance
weights can also be computed by a least-squares regression of one asset's return on its differences
from the others, which links this entry to the regression entry. Expected returns are even harder to
estimate than covariances, which motivates the Black–Litterman model.
