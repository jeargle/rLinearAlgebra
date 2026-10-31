# Python version of notebooks/04-stoichiometric-matrices-of-reaction-networks.py: balancing an
# equation and a five-species toy network worked by hand, then the E. coli core metabolic model
# from BiGG, using the notebook's variable names. Runs as it stands, with only numpy (the model
# is embedded in this file):
#
#     python 04-stoichiometric-matrices-of-reaction-networks.py
#
# The null spaces are computed exactly, in fractions, so the hand-checked vectors come out as
# integers. Python counts from 0, so reaction 1 is column 0. Each section is shown on the entry
# page (except the data) next to its Julia twin. The assert lines check the results: the toy
# against the numbers worked by hand, the E. coli model against properties any version of it
# must have. Lines ending in #hide run but are not shown.

# --- snippet setup: Exact null spaces in fractions ---
import re
from fractions import Fraction
from math import gcd, lcm
import numpy as np


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

# --- snippet balance: Balancing an equation: Z s = 0 ---
species_bal = ["C6H12O6", "O2", "CO2", "H2O"]    # glucose, oxygen, carbon dioxide, water
elements_bal = sorted({e for f in species_bal for e in atom_counts(f)})   # C, H, O
Z_bal = [[atom_counts(f).get(e, 0) for f in species_bal] for e in elements_bal]
K_bal = nullspace_exact(Z_bal)
assert len(K_bal) == 1                            # nullity 1: one balanced reaction, up to scale
s_bal = integer_vector(K_bal[0])
s_bal = [-x for x in s_bal] if s_bal[0] > 0 else s_bal   # glucose is consumed: negative
assert Z_bal == [[6, 0, 1, 0],
                 [12, 0, 0, 2],
                 [6, 2, 2, 1]]
assert s_bal == [-1, -6, 6, 6]                    # C6H12O6 + 6 O2 -> 6 CO2 + 6 H2O
print("s_bal =", s_bal)

# --- snippet toy: A five-species network ---
species_toy = ["P", "Q", "R", "ATP", "ADP"]
#        reaction:  1   2   3   4   5   6
S_toy = [          [1, -1,  0,  0,  0,  0],   # P
                   [0,  1, -1,  0,  0, -1],   # Q
                   [0,  0,  1, -1,  0,  1],   # R
                   [0, -1,  2,  0, -1,  0],   # ATP
                   [0,  1, -2,  0,  1,  0]]   # ADP
m_toy, r_toy = len(S_toy), len(S_toy[0])      # 5 species, 6 reactions

# --- snippet rank: Rank and the two null spaces ---
rank_toy = len(rref_exact(S_toy)[1])
K_toy = nullspace_exact(S_toy)                              # S v = 0: flux space, R^6
Y_toy = nullspace_exact([list(col) for col in zip(*S_toy)])  # y^T S = 0: species space, R^5
assert rank_toy == 4
assert [integer_vector(k) for k in K_toy] == [[1, 1, 1, 1, 1, 0],
                                              [2, 2, 1, 2, 0, 1]]
assert [integer_vector(y) for y in Y_toy] == [[0, 0, 0, 1, 1]]   # ATP + ADP
assert rank_toy + len(K_toy) == r_toy and rank_toy + len(Y_toy) == m_toy
print("rank =", rank_toy, " nullity =", len(K_toy), " left nullity =", len(Y_toy))

# --- snippet ode: Mass action: the concentrations move, ATP + ADP does not ---
k5, atp0 = 0.5, 1.5                       # the sliders: ATP demand, starting ATP
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
assert np.abs(S_toy_f @ v_end).max() < 1e-6              # the run has reached steady state
print("ATP + ADP =", total_toy[0], " steady-state flux v =", v_end.round(3), " (a, b) =", ab_end.round(3))

