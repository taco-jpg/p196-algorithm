# AC20: phase-11 W9/U3 short fixed-junction obstruction

**Label: COMPUTED.** Exact unpruned finite decimal pairword census; this is NOT a decimal Lychrel certificate or a general no-go.

**Target.** In rooted phase 11 of the p12/m9 lattice, write P(q,k)=H C reverse(H) (LSD-first), H=B11 W11^q J U^k, J in {0,...,18}^3 or ^4, U one of all 30 rotations of (9,a,18-a) with even a=0..18, and C a realizable palindromic coefficient centre. An exact 120-step fixed-J/C return with q unchanged and k increased by 5 necessarily restores the entire B11 W11^q prefix at its endpoint.

**Exhaustive calculation.** At q=14,k=100, the direct C++ program enumerated 2 * 30 * (19^3+19^4)=**8,230,800** instances with C=[4,14,4] and [4,4], for both parities; each was evolved through all 120 base-10 carry/normalization steps with NO intermediate W9 rejection. **Zero** preserved the endpoint B11 W11^14 prefix; **zero** had an incorrect total overflow count or final length. Every first mismatch occurred at LSD index 135..151, strictly before the cut at 160. Histogram: 135:69276, 136:472992, 137:1000618, 138:5237312, 139:768186, 140:345946, 141:273832, 142:37824, 143:19844, 144:1924, 145:2464, 146:32, 147:466, 148:24, 149:28, 150:26, 151:6. Counts sum exactly to 8,230,800.

**Uniform carry-port reasoning.** Phase-11 W9 protected-prefix retreat over 120 steps is exactly 90, leaving 70 protected coefficients at q14, 18 beyond the stationary W insertion cut at 52. For the 30 U3 words the exact junction/centre retreat pairs are (150,119), (149,120), (151,121), ten words each. Because 300-272=28 clean U coefficients remain at k100, the W9-prefix necessary condition is independent of ANY realizable palindromic centre, including both parities. The U insertion cut after 55 copies retains minimum guards 165-151=14 and 300-165-121=14. Applying the already established T12 paired-insertion/reset-cone argument with the phase-11 rows lifts the reference-width W9 obstruction to all independent q>=14,k>=100 with fixed J,U,C. This is the precise proof-relevant reduction; it does NOT exclude longer/moving J, q-changing returns, mixed U, other clocks, or all-time decimal possibilities.

**Independent replay.** AC20/verify_independent.py uses real unbounded Python integers and 120 direct n+reverse(n) operations per trajectory; 160 trajectories, 19,200 physical steps, passed across (q,k)=(14,100),(20,100),(40,160),(80,320),(160,640), both C parities and selected U/J. An additional 480 real-integer cases with eight diverse palindromic centres and all 30 U rotations found no centre dependence of first endpoint mismatch in the tested J. AC20/phase_cones.py checks the 30 U cycles and phase-11 cone table. Neither sample substitutes for the exhaustive native scan.

**Reproduce.** From repo root:
- g++ -O3 -std=c++20 -pthread calculation/new_structures/AC20/census.cpp -o /tmp/ac20-census && /tmp/ac20-census 0 30 2 4
- python3 calculation/new_structures/AC20/verify_independent.py
- python3 calculation/new_structures/AC20/phase_cones.py
- python3 calculation/new_structures/AC20/reproduce.py --full (independent shared V16 collar implementation)

**Missing all-time lemma.** A 120-step returning repair with a longer or dynamic junction or a compensating q-changing regeneration. No actual decimal all-time Lychrel orbit has been established.