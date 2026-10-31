# Julia version of notebooks/04-stoichiometric-matrices-of-reaction-networks.py: balancing an
# equation and a five-species toy network worked by hand, then the E. coli core metabolic model
# from BiGG, using the notebook's variable names. Runs as it stands, with only Julia's standard
# library (the model is embedded in this file):
#
#     julia 04-stoichiometric-matrices-of-reaction-networks.jl
#
# The null spaces are computed exactly, in Rational{BigInt}, so the hand-checked vectors come out
# as integers. (LinearAlgebra's own nullspace works in floating point, from the SVD.) Each
# section is shown in the notebook (and, except the data, on the entry page). The @assert lines
# check the results: the toy against the numbers worked by hand, the E. coli model against
# properties any version of it must have. Lines ending in #hide run but are not shown.

# --- snippet setup: Exact null spaces in fractions ---
using LinearAlgebra

"Reduced row echelon form of M in exact fractions, and its pivot columns."
function rref_exact(M)
    R = Rational{BigInt}.(M)
    pivots, top = Int[], 1
    for col in 1:size(R, 2)
        p = findfirst(!iszero, R[top:end, col])
        p === nothing && continue          # no pivot here: col is a free column
        p += top - 1
        R[[top, p], :] = R[[p, top], :]
        R[top, :] ./= R[top, col]
        for i in 1:size(R, 1)
            if i != top && !iszero(R[i, col])
                R[i, :] .-= R[i, col] .* R[top, :]
            end
        end
        push!(pivots, col)
        top += 1
        top > size(R, 1) && break
    end
    return R, pivots
end

"Basis of {x : M x = 0}: one vector per free column, with 1 there and 0 in the other free columns."
function nullspace_exact(M)
    R, pivots = rref_exact(M)
    basis = Vector{Vector{Rational{BigInt}}}()
    for f in setdiff(1:size(M, 2), pivots)
        x = zeros(Rational{BigInt}, size(M, 2))
        x[f] = 1
        for (row, p) in enumerate(pivots)
            x[p] = -R[row, f]
        end
        push!(basis, x)
    end
    return basis
end

"x rescaled to the shortest vector of integers: clear denominators, divide out the common factor."
function integer_vector(x)
    ints = numerator.(x .* lcm(denominator.(x)))
    return ints .÷ gcd(ints)
end

"Dict(element => number of atoms) for a formula such as \"C6H12O6\"."
function atom_counts(formula)
    counts = Dict{String,Int}()
    for m in eachmatch(r"([A-Z][a-z]?)(\d*)", formula)
        counts[m[1]] = get(counts, m[1], 0) + (isempty(m[2]) ? 1 : parse(Int, m[2]))
    end
    return counts
end

# --- snippet balance: Balancing an equation: Z s = 0 ---
species_bal = ["C6H12O6", "O2", "CO2", "H2O"]    # glucose, oxygen, carbon dioxide, water
elements_bal = sort(unique(e for f in species_bal for e in keys(atom_counts(f))))   # C, H, O
Z_bal = [get(atom_counts(f), e, 0) for e in elements_bal, f in species_bal]
K_bal = nullspace_exact(Z_bal)
@assert length(K_bal) == 1                        # nullity 1: one balanced reaction, up to scale
s_bal = integer_vector(K_bal[1])
s_bal = s_bal[1] > 0 ? -s_bal : s_bal             # glucose is consumed: negative
@assert Z_bal == [ 6 0 1 0
                  12 0 0 2
                   6 2 2 1]
@assert s_bal == [-1, -6, 6, 6]                   # C6H12O6 + 6 O2 -> 6 CO2 + 6 H2O
@show s_bal

# --- snippet toy: A five-species network ---
species_toy = ["P", "Q", "R", "ATP", "ADP"]
#   reaction: 1   2   3   4   5   6
S_toy = [     1  -1   0   0   0   0     # P
              0   1  -1   0   0  -1     # Q
              0   0   1  -1   0   1     # R
              0  -1   2   0  -1   0     # ATP
              0   1  -2   0   1   0]    # ADP
m_toy, r_toy = size(S_toy)                # 5 species, 6 reactions

# --- snippet rank: Rank and the two null spaces ---
rank_toy = length(rref_exact(S_toy)[2])
K_toy = nullspace_exact(S_toy)                    # S v = 0: flux space, R^6
Y_toy = nullspace_exact(permutedims(S_toy))       # y' S = 0: species space, R^5
@assert rank_toy == 4
@assert integer_vector.(K_toy) == [[1, 1, 1, 1, 1, 0],
                                   [2, 2, 1, 2, 0, 1]]
@assert integer_vector.(Y_toy) == [[0, 0, 0, 1, 1]]   # ATP + ADP
@assert rank_toy + length(K_toy) == r_toy && rank_toy + length(Y_toy) == m_toy
println("rank = $rank_toy  nullity = $(length(K_toy))  left nullity = $(length(Y_toy))")

# --- snippet ode: Mass action: the concentrations move, ATP + ADP does not ---
k5, atp0 = 0.5, 1.5                       # the sliders: ATP demand, starting ATP
k_toy = [1.0, 1.0, 1.0, 1.0, k5, 0.5]
S_toy_f = Float64.(S_toy)

"Mass-action rates v(c) of the six reactions."
function rates_toy(c)
    P, Q, R, ATP, ADP = c
    return k_toy .* [1.0, P * ATP, Q * ADP^2, R, ATP, Q]
end

dt_toy, n_toy = 0.02, 3000                # 60 time units
c_toy = [0.0, 0.0, 0.0, atp0, 0.5]
traj_toy = [c_toy]
for _ in 1:n_toy                          # classical Runge-Kutta steps of dc/dt = S v(c)
    f1 = S_toy_f * rates_toy(c_toy)
    f2 = S_toy_f * rates_toy(c_toy + dt_toy / 2 * f1)
    f3 = S_toy_f * rates_toy(c_toy + dt_toy / 2 * f2)
    f4 = S_toy_f * rates_toy(c_toy + dt_toy * f3)
    global c_toy = c_toy + dt_toy / 6 * (f1 + 2 * f2 + 2 * f3 + f4)
    push!(traj_toy, c_toy)
end
traj_toy = permutedims(reduce(hcat, traj_toy))   # one row per time step
y_toy = Float64.(Y_toy[1])
total_toy = traj_toy * y_toy              # ATP + ADP at every time step
v_end = rates_toy(traj_toy[end, :])
ab_end = Float64.(reduce(hcat, K_toy)) \ v_end   # least squares: v = a K1 + b K2
@assert maximum(abs, total_toy .- total_toy[1]) < 1e-12   # conserved, whatever the kinetics
@assert maximum(abs, S_toy_f * v_end) < 1e-6              # the run has reached steady state
println("ATP + ADP = $(total_toy[1])  steady-state flux v = $(round.(v_end, digits=3))  (a, b) = $(round.(ab_end, digits=3))")

# --- snippet data: The E. coli core model ---
# BEGIN BIGG DATA: BiGG e_coli_core, 72 metabolites x 95 reactions, 360 nonzeros (written by data/prepare_ecoli_core.py)
met_ids = [
    "glc__D_e", "gln__L_c", "gln__L_e", "glu__L_c", "glu__L_e", "glx_c", "h2o_c", "h2o_e", "h_c",
    "h_e", "icit_c", "lac__D_c", "lac__D_e", "mal__L_c", "mal__L_e", "nad_c", "nadh_c", "nadp_c",
    "nadph_c", "nh4_c", "13dpg_c", "nh4_e", "o2_c", "2pg_c", "o2_e", "3pg_c", "oaa_c", "pep_c",
    "6pgc_c", "pi_c", "6pgl_c", "pi_e", "ac_c", "pyr_c", "pyr_e", "q8_c", "q8h2_c", "r5p_c",
    "ru5p__D_c", "ac_e", "acald_c", "s7p_c", "acald_e", "accoa_c", "succ_c", "succ_e", "succoa_c",
    "acon_C_c", "xu5p__D_c", "actp_c", "adp_c", "akg_c", "akg_e", "amp_c", "atp_c", "cit_c",
    "co2_c", "co2_e", "coa_c", "dhap_c", "e4p_c", "etoh_c", "etoh_e", "f6p_c", "fdp_c", "for_c",
    "for_e", "fru_e", "fum_c", "fum_e", "g3p_c", "g6p_c",
]
met_names = [
    "D-Glucose", "L-Glutamine", "L-Glutamine", "L-Glutamate", "L-Glutamate", "Glyoxylate",
    "H2O H2O", "H2O H2O", "H+", "H+", "Isocitrate", "D-Lactate", "D-Lactate", "L-Malate",
    "L-Malate", "Nicotinamide adenine dinucleotide", "Nicotinamide adenine dinucleotide - reduced",
    "Nicotinamide adenine dinucleotide phosphate",
    "Nicotinamide adenine dinucleotide phosphate - reduced", "Ammonium",
    "3-Phospho-D-glyceroyl phosphate", "Ammonium", "O2 O2", "D-Glycerate 2-phosphate", "O2 O2",
    "3-Phospho-D-glycerate", "Oxaloacetate", "Phosphoenolpyruvate", "6-Phospho-D-gluconate",
    "Phosphate", "6-phospho-D-glucono-1,5-lactone", "Phosphate", "Acetate", "Pyruvate", "Pyruvate",
    "Ubiquinone-8", "Ubiquinol-8", "Alpha-D-Ribose 5-phosphate", "D-Ribulose 5-phosphate",
    "Acetate", "Acetaldehyde", "Sedoheptulose 7-phosphate", "Acetaldehyde", "Acetyl-CoA",
    "Succinate", "Succinate", "Succinyl-CoA", "Cis-Aconitate", "D-Xylulose 5-phosphate",
    "Acetyl phosphate", "ADP C10H12N5O10P2", "2-Oxoglutarate", "2-Oxoglutarate", "AMP C10H12N5O7P",
    "ATP C10H12N5O13P3", "Citrate", "CO2 CO2", "CO2 CO2", "Coenzyme A",
    "Dihydroxyacetone phosphate", "D-Erythrose 4-phosphate", "Ethanol", "Ethanol",
    "D-Fructose 6-phosphate", "D-Fructose 1,6-bisphosphate", "Formate", "Formate", "D-Fructose",
    "Fumarate", "Fumarate", "Glyceraldehyde 3-phosphate", "D-Glucose 6-phosphate",
]
met_formulas = [
    "C6H12O6", "C5H10N2O3", "C5H10N2O3", "C5H8NO4", "C5H8NO4", "C2H1O3", "H2O", "H2O", "H", "H",
    "C6H5O7", "C3H5O3", "C3H5O3", "C4H4O5", "C4H4O5", "C21H26N7O14P2", "C21H27N7O14P2",
    "C21H25N7O17P3", "C21H26N7O17P3", "H4N", "C3H4O10P2", "H4N", "O2", "C3H4O7P", "O2", "C3H4O7P",
    "C4H2O5", "C3H2O6P", "C6H10O10P", "HO4P", "C6H9O9P", "HO4P", "C2H3O2", "C3H3O3", "C3H3O3",
    "C49H74O4", "C49H76O4", "C5H9O8P", "C5H9O8P", "C2H3O2", "C2H4O", "C7H13O10P", "C2H4O",
    "C23H34N7O17P3S", "C4H4O4", "C4H4O4", "C25H35N7O19P3S", "C6H3O6", "C5H9O8P", "C2H3O5P",
    "C10H12N5O10P2", "C5H4O5", "C5H4O5", "C10H12N5O7P", "C10H12N5O13P3", "C6H5O7", "CO2", "CO2",
    "C21H32N7O16P3S", "C3H5O6P", "C4H7O7P", "C2H6O", "C2H6O", "C6H11O9P", "C6H10O12P2", "CH1O2",
    "CH1O2", "C6H12O6", "C4H2O4", "C4H2O4", "C3H5O6P", "C6H11O9P",
]
met_charges = [
    0, 0, 0, -1, -1, -1, 0, 0, 1, 1, -3, -1, -1, -2, -2, -1, -2, -3, -4, 1, -4, 1, 0, -3, 0, -3,
    -2, -3, -3, -2, -2, -2, -1, -1, -1, 0, 0, -2, -2, -1, 0, -2, 0, -4, -2, -2, -5, -3, -2, -2, -3,
    -2, -2, -2, -4, -3, 0, 0, -4, -2, -2, 0, 0, -2, -4, -1, -1, 0, -2, -2, -2, -2,
]
rxn_ids = [
    "PFK", "PFL", "PGI", "PGK", "PGL", "ACALD", "AKGt2r", "PGM", "PIt2r", "ALCD2x", "ACALDt",
    "ACKr", "PPC", "ACONTa", "ACONTb", "ATPM", "PPCK", "ACt2r", "PPS", "ADK1", "AKGDH", "ATPS4r",
    "PTAr", "PYK", "BIOMASS_Ecoli_core_w_GAM", "PYRt2", "CO2t", "RPE", "CS", "RPI", "SUCCt2_2",
    "CYTBD", "D_LACt2", "ENO", "SUCCt3", "ETOHt2r", "SUCDi", "SUCOAS", "TALA", "THD2", "TKT1",
    "TKT2", "TPI", "EX_ac_e", "EX_acald_e", "EX_akg_e", "EX_co2_e", "EX_etoh_e", "EX_for_e",
    "EX_fru_e", "EX_fum_e", "EX_glc__D_e", "EX_gln__L_e", "EX_glu__L_e", "EX_h_e", "EX_h2o_e",
    "EX_lac__D_e", "EX_mal__L_e", "EX_nh4_e", "EX_o2_e", "EX_pi_e", "EX_pyr_e", "EX_succ_e", "FBA",
    "FBP", "FORt2", "FORt", "FRD7", "FRUpts2", "FUM", "FUMt2_2", "G6PDH2r", "GAPD", "GLCpts",
    "GLNS", "GLNabc", "GLUDy", "GLUN", "GLUSy", "GLUt2r", "GND", "H2Ot", "ICDHyr", "ICL", "LDH_D",
    "MALS", "MALt2_2", "MDH", "ME1", "ME2", "NADH16", "NADTRHD", "NH4t", "O2t", "PDH",
]
rxn_names = [
    "Phosphofructokinase", "Pyruvate formate lyase", "Glucose-6-phosphate isomerase",
    "Phosphoglycerate kinase", "6-phosphogluconolactonase",
    "Acetaldehyde dehydrogenase (acetylating)", "2 oxoglutarate reversible transport via symport",
    "Phosphoglycerate mutase", "Phosphate reversible transport via symport",
    "Alcohol dehydrogenase (ethanol)", "Acetaldehyde reversible transport", "Acetate kinase",
    "Phosphoenolpyruvate carboxylase", "Aconitase (half-reaction A, Citrate hydro-lyase)",
    "Aconitase (half-reaction B, Isocitrate hydro-lyase)", "ATP maintenance requirement",
    "Phosphoenolpyruvate carboxykinase", "Acetate reversible transport via proton symport",
    "Phosphoenolpyruvate synthase", "Adenylate kinase", "2-Oxogluterate dehydrogenase",
    "ATP synthase (four protons for one ATP)", "Phosphotransacetylase", "Pyruvate kinase",
    "Biomass Objective Function with GAM", "Pyruvate transport in via proton symport",
    "CO2 transporter via diffusion", "Ribulose 5-phosphate 3-epimerase", "Citrate synthase",
    "Ribose-5-phosphate isomerase", "Succinate transport via proton symport (2 H)",
    "Cytochrome oxidase bd (ubiquinol-8: 2 protons)", "D lactate transport via proton symport",
    "Enolase", "Succinate transport out via proton antiport",
    "Ethanol reversible transport via proton symport", "Succinate dehydrogenase (irreversible)",
    "Succinyl-CoA synthetase (ADP-forming)", "Transaldolase", "NAD(P) transhydrogenase",
    "Transketolase", "Transketolase", "Triose-phosphate isomerase", "Acetate exchange",
    "Acetaldehyde exchange", "2-Oxoglutarate exchange", "CO2 exchange", "Ethanol exchange",
    "Formate exchange", "D-Fructose exchange", "Fumarate exchange", "D-Glucose exchange",
    "L-Glutamine exchange", "L-Glutamate exchange", "H+ exchange", "H2O exchange",
    "D-lactate exchange", "L-Malate exchange", "Ammonia exchange", "O2 exchange",
    "Phosphate exchange", "Pyruvate exchange", "Succinate exchange",
    "Fructose-bisphosphate aldolase", "Fructose-bisphosphatase",
    "Formate transport in via proton symport", "Formate transport via diffusion",
    "Fumarate reductase", "Fructose transport via PEP:Pyr PTS (f6p generating)", "Fumarase",
    "Fumarate transport via proton symport (2 H)", "Glucose 6-phosphate dehydrogenase",
    "Glyceraldehyde-3-phosphate dehydrogenase", "D-glucose transport via PEP:Pyr PTS",
    "Glutamine synthetase", "L-glutamine transport via ABC system",
    "Glutamate dehydrogenase (NADP)", "Glutaminase", "Glutamate synthase (NADPH)",
    "L glutamate transport via proton symport  reversible", "Phosphogluconate dehydrogenase",
    "H2O transport via diffusion", "Isocitrate dehydrogenase (NADP)", "Isocitrate lyase",
    "D-lactate dehydrogenase", "Malate synthase", "Malate transport via proton symport (2 H)",
    "Malate dehydrogenase", "Malic enzyme (NAD)", "Malic enzyme (NADP)",
    "NADH dehydrogenase (ubiquinone-8 & 3 protons)", "NAD transhydrogenase",
    "Ammonia reversible transport", "O2 transport  diffusion ", "Pyruvate dehydrogenase",
]
S_columns = [   # S_columns[j]: (metabolite index (1-based), numerator, denominator) for each species in reaction j
    [(9, 1, 1), (51, 1, 1), (55, -1, 1), (64, -1, 1), (65, 1, 1)],   # PFK
    [(34, -1, 1), (44, 1, 1), (59, -1, 1), (66, 1, 1)],   # PFL
    [(64, 1, 1), (72, -1, 1)],   # PGI
    [(21, 1, 1), (26, -1, 1), (51, 1, 1), (55, -1, 1)],   # PGK
    [(7, -1, 1), (9, 1, 1), (29, 1, 1), (31, -1, 1)],   # PGL
    [(9, 1, 1), (16, -1, 1), (17, 1, 1), (41, -1, 1), (44, 1, 1), (59, -1, 1)],   # ACALD
    [(9, 1, 1), (10, -1, 1), (52, 1, 1), (53, -1, 1)],   # AKGt2r
    [(24, -1, 1), (26, 1, 1)],   # PGM
    [(9, 1, 1), (10, -1, 1), (30, 1, 1), (32, -1, 1)],   # PIt2r
    [(9, 1, 1), (16, -1, 1), (17, 1, 1), (41, 1, 1), (62, -1, 1)],   # ALCD2x
    [(41, 1, 1), (43, -1, 1)],   # ACALDt
    [(33, -1, 1), (50, 1, 1), (51, 1, 1), (55, -1, 1)],   # ACKr
    [(7, -1, 1), (9, 1, 1), (27, 1, 1), (28, -1, 1), (30, 1, 1), (57, -1, 1)],   # PPC
    [(7, 1, 1), (48, 1, 1), (56, -1, 1)],   # ACONTa
    [(7, -1, 1), (11, 1, 1), (48, -1, 1)],   # ACONTb
    [(7, -1, 1), (9, 1, 1), (30, 1, 1), (51, 1, 1), (55, -1, 1)],   # ATPM
    [(27, -1, 1), (28, 1, 1), (51, 1, 1), (55, -1, 1), (57, 1, 1)],   # PPCK
    [(9, 1, 1), (10, -1, 1), (33, 1, 1), (40, -1, 1)],   # ACt2r
    [(7, -1, 1), (9, 2, 1), (28, 1, 1), (30, 1, 1), (34, -1, 1), (54, 1, 1), (55, -1, 1)],   # PPS
    [(51, 2, 1), (54, -1, 1), (55, -1, 1)],   # ADK1
    [(16, -1, 1), (17, 1, 1), (47, 1, 1), (52, -1, 1), (57, 1, 1), (59, -1, 1)],   # AKGDH
    [(7, 1, 1), (9, 3, 1), (10, -4, 1), (30, -1, 1), (51, -1, 1), (55, 1, 1)],   # ATPS4r
    [(30, -1, 1), (44, -1, 1), (50, 1, 1), (59, 1, 1)],   # PTAr
    [(9, -1, 1), (28, -1, 1), (34, 1, 1), (51, -1, 1), (55, 1, 1)],   # PYK
    [(2, -2557, 10000), (4, -24707, 5000), (7, -5981, 100), (9, 5981, 100), (16, -3547, 1000), (17, 3547, 1000), (18, 130279, 10000), (19, -130279, 10000), (26, -187, 125), (27, -17867, 10000), (28, -5191, 10000), (30, 5981, 100), (34, -3541, 1250), (38, -8977, 10000), (44, -18739, 5000), (51, 5981, 100), (52, 20591, 5000), (55, -5981, 100), (59, 18739, 5000), (61, -361, 1000), (64, -709, 10000), (71, -129, 1000), (72, -41, 200)],   # BIOMASS_Ecoli_core_w_GAM
    [(9, 1, 1), (10, -1, 1), (34, 1, 1), (35, -1, 1)],   # PYRt2
    [(57, 1, 1), (58, -1, 1)],   # CO2t
    [(39, -1, 1), (49, 1, 1)],   # RPE
    [(7, -1, 1), (9, 1, 1), (27, -1, 1), (44, -1, 1), (56, 1, 1), (59, 1, 1)],   # CS
    [(38, -1, 1), (39, 1, 1)],   # RPI
    [(9, 2, 1), (10, -2, 1), (45, 1, 1), (46, -1, 1)],   # SUCCt2_2
    [(7, 1, 1), (9, -2, 1), (10, 2, 1), (23, -1, 2), (36, 1, 1), (37, -1, 1)],   # CYTBD
    [(9, 1, 1), (10, -1, 1), (12, 1, 1), (13, -1, 1)],   # D_LACt2
    [(7, 1, 1), (24, -1, 1), (28, 1, 1)],   # ENO
    [(9, 1, 1), (10, -1, 1), (45, -1, 1), (46, 1, 1)],   # SUCCt3
    [(9, 1, 1), (10, -1, 1), (62, 1, 1), (63, -1, 1)],   # ETOHt2r
    [(36, -1, 1), (37, 1, 1), (45, -1, 1), (69, 1, 1)],   # SUCDi
    [(30, 1, 1), (45, -1, 1), (47, 1, 1), (51, 1, 1), (55, -1, 1), (59, -1, 1)],   # SUCOAS
    [(42, -1, 1), (61, 1, 1), (64, 1, 1), (71, -1, 1)],   # TALA
    [(9, 2, 1), (10, -2, 1), (16, 1, 1), (17, -1, 1), (18, -1, 1), (19, 1, 1)],   # THD2
    [(38, -1, 1), (42, 1, 1), (49, -1, 1), (71, 1, 1)],   # TKT1
    [(49, -1, 1), (61, -1, 1), (64, 1, 1), (71, 1, 1)],   # TKT2
    [(60, -1, 1), (71, 1, 1)],   # TPI
    [(40, -1, 1)],   # EX_ac_e
    [(43, -1, 1)],   # EX_acald_e
    [(53, -1, 1)],   # EX_akg_e
    [(58, -1, 1)],   # EX_co2_e
    [(63, -1, 1)],   # EX_etoh_e
    [(67, -1, 1)],   # EX_for_e
    [(68, -1, 1)],   # EX_fru_e
    [(70, -1, 1)],   # EX_fum_e
    [(1, -1, 1)],   # EX_glc__D_e
    [(3, -1, 1)],   # EX_gln__L_e
    [(5, -1, 1)],   # EX_glu__L_e
    [(10, -1, 1)],   # EX_h_e
    [(8, -1, 1)],   # EX_h2o_e
    [(13, -1, 1)],   # EX_lac__D_e
    [(15, -1, 1)],   # EX_mal__L_e
    [(22, -1, 1)],   # EX_nh4_e
    [(25, -1, 1)],   # EX_o2_e
    [(32, -1, 1)],   # EX_pi_e
    [(35, -1, 1)],   # EX_pyr_e
    [(46, -1, 1)],   # EX_succ_e
    [(60, 1, 1), (65, -1, 1), (71, 1, 1)],   # FBA
    [(7, -1, 1), (30, 1, 1), (64, 1, 1), (65, -1, 1)],   # FBP
    [(9, 1, 1), (10, -1, 1), (66, 1, 1), (67, -1, 1)],   # FORt2
    [(66, 1, 1), (67, -1, 1)],   # FORt
    [(36, 1, 1), (37, -1, 1), (45, 1, 1), (69, -1, 1)],   # FRD7
    [(28, -1, 1), (34, 1, 1), (64, 1, 1), (68, -1, 1)],   # FRUpts2
    [(7, -1, 1), (14, 1, 1), (69, -1, 1)],   # FUM
    [(9, 2, 1), (10, -2, 1), (69, 1, 1), (70, -1, 1)],   # FUMt2_2
    [(9, 1, 1), (18, -1, 1), (19, 1, 1), (31, 1, 1), (72, -1, 1)],   # G6PDH2r
    [(9, 1, 1), (16, -1, 1), (17, 1, 1), (21, 1, 1), (30, -1, 1), (71, -1, 1)],   # GAPD
    [(1, -1, 1), (28, -1, 1), (34, 1, 1), (72, 1, 1)],   # GLCpts
    [(2, 1, 1), (4, -1, 1), (9, 1, 1), (20, -1, 1), (30, 1, 1), (51, 1, 1), (55, -1, 1)],   # GLNS
    [(2, 1, 1), (3, -1, 1), (7, -1, 1), (9, 1, 1), (30, 1, 1), (51, 1, 1), (55, -1, 1)],   # GLNabc
    [(4, -1, 1), (7, -1, 1), (9, 1, 1), (18, -1, 1), (19, 1, 1), (20, 1, 1), (52, 1, 1)],   # GLUDy
    [(2, -1, 1), (4, 1, 1), (7, -1, 1), (20, 1, 1)],   # GLUN
    [(2, -1, 1), (4, 2, 1), (9, -1, 1), (18, 1, 1), (19, -1, 1), (52, -1, 1)],   # GLUSy
    [(4, 1, 1), (5, -1, 1), (9, 1, 1), (10, -1, 1)],   # GLUt2r
    [(18, -1, 1), (19, 1, 1), (29, -1, 1), (39, 1, 1), (57, 1, 1)],   # GND
    [(7, 1, 1), (8, -1, 1)],   # H2Ot
    [(11, -1, 1), (18, -1, 1), (19, 1, 1), (52, 1, 1), (57, 1, 1)],   # ICDHyr
    [(6, 1, 1), (11, -1, 1), (45, 1, 1)],   # ICL
    [(9, 1, 1), (12, -1, 1), (16, -1, 1), (17, 1, 1), (34, 1, 1)],   # LDH_D
    [(6, -1, 1), (7, -1, 1), (9, 1, 1), (14, 1, 1), (44, -1, 1), (59, 1, 1)],   # MALS
    [(9, 2, 1), (10, -2, 1), (14, 1, 1), (15, -1, 1)],   # MALt2_2
    [(9, 1, 1), (14, -1, 1), (16, -1, 1), (17, 1, 1), (27, 1, 1)],   # MDH
    [(14, -1, 1), (16, -1, 1), (17, 1, 1), (34, 1, 1), (57, 1, 1)],   # ME1
    [(14, -1, 1), (18, -1, 1), (19, 1, 1), (34, 1, 1), (57, 1, 1)],   # ME2
    [(9, -4, 1), (10, 3, 1), (16, 1, 1), (17, -1, 1), (36, -1, 1), (37, 1, 1)],   # NADH16
    [(16, -1, 1), (17, 1, 1), (18, 1, 1), (19, -1, 1)],   # NADTRHD
    [(20, 1, 1), (22, -1, 1)],   # NH4t
    [(23, 1, 1), (25, -1, 1)],   # O2t
    [(16, -1, 1), (17, 1, 1), (34, -1, 1), (44, 1, 1), (57, 1, 1), (59, -1, 1)],   # PDH
]
# END BIGG DATA  #hide

