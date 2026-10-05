# /// script
# requires-python = ">=3.11"
# dependencies = ["marimo", "numpy", "matplotlib"]
# ///
"""Leontief input-output: a two-sector toy, then the 2023 US economy in 15 sectors.

Companion notebook to entries/05-leontief-input-output-economics.md.
Runs in the browser (marimo WebAssembly export) or locally:
    uv run --group notebooks marimo edit notebooks/05-leontief-input-output-economics.py
    uv run --group notebooks python notebooks/05-leontief-input-output-economics.py
"""
import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import numpy as np
    import matplotlib.pyplot as plt
    return mo, np, plt


@app.cell
def _():
    def md_table(headers, rows):
        """A markdown table from a header list and rows of already-formatted cells."""
        lines = ["| " + " | ".join(headers) + " |", "|" + "---|" * len(headers)]
        lines += ["| " + " | ".join(str(c) for c in row) + " |" for row in rows]
        return "\n".join(lines)

    def money(v, unit=""):
        return f"{v:,.2f}{unit}"
    return md_table, money


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Leontief input–output: how much steel does a car actually take?

    Industries buy from each other. Making steel takes electricity, and generating electricity
    takes steel, so the requirements go round in a circle. The question is how much every industry
    must produce, in total, so that after all the industries have bought what they need from each
    other, exactly the right amounts are left over for the final users.

    Writing one equation per industry gives

    $$x = A x + d \quad\Longrightarrow\quad (I - A)\,x = d,$$

    where $x$ is each industry's total output, $d$ is what final users take, and column $j$ of $A$
    is the recipe of inputs for one dollar of industry $j$'s output.

    This notebook works the problem twice: first a **two-sector toy** you can check by hand, then
    the **2023 US economy in 15 sectors** from the Bureau of Economic Analysis.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Part 1 — A two-sector toy economy

    There are two industries, steel and electricity. Their recipes, per dollar of output, are:

    | Input | per \$1 of steel | per \$1 of electricity |
    |---|---|---|
    | steel | \$0.20 | \$0.20 |
    | electricity | \$0.40 | \$0.10 |

    These columns are the columns of $A$. The numbers are made up, but chosen so that the hand
    calculation comes out in exact decimals. Move the sliders to set what final users want.
    """)
    return


@app.cell
def _(np):
    toy_sectors = ["Steel", "Electricity"]
    A_toy = np.array([[0.2, 0.2],
                      [0.4, 0.1]])
    return A_toy, toy_sectors


@app.cell
def _(mo):
    d_steel = mo.ui.slider(0, 200, step=5, value=100, label="Final demand for steel ($)",
                           show_value=True)
    d_elec = mo.ui.slider(0, 200, step=5, value=50, label="Final demand for electricity ($)",
                          show_value=True)
    mo.vstack([d_steel, d_elec])
    return d_elec, d_steel


@app.cell
def _(A_toy, d_elec, d_steel, np):
    d_toy = np.array([d_steel.value, d_elec.value], dtype=float)
    x_toy = np.linalg.solve(np.eye(2) - A_toy, d_toy)
    Z_toy = A_toy * x_toy          # z_ij = a_ij x_j: what sector j buys from sector i
    return Z_toy, d_toy, x_toy


@app.cell(hide_code=True)
def _(Z_toy, d_toy, md_table, mo, money, toy_sectors, x_toy):
    _rows = [[toy_sectors[i], money(Z_toy[i, 0]), money(Z_toy[i, 1]), money(d_toy[i]),
              f"**{money(x_toy[i])}**"] for i in range(2)]
    mo.md(
        "### The answer, and the accounting check\n\n"
        f"Steel must produce **\\${x_toy[0]:,.2f}** and electricity **\\${x_toy[1]:,.2f}**. "
        "Each row below adds up: what the two industries buy, plus what final users take, "
        "equals the total produced.\n\n"
        + md_table(["Output of", "bought by steel", "bought by electricity", "final users",
                    "total output x"], _rows)
    )
    return


@app.cell(hide_code=True)
def _(A_toy, mo, np):
    _M = np.eye(2) - A_toy
    _det = np.linalg.det(_M)
    _L = np.linalg.inv(_M)
    # the hand calculation below relies on these exact values
    assert np.isclose(_det, 0.64) and np.allclose(_L, [[1.40625, 0.3125], [0.625, 1.25]])
    mo.md(r"""
    ### By hand

    $$I - A = \begin{pmatrix} 0.8 & -0.2 \\ -0.4 & 0.9 \end{pmatrix}, \qquad
    \det(I - A) = 0.8 \cdot 0.9 - (-0.2)(-0.4) = 0.64,$$

    so, with the usual $2 \times 2$ inverse formula,

    $$L = (I - A)^{-1} = \frac{1}{0.64}\begin{pmatrix} 0.9 & 0.2 \\ 0.4 & 0.8 \end{pmatrix}
    = \begin{pmatrix} 1.40625 & 0.3125 \\ 0.625 & 1.25 \end{pmatrix}.$$

    With the default demand $d = (100, 50)$: $x = L d = (140.625 + 15.625,\; 62.5 + 62.5) =
    (156.25,\; 125)$.

    Each entry of $L$ has a meaning. The first column says that one extra dollar of steel for final
    users requires \$1.41 of steel output in total, and \$0.63 of electricity, once every round of
    the supply chain is counted.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Round by round

    The same answer can be reached the long way round, which shows where it comes from. To deliver
    $d$, the industries first need inputs $A d$. Producing those inputs needs $A(Ad) = A^2 d$, and
    so on:

    $$x = d + A d + A^2 d + A^3 d + \cdots$$

    Each round is smaller than the last, because every column of $A$ adds up to less than 1: each
    dollar of output uses less than a dollar of inputs.
    """)
    return


@app.cell
def _(A_toy, d_toy, np):
    toy_rounds = [d_toy]
    for _ in range(11):
        toy_rounds.append(A_toy @ toy_rounds[-1])
    toy_running = np.cumsum(toy_rounds, axis=0)
    return toy_rounds, toy_running


@app.cell(hide_code=True)
def _(md_table, mo, money, toy_rounds, toy_running, x_toy):
    _rows = [[k, money(r[0]), money(r[1]), money(s[0]), money(s[1])]
             for k, (r, s) in enumerate(zip(toy_rounds[:8], toy_running[:8]))]
    _rows.append(["exact", "", "", f"**{money(x_toy[0])}**", f"**{money(x_toy[1])}**"])
    mo.md(md_table(["round k", "steel in A^k d", "electricity in A^k d", "steel so far",
                    "electricity so far"], _rows))
    return


@app.cell
def _(plt, toy_running, toy_sectors, x_toy):
    _fig, _ax = plt.subplots(figsize=(6.5, 3.2))
    for _i, _c in enumerate(["#1d4ed8", "#d97706"]):
        _ax.plot(range(len(toy_running)), toy_running[:, _i], "o-", color=_c,
                 label=f"{toy_sectors[_i]}: running total")
        _ax.axhline(x_toy[_i], color=_c, ls="--", lw=1)
    _ax.set_xlabel("rounds of the supply chain included")
    _ax.set_ylabel("output ($)")
    _ax.set_title("Adding up the rounds approaches the exact answer (dashed)")
    _ax.legend(frameon=False)
    _fig.tight_layout()
    _fig
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### When the economy is not productive

    The rounds shrink only if the economy produces more than it uses up in production. Scale every
    recipe by a factor $s$, as if each industry became less efficient, and watch what happens.

    A useful first-course test: if every column of $A$ adds up to less than 1, the economy is
    productive. That test is sufficient but not necessary. The exact condition, which needs
    eigenvalues (Tier 2), is that the largest $|\lambda|$ of $A$, its *spectral radius*, is below 1.
    """)
    return


