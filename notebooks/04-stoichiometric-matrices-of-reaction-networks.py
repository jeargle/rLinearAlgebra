# /// script
# requires-python = ">=3.11"
# dependencies = ["marimo", "numpy", "matplotlib"]
# ///
"""Stoichiometric matrices: a balanced equation and a five-species toy, then E. coli's core metabolism.

Companion notebook to entries/04-stoichiometric-matrices-of-reaction-networks.md.
Runs in the browser (marimo WebAssembly export) or locally:
    uv run --group notebooks marimo edit notebooks/04-stoichiometric-matrices-of-reaction-networks.py
    uv run --group notebooks python notebooks/04-stoichiometric-matrices-of-reaction-networks.py
"""
import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import numpy as np
    import matplotlib.pyplot as plt
    import re
    import textwrap
    from fractions import Fraction
    from math import gcd, lcm
    return Fraction, gcd, lcm, mo, np, plt, re, textwrap


@app.cell
def _(Fraction):
    def md_table(headers, rows):
        """A markdown table from a header list and rows of already-formatted cells."""
        lines = ["| " + " | ".join(headers) + " |", "|" + "---|" * len(headers)]
        lines += ["| " + " | ".join(str(c) for c in row) + " |" for row in rows]
        return "\n".join(lines)

    def latex_matrix(M, row_labels=None, col_labels=None):
        """A LaTeX array, one matrix row per line, with optional row and column labels."""
        def entry(x):
            q = Fraction(x)
            return str(q.numerator) if q.denominator == 1 else rf"\tfrac{{{q.numerator}}}{{{q.denominator}}}"
        lead = "r|" if row_labels else ""
        lines = []
        if col_labels:
            lines.append((" & " if row_labels else "") + " & ".join(col_labels) + r" \\ \hline")
        for i, row in enumerate(M):
            label = f"{row_labels[i]} & " if row_labels else ""
            lines.append(label + " & ".join(entry(x) for x in row) + r" \\")
        return (r"\begin{array}{" + lead + "r" * len(M[0]) + "}\n" + "\n".join(lines)
                + "\n" + r"\end{array}")

    SUBSCRIPTS = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")

    def equation_string(s, species):
        """'C₆H₁₂O₆ + 6 O₂ → 6 CO₂ + 6 H₂O' from signed coefficients (negative: consumed)."""
        def side(pairs):
            terms = [(f"{abs(c)} " if abs(c) != 1 else "") + sp.translate(SUBSCRIPTS)
                     for c, sp in pairs]
            return " + ".join(terms) or "∅"
        left = side([(c, sp) for c, sp in zip(s, species) if c < 0])
        right = side([(c, sp) for c, sp in zip(s, species) if c > 0])
        return f"{left} → {right}"
    return equation_string, latex_matrix, md_table


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Stoichiometric matrices: what a reaction network can and cannot do at steady state

    Write a table with one row per chemical species and one column per reaction. Entry $s_{ij}$
    is the number of molecules of species $i$ that one occurrence of reaction $j$ produces
    (positive) or consumes (negative). That table is the **stoichiometric matrix** $S$. It says
    nothing about how fast anything happens, yet it already answers two questions.

    Each species' concentration changes at the rate it is produced minus the rate it is consumed,
    summed over the reactions:

    $$\frac{dc}{dt} = S\,v(c).$$

    Here $c$ holds the $m$ concentrations and $v$ the $r$ reaction rates (fluxes). The rates
    $v(c)$ are the kinetics: nonlinear, and full of rate constants that are hard to measure. $S$ is
    a constant integer matrix fixed by the chemistry. It maps **flux space** $\mathbb{R}^r$ (one
    entry per reaction) into **species space** $\mathbb{R}^m$ (one entry per species), and those
    are two different spaces:

    - **Steady state.** $dc/dt = 0$ means $S v = 0$: the steady-state fluxes form the *right* null
      space of $S$, a subspace of $\mathbb{R}^r$.
    - **Conservation laws.** If $y^\mathsf{T} S = 0$ then
      $d(y^\mathsf{T} c)/dt = y^\mathsf{T} S v = 0$, so $y^\mathsf{T} c$ never changes, whatever
      the kinetics. These $y$ form the *left* null space of $S$, a subspace of $\mathbb{R}^m$.

    This notebook works the problem twice: first **a balanced chemical equation and a five-species
    toy network** you can check by hand, then **the core metabolism of *E. coli***, a real model
    from the BiGG Models database.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    show_julia = mo.ui.switch(value=False, label="Show Julia equivalents")
    mo.callout(mo.hstack([show_julia, mo.md(
        "The notebook runs Python. Switch this on to see the same computations in Julia "
        "beneath the Python cells that do them. All of them together, data included, are in "
        "[one Julia file](https://github.com/jeargle/rLinearAlgebra/blob/main/snippets/"
        "04-stoichiometric-matrices-of-reaction-networks.jl) that runs as it stands: "
        "`julia 04-stoichiometric-matrices-of-reaction-networks.jl`.")], justify="start", gap=1),
        kind="neutral")
    return (show_julia,)


