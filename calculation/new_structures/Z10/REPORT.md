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


## Slice 12/12 — phase-0 J5 (2026-10-29)

**Status: EXHAUSTED-NONE. Label: COMPUTED, using the existing T12 PAPER PROOF for the all-width reduction.**

Scope: rooted decimal p12/m9 phase 0, |J|=5, all J in {0,...,18}^5, U ranks 12 and 24 in the canonical lexicographic 30-rotation ordering: U=(9,2,16),(12,9,6). Each U has 19^5=2,476,099 J words; combined domain 4,952,198. Reference width (q,k)=(14,100), representative centre C=[2].

The direct bit-sliced scan checked every J for each U. Each run retained all 2,476,099 clock-valid cases and 0 restored the required B34 W9^14 prefix. No MDD prefilter was used. Full mismatch histograms are in `scan_slice12_output.txt`:

- U=(9,2,16): -25:27,582; -24:59,015; -23:1,159,779; -22:984,589; -21:113,160; -20:113,548; -19:8,029; -18:8,728; -16:951; -15:594; -14:81; -13:40; -11:3.
- U=(12,9,6): -25:28,114; -24:58,189; -23:1,160,989; -22:984,633; -21:113,780; -20:112,721; -19:8,109; -18:7,711; -16:916; -15:806; -14:78; -13:52; -12:1.

Each histogram sums to 2,476,099; all mismatches are 11–25 coefficients before the W9|J cut. Independent arbitrary-precision checks of the first 64 J words match the C++ mismatch histograms exactly: U=(9,2,16), -23:26/-22:38; U=(12,9,6), -23:25/-22:39. Forty more true-decimal controls cover q=20,40,80,160 with k=5q and reference (14,100); all exact 120/240 overflow clocks match, and no control returns the full template or reaches a palindrome through step 240. See `bigint_controls_slice12.tsv`.

The existing `results/T12Rooted120CutPumping.md` theorem reduces any fixed-J/C/U uniform return to (14,100). The reset-cone bounds leave 26 protected coefficients in U^100, so the tested B34 W9^14 prefix is independent of every admissible finite palindromic centre. Since every J fails the necessary prefix test, no fixed-seam member of this U slice can be the required uniform all-width return. This is not a global nonexistence proof for decimal Lychrel numbers.

Reproduce from repository root:
```sh
g++ -O3 -std=c++17 -Wall -Wextra -o /tmp/z10slice12 calculation/new_structures/Z10/scan_slice12.cpp
/tmp/z10slice12 --lattice calculation/new_structures/Z10/input_lat_p12m9.txt > calculation/new_structures/Z10/scan_slice12_output.txt
/tmp/z10slice12 --lattice calculation/new_structures/Z10/input_lat_p12m9.txt --limit 64 > calculation/new_structures/Z10/scan_slice12_first64.txt
python3 calculation/new_structures/Z10/replay_controls_slice12.py --lattice calculation/new_structures/Z10/input_lat_p12m9.txt --out calculation/new_structures/Z10/bigint_controls_slice12.json
```


## Slice 9/12 — phase-0 J5 (2026-10-29)

**Status: EXHAUSTED-NONE. Label: COMPUTED, using the existing T12 PAPER PROOF for the all-width reduction.**

Scope: rooted decimal p12/m9 phase 0, |J|=5, all J in {0,...,18}^5, U ranks 9 and 21 in the canonical lexicographic 30-rotation ordering: U=(8,9,10),(10,8,9). Each U has 2,476,099 J words; combined domain 4,952,198. Reference width (q,k)=(14,100), representative C=[2].

The direct bit-sliced scan checked every J for each U. Each run retained all 2,476,099 clock-valid cases and 0 restored the required B34 W9^14 prefix. Complete histograms in `scan_slice9_output.txt`:

- U=(8,9,10): -25:28,051; -24:58,236; -23:1,159,623; -22:984,631; -21:113,827; -20:112,754; -19:7,828; -18:8,813; -16:1,135; -15:951; -14:113; -13:137.
- U=(10,8,9): -25:27,891; -24:58,744; -23:1,159,760; -22:984,640; -21:113,462; -20:113,407; -19:8,357; -18:8,437; -16:858; -15:457; -14:6; -13:80.