@app.cell
def _(mo):
    scale = mo.ui.slider(0.5, 2.6, step=0.05, value=1.0,
                         label="Scale every input requirement by s", show_value=True)
    scale
    return (scale,)


@app.cell
def _(A_toy, d_toy, np, scale):
    A_s = scale.value * A_toy
    colsums_s = A_s.sum(axis=0)
    rho_s = max(abs(np.linalg.eigvals(A_s)))
    x_s = np.linalg.solve(np.eye(2) - A_s, d_toy)
    rounds_s = [d_toy]
    for _ in range(25):
        rounds_s.append(A_s @ rounds_s[-1])
    running_s = np.cumsum(rounds_s, axis=0)
    return colsums_s, rho_s, running_s, x_s


@app.cell(hide_code=True)
def _(colsums_s, mo, rho_s, scale, x_s):
    if rho_s < 1 and colsums_s.max() < 1:
        _verdict = "Productive, and the simple column-sum test already shows it."
    elif rho_s < 1:
        _verdict = ("**Still productive**, even though a column adds up to more than 1. "
                    "The column-sum test is not enough here; the spectral radius settles it.")
    else:
        _verdict = ("**Not productive.** The rounds grow instead of shrinking, and the "
                    "'solution' of (I − A)x = d is meaningless: it has a negative output or "
                    "an absurdly large one.")
    mo.md(
        f"With s = {scale.value:.2f}: column sums of A are "
        f"{colsums_s[0]:.2f} (steel) and {colsums_s[1]:.2f} (electricity); "
        f"spectral radius = **{rho_s:.3f}**.\n\n"
        f"Solving anyway gives x = ({x_s[0]:,.1f}, {x_s[1]:,.1f}).\n\n{_verdict}"
    )
    return


