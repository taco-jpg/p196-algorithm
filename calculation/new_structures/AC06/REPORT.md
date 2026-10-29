# AC06 centre-only return census

**Label: COMPUTED. Not a decimal Lychrel number or an infinite-time certificate.**

Rooted phase-0 B34 W9^q J U^k C reverse(U)^k reverse(J) reverse(W9)^q reverse(B34) in decimal, with J=[5], q=14,k=100, and U in {(9,10,8),(10,8,9),(8,9,10)}. All palindromic C of lengths 7 and 8 were exhaustively enumerated, no pruning. Seven-coefficient centres: 19^3*10=68,590 each U, with even central coefficient. Eight-coefficient centres: 19^4=130,321 each U. Exactly 596,733 cases across all rotations. All have 30 actual decimal overflows in 120 steps, gamma=(1000)^30; no candidate returns even the central radius-five coefficient window of the expected U^(k+5) C reverse(U)^(k+5). No full return and no return of the wider radius (122+|C|+30). Intermediate strict-W9 preservation was NOT assumed.

**Proof relevance, conditional on the published T12 PAPER PROOF:** T12 has 152-column J-side and at most 122-column centre-side U carry cones over 120 phases. k=100 yields 300 U coefficients and a protected 300-152-122=26 gap, so a radius-five centred necessary-condition mismatch cannot be affected by changing finite J. T12's cut/insertion theorem lifts the no-fixed-centre predicate to every q>=14,k>=100 and any finite J, for these C lengths and U words. This remains a one-epoch negative subcase, not an all-time existence proof; the larger 159/160 radius *alone* is not junction-independent.

Reproduce by compiling calculation/new_structures/AC06/census.cpp with g++ -O3 -std=c++17, then running for u in 0,1,2 and L in 7,8, arguments: u L 0 14 100 5. The output should give clock_ok=scanned and radius5_matches=0 in all six cells. The C++ enumerator is genuine exact decimal normalization of folded pairwords, with the overflow-index shift included.

Python independent.py verifies 90 arbitrary-precision decimal cases at q/k (14,100),(20,80),(40,160),(80,320),(160,640). It is a sampled independent check, not a second exhaustive implementation. Additional Python bigint controls for five distinct J lengths at 60 cases verified that the central radius-five window is J-independent. C lengths 9..14 were only sampled at 1000 deterministic IDs each/U, hence are **UNDECIDED**.

**Missing lemma this supplies:** a junction-independent necessary central-return condition, exhausted for all palindromic C lengths 7/8 in U-group m=5. The unbounded-centre search and periodic seam repair are unsolved.
