# AgentQ09TStarSymmetry

**Label: PAPER PROOF.** For the actual rooted decimal p12/m9 phase-0 B34 exterior, every carry-preserving state-conditioned digit-permutation lift that preserves a canonical symmetric pairword is identity, for every realizable interior width.

- The exact rooted mismatch set is R0={0,2,3,4,5,6,7,8}; with pi(0)=0 and pi(9)=9, it forces pi(r+1)=pi(r)+1 and hence pi=id.
- The all-12-phase outer-boundary enumeration leaves candidate counts (1,2,2,1,1,1,1,1,2,1,1,24); phases 1,2,8,11 retain boundary candidates only, not proven full-word symmetries.
- Checker/proof: `calculation/new_structures/Q09/tstar_symmetry.py`; run `python3 calculation/new_structures/Q09/tstar_symmetry.py`.
- The checker runs base-9 and base-50 positive controls and true decimal source/carry checks at q=20,40,80,160.
- **Scope:** this rules out only a fixed-digit, carry-preserving, state-conditioned phase-0 quotient. The full T* 120-step return and decimal Lychrel existence remain **UNDECIDED**.