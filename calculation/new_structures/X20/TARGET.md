# X20 target: rooted p12/m9 U6 240-step seam return

**Status:** EXHAUSTED-NONE for this fixed U6 / short-junction cell; do not treat this as a global no-go or a decimal Lychrel certificate.

Fix the canonical phase-0 rooted exterior `B0 W0^q` from `calculation/decimal_frontier/lattice_kinks/data/lat_p12m9.txt`, with `|B0|=34`, `W0=(5,18,4,8,1,15,4,0,5)`, and true overflow clock `gamma_t=1` iff `t mod 4=0`. Use the six-column charge-zero band

`U0=(3,3,9,15,15,9)`,

and a finite junction `J` of length 3 or 4, each coefficient in `0..18`. The candidate folded pairword is

`P(q,k;J,C) = H C reverse(H)`, `H = B0 W0^q J U0^k`,

with a physically realizable palindromic coefficient centre `C` (if `C` has odd length, its middle coefficient is even).

The macro target is 240 genuine decimal reverse-and-add steps, clock `(1000)^60`, and `P(q,k;J,C) -> P(q,k+5;J,C)` with `q` fixed. The exact missing seam obligation is a physical 240-step return of the complete `B/W/J/U/C` interface. A uniform two-counter cut/insertion theorem reduces the return question to `(q,k)=(24,100)`. The exact two-ended carry census finds no endpoint W9 restoration for any of the 137,180 short junctions, with independent ordinary-integer controls.

**Scope boundary:** this lane concerns only the fixed U6 word above and `|J|=3,4`. It does not decide other U6 motifs, longer junctions, the original U3 target, or base-10 Lychrel existence globally.