@app.cell(hide_code=True)
def _():
    # BEGIN JULIA SNIPPETS (generated by build/sync_snippets.py from snippets/; do not edit)
    julia_snippets = {
        'setup': ('Exact null spaces in fractions', 'using LinearAlgebra\n\n"Reduced row echelon form of M in exact fractions, and its pivot columns."\nfunction rref_exact(M)\n    R = Rational{BigInt}.(M)\n    pivots, top = Int[], 1\n    for col in 1:size(R, 2)\n        p = findfirst(!iszero, R[top:end, col])\n        p === nothing && continue          # no pivot here: col is a free column\n        p += top - 1\n        R[[top, p], :] = R[[p, top], :]\n        R[top, :] ./= R[top, col]\n        for i in 1:size(R, 1)\n            if i != top && !iszero(R[i, col])\n                R[i, :] .-= R[i, col] .* R[top, :]\n            end\n        end\n        push!(pivots, col)\n        top += 1\n        top > size(R, 1) && break\n    end\n    return R, pivots\nend\n\n"Basis of {x : M x = 0}: one vector per free column, with 1 there and 0 in the other free columns."\nfunction nullspace_exact(M)\n    R, pivots = rref_exact(M)\n    basis = Vector{Vector{Rational{BigInt}}}()\n    for f in setdiff(1:size(M, 2), pivots)\n        x = zeros(Rational{BigInt}, size(M, 2))\n        x[f] = 1\n        for (row, p) in enumerate(pivots)\n            x[p] = -R[row, f]\n        end\n        push!(basis, x)\n    end\n    return basis\nend\n\n"x rescaled to the shortest vector of integers: clear denominators, divide out the common factor."\nfunction integer_vector(x)\n    ints = numerator.(x .* lcm(denominator.(x)))\n    return ints .÷ gcd(ints)\nend\n\n"Dict(element => number of atoms) for a formula such as \\"C6H12O6\\"."\nfunction atom_counts(formula)\n    counts = Dict{String,Int}()\n    for m in eachmatch(r"([A-Z][a-z]?)(\\d*)", formula)\n        counts[m[1]] = get(counts, m[1], 0) + (isempty(m[2]) ? 1 : parse(Int, m[2]))\n    end\n    return counts\nend'),
        'balance': ('Balancing an equation: Z s = 0', 'species_bal = ["C6H12O6", "O2", "CO2", "H2O"]    # glucose, oxygen, carbon dioxide, water\nelements_bal = sort(unique(e for f in species_bal for e in keys(atom_counts(f))))   # C, H, O\nZ_bal = [get(atom_counts(f), e, 0) for e in elements_bal, f in species_bal]\nK_bal = nullspace_exact(Z_bal)\n@assert length(K_bal) == 1                        # nullity 1: one balanced reaction, up to scale\ns_bal = integer_vector(K_bal[1])\ns_bal = s_bal[1] > 0 ? -s_bal : s_bal             # glucose is consumed: negative\n@assert Z_bal == [ 6 0 1 0\n                  12 0 0 2\n                   6 2 2 1]\n@assert s_bal == [-1, -6, 6, 6]                   # C6H12O6 + 6 O2 -> 6 CO2 + 6 H2O\n@show s_bal'),
        'toy': ('A five-species network', 'species_toy = ["P", "Q", "R", "ATP", "ADP"]\n#   reaction: 1   2   3   4   5   6\nS_toy = [     1  -1   0   0   0   0     # P\n              0   1  -1   0   0  -1     # Q\n              0   0   1  -1   0   1     # R\n              0  -1   2   0  -1   0     # ATP\n              0   1  -2   0   1   0]    # ADP\nm_toy, r_toy = size(S_toy)                # 5 species, 6 reactions'),
        'rank': ('Rank and the two null spaces', 'rank_toy = length(rref_exact(S_toy)[2])\nK_toy = nullspace_exact(S_toy)                    # S v = 0: flux space, R^6\nY_toy = nullspace_exact(permutedims(S_toy))       # y\' S = 0: species space, R^5\n@assert rank_toy == 4\n@assert integer_vector.(K_toy) == [[1, 1, 1, 1, 1, 0],\n                                   [2, 2, 1, 2, 0, 1]]\n@assert integer_vector.(Y_toy) == [[0, 0, 0, 1, 1]]   # ATP + ADP\n@assert rank_toy + length(K_toy) == r_toy && rank_toy + length(Y_toy) == m_toy\nprintln("rank = $rank_toy  nullity = $(length(K_toy))  left nullity = $(length(Y_toy))")'),
        'ode': ('Mass action: the concentrations move, ATP + ADP does not', 'k5, atp0 = 0.5, 1.5                       # the sliders: ATP demand, starting ATP\nk_toy = [1.0, 1.0, 1.0, 1.0, k5, 0.5]\nS_toy_f = Float64.(S_toy)\n\n"Mass-action rates v(c) of the six reactions."\nfunction rates_toy(c)\n    P, Q, R, ATP, ADP = c\n    return k_toy .* [1.0, P * ATP, Q * ADP^2, R, ATP, Q]\nend\n\ndt_toy, n_toy = 0.02, 3000                # 60 time units\nc_toy = [0.0, 0.0, 0.0, atp0, 0.5]\ntraj_toy = [c_toy]\nfor _ in 1:n_toy                          # classical Runge-Kutta steps of dc/dt = S v(c)\n    f1 = S_toy_f * rates_toy(c_toy)\n    f2 = S_toy_f * rates_toy(c_toy + dt_toy / 2 * f1)\n    f3 = S_toy_f * rates_toy(c_toy + dt_toy / 2 * f2)\n    f4 = S_toy_f * rates_toy(c_toy + dt_toy * f3)\n    global c_toy = c_toy + dt_toy / 6 * (f1 + 2 * f2 + 2 * f3 + f4)\n    push!(traj_toy, c_toy)\nend\ntraj_toy = permutedims(reduce(hcat, traj_toy))   # one row per time step\ny_toy = Float64.(Y_toy[1])\ntotal_toy = traj_toy * y_toy              # ATP + ADP at every time step\nv_end = rates_toy(traj_toy[end, :])\nab_end = Float64.(reduce(hcat, K_toy)) \\ v_end   # least squares: v = a K1 + b K2\n@assert maximum(abs, total_toy .- total_toy[1]) < 1e-12   # conserved, whatever the kinetics\n@assert maximum(abs, S_toy_f * v_end) < 1e-6              # the run has reached steady state\nprintln("ATP + ADP = $(total_toy[1])  steady-state flux v = $(round.(v_end, digits=3))  (a, b) = $(round.(ab_end, digits=3))")'),
        'data': ('The E. coli core model', '# BEGIN BIGG DATA: BiGG e_coli_core, 72 metabolites x 95 reactions, 360 nonzeros (written by data/prepare_ecoli_core.py)\nmet_ids = [\n    "glc__D_e", "gln__L_c", "gln__L_e", "glu__L_c", "glu__L_e", "glx_c", "h2o_c", "h2o_e", "h_c",\n    "h_e", "icit_c", "lac__D_c", "lac__D_e", "mal__L_c", "mal__L_e", "nad_c", "nadh_c", "nadp_c",\n    "nadph_c", "nh4_c", "13dpg_c", "nh4_e", "o2_c", "2pg_c", "o2_e", "3pg_c", "oaa_c", "pep_c",\n    "6pgc_c", "pi_c", "6pgl_c", "pi_e", "ac_c", "pyr_c", "pyr_e", "q8_c", "q8h2_c", "r5p_c",\n    "ru5p__D_c", "ac_e", "acald_c", "s7p_c", "acald_e", "accoa_c", "succ_c", "succ_e", "succoa_c",\n    "acon_C_c", "xu5p__D_c", "actp_c", "adp_c", "akg_c", "akg_e", "amp_c", "atp_c", "cit_c",\n    "co2_c", "co2_e", "coa_c", "dhap_c", "e4p_c", "etoh_c", "etoh_e", "f6p_c", "fdp_c", "for_c",\n    "for_e", "fru_e", "fum_c", "fum_e", "g3p_c", "g6p_c",\n]\nmet_names = [\n    "D-Glucose", "L-Glutamine", "L-Glutamine", "L-Glutamate", "L-Glutamate", "Glyoxylate",\n    "H2O H2O", "H2O H2O", "H+", "H+", "Isocitrate", "D-Lactate", "D-Lactate", "L-Malate",\n    "L-Malate", "Nicotinamide adenine dinucleotide", "Nicotinamide adenine dinucleotide - reduced",\n    "Nicotinamide adenine dinucleotide phosphate",\n    "Nicotinamide adenine dinucleotide phosphate - reduced", "Ammonium",\n    "3-Phospho-D-glyceroyl phosphate", "Ammonium", "O2 O2", "D-Glycerate 2-phosphate", "O2 O2",\n    "3-Phospho-D-glycerate", "Oxaloacetate", "Phosphoenolpyruvate", "6-Phospho-D-gluconate",\n    "Phosphate", "6-phospho-D-glucono-1,5-lactone", "Phosphate", "Acetate", "Pyruvate", "Pyruvate",\n    "Ubiquinone-8", "Ubiquinol-8", "Alpha-D-Ribose 5-phosphate", "D-Ribulose 5-phosphate",\n    "Acetate", "Acetaldehyde", "Sedoheptulose 7-phosphate", "Acetaldehyde", "Acetyl-CoA",\n    "Succinate", "Succinate", "Succinyl-CoA", "Cis-Aconitate", "D-Xylulose 5-phosphate",\n    "Acetyl phosphate", "ADP C10H12N5O10P2", "2-Oxoglutarate", "2-Oxoglutarate", "AMP C10H12N5O7P",\n    "ATP C10H12N5O13P3", "Citrate", "CO2 CO2", "CO2 CO2", "Coenzyme A",\n    "Dihydroxyacetone phosphate", "D-Erythrose 4-phosphate", "Ethanol", "Ethanol",\n    "D-Fructose 6-phosphate", "D-Fructose 1,6-bisphosphate", "Formate", "Formate", "D-Fructose",\n    "Fumarate", "Fumarate", "Glyceraldehyde 3-phosphate", "D-Glucose 6-phosphate",\n]\nmet_formulas = [\n    "C6H12O6", "C5H10N2O3", "C5H10N2O3", "C5H8NO4", "C5H8NO4", "C2H1O3", "H2O", "H2O", "H", "H",\n    "C6H5O7", "C3H5O3", "C3H5O3", "C4H4O5", "C4H4O5", "C21H26N7O14P2", "C21H27N7O14P2",\n    "C21H25N7O17P3", "C21H26N7O17P3", "H4N", "C3H4O10P2", "H4N", "O2", "C3H4O7P", "O2", "C3H4O7P",\n    "C4H2O5", "C3H2O6P", "C6H10O10P", "HO4P", "C6H9O9P", "HO4P", "C2H3O2", "C3H3O3", "C3H3O3",\n    "C49H74O4", "C49H76O4", "C5H9O8P", "C5H9O8P", "C2H3O2", "C2H4O", "C7H13O10P", "C2H4O",\n    "C23H34N7O17P3S", "C4H4O4", "C4H4O4", "C25H35N7O19P3S", "C6H3O6", "C5H9O8P", "C2H3O5P",\n    "C10H12N5O10P2", "C5H4O5", "C5H4O5", "C10H12N5O7P", "C10H12N5O13P3", "C6H5O7", "CO2", "CO2",\n    "C21H32N7O16P3S", "C3H5O6P", "C4H7O7P", "C2H6O", "C2H6O", "C6H11O9P", "C6H10O12P2", "CH1O2",\n    "CH1O2", "C6H12O6", "C4H2O4", "C4H2O4", "C3H5O6P", "C6H11O9P",\n]\nmet_charges = [\n    0, 0, 0, -1, -1, -1, 0, 0, 1, 1, -3, -1, -1, -2, -2, -1, -2, -3, -4, 1, -4, 1, 0, -3, 0, -3,\n    -2, -3, -3, -2, -2, -2, -1, -1, -1, 0, 0, -2, -2, -1, 0, -2, 0, -4, -2, -2, -5, -3, -2, -2, -3,\n    -2, -2, -2, -4, -3, 0, 0, -4, -2, -2, 0, 0, -2, -4, -1, -1, 0, -2, -2, -2, -2,\n]\nrxn_ids = [\n    "PFK", "PFL", "PGI", "PGK", "PGL", "ACALD", "AKGt2r", "PGM", "PIt2r", "ALCD2x", "ACALDt",\n    "ACKr", "PPC", "ACONTa", "ACONTb", "ATPM", "PPCK", "ACt2r", "PPS", "ADK1", "AKGDH", "ATPS4r",\n    "PTAr", "PYK", "BIOMASS_Ecoli_core_w_GAM", "PYRt2", "CO2t", "RPE", "CS", "RPI", "SUCCt2_2",\n    "CYTBD", "D_LACt2", "ENO", "SUCCt3", "ETOHt2r", "SUCDi", "SUCOAS", "TALA", "THD2", "TKT1",\n    "TKT2", "TPI", "EX_ac_e", "EX_acald_e", "EX_akg_e", "EX_co2_e", "EX_etoh_e", "EX_for_e",\n    "EX_fru_e", "EX_fum_e", "EX_glc__D_e", "EX_gln__L_e", "EX_glu__L_e", "EX_h_e", "EX_h2o_e",\n    "EX_lac__D_e", "EX_mal__L_e", "EX_nh4_e", "EX_o2_e", "EX_pi_e", "EX_pyr_e", "EX_succ_e", "FBA",\n    "FBP", "FORt2", "FORt", "FRD7", "FRUpts2", "FUM", "FUMt2_2", "G6PDH2r", "GAPD", "GLCpts",\n    "GLNS", "GLNabc", "GLUDy", "GLUN", "GLUSy", "GLUt2r", "GND", "H2Ot", "ICDHyr", "ICL", "LDH_D",\n    "MALS", "MALt2_2", "MDH", "ME1", "ME2", "NADH16", "NADTRHD", "NH4t", "O2t", "PDH",\n]\nrxn_names = [\n    "Phosphofructokinase", "Pyruvate formate lyase", "Glucose-6-phosphate isomerase",\n    "Phosphoglycerate kinase", "6-phosphogluconolactonase",\n    "Acetaldehyde dehydrogenase (acetylating)", "2 oxoglutarate reversible transport via symport",\n    "Phosphoglycerate mutase", "Phosphate reversible transport via symport",\n    "Alcohol dehydrogenase (ethanol)", "Acetaldehyde reversible transport", "Acetate kinase",\n    "Phosphoenolpyruvate carboxylase", "Aconitase (half-reaction A, Citrate hydro-lyase)",\n    "Aconitase (half-reaction B, Isocitrate hydro-lyase)", "ATP maintenance requirement",\n    "Phosphoenolpyruvate carboxykinase", "Acetate reversible transport via proton symport",\n    "Phosphoenolpyruvate synthase", "Adenylate kinase", "2-Oxogluterate dehydrogenase",\n    "ATP synthase (four protons for one ATP)", "Phosphotransacetylase", "Pyruvate kinase",\n    "Biomass Objective Function with GAM", "Pyruvate transport in via proton symport",\n    "CO2 transporter via diffusion", "Ribulose 5-phosphate 3-epimerase", "Citrate synthase",\n    "Ribose-5-phosphate isomerase", "Succinate transport via proton symport (2 H)",\n    "Cytochrome oxidase bd (ubiquinol-8: 2 protons)", "D lactate transport via proton symport",\n    "Enolase", "Succinate transport out via proton antiport",\n    "Ethanol reversible transport via proton symport", "Succinate dehydrogenase (irreversible)",\n    "Succinyl-CoA synthetase (ADP-forming)", "Transaldolase", "NAD(P) transhydrogenase",\n    "Transketolase", "Transketolase", "Triose-phosphate isomerase", "Acetate exchange",\n    "Acetaldehyde exchange", "2-Oxoglutarate exchange", "CO2 exchange", "Ethanol exchange",\n    "Formate exchange", "D-Fructose exchange", "Fumarate exchange", "D-Glucose exchange",\n    "L-Glutamine exchange", "L-Glutamate exchange", "H+ exchange", "H2O exchange",\n    "D-lactate exchange", "L-Malate exchange", "Ammonia exchange", "O2 exchange",\n    "Phosphate exchange", "Pyruvate exchange", "Succinate exchange",\n    "Fructose-bisphosphate aldolase", "Fructose-bisphosphatase",\n    "Formate transport in via proton symport", "Formate transport via diffusion",\n    "Fumarate reductase", "Fructose transport via PEP:Pyr PTS (f6p generating)", "Fumarase",\n    "Fumarate transport via proton symport (2 H)", "Glucose 6-phosphate dehydrogenase",\n    "Glyceraldehyde-3-phosphate dehydrogenase", "D-glucose transport via PEP:Pyr PTS",\n    "Glutamine synthetase", "L-glutamine transport via ABC system",\n    "Glutamate dehydrogenase (NADP)", "Glutaminase", "Glutamate synthase (NADPH)",\n    "L glutamate transport via proton symport  reversible", "Phosphogluconate dehydrogenase",\n    "H2O transport via diffusion", "Isocitrate dehydrogenase (NADP)", "Isocitrate lyase",\n    "D-lactate dehydrogenase", "Malate synthase", "Malate transport via proton symport (2 H)",\n    "Malate dehydrogenase", "Malic enzyme (NAD)", "Malic enzyme (NADP)",\n    "NADH dehydrogenase (ubiquinone-8 & 3 protons)", "NAD transhydrogenase",\n    "Ammonia reversible transport", "O2 transport  diffusion ", "Pyruvate dehydrogenase",\n]\nS_columns = [   # S_columns[j]: (metabolite index (1-based), numerator, denominator) for each species in reaction j\n    [(9, 1, 1), (51, 1, 1), (55, -1, 1), (64, -1, 1), (65, 1, 1)],   # PFK\n    [(34, -1, 1), (44, 1, 1), (59, -1, 1), (66, 1, 1)],   # PFL\n    [(64, 1, 1), (72, -1, 1)],   # PGI\n    [(21, 1, 1), (26, -1, 1), (51, 1, 1), (55, -1, 1)],   # PGK\n    [(7, -1, 1), (9, 1, 1), (29, 1, 1), (31, -1, 1)],   # PGL\n    [(9, 1, 1), (16, -1, 1), (17, 1, 1), (41, -1, 1), (44, 1, 1), (59, -1, 1)],   # ACALD\n    [(9, 1, 1), (10, -1, 1), (52, 1, 1), (53, -1, 1)],   # AKGt2r\n    [(24, -1, 1), (26, 1, 1)],   # PGM\n    [(9, 1, 1), (10, -1, 1), (30, 1, 1), (32, -1, 1)],   # PIt2r\n    [(9, 1, 1), (16, -1, 1), (17, 1, 1), (41, 1, 1), (62, -1, 1)],   # ALCD2x\n    [(41, 1, 1), (43, -1, 1)],   # ACALDt\n    [(33, -1, 1), (50, 1, 1), (51, 1, 1), (55, -1, 1)],   # ACKr\n    [(7, -1, 1), (9, 1, 1), (27, 1, 1), (28, -1, 1), (30, 1, 1), (57, -1, 1)],   # PPC\n    [(7, 1, 1), (48, 1, 1), (56, -1, 1)],   # ACONTa\n    [(7, -1, 1), (11, 1, 1), (48, -1, 1)],   # ACONTb\n    [(7, -1, 1), (9, 1, 1), (30, 1, 1), (51, 1, 1), (55, -1, 1)],   # ATPM\n    [(27, -1, 1), (28, 1, 1), (51, 1, 1), (55, -1, 1), (57, 1, 1)],   # PPCK\n    [(9, 1, 1), (10, -1, 1), (33, 1, 1), (40, -1, 1)],   # ACt2r\n    [(7, -1, 1), (9, 2, 1), (28, 1, 1), (30, 1, 1), (34, -1, 1), (54, 1, 1), (55, -1, 1)],   # PPS\n    [(51, 2, 1), (54, -1, 1), (55, -1, 1)],   # ADK1\n    [(16, -1, 1), (17, 1, 1), (47, 1, 1), (52, -1, 1), (57, 1, 1), (59, -1, 1)],   # AKGDH\n    [(7, 1, 1), (9, 3, 1), (10, -4, 1), (30, -1, 1), (51, -1, 1), (55, 1, 1)],   # ATPS4r\n    [(30, -1, 1), (44, -1, 1), (50, 1, 1), (59, 1, 1)],   # PTAr\n    [(9, -1, 1), (28, -1, 1), (34, 1, 1), (51, -1, 1), (55, 1, 1)],   # PYK\n    [(2, -2557, 10000), (4, -24707, 5000), (7, -5981, 100), (9, 5981, 100), (16, -3547, 1000), (17, 3547, 1000), (18, 130279, 10000), (19, -130279, 10000), (26, -187, 125), (27, -17867, 10000), (28, -5191, 10000), (30, 5981, 100), (34, -3541, 1250), (38, -8977, 10000), (44, -18739, 5000), (51, 5981, 100), (52, 20591, 5000), (55, -5981, 100), (59, 18739, 5000), (61, -361, 1000), (64, -709, 10000), (71, -129, 1000), (72, -41, 200)],   # BIOMASS_Ecoli_core_w_GAM\n    [(9, 1, 1), (10, -1, 1), (34, 1, 1), (35, -1, 1)],   # PYRt2\n    [(57, 1, 1), (58, -1, 1)],   # CO2t\n    [(39, -1, 1), (49, 1, 1)],   # RPE\n    [(7, -1, 1), (9, 1, 1), (27, -1, 1), (44, -1, 1), (56, 1, 1), (59, 1, 1)],   # CS\n    [(38, -1, 1), (39, 1, 1)],   # RPI\n    [(9, 2, 1), (10, -2, 1), (45, 1, 1), (46, -1, 1)],   # SUCCt2_2\n    [(7, 1, 1), (9, -2, 1), (10, 2, 1), (23, -1, 2), (36, 1, 1), (37, -1, 1)],   # CYTBD\n    [(9, 1, 1), (10, -1, 1), (12, 1, 1), (13, -1, 1)],   # D_LACt2\n    [(7, 1, 1), (24, -1, 1), (28, 1, 1)],   # ENO\n    [(9, 1, 1), (10, -1, 1), (45, -1, 1), (46, 1, 1)],   # SUCCt3\n    [(9, 1, 1), (10, -1, 1), (62, 1, 1), (63, -1, 1)],   # ETOHt2r\n    [(36, -1, 1), (37, 1, 1), (45, -1, 1), (69, 1, 1)],   # SUCDi\n    [(30, 1, 1), (45, -1, 1), (47, 1, 1), (51, 1, 1), (55, -1, 1), (59, -1, 1)],   # SUCOAS\n    [(42, -1, 1), (61, 1, 1), (64, 1, 1), (71, -1, 1)],   # TALA\n    [(9, 2, 1), (10, -2, 1), (16, 1, 1), (17, -1, 1), (18, -1, 1), (19, 1, 1)],   # THD2\n    [(38, -1, 1), (42, 1, 1), (49, -1, 1), (71, 1, 1)],   # TKT1\n    [(49, -1, 1), (61, -1, 1), (64, 1, 1), (71, 1, 1)],   # TKT2\n    [(60, -1, 1), (71, 1, 1)],   # TPI\n    [(40, -1, 1)],   # EX_ac_e\n    [(43, -1, 1)],   # EX_acald_e\n    [(53, -1, 1)],   # EX_akg_e\n    [(58, -1, 1)],   # EX_co2_e\n    [(63, -1, 1)],   # EX_etoh_e\n    [(67, -1, 1)],   # EX_for_e\n    [(68, -1, 1)],   # EX_fru_e\n    [(70, -1, 1)],   # EX_fum_e\n    [(1, -1, 1)],   # EX_glc__D_e\n    [(3, -1, 1)],   # EX_gln__L_e\n    [(5, -1, 1)],   # EX_glu__L_e\n    [(10, -1, 1)],   # EX_h_e\n    [(8, -1, 1)],   # EX_h2o_e\n    [(13, -1, 1)],   # EX_lac__D_e\n    [(15, -1, 1)],   # EX_mal__L_e\n    [(22, -1, 1)],   # EX_nh4_e\n    [(25, -1, 1)],   # EX_o2_e\n    [(32, -1, 1)],   # EX_pi_e\n    [(35, -1, 1)],   # EX_pyr_e\n    [(46, -1, 1)],   # EX_succ_e\n    [(60, 1, 1), (65, -1, 1), (71, 1, 1)],   # FBA\n    [(7, -1, 1), (30, 1, 1), (64, 1, 1), (65, -1, 1)],   # FBP\n    [(9, 1, 1), (10, -1, 1), (66, 1, 1), (67, -1, 1)],   # FORt2\n    [(66, 1, 1), (67, -1, 1)],   # FORt\n    [(36, 1, 1), (37, -1, 1), (45, 1, 1), (69, -1, 1)],   # FRD7\n    [(28, -1, 1), (34, 1, 1), (64, 1, 1), (68, -1, 1)],   # FRUpts2\n    [(7, -1, 1), (14, 1, 1), (69, -1, 1)],   # FUM\n    [(9, 2, 1), (10, -2, 1), (69, 1, 1), (70, -1, 1)],   # FUMt2_2\n    [(9, 1, 1), (18, -1, 1), (19, 1, 1), (31, 1, 1), (72, -1, 1)],   # G6PDH2r\n    [(9, 1, 1), (16, -1, 1), (17, 1, 1), (21, 1, 1), (30, -1, 1), (71, -1, 1)],   # GAPD\n    [(1, -1, 1), (28, -1, 1), (34, 1, 1), (72, 1, 1)],   # GLCpts\n    [(2, 1, 1), (4, -1, 1), (9, 1, 1), (20, -1, 1), (30, 1, 1), (51, 1, 1), (55, -1, 1)],   # GLNS\n    [(2, 1, 1), (3, -1, 1), (7, -1, 1), (9, 1, 1), (30, 1, 1), (51, 1, 1), (55, -1, 1)],   # GLNabc\n    [(4, -1, 1), (7, -1, 1), (9, 1, 1), (18, -1, 1), (19, 1, 1), (20, 1, 1), (52, 1, 1)],   # GLUDy\n    [(2, -1, 1), (4, 1, 1), (7, -1, 1), (20, 1, 1)],   # GLUN\n    [(2, -1, 1), (4, 2, 1), (9, -1, 1), (18, 1, 1), (19, -1, 1), (52, -1, 1)],   # GLUSy\n    [(4, 1, 1), (5, -1, 1), (9, 1, 1), (10, -1, 1)],   # GLUt2r\n    [(18, -1, 1), (19, 1, 1), (29, -1, 1), (39, 1, 1), (57, 1, 1)],   # GND\n    [(7, 1, 1), (8, -1, 1)],   # H2Ot\n    [(11, -1, 1), (18, -1, 1), (19, 1, 1), (52, 1, 1), (57, 1, 1)],   # ICDHyr\n    [(6, 1, 1), (11, -1, 1), (45, 1, 1)],   # ICL\n    [(9, 1, 1), (12, -1, 1), (16, -1, 1), (17, 1, 1), (34, 1, 1)],   # LDH_D\n    [(6, -1, 1), (7, -1, 1), (9, 1, 1), (14, 1, 1), (44, -1, 1), (59, 1, 1)],   # MALS\n    [(9, 2, 1), (10, -2, 1), (14, 1, 1), (15, -1, 1)],   # MALt2_2\n    [(9, 1, 1), (14, -1, 1), (16, -1, 1), (17, 1, 1), (27, 1, 1)],   # MDH\n    [(14, -1, 1), (16, -1, 1), (17, 1, 1), (34, 1, 1), (57, 1, 1)],   # ME1\n    [(14, -1, 1), (18, -1, 1), (19, 1, 1), (34, 1, 1), (57, 1, 1)],   # ME2\n    [(9, -4, 1), (10, 3, 1), (16, 1, 1), (17, -1, 1), (36, -1, 1), (37, 1, 1)],   # NADH16\n    [(16, -1, 1), (17, 1, 1), (18, 1, 1), (19, -1, 1)],   # NADTRHD\n    [(20, 1, 1), (22, -1, 1)],   # NH4t\n    [(23, 1, 1), (25, -1, 1)],   # O2t\n    [(16, -1, 1), (17, 1, 1), (34, -1, 1), (44, 1, 1), (57, 1, 1), (59, -1, 1)],   # PDH\n]'),
        'matrix': ('Build S', 'm_ec, r_ec = length(met_ids), length(rxn_ids)\nS_ec_exact = zeros(Rational{BigInt}, m_ec, r_ec)\nfor (j, col) in enumerate(S_columns), (i, num, den) in col\n    S_ec_exact[i, j] = num // den\nend\nS_ec = Float64.(S_ec_exact)\nnnz_ec = count(!iszero, S_ec)\nprintln("$m_ec metabolites x $r_ec reactions, $nnz_ec nonzeros")'),
        'rank_ec': ('Rank and nullities', 'rank_ec = length(rref_exact(S_ec_exact)[2])\nK_ec = nullspace_exact(S_ec_exact)                # steady-state fluxes\nY_ec = nullspace_exact(permutedims(S_ec_exact))   # conservation laws\nsv_ec = svdvals(S_ec)\n@assert rank_ec == rank(S_ec)                     # exact and floating-point ranks agree\n@assert rank_ec + length(K_ec) == r_ec && rank_ec + length(Y_ec) == m_ec\nprintln("rank = $rank_ec  nullity = $(length(K_ec))  left nullity = $(length(Y_ec))")'),
        'moieties': ('Conserved moieties: the left null space', 'K_ec_f = Float64.(reduce(hcat, K_ec))             # r x nullity, one basis vector per column\nY_ec_f = Float64.(permutedims(reduce(hcat, Y_ec)))   # one conservation vector y per row\n@assert maximum(abs, Y_ec_f * S_ec) < 1e-9 && maximum(abs, S_ec * K_ec_f) < 1e-9\nmoieties = [met_ids[findall(!iszero, y)] for y in eachrow(Y_ec_f)]\ny_nad = Float64.(in(["nad_c", "nadh_c"]).(met_ids))\n@assert maximum(abs, y_nad\' * S_ec) < 1e-9        # NAD + NADH is one of them\nforeach(pool -> println(join(pool, " + ")), moieties)'),
        'elements': ('Atoms balance in every internal reaction', 'ELEMENTS = ["C", "H", "N", "O", "P", "S"]\nZ_ec = [get(atom_counts(f), e, 0) for e in ELEMENTS, f in met_formulas]\ninternal = [j for (j, rid) in enumerate(rxn_ids) if !startswith(rid, "EX_") && !startswith(rid, "BIOMASS")]\nS_int = S_ec[:, internal]\n@assert maximum(abs, Z_ec * S_int) < 1e-9          # Z s = 0 for every internal reaction\n@assert maximum(abs, met_charges\' * S_int) < 1e-9  # and charge balances too\nrank_int = rank(S_int)\nlaws_int = vcat(Z_ec, met_charges\', Y_ec_f)       # elements, charge, moieties\n@assert rank(laws_int) == m_ec - rank_int         # together they span the left null space\nprintln("$(length(internal)) internal reactions; rank $rank_int; left nullity $(m_ec - rank_int)")'),
        'coupled': ('Fully coupled reactions: the right null space', 'nonzero_rows = vec(maximum(abs, K_ec_f, dims=2)) .> 0   # a zero row: flux forced to 0 at steady state\nU_ec = K_ec_f ./ max.(norm.(eachrow(K_ec_f)), 1e-300)\ncoupled, seen = Vector{Vector{Int}}(), Set{Int}()\nfor j in findall(nonzero_rows)\n    if !(j in seen)                                 # parallel rows: fluxes in a fixed ratio\n        group = [i for i in findall(nonzero_rows) if abs(abs(dot(U_ec[j, :], U_ec[i, :])) - 1) < 1e-9]\n        union!(seen, group)\n        push!(coupled, group)\n    end\nend\n@assert sum(length, coupled) == count(nonzero_rows)   # every reaction is in exactly one group\nfor group in coupled\n    length(group) > 1 && println(join(rxn_ids[group], ", "))\nend'),
    }
    # END JULIA SNIPPETS
    return (julia_snippets,)


