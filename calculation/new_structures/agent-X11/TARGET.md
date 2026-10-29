# X11 target: phase-0 U=(9,10,8), even-centre extension

**Status:** COMPUTED scoped exclusion; base-10 Lychrel existence remains UNDECIDED.

Let B and W be the canonical phase-0 rooted p12/m9 words in calculation/decimal_frontier/lattice_kinks/data/lat_p12m9.txt, and define

P(q,k;J,C) = H ++ C ++ reverse(H), H = B ++ W^q ++ J ++ (9,10,8)^k.

Target: for every J over coefficients 0..18 of length 3 or 4, and every even palindromic coefficient centre C of length 14, 16, 18, 20, 22, or 24, decide whether the exact 120-step decimal reverse-and-add epoch P(q,k;J,C) -> P(q,k+5;J,C) returns for all independent q>=14,k>=100.

The route is refuted for this cell: no one of the 137,180 junctions restores even the required rooted B ++ W^q prefix at reference width (q,k)=(14,100). T12's centre-side reset cone extends this obstruction to every admissible finite palindromic centre, not just the six requested even lengths. T12's insertion theorem lifts the reference-width obstruction to all q>=14,k>=100 for fixed J,C,U.

This is not a global no-go theorem. It excludes only this fixed oriented U3 cell with |J|=3..4; longer junctions, moving interfaces, other rooted phases, and other band formats remain open.