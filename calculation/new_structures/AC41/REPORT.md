# AC41: phase-8 length-6 junction W9 endpoint obstruction

**Label: COMPUTED. Not Lean-verified and not a decimal Lychrel certificate.**

**Exact necessary-edge decision.** Let P=H++C++reverse(H), H=B8++W8^14++J++U^k, be the symmetric LSD-first pairword from the published p12/m9 root, with |B8|=34 and |W8|=9, J=(0,j1,j2,j3,j4,j5), each ji in 0..18, U=(9,0,18), k>=40, and any physically realizable palindromic centre C of either parity. A physical 120-step fixed-J/C T* return with k->k+5 requires the endpoint to have first 160 coefficients B8++W8^14.

**EXHAUSTED-NONE: 19^5=2,476,099 / 2,476,099 distinct J suffixes, zero W9 endpoint restorations.** All have exact expected physical 120-step overflow clock gamma=1000 repeated 30 times (30 actual overflows), and zero unresolved carry cones. First mismatch coefficient (zero-indexed): 135 in 1,359,194 cases and 136 in 1,116,905. Minimum/maximum certified final prefix length: 155/176, so every mismatch is safely within the known prefix and strictly before the W9 cut at 160. The result excludes this one stationary-J reference-width subcell for every k>=40 and every centre C, not all other U/J/q or moving seams.

**Soundness, inherited from AC11/AC15/AC26 (not a new lemma).** For a symmetric pairword whose first m coefficients are known, the high mirrored-prefix incoming carry is an unknown bit 0 or 1. When scanned from the interior toward the exterior, the first coefficient !=9 resets both carry possibilities; all digits beyond that point and the overflow become independent of the unknown interior. Together with the exact low-side digits from carry zero, this yields an exact next prefix of length r for overflow 0 or min(m,r+1) for overflow 1, where r is the highest index of a non-9 known coefficient. Induct through all 120 genuine steps without imposing W9 preservation at any intermediate time. Initial known prefix B8++W8^14++J++U^40 has length 286, and for k>=40 the two mirrored pieces do not overlap. Every unresolved state would be reported, never pruned as a failure.

**Reproduce.** Compile: g++ -O3 -std=c++17 calculation/new_structures/AC41/phase8_envelope.cpp -o /tmp/ac41. Run: /tmp/ac41 0 2476099. Parameters are first/inclusive and last/exclusive LSD-first base-19 J suffix codes (J1..J5); no sampled centres or strict-phase MDD pruning. Independent physical checks: python3 calculation/new_structures/AC41/independent_bigint.py. These check 25 true Python arbitrary-precision 120-step orbits, all intermediate pairwords against an independent schoolbook engine, and the five widths (q,k)=(14,100),(20,80),(40,160),(80,320),(160,640). Separately during local investigation, 10,000 adversarial random one-step free-middle cases and 100×120 genuine bigint/prefix tests passed.

**Exact missing all-time lemma remains:** find a physically carry-sound, nondepleting stationary or moving seam return with a complete nonpalindrome guard. This negative necessary-edge decision does not give an infinite decimal orbit and does not justify a uniform q>=14 assertion without the additional T12 cut-lift premises.


## Second complete U rotation (2026-10-29): U=(0,18,9)

**COMPUTED, EXHAUSTED-NONE at the identical phase8 J0=0, q14, k>=40, all-realizable-centre predicate.** This is the zero-based rank-1 rotation of (9,0,18), not a second run of the rank-0 cell. All 19^5=2,476,099 J1..J5 suffixes were enumerated without intermediate strict-W9 pruning; zero exact W9 endpoint restorations, zero unresolved cones, zero incorrect 120-step overflow clocks. Endpoint first mismatch index 135 in **1,358,747** suffixes and index 136 in **1,117,352** suffixes; terminal certified prefix lengths 155..175. Combined with the rank-0 result, exactly **4,952,198** distinct (U,J) combinations are decided out of 30×19^5 for the fixed J0=0 slice; the other 28 rotations remain **UNDECIDED**. Underlying centre-independent soundness is the same preexisting carry lemma, so this is not a new all-time theorem.

**Reproduce either independently:** compile the same phase8_envelope.cpp and run `/tmp/ac41 0 2476099 0` for the original rank 0 or `/tmp/ac41 0 2476099 1` for rank 1. The optional third argument selects zero-based U rank defined by a=0,2,...,18 and cyclic rotation. A distinct Python unbounded-integer / schoolbook source control with U=(0,18,9), J=(0,1,0,0,0,0), C=(4,14,4) passed every physical step at (q,k)=(14,100),(20,80),(40,160),(80,320),(160,640). This is code validation only, not an inference to q>=14.