@app.cell(hide_code=True)
def _(julia_snippets, mo, show_julia):
    def julia(name, note=""):
        """The Julia version of one computation, shown only while the switch is on."""
        if not show_julia.value:
            return None
        title, code = julia_snippets[name]
        return mo.md(f"**Julia — {title}**{note}\n\n```julia\n{code}\n```")
    return (julia,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Part 1 — By hand

    ### Balancing an equation is a null-space problem

    Start with one reaction and no kinetics at all. Glucose burns in oxygen to carbon dioxide and
    water. The species are known; their coefficients $s$ (negative for what is consumed, positive
    for what is made) are the unknowns.

    Atoms are neither created nor destroyed. Take carbon first. A glucose molecule has 6 carbon
    atoms, $\mathrm{O_2}$ none, $\mathrm{CO_2}$ one and water none, so the carbon balance is

    $$6\,s_{\mathrm{glucose}} + 0\,s_{\mathrm{O_2}} + 1\,s_{\mathrm{CO_2}} + 0\,s_{\mathrm{H_2O}} = 0.$$

    The numbers $6, 0, 1, 0$ are the carbon row of the **atom-count matrix** $Z$: $z_{ei}$ is the
    number of atoms of element $e$ in one molecule of species $i$. One such row per element,
    stacked, gives

    $$Z\,s = 0.$$

    $Z$ is known from the molecular formulas. A balanced equation is an integer vector in the null
    space of $Z$. The cell below finds it in exact fractions, by row reduction, and then clears the
    denominators.
    """)
    return


@app.cell
def _(Fraction, gcd, lcm, re):
    def rref_exact(M):
        """Reduced row echelon form of M (rows of numbers) in exact fractions, and its pivot columns."""
        R = [[Fraction(x) for x in row] for row in M]
        pivots, top = [], 0
        for col in range(len(R[0])):
            p = next((i for i in range(top, len(R)) if R[i][col] != 0), None)
            if p is None:
                continue                       # no pivot here: col is a free column
            R[top], R[p] = R[p], R[top]
            R[top] = [x / R[top][col] for x in R[top]]
            for i in range(len(R)):
                if i != top and R[i][col] != 0:
                    f = R[i][col]
                    R[i] = [a - f * b for a, b in zip(R[i], R[top])]
            pivots.append(col)
            top += 1
            if top == len(R):
                break
        return R, pivots

    def nullspace_exact(M):
        """Basis of {x : M x = 0}: one vector per free column, with 1 there and 0 in the other free columns."""
        R, pivots = rref_exact(M)
        n = len(M[0])
        basis = []
        for f in (c for c in range(n) if c not in pivots):
            x = [Fraction(0)] * n
            x[f] = Fraction(1)
            for row, p in zip(R, pivots):
                x[p] = -row[f]
            basis.append(x)
        return basis

    def integer_vector(x):
        """x rescaled to the shortest vector of integers: clear denominators, divide out the common factor."""
        ints = [int(q * lcm(*(q.denominator for q in x))) for q in x]
        g = gcd(*ints)
        return [i // g for i in ints]

    def atom_counts(formula):
        """{element: number of atoms} for a formula such as 'C6H12O6'."""
        counts = {}
        for element, n in re.findall(r"([A-Z][a-z]?)(\d*)", formula):
            counts[element] = counts.get(element, 0) + (int(n) if n else 1)
        return counts
    return atom_counts, integer_vector, nullspace_exact, rref_exact


@app.cell(hide_code=True)
def _(julia):
    julia("setup")
    return


@app.cell
def _(mo):
    balance_examples = {
        "Respiration: glucose + oxygen → carbon dioxide + water": ["C6H12O6", "O2", "CO2", "H2O"],
        "Alcoholic fermentation: glucose → ethanol + carbon dioxide": ["C6H12O6", "C2H6O", "CO2"],
        "Ammonia synthesis: nitrogen + hydrogen → ammonia": ["N2", "H2", "NH3"],
        "Pitfall: hydrogen + oxygen → water + hydrogen peroxide": ["H2", "O2", "H2O", "H2O2"],
    }
    balance_choice = mo.ui.dropdown(options=list(balance_examples),
                                    value=next(iter(balance_examples)), label="Reaction")
    balance_choice
    return balance_choice, balance_examples


@app.cell
def _(atom_counts, balance_choice, balance_examples, integer_vector, nullspace_exact):
    species_bal = balance_examples[balance_choice.value]
    elements_bal = sorted({e for f in species_bal for e in atom_counts(f)})
    Z_bal = [[atom_counts(f).get(e, 0) for f in species_bal] for e in elements_bal]
    K_bal = nullspace_exact(Z_bal)
    s_bal_all = []
    for _k in K_bal:
        _s = integer_vector(_k)
        s_bal_all.append([-x for x in _s] if _s[0] > 0 else _s)   # first species consumed
    return K_bal, Z_bal, elements_bal, s_bal_all, species_bal


@app.cell(hide_code=True)
def _(julia):
    julia("balance", " (for respiration, the first reaction in the list)")
    return


@app.cell(hide_code=True)
def _(K_bal, Z_bal, elements_bal, equation_string, latex_matrix, mo, s_bal_all, species_bal):
    _cols = [r"\mathrm{" + f + "}" for f in species_bal]
    _Z = latex_matrix(Z_bal, [r"\text{" + e + "}" for e in elements_bal], _cols)
    if len(K_bal) == 1:
        _verdict = (f"The null space of $Z$ has dimension **1**, so there is exactly one balanced "
                    f"reaction, up to scale:\n\n**{equation_string(s_bal_all[0], species_bal)}**"
                    f"\n\nwith $s = ({', '.join(map(str, s_bal_all[0]))})$.")
    elif not K_bal:
        _verdict = ("The null space of $Z$ is just $\\{0\\}$: no choice of coefficients balances "
                    "these species.")
    else:
        _lines = "\n".join(f"- {equation_string(s, species_bal)}" for s in s_bal_all)
        _verdict = (f"**The null space of $Z$ has dimension {len(K_bal)}.** Every combination of "
                    f"these balanced reactions also balances:\n\n{_lines}\n\nThe species list "
                    "describes more than one reaction, so atom counting cannot say which "
                    "coefficients are meant. That has to come from the chemistry.")
    mo.md(f"$$Z = {_Z}$$\n\n"
          f"{len(elements_bal)} elements and {len(species_bal)} species: $Z$ is "
          f"{len(elements_bal)} × {len(species_bal)}, and $s$ lives in "
          f"$\\mathbb{{R}}^{{{len(species_bal)}}}$.\n\n{_verdict}")
    return


@app.cell(hide_code=True)
def _(atom_counts, integer_vector, mo, nullspace_exact):
    _sp = ["C6H12O6", "O2", "CO2", "H2O"]
    _Z = [[atom_counts(f).get(e, 0) for f in _sp] for e in ["C", "H", "O"]]
    _K = nullspace_exact(_Z)
    # the hand calculation below relies on these exact values
    assert _Z == [[6, 0, 1, 0], [12, 0, 0, 2], [6, 2, 2, 1]]
    assert len(_K) == 1 and integer_vector(_K[0]) in ([-1, -6, 6, 6], [1, 6, -6, -6])
    mo.md(r"""
    ### By hand, for respiration

    The carbon row gives $s_{\mathrm{CO_2}} = -6\,s_{\mathrm{glucose}}$. The hydrogen row,
    $12\,s_{\mathrm{glucose}} + 2\,s_{\mathrm{H_2O}} = 0$, gives
    $s_{\mathrm{H_2O}} = -6\,s_{\mathrm{glucose}}$. The oxygen row then reads

    $$6\,s_{\mathrm{glucose}} + 2\,s_{\mathrm{O_2}} + 2(-6\,s_{\mathrm{glucose}}) + (-6\,s_{\mathrm{glucose}}) = 0
    \quad\Longrightarrow\quad s_{\mathrm{O_2}} = 6\,s_{\mathrm{glucose}}.$$

    One coefficient is free, so the null space is a line. Choosing $s_{\mathrm{glucose}} = -1$
    (one glucose consumed) gives $s = (-1, -6, 6, 6)$:
    $\mathrm{C_6H_{12}O_6 + 6\,O_2 \to 6\,CO_2 + 6\,H_2O}$. The trial and error of first-year
    chemistry is Gaussian elimination on $Z$.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### A network of six reactions

    Now a network with kinetics. A nutrient $P$ is taken up, activated by spending one ATP, and
    converted to a product $R$ that leaves the cell. The conversion goes either through a step
    that makes two ATP, or through a bypass that makes none. A sixth reaction stands for
    everything else in the cell that spends ATP. (Phosphate and water are left out to keep the
    matrix small.)

    | Reaction | Equation | Rate under mass action |
    |---|---|---|
    | 1 | $\varnothing \to P$ | $v_1 = k_1$ |
    | 2 | $P + \mathrm{ATP} \to Q + \mathrm{ADP}$ | $v_2 = k_2\,[P]\,[\mathrm{ATP}]$ |
    | 3 | $Q + 2\,\mathrm{ADP} \to R + 2\,\mathrm{ATP}$ | $v_3 = k_3\,[Q]\,[\mathrm{ADP}]^2$ |
    | 4 | $R \to \varnothing$ | $v_4 = k_4\,[R]$ |
    | 5 | $\mathrm{ATP} \to \mathrm{ADP}$ | $v_5 = k_5\,[\mathrm{ATP}]$ |
    | 6 | $Q \to R$ | $v_6 = k_6\,[Q]$ |

    The rates follow the **law of mass action**: a reaction runs at a rate constant times the
    concentration of each reactant, raised to the number of molecules of it consumed. These rates
    are nonlinear in $c$, and the constants $k_j$ are what is rarely known.

    **One row first.** ATP is consumed once by reaction 2, produced twice by reaction 3, and
    consumed once by reaction 5. Nothing else touches it, so

    $$\frac{d[\mathrm{ATP}]}{dt} = -v_2 + 2\,v_3 - v_5 = (0,\ -1,\ 2,\ 0,\ -1,\ 0)\cdot v.$$

    That coefficient vector is the ATP row of $S$. Each species gets one such row; stacking them
    gives $dc/dt = S\,v$. $S$ is known from the equations alone. The fluxes $v$ and the
    concentrations $c(t)$ are unknown.
    """)
    return


@app.cell
def _():
    species_toy = ["P", "Q", "R", "ATP", "ADP"]
    #        reaction:  1   2   3   4   5   6
    S_toy = [          [1, -1,  0,  0,  0,  0],   # P
                       [0,  1, -1,  0,  0, -1],   # Q
                       [0,  0,  1, -1,  0,  1],   # R
                       [0, -1,  2,  0, -1,  0],   # ATP
                       [0,  1, -2,  0,  1,  0]]   # ADP
    m_toy, r_toy = len(S_toy), len(S_toy[0])      # 5 species, 6 reactions
    return S_toy, m_toy, r_toy, species_toy


@app.cell(hide_code=True)
def _(julia):
    julia("toy")
    return


@app.cell(hide_code=True)
def _(S_toy, latex_matrix, m_toy, mo, r_toy, species_toy):
    _rows = [r"\text{" + s + "}" for s in species_toy]
    _cols = [str(j) for j in range(1, r_toy + 1)]
    mo.md(f"$$S = {latex_matrix(S_toy, _rows, _cols)}$$\n\n"
          f"{m_toy} species by {r_toy} reactions. Each column is one reaction's equation; each "
          "row is one species' balance.")
    return


@app.cell
def _(S_toy, m_toy, nullspace_exact, r_toy, rref_exact):
    rank_toy = len(rref_exact(S_toy)[1])
    K_toy = nullspace_exact(S_toy)                              # S v = 0: flux space, R^6
    Y_toy = nullspace_exact([list(col) for col in zip(*S_toy)])  # y^T S = 0: species space, R^5
    assert rank_toy + len(K_toy) == r_toy and rank_toy + len(Y_toy) == m_toy
    return K_toy, Y_toy, rank_toy


@app.cell(hide_code=True)
def _(julia):
    julia("rank")
    return


@app.cell(hide_code=True)
def _(K_toy, Y_toy, integer_vector, latex_matrix, m_toy, md_table, mo, r_toy, rank_toy, species_toy,
      textwrap):
    # the hand calculation below relies on these exact values
    assert rank_toy == 4
    assert [integer_vector(k) for k in K_toy] == [[1, 1, 1, 1, 1, 0], [2, 2, 1, 2, 0, 1]]
    assert [integer_vector(y) for y in Y_toy] == [[0, 0, 0, 1, 1]]
    _K = latex_matrix([list(row) for row in zip(*K_toy)],
                      [f"v_{j}" for j in range(1, r_toy + 1)], ["K_1", "K_2"])
    _y = latex_matrix([[x] for x in Y_toy[0]], [r"\text{" + s + "}" for s in species_toy], ["y"])
    _book = md_table(
        ["space", "dimension", "rank of S", "null space", "rank + nullity"],
        [[f"flux space ℝ^{r_toy} (reactions)", f"r = {r_toy}", rank_toy,
          f"right null space, dimension {len(K_toy)}", f"{rank_toy} + {len(K_toy)} = {r_toy}"],
         [f"species space ℝ^{m_toy} (species)", f"m = {m_toy}", rank_toy,
          f"left null space, dimension {len(Y_toy)}", f"{rank_toy} + {len(Y_toy)} = {m_toy}"]])
    _text = textwrap.dedent(r"""
    ### Steady states and conservation laws, by hand

    **Right null space.** Set each row of $S v$ to zero. The $P$ row gives $v_1 = v_2$. The $Q$ and
    $R$ rows give $v_2 = v_3 + v_6$ and $v_4 = v_3 + v_6$. The ATP row, $2 v_3 = v_2 + v_5$, then
    gives $v_3 = v_5 + v_6$. So $v_5$ and $v_6$ are free, and every other flux follows from them.
    Setting each free flux to 1 in turn gives a basis, one vector per column:

    $$K = @K@$$

    $K_1$ runs every reaction at the same rate: each $P$ yields one ATP net ($-1$ in reaction 2,
    $+2$ in reaction 3), which reaction 5 spends. $K_2$ takes in two $P$ and sends one through each
    branch. The two ATP made pay for the two spent activating $P$, and nothing is left for
    reaction 5. Every steady state is $v = a K_1 + b K_2$. Since $v_5 = a$ and $v_6 = b$, the
    steady states with no negative flux are exactly those with $a, b \ge 0$. $K_1$ and $K_2$ are
    then the network's *elementary flux modes*. (In a bigger network, a basis from row reduction
    usually has negative entries, and the elementary modes have to be found separately.)

    **Left null space.** The ATP and ADP rows of $S$ are negatives of each other, and the rows of
    $P$, $Q$, $R$ and ATP are independent (that is the rank of 4), so

    $$y = @y@, \qquad y^\mathsf{T} S = 0, \qquad [\mathrm{ATP}] + [\mathrm{ADP}] = \text{constant}.$$

    Reactions 2, 3 and 5 turn ATP into ADP or back; reactions 1, 4 and 6 leave both alone.

    **Rank–nullity, in two different spaces.** The rank, @rank@, is the same counted by rows
    or by columns. The two null spaces live in different spaces and have different dimensions:

    @book@
    """)
    for _key, _val in [("@K@", _K), ("@y@", _y), ("@rank@", str(rank_toy)), ("@book@", _book)]:
        _text = _text.replace(_key, _val)
    mo.md(_text)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Run the kinetics: the concentrations move, ATP + ADP does not

    The conservation law came from $S$ alone, so it must hold for any rate constants. The cell
    below integrates $dc/dt = S\,v(c)$ with the mass-action rates and $k_1 = k_2 = k_3 = k_4 = 1$,
    $k_6 = 0.5$, starting with no $P$, $Q$ or $R$ and $[\mathrm{ADP}] = 0.5$. Change the ATP demand
    $k_5$ and the starting ATP.
    """)
    return


