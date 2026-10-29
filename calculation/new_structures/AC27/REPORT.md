# AC27: phase-6 fixed five-symbol junction census

**Label: COMPUTED.** The exhaustive decision is negative for the precisely stated **120-step endpoint-only** rooted p12/m9, clock phase 6, fixed |J|=5 T* cell. It is **not** an all-time decimal Lychrel certificate or a no-go for other seam lengths, moving/growing seams, or other phases.

## Exact cell and result

Write P(q,k)=H+C+reverse(H), H=B6+W6^q+J+U^k, with least-significant coefficients first and genuine canonical base-10 reverse-and-add. The rooted B6 has 34 coefficients, W6 has nine, J ranges over **all 19^5=2,476,099** five-symbol words (symbols 0..18), U over **all 30** distinct rotations of (9,a,18-a) for a even in 0..18; C may be **any physically realizable palindromic centre**, including both length parities. Reference widths q=14,k=100, target H'=B6+W6^14+J+U^105 with identical C,J. Input lattice is calculation/decimal_frontier/lattice_kinks/data/lat_p12m9.txt.

All **74,282,970** U/J pairs were checked with an unpruned AVX2, 32-lane folded-coefficient two-sided carry cone. **Every pair has a definite W6 mismatch at the 120-step endpoint, at an index in [133,156], strictly before the junction at index 160.** Restoring W6^14 is necessary for the claimed fixed T* return. For every lane, the W-prefix through index 159 was resolved; unknown carry cases 0, short-prefix cases 0, unexpected overflow clocks 0, W9 restorations 0. The actual overflow phase is (0010)^30 with exactly 30 length gains. No intermediate W9 damage was used as a rejection criterion.

## Exact first-mismatch histogram (coefficient positions, **not temporal steps**)

| First differing W9 index (LSD-first) | Count | Prefix survivors after this index |
|---:|---:|---:|
| 133 | 19,244 | 74,263,726 |
| 135 | 487,893 | 73,775,833 |
| 136 | 25,729,805 | 48,046,028 |
| 137 | 19,739,428 | 28,306,600 |
| 138 | 11,299,727 | 17,006,873 |
| 139 | 14,377,059 | 2,629,814 |
| 141 | 2,287,465 | 342,349 |
| 142 | 134,760 | 207,589 |
| 143 | 87,203 | 120,386 |
| 144 | 94,863 | 25,523 |
| 145 | 13,285 | 12,238 |
| 146 | 9,732 | 2,506 |
| 147 | 995 | 1,511 |
| 148 | 1,288 | 223 |
| 150 | 171 | 52 |
| 151 | 45 | 7 |
| 152 | 3 | 4 |
| 153 | 1 | 3 |
| 154 | 2 | 1 |
| 156 | 1 | 0 |

The histogram totals 74,282,970. "Prefix survivors" counts assignments without a W mismatch at any smaller or equal reported index; zero remain after index 156. There are no observed first mismatches at omitted indices. Per-U histograms are printed by the executable.

## Why unknown centres are genuinely covered

For a palindromic pair-coefficient source, normalization's carry map is c -> floor((x+c)/10). If x=9 it transmits c, while if x!=9 the carry out is independent of c in {0,1}. The engine follows both low and reflected high carries, recording the nearest resolved non-9 from the unknown interior. Its coefficient validity mask is retained only when that higher-index reset is known. Thus each flagged W mismatch holds for **every** completion of the unknown centre and the unobserved inner U bulk. The first 340 coefficients are given; 120 steps shorten the conservative known cone to at least 220, with validity verified at index 159. This is endpoint-only carry propagation, not the unsound strict-per-phase W9 MDD.

The independent reimplementation used for the completed run also passed **36,000 complete pairword/partial-cone transition comparisons** (30 U x 5 J x 2 centre parities x 120 steps). Ordinary unbounded Python integer reverse-and-add was cross-checked on **310 runs x 120 = 37,200 genuine steps**, across (q,k)=(14,100),(20,100),(40,200),(80,400),(160,800), 30 U groups plus the rare J=(14,5,14,16,4), and both C=[4,4] and [4,14,4]; a separately implemented schoolbook adder matched all 120 steps at q=14,k=100. W-cut-relative offsets agreed across those five widths. These finite-width controls are differential validation, not the proof of a uniform pumping theorem.

## Reproduction and missing lemma

Run `bash calculation/new_structures/AC27/run.sh` (C++17, AVX2, OpenMP, Python 3). This uses the already-audited Z11 centre-free cone implementation adapted only to the exact phase-6 B/W rows, all U rotations, and shifted overflow clock; the selftest checks all 30 U. `control.py` independently checks actual decimal integer addition and the odd/even centres. The complete global histogram is above. This closes the finite **PHYSICAL_TSTAR_RETURN_AT_REFERENCE_WIDTH** W9-necessary-condition cell for P=6, |J|=5. T12's all-width cut/insertion theorem is relevant to extending the exclusion, but no Lean-checked phase-6 all-width proof is asserted here. The missing constructive lemma remains a regenerating moving/growing seam (or another mechanism) with a genuine nondepleting all-time return.