## Third and fourth exhaustive U rotations (2026-10-29)

**COMPUTED, EXHAUSTED-NONE** at phase8, J0=0, |J|=6, q14, all k>=40 and every physically realizable odd/even palindromic centre:

- Rank2 U=(18,9,0): 2,476,099 / 2,476,099 independent J suffixes excluded, unknown=0, clockbad=0, final known prefix range 158..176. First W9 endpoint mismatch 135: 1,358,224; 136: 1,117,875.
- Rank3 U=(9,2,16): 2,476,099 / 2,476,099 independent J suffixes excluded, unknown=0, clockbad=0, final known prefix range 156..176. First W9 endpoint mismatch 135: 1,359,136; 136: 1,116,963.

Together ranks0..3 decide 4×19^5=9,904,396 distinct (U,J) assignments, with no W9 endpoint restorations. The remaining 26 U ranks and J0=1..18 are not covered by these four cells.

**Previously proved all-phase lift, not a new AC41 theorem:** AC35/PHASE_T12.md (PAPER PROOF, phase-start generalisation, plus phase_cut.py) establishes exact paired-insertion commutation and Return_8(q,k) iff Return_8(14,100) for every fixed J,C,U with independently varying q>=14,k>=100. Its phase-8 W protected cone loss is 92 cells, still leaving >9 reset cells beyond the cut52; all U words have junction/centre losses <=152/122, and k=100 leaves 13 cells on either side of the protected U cut. Accordingly each AC41 reference-width W9 necessary-condition failure also excludes the fixed-J/C exact physical T* return for these **all q>=14,k>=100**, conditional on that already published non-Lean paper theorem. No all-width claim is made for k=40..99 when q>14. This combination does not exclude moving J, q-changing 240-step returns, or solve decimal Lychrel.

**Reproduce ranks2/3:** g++ -O3 -std=c++17 calculation/new_structures/AC41/phase8_envelope.cpp -o /tmp/ac41 ; /tmp/ac41 0 2476099 2 ; /tmp/ac41 0 2476099 3 . Each enumerates the whole code range, checks the true physical (1000)^30 overflow and endpoint-only W9 prefix, reports no unresolved prefix in its output. An independently written Python bigint + schoolbook program checked 60 stratified 120-step controls across ranks2/3, both centre parities and five widths q14/20/40/80/160. Independently, 1,936 phase8 paired-insertion checkpoints for ranks2..5 agreed with actual Python big integers.


## Fifth and sixth exhaustive U rotations (2026-10-29)

**COMPUTED, EXHAUSTED-NONE** for every one of the 19^5 junction suffixes at phase8 J0=0, |J|=6, q14, k>=40 and every canonically realizable palindromic centre of either parity:

- Rank4 U=(2,16,9): tested=2,476,099, W9 endpoint failures=2,476,099, unresolved=0, wrong clock=0, final certified prefix length 155..175; first mismatch histogram 135:1,358,614 and 136:1,117,485.
- Rank5 U=(16,9,2): tested=2,476,099, W9 endpoint failures=2,476,099, unresolved=0, wrong clock=0, final certified prefix length 157..176; first mismatch histogram 135:1,357,542 and 136:1,118,557.

**Six-rank audited subtotal** (zero-based ranks0..5, i.e. the complete a=0 and a=2 triples): 6 × 19^5 = **14,856,594** distinct (U,J) combinations. All 14,856,594 fail the necessary endpoint W9 prefix, all have 30 true overflows and no unresolved carry prefixes. First-mismatch aggregate index 135:8,151,457 and index 136:6,705,137. The remaining 24 U ranks and other J0 slices are not included.

**All-width implication under existing AC35 PAPER PROOF:** this exact reference-width exclusion, together with the already published phase8 paired-insertion equivalence in calculation/new_structures/AC35/PHASE_T12.md, rules out a fixed-J/C 120-step return for every independent q>=14,k>=100 within these six U ranks/J0=0. This is not a new proof of the insertion theorem or any decimal Lychrel certificate. Runs with q>14 and k<100 are not claimed.

**Reproduction:** compile the existing phase8_envelope.cpp and invoke /tmp/ac41 0 2476099 4 and /tmp/ac41 0 2476099 5. The independent_bigint.py source now cross-checks 45 full true-decimal 120-step trajectories at five widths, including U ranks 2–5, with two independent integer / pair-digit update implementations. An additional 60 stratified q14/20/40/80/160 physical controls specifically for ranks4/5 were checked locally.
