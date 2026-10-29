# X24 current exact target: mixed U6, phase 1

Decide the 240-step epoch seam map for the phase-1 row `U6_1=(17,14,17,1,4,1)`, obtained from the mixed six-column cycle seeded at phase 0 by `U6_0=(7,7,9,11,11,9)`.

- rooted p12/m9 source halfword: `B_1 ++ W_1^q ++ J ++ U6_1^k`, mirrored around a legal palindromic coefficient centre `C`;
- `q >= 24`, `k >= 100`, `|J| in {3,4}`, every J coefficient in `0..18`;
- 240 genuine decimal reverse-and-add steps, with the target inner exponent `k -> k+10` (60 overflow columns = 10 U6 copies);
- `C` includes every legal finite centre, both even and odd (odd midpoint even).

A necessary condition for any fixed point or finite epoch cycle is restoration of the entire rooted `B_1 ++ W_1^q` prefix at step 240. The phase-1 U6 cone is `(left,right)=(299,239)`, W9 erosion is at most 181, the W insertion cut has guard 17 at q=24, and the U insertion cut after 55 U6 copies has guard 31. These reset/insertion bounds are intended to lift the reference-width decision `(q,k)=(24,100)` to every `q>=24,k>=100`.

The previous U3 phase-1 cell exclusion remains documented in `CELL_REPORT.md`; this target is a distinct mixed-U6 follow-on, not a global Lychrel proof.
