# AgentAC35AllPhaseRootedCut
**Label:** PAPER PROOF (finite exact carry kernel; true-integer controls), not Lean.
**Statement:** For any rooted p12/m9 starting phase p=0..11, any of 30 charge-zero U3 rotations, any fixed J and realizable palindromic C, and all independently large q>=14,k>=100, the genuine 120-step physical return P_p(q,k) -> P_p(q,k+5) holds iff it holds at (q,k)=(14,100).
**New finite bounds:** W9 120-step protected-edge loss by phase is (91,91,92,90,90,90,90,91,92,92,93,90); U3 left/right losses <=152/122. The phase-2 edge loss is 92, not the phase-0 value 91.
**Proof:** exact two-port carry reset and mirrored whole-band insertion, including gamma=1 shift. Every rooted B_p has an odd coefficient throughout all 120 phases, guarding nonpalindromes. See calculation/new_structures/AC35/PHASE_T12.md.
**Reproduce:** python3 calculation/new_structures/AC35/phase_cut.py.
**Scope:** Conditional reduction, no returning decimal seam, no Lychrel witness, no Lean proof; the unknown step is Return_p(14,100).
