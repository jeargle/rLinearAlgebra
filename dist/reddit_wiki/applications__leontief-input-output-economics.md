# Leontief input–output: how much steel does a car actually take?

### Start here

Building a car takes steel. Making steel takes electricity. Generating electricity takes steel. The
requirements are circular, so you cannot just add them up — following the chain never terminates.

Suppose you want one more car delivered to a customer. You need some steel for it directly. But you also
need extra electricity to make that steel, and extra steel to make that electricity, and so on forever.
Each round is smaller than the last, so the total is finite; the question is what it adds up to.

Economists answer this by writing one equation per industry: total output equals what other industries
consume from it, plus what consumers finally take. Solving the system gives every industry's required
output at once, with the infinite chain of indirect requirements already accounted for.

The same computation, with pollution added as an extra row, is how the carbon footprint of a product is
usually estimated — including all the emissions from its suppliers' suppliers.

**Field:** Economics (and, in its modern form, environmental footprint accounting)  
**Tier:** 1 — posing and solving `(I − A)x = d` needs only a linear solve. The Perron–Frobenius convergence condition lifts it to Tier 2.  
**Scalar field:** R (nonnegative)  
**Vectors:** outputs and demands in R^n, n = number of sectors  
**Underlying equations:** None: a static accounting identity for one period (the dynamic Leontief model adds an ODE)

### The problem

Industries consume each other's output. Making a car needs steel; making steel needs electricity; making electricity needs steel. Given final consumer demand, find the total production every sector must run.

### Variables

| Symbol | Name | What it holds | Shape | Units |
|---|---|---|---|---|
| n | number of sectors | industries in the table | integer | — |
| Z | inter-industry flow matrix | z_ij is the value of sector i's output bought by sector j during the year | n × n | currency per year ($/yr) |
| x | gross output | total output of each sector during the year | n × 1 | $/yr |
| d | final demand | output delivered to final users: households, government, investment, exports | n × 1 | $/yr |
| A | technical-coefficient matrix | a_ij = z_ij / x_j, the input from sector i per dollar of sector j's output | n × n | dimensionless ($ per $) |
| I | identity matrix |  | n × n | — |
| L | Leontief inverse | L = (I − A)⁻¹; l_ij is the total output of sector i required per dollar of final demand for sector j, all rounds of the supply chain included | n × n | dimensionless |
| e | emission intensities (row vector) | direct emissions per dollar of each sector's output | 1 × n | kg CO₂e per $ |

Everything is measured in money at base-year prices, which is why a_ij is dimensionless. Physical tables in tonnes or joules exist, but then A carries mixed units and the coefficients are no longer comparable across rows.

### Formulation

**Where the equations come from.** There is no differential equation here. The model is a static accounting identity over one period, usually a year: every sector's output goes either to other industries or to final users,

```
x_i = Σ_j z_ij + d_i
```

**The modelling assumption.** Leontief's assumption is that each industry uses inputs in fixed proportion to its output: z_ij = a_ij x_j. It is a fixed recipe, with no substitution between inputs and constant returns to scale. Substituting it into the identity:

```
x = A x + d      ⟹      (I − A) x = d      ⟹      x = L d
```

This models, for any given final demand, the gross output each industry must produce. The solution x is the level of production that exactly meets final demand plus all of the intermediate demand that meeting it induces.

**Footprints.** Multiplying by emission intensities gives total emissions, e L d, in kg CO₂e per year. The row vector e L gives emissions per dollar of final demand for each product, including every upstream supplier.

**The differential-equation version.** The dynamic Leontief model adds investment in productive capacity: x = A x + B dx/dt + d, where B holds capital coefficients (capital stock from sector i needed per unit increase of output rate in sector j). That is a system of linear ODEs and is a Tier 3 extension; this entry uses only the static model.

### Matrix structure

Square, entrywise nonnegative, dense-ish, with column sums below 1 for a productive economy. National tables run 400–500 sectors; the global multi-region tables (EXIOBASE, WIOD) reach tens of thousands.

### What is computed

`(I − A)⁻¹`, the Leontief inverse, is the object of interest itself — entry `(i,j)` is the total output of `i` required per unit of final demand for `j`, summed over all supply-chain depths. The Neumann series

```
(I − A)⁻¹ = I + A + A² + A³ + …
```

has a direct reading: direct requirements, then requirements of requirements, and so on.

### Why linear algebra is the right tool

The circularity that makes the accounting hard by hand — steel needs electricity needs steel — is precisely what a matrix inverse resolves in closed form.

### Pitfall worth teaching

By Perron–Frobenius, the series converges exactly when the spectral radius of `A` is below 1. That is not a technical condition: it is the statement that the economy produces more than it consumes in production. A nonnegative matrix's dominant eigenvalue carries economic meaning.

### Extensions

Environmentally-extended I/O appends rows for CO₂, water, and land use, and the same inverse yields the full upstream carbon footprint of a product — this is how most corporate Scope 3 emissions are estimated. Same mathematics: Markov chain fundamental matrices, and structural path analysis.

### Terminology

How this field's vocabulary reads as linear algebra.

| Domain term | In linear algebra |
|---|---|
| technical coefficient matrix A | input from sector i per unit output of sector j |
| final demand | the right-hand side d |
| gross / total output | the unknown x |
| Leontief inverse | (I - A)^-1 |
| multiplier | a single entry of the Leontief inverse |
| productive economy | spectral radius of A below 1, so the Neumann series converges |
| direct vs indirect requirements | the successive terms A, A^2, A^3 of the Neumann series |
| embodied / Scope 3 emissions | an appended satellite row multiplied through the same inverse |

---

[Back to the index](/r/LinearAlgebra/wiki/applications)
