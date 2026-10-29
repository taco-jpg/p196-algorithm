# X20 target: rooted p12/m9 U6 240-step length-5 seam return

**Status:** EXHAUSTED-NONE for the length-5 cell; do not treat this as a decimal Lychrel certificate.

Fix the canonical phase-0 rooted exterior `B0 W0^q` from `calculation/decimal_frontier/lattice_kinks/data/lat_p12m9.txt`, with `|B0|=34`, `W0=(5,18,4,8,1,15,4,0,5)`, and true overflow clock `gamma_t=1` iff `t mod 4=0`. Use the six-column charge-zero band

`U0=(3,3,9,15,15,9)`,

and a finite junction `J` of length exactly 5, each coefficient in `0..18`. The candidate folded pairword is

`P(q,k;J,C) = H C reverse(H)`, `H = B0 W0^q J U0^k`,

with a physically realizable palindromic coefficient centre `C` (if `C` has odd length, its middle coefficient is even).

The macro target is 240 genuine decimal reverse-and-add steps, clock `(1000)^60`, and `P(q,k;J,C) -> P(q,k+5;J,C)` with `q` fixed. The all-width U6 cut/insertion theorem reduces this route to `(q,k)=(24,100)` and makes the tracked prefix independent of `C`. The assertion-enabled exact compiled scan exhausted all `19^5=2,476,099` ordered junctions without modular or MDD pruning: no W9 endpoint restoration occurs. Together with the previously exhausted lengths 3 and 4, this excludes `|J|=3..5` for this fixed U6 word and all admissible centres.

**Scope boundary:** this lane concerns only the fixed U6 word above and `|J|=5`; the already-exhausted `|J|=3,4` and `|J|=5` reports are in `CELL_REPORT.md` and `CELL_REPORT_J5.md`, respectively. This work does not decide other U6 motifs, longer junctions, the original U3 target, or base-10 Lychrel existence globally.