@app.cell
def _(np, plt, rho_s, running_s, x_s):
    _fig, _ax = plt.subplots(figsize=(6.5, 3.0))
    _ax.plot(running_s[:, 0], "o-", ms=3, color="#1d4ed8", label="steel: running total")
    if rho_s < 1:
        _ax.axhline(x_s[0], color="#1d4ed8", ls="--", lw=1, label="exact answer")
    else:
        _ax.set_yscale("log")    # divergent rounds grow geometrically
    _ax.set_xlabel("rounds of the supply chain included")
    _ax.set_ylabel("steel output ($)")
    _ax.set_title(f"spectral radius {rho_s:.3f}: the rounds "
                  + ("converge" if rho_s < 1 else "diverge"))
    _ax.legend(frameon=False)
    _fig.tight_layout()
    _fig
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Part 2 — The US economy in 2023, in 15 sectors

    The same computation at a realistic scale. The data are the Bureau of Economic Analysis's
    2023 input–output tables at its coarsest ("sector") level, in millions of dollars. Real national
    tables go to about 400 sectors; 15 is small enough to show on screen, but large enough that
    nobody would do it by hand.

    BEA publishes its tables commodity-by-industry. `data/prepare_bea_2023.py` in the repository
    downloads them and converts them to a square industry-by-industry table with BEA's standard
    method, then writes the numbers into the cell below. *Final demand* $d$ is everything that
    leaves the inter-industry system: household purchases, investment, government purchases, and
    exports, minus imports.
    """)
    return


@app.cell
def _(np):
    # BEGIN BEA DATA (generated by data/prepare_bea_2023.py; 2023, $ millions)
    sectors = ['Agriculture', 'Mining', 'Utilities', 'Construction', 'Manufacturing', 'Wholesale trade', 'Retail trade', 'Transportation', 'Information', 'Finance & real estate', 'Professional services', 'Education & health', 'Arts, food & lodging', 'Other services', 'Government']
    Z_us = np.array([
        [155139, 151, 5, 2424, 328784, 60, 1216, 48, 85, 223, 3845, 389, 13363, 107, 8588],
        [1841, 55268, 23380, 25565, 445075, 1009, 590, 1512, 2870, 756, 4741, 3891, 3547, 1919, 26907],
        [8069, 11529, 27020, 10974, 59953, 14436, 38376, 10997, 13345, 41279, 15753, 20098, 32165, 7605, 40559],
        [2097, 4742, 5656, 525, 25667, 5846, 12788, 8590, 5405, 138516, 6036, 5932, 11897, 5737, 142406],
        [84226, 81951, 20514, 544329, 2193324, 135963, 58877, 134412, 92044, 84576, 251596, 259175, 155471, 62312, 558162],
        [52875, 22157, 7425, 136318, 526171, 74972, 35605, 30483, 39808, 38418, 72354, 77397, 43078, 17923, 108765],
        [1760, 895, 2558, 109690, 20548, 688, 8091, 18822, 421, 11154, 7874, 972, 14341, 8429, 366],
        [18120, 15987, 26188, 44355, 193891, 139015, 110495, 211671, 23865, 66709, 73950, 41034, 24381, 6828, 100114],
        [710, 4860, 7505, 19094, 41731, 47499, 58420, 17013, 316882, 143017, 191761, 62632, 63033, 24121, 199651],
        [14270, 38446, 21460, 86091, 150578, 264691, 320427, 193954, 159002, 1857061, 478329, 375355, 287033, 137742, 124605],
        [3814, 63753, 29685, 119855, 223812, 407348, 263880, 100991, 289883, 846591, 787838, 339667, 221592, 89010, 400069],
        [2, 0, 21, 1, 6, 1784, 3672, 103, 32, 53, 607, 35575, 5476, 3458, 34052],
        [572, 425, 3031, 2301, 8663, 22704, 13654, 13048, 55967, 145438, 101599, 95735, 79581, 5285, 44696],
        [351, 442, 1104, 9919, 17326, 24886, 17234, 19279, 9307, 64871, 54540, 28017, 21124, 8663, 78763],
        [3742, 4441, 10160, 5800, 31917, 34248, 28057, 18222, 11427, 50492, 26136, 26901, 30575, 6163, 38120],
    ], dtype=float)
    d_us = np.array([109116, 96859, 277658, 2086499, 2188266, 1504361, 2435071, 645397, 1261270, 4857029, 1946469, 3559780, 1694797, 857344, 4455159], dtype=float)
    x_us = np.array([623540, 695731, 629815, 2468340, 6905201, 2788110, 2641681, 1742000, 2459201, 9366073, 6134256, 3644624, 2287495, 1213169, 4787577], dtype=float)
    # END BEA DATA
    return Z_us, d_us, sectors, x_us


@app.cell
def _(Z_us, d_us, np, x_us):
    n_us = len(x_us)
    A_us = Z_us / x_us                     # a_ij = z_ij / x_j
    L_us = np.linalg.inv(np.eye(n_us) - A_us)
    x_solved = np.linalg.solve(np.eye(n_us) - A_us, d_us)
    closure = x_solved / x_us - 1
    rho_us = max(abs(np.linalg.eigvals(A_us)))
    assert abs(closure).max() < 0.005, "solved output should match BEA's published output"
    return A_us, L_us, closure, n_us, rho_us, x_solved


@app.cell(hide_code=True)
def _(A_us, closure, md_table, mo, rho_us, sectors, x_solved, x_us):
    _rows = [[s, f"{x_us[i] / 1e3:,.0f}", f"{x_solved[i] / 1e3:,.0f}", f"{100 * closure[i]:+.2f}%"]
             for i, s in enumerate(sectors)]
    mo.md(
        "### Check: does solving the system recover the real economy?\n\n"
        "Give the model the actual 2023 final demand, solve $(I - A)x = d$, and compare with what "
        "each industry actually produced in 2023 ($ billions). The small differences come from "
        "rounding and from two minor rows that a square industry table leaves out: scrap, and "
        "imports with no domestic counterpart.\n\n"
        + md_table(["Sector", "actual output", "solved output", "difference"], _rows)
        + f"\n\nEvery column of $A$ adds up to less than 1 (largest: {A_us.sum(0).max():.2f}), "
        f"so the economy is productive; its spectral radius is {rho_us:.3f}."
    )
    return


@app.cell
def _(A_us, plt, sectors):
    _fig, _ax = plt.subplots(figsize=(7.5, 6.2))
    _im = _ax.imshow(A_us, cmap="Blues", vmin=0)
    _ax.set_xticks(range(len(sectors)), sectors, rotation=60, ha="right", fontsize=8)
    _ax.set_yticks(range(len(sectors)), sectors, fontsize=8)
    _ax.set_xlabel("buying sector j (column = its recipe per $1 of output)")
    _ax.set_ylabel("supplying sector i")
    _ax.set_title("Technical coefficients A, US 2023")
    _fig.colorbar(_im, ax=_ax, shrink=0.7, label=r"\$ of input per \$1 of output")
    _fig.tight_layout()
    _fig
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Multipliers: what one dollar of demand sets in motion

    Column $j$ of the Leontief inverse $L = (I - A)^{-1}$ is the output every sector must produce
    for one extra dollar of final demand for sector $j$'s product. Its column sum is that
    sector's *output multiplier*: the total output, across the whole economy, that one dollar of
    its final demand requires.
    """)
    return