@app.cell
def _(mo):
    k5_slider = mo.ui.slider(0.1, 1.5, step=0.1, value=0.5, label="ATP demand k5", show_value=True)
    atp0_slider = mo.ui.slider(0.0, 2.0, step=0.1, value=1.5, label="Starting ATP",
                               show_value=True)
    mo.hstack([k5_slider, atp0_slider], justify="start", gap=2)
    return atp0_slider, k5_slider


@app.cell
def _(K_toy, S_toy, Y_toy, atp0_slider, k5_slider, np):
    k5, atp0 = k5_slider.value, atp0_slider.value
    k_toy = np.array([1.0, 1.0, 1.0, 1.0, k5, 0.5])
    S_toy_f = np.array(S_toy, dtype=float)

    def rates_toy(c):
        """Mass-action rates v(c) of the six reactions."""
        P, Q, R, ATP, ADP = c
        return k_toy * np.array([1.0, P * ATP, Q * ADP**2, R, ATP, Q])

    dt_toy, n_toy = 0.02, 3000                # 60 time units
    c_toy = np.array([0.0, 0.0, 0.0, atp0, 0.5])
    traj_toy = [c_toy]
    for _ in range(n_toy):                    # classical Runge-Kutta steps of dc/dt = S v(c)
        f1 = S_toy_f @ rates_toy(c_toy)
        f2 = S_toy_f @ rates_toy(c_toy + dt_toy / 2 * f1)
        f3 = S_toy_f @ rates_toy(c_toy + dt_toy / 2 * f2)
        f4 = S_toy_f @ rates_toy(c_toy + dt_toy * f3)
        c_toy = c_toy + dt_toy / 6 * (f1 + 2 * f2 + 2 * f3 + f4)
        traj_toy.append(c_toy)
    traj_toy = np.array(traj_toy)
    y_toy = np.array(Y_toy[0], dtype=float)
    total_toy = traj_toy @ y_toy              # ATP + ADP at every time step
    v_end = rates_toy(traj_toy[-1])
    ab_end = np.linalg.lstsq(np.array(K_toy, dtype=float).T, v_end, rcond=None)[0]   # v = a K1 + b K2
    assert np.abs(total_toy - total_toy[0]).max() < 1e-12    # conserved, whatever the kinetics
    return S_toy_f, ab_end, dt_toy, total_toy, traj_toy, v_end


