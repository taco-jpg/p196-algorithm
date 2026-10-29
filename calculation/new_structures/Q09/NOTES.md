# Q09 technical notes
Claim in #474: 6488339210. DONE for the universal columnwise symmetry theorem: commit 0312348a7b8d0fc622801dbaa863a1162f0359ae.

Positive controls: independently rebuilt base9 Lean-certified p10/m4 cycle and base50 four-step neutral cycle, bigint 80 edges at four widths (20,40,80,160). Decimal actual seeds 93(525)^m28 tested at those widths. Running full GitHub repository verify.py was unavailable; both new files are pure Python/PAPER and no Lean code is added.

Next analysis discovered rooted carry-preserving state-CONDITIONED coefficient maps: each fixed output-digit pi with pi(0)=0 and pi(9)=9 induces unique local pair-coefficient permutations a_0,a_1 (40320 in decimal). For the actual p8/m20 first rooted 39-column exterior B, seven mirrored carry mismatch indices 1,3,6,7,14,29,30 enforce pi(r+1)=pi(r)+1 for r=5,1,4,2,7,3,8. Combined with pi(0)=0,pi(9)=9, this forces pi=id. The first reversed-B coefficient 13 resets high carry for all centre contents and lengths, proving the seven constraints universally. Proof/independent 40320 enumeration/bigint tests in rigidity_proof.md and rigidity.py.

## 2026-10-29 T* continuation
- Read the last 40 FEED/COMBINE items on #474 and recent #475 activity. #474 is full/read-only. Latest constraints include scoped root-only and one-/two-symbol junction no-return results; a new π182 two-12-epoch W9 re-emission route remains short of a complete T* all-time certificate.
- Migrated CLAIM posted to #475 as comment 6491233819; DONE posted as comment 6491372705.
- Result commit: 49651f970f5f88d3b178d4b5544a87766ff97c42, self-contained checker/proof in tstar_symmetry.py. The theorem is PAPER PROOF: the rooted p12/m9 phase-0 exterior B0 admits no nonidentity carry-preserving state-conditioned digit-permutation quotient preserving a canonical symmetric pairword, for any realizable interior width.
- Exact gate: R0={0,2,3,4,5,6,7,8}; eight mirrored carry mismatches force pi(r+1)=pi(r)+1 and pi(0)=0, pi(9)=9, hence pi=id. The all-phase outer-boundary counts are (1,2,2,1,1,1,1,1,2,1,1,24); phases 1,2,8,11 retain candidates only at the boundary.
- Reproduction command: python3 calculation/new_structures/Q09/tstar_symmetry.py. The checker first runs Q09/check.py positive controls, then checks all 40,320 permutations across 12 phases and true canonical decimal sources/carries at q=20,40,80,160.
- These controls support the all-width carry-reset proof; they are not orbit extrapolation. The T* 120-step full seam return and decimal Lychrel existence remain UNDECIDED.