@app.cell
def _(L_us, np, plt, sectors):
    _mult = L_us.sum(axis=0)
    _order = np.argsort(_mult)
    _fig, _ax = plt.subplots(figsize=(7, 4.6))
    _ax.barh([sectors[i] for i in _order], _mult[_order], color="#1d4ed8")
    _ax.axvline(1, color="#555", lw=1)
    _ax.set_xlabel("total output required per $1 of final demand")
    _ax.set_title("Output multipliers (column sums of L)")
    for _k, _i in enumerate(_order):
        _ax.text(_mult[_i] + 0.01, _k, f"{_mult[_i]:.2f}", va="center", fontsize=8)
    _ax.set_xlim(0, _mult.max() * 1.12)
    _fig.tight_layout()
    _fig
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### A demand shock, traced through the supply chain

    Pick a sector and add extra final demand for it. The bars split each sector's extra output
    into the demand itself, the first round of inputs $A\,\Delta d$, and every later round
    $A^2 \Delta d + A^3 \Delta d + \cdots$.
    """)
    return


@app.cell
def _(mo, sectors):
    shock_sector = mo.ui.dropdown(options=sectors, value="Manufacturing",
                                  label="Extra final demand for")
    shock_size = mo.ui.slider(1, 100, step=1, value=10, label="Amount ($ billions)",
                              show_value=True)
    mo.hstack([shock_sector, shock_size], justify="start", gap=2)
    return shock_sector, shock_size


@app.cell
def _(A_us, L_us, n_us, np, sectors, shock_sector, shock_size):
    dd = np.zeros(n_us)
    dd[sectors.index(shock_sector.value)] = shock_size.value
    dx_total = L_us @ dd
    dx_first = A_us @ dd
    dx_later = dx_total - dd - dx_first
    return dd, dx_first, dx_later, dx_total


@app.cell
def _(dd, dx_first, dx_later, dx_total, np, plt, sectors, shock_sector):
    _order = np.argsort(dx_total)
    _labels = [sectors[i] for i in _order]
    _fig, _ax = plt.subplots(figsize=(7, 4.8))
    _ax.barh(_labels, dd[_order], color="#1d4ed8", label="the demand itself")
    _ax.barh(_labels, dx_first[_order], left=dd[_order], color="#60a5fa",
             label="first round of inputs")
    _ax.barh(_labels, dx_later[_order], left=(dd + dx_first)[_order], color="#d97706",
             label="all later rounds")
    _ax.set_xlabel("extra output ($ billions)")
    _ax.set_title(f"Extra demand for {shock_sector.value}: total extra output "
                  f"${dx_total.sum():,.1f} billion")
    _ax.legend(frameon=False, loc="lower right")
    _fig.tight_layout()
    _fig
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### How many rounds does the real economy need?

    The rounds shrink roughly by a factor of the spectral radius each time, so its size decides how
    many rounds matter. This plot measures the error of the running total
    $I + A + \cdots + A^k$ against the exact inverse.
    """)
    return


