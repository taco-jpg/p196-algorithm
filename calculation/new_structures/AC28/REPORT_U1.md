# AC28 phase-7 U=(0,18,9) carry-prefix no-return

**Label: COMPUTED.** Second complete U3-rotation slice of the phase-7, length-five rooted p12/m9 endpoint-only T* cell, following the general carry-prefix proof and code in REPORT.md and prefix_census.cpp (commit e3f37506bb08bef157205e68b2a928798daa0ada).

**Exact predicate.** H=B7 ++ W7^14 ++ J ++ (0,18,9)^k; P=H ++ C ++ reverse(H), every J in {0,...,18}^5 (2,476,099 distinct), all k>=100, and every palindromic coefficient centre C with a canonical positive decimal source. A fixed J/C return after 120 genuine decimal reverse-and-add steps to P(14,k+5) requires restoration of the 160-coefficient B7 ++ W7^14 endpoint prefix.

**Missing lemma supplied, in one sentence:** for the second U rotation (0,18,9), every length-five phase-7 junction has a centre-independent strict W9 endpoint contradiction after 120 true decimal steps, for all k>=100 (q=14).

**Method.** The already committed exact two-high-carry prefix evaluator uses the known 50-copy U collar and quantifies both possible carry values (0,1) entering the mirrored high suffix. It tests only the final 120-step W9 restoration, not strict W9 preservation at intermediate steps. The soundness induction in REPORT.md applies unchanged. An uncertain overflow, an insufficient known prefix, or a W9 match is never classified as a negative.

**Reproduce** from calculation/new_structures/AC28:
g++ -O3 -march=native -std=c++17 -fopenmp prefix_census.cpp -o prefix_census
./prefix_census 1 4 0 2476099

**Complete census output:** 2,476,099/2,476,099 J codes visited; gammaWrong=0; uncertain=0; short=0; W9 endpoints preserved=0. Runtime ~1,107 seconds on the shared four-thread machine. Exact first differing coefficient index, LSD-first:

| Index | Count |
|---:|---:|
| 136 | 821673 |
| 137 | 1028957 |
| 138 | 225001 |
| 139 | 352660 |
| 140 | 6293 |
| 141 | 35902 |
| 142 | 2274 |
| 143 | 1580 |
| 144 | 1436 |
| 145 | 163 |
| 146 | 139 |
| 147 | 14 |
| 148 | 7 |

Sum exactly 2,476,099. These are endpoint **spatial** first differences; no timewise-pruning histogram is claimed.

**Independent controls:** python3 audit_u1_quick.py passes 30 genuine Python unbounded-integer reverse-and-add endpoint trajectories, covering q/k=(14,100),(20,80),(40,160),(80,320),(160,640), three stratified junction codes and both fixed odd/even centres. Six full 120-step cases independently compare the two-carry abstract prefix against the actual BigInt pairword at every step.

**Scope:** one further U rotation out of 30. Together with the first U=(9,0,18) slice, 4,952,198 J/U choices are excluded centre-universally. The 28 other U rotations, moving seams, alternate q, phases and junction lengths remain UNDECIDED. No all-time base-10 Lychrel certificate follows.