# --- snippet data: The E. coli core model ---
# BEGIN BIGG DATA: BiGG e_coli_core, 72 metabolites x 95 reactions, 360 nonzeros (written by data/prepare_ecoli_core.py)
met_ids = [
    'glc__D_e', 'gln__L_c', 'gln__L_e', 'glu__L_c', 'glu__L_e', 'glx_c', 'h2o_c', 'h2o_e', 'h_c',
    'h_e', 'icit_c', 'lac__D_c', 'lac__D_e', 'mal__L_c', 'mal__L_e', 'nad_c', 'nadh_c', 'nadp_c',
    'nadph_c', 'nh4_c', '13dpg_c', 'nh4_e', 'o2_c', '2pg_c', 'o2_e', '3pg_c', 'oaa_c', 'pep_c',
    '6pgc_c', 'pi_c', '6pgl_c', 'pi_e', 'ac_c', 'pyr_c', 'pyr_e', 'q8_c', 'q8h2_c', 'r5p_c',
    'ru5p__D_c', 'ac_e', 'acald_c', 's7p_c', 'acald_e', 'accoa_c', 'succ_c', 'succ_e', 'succoa_c',
    'acon_C_c', 'xu5p__D_c', 'actp_c', 'adp_c', 'akg_c', 'akg_e', 'amp_c', 'atp_c', 'cit_c',
    'co2_c', 'co2_e', 'coa_c', 'dhap_c', 'e4p_c', 'etoh_c', 'etoh_e', 'f6p_c', 'fdp_c', 'for_c',
    'for_e', 'fru_e', 'fum_c', 'fum_e', 'g3p_c', 'g6p_c',
]
met_names = [
    'D-Glucose', 'L-Glutamine', 'L-Glutamine', 'L-Glutamate', 'L-Glutamate', 'Glyoxylate',
    'H2O H2O', 'H2O H2O', 'H+', 'H+', 'Isocitrate', 'D-Lactate', 'D-Lactate', 'L-Malate',
    'L-Malate', 'Nicotinamide adenine dinucleotide', 'Nicotinamide adenine dinucleotide - reduced',
    'Nicotinamide adenine dinucleotide phosphate',
    'Nicotinamide adenine dinucleotide phosphate - reduced', 'Ammonium',
    '3-Phospho-D-glyceroyl phosphate', 'Ammonium', 'O2 O2', 'D-Glycerate 2-phosphate', 'O2 O2',
    '3-Phospho-D-glycerate', 'Oxaloacetate', 'Phosphoenolpyruvate', '6-Phospho-D-gluconate',
    'Phosphate', '6-phospho-D-glucono-1,5-lactone', 'Phosphate', 'Acetate', 'Pyruvate', 'Pyruvate',
    'Ubiquinone-8', 'Ubiquinol-8', 'Alpha-D-Ribose 5-phosphate', 'D-Ribulose 5-phosphate',
    'Acetate', 'Acetaldehyde', 'Sedoheptulose 7-phosphate', 'Acetaldehyde', 'Acetyl-CoA',
    'Succinate', 'Succinate', 'Succinyl-CoA', 'Cis-Aconitate', 'D-Xylulose 5-phosphate',
    'Acetyl phosphate', 'ADP C10H12N5O10P2', '2-Oxoglutarate', '2-Oxoglutarate', 'AMP C10H12N5O7P',
    'ATP C10H12N5O13P3', 'Citrate', 'CO2 CO2', 'CO2 CO2', 'Coenzyme A',
    'Dihydroxyacetone phosphate', 'D-Erythrose 4-phosphate', 'Ethanol', 'Ethanol',
    'D-Fructose 6-phosphate', 'D-Fructose 1,6-bisphosphate', 'Formate', 'Formate', 'D-Fructose',
    'Fumarate', 'Fumarate', 'Glyceraldehyde 3-phosphate', 'D-Glucose 6-phosphate',
]
met_formulas = [
    'C6H12O6', 'C5H10N2O3', 'C5H10N2O3', 'C5H8NO4', 'C5H8NO4', 'C2H1O3', 'H2O', 'H2O', 'H', 'H',
    'C6H5O7', 'C3H5O3', 'C3H5O3', 'C4H4O5', 'C4H4O5', 'C21H26N7O14P2', 'C21H27N7O14P2',
    'C21H25N7O17P3', 'C21H26N7O17P3', 'H4N', 'C3H4O10P2', 'H4N', 'O2', 'C3H4O7P', 'O2', 'C3H4O7P',
    'C4H2O5', 'C3H2O6P', 'C6H10O10P', 'HO4P', 'C6H9O9P', 'HO4P', 'C2H3O2', 'C3H3O3', 'C3H3O3',
    'C49H74O4', 'C49H76O4', 'C5H9O8P', 'C5H9O8P', 'C2H3O2', 'C2H4O', 'C7H13O10P', 'C2H4O',
    'C23H34N7O17P3S', 'C4H4O4', 'C4H4O4', 'C25H35N7O19P3S', 'C6H3O6', 'C5H9O8P', 'C2H3O5P',
    'C10H12N5O10P2', 'C5H4O5', 'C5H4O5', 'C10H12N5O7P', 'C10H12N5O13P3', 'C6H5O7', 'CO2', 'CO2',
    'C21H32N7O16P3S', 'C3H5O6P', 'C4H7O7P', 'C2H6O', 'C2H6O', 'C6H11O9P', 'C6H10O12P2', 'CH1O2',
    'CH1O2', 'C6H12O6', 'C4H2O4', 'C4H2O4', 'C3H5O6P', 'C6H11O9P',
]
met_charges = [
    0, 0, 0, -1, -1, -1, 0, 0, 1, 1, -3, -1, -1, -2, -2, -1, -2, -3, -4, 1, -4, 1, 0, -3, 0, -3,
    -2, -3, -3, -2, -2, -2, -1, -1, -1, 0, 0, -2, -2, -1, 0, -2, 0, -4, -2, -2, -5, -3, -2, -2, -3,
    -2, -2, -2, -4, -3, 0, 0, -4, -2, -2, 0, 0, -2, -4, -1, -1, 0, -2, -2, -2, -2,
]
rxn_ids = [
    'PFK', 'PFL', 'PGI', 'PGK', 'PGL', 'ACALD', 'AKGt2r', 'PGM', 'PIt2r', 'ALCD2x', 'ACALDt',
    'ACKr', 'PPC', 'ACONTa', 'ACONTb', 'ATPM', 'PPCK', 'ACt2r', 'PPS', 'ADK1', 'AKGDH', 'ATPS4r',
    'PTAr', 'PYK', 'BIOMASS_Ecoli_core_w_GAM', 'PYRt2', 'CO2t', 'RPE', 'CS', 'RPI', 'SUCCt2_2',
    'CYTBD', 'D_LACt2', 'ENO', 'SUCCt3', 'ETOHt2r', 'SUCDi', 'SUCOAS', 'TALA', 'THD2', 'TKT1',
    'TKT2', 'TPI', 'EX_ac_e', 'EX_acald_e', 'EX_akg_e', 'EX_co2_e', 'EX_etoh_e', 'EX_for_e',
    'EX_fru_e', 'EX_fum_e', 'EX_glc__D_e', 'EX_gln__L_e', 'EX_glu__L_e', 'EX_h_e', 'EX_h2o_e',
    'EX_lac__D_e', 'EX_mal__L_e', 'EX_nh4_e', 'EX_o2_e', 'EX_pi_e', 'EX_pyr_e', 'EX_succ_e', 'FBA',
    'FBP', 'FORt2', 'FORt', 'FRD7', 'FRUpts2', 'FUM', 'FUMt2_2', 'G6PDH2r', 'GAPD', 'GLCpts',
    'GLNS', 'GLNabc', 'GLUDy', 'GLUN', 'GLUSy', 'GLUt2r', 'GND', 'H2Ot', 'ICDHyr', 'ICL', 'LDH_D',
    'MALS', 'MALt2_2', 'MDH', 'ME1', 'ME2', 'NADH16', 'NADTRHD', 'NH4t', 'O2t', 'PDH',
]
rxn_names = [
    'Phosphofructokinase', 'Pyruvate formate lyase', 'Glucose-6-phosphate isomerase',
    'Phosphoglycerate kinase', '6-phosphogluconolactonase',
    'Acetaldehyde dehydrogenase (acetylating)', '2 oxoglutarate reversible transport via symport',
    'Phosphoglycerate mutase', 'Phosphate reversible transport via symport',
    'Alcohol dehydrogenase (ethanol)', 'Acetaldehyde reversible transport', 'Acetate kinase',
    'Phosphoenolpyruvate carboxylase', 'Aconitase (half-reaction A, Citrate hydro-lyase)',
    'Aconitase (half-reaction B, Isocitrate hydro-lyase)', 'ATP maintenance requirement',
    'Phosphoenolpyruvate carboxykinase', 'Acetate reversible transport via proton symport',
    'Phosphoenolpyruvate synthase', 'Adenylate kinase', '2-Oxogluterate dehydrogenase',
    'ATP synthase (four protons for one ATP)', 'Phosphotransacetylase', 'Pyruvate kinase',
    'Biomass Objective Function with GAM', 'Pyruvate transport in via proton symport',
    'CO2 transporter via diffusion', 'Ribulose 5-phosphate 3-epimerase', 'Citrate synthase',
    'Ribose-5-phosphate isomerase', 'Succinate transport via proton symport (2 H)',
    'Cytochrome oxidase bd (ubiquinol-8: 2 protons)', 'D lactate transport via proton symport',
    'Enolase', 'Succinate transport out via proton antiport',
    'Ethanol reversible transport via proton symport', 'Succinate dehydrogenase (irreversible)',
    'Succinyl-CoA synthetase (ADP-forming)', 'Transaldolase', 'NAD(P) transhydrogenase',
    'Transketolase', 'Transketolase', 'Triose-phosphate isomerase', 'Acetate exchange',
    'Acetaldehyde exchange', '2-Oxoglutarate exchange', 'CO2 exchange', 'Ethanol exchange',
    'Formate exchange', 'D-Fructose exchange', 'Fumarate exchange', 'D-Glucose exchange',
    'L-Glutamine exchange', 'L-Glutamate exchange', 'H+ exchange', 'H2O exchange',
    'D-lactate exchange', 'L-Malate exchange', 'Ammonia exchange', 'O2 exchange',
    'Phosphate exchange', 'Pyruvate exchange', 'Succinate exchange',
    'Fructose-bisphosphate aldolase', 'Fructose-bisphosphatase',
    'Formate transport in via proton symport', 'Formate transport via diffusion',
    'Fumarate reductase', 'Fructose transport via PEP:Pyr PTS (f6p generating)', 'Fumarase',
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
# END BIGG DATA  #hide

# --- snippet matrix: Build S ---
m_ec, r_ec = len(met_ids), len(rxn_ids)
S_ec_exact = [[Fraction(0)] * r_ec for _ in range(m_ec)]
for j, col in enumerate(S_columns):
    for i, num, den in col:
        S_ec_exact[i][j] = Fraction(num, den)
S_ec = np.array(S_ec_exact, dtype=float)
nnz_ec = int((S_ec != 0).sum())
print(m_ec, "metabolites x", r_ec, "reactions,", nnz_ec, "nonzeros")

# --- snippet rank_ec: Rank and nullities ---
rank_ec = len(rref_exact(S_ec_exact)[1])
K_ec = nullspace_exact(S_ec_exact)                                # steady-state fluxes
Y_ec = nullspace_exact([list(col) for col in zip(*S_ec_exact)])   # conservation laws
sv_ec = np.linalg.svd(S_ec, compute_uv=False)
assert rank_ec == np.linalg.matrix_rank(S_ec)        # exact and floating-point ranks agree
assert rank_ec + len(K_ec) == r_ec and rank_ec + len(Y_ec) == m_ec
print("rank =", rank_ec, " nullity =", len(K_ec), " left nullity =", len(Y_ec))

# --- snippet moieties: Conserved moieties: the left null space ---
K_ec_f = np.array(K_ec, dtype=float).T               # r x nullity, one basis vector per column
Y_ec_f = np.array(Y_ec, dtype=float)                 # one conservation vector y per row
assert np.abs(Y_ec_f @ S_ec).max() < 1e-9 and np.abs(S_ec @ K_ec_f).max() < 1e-9
moieties = [[met_ids[i] for i in np.flatnonzero(y)] for y in Y_ec_f]
y_nad = np.isin(met_ids, ["nad_c", "nadh_c"]).astype(float)
assert np.abs(y_nad @ S_ec).max() < 1e-9             # NAD + NADH is one of them
for pool in moieties:
    print(" + ".join(pool))

# --- snippet elements: Atoms balance in every internal reaction ---
ELEMENTS = ["C", "H", "N", "O", "P", "S"]
Z_ec = np.array([[atom_counts(f).get(e, 0) for f in met_formulas] for e in ELEMENTS])
internal = [j for j, rid in enumerate(rxn_ids) if not rid.startswith(("EX_", "BIOMASS"))]
S_int = S_ec[:, internal]
assert np.abs(Z_ec @ S_int).max() < 1e-9               # Z s = 0 for every internal reaction
assert np.abs(np.array(met_charges) @ S_int).max() < 1e-9   # and charge balances too
rank_int = np.linalg.matrix_rank(S_int)
laws_int = np.vstack([Z_ec, met_charges, Y_ec_f])    # elements, charge, moieties
assert np.linalg.matrix_rank(laws_int) == m_ec - rank_int   # together they span the left null space
print(len(internal), "internal reactions; rank", rank_int, "; left nullity", m_ec - rank_int)

# --- snippet coupled: Fully coupled reactions: the right null space ---
nonzero_rows = np.abs(K_ec_f).max(axis=1) > 0        # a zero row: flux forced to 0 at steady state
U_ec = K_ec_f / np.maximum(np.linalg.norm(K_ec_f, axis=1, keepdims=True), 1e-300)
coupled, seen = [], set()
for j in np.flatnonzero(nonzero_rows):
    if j not in seen:                                # parallel rows: fluxes in a fixed ratio
        group = [i for i in np.flatnonzero(nonzero_rows) if abs(abs(U_ec[j] @ U_ec[i]) - 1) < 1e-9]
        seen.update(group)
        coupled.append(group)
assert sum(map(len, coupled)) == nonzero_rows.sum()  # every reaction is in exactly one group
for group in coupled:
    if len(group) > 1:
        print(", ".join(rxn_ids[i] for i in group))
