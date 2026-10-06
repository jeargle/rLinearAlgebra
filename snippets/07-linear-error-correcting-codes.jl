# Julia version of notebooks/07-linear-error-correcting-codes.py: Hamming(7,4) worked by hand,
# then Mariner 9's Reed–Muller code on a real image of Mars, using the notebook's variable names.
# Runs as it stands, with only Julia's standard library (the image is embedded in this file):
#
#     julia 07-linear-error-correcting-codes.jl
#
# All arithmetic on bits is modulo 2 (GF(2)), written mod.(…, 2). Julia counts array positions
# from 1, the notebook's Python from 0, so bit 6 is index 6 here and index 5 there. Each section
# is shown in the notebook (and, except the data, on the entry page). The @assert lines check the
# results. Lines ending in #hide run but are not shown.

# --- snippet setup: Hamming(7,4): generator and parity-check matrices ---
using LinearAlgebra
B = [1 1 0
     1 0 1
     0 1 1
     1 1 1]
G = [I(4) B]          # 4 × 7, systematic form [I B]: the message appears in the first 4 bits
H = [B' I(3)]         # 3 × 7, one parity check per row; its columns are all 7 nonzero 3-bit vectors
@assert all(mod.(G * H', 2) .== 0)    # every codeword passes every check

# --- snippet encode: Encode: c = m G (modulo 2) ---
m = [1 0 1 1]         # the message, a row vector
c = mod.(m * G, 2)    # adds rows 1, 3 and 4 of G
@assert vec(c) == [1, 0, 1, 1, 0, 1, 0]
@show c

# --- snippet syndrome: Receive, compute the syndrome, correct ---
e = [0 0 0 0 0 1 0]               # the channel flips bit 6
y = mod.(c + e, 2)                # what arrives
s = mod.(H * vec(y), 2)           # syndrome: which checks fail
flip_at = any(s .== 1) ? findfirst(j -> H[:, j] == s, 1:7) : nothing
c_hat = copy(y)
flip_at === nothing || (c_hat[flip_at] = 1 - c_hat[flip_at])
m_hat = c_hat[1:4]
@assert s == [0, 1, 0] && flip_at == 6 && m_hat == vec(m)
@show s flip_at m_hat

# --- snippet table: The decoding table ---
table = Dict(H[:, j] => "bit $j" for j in 1:7)
table[[0, 0, 0]] = "no error"
@assert table[s] == "bit 6"

# --- snippet distance: Minimum distance ---
all_msgs = [(v >> (3 - i)) & 1 for v in 0:15, i in 0:3]   # all 16 messages, one per row
codebook = mod.(all_msgs * G, 2)
weights = vec(sum(codebook, dims=2))
d_min = minimum(w for w in weights if w > 0)
@assert d_min == 3                                        # so the code corrects 1 error
@assert all(mod.(H[:, 1] + H[:, 5] + H[:, 6], 2) .== 0)   # three dependent columns of H

# --- snippet pitfall: No lengths in GF(2) ---
cw = codebook[12, :]                  # message 1011 is row 12 (Julia counts from 1)
@assert any(cw .== 1) && mod(cw ⋅ cw, 2) == 0   # nonzero, yet orthogonal to itself
@assert 7 - rank(H) == 4              # the code is the null space of H: dimension 4

# --- snippet data: The Mariner 9 image ---
using Base64
# The image is embedded in this file (not shown here): 128 × 128 pixels at 64 grey levels
# (0–63), one byte per pixel, base64-encoded, about 22 KB of text. data/prepare_mariner9.py made
# it from NASA/JPL frame PIA02999. To start from the original photograph instead, something
# like this works (a sketch, not run by CI; it needs the FileIO, ImageIO and Images packages,
# and its resampling differs slightly from the prepared image's):
#
#     using FileIO, Images
#     url = "https://images-assets.nasa.gov/image/PIA02999/PIA02999~medium.jpg"
#     photo = Gray.(load(download(url)))
#     small = imresize(photo[301:940, 21:660], (128, 128))     # crop rows, columns; shrink
#     mars = round.(Int, 63 .* Float64.(small))                # 64 grey levels
#
# BEGIN MARINER DATA (written by data/prepare_mariner9.py; NASA/JPL PIA02999)  #hide
image_shape = (128, 128)  #hide
image_b64 = join([  #hide
    "FyIdEwwVDg4PEgsKCw4XGhUXGx8YGxciJyQlIh8jIiIlHBoZGRsSEBgUGBkYGxUaICElJCceHBcYFh8cHBobFxocHSgr",  #hide
    "JB8eGBwhHyYlHiQoJycpJigkKSYlIiocGxgWFxsYGhkYFhUbICYnLCsqLissLS4uLiYqMjEtLC8sKSkcGhkWEhATGA8R",  #hide
    "DQsLDg0VFx4iJR8eGSQjIB8jHRglJB4bEhAaFhYOExQWGCQgGB4fHisiHRsbIRYWGB4eICUTFRcYIiUhGyIeIyYiJykl",  #hide
    "KioqKysjKSgkHh0gJBwZFRoWFRcbExMVFholKi4uLSkqKiswLy8sJCgtLzAvLi8sKx0eFhcTERAYFxIPCgkODxETHxse",  #hide
    "ICEmJSEfIBgaFxcdJSUbEhQTFRUXFBkdISYoJCogKgwFHB4YIRcZFh0cGBQQFhshICEhISAiHCQlJSUvLC4uLicpJiQg",  #hide
    "Gx4jJiYZFxYZGBoSFBYfGCQtLicpLCcoLissMTIqLCknLSwuLycoKSUeGBQWEhUWFxQTDxAPExUXHSAeJCMcIxwYEQ8U",  #hide
    "FRkiIh8eGhQZGh0ZFxsdIiIaHyEhEhwdHRoZGBgYHhsZFhcaHiIlHBsbIh4cIiwnJywqMDIuLygkKyQoIyQgHRgSGR4V",  #hide
    "ExMYGh8cJSIlICgsJycoJy0vMiwuKiYkKysvLiouKiEdERIUExEVERwXEhATFRMbIR0cIiEfHBcTExkTERgYGhcSFRcS",  #hide
    "ICofHCQbDgsoISIpJh4lGhIYFRMaGBMTHh4dHR0TGhofISYiJiUpLS8tLS4qJiYqKCgrJiIjGhYYFxEVFR8ZFRgjHxoj",  #hide
    "KiUoJykqLC4yMi0rLy0uKSknJycrIiIdFxASDg4OFBYUERQWGRseHRkWHRYaGBcWExIRFxETFxYTFRQbHx4fIBUYHCof",  #hide
    "HR8nIB8cGRkUERINDg0YHCMjIhodICImJiIlKCkvMCksLCkpKCkqLSonJSMlJBgcGR0cIBwfGyAjHyEnJywmJy8sLjEy",  #hide
    "MDEyMzMwMx0HKi0lIRsTFhkREREYFRAUFRYYGx0dHhMQGRYQExYQExMXEhUcHBgZFBoeJRobIBsaIhohIioaFh0gIBgX",  #hide
    "EA4PDxcXHCQkHh4gJSQkKyooJCssLCwyLycmICArJyokIyUjICIdJiIjIB8aHicuMTExMzUzNDI0NDQ0MzQ0NTU3Jgww",  #hide
    "LichIB0VFh4cGBkOERIUFBQcFhQUEBEWExYcHBQSFRcVGhIQFx8VJh4hHRocIh8mHCAkJyEfICMfGQ0PDhAVGBwdJxUN",  #hide
    "IycnKyw3NC0uMDAyMjMxNCkIBSo1NDIwLyopMC4yMDAuLCooLDIrKSQhIicpJSUoLCwsLi0vLysrMiosKCQhIBUbFx4a",  #hide
    "GBASEhUWFBMXExUTDxcTERskGhYWGh4gExQdGBMfHSIiIyAfFBoaHCIlJB4fHxYZERENERobHyIsHh0tLissMjAvMDEx",  #hide
    "MS8yMi8vLhceMzA1Mi0rLSopKCssKB0gHiEkIhwaHR0aKCYeHiYoKDAuLS4wMSspKiooJBoUIBwSFRERDRIVExcRFhYY",  #hide
    "FBYVGA0UFhweIB4fJCYeHSAfHh8mKiklJioMABIjKCwnKCcsIyMfHRsiJCUjHSctJSAbGR8hICEkJikoKSctKSouNDQz",  #hide
    "MDEvKCcoJSYaGR8hFh8dHRsbIBwVGBkhJiEcIy0lKikvKy8uLispLiYgFRUeFREYFhENDQ0bHQoRGBESGhYYFRofLCIm",  #hide
    "KScqMCUhJyIhJyowKyYnLR0PIyojKisrJiUdHyIWFBYZGRYPGSAYHBobIiIiJiciJSItLC0rLisrLjIyMjAsKykoKyUh",  #hide
    "HxsXGxocGyAcGBISGiEnJyssIiQnJC4rLisqKTExLiwgHRUWDAsKDxMNDxMcGx0aFRUeGhkeHxggJCAaJBseHhgVExMd",  #hide
    "IyMcHBgjJzAhGRccIRwdGhcYEQsPEBEPFhEUExUWHxwcHiMhIB0bGSorLiwsJisuLy4uLy8sLi0sJycfHhoaGxoYHx0Y",  #hide
    "FBEUHSMmKCglJCcnKS0uLCsqNTQzNS8mGhkDARMRHBsfICkpJCEgJywnJycoJighFRAeHBcdHQ8ZGiAfHx0WGSEeHxkd",  #hide
    "HSYiGBwZEhoSCgkMDRMXFRMbFRUhIR4bJR4fIB4bKSguKy4qKi0xLy4uLiwvLCspLSkkGx4fHRYcGhoVEBEcJSkqIBwh",  #hide
    "LS0pJSosKiovLSUjIxcQFhkhIQ8PFRcUHh4aEhEUFBoaFRUWHBkWFRodIBkeHRIZIxolJBsTEBceGR4jIhYaIRURFRcL",  #hide
    "BxMXExYUFhoWDxodISElIx0YISEpKi0rLCYlLTIuLikuLywpLisuKikjJCQfGxobGBIeFRQhJCYlHAwiMSwmKSsmJiQg",  #hide
    "GRwODwoTIiMSDAkICwoSGxsREA4PFB0VGxYVFRohHRYeGxkYFRMbHCQdHSAZExwcHyIeEhgbGx8aFg4MDRITGBgUExUR",  #hide
    "DhIXHyAaFRMhJSYmMC0nJCwuLy8uLTIuLygrKi0rKiYoICEiHhsWEh4aExocJSYYDSEsKy4xLiYoJSkhJRUVDg4PEhYR",  #hide
    "CwsSERIXGhAPERAbJBcaFRQWGyAcGBwbGBkXEBsaJR4YFRgQFhwjGR0dGhsZHxkTFhEOEhMaFhkPFRQOExgZGhUSEBwh",  #hide
    "JCguKy8rMC8uLjAyMy4sKysmKS0sJSYhIyQgGxcOEhkZJSEhHyMrJCUuKy4sKSUYHhsaEhQTERcNDhAOCgsLFRscHRUP",  #hide
    "GRkdGxgQFRgdGyAcKR0cHB0WGh4jGRccGxkdHxgTFR8XGB0gHBgYFBQVExYXFxYaFxEREg8QFBURGBsqJiopLC0vMCst",  #hide
    "MigrMC0sLiUvLywpKiIeJScgGA4SHB0jJyAfISclJCwoKCQmISUbFxUREhQWHRkUERQNDQ4PFxoaGBUZFhoZFxoREBgc",  #hide
    "ISIqHh0YHhUiLCMNExUbHSAVExUeHBoVGx8ZGhYVFw4MFBgRFxUSExEODxMWFRkaGCEiKiorKiwrLS00Ly4pLCknLTIu",  #hide
    "LCosJiEqJhwfHiAhHh8kJB8hISkoKyUmJSYlJyAVHBMREhUbGxYRCxQYFRIVHRUVExMUFRchFxYYFxgYICohHhwbICMk",  #hide
    "JhETFhsaHBgTGBwWHBkYGhcdHRoSDRAZFhASFRATFhQQFBcWGh8VHh8rKCcpKiouMDIwMCQpJycnKywnIissLCwjHRwk",  #hide
    "HSMbISEdGSoqJCQmJS0kJSkbHRoaGBUXFxMWFQ8SGhsUFhMTERsXHBQZESEcExodHR8gKiciHBobIRwXGhwUDhQfGBMN",  #hide
    "ERYbGhscGiQdEREREBwYExIVFBcTFQ8RFhITHRUiIiQkISAlKy0tMC4tJSInLioqKiUoLC8tLCIeHyAWIiAeIR8bISQj",  #hide
    "JiQkKyIoJiMdHBwVFBISDxEQDxARFxMZEQ8TFh0bDRwXFhcXGyIgKCIoKSkpJCEqJBkTEhMTFBwVDw0OERYbGRkbHhsZ",  #hide
    "FxkSFxMTFhUOGA4VFA8QEhITFyYmKiEdIiooLC8uLy0iJyouKyoqKywqKComKCIiHBgnJB0bKSYqJBghJSstKSYeIyMi",  #hide
    "HhURFRUQDhQTFRAXFRYVFhQbIBcSHBYVERggJR8pJiorKiUmJigjHhcSFBsXHBoSFw8NDxEVFx8cFBsTExcXDxkYGBAO",  #hide
    "DxQTFBQRERQVHigsHh4mKS0vLS0tKyElKiklKiwsLSomLCkpKCEkHiMmDA0dHyUaFh0qLC4rKBsmJCMlHBcYFxQOExQX",  #hide
    "GhkSGRAUFhkcFxcgGxUTGB8kJCQkJSMqKSQjJh4bGRcXHB0hHBcUERIOEBYaHRwaHA4QFh4QERQWEA8MDgwTFhcRFBUi",  #hide
    "IyAdHyYrJi4uLCAfJB0eJC0xMTAuLiwrKiwpJCYqHx4WCw4UIR8oKC0sLiclKSoqHSEfEhERExQSDg8UGA4RGBsWFxYb",  #hide
    "FhobFx4hFx0jJyMoHiMgISMiIx4fHBoeHR4gGhoUGBYOEB0dHxsVEBUWHRYXFQ8NEQ4WFRkaGhAaFBweHh8hKSwpLjAr",  #hide
    "IyccHiElKCotLysuKyorLCciHx4cGiEWGRUgJCQjKCsqKissKywmICAUEREWHBsTEBQZEhEYGRMSERkZGxchJyMhJyAl",  #hide
    "KCYcGhkgIx0gIBwbHSMhJSMfFhUaFBgWGh4fFxYTExESDxMQEhITEg8PFhUWEhcWExokIx8hLCUpIysmJhYfLSYqLCwx",  #hide
    "KyopLi0vKicjCRokICEjHCIhHyIoJSoqKywuKCQjJiEUFA4UGAwNDREUEBMXFA8RIhwdHyonHCUpHR8kIh8fGx8kGBgg",  #hide
    "Gh0iGh8nIyUdGxkXGx0aGh0cGBIPDhQVGBUVEQ8PEBATEhcSGBYaHSEbIxohISkqKiIhHyElKCkqKi8sJisrKicnIygc",  #hide
    "JigmKConIRscHyUoKCMtLC0dHyogHB4dFg4NDxAQFxURDgwMFSMlHh8aJyYjHiEdHSIrIR0eIh4cFCIcHyEeHyIkJx4V",  #hide
    "FBwaIh4eHxwbFBYUFhUUEhEODhAUFRYSFRUbFhgfHxQXFx0gJyokHyAnIyEpKiYqKSsnKywpKSQYJiYnKCspJiUkHh8U",  #hide
    "HiYnJSgkLCchJyYZICEcGBAMEw0UExANDQ8THSMcJCUiISUdGxwkGiIiHRgkHhkiIhwhIB8dJhwiHxYSFB0mJSAiGhcY",  #hide
    "GxUeHxoUFg8REhgXFhISFBYUGh4eFQ4NHiAgIyQiHSQkHyguJysoKyknLjEtIyAnHyglLCAqKSYcKSQgIyQpJCYhIx4X",  #hide
    "JBsUIB0REA4PDA0QEQsNDhQYIiQlKConHiAgHB4fKSUdGiQgGh4gFxgcIB0iHBwaFhYPGh8fIyUaGxwdFyMdHRkbFBsQ",  #hide
    "FhUXFBEPExcZFRUTEBEcHCQgIiIbHCQhICUkJyoqJCcvKyYnHSUjJyYoKC8oJiMsJiIkJRwgJi8nHx0lHh0dGxEUCwsN",  #hide
    "EBIPCgsNFRkkHhslJxsiJyMaHiEpIx0iHx8jICUYFRcaJSUiFhgYHRccIR8WIBwgGx4eHxoYFxwOFhkREhQXExAVGxgX",  #hide
    "IRkXERUZIyMcGxkZHR4WIB8lJywlJyUqKSgoJyIpKyosLiMoLCwpKSYlISglMiciJCEZGxkaFhQKDwoODw0MDgwVGx8i",  #hide
    "JCUgHB8iGhsgICMfIR0ZJCUeIhwSFBYcHBkbIBkZHR0YHh4gGiIkIR8hGx8UGBkSFRERExMQFhkTFBgaICAcGyMkIBoZ",  #hide
    "GhwWHhkhISQjKiYiHiMmJikkISwuLyotKCopLSwoJSgmIyUwLyokJxwYIB8XFQ0PCg8LDQsPDRYZHyAfISQeICQhISAp",  #hide
    "KCEhHxkfJx0bGBMUERYaGh4cGBsbIyElHSEdHCMnISQjIR0cHBUQEBEREhIUGAwRFxkcHRUeHhwbIB4hGRkVHyEfHRsY",  #hide
    "ISYgJCgqJikqLjIrJiknKSknJicnKSYiIzQ1MyYpIhwYHhgXDxMLDg0OChAOGRYdHhocHxciHiEhICYiHSAkHh8gGRgR",  #hide
    "FRoUGR0dHBgUGBYjJiUYIh8bHSkgHR4hIR8dHBYVFRMSERARDxYaHRkXFRogIx4gHB8bFxYcHhkPGSQjJSEkJC0rKi0u",  #hide
    "KycjKigsJycpLCwoKiooNDEtJicgJhsbGRkNEA0RCw8NDA4WGR4ZHh8ZGiEcJSMgGh0iJiQoIh0gGhYUGhMWGRkUGRQZ",  #hide
    "GB4eIiIgJyMbJiIhHiMgGhsdGRgaGxsWEhEXFhocFRgUGyEaGRkTEBMUFxciHBgcHx0jISAhKCckJiknKCInKS4nKysu",  #hide
    "KyYpIyI1MS4sIx0tJR0eFQ4QDRINDQ0RDhMYHBgeHhccGiMnJigkFh0jKSQjJSEYExYYFB0cHBscFhUZGBYbICQkJB0i",  #hide
    "HRweKSAYHyYjIyEYEx4XGhoUFxEQEhATGRkYFBENDxEbHyQdFhUdFhsjJysuJCYqJScwLS8sLikrKy0rIh8kJDcyLyUj",  #hide
    "HCwhHSEZERgUERIMCw4KFhgcGRojHhwaISQkJCYbHCMiGB8hHBwUDxQVHRwiIBgZHCAfGyQaIBgcGyQkHiAlIRojKCUm",  #hide
    "Ix8bHyIbHR0ZFxUTEQ8cGBMNCxMTEhQYIRQVFBYYHicqKCYjKicjJy0qMDAwLC4vKyspIiIsNTErJyYgIiAhJB4WGg4W",  #hide
    "GBEODxYUEBscGRkcFxwdHxoZIhsdHh0dIR8iHxoVGBkiGRsbHxYdHCEVIBwdHRsgISEmHxUWHSEmKCYfKCQjGRYXGxUX",  #hide
    "FRQSGBgQExEMERQUFRQYGBwbGRgeGxgYGhgeHR8iLC0uLi0wMS4tLiwrJic4MzAsKCwmKCUkJRshFx0VGhYXGR4XGRce",  #hide
    "HRUSERwiHRciFxsXHCMoIicmHxMWFxoYGhoYGB8VHBcZGCAdHx4dICAeHR0hICkkKCklKCEeIR8fFRYTDREUEQ0SERIS",  #hide
    "ExQWFx8hHBsdFxsPGRkbFyAbIyQnKjAvKzAwLy8wLCgoJTgzNCsoIykgJCIgFhYaHxkfFxIRFxUUFSMbEhINEhoZFyEd",  #hide
    "GBghJScaHiUfDRwcGhccFRobGBceHBoeISAfGxwfJCIjIigjJCAmIyklHyIfHx8eFRIQDQ4REQ4PERYYEBoYGBgYDhYa",  #hide
    "HREcGxQUHBogICcrLCYrLS4wMS4tKSoqNCopKx4UIhscICMXFBQbICEXHRwVFxwbIxoVGBUZFhYaGR0gHCEmHBMMDhYU",  #hide
    "HBkjJBsWHRkYFB4eISMdGxwZHyMoHx4fJyQgJCUkJiMiIyEdICQdExEXExEOExMNGB0SHh0fFRgSFRUaHhsSFxQXGBYe",  #hide
    "JykqIisvMjM1MC0qKioxKiAjHhYiIRoVIh0UEA8VHh8ZGRwZHSUjIB4cIBsXGRsdICktMigWDwMBAgYMEB8hJRkdGBcc",  #hide
    "HyAkIiUhIyMoKCQbHhkeICIqLCYhJyIkISEeIRwcFRoYFBQXFBEUGhchHhsVFhASDRIUGRIXERMVHxgeIyYmLjIzMjEx",  #hide
    "LC0rKzUvJiUkER8ZGRUXGBsVFBQbGxccFBIdIB4iIB4YGBceJzM2MjAlIRsWEwcGAQIGEB4qJyIZHSAgHyghHyAnKC0l",  #hide
    "KCAdGB0hJignKCUlIR0gIRweGhgVGxMXExQXERcbERUWGBQXEBAOEQ4UGBgSExQhFwwaISEnKzEtLi8uKSwqNzQsJysV",  #hide
    "GRIZFhYZIRkaHhsXFBQTFRcaGxYWGB8iJTE6LyccFSAiICQfExEFAgICDyYrKCIgICghIyQiICQkLC0sKR8aGBYgJCEm",  #hide
    "IyAbICQhHyAVFx0aFRgcGxQTFxcVFRcgHBYUEhYWFxUaGhYfISAkEhEcGiQsMSwsLC4qKyo1MisoJxwhGx0VFBcZExQZ",  #hide
    "GxkTERERDhcZCxAWHi8zOCwkHxkbHCEoJSglGhUMAwIBFyotKSUjIycrJyYiKDAzNDQwIRILCBARGyUiGhUeHx0fIxwZ",  #hide
    "Hh0bIBwbGRMTExUYFCAbGBMZGhYXFRMcGBofJSUcFhIRIycrLy0sKyorKzYuLCgoGygZFhINDxUWEhgcGBYRDhMQFBcT",  #hide
    "FR4mNzkvHxkdHBwcJi0jJiohHhAFAgIEHy4qLCcrLS4nKiwvNDQwMS0lJBkOCQgIDhEUGRsdHR0nJx8cGR0jGx8gExUc",  #hide
    "GR4dGRMdGCMaExUUDxwXExciJCAbGR4jJjAtLi4uKBMaNC0wLSgaIh0TFAoDDhESFhocFBIVEQ4UFBsaITA3LCIcFBQZ",  #hide
    "GhsdKi4pISYcEwUDAgEVLS4sLTIvLiQvNzIpKCQpKiomKiMXFQwIAgUSICMgHSUjKBkVFx8jIxcaGRoaGB0fFRgUGCAd",  #hide
    "HSQlKicmJS0sLiwuKy4xNTMzMjInAQ4xLCopJSQiGRQODg4SGRISGh8eFxIUFA8PFRgpOC8eGhMZGh0cHygrLS0mKx4T",  #hide
    "CQMCARUnKykrMSspLzYvLywmJiQlIiYnGxwfHyATBwMKHh8fJiYqIhMDGCgjHB4eHh8iJSkdGx0hJyooMTAiHCMjKSUn",  #hide
    "JygqKCcoLi0qKCQkLC8tIyAnIR4YFxYWDxUYFxUdGxUQDBMcDxAdGyw3KCIYFh0YFyAlKC4oJSYiHBoLAwIDEBoXIx0c",  #hide
    "IjI3MjI2MysqKicpMy4dFRUYICYjHhQJEyowLzArEAglLCwsLSUmKSomKCAfGiAnJyIgGxwZGx0hISciIiYeHyoqJygp",  #hide
    "LCksMy4pJR4ZFxMXFhILCxYaFhweFQ8PEhYVFR0dJjMsIBgaIBgnKigrLicpJysoJQ0CAQQRJSsrHhsrNzQzNzcuLDM4",  #hide
    "ODY1KxsJAgMGDxccHxEDCiAiJyQtMC0kJSEeFx0eIRoZDhAOEA8TFRcWHhcbGyIoJCkkIiEfKScmJycoKCU1LSojIB0b",  #hide
    "GBgYFxIODhQZFBQVFQ8PFRUVHB8nMjUqIyovKi0sLjI0LzApLScgEgMMDh8yNzQqKjI0NDYzMS8sMC4kJCknIRUHAwIA",  #hide
    "AgkVFQ4CBxspLS8tMCorJCEeHx8oIxwTExQbERUeHBcWFRwhJSsqJyQiIyIkIyYoISIiHzUwKSwkGyAUDREWExgQEhUX",  #hide
    "GBgTEh0hGRwfGSYuNCMXFSAdGxoiJiQYHhQUFhwuLioUHCwqIyQkLjUzLB8eJi00KBcYFiApHQwDBwQBAQsYFQcCDCUt",  #hide
    "MSsvLzIrLCMmJicjJBoWExUZGhUVFBIRGCUqKyonKCYiJyYnJSEmIB0kNzUyMC4vLhUADiEhJSYnIygnJBsXISgnIx0a",  #hide
    "FxszIgoJFRMcHh4jJBgcGh8rNDk5KxcbKSEnLikvJiEgDRIjMzEqJSciHh8WERAGDAcCAQUTDQQDGygwLi8wMzIsJCMk",  #hide
    "KSAoHB4bGRcUEBAQDhQhISMpJSQmJSMjJigiIScjJCY4MjEoJigjHR0nHRwdHR0VExoWDw8PExIKDQ0KBhcvGgwREBMV",  #hide
    "IycqIh4jMjk4NDElGCQjICYjKB0XGR0JCSAuISQiFxoWGBgnLhcTEwcJBQQFAwELJS8uLiwyLy4nKiksIh4aGBggGhUO",  #hide
    "ERUSGh4XJCYhISQjHCInKSMoKiIcITYrJBoeGh4jLyQaFxUYGRISEQ8LDBUQDQ8SCwoHByUsEA4QERQkKiglLDM4NjQw",  #hide
    "LTA1Ni8hHRQlHyAhGg8HDxgaGB4aCREeHiUoKBoVEhMXDQMBAgMZLC0vLDAyMCwtLSggHRwgIiAfGhUTEhYXFhcdIiAe",  #hide
    "HB4cHSUnKSonHiAnMikpJiUhJyQiIBsWFBYVGhkTDAwLEw8MDg8ICQgHCh8hFRMTGCYkLTQ4NzY1MC0xNjUyMiQnJCYl",  #hide
    "Jh4dEQoJChIXGRcLBQsXIyMiJCYlFg0XBgICAQokMTAwMjEwLi0qLCcnIiIdIiEdGhQMEBMYFxkdHRwaHR8mJiwuJiIp",  #hide
    "IiMxJx8kHSAeIB8TGg8NDBMYEhYQDQwPExEHCAcIBgcGBQ8TCx4wHyU1OTc3NjMyMjU4Ny8pJycjIiQgIR8XFRARExgR",  #hide
    "DBAIBAwQGicjKSkjDQYGBAIBBx8uMTM1MzEvLiwsKCYlIxwhIh0UFxYTFh4cGBYcIBQVFCMgLiYiIyUlJzYnIB0YISUZ",  #hide
    "DA0ZFhUTGxsNEhAMDA4QEQkHBAUEBQYJCQoIMDEwNzg3Njc3Nzc2ODEuJhgdGxoaHyEeIhkVHxoZISAWFRAHBgYSGhwh",  #hide
    "IiIXCgMDAgAJIi4zMzQyMCwtLy8qJiAdFx8gHhcYFA4WIRwdGh4jFhgZIikqJSQmJyQlMyooIhsbIhsZNCsXFRUYFQ8N",  #hide
    "CA8ODQgIBwYDBAQEBAkKCRs2Lzc3NTc2Nzg2NTQ3KiYeGRYdGhQfHhgVFyEiJSQjHRsaEg4ECAsTEBUfIBcRAwECAA8m",  #hide
    "LTQ1NDIyLS8tLyopIB0aIBwYGRgbExgbISEeGxwZHSAkKiIfIyQqIyEwKyUlJCAlHCUqJhQUFhUTEA0KCgkJBwcGBgQE",  #hide
    "BAUFBxEcMjY1ODY0NTc3ODc2NS8qLRwXGCQhHSIkIx4jKSUmKykkGhYTGg0GAw0XBA4hIRECAQIADCYsMzQ2MzEvMiww",  #hide
    "KSIeHh4cGxoaGBsVER4eJCQgIh0fICIjKCIhHhwgJzArKBwgJiIeGxoYEhMPDg4RDAsJCAkIBwgEBAUEBQYPKC81NDc0",  #hide
    "Ky0yODY1ODgtJBofHxkYISkjJSYmJSEjKisrKCwnFQ0QDwwHAg8PAxUYCQICAgAHJyozNTY1NTIzMC8qKCIdIB0aGxoe",  #hide
    "GhEQFBYdHiEkIR4eJScjHyAeHh8oMSstIR8nHx4aHBkWExQQEhQNCQgJCAcIBwYDBAQIBh80MSQwNSsoMTQ4NjQ4NSkh",  #hide
    "Gx4eGh8pJycoKyooIigwMTEuKykkFxIPCwwEBhMDBxAEAwIBAQIhKDAyMzI0NjQwLS0xJiIiICIgHhkaFhEQGhofHyMg",  #hide
    "JBwbKSopJR4eGSAyLiofIh0dFxkUExAQEAoNEhEGCQgJBwoICAYGBQcHIzcsFCspLCktNjg2NjgyKCMkJCEcJCopKy8u",  #hide
    "IyUoJC8vMDAsKywhGA8JDQ4GCwYCAwIGAwEBAiEnKjA0MTQzMjMvLi4oJR0bHxsVGRsTEBAdGiQgGhIgIiEkLyolICQd",  #hide
    "IzUyKB4hISIbGBkZFQ4OEBEPDwsNCQ0JBwgJBwQFBwYdOSQYJSAoLzA0OTQ2NyoeISUhHR8eIyorKywnJywpLTEwLi8q",  #hide
    "LygYEAoNDgQMCgECAwQCAgECGisrMjQ1NTM0NDQvLC0qIBwaHBUWEQwQGR0YIxsOGB0nKSQvLyslIR8iNzAqKR4gGxgV",  #hide
    "GhUQDg8RDgkOCwkKDwgKDQoHBgQHAx45JyAlDg4tNTM4NzU2IxocIh8hJSMlJikrKikrMCosLy8tMSoqKR8MDRISBAwJ",  #hide
    "AQIHAgMCAgEFEB4uMjU1NDQ0MzIvLCQoIh0XGBUXDhIOGRYXGx4YGhkmIiwwLicfIiQ1KCwmGRsfGBobFxMPDw0NDQ8I",  #hide
    "CAsPCQwLBgYHBAYKKzchGCUTDh4uNDg4NzYpHh0iIBodIigpKiomKSYsKiwwLikvKiwsHxEVDg0LFQ0GAwYLBAICAwIA",  #hide
    "CCAyMTQzMzI0NDAtKS4pJiAcHBkMDQoTFBcYJSAbHykmKzAuIx0iITIwKiQbGxsYGRsTFw4NCw8PEAkLERANDwgHBwYI",  #hide
    "CQkqNR4VFQwMFRkjNDk4NCslIB8kGhciKCYpJSMrKictKygvKykkKiokFw8VCQwbEgYGGBsOAwICAgMACSgxMTAzNDUx",  #hide
    "Mi0rJygoJh4XGBITDBEQFRIdGBggKSgtLy4nHyUpMC0eISMeIBQJFBURDhENCwkNCQ8NFxAODAsFBgkQBCU4Hg8QCg8P",  #hide
    "ExInNzk4NC8oISIfHSMmJSgoJCshKSgsJyopKCMqKycfGxoJCw4FBxkfFSEQCQMCAgIAFS8yMS4xNTAuLS4nJyomJB4X",  #hide
    "ExMRFxIVFxgUEx8mLC8sKSomIiYzLyMhJCYjGhQUFxQSEgwODAoKCw0UDw0IDggHBwwJHDgiDgwLDgwMEhcnOTg4MSsl",  #hide
    "JSEdHBskJiUjIyAlIi4pKSImJikpKyImHhMKBgMgKh8TJh4bCwICAgEJJy0uMDEvMDIuLiYlJSMgHxwWGhAUEw8RFB8f",  #hide
    "HSgpListLSgeJC4wJyApKCAbIhoTGA0XFhUMDQ8LDw4ODQoKCAsKCg0cNSgXDgkLDQkSFxInOTg3MSkiHRgZGyIfISAm",  #hide
    "JiUhKSkrJyosKCMtICkfDwQDECopJiInIiMVAwICAQgmLjAvMDArKSknKCUhJB4XHRMXExUUEg4THB8cIScrJywrKBwe",  #hide
    "LCkeJCUhGSIcFBMWDxISEhAODBUSEBISDgwJCgkPDxYyLhEPDxANCRAXDR03ODg3MSQZFRYXGhciISAhKCIkJSssKiYn",  #hide
    "ISwqJhgIAQkcKSonJykmJBUCAgIAEy8wMC0rLS0qKiYmJh8lJBwYExQPFhUaExcSFRgiHCsrLC4rKyMvKR8gGx8cIBMU",  #hide
    "EhcUEBQSERMPEg4SFx0QEgkJCQkKBh80GhAQDw0MCQwVGSg4ODg1LBsVGhQZHyMhIh4oJCUmLi8sKiQmKiAYFgkBByAu",  #hide
    "Ky0vLiUmFAECAgAYLy0tLy0qLSopKionIR4eHR4QDRMbExkTFhMZFCMYKC4uKyonHi0nHBgZIBwXFhUSERIZERAYGhIT",  #hide
    "EhIVFw8QDQ4PDAwTCxsoJyMPDA4LCA0RHyw4ODEvJhgXGyInJiQlISopKi0xLysVISkaCxIOBgAYKi4uLSooGBoLAgQC",  #hide
    "ASAyLi0tKyssKikrKCYiHR0SEhoHDRYZHQ4SGBoaIyofLTEuLSsgLyYaJx8eGBUTGBkVFBwTFhgZDw8RFx0bERAOCQ8R",  #hide
    "Cw8PERklLBoPCgsMCw0UHik3NS01Kh8dJCgqKCgqLSwxMi4pIQ8OGRcHBgIEFS8tKScmIBsSEQ4IAQETKi0pKyUpKScf",  #hide
    "JSciHyMcGhAQEg4KFR0fGBkWHCQmHSItMjErKCEyKB0hICIdHBgaExgWFRMVERQNERUTFhUOERAMDhIKCw8TChcjKiUP",  #hide
    "CgoHChESGSUvNTg4MiowLi4vLi4vKSwtJhsSBgQHBQMBCCItMS8rKSoiHhIKDhQTIS8tLigfICMjIBkcHBkVGRsXDg8M",  #hide
    "EAoUExceHx0hIigjJCksLiwjJTEpHxgjHRUeFxINEhUWExoXExMcFRUcHBcUDg4OEhAMCwkKDBMZLiwXCwoNDw4QFhon",  #hide
    "Mjc4NzY2NDMyMC0jISATDAkDAQAABRghJystLC4vIQ4VFRkjJyswLSgkICIiGh0eGxgPEBUSFBILDw4OEBQTGBQXGyUm",  #hide
    "KiIjKSgsKyYhKSUjFxoXFRwWEwwOEhAVGhcbDxYaGhgWEg4KDg4PERIKCQsMCgweKywlFRAVFBkeHiAsKjQ5OTk2MzAs",  #hide
    "JRQPBwMBAQMJDBgfIh0fIychKConKS0qJSYmIyUpKiIZICAdGRYWGA4TERIRDQ4PDxIQEhYbFRYYJSsrKSclJycoIhku",  #hide
    "KiIgHiEWGRQRDxESDxcaFhYQGhkcGh0WEg0WEAsRDwwPDgoMDxQSEyUcGicqLyorJCosLCoqKjAnGxUHBAgIDRQYFyUo",  #hide
    "KCAfHCMlJCQlJSojISMjHyUjISUjJiAeHBkVExcZExYUEg4MCAkKERESEBcdGBsiJC0qKygnKScnIi8qJyUVFRoXEA8R",  #hide
    "DxMTEBMUEQ0TGh0iIBkTEhARFRYODxgRDREXHRQUEBUhICAoISkkIB0TCg4ZHhwUDRQZIyIhHiAeJSQhHRwUIh4bHiUl",  #hide
    "JSEgICIjKCgmICYnIhwdICMdEQ4QFRAQDgwMCwgSFxsSHiIhICIkLCUmKiwoKComMyklKhodHhkTEw0PFRINDxAWFhgY",  #hide
    "HBUcGhkUDBMbERMRFxMQEhgVEhMYFhIWFhkYHRQVFhUWHBYXFRYcJyUrKiAQGBkbHhsbIB8mIiUlJSgqJCcjJCssLCoj",  #hide
    "KCQcHhcWIxwTGRAPFxUPDhEQDhMZIRYZFh4bIichJSMjKCksKyQ2MC8vIiciHBoYEBYTFBIWEBMWHBwaGBcaIBQRFxoS",  #hide
    "FA4RFxEYFRMREhgZERgZHBocEhQXHBcaGh0TGyAeHSEgGRcaFRccGx8nJywnJSgpJSonIiAjHyYqKCMeIhsYFBobGRUW",  #hide
    "EREUEgwPDhUSFRQdGhkXGBwkJSYqJyElKCgpITQ0LCYhKSIbGhgVEQ0TDhMMEhUZFBQVFhcbFBQYGBoWExQTFx4bFg8U",  #hide
    "FBoVFxgaGR0ZFg4TGBkSGBQZFBkgGxwZFxcZGhcjJSYsLCknJS0mKikiISEhKSYkJyUdGRYXIBoZEBQVEw0TFRUJDQ8W",  #hide
    "ExkcIBkXHCQoLComHyIjIR0eNDEsKCQpICEbFBoXFBIQEAoVFBUVGRggFxYRFxkVGxoTEREVHB4XEBsYFxMSFxYcIxoT",  #hide
    "DhQZHBkUDxQRHR4aFxwZExYgHykoJSMqKSssLisrKyUdISMgIiQhHRkUFBgUEBYSEwwVDxEWEw4LDBYTFRIbFBYbJCsq",  #hide
    "LTApHh4fGR0zMicoHyMbHxQNERYVFBUPCREQHBYXFxwYGhkZHRQUFw8LEB4WFxsQExQOGCAbHB8cGBsQFhoeGRYRFRET",  #hide
    "FBcXGBIREh4hIiomJisoKS4vLycoKCcmISQkJCMXHRcVFhwQERMRCxUVEg8UEg8PERMWFyMTFSEqMS0mJiQfGxkjHDUr",  #hide
    "JCkiISQeERITEBARDhEPDBEaFhgYGxYZFBEUExISFBMSFhYVGhQVFBUYGxoZGCIbGxYXFyEYGxEPExgXERUaExkVHyAn",  #hide
    "JiUoJyYpLS4wLywtIiQmJh4gIRkXDxoWEQ8NDAwREBMZFBMQDxMVFR8YIhoWGykqLykgHBgaFxgYNi8nKSseIyEXFw4P",  #hide
    "EREQDA0SEhUUFSMiFRISERMNERocFhMXGBIYFRITEhEWFx0bJR4bFhwYHyAZDxMTFhwbFBkREhkeICMiJiIhJiwqLS4v",  #hide
    "LC0pJCEhJBgTEhUQEhMSExAUEA4SFBYbHBMWFRoaIiUnJSIgKyowLCkhJh0EBxswLCkvJyAYHhgTDBIQDg0LChIVExEY",  #hide
    "HSMUDxITExQYFRUPERMYERkVEhIREBsZGRwdFxwYHRwhISAfGBYVGSIfFw8UFxwgHiIlICgpKiwxMC4vKywlIhkbFxEZ",  #hide
    "Gw4NDxEPFBERERUaGRcqKyosKyYsLCstLS8wLjIzLCYoHQcYKDQyMDIvLB8bFA8TGhMPEhANEB4WFBsbHBsOEBIYFh8S",  #hide
    "DRAVEhgWDxQTERMSHSMgHRwYHBkcHB0hJh8YFhwXFBcYEB8hHiElKCcqLC0vMTM0MDEyMS4bABInIh4fHSMfIxwfGh8i",  #hide
    "IiQfIysrJBocIiMgIiMkHiQnJCUfFA8VIyseNTU0LikfGBUNExEMDREQExUTFR0YExMTGRQTFhcSEQ4ODwwPHhkaFBgT",  #hide
    "GBMXHBsVFhwgGB4gIh4iIxcXIyEfGBocKSsuLywuMDAvMTIxNjUwMSwuIxMTLCgkHhsdHRQUGB0THB8bFRYdGxUZGhsc",  #hide
    "IxofGxweJiYnJiEWFRUXIh41MTAuKSUVFg0MChEWGRUYFRQUGx4VDhEXIRgVEREbHBURFBshGCEhJx4ZHCMcCAAZKSkm",  #hide
    "LSstKSsrJB4oLS8qKCklJR8fIiQiJCMgIykpLjArJCMgJDEzJyEZFBEPDg8SEA4UDRgVFRUYExoVGRchGxcYHh0eJioj",  #hide
    "GxcaGRUfHjU0LjAqJiMeDQkOFQ0SEREVGRgXFxgXFx4aIRwgJiwlHiEiHiYjIygoKSAfHx4OFy0lJScoIyQsJhsaExgh",  #hide
    "ISAaHBgWHx4bJSMlJCIfJyQsKiksJCUhISkiIhQWDxMTEhESDBEUHhcfHR0WFRMZHichHiEgHiImKCchFBMYGRsfNzg0",  #hide
    "MjMqISECBhUYGRwgHSMoKiYiJSMfICMnJSsiFRcTDRMNFRQTGxsUGRkXFiUuIhkaHR8dIiYiDhMWFRwXFBcVFBcfIR0k",  #hide
    "Jh8iIhkiKCknJiEfIiUiKSIhFBgWFhUTERUMEREXFhkZExUXFB4mIyIjHx4iJyUkKCAUExETFRQ4NDI0MCgnFgwhHBcW",  #hide
    "GhsfIRsgIB4cHBsZEgwVHhMWFhgREhQRHyIVFQ0bGxsQGhojGyAbHiAnKR4WGhohJRkSFxcZGyIYISEdGhwlHR4kJikk",  #hide
    "Hh4gHR0pIBkXGRgcFhMUGBETEBYTGRcYFhcWHh4iJx8YHhchJSoiHBATExQdFTMwKSoiHhgdKiYPDQwTEhgUEBMZGBYV",  #hide
    "FhIKCA8cFRsXFhULCxMeJBsWERISFxUXFyAgIBkfIycmGRYWFSMhGhgXFhMWHRodIhsaHyQjGh8lHyQeIR0eHxsWGBYZ",  #hide
    "HR4UFhYXFxcQFxUaHR0UFRkjIicoJCMkISUoIh4XFRQSFBsWNDEqIyAgGh0VDxAQEREYHBcSEhIYHRcVFAwLERcXGBUR",  #hide
    "EA8PFRQfGhoVGRYgHhsXHRwiGR0lJxsWFRseIiEbHhsYFhgkHyMmIx4hHhkYICMfJxwfHR0gHRYaGxgbGRYcFRMTGBIU",  #hide
    "Fh0dGhMUFSUpIh0jJiQmISEeHRoTFhQVFxM3NC8qJychFxMUFRYUExoiFhIaFxcUGBoXEQ0RGhcYExIMExARDh0ZGREe",  #hide
    "GR0aHhgYExYXJRwmIxUSFhsgISAYGBgTIR4ZISEeGBYaFBoaIiEiHh8eGhskFhgZHBUbGSMbFhEdEBUdIBoXFxwZHRkd",  #hide
    "GSMlICUhHB0hGhQQExcdGTUwLTAnKyAXDw8QFRMUFhgYFRkWExIUGRQPEhQbIBsRDhEYFhgQGBkVEBgVGhwZFRkUFhoi",  #hide
    "ISYgFhIcHCMjIBogHhcZHBodJyEYFyEdGR0mIiIgHxkgGR4XHB8jGBsZHBweHCMVFx4eFxkbGyIjHSAiHiYhICMeGyEh",  #hide
    "FhAaFBIUMzMtLComIRUTEgsMFBMcGBUOFhMOERgaGxEUFh4eGRMUExMYHBgVEREVIBwXFBoeFBEVFh0fICAXEhgiKyQR",  #hide
    "FhofHBgbHBYiHhgUHRseHBwcIh8fFx8aGh4eHB4ZGBMfHSQgGBQWHyQbFhMYGx8eHCAfJiwjIRgZFxYXFx4bEBYxMi4t",  #hide
    "Jx0fFhMPDw8PERMPEhEUERMVFhUiFhcYHxcZFRYRFBkaDxUaFxETFSESHB8YERcWIRYYHhgVICYjJiAeFRUbHhwbGR4U",  #hide
    "FRQbGSAZGhcbHRsWFx0fGiIdGx4cHSUeJSQdFhsnJB4VGBoXICMjHyUqJCEiGhQXFRUZGhUZFzYxLi4kHBkQDhYMDRIO",  #hide
    "Dw4PFRYOGBodGxwXGRUXGBcQEhITFB4VFRoXExIWHBccGxsVGRUgGxwfGRsbHx4fHxkbHhkcHhkdGxsbHBsYJh0eGRoZ",  #hide
    "HRQXGBsVHh0gHiAeJR0cHB0gIyYkIh4dFRUiHCMmJCglIBkUEBsTEBIUFh4bODUuLiweGBUUEQ4LCgsNDw8REhkaGRYY",  #hide
    "FxIUDxkZHBMWExEOHBoYHRoREBcZGBsVGxEUGxogJh8eGxoZHR8fFhYdFxcbHhwbFhYZFxUdGyYXGRUVFRcZHR0ZGyEb",  #hide
    "GhojGiEiIh0dIikjJRsYFh4iISUlJyYfGRIPFRETFhQVIBs5ODExLSceHRIODwoICg0MCQkQGh8ZGBAXGxoVFBogGBcN",  #hide
    "Dg8RFBggFQ4VFh4XIh8UDRIbGRwlICMYFhsiIR4cFRoWFhsdEh4cGhMYHBoYJBkfJBwSGyEjHhkdHBoYHCQcJBwkIB4l",  #hide
    "Ix0XGSQfHCQkJSEoIxsVFRATEhIYFxUfGDg2MjAnJR4TEQ8ODQ8PEQ0LERUNFBceExcQExYUGBkZDwoOESAVFx4cEBka",  #hide
    "GxYfIBMNFhgTGB0fGx4fGyAcGBoXHRcVGxsZHR8dExYXHBQdFxwbHxUgICUbFRkdICEgIh0iJCEcGxwlGxYaISEdIiIg",  #hide
    "JCEgHRETEBMWExQdGxUXODcvJyIjHRUTEBIVFRIQEQ8PEREUDhgbGg8PDxcXHBgQEBUSKSAVGhwRExQaHiEdFxkaEhoX",  #hide
    "FBsZFR8YFR0bGhgVFhoZHhsiHR4WFBQUFB8YFhkbGRwdIhcYHhwXJCglIyQmIR4aHSYkIBsbJygjHiQkIRcUDxEZGBIW",  #hide
    "GhkXIh43NzEqKighGA8REhMSDhIRDgoMDw4LDxEYDhIWHBYaFxIOGRcdGRkYGhQTEBoeIRUVGhUTFxQYGBgeHxsYHxgW",  #hide
    "FhQYHholHCgfEhgcGhkSFxkdGxUjIBofHSUgHCIiKSceHx4jKRoXJSAXGxklKyAeISQgEhATFBkfFxMVHBYeGDg2MjAu",  #hide
    "KiUaFxgTEBUQEhAODRAUDg0UCw4MGBoYGBwTEhQVFx8ZHRsZGR0YJSUfFxkaEw8QEREYGRkcJBkXFRoYFRAZERwkHx0T",  #hide
    "FyEaFRMTGSQhHhwiIyIZGB0bHCAnJyIlHyMpHRUfHhsbHhojKSgeHxsNFBwaGRUTGxQZFRgVOTc1MzAvJCAfFxkSEg8Q",  #hide
    "DAsLEBISDhYODgoTFxYVHRAMDBUXHhYdHxkZGxgfICEeGxMOERkZEBcbFRshIh8bGBgVERUbGhkfHh0TGxQUExYXIR4h",  #hide
    "GhsdKiUUICAdIiUpIR4gJC8eERwZGRshIyQmKCEcFhQXExUYGRcVEBMSGRk4NzQ0LiYnHBoXFBIOEBIQCwsREg8NExAO",  #hide
    "DxMRGR0dEhAQFhodFx0jFxMWHB0bGhsaEg8QGBIUGBgeFh0eIBcWFBoVFxokFhgYGRIYFxkSGhkdHCMfGx0pKx4fIyEp",  #hide
    "JSckHB8lKhkVHBwbFCYnKCcmJhoZFRQXGBYXFxYUFxcaHTk2NDEsLioaHRcWDgsQFBAQFxQKDhARDw4MEBEZIiAVEw0X",  #hide
    "HiMYGB8jERYfIB4ZHBMSFxUXFxoeGBkXIRcYGRscGBUaGh0aFhQUGR4bFxEYFBofGRslKCojHSEgJCUgKSQeIx8iGhYa",  #hide
    "IB4bJiclIiQlEhkUEhgVGBcVFRUWGR0aNzMzMigkJx4aEhgQDQ4WDQ4UFQ4TDRUREQ8NExUcJBgUFBcYJR0dGRsUICEd",  #hide
    "HRQaERUeFRcZIRcRFyIhGBkgHBAUFhMUGRYVFRYVHRcUFRkaHRMZJCYmJh4eJR4gJyUoIBwkHiEdHyAeHSQiIh8fHxsY",  #hide
    "GBMYFBEVFhgZGx4WGxs4NDAtKCElIBsUFhMUEBUODQ0UDQ0QEgsRERAUFxgZFBYVGhcbGxoUEhMdIyEYFhwMDhcSEhoa",  #hide
    "FhETHhwZIBgVExcXGBQYFBwVERMaFCAXGh4jGBkfJyIcHRoeKCUlHh8eJCEjHx0fICMeHCQkISMbFRQUFhkVFxMYGBoW",  #hide
    "GhQcHzczMCsrJyIdGxUUFhYTFwoJCw8PERYUDg4TEg8WFA8XFxcYFB4gGRgWFBYdHRkaHQ8RFhMXHxUfHhYTGRkfFxUa",  #hide
    "GRkgHBoYGBQPERUVHBkfIyMXGhkgIiAaGiQsKCUdJh4cGhwfIB0lHh0gJCgiIBwXGRwYHRQUGRkXFRMUFhobODg2LSkr",  #hide
    "IR0fGBkTFBMbDw8PDxMXERETDw4TERIUFRkXFRwXIR0eHBsVFBkaGxgbFRQTDxAQExkYGhAaHCAUGBQSGh8lHBcXEAwP",  #hide
    "EhIdGx8hGRYdHiIgJSEbHiQfHyAlHRocHiAkIiIdHCMeIRsdGBgWFhMZGBcXFRUTFxkWGx06NjMvLCsnIB0aHxUWFh0Q",  #hide
    "DwsTFRcRDQsODxIXEg8UFBIUFxgdGxUWFxMVExQYGRcQFBISEQ0WEhAWFx8gIhsZFBkbHB8aFhQOEBAVExodJRocHhIe",  #hide
    "Hx4iHhseJSMlGxscIiEjHx8hKCQeHBsfGiEYGBcaFBcYFhEYExYVGhodIDg1NjMuJiUiIyIeGRgSFA0PEBIVERERCgoQ",  #hide
    "ExUWGRITFBYcGhsVGBkWFx0SExcYGREWFhYWERcaFhUZGh4dHRsSGBggGxsRERMRFR0UHyUkHh4YFRkdGhwdHCIqJici",  #hide
    "GRgbHB8fGh4iJiAeHB4gJRoXFxoVHRwYFRgZHRMSFyIhODQyMC8rHR4dHB4VEhUYDg8OFRURFBgNDxARFhkVEhMWERoX",  #hide
    "GRoXFhQbHBcZFBgdEhcTDxMWFRkUExgZGh8YFxMZFhseGxUWFxcUFhIeIB8bHRwaEx4aHB0cISQiJRwbIBsdIScfISAj",  #hide
    "Hx0gIh8fGx0UGhMYGxoTGhUYGhUXHCM4LzQwMCUbExcWHRUXFRgQFA0VExUYGBcRDQ4SHBYUFRcPEhsgFRYWFB0YGxsU",  #hide
    "GxwPFhIVFhsRGhIRFBccJRsVFBkbGhwXFRwaFRAWFCAfHx0gHR4XIhkXHR0ZGiUhHiQhHR4iIiMgHiQdHyAjJSMaHBch",  #hide
    "GRYVFxMUEhMWIB4XHDc0NDMkHCIaGxYaEhYRExIODBURFRoWFRIRERAVGhUREhQeHh0dGB4aFhQZHRoZHRQMFRUSHRYY",  #hide
    "FQ4VHBofFxYYHBgbGxweHhoTEhcWGR0hHRwbExkkFxsfFhUdISIfHh8ZICMiHB0fHyMiHCMiJR8ZFBgTFRIeFA4TFRUa",  #hide
    "GhsjNzQyNi4nIRkdGh0REhQPDwsMEhEOFhYVFQ0TGhQaFxEXHBURGR0YGBYaGRwcGxUVExQVEBEfHRYUDg0VGBYVHhYY",  #hide
    "FRoWIhweFBQSFxocHiEaHB4YGhchIBgVFB8cJCcbHRsaICEdHiMkIRoeJR4fISARGRUXGB8cGhIUFBcaHSA4ODU1MCsp",  #hide
    "GBMUGBERERULCw8WExIRFxcSDhIXEg4TExQXExMhHRgYGR8jJB4dFRQUFxUPExsVFxsSDBUXHBkUGBkZIRYZIR8bHBEV",  #hide
    "HR0ZHhweHhwWFxwbGBkcISEiJSEdGhshIyElHyMdIR0kHCIaGBMYFhcaHhseFg8XGR0eHzk3ODQwJygcERIUFBAPFA4R",  #hide
    "DRIQERUdFxALDBIbFhQSFxUXGSceGx8ZHRwhHhkaHhgcHRkaFxUVFRQQFRAXFhcXHhYYFhgaHBsaFRghIB0WGBkXHBsb",  #hide
    "HxYVGRMbHx0gHh4XFR0lJSMjIBweJCgdIBkdFhoZHBUbGxwcFBUfGRwdOzc1NS0qKiIdFRsRDwsQDQ4PEQ0UGRcQDA0K",  #hide
    "DiAaFQ8QDxUVGxsbHxghFxcWGRYeFhodHRQTFx4QExQYCxQVGRMaHB0WGxMXFhoXFxkgHhsWFQ4WGxUeGhQSFxwcGx8a",  #hide
    "FxoYGCQlIyMnHCIeIh8aFx8YHB4aEh0cFhUVFxwdGRw5ODcxLiolGxcTDwsNEQ8MCgoNDQ8QDwoSNS8XGh8ZDQ4TEhEW",  #hide
    "HB4bGh0gHhQWFw4VHiAbGhYYGRMTFxcRGxUWFyIcGxUYFxcbIRsaGBcbFRITERARFh4eFhQaGxkcGBQaIBwZKCcrJSYe",  #hide
    "JSQjHB0YGxYZFxgYHR0dFxcZGx4gHjg3ODEvKSAbGRETDw4RDxANCA4PEA8VDRUgHRITHRsRDhEREhwaHB0UFxwhHxsX",  #hide
    "GhYZGRoZGhsUFhkTEhEWFBoXHRUWFRsXHBgYFhgdHyEZFRYMEBUbGBsdFBscGSQYGR0bIBYgJSopKSEmIygcIBwTESEb",  #hide
    "GRgeHBwWFBsfHSAkOzk5MzMrLCIcGhkNEA8NDgoLEA4TExMMERUZFxcYFRMSDxQTGxoZFxQcFhseHR0WFRkbGBsfJB8Z",  #hide
    "GxkfEBEWGxkYFRUVHBYjHBcaGxUbGhgXFRAWFxQXGRUVGx0cHSQYGR4gHiMoKiUjHiMdJSAeGBcVHhwbGhkZGBYdHBYV",  #hide
    "HyA7ODY1MickFRURDgoMDwwKDAsRFBQWFQ8TFhkbHR8ZDhUSDxgaHRgfGhUWHxMXGxUOEx4lGCIjIBYcHCAXGRgZFhQZ",  #hide
    "FBQXGR4cHRkfGRcaHxQNDxIRFBoUFBESFx8dJBsXGiIgKSYnKiokKisrJyMjIB0lISQhKSMdJSUhDwMhKjo3NTMxKxsY",  #hide
    "FA8PEQ0NDAwODAwPEBMSEREVFBEcGxkcFxMSGRohGRsWFhkTFRsQEBAZFRkZGR4bGB4aHhoeFxkVGh4YFxshHxsbGh0d",  #hide
    "GxwcFhQRDxEQDQwTHR4aHCAhGh4bJSkrKiotMjExKC0uLyspIicmKScpIxwkJxkMHzArOjc3NTMlGxgWFBEMDQoNCgkO",  #hide
    "Dw8REBETERUXER0hExkYFx4WGRoYIBYVGhMcGxkUFBYdHhkbGhodHRkkHCEZFBEaHSEgJiYqKyomJycnIyEkHx0eGQMF",  #hide
    "Gx0kJCUoKiopLCovMjEuMzMxMiweIhohGxoTFxMUFhsWEhQZHyUxKSA6NTc4MCIdFRYMDg4NCgsMCQ4PDhMRFBUPFxQV",  #hide
    "HSMaFhsgGxsjIhwXExUVFBUXEwoMFRgdFSMaGiIgHSQbIx8eGyQoLCosKSIjJiEfICMiHB8aExUODSEfHBkZGx0bHSAk",  #hide
    "KiUlKCoqKS0qIx0lFxogGhEaFhUXHhoVGh4mJScoJw==",  #hide
])  #hide
# END MARINER DATA  #hide
mars = permutedims(reshape(base64decode(image_b64), reverse(image_shape)))  # bytes are row by row
@assert size(mars) == (128, 128) && maximum(mars) < 64

# --- snippet rm_code: Reed–Muller RM(1,5) ---
G_rm = vcat(ones(Int, 1, 32), [(pos >> i) & 1 for i in 0:4, pos in 0:31])   # 6 × 32
pixel_msgs = [(v >> i) & 1 for v in 0:63, i in 0:5]   # the 6 bits of each grey level 0..63
rm_codebook = mod.(pixel_msgs * G_rm, 2)              # 64 × 32: one codeword per grey level
rm_weights = vec(sum(rm_codebook, dims=2))
@assert sort(unique(rm_weights)) == [0, 16, 32] && count(==(16), rm_weights) == 62

# --- snippet decode: Nearest-codeword decoding by dot products ---
rm_signs = 1 .- 2 .* rm_codebook          # bits as ±1: 0 → +1, 1 → −1
function rm_decode(received)              # rows of 32 received bits → grey levels 0..63
    scores = (1 .- 2 .* received) * rm_signs'           # entry = 32 − 2 × (Hamming distance)
    return [argmax(row) - 1 for row in eachrow(scores)] # − 1: grey levels start at 0
end
@assert rm_decode(rm_codebook) == 0:63

# --- snippet channel: Send the image through a noisy channel ---
using Random
p = 0.10                                  # probability that each bit flips
rng = Xoshiro(1971)                       # Julia's generator: other draws than numpy's, same odds
pixel_values = Int.(vec(permutedims(mars)))           # row by row, as in the notebook
N = length(pixel_values)
draws_coded = rand(rng, N, 32)
draws_plain = rand(rng, N, 6)
plain = mod.(pixel_msgs[pixel_values .+ 1, :] .+ (draws_plain .< p), 2)   # no code: 6 bits
received_plain = plain * (1 .<< (0:5))                                    # back to grey levels
received = mod.(rm_codebook[pixel_values .+ 1, :] .+ (draws_coded .< p), 2)
received_coded = rm_decode(received)
wrong_plain = count(received_plain .!= pixel_values) / N
wrong_coded = count(received_coded .!= pixel_values) / N
@assert wrong_plain > 0.4 && wrong_coded < 0.01
@show wrong_plain wrong_coded

# --- snippet simulation: Guarantee versus actual error rate ---
p_over7 = sum(binomial(32, j) * p^j * (1 - p)^(32 - j) for j in 8:32)   # more than 7 flips
sim_draws = rand(Xoshiro(32), 20000, 32)
function failure_rate(q)                  # send the all-zero codeword (row 1); ties count as failures
    scores = (1 .- 2 .* (sim_draws .< q)) * rm_signs'
    best_other = vec(maximum(scores[:, 2:end], dims=2))
    return count(best_other .>= scores[:, 1]) / size(scores, 1)
end
sim_p = range(0.02, 0.30, length=15)
sim_coded = failure_rate.(sim_p)
@assert failure_rate(p) < p_over7         # the decoder beats its 7-error guarantee
@show p_over7 failure_rate(p)