@app.cell(hide_code=True)
def _(julia):
    julia("ode", " (with the default sliders: k5 = 0.5, starting ATP = 1.5)")
    return


@app.cell
def _(dt_toy, np, plt, species_toy, total_toy, traj_toy):
    _t = dt_toy * np.arange(len(traj_toy))
    _fig, _ax = plt.subplots(figsize=(7, 3.4))
    _colors = ["#64748b", "#94a3b8", "#0f766e", "#1d4ed8", "#d97706"]
    for _i, _name in enumerate(species_toy):
        _ax.plot(_t, traj_toy[:, _i], color=_colors[_i], lw=1.6, label=f"[{_name}]")
    _ax.plot(_t, total_toy, "k--", lw=1.2, label="[ATP] + [ADP]")
    _ax.set_xlabel("time")
    _ax.set_ylabel("concentration")
    _ax.set_title("Mass-action kinetics: every species moves, ATP + ADP stays fixed")
    _ax.legend(frameon=False, ncol=3, fontsize=8)
    _fig.tight_layout()
    _fig
    return


@app.cell(hide_code=True)
def _(S_toy_f, ab_end, dt_toy, mo, np, total_toy, traj_toy, v_end):
    _drift = np.abs(total_toy - total_toy[0]).max()
    _res = np.abs(S_toy_f @ v_end).max()
    _t_end = dt_toy * (len(traj_toy) - 1)
    _v = ", ".join(f"{x:.3f}" for x in v_end)
    if _res < 1e-6:
        _state = (f"By $t = {_t_end:.0f}$ the network has reached steady state "
                  f"($\\max |S v| = {_res:.1e}$). ")
    else:
        _state = (f"By $t = {_t_end:.0f}$ the network is still settling "
                  f"($\\max |S v| = {_res:.1e}$); the decomposition below is approximate. ")
    mo.md(
        f"$[\\mathrm{{ATP}}] + [\\mathrm{{ADP}}]$ stays at **{total_toy[0]:.2f}** throughout; its "
        f"largest change over the run is {_drift:.1e}, which is rounding error.\n\n"
        f"{_state}The fluxes there are $v = ({_v})$, which is "
        f"$a K_1 + b K_2$ with $a = {ab_end[0]:.3f}$ and $b = {ab_end[1]:.3f}$: a point in the "
        "right null space, as it must be. The kinetics decide *which* point. The conserved total "
        "matters too: change the starting ATP and the network settles at a different steady "
        "state, because each trajectory stays on its own plane $[\\mathrm{ATP}] + [\\mathrm{ADP}] = "
        "\\text{constant}$."
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Part 2 — The core metabolism of *E. coli*

    The same computations on a real network. The model is `e_coli_core` from the BiGG Models
    database: the central carbon metabolism of *E. coli* (glycolysis, the pentose phosphate
    pathway, the citric acid cycle, the glyoxylate shunt, oxidative phosphorylation and
    fermentation), a standard teaching model for genome-scale analysis. Besides the chemical
    reactions it has two kinds of bookkeeping reaction:

    - **exchange reactions** (`EX_…`), which let a metabolite in the medium enter or leave the
      system, like reactions 1 and 4 of the toy;
    - one **biomass reaction**, which drains the building blocks a cell needs to grow, in the
      proportions measured for *E. coli*. Its coefficients are measured rather than counted, so
      they are decimals rather than small integers.

    `data/prepare_ecoli_core.py` in the repository downloads the model from BiGG and writes its
    stoichiometric matrix into the cell below: for each reaction, the metabolites it uses and each
    coefficient as an exact fraction. Metabolite ids end in `_c` (cytoplasm) or `_e` (medium).
    """)
    return


@app.cell
def _():
    # BEGIN BIGG DATA (generated by data/prepare_ecoli_core.py; BiGG e_coli_core, 72 metabolites x 95 reactions, 360 nonzeros)
    met_ids = [
        'glc__D_e', 'gln__L_c', 'gln__L_e', 'glu__L_c', 'glu__L_e', 'glx_c', 'h2o_c', 'h2o_e',
        'h_c', 'h_e', 'icit_c', 'lac__D_c', 'lac__D_e', 'mal__L_c', 'mal__L_e', 'nad_c', 'nadh_c',
        'nadp_c', 'nadph_c', 'nh4_c', '13dpg_c', 'nh4_e', 'o2_c', '2pg_c', 'o2_e', '3pg_c',
        'oaa_c', 'pep_c', '6pgc_c', 'pi_c', '6pgl_c', 'pi_e', 'ac_c', 'pyr_c', 'pyr_e', 'q8_c',
        'q8h2_c', 'r5p_c', 'ru5p__D_c', 'ac_e', 'acald_c', 's7p_c', 'acald_e', 'accoa_c', 'succ_c',
        'succ_e', 'succoa_c', 'acon_C_c', 'xu5p__D_c', 'actp_c', 'adp_c', 'akg_c', 'akg_e',
        'amp_c', 'atp_c', 'cit_c', 'co2_c', 'co2_e', 'coa_c', 'dhap_c', 'e4p_c', 'etoh_c',
        'etoh_e', 'f6p_c', 'fdp_c', 'for_c', 'for_e', 'fru_e', 'fum_c', 'fum_e', 'g3p_c', 'g6p_c',
    ]
    met_names = [
        'D-Glucose', 'L-Glutamine', 'L-Glutamine', 'L-Glutamate', 'L-Glutamate', 'Glyoxylate',
        'H2O H2O', 'H2O H2O', 'H+', 'H+', 'Isocitrate', 'D-Lactate', 'D-Lactate', 'L-Malate',
        'L-Malate', 'Nicotinamide adenine dinucleotide',
        'Nicotinamide adenine dinucleotide - reduced',
        'Nicotinamide adenine dinucleotide phosphate',
        'Nicotinamide adenine dinucleotide phosphate - reduced', 'Ammonium',
        '3-Phospho-D-glyceroyl phosphate', 'Ammonium', 'O2 O2', 'D-Glycerate 2-phosphate', 'O2 O2',
        '3-Phospho-D-glycerate', 'Oxaloacetate', 'Phosphoenolpyruvate', '6-Phospho-D-gluconate',
        'Phosphate', '6-phospho-D-glucono-1,5-lactone', 'Phosphate', 'Acetate', 'Pyruvate',
        'Pyruvate', 'Ubiquinone-8', 'Ubiquinol-8', 'Alpha-D-Ribose 5-phosphate',
        'D-Ribulose 5-phosphate', 'Acetate', 'Acetaldehyde', 'Sedoheptulose 7-phosphate',
        'Acetaldehyde', 'Acetyl-CoA', 'Succinate', 'Succinate', 'Succinyl-CoA', 'Cis-Aconitate',
        'D-Xylulose 5-phosphate', 'Acetyl phosphate', 'ADP C10H12N5O10P2', '2-Oxoglutarate',
        '2-Oxoglutarate', 'AMP C10H12N5O7P', 'ATP C10H12N5O13P3', 'Citrate', 'CO2 CO2', 'CO2 CO2',
        'Coenzyme A', 'Dihydroxyacetone phosphate', 'D-Erythrose 4-phosphate', 'Ethanol',
        'Ethanol', 'D-Fructose 6-phosphate', 'D-Fructose 1,6-bisphosphate', 'Formate', 'Formate',
        'D-Fructose', 'Fumarate', 'Fumarate', 'Glyceraldehyde 3-phosphate',
        'D-Glucose 6-phosphate',
    ]
    met_formulas = [
        'C6H12O6', 'C5H10N2O3', 'C5H10N2O3', 'C5H8NO4', 'C5H8NO4', 'C2H1O3', 'H2O', 'H2O', 'H',
        'H', 'C6H5O7', 'C3H5O3', 'C3H5O3', 'C4H4O5', 'C4H4O5', 'C21H26N7O14P2', 'C21H27N7O14P2',
        'C21H25N7O17P3', 'C21H26N7O17P3', 'H4N', 'C3H4O10P2', 'H4N', 'O2', 'C3H4O7P', 'O2',
        'C3H4O7P', 'C4H2O5', 'C3H2O6P', 'C6H10O10P', 'HO4P', 'C6H9O9P', 'HO4P', 'C2H3O2', 'C3H3O3',
        'C3H3O3', 'C49H74O4', 'C49H76O4', 'C5H9O8P', 'C5H9O8P', 'C2H3O2', 'C2H4O', 'C7H13O10P',
        'C2H4O', 'C23H34N7O17P3S', 'C4H4O4', 'C4H4O4', 'C25H35N7O19P3S', 'C6H3O6', 'C5H9O8P',
        'C2H3O5P', 'C10H12N5O10P2', 'C5H4O5', 'C5H4O5', 'C10H12N5O7P', 'C10H12N5O13P3', 'C6H5O7',
        'CO2', 'CO2', 'C21H32N7O16P3S', 'C3H5O6P', 'C4H7O7P', 'C2H6O', 'C2H6O', 'C6H11O9P',
        'C6H10O12P2', 'CH1O2', 'CH1O2', 'C6H12O6', 'C4H2O4', 'C4H2O4', 'C3H5O6P', 'C6H11O9P',
    ]
    met_charges = [
        0, 0, 0, -1, -1, -1, 0, 0, 1, 1, -3, -1, -1, -2, -2, -1, -2, -3, -4, 1, -4, 1, 0, -3, 0,
        -3, -2, -3, -3, -2, -2, -2, -1, -1, -1, 0, 0, -2, -2, -1, 0, -2, 0, -4, -2, -2, -5, -3, -2,
        -2, -3, -2, -2, -2, -4, -3, 0, 0, -4, -2, -2, 0, 0, -2, -4, -1, -1, 0, -2, -2, -2, -2,
    ]
    rxn_ids = [
        'PFK', 'PFL', 'PGI', 'PGK', 'PGL', 'ACALD', 'AKGt2r', 'PGM', 'PIt2r', 'ALCD2x', 'ACALDt',
        'ACKr', 'PPC', 'ACONTa', 'ACONTb', 'ATPM', 'PPCK', 'ACt2r', 'PPS', 'ADK1', 'AKGDH',
        'ATPS4r', 'PTAr', 'PYK', 'BIOMASS_Ecoli_core_w_GAM', 'PYRt2', 'CO2t', 'RPE', 'CS', 'RPI',
        'SUCCt2_2', 'CYTBD', 'D_LACt2', 'ENO', 'SUCCt3', 'ETOHt2r', 'SUCDi', 'SUCOAS', 'TALA',
        'THD2', 'TKT1', 'TKT2', 'TPI', 'EX_ac_e', 'EX_acald_e', 'EX_akg_e', 'EX_co2_e',
        'EX_etoh_e', 'EX_for_e', 'EX_fru_e', 'EX_fum_e', 'EX_glc__D_e', 'EX_gln__L_e',
        'EX_glu__L_e', 'EX_h_e', 'EX_h2o_e', 'EX_lac__D_e', 'EX_mal__L_e', 'EX_nh4_e', 'EX_o2_e',
        'EX_pi_e', 'EX_pyr_e', 'EX_succ_e', 'FBA', 'FBP', 'FORt2', 'FORt', 'FRD7', 'FRUpts2',
        'FUM', 'FUMt2_2', 'G6PDH2r', 'GAPD', 'GLCpts', 'GLNS', 'GLNabc', 'GLUDy', 'GLUN', 'GLUSy',
        'GLUt2r', 'GND', 'H2Ot', 'ICDHyr', 'ICL', 'LDH_D', 'MALS', 'MALt2_2', 'MDH', 'ME1', 'ME2',
        'NADH16', 'NADTRHD', 'NH4t', 'O2t', 'PDH',
    ]
    rxn_names = [
        'Phosphofructokinase', 'Pyruvate formate lyase', 'Glucose-6-phosphate isomerase',
        'Phosphoglycerate kinase', '6-phosphogluconolactonase',
        'Acetaldehyde dehydrogenase (acetylating)',
        '2 oxoglutarate reversible transport via symport', 'Phosphoglycerate mutase',
        'Phosphate reversible transport via symport', 'Alcohol dehydrogenase (ethanol)',
        'Acetaldehyde reversible transport', 'Acetate kinase', 'Phosphoenolpyruvate carboxylase',
        'Aconitase (half-reaction A, Citrate hydro-lyase)',
        'Aconitase (half-reaction B, Isocitrate hydro-lyase)', 'ATP maintenance requirement',
        'Phosphoenolpyruvate carboxykinase', 'Acetate reversible transport via proton symport',
        'Phosphoenolpyruvate synthase', 'Adenylate kinase', '2-Oxogluterate dehydrogenase',
        'ATP synthase (four protons for one ATP)', 'Phosphotransacetylase', 'Pyruvate kinase',
        'Biomass Objective Function with GAM', 'Pyruvate transport in via proton symport',
        'CO2 transporter via diffusion', 'Ribulose 5-phosphate 3-epimerase', 'Citrate synthase',
        'Ribose-5-phosphate isomerase', 'Succinate transport via proton symport (2 H)',
        'Cytochrome oxidase bd (ubiquinol-8: 2 protons)', 'D lactate transport via proton symport',
        'Enolase', 'Succinate transport out via proton antiport',
        'Ethanol reversible transport via proton symport',
        'Succinate dehydrogenase (irreversible)', 'Succinyl-CoA synthetase (ADP-forming)',
        'Transaldolase', 'NAD(P) transhydrogenase', 'Transketolase', 'Transketolase',
        'Triose-phosphate isomerase', 'Acetate exchange', 'Acetaldehyde exchange',
        '2-Oxoglutarate exchange', 'CO2 exchange', 'Ethanol exchange', 'Formate exchange',
        'D-Fructose exchange', 'Fumarate exchange', 'D-Glucose exchange', 'L-Glutamine exchange',
        'L-Glutamate exchange', 'H+ exchange', 'H2O exchange', 'D-lactate exchange',
        'L-Malate exchange', 'Ammonia exchange', 'O2 exchange', 'Phosphate exchange',
        'Pyruvate exchange', 'Succinate exchange', 'Fructose-bisphosphate aldolase',
        'Fructose-bisphosphatase', 'Formate transport in via proton symport',
        'Formate transport via diffusion', 'Fumarate reductase',
        'Fructose transport via PEP:Pyr PTS (f6p generating)', 'Fumarase',
        'Fumarate transport via proton symport (2 H)', 'Glucose 6-phosphate dehydrogenase',
        'Glyceraldehyde-3-phosphate dehydrogenase', 'D-glucose transport via PEP:Pyr PTS',
        'Glutamine synthetase', 'L-glutamine transport via ABC system',
        'Glutamate dehydrogenase (NADP)', 'Glutaminase', 'Glutamate synthase (NADPH)',
        'L glutamate transport via proton symport  reversible', 'Phosphogluconate dehydrogenase',
        'H2O transport via diffusion', 'Isocitrate dehydrogenase (NADP)', 'Isocitrate lyase',
        'D-lactate dehydrogenase', 'Malate synthase', 'Malate transport via proton symport (2 H)',
        'Malate dehydrogenase', 'Malic enzyme (NAD)', 'Malic enzyme (NADP)',
        'NADH dehydrogenase (ubiquinone-8 & 3 protons)', 'NAD transhydrogenase',
        'Ammonia reversible transport', 'O2 transport  diffusion ', 'Pyruvate dehydrogenase',
    ]
    S_columns = [   # S_columns[j]: (metabolite index (0-based), numerator, denominator) for each species in reaction j
        [(8, 1, 1), (50, 1, 1), (54, -1, 1), (63, -1, 1), (64, 1, 1)],   # PFK
        [(33, -1, 1), (43, 1, 1), (58, -1, 1), (65, 1, 1)],   # PFL
        [(63, 1, 1), (71, -1, 1)],   # PGI
        [(20, 1, 1), (25, -1, 1), (50, 1, 1), (54, -1, 1)],   # PGK
        [(6, -1, 1), (8, 1, 1), (28, 1, 1), (30, -1, 1)],   # PGL
        [(8, 1, 1), (15, -1, 1), (16, 1, 1), (40, -1, 1), (43, 1, 1), (58, -1, 1)],   # ACALD
        [(8, 1, 1), (9, -1, 1), (51, 1, 1), (52, -1, 1)],   # AKGt2r
        [(23, -1, 1), (25, 1, 1)],   # PGM
        [(8, 1, 1), (9, -1, 1), (29, 1, 1), (31, -1, 1)],   # PIt2r
        [(8, 1, 1), (15, -1, 1), (16, 1, 1), (40, 1, 1), (61, -1, 1)],   # ALCD2x
        [(40, 1, 1), (42, -1, 1)],   # ACALDt
        [(32, -1, 1), (49, 1, 1), (50, 1, 1), (54, -1, 1)],   # ACKr
        [(6, -1, 1), (8, 1, 1), (26, 1, 1), (27, -1, 1), (29, 1, 1), (56, -1, 1)],   # PPC
        [(6, 1, 1), (47, 1, 1), (55, -1, 1)],   # ACONTa
        [(6, -1, 1), (10, 1, 1), (47, -1, 1)],   # ACONTb
        [(6, -1, 1), (8, 1, 1), (29, 1, 1), (50, 1, 1), (54, -1, 1)],   # ATPM
        [(26, -1, 1), (27, 1, 1), (50, 1, 1), (54, -1, 1), (56, 1, 1)],   # PPCK
        [(8, 1, 1), (9, -1, 1), (32, 1, 1), (39, -1, 1)],   # ACt2r
        [(6, -1, 1), (8, 2, 1), (27, 1, 1), (29, 1, 1), (33, -1, 1), (53, 1, 1), (54, -1, 1)],   # PPS
        [(50, 2, 1), (53, -1, 1), (54, -1, 1)],   # ADK1
        [(15, -1, 1), (16, 1, 1), (46, 1, 1), (51, -1, 1), (56, 1, 1), (58, -1, 1)],   # AKGDH
        [(6, 1, 1), (8, 3, 1), (9, -4, 1), (29, -1, 1), (50, -1, 1), (54, 1, 1)],   # ATPS4r
        [(29, -1, 1), (43, -1, 1), (49, 1, 1), (58, 1, 1)],   # PTAr
        [(8, -1, 1), (27, -1, 1), (33, 1, 1), (50, -1, 1), (54, 1, 1)],   # PYK
        [(1, -2557, 10000), (3, -24707, 5000), (6, -5981, 100), (8, 5981, 100), (15, -3547, 1000), (16, 3547, 1000), (17, 130279, 10000), (18, -130279, 10000), (25, -187, 125), (26, -17867, 10000), (27, -5191, 10000), (29, 5981, 100), (33, -3541, 1250), (37, -8977, 10000), (43, -18739, 5000), (50, 5981, 100), (51, 20591, 5000), (54, -5981, 100), (58, 18739, 5000), (60, -361, 1000), (63, -709, 10000), (70, -129, 1000), (71, -41, 200)],   # BIOMASS_Ecoli_core_w_GAM
        [(8, 1, 1), (9, -1, 1), (33, 1, 1), (34, -1, 1)],   # PYRt2
        [(56, 1, 1), (57, -1, 1)],   # CO2t
        [(38, -1, 1), (48, 1, 1)],   # RPE
        [(6, -1, 1), (8, 1, 1), (26, -1, 1), (43, -1, 1), (55, 1, 1), (58, 1, 1)],   # CS
        [(37, -1, 1), (38, 1, 1)],   # RPI
        [(8, 2, 1), (9, -2, 1), (44, 1, 1), (45, -1, 1)],   # SUCCt2_2
        [(6, 1, 1), (8, -2, 1), (9, 2, 1), (22, -1, 2), (35, 1, 1), (36, -1, 1)],   # CYTBD
        [(8, 1, 1), (9, -1, 1), (11, 1, 1), (12, -1, 1)],   # D_LACt2
        [(6, 1, 1), (23, -1, 1), (27, 1, 1)],   # ENO
        [(8, 1, 1), (9, -1, 1), (44, -1, 1), (45, 1, 1)],   # SUCCt3
        [(8, 1, 1), (9, -1, 1), (61, 1, 1), (62, -1, 1)],   # ETOHt2r
        [(35, -1, 1), (36, 1, 1), (44, -1, 1), (68, 1, 1)],   # SUCDi
        [(29, 1, 1), (44, -1, 1), (46, 1, 1), (50, 1, 1), (54, -1, 1), (58, -1, 1)],   # SUCOAS
        [(41, -1, 1), (60, 1, 1), (63, 1, 1), (70, -1, 1)],   # TALA
        [(8, 2, 1), (9, -2, 1), (15, 1, 1), (16, -1, 1), (17, -1, 1), (18, 1, 1)],   # THD2
        [(37, -1, 1), (41, 1, 1), (48, -1, 1), (70, 1, 1)],   # TKT1
        [(48, -1, 1), (60, -1, 1), (63, 1, 1), (70, 1, 1)],   # TKT2
        [(59, -1, 1), (70, 1, 1)],   # TPI
        [(39, -1, 1)],   # EX_ac_e
        [(42, -1, 1)],   # EX_acald_e
        [(52, -1, 1)],   # EX_akg_e
        [(57, -1, 1)],   # EX_co2_e
        [(62, -1, 1)],   # EX_etoh_e
        [(66, -1, 1)],   # EX_for_e
        [(67, -1, 1)],   # EX_fru_e
        [(69, -1, 1)],   # EX_fum_e
        [(0, -1, 1)],   # EX_glc__D_e
        [(2, -1, 1)],   # EX_gln__L_e
        [(4, -1, 1)],   # EX_glu__L_e
        [(9, -1, 1)],   # EX_h_e
        [(7, -1, 1)],   # EX_h2o_e
        [(12, -1, 1)],   # EX_lac__D_e
        [(14, -1, 1)],   # EX_mal__L_e
        [(21, -1, 1)],   # EX_nh4_e
        [(24, -1, 1)],   # EX_o2_e
        [(31, -1, 1)],   # EX_pi_e
        [(34, -1, 1)],   # EX_pyr_e
        [(45, -1, 1)],   # EX_succ_e
        [(59, 1, 1), (64, -1, 1), (70, 1, 1)],   # FBA
        [(6, -1, 1), (29, 1, 1), (63, 1, 1), (64, -1, 1)],   # FBP
        [(8, 1, 1), (9, -1, 1), (65, 1, 1), (66, -1, 1)],   # FORt2
        [(65, 1, 1), (66, -1, 1)],   # FORt
        [(35, 1, 1), (36, -1, 1), (44, 1, 1), (68, -1, 1)],   # FRD7
        [(27, -1, 1), (33, 1, 1), (63, 1, 1), (67, -1, 1)],   # FRUpts2
        [(6, -1, 1), (13, 1, 1), (68, -1, 1)],   # FUM
        [(8, 2, 1), (9, -2, 1), (68, 1, 1), (69, -1, 1)],   # FUMt2_2
        [(8, 1, 1), (17, -1, 1), (18, 1, 1), (30, 1, 1), (71, -1, 1)],   # G6PDH2r
        [(8, 1, 1), (15, -1, 1), (16, 1, 1), (20, 1, 1), (29, -1, 1), (70, -1, 1)],   # GAPD
        [(0, -1, 1), (27, -1, 1), (33, 1, 1), (71, 1, 1)],   # GLCpts
        [(1, 1, 1), (3, -1, 1), (8, 1, 1), (19, -1, 1), (29, 1, 1), (50, 1, 1), (54, -1, 1)],   # GLNS
        [(1, 1, 1), (2, -1, 1), (6, -1, 1), (8, 1, 1), (29, 1, 1), (50, 1, 1), (54, -1, 1)],   # GLNabc
        [(3, -1, 1), (6, -1, 1), (8, 1, 1), (17, -1, 1), (18, 1, 1), (19, 1, 1), (51, 1, 1)],   # GLUDy
        [(1, -1, 1), (3, 1, 1), (6, -1, 1), (19, 1, 1)],   # GLUN
        [(1, -1, 1), (3, 2, 1), (8, -1, 1), (17, 1, 1), (18, -1, 1), (51, -1, 1)],   # GLUSy
        [(3, 1, 1), (4, -1, 1), (8, 1, 1), (9, -1, 1)],   # GLUt2r
        [(17, -1, 1), (18, 1, 1), (28, -1, 1), (38, 1, 1), (56, 1, 1)],   # GND
        [(6, 1, 1), (7, -1, 1)],   # H2Ot
        [(10, -1, 1), (17, -1, 1), (18, 1, 1), (51, 1, 1), (56, 1, 1)],   # ICDHyr
        [(5, 1, 1), (10, -1, 1), (44, 1, 1)],   # ICL
        [(8, 1, 1), (11, -1, 1), (15, -1, 1), (16, 1, 1), (33, 1, 1)],   # LDH_D
        [(5, -1, 1), (6, -1, 1), (8, 1, 1), (13, 1, 1), (43, -1, 1), (58, 1, 1)],   # MALS
        [(8, 2, 1), (9, -2, 1), (13, 1, 1), (14, -1, 1)],   # MALt2_2
        [(8, 1, 1), (13, -1, 1), (15, -1, 1), (16, 1, 1), (26, 1, 1)],   # MDH
        [(13, -1, 1), (15, -1, 1), (16, 1, 1), (33, 1, 1), (56, 1, 1)],   # ME1
        [(13, -1, 1), (17, -1, 1), (18, 1, 1), (33, 1, 1), (56, 1, 1)],   # ME2
        [(8, -4, 1), (9, 3, 1), (15, 1, 1), (16, -1, 1), (35, -1, 1), (36, 1, 1)],   # NADH16
        [(15, -1, 1), (16, 1, 1), (17, 1, 1), (18, -1, 1)],   # NADTRHD
        [(19, 1, 1), (21, -1, 1)],   # NH4t
        [(22, 1, 1), (24, -1, 1)],   # O2t
        [(15, -1, 1), (16, 1, 1), (33, -1, 1), (43, 1, 1), (56, 1, 1), (58, -1, 1)],   # PDH
    ]
    # END BIGG DATA
    return S_columns, met_charges, met_formulas, met_ids, met_names, rxn_ids, rxn_names


@app.cell(hide_code=True)
def _(julia):
    julia("data", " (the same model, as Julia literals)")
    return


@app.cell
def _(Fraction, S_columns, met_ids, np, rxn_ids):
    m_ec, r_ec = len(met_ids), len(rxn_ids)
    S_ec_exact = [[Fraction(0)] * r_ec for _ in range(m_ec)]
    for _j, _col in enumerate(S_columns):
        for _i, _num, _den in _col:
            S_ec_exact[_i][_j] = Fraction(_num, _den)
    S_ec = np.array(S_ec_exact, dtype=float)
    nnz_ec = int((S_ec != 0).sum())
    return S_ec, S_ec_exact, m_ec, nnz_ec, r_ec


@app.cell(hide_code=True)
def _(julia):
    julia("matrix")
    return


@app.cell(hide_code=True)
def _(S_ec, m_ec, mo, nnz_ec, np, r_ec, rxn_ids):
    _n_ex = sum(r.startswith("EX_") for r in rxn_ids)
    _n_bio = sum(r.startswith("BIOMASS") for r in rxn_ids)
    _non_int = int((S_ec != np.round(S_ec)).sum())
    mo.md(
        f"$S$ is **{m_ec} × {r_ec}**: {m_ec} metabolites, and {r_ec} reactions of which {_n_ex} "
        f"are exchanges and {_n_bio} is the biomass reaction. Only {nnz_ec} of its "
        f"{m_ec * r_ec:,} entries are nonzero ({100 * nnz_ec / (m_ec * r_ec):.1f}%), and "
        f"{_non_int} of those are not integers. A typical reaction touches "
        f"{np.median((S_ec != 0).sum(axis=0)):.0f} metabolites."
    )
    return


@app.cell
def _(S_ec, met_ids, np, plt, rxn_ids):
    _order = sorted(range(len(rxn_ids)), key=lambda j: (rxn_ids[j].startswith("BIOMASS"),
                                                         rxn_ids[j].startswith("EX_")))
    _n_int = sum(not r.startswith(("EX_", "BIOMASS")) for r in rxn_ids)
    _sgn = np.sign(S_ec[:, _order])
    _fig, _ax = plt.subplots(figsize=(11, 8.2))
    for _val, _color, _label in [(-1, "#b91c1c", "consumed (s < 0)"), (1, "#1d4ed8", "produced (s > 0)")]:
        _ii, _jj = np.nonzero(_sgn == _val)
        _ax.scatter(_jj, _ii, s=9, marker="s", color=_color, label=_label)
    for _x in (_n_int - 0.5, len(rxn_ids) - 1.5):
        _ax.axvline(_x, color="#555", lw=0.8)
    _ax.set_xticks(range(len(rxn_ids)), [rxn_ids[j] for j in _order], rotation=90, fontsize=4.5)
    _ax.set_yticks(range(len(met_ids)), met_ids, fontsize=4.5)
    _ax.set_xlim(-1, len(rxn_ids))
    _ax.set_ylim(len(met_ids), -1)
    _ax.set_xlabel("reaction j (internal | exchange | biomass)")
    _ax.set_ylabel("metabolite i")
    _ax.set_title("Sign pattern of S for E. coli core")
    _ax.legend(frameon=False, loc="upper right", bbox_to_anchor=(1.0, 1.06), ncol=2, fontsize=8)
    _fig.tight_layout()
    _fig
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Rank and the two nullities

    Row reduction in exact fractions gives the rank and a basis for each null space with no
    rounding. The rank is checked against NumPy's floating-point rank, which counts the singular
    values above a tolerance.
    """)
    return


