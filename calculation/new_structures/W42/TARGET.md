# W42 target

Exact missing lemma: determine whether the phase-0 rooted p12/m9 cell with U=(10,8,9), odd palindromic centre C of lengths 3,5,7,9,11,13, and seam length |J|=3 or 4 can preserve the full B34 W9^q prefix through the required 120 ordinary reverse-and-add steps for every independent q,k beyond a bound.

Template, LSD-first pair coefficients:
P(q,k;J,U,C) = H ++ C ++ reverse(H)
H = B ++ W^q ++ J ++ U^k
B and W are the canonical phase-0 words in calculation/decimal_frontier/lattice_kinks/data/lat_p12m9.txt.
U is fixed to (10,8,9). J coefficients lie in 0..18. C is a palindrome over 0..18 with an even midpoint coefficient so it has a canonical decimal realization.

Success requires the exact physical 120-step endpoint P(q,k+5), all 30 overflow bits at the rooted clock, the full B34 W9^q prefix intact, and a seam image in the same cell. A finite-width replay alone is not a result. This task only targets the first necessary condition, strict preservation of B34 W9^q; a failure there excludes every same-cell cycle in this slice.
