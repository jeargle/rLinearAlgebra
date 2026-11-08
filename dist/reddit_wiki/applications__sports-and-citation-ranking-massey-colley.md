# Massey and Colley ratings: ranking teams by least squares on the schedule

### Start here

In leagues where every team plays every other team the same number of times, the standings table is a
fair ranking. College sports are different. In American [college football](https://en.wikipedia.org/wiki/College_football), more than a hundred teams
in the top division play about twelve games each, mostly within their own conference. A team that wins
every game against weak opponents may be worse than one that lost once to a strong one. The standings
cannot tell, and for years a national championship depended on how computer rankings settled the
question.

Kenneth Massey's idea, in his 1997 undergraduate honours thesis, was to give every team a single
rating and ask that the difference of two teams' ratings predict the margin when they meet. With more
games than teams, no ratings fit every result exactly, so the method chooses the ratings that fit best
in the [least-squares](https://en.wikipedia.org/wiki/Least_squares) sense. Wesley Colley's method uses only wins and losses. Both were among the
computer rankings used in college football's [Bowl Championship Series](https://en.wikipedia.org/wiki/Bowl_Championship_Series).

The same calculation ranks anything that is compared in pairs: players in chess or tennis, products in
taste tests, or journals by how often they cite each other. The linear algebra also shows exactly when
a schedule is too thin to rank two teams against each other at all.

**Field:** Sports analytics, college football and basketball rankings, ranking from pairwise comparisons  
**Tier:** 1 — Massey's method is least squares with one equation per game, and its normal-equations matrix is built from the schedule, [rank-deficient](https://en.wikipedia.org/wiki/Rank_%28linear_algebra%29) by one for every separate group of teams. Colley's method adds 2I to the same matrix and becomes invertible. Ranking by [eigenvectors](https://en.wikipedia.org/wiki/Eigenvalues_and_eigenvectors) instead, as in [PageRank](https://en.wikipedia.org/wiki/PageRank), is Tier 2.  
**Scalar field:** R  
**Vectors:** R^T, one rating per team, and R^G, one observed margin per game. Ratings enter only through differences, so the constant vector is in the [null space](https://en.wikipedia.org/wiki/Kernel_%28linear_algebra%29) of the [design matrix](https://en.wikipedia.org/wiki/Design_matrix), with one more null direction for each group of teams that never plays the rest  
**Underlying equations:** A statistical model for each game: rating of winner − rating of loser = margin of victory + noise (Massey); Colley replaces margins with wins and losses and adds a prior that every team starts at 1/2

### The problem

There are T **teams** and G **games**. Each game has a winner, a loser and a **margin of victory**,
the winner's points minus the loser's. The **schedule graph** has the teams as nodes and a line for
each game. Its structure decides what can be learned: if two groups of teams never play each other,
nothing in the results compares them.

The known quantities are the schedule and the margins. The unknowns are T **ratings**, one per team,
chosen so that the rating difference of the two teams in each game predicts its margin. Find the
ratings that fit best, decide what fixes their overall level, and decide when the schedule makes them
meaningless.

### Variables

| Symbol | Name | What it holds | Shape | Units |
|---|---|---|---|---|
| T | number of teams | columns of A | integer | — |
| G | number of games | rows of A | integer | — |
| r | ratings | r_i for team i | T × 1 | points (Massey) or win fraction (Colley) |
| y | margins | margin of victory in each game | G × 1 | points |
| A | game matrix | +1 for the winner, −1 for the loser in each row | G × T | — |
| M | Massey matrix | M = AᵀA | T × T | games |
| p | point differentials | p = Aᵀ y, points scored minus allowed per team | T × 1 | points |
| e | residuals | e = y − A r, how much each game beat the prediction | G × 1 | points |
| n_i | games played | diagonal of M | number per team | games |
| w_i, l_i | wins and losses | per team | numbers | games |
| C | Colley matrix | C = 2I + M | T × T | games |
| b | Colley right-hand side | b_i = 1 + (w_i − l_i)/2 | T × 1 | games |
| 1 | ones vector | all entries 1 | T × 1 | — |

### Formulation

**Where the equations come from.** The model is a statistical one: in each game,

```
rating of winner  −  rating of loser  =  margin of victory  +  noise
```

**One game.** If team i beat team j by y points, the game contributes the equation r_i − r_j = y. As a
row of the system, it has +1 in column i, −1 in column j and 0 elsewhere, the same pattern as one
resistor in the resistor-network entry or one [levelling](https://en.wikipedia.org/wiki/Levelling) run in the geodetic entry.

**All the games.** Stacking the rows gives A r ≈ y, with more equations than unknowns. Least squares
chooses r to minimize the sum of squared residuals, and the normal equations are

```
AᵀA r = Aᵀ y,       that is,       M r = p
```

Both sides have a meaning. M has the number of games each team played, n_i, on its diagonal, and minus
the number of meetings between teams i and j off it. It is the [Laplacian](https://en.wikipedia.org/wiki/Laplacian_matrix) of the schedule graph, the
matrix of the resistor-network entry with every conductance equal to 1. p_i is team i's **point
differential**. Row i of M r = p reads n_i r_i − (sum of its opponents' ratings) = p_i: a team's rating
is its average margin plus the average rating of the teams it played, so [strength of schedule](https://en.wikipedia.org/wiki/Strength_of_schedule) is built
in.

**The null space.** Every row of A has one +1 and one −1, so A 1 = 0: adding the same number to every
rating changes no prediction. M is singular, and the ratings are determined only up to a common shift.
This is the [datum](https://en.wikipedia.org/wiki/Geodetic_datum) defect of the geodetic entry. Massey's fix is to replace the last equation of M r = p
by the constraint that the ratings add up to zero.

**Worked case: four teams, five games.** Teams P, Q, R and S played five games:

| Game | Winner | Loser | Margin |
|---|---|---|---|
| 1 | P | Q | 2 |
| 2 | Q | R | 3 |
| 3 | R | S | 1 |
| 4 | P | R | 6 |
| 5 | S | Q | 1 |

As scalar equations, with the ratings r_P, r_Q, r_R, r_S as the unknowns,

```
r_P − r_Q = 2
r_Q − r_R = 3
r_R − r_S = 1
r_P − r_R = 6
r_S − r_Q = 1
```

and as a matrix product,

```
[ 1  −1   0   0 ]            [ 2 ]
[ 0   1  −1   0 ] [ r_P ]    [ 3 ]
[ 0   0   1  −1 ] [ r_Q ] ≈  [ 1 ]
[ 1   0  −1   0 ] [ r_R ]    [ 6 ]
[ 0  −1   0   1 ] [ r_S ]    [ 1 ]
```

The five equations are inconsistent. Around the loop Q → R → S → Q they add up to 0 = 5. The normal
equations, with the last row replaced by the sum constraint, are

```
[  2  −1  −1   0 ] [ r_P ]   [  8 ]
[ −1   3  −1  −1 ] [ r_Q ] = [  0 ]
[ −1  −1   3  −1 ] [ r_R ]   [ −8 ]
[  1   1   1   1 ] [ r_S ]   [  0 ]
```

The first three rows are rows of M: P played two games, Q and R three each. The right side holds the
point differentials, 2 + 6 = 8 for P and −3 + 1 − 6 = −8 for R. The solution is r = (3, 0, −2, −1), so the
ranking is P, Q, S, R. The residuals e = y − A r are (−1, 1, 2, 1, 2). S beat Q by 1, yet Q is rated above
S, because Q's other results, against P and R, were better than S's.

**Colley's method.** Colley ignores margins and uses only wins and losses. His ratings solve

```
C r = b,       C = 2I + M,       b_i = 1 + (w_i − l_i)/2
```

which comes from starting every team at a rating of 1/2 and adjusting for results and opponents. Each
diagonal entry of C exceeds the sum of the sizes of the other entries in its row, so C is invertible
with no constraint needed, and the ratings always average exactly 1/2. For the worked case,
b = (2, 0.5, 0.5, 1), and

```
[  4  −1  −1   0 ] [ r_P ]   [ 2   ]
[ −1   5  −1  −1 ] [ r_Q ] = [ 0.5 ]          so   r = (17/24, 5/12, 5/12, 11/24)
[ −1  −1   5  −1 ] [ r_R ]   [ 0.5 ]
[  0  −1  −1   4 ] [ r_S ]   [ 1   ]
```

that is, about (0.708, 0.417, 0.417, 0.458). Colley ranks S above Q, the opposite of Massey. Without
margins, Q's record is one win and two losses, S's is one of each, and S beat Q. With margins, Q's
narrow loss to the strongest team and its 3-point win over R count in its favour.

### Matrix structure

A has two nonzeros per row. M is [symmetric](https://en.wikipedia.org/wiki/Symmetric_matrix), [positive semidefinite](https://en.wikipedia.org/wiki/Definite_matrix) and as [sparse](https://en.wikipedia.org/wiki/Sparse_matrix) as the schedule: one
off-diagonal entry per pair of teams that met. Its null space has one dimension for each connected
piece of the schedule graph. C = 2I + M is symmetric positive definite and strictly
[diagonally dominant](https://en.wikipedia.org/wiki/Diagonally_dominant_matrix), so [Cholesky factorization](https://en.wikipedia.org/wiki/Cholesky_decomposition) or simple iteration solves it reliably. For a few hundred teams
either is instant.

### What is computed

Ranking sites recompute the ratings after every round of games, solving a T × T system that is small
for any sport. In practice the methods are adjusted: [home-field advantage](https://en.wikipedia.org/wiki/Home_advantage) becomes an extra unknown with
its own column in A, margins are capped to discourage running up the score, and recent games may get
larger weights through [weighted least squares](https://en.wikipedia.org/wiki/Weighted_least_squares).

### Why linear algebra is the right tool

The method turns a schedule into a matrix, and every question about fairness becomes a question about
that matrix. Strength of schedule is the off-diagonal part of M. The overall level of the ratings is
the null space, and the sum constraint is the choice of datum. Whether two teams can be compared is
whether they are in the same [connected piece](https://en.wikipedia.org/wiki/Component_%28graph_theory%29), which is the rank of M. The same least-squares
[projection](https://en.wikipedia.org/wiki/Projection_%28linear_algebra%29) appears in the regression and geodetic entries, so their tools, such as residuals and
[leverage](https://en.wikipedia.org/wiki/Leverage_%28statistics%29), apply here too.

### Pitfall worth teaching

A schedule that falls into separate pieces cannot be ranked across the pieces, and the sum constraint
does not fix it. Suppose that early in a season P has played only Q, and R only S: P beat Q by 2 and R
beat S by 5. Then

```
    [  1  −1   0   0 ]
M = [ −1   1   0   0 ]
    [  0   0   1  −1 ]
    [  0   0  −1   1 ]
```

has rank 2, and its null space contains both (1, 1, 0, 0) and (0, 0, 1, 1). Replacing one equation by
the sum constraint removes only one of those directions, and the matrix stays singular: its [determinant](https://en.wikipedia.org/wiki/Determinant)
is 0. The results say how P compares with Q and how R compares with S, but nothing about P against R.
Any software that returns an answer has broken the tie arbitrarily. Colley's 2I makes the matrix
invertible, but only by falling back on its prior: the comparison between the two groups is then the
starting assumption that all teams are equal. Ratings across conferences rest on the few games played
between conferences, and the linear algebra shows how few of those there can be before the ranking
means nothing.

### Extensions

Keener's method and PageRank rank teams by the dominant eigenvector of a matrix of results (Tier 2;
see the PageRank entry). The [Bradley–Terry](https://en.wikipedia.org/wiki/Bradley%E2%80%93Terry_model) model and the [Elo system](https://en.wikipedia.org/wiki/Elo_rating_system) used in chess treat each game as a
probability of winning instead of a margin, which leads to nonlinear or iterative fits. Langville and
Meyer's book Who's #1? surveys these methods. Weighted least squares down-weights old or lopsided games,
as in the regression entry. The geodetic network adjustment entry has the same rank-deficient
structure with heights instead of ratings, and the resistor-network entry has the same Laplacian with
voltages instead.

### Terminology

How this field's vocabulary reads as linear algebra.

| Domain term | In linear algebra |
|---|---|
| rating | a number per team whose differences predict results |
| margin of victory | the winner's points minus the loser's points in one game |
| schedule graph | teams as nodes and games as edges |
| Massey matrix | the T × T normal-equations matrix, games played on the diagonal and minus the number of meetings off it |
| point differential | a team's total points scored minus points allowed |
| Colley matrix | 2I plus the Massey matrix |
| connected schedule | one in which every team is linked to every other by a chain of games |
| strength of schedule | how good a team's opponents were; built into both methods |

---

[Back to the index](/r/LinearAlgebra/wiki/applications)