@app.cell
def _(S_ec, S_ec_exact, m_ec, np, nullspace_exact, r_ec, rref_exact):
    rank_ec = len(rref_exact(S_ec_exact)[1])
    K_ec = nullspace_exact(S_ec_exact)                                # steady-state fluxes
    Y_ec = nullspace_exact([list(col) for col in zip(*S_ec_exact)])   # conservation laws
    sv_ec = np.linalg.svd(S_ec, compute_uv=False)
    assert rank_ec == np.linalg.matrix_rank(S_ec)        # exact and floating-point ranks agree
    assert rank_ec + len(K_ec) == r_ec and rank_ec + len(Y_ec) == m_ec
    return K_ec, Y_ec, rank_ec, sv_ec


@app.cell(hide_code=True)
def _(julia):
    julia("rank_ec")
    return


@app.cell(hide_code=True)
def _(K_ec, Y_ec, m_ec, md_table, mo, r_ec, rank_ec):
    _book = md_table(
        ["space", "dimension", "rank of S", "null space", "rank + nullity"],
        [[f"flux space ℝ^{r_ec}", f"r = {r_ec}", rank_ec, f"right, dimension {len(K_ec)}",
          f"{rank_ec} + {len(K_ec)} = {r_ec}"],
         [f"species space ℝ^{m_ec}", f"m = {m_ec}", rank_ec, f"left, dimension {len(Y_ec)}",
          f"{rank_ec} + {len(Y_ec)} = {m_ec}"]])
    mo.md(
        f"The rank is **{rank_ec}**: of the {r_ec} reactions, only {rank_ec} are independent as "
        f"directions in species space. At steady state the network has **{len(K_ec)}** degrees "
        f"of freedom (the dimension of the right null space), and there are **{len(Y_ec)}** "
        "independent conservation laws (the dimension of the left null space).\n\n" + _book
    )
    return


