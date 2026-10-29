# Z07 J5 slice 7/12 report

**Status: EXHAUSTED-NONE for the exact assigned cell. Label: COMPUTED.** This is a scoped negative result, not a decimal Lychrel certificate and not a global no-go theorem.

## Exact statement

For the rooted phase-0 p12/m9 template with the published B34 and W9 rows, every one of the 19^5 = 2,476,099 length-5 junction words J fails to restore the full required B ++ W^14 prefix after 120 exact pair-coefficient reverse-and-add steps at (q,k)=(14,100) for each assigned U=(6,9,12) and U=(9,16,2). Thus the shard has 2 * 19^5 = 4,952,198 (J,U) cases, 4,952,198 exact clocks (100010001000)^10, zero restored W9 prefixes, and zero full returns to P(14,105;J,U,[0,0,0]).

The contribution is an exact finite obstruction for this fixed phase-0 J5/U slice, redirecting further search to other U ranks, longer or moving seams, and other clock phases. It does not close the constructive regenerative lemma globally.

## Why the finite computation decides this cell

The C++ engine enumerates every base-19 word J in [0,19^5) for each U, with least-significant coefficient first. It applies the exact pairword normalization recurrence for all 120 steps to the full literal representative P(14,100;J,U,[0,0,0]), checks every overflow against g=(100010001000)^10, and compares the endpoint against the required W9 prefix. There is no J pruning. The only removed dimension is the centre: T12's published two-sided reset-cone/insertion theorem protects the W9 cut from the centre for k>=100 and reduces a fixed (J,C,U) return at all independent widths q>=14,k>=100 to the reference width (14,100). The observed mismatch is inside the W9 band, 11–25 coefficients before its J cut, so no full template return can exist for any legal palindromic centre C in this fixed-J/U cell. Odd-centre-only mod-11 gates were not used; even centres are covered by the centre-independence argument.

The strict-W9 MDD was not used as a hard prefilter. A strict-at-every-phase filter is not sound for an endpoint-only return question because temporary W9 damage could in principle be repaired by phase 120. Direct enumeration is complete and took about 10 minutes per U on the execution host.

## Exhaustive output

Both runs completed with exact count 2,476,099, all clocks correct, prefix_restored=0, and full_return=0.

| First mismatch offset from W9/J cut | U rank 7: count | U rank 19: count |
|---:|---:|---:|
| -25 | 27,814 | 27,797 |
| -24 | 58,507 | 58,744 |
| -23 | 1,161,759 | 1,160,108 |
| -22 | 983,458 | 984,445 |
| -21 | 113,590 | 114,373 |
| -20 | 112,987 | 112,309 |
| -19 | 8,053 | 7,959 |
| -18 | 7,938 | 8,673 |
| -16 | 983 | 863 |
| -15 | 809 | 661 |
| -14 | 64 | 93 |
| -13 | 133 | 56 |
| -12 | 0 | 4 |
| -11 | 4 | 14 |
| **Total** | **2,476,099** | **2,476,099** |

Every first mismatch is within W9 itself, rather than the exterior B or the interior U/C. There were no mismatches at offsets -17 or other unlisted offsets.

## Independent controls

independent_bigint.py passed 40 controls: 2 U values × 5 representative length-5 J words × (q,k)=(20,100),(40,160),(80,320),(160,640). At every one of the 120 phases it cross-checked (1) Python arbitrary-precision n + reverse(n), (2) a fresh-buffer schoolbook decimal digit-array adder, and (3) the pairword recurrence. All 40 controls had the exact 30-overflow clock and failed W9-prefix restoration.

The published R30 symbolic engine was also locally reproduced for 10 representatives at q,k>=256; all had the exact clock, complete odd-pair witnesses, and an all-width first mismatch of the form 9q+c. The exhaustive classification does not rely on these ten symbolic spot checks. Reproduce symbolic checks with the official tools/parametric_verify_r30.py commands in run.sh.

## Reproduction

From repository root:

    bash calculation/new_structures/Z07/run.sh

The exhaustive C++ runs each enumerate all 2,476,099 junctions and take about 10 minutes per U on the tested host. The independent decimal controls and R30 symbolic controls run afterward. search.cpp has no external dependencies beyond a C++17 compiler; independent_bigint.py uses only the Python standard library.

## Scope boundary / redirect

This excludes only phase 0, |J|=5, U-ranks 7 and 19 of the fixed lexicographic ordering, for the rooted p12/m9 family with arbitrary legal palindromic C, under T12's stated hypotheses. It does not exclude any of the other 28 U rotations, other root phases, longer junctions, moving/phase-changing seams, or alternate template architectures. Do not rerun this exact shard; continue with an unclaimed neighbouring U-rank slice or a genuinely different interface mechanism.