Each histogram sums to 2,476,099. Every first mismatch is 13–25 coefficients before the W9|J cut. Independent arbitrary-precision checks of the first 64 J words match exactly: U=(8,9,10), -23:28/-22:36; U=(10,8,9), -23:26/-22:38. Forty additional true-decimal controls cover q=20,40,80,160 with k=5q plus the reference (14,100); all clocks through 120 and 240 steps match, no full template return occurs, and no control reaches a palindrome through step 240. See `bigint_controls_slice9.tsv`.

The existing `results/T12Rooted120CutPumping.md` theorem reduces any fixed-J/C/U uniform return to (14,100). The reset-cone bounds leave 26 protected coefficients inside U^100, making the tested B34 W9^14 prefix independent of every admissible finite palindromic centre. Since every J fails the necessary prefix test, this U slice has no required uniform all-width fixed-seam return. This does not prove global nonexistence of decimal Lychrel numbers.

Reproduce from repository root:
```sh
g++ -O3 -std=c++17 -Wall -Wextra -o /tmp/z10slice9 calculation/new_structures/Z10/scan_slice9.cpp
/tmp/z10slice9 --lattice calculation/new_structures/Z10/input_lat_p12m9.txt > calculation/new_structures/Z10/scan_slice9_output.txt
/tmp/z10slice9 --lattice calculation/new_structures/Z10/input_lat_p12m9.txt --limit 64 > calculation/new_structures/Z10/scan_slice9_first64.txt
python3 calculation/new_structures/Z10/replay_controls_slice9.py --lattice calculation/new_structures/Z10/input_lat_p12m9.txt --out calculation/new_structures/Z10/bigint_controls_slice9.json
```


## Slice 8/12 — phase-0 J5 (2026-10-29)

**Status: EXHAUSTED-NONE. Label: COMPUTED, using the existing T12 PAPER PROOF for the all-width reduction.**

Scope: rooted decimal p12/m9 phase 0, |J|=5, all J in {0,...,18}^5, U ranks 8 and 20 in the canonical lexicographic 30-rotation ordering: U=(6,12,9),(9,18,0). Each U has 2,476,099 J words; combined domain 4,952,198. Reference width (q,k)=(14,100), representative C=[2].

The direct bit-sliced scan checked every J for each U. Each run retained all 2,476,099 clock-valid cases and 0 restored the required B34 W9^14 prefix. Complete histograms in `scan_slice8_output.txt`:

- U=(6,12,9): -25:27,957; -24:58,522; -23:1,158,670; -22:985,914; -21:113,610; -20:113,240; -19:8,662; -18:8,000; -16:652; -15:722; -14:56; -13:94.
- U=(9,18,0): -25:27,961; -24:58,604; -23:1,159,866; -22:984,427; -21:114,357; -20:112,060; -19:8,091; -18:8,772; -16:967; -15:813; -14:70; -13:103; -11:8.

Each histogram sums to 2,476,099. Every mismatch is 11–25 coefficients before the W9|J cut. Independent arbitrary-precision checks of the first 64 J words match exactly: U=(6,12,9), -23:31/-22:33; U=(9,18,0), -23:27/-22:37. Forty additional true-decimal controls cover q=20,40,80,160 with k=5q plus the reference (14,100); all 120/240 clocks match, no full template return occurs, and no control reaches a palindrome through step 240. See `bigint_controls_slice8.tsv`.

The existing `results/T12Rooted120CutPumping.md` theorem reduces any fixed-J/C/U uniform return to (14,100). The reset-cone bounds leave 26 protected coefficients inside U^100, making the tested B34 W9^14 prefix independent of every admissible finite palindromic centre. Since every J fails the necessary prefix test, no fixed-seam member of this U slice can be the required uniform all-width return. This is not a global nonexistence proof for decimal Lychrel numbers.

Reproduce from repository root:
```sh
g++ -O3 -std=c++17 -Wall -Wextra -o /tmp/z10slice8 calculation/new_structures/Z10/scan_slice8.cpp
/tmp/z10slice8 --lattice calculation/new_structures/Z10/input_lat_p12m9.txt > calculation/new_structures/Z10/scan_slice8_output.txt
/tmp/z10slice8 --lattice calculation/new_structures/Z10/input_lat_p12m9.txt --limit 64 > calculation/new_structures/Z10/scan_slice8_first64.txt
python3 calculation/new_structures/Z10/replay_controls_slice8.py --lattice calculation/new_structures/Z10/input_lat_p12m9.txt --out calculation/new_structures/Z10/bigint_controls_slice8.json
```