@app.cell
def _(Y_ec, m_ec, np, plt, rank_ec, sv_ec):
    _fig, _ax = plt.subplots(figsize=(7, 3.4))
    _k = np.arange(1, len(sv_ec) + 1)
    _floor = 1e-17
    _ax.semilogy(_k, np.maximum(sv_ec, _floor), "o", ms=3.5, color="#1d4ed8")
    _ax.axvline(rank_ec + 0.5, color="#d97706", lw=1)
    _ax.text(rank_ec + 0.2, sv_ec[0], f"rank {rank_ec}", ha="right", va="top", fontsize=9,
             color="#d97706")
    _ax.set_xlabel("index k")
    _ax.set_ylabel("singular value $\\sigma_k$")
    _ax.set_title(f"{m_ec} singular values of S; the last {len(Y_ec)} are rounding-level zeros")
    _fig.tight_layout()
    _fig
    return


@app.cell(hide_code=True)
def _(K_ec, Y_ec, m_ec, mo, r_ec, rank_ec, sv_ec):
    _n_zero = int((sv_ec < 1e-10 * sv_ec[0]).sum())
    mo.md(
        f"$S$ has min(m, r) = {len(sv_ec)} singular values. The gap after the {rank_ec}th "
        f"(from {sv_ec[rank_ec - 1]:.3f} to {sv_ec[rank_ec]:.1e}) is the rank, and the "
        f"{_n_zero} zero singular values are the {len(Y_ec)} conservation laws. The "
        f"{len(K_ec)} steady-state degrees of freedom do not all show up here: S is wider than it "
        f"is tall, so {r_ec - m_ec} of them ({r_ec} − {m_ec}) are guaranteed by its shape alone."
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Conserved moieties: the left null space

    A conservation vector $y$ assigns a weight to each metabolite so that $y^\mathsf{T} c$ never
    changes. Biochemists call such a conserved group a **moiety**: a chemical unit that is passed
    from molecule to molecule but never made or destroyed within the network.
    """)
    return


@app.cell
def _(K_ec, S_ec, Y_ec, met_ids, np):
    K_ec_f = np.array(K_ec, dtype=float).T               # r x nullity, one basis vector per column
    Y_ec_f = np.array(Y_ec, dtype=float)                 # one conservation vector y per row
    assert np.abs(Y_ec_f @ S_ec).max() < 1e-9 and np.abs(S_ec @ K_ec_f).max() < 1e-9
    moieties = [[met_ids[i] for i in np.flatnonzero(y)] for y in Y_ec_f]
    y_nad = np.isin(met_ids, ["nad_c", "nadh_c"]).astype(float)
    assert np.abs(y_nad @ S_ec).max() < 1e-9             # NAD + NADH is one of them
    return K_ec_f, Y_ec_f, moieties


@app.cell(hide_code=True)
def _(julia):
    julia("moieties")
    return


@app.cell(hide_code=True)
def _(S_ec, S_ec_exact, Y_ec, Y_ec_f, md_table, met_ids, met_names, mo, np, rxn_ids):
    _rows = []
    for _k, _y in enumerate(Y_ec):
        _idx = [i for i, x in enumerate(_y) if x != 0]
        _ids = " + ".join(("" if _y[i] == 1 else f"{_y[i]} ") + f"`{met_ids[i]}`" for i in _idx)
        _names = "; ".join(met_names[i] for i in _idx)
        _touch = int((np.abs(S_ec[_idx, :]).sum(axis=0) > 0).sum())
        _rows.append([_k + 1, _ids, _names, _touch])
    _clean = all(set(_y) <= {0, 1} for _y in Y_ec)
    _bio = next(j for j, r in enumerate(rxn_ids) if r.startswith("BIOMASS"))
    _atp, _adp = met_ids.index("atp_c"), met_ids.index("adp_c")
    mo.md(
        f"Row reduction returns these {len(Y_ec)} basis vectors"
        + (", every weight 0 or 1" if _clean else "") + ":\n\n"
        + md_table(["y", "conserved pool", "names", "reactions involved"], _rows)
        + f"\n\nEach pool is a carrier that the network recycles but never synthesizes: the "
        "redox carriers NAD and NADP, the quinone of the respiratory chain, the adenine "
        "nucleotides, and coenzyme A. Even the biomass reaction respects them: it spends "
        f"{float(-S_ec_exact[_atp][_bio]):g} ATP and returns {float(S_ec_exact[_adp][_bio]):g} ADP. A real cell "
        "does make these carriers, but in pathways this model leaves out, so here each total is "
        f"fixed. The vectors are checked: the largest entry of $Y S$ is "
        f"{np.abs(Y_ec_f @ S_ec).max():.1e}."
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Close the network and the atoms come back

    Part 1 balanced one equation by asking $Z s = 0$. Every chemical reaction in a curated model
    should pass the same test. Take the formulas BiGG gives for the metabolites, build $Z$ (one row
    per element), and test every internal reaction: everything except the exchanges and the
    biomass reaction.

    If all of them balance, then each row of $Z$ is a conservation vector of the *closed*
    network: total carbon, total nitrogen, and so on. The exchange reactions destroy those laws
    in the open network, because atoms enter and leave through them.
    """)
    return