# --- snippet matrix: Build S ---
m_ec, r_ec = length(met_ids), length(rxn_ids)
S_ec_exact = zeros(Rational{BigInt}, m_ec, r_ec)
for (j, col) in enumerate(S_columns), (i, num, den) in col
    S_ec_exact[i, j] = num // den
end
S_ec = Float64.(S_ec_exact)
nnz_ec = count(!iszero, S_ec)
println("$m_ec metabolites x $r_ec reactions, $nnz_ec nonzeros")

# --- snippet rank_ec: Rank and nullities ---
rank_ec = length(rref_exact(S_ec_exact)[2])
K_ec = nullspace_exact(S_ec_exact)                # steady-state fluxes
Y_ec = nullspace_exact(permutedims(S_ec_exact))   # conservation laws
sv_ec = svdvals(S_ec)
@assert rank_ec == rank(S_ec)                     # exact and floating-point ranks agree
@assert rank_ec + length(K_ec) == r_ec && rank_ec + length(Y_ec) == m_ec
println("rank = $rank_ec  nullity = $(length(K_ec))  left nullity = $(length(Y_ec))")

# --- snippet moieties: Conserved moieties: the left null space ---
K_ec_f = Float64.(reduce(hcat, K_ec))             # r x nullity, one basis vector per column
Y_ec_f = Float64.(permutedims(reduce(hcat, Y_ec)))   # one conservation vector y per row
@assert maximum(abs, Y_ec_f * S_ec) < 1e-9 && maximum(abs, S_ec * K_ec_f) < 1e-9
moieties = [met_ids[findall(!iszero, y)] for y in eachrow(Y_ec_f)]
y_nad = Float64.(in(["nad_c", "nadh_c"]).(met_ids))
@assert maximum(abs, y_nad' * S_ec) < 1e-9        # NAD + NADH is one of them
foreach(pool -> println(join(pool, " + ")), moieties)

# --- snippet elements: Atoms balance in every internal reaction ---
ELEMENTS = ["C", "H", "N", "O", "P", "S"]
Z_ec = [get(atom_counts(f), e, 0) for e in ELEMENTS, f in met_formulas]
internal = [j for (j, rid) in enumerate(rxn_ids) if !startswith(rid, "EX_") && !startswith(rid, "BIOMASS")]
S_int = S_ec[:, internal]
@assert maximum(abs, Z_ec * S_int) < 1e-9          # Z s = 0 for every internal reaction
@assert maximum(abs, met_charges' * S_int) < 1e-9  # and charge balances too
rank_int = rank(S_int)
laws_int = vcat(Z_ec, met_charges', Y_ec_f)       # elements, charge, moieties
@assert rank(laws_int) == m_ec - rank_int         # together they span the left null space
println("$(length(internal)) internal reactions; rank $rank_int; left nullity $(m_ec - rank_int)")

# --- snippet coupled: Fully coupled reactions: the right null space ---
nonzero_rows = vec(maximum(abs, K_ec_f, dims=2)) .> 0   # a zero row: flux forced to 0 at steady state
U_ec = K_ec_f ./ max.(norm.(eachrow(K_ec_f)), 1e-300)
coupled, seen = Vector{Vector{Int}}(), Set{Int}()
for j in findall(nonzero_rows)
    if !(j in seen)                                 # parallel rows: fluxes in a fixed ratio
        group = [i for i in findall(nonzero_rows) if abs(abs(dot(U_ec[j, :], U_ec[i, :])) - 1) < 1e-9]
        union!(seen, group)
        push!(coupled, group)
    end
end
@assert sum(length, coupled) == count(nonzero_rows)   # every reaction is in exactly one group
for group in coupled
    length(group) > 1 && println(join(rxn_ids[group], ", "))
end
