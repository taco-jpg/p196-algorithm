# Current X11 target: phase-0 U=(9,12,6), even-centre extension

Let B and W be the canonical phase-0 rooted p12/m9 words in calculation/decimal_frontier/lattice_kinks/data/lat_p12m9.txt, and define P(q,k;J,C)=H++C++reverse(H), H=B++W^q++J++(9,12,6)^k.

Target: for every J over coefficients 0..18 of length 3 or 4, and every even palindromic coefficient centre C of length 14,16,18,20,22,24, decide whether the exact 120-step decimal reverse-and-add epoch P(q,k;J,C)->P(q,k+5;J,C) returns for all independent q>=14,k>=100.

Refuted for this cell: all 137,180 junctions fail to restore even the required B++W^14 prefix at reference width (q,k)=(14,100). The exact U=(9,12,6) reset cones are (152,121), leaving 27 coefficients of U^100 outside both cones; therefore the endpoint is independent of every admissible finite centre. T12's insertion theorem lifts the reference-width obstruction to all q>=14,k>=100. See CELL_REPORT_U_9_12_6.md. The previous U=(9,10,8) cell is recorded in CELL_REPORT.md.

This is not a global no-go theorem. Longer junctions, moving interfaces, other rooted phases, and other band formats remain open.