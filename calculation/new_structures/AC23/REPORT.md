# AC23: rooted phase-2 W9/U3 stationary five-site junction decision

**Label: COMPUTED** (finite exact exhaustive scan) with an independently checked carry-cone argument and conditional reliance on the existing T12 paper pumping theorem. **No decimal Lychrel certificate; no all-time orbit is proved.**

## Missing decision and exact scope

The missing all-time-proof sublemma this supplies is the **negative phase-2, |J|=5 fixed-junction branch of PHYSICAL_TSTAR_RETURN_AT_REFERENCE_WIDTH**: no literal junction among the 2,476,099 words and no U among all 30 charge-zero U3 rotations restores even the necessary B2 W2^14 exterior after 120 genuine decimal steps at (q,k)=(14,100), with the rooted p12/m9 overflow clock. A complete uniform T* fixed-J/C renewal must pass this gate; under the published T12 width-lift hypotheses it therefore cannot use this phase/length/U3 branch. This is a narrow obstruction, not a global impossibility theorem.

**Physical objects:** H=B2 ++ W2^q ++ J ++ U^k (least-significant coefficient first), P=H ++ C ++ reverse(H), and the necessary endpoint gate P_120[0:34+9q]=B2 ++ W2^q. The canonical B2 and W2 come directly from `calculation/decimal_frontier/lattice_kinks/data/lat_p12m9.txt`; all 30 U are sorted rotations of `(9,a,18-a)` for even a=0,...,18. All 5 J coefficients range independently from 0 to 18. Every transition is a genuine ten-base pairword normalization and reflected digit sum, never a finite-horizon guess; overflow carry and required temporal length are checked at all 120 steps.

## Exhaustive endpoint-only census

- Exactly **2,476,099 J per U × 30 U = 74,282,970 distinct J/U combinations** were checked with even centre `[4,4]`, `q=14,k=100`; all 74,282,970 trajectories have exactly the required 30 overflow events in the prescribed phase-2 schedule.
- **0** cases restore the necessary W9/B2 exterior at ordinary step 120; **0** literal 120-step fixed-J/C/U T* returns in this reference cell. There is no MDD or other strict-intermediate prefix pruning. Every cell is included, even if W9 breaks and later heals.
- The first mismatch on LSD-first coefficients is in positions **135..154** (W9|J cut=160); the closest failure is coefficient 154 (cut−6) for U=(0,9,18), J=(9,2,14,16,12). Complete 30-U per-rank histograms are in `hist_all.tsv`. Histogram totals assert the exact denominator, with no sampled/estimated rows.
- Both centre parities have been independently checked on all 30 U × first 64 J; U=(0,9,18) closest-miss controls were also checked at q,k=(14,100),(20,80),(40,160),(80,320),(160,640), both `[4,4]` and `[4,14,4]`. They all mismatch at cut−6 with the correct 30-overflow clock.

## Why only one representative centre is sufficient for this W9 gate

The T12 carry-reset difference rule is T_x(c)=floor((x+c)/10), with dependence on c only when x=9. The phase-2 finite 120-step U3 row evolution yields junction-facing/centre-facing front widths (150,120), (151,122), or (152,121), ten U each, max sum **273**. Since |U^100|=300, there are **at least 27 protected pair coefficients** between the two cones. This bounds centre influence on the junction and W9 endpoint at fixed reference width independently of the finite legal palindromic centre C (odd or even). The phase-2 W9 source-side retreat computation is 92 coefficients, leaving a protected rooted exterior. Thus every tested W9 failure carries to every legal C *provided the T12 carry/insertion hypotheses apply*. The result does not independently establish the entire T12 all-q,k symbolic pumping proof in phase 2.

## Strict-versus-endpoint diagnostic and reproducibility

An exact, **non-pruning** 120-step survivor trace for U=(0,9,18) is `step_survivors_u01.csv` (2,476,099 distinct J). At step 15, **31,437** junctions match W9 instantaneously, while **27,571** have matched at *every* previous step: 3,866 literal trajectories temporarily broke and healed the prefix. A concrete integer-realised example is J=(1,9,15,15,16), which first breaks W9 at t10 and restores it at t15. The strongest-miss J=(9,2,14,16,12) first breaks at t22, heals at t48..57 and t84..85, then fails at t86 and t120. Independent Python bigint reverse-and-add reproduces this exact chronology at five scaled widths. It is therefore unsound to treat a strict-phase MDD prefix as a complete endpoint-only pruner.

Reproduce from repository root:

```sh
g++ -O3 -std=c++17 -Wall -Wextra calculation/new_structures/AC23/scan.cpp -o /tmp/ac23-scan
/tmp/ac23-scan calculation/decimal_frontier/lattice_kinks/data/lat_p12m9.txt /tmp/ac23-hist.tsv --phase 2 --u all --count 2476099 --centre 2
python3 calculation/new_structures/AC23/aggregate.py
python3 calculation/new_structures/AC23/verify_first64.py
python3 calculation/new_structures/AC23/verify.py
python3 calculation/new_structures/AC23/cones.py
g++ -O3 -std=c++17 calculation/new_structures/AC23/trace.cpp -o /tmp/ac23-trace
/tmp/ac23-trace 0 2476099 calculation/decimal_frontier/lattice_kinks/data/lat_p12m9.txt
g++ -O3 -std=c++17 calculation/new_structures/AC23/witness.cpp -o /tmp/ac23-witness
/tmp/ac23-witness calculation/decimal_frontier/lattice_kinks/data/lat_p12m9.txt
```

`scan.cpp` independently matched **1,920 complete 120-step Python-bigint controls** (64 J × 30 U) for every first-mismatch histogram at the reference width, plus parity/width/near-miss controls in `verify.py` and the documented witness checks. This is a scoped negative reference-width decision, not an exclusion of longer, moving or growing junctions, U4/mixed U, other phases or q-changing returns. The missing *positive* all-time lemma remains a physically rooted, self-reproducing decimal repair of the seam/centre and a nonpalindrome guard through every iterated macro.
