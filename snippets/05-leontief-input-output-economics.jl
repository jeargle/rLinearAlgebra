# Julia version of notebooks/05-leontief-input-output-economics.py: the two-sector toy, then
# the 2023 US economy in 15 sectors, using the notebook's variable names. Runs as it stands,
# with only Julia's standard library:
#
#     julia 05-leontief-input-output-economics.jl
#
# Each section is shown in the notebook (and, except the data, on the entry page). The @assert
# lines check the results: the toy against the numbers worked by hand, the US table against
# BEA's published outputs. Lines ending in #hide run but are not shown.

# --- snippet setup: The toy economy ---
using LinearAlgebra
A_toy = [0.2 0.2
         0.4 0.1]      # column j: inputs per $1 of sector j's output
d_toy = [100.0, 50.0]  # final demand

# --- snippet solve: Solve (I − A) x = d ---
x_toy = (I - A_toy) \ d_toy    # I adapts its size; \ solves without forming an inverse
@assert x_toy ≈ [156.25, 125.0]
@show x_toy

# --- snippet inverse: The Leontief inverse ---
@assert det(I - A_toy) ≈ 0.64
L_toy = inv(I - A_toy)         # entry (i, j): output of i needed per $1 of final demand for j
@assert L_toy ≈ [1.40625 0.3125
                 0.625   1.25]
@show L_toy

# --- snippet rounds: Round by round: d + A d + A² d + ... ---
@assert sum(A_toy^k * d_toy for k in 0:30) ≈ x_toy

# --- snippet productive: Is the economy productive? ---
s = 1.0                                  # the slider: scale every input requirement by s
A_s = s * A_toy
colsums_s = sum(A_s, dims=1)             # quick test: every column sums below 1
rho_s = maximum(abs, eigvals(A_s))       # exact test: spectral radius below 1
@assert all(colsums_s .< 1) && rho_s < 1
@show rho_s

# --- snippet data: The 2023 US table ---
# BEGIN BEA DATA: US 2023, 15 sectors, $ millions (written by data/prepare_bea_2023.py)
sectors = ["Agriculture", "Mining", "Utilities", "Construction", "Manufacturing", "Wholesale trade", "Retail trade", "Transportation", "Information", "Finance & real estate", "Professional services", "Education & health", "Arts, food & lodging", "Other services", "Government"]
Z_us = Float64[
    155139 151 5 2424 328784 60 1216 48 85 223 3845 389 13363 107 8588
    1841 55268 23380 25565 445075 1009 590 1512 2870 756 4741 3891 3547 1919 26907
    8069 11529 27020 10974 59953 14436 38376 10997 13345 41279 15753 20098 32165 7605 40559
    2097 4742 5656 525 25667 5846 12788 8590 5405 138516 6036 5932 11897 5737 142406
    84226 81951 20514 544329 2193324 135963 58877 134412 92044 84576 251596 259175 155471 62312 558162
    52875 22157 7425 136318 526171 74972 35605 30483 39808 38418 72354 77397 43078 17923 108765
    1760 895 2558 109690 20548 688 8091 18822 421 11154 7874 972 14341 8429 366
    18120 15987 26188 44355 193891 139015 110495 211671 23865 66709 73950 41034 24381 6828 100114
    710 4860 7505 19094 41731 47499 58420 17013 316882 143017 191761 62632 63033 24121 199651
    14270 38446 21460 86091 150578 264691 320427 193954 159002 1857061 478329 375355 287033 137742 124605
    3814 63753 29685 119855 223812 407348 263880 100991 289883 846591 787838 339667 221592 89010 400069
    2 0 21 1 6 1784 3672 103 32 53 607 35575 5476 3458 34052
    572 425 3031 2301 8663 22704 13654 13048 55967 145438 101599 95735 79581 5285 44696
    351 442 1104 9919 17326 24886 17234 19279 9307 64871 54540 28017 21124 8663 78763
    3742 4441 10160 5800 31917 34248 28057 18222 11427 50492 26136 26901 30575 6163 38120
]
d_us = Float64[109116, 96859, 277658, 2086499, 2188266, 1504361, 2435071, 645397, 1261270, 4857029, 1946469, 3559780, 1694797, 857344, 4455159]
x_us = Float64[623540, 695731, 629815, 2468340, 6905201, 2788110, 2641681, 1742000, 2459201, 9366073, 6134256, 3644624, 2287495, 1213169, 4787577]
# END BEA DATA  #hide

# --- snippet coefficients: Coefficients from a flow table ---
n_us = length(x_us)
A_us = Z_us ./ x_us'               # a_ij = z_ij / x_j  (x_us' is a row: column j divided by x_j)
L_us = inv(I - A_us)
x_solved = (I - A_us) \ d_us       # should recover BEA's published output x_us
closure = x_solved ./ x_us .- 1
rho_us = maximum(abs, eigvals(A_us))
@assert maximum(abs, closure) < 0.005 && rho_us < 1
@show maximum(abs, closure) rho_us

# --- snippet multipliers: Output multipliers ---
multipliers = vec(sum(L_us, dims=1))   # column sums of L
@assert 1 < minimum(multipliers) && maximum(multipliers) < 3
for (sector, m) in sort(collect(zip(sectors, multipliers)), by=last, rev=true)
    println(rpad(sector, 24), round(m, digits=2))
end

# --- snippet shock: A demand shock, round by round ---
dd = zeros(n_us)
dd[findfirst(==("Manufacturing"), sectors)] = 10.0   # $10 billion of extra final demand
dx_total = L_us * dd               # total extra output, $ billions
dx_first = A_us * dd               # first round of inputs
dx_later = dx_total - dd - dx_first
@assert sum(dx_total) > sum(dd)
@show sum(dx_total)
