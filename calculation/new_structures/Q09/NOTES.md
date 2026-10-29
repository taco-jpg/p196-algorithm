# Q09 technical notes
Claim in #474: 6488339210. DONE for the universal columnwise symmetry theorem: commit 0312348a7b8d0fc622801dbaa863a1162f0359ae.

Positive controls: independently rebuilt base9 Lean-certified p10/m4 cycle and base50 four-step neutral cycle, bigint 80 edges at four widths (20,40,80,160). Decimal actual seeds 93(525)^m28 tested at those widths. Running full GitHub repository verify.py was unavailable; both new files are pure Python/PAPER and no Lean code is added.

Next analysis discovered rooted carry-preserving state-CONDITIONED coefficient maps: each fixed output-digit pi with pi(0)=0 and pi(9)=9 induces unique local pair-coefficient permutations a_0,a_1 (40320 in decimal). For the actual p8/m20 first rooted 39-column exterior B, seven mirrored carry mismatch indices 1,3,6,7,14,29,30 enforce pi(r+1)=pi(r)+1 for r=5,1,4,2,7,3,8. Combined with pi(0)=0,pi(9)=9, this forces pi=id. The first reversed-B coefficient 13 resets high carry for all centre contents and lengths, proving the seven constraints universally. Proof/independent 40320 enumeration/bigint tests in rigidity_proof.md and rigidity.py.