@app.cell
def _(A_us, L_us, n_us, np, plt, rho_us):
    _S, _P, _err = np.eye(n_us), np.eye(n_us), []
    for _ in range(30):
        _P = _P @ A_us
        _S = _S + _P
        _err.append(np.abs(_S - L_us).max())
    _k6 = next(k for k, e in enumerate(_err, 1) if e < 1e-6)
    _fig, _ax = plt.subplots(figsize=(6.5, 3.2))
    _ax.semilogy(range(1, 31), _err, "o-", ms=3, color="#1d4ed8", label="largest error in L")
    _ax.semilogy(range(1, 31), [rho_us ** k for k in range(1, 31)], "--", color="#555",
                 label=f"spectral radius^k = {rho_us:.3f}^k")
    _ax.axvline(_k6, color="#d97706", lw=1)
    _ax.set_xlabel("rounds k")
    _ax.set_title(f"Error falls below one in a million after {_k6} rounds")
    _ax.legend(frameon=False)
    _fig.tight_layout()
    _fig
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Notes

    - **Solve, do not invert, for one demand vector.** `np.linalg.solve(I - A, d)` is the right
      call for a single $d$. Forming $L$ explicitly is justified here because $L$ itself is the
      object of interest: its entries and column sums are the multipliers.
    - **Fixed recipes are the model's big assumption.** Every industry is assumed to buy inputs in
      fixed proportion to its output, so the model cannot capture substitution or economies of
      scale. Treat large shocks with caution.
    - **BEA's own total-requirements table.** BEA also publishes $L$ directly. Its version differs
      from the one computed here by at most 0.05 in any entry, because BEA applies further
      adjustments.
    """)
    return


if __name__ == "__main__":
    app.run()