@app.cell
def _(S_ec, Y_ec_f, atom_counts, m_ec, met_charges, met_formulas, np, rxn_ids):
    ELEMENTS = ["C", "H", "N", "O", "P", "S"]
    Z_ec = np.array([[atom_counts(f).get(e, 0) for f in met_formulas] for e in ELEMENTS])
    internal = [j for j, rid in enumerate(rxn_ids) if not rid.startswith(("EX_", "BIOMASS"))]
    S_int = S_ec[:, internal]
    assert np.abs(Z_ec @ S_int).max() < 1e-9               # Z s = 0 for every internal reaction
    assert np.abs(np.array(met_charges) @ S_int).max() < 1e-9   # and charge balances too
    rank_int = np.linalg.matrix_rank(S_int)
    laws_int = np.vstack([Z_ec, met_charges, Y_ec_f])    # elements, charge, moieties
    assert np.linalg.matrix_rank(laws_int) == m_ec - rank_int   # together they span the left null space
    return ELEMENTS, Z_ec, internal, laws_int, rank_int


@app.cell(hide_code=True)
def _(julia):
    julia("elements")
    return


@app.cell(hide_code=True)
def _(ELEMENTS, S_ec, Y_ec, Z_ec, internal, laws_int, m_ec, md_table, mo, np, r_ec, rank_int, rxn_ids):
    _open = [j for j in range(r_ec) if j not in internal]
    _broken = [j for j in _open if np.abs(Z_ec @ S_ec[:, j]).max() > 1e-9]
    _rows = [["open (all reactions)", r_ec, int(np.linalg.matrix_rank(S_ec)),
              m_ec - int(np.linalg.matrix_rank(S_ec)), f"the {len(Y_ec)} moieties"],
             ["closed (internal only)", len(internal), rank_int, m_ec - rank_int,
              f"{len(ELEMENTS)} elements, charge, the {len(Y_ec)} moieties"]]
    mo.md(
        f"All **{len(internal)}** internal reactions balance every element "
        f"({', '.join(ELEMENTS)}) and charge. Of the {len(_open)} exchange and biomass "
        f"reactions, {len(_broken)} change the atom counts, as they should: "
        f"{', '.join('`' + rxn_ids[j] + '`' for j in _broken[:4])}, ….\n\n"
        + md_table(["network", "reactions r", "rank", "left nullity", "spanned by"], _rows)
        + f"\n\nFor the closed network the {len(ELEMENTS)} element rows, the charge row and the "
        f"{len(Y_ec)} moiety vectors are {laws_int.shape[0]} vectors of rank "
        f"{np.linalg.matrix_rank(laws_int)}, exactly the dimension of the left null space, so "
        f"they span it"
        + (" (one of them is a combination of the others)."
           if laws_int.shape[0] > np.linalg.matrix_rank(laws_int) else ".")
        + " A row-reduction basis of the same space is far less readable: a basis of a null "
        "space is not unique, and the one elimination hands back depends on the order of the "
        "columns. Finding the chemically meaningful basis is the interpretive step."
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Fully coupled reactions: the right null space

    Each steady-state flux is $v = K a$ for some coefficient vector $a$, so reaction $j$'s flux is
    row $j$ of $K$ times $a$. Two consequences can be read straight off $K$:

    - a zero row means that reaction's flux is zero at *every* steady state (a blocked reaction);
    - two parallel rows mean the two fluxes stand in a fixed ratio at every steady state. Such
      reactions are **fully coupled**: they behave as one unit, typically the steps of an
      unbranched stretch of pathway.

    Neither test depends on the basis chosen, because a change of basis multiplies every row of
    $K$ by the same invertible matrix.
    """)
    return


@app.cell
def _(K_ec_f, np):
    nonzero_rows = np.abs(K_ec_f).max(axis=1) > 0        # a zero row: flux forced to 0 at steady state
    U_ec = K_ec_f / np.maximum(np.linalg.norm(K_ec_f, axis=1, keepdims=True), 1e-300)
    coupled, seen = [], set()
    for j in np.flatnonzero(nonzero_rows):
        if j not in seen:                                # parallel rows: fluxes in a fixed ratio
            group = [i for i in np.flatnonzero(nonzero_rows) if abs(abs(U_ec[j] @ U_ec[i]) - 1) < 1e-9]
            seen.update(group)
            coupled.append(group)
    assert sum(map(len, coupled)) == nonzero_rows.sum()  # every reaction is in exactly one group
    return coupled, nonzero_rows


@app.cell(hide_code=True)
def _(julia):
    julia("coupled")
    return


@app.cell(hide_code=True)
def _(K_ec_f, S_ec, coupled, md_table, met_ids, mo, nonzero_rows, r_ec, rxn_ids, rxn_names):
    _multi = sorted((g for g in coupled if len(g) > 1), key=len, reverse=True)
    _rows = []
    for _g in _multi:
        _ratio = K_ec_f[_g] @ K_ec_f[_g[0]] / (K_ec_f[_g[0]] @ K_ec_f[_g[0]])
        _rows.append([", ".join(f"`{rxn_ids[i]}`" for i in _g),
                      "; ".join(rxn_names[i] for i in _g),
                      " : ".join(f"{x:.4g}" for x in _ratio)])
    _blocked = r_ec - int(nonzero_rows.sum())
    _pgk = rxn_ids.index("PGK")

    def _eq(j):
        _left = " + ".join(f"`{met_ids[i]}`" for i in range(len(met_ids)) if S_ec[i, j] < 0)
        _right = " + ".join(f"`{met_ids[i]}`" for i in range(len(met_ids)) if S_ec[i, j] > 0)
        return f"{_left} → {_right}"
    mo.md(
        f"{_blocked} reaction(s) are blocked. The {r_ec - _blocked} others fall into "
        f"**{len(coupled)}** groups: within the {len(K_ec_f[0])}-dimensional space of steady "
        f"states, these {r_ec} reactions move as only {len(coupled)} units. "
        f"{len(_multi)} groups have more than one reaction:\n\n"
        + md_table(["fully coupled reactions", "names", "flux ratio"], _rows)
        + "\n\nMany are an exchange reaction with the transporter that carries the same "
        "metabolite across the membrane; others are consecutive enzymes of glycolysis, the "
        "pentose phosphate pathway or the citric acid cycle. A negative ratio means the two "
        "reactions are written in opposite directions in the model, so equal and opposite "
        f"fluxes are one flow. `{rxn_ids[_pgk]}`, for example, is written as "
        f"{_eq(_pgk)}, the reverse of the glycolytic direction."
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Notes

    - **Exact arithmetic is cheap here.** $S$ has small integer entries (the biomass reaction's
      decimals become fractions), so row reduction in fractions is fast and gives integer
      bases with no tolerance to choose. For genome-scale models, thousands of rows and columns,
      floating-point methods (a rank-revealing QR or the SVD) are used instead, with a tolerance.
    - **The null space ignores irreversibility.** Many reactions can only run forwards. The
      steady states a cell can actually reach are the part of the null space with those fluxes
      nonnegative: a convex cone, whose extreme rays are the elementary flux modes. Coupling
      computed under those constraints (flux coupling analysis) finds more coupled pairs than the
      plain null space does.
    - **Flux balance analysis** goes one step further: add bounds on the exchange fluxes and a
      linear objective (often the biomass flux), and the steady-state question becomes a linear
      program.
    """)
    return


if __name__ == "__main__":
    app.run()
