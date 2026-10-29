# Z10 report: phase-0 J5 slice 10/12

**Status: EXHAUSTED-NONE. Label: COMPUTED, using the existing T12 PAPER PROOF for the all-width reduction.**

## Exact scope

Rooted decimal p12/m9 phase 0, canonical B34 W9^q J U^k C reverse(U)^k reverse(J) reverse(W9)^q reverse(B34) pairword, |J|=5, every J_i in 0..18, and U ranks 10 and 22 of the lexicographically sorted 30 charge-zero rotations: (8,10,9) and (10,9,8). The full domain is 19^5 = 2,476,099 J words per U, 4,952,198 (J,U) cases total. Reference exponents are (q,k)=(14,100).

## Result

The direct bit-sliced scan checked all 2,476,099 words for each U. All words retained the exact rooted 120-step overflow clock (100010001000)^10 (30 overflows), but **0** restored the required B34 W9^14 prefix at step 120. Thus there are zero first-epoch W9-prefix survivors and zero full 120-step template returns. The first-mismatch histogram partitions every case:

- U rank 10, (8,10,9): offsets from the W9|J cut are -25: 27,691; -24: 58,452; -23: 1,158,888; -22: 986,256; -21: 114,516; -20: 112,500; -19: 8,369; -18: 7,619; -16: 1,036; -15: 611; -14: 156; -13: 4; -12: 1. Total: 2,476,099.
- U rank 22, (10,9,8): offsets are -25: 28,531; -24: 58,614; -23: 1,159,490; -22: 984,295; -21: 113,127; -20: 113,952; -19: 8,434; -18: 8,066; -16: 775; -15: 648; -14: 116; -13: 51. Total: 2,476,099.

No R02/V48 MDD prefilter was used: the compiled direct scan exhausts the entire candidate domain without pruning, so the result does not depend on an external prefilter's soundness or completeness. The mismatch histogram is asserted to partition every clock-valid candidate.

## Why the result lifts beyond the reference width

The scan uses representative C=[2]. The T12 reset-cone bound is at most 152 coefficients from the junction and at most 122 from the centre; U^100 has 300 coefficients, leaving 26 protected coefficients between those cones. Therefore the tested outer B34 W9^q prefix is independent of every admissible finite palindromic centre C. Every fixed-J/C/U uniform return must also return at (14,100) by results/T12Rooted120CutPumping.md. Since the necessary W9 prefix is wrong for every J at that reference, no fixed-seam member of this U slice can satisfy the required all-width P_120(q,k)=P(q,k+5) return for all independent q>=14,k>=100.

The existing root-only nonpalindrome guard applies to canonical sources beginning with B34 W9^7 W9[:2]; all these q>=14 templates contain that prefix. This guard is not used to prune the census. It is simply the known phasewise guard for any would-be rooted return.

## Independent controls and reproduction

replay_controls.py uses Python arbitrary-precision integers for literal n <- n + reverse10(n) and independently reconstructs pairwords. Its first-64-J histograms exactly match the bit-sliced engine for both U rotations. Thirty additional controls cover the all-zero and all-18 seams plus the closest-mismatch examples at q=14,20,40,80,160 (k=100 at q=14; k=4q otherwise). All controls have the exact 120/240 overflow clocks, no full template return at 120 or 240, and no palindrome.

From repository root, run:

    g++ -O3 -std=c++17 -Wall -Wextra -o /tmp/z10scan calculation/new_structures/Z10/scan.cpp
    /tmp/z10scan --lattice calculation/decimal_frontier/lattice_kinks/data/lat_p12m9.txt --u both > calculation/new_structures/Z10/scan_output.txt
    python3 calculation/new_structures/Z10/replay_controls.py --mode all --out calculation/new_structures/Z10/bigint_controls.json

The two-epoch check is correctly skipped because no candidate survives the necessary first-epoch W9-prefix gate. This is a scoped fixed-seam obstruction, not a global decimal Lychrel nonexistence result. The commit hash is recorded in the accompanying #475 DONE line.


## Slice 11/12 — phase-0 J5 (2026-10-29)

**Status: EXHAUSTED-NONE. Label: COMPUTED, using the existing T12 PAPER PROOF for the all-width reduction.**

Scope: canonical rooted decimal p12/m9 phase 0, |J|=5, all J in {0,...,18}^5, and U ranks 11 and 23 in the lexicographically sorted 30 charge-zero rotations: U=(9,0,18),(12,6,9). Each U has 19^5=2,476,099 cases, combined 4,952,198. Reference exponents q=14,k=100 and representative palindromic centre C=[2].

The bit-sliced scan was compiled and run directly over every J. For each U, clock_survivors=2,476,099, W9_prefix_survivors=0, and the first-mismatch histogram total is 2,476,099. No MDD prefilter was used. The complete histograms are in `scan_slice11_output.txt`:

- U=(9,0,18): -25:27,893; -24:58,828; -23:1,160,751; -22:983,301; -21:112,943; -20:113,596; -19:8,332; -18:8,576; -16:861; -15:798; -14:122; -13:75; -12:23.
- U=(12,6,9): -25:27,794; -24:58,557; -23:1,161,664; -22:983,641; -21:113,440; -20:113,328; -19:7,928; -18:8,083; -16:835; -15:701; -14:63; -13:37; -12:10; -11:18.

The mismatch histogram accounts for the whole domain for each U; all mismatches lie 11–25 coefficients before the W9|J cut. The independent first-64-J arbitrary-precision histogram matches the bit-sliced output exactly for both U words. The independent checker also ran 40 genuine-integer controls at q=20,40,80,160 with k scaled as 5q (and q=14,k=100): all exact 120/240 clocks matched; no control returned the full template at either checkpoint, and no palindrome occurred through 240 steps. See `bigint_controls_slice11.tsv`.

The existing `results/T12Rooted120CutPumping.md` theorem says a fixed J,C,U uniform return for all q>=14,k>=100 is equivalent to the reference return at (14,100). The reset-cone bounds give a 26-coefficient protected interval in U^100 (300-152-122), so the tested B34 W9^14 prefix is independent of every admissible finite palindromic centre. Since the necessary prefix is wrong for every J, no fixed-seam member of this U slice can be the required all-width 120-step return. This is not a global nonexistence proof for decimal Lychrel numbers.

Reproduce from repository root:

```sh
g++ -O3 -std=c++17 -Wall -Wextra -o /tmp/z10slice11 calculation/new_structures/Z10/scan_slice11.cpp
/tmp/z10slice11 --lattice calculation/new_structures/Z10/input_lat_p12m9.txt > calculation/new_structures/Z10/scan_slice11_output.txt
/tmp/z10slice11 --lattice calculation/new_structures/Z10/input_lat_p12m9.txt --limit 64 > calculation/new_structures/Z10/scan_slice11_first64.txt
python3 calculation/new_structures/Z10/replay_controls_slice11.py --lattice calculation/new_structures/Z10/input_lat_p12m9.txt --out calculation/new_structures/Z10/bigint_controls_slice11.json
```
