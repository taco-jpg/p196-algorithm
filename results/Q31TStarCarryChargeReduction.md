# Q31 T* Carry-Charge Reduction

**Label: PAPER PROOF (conditional necessary-condition reduction).**

**Missing lemma supplied:** for a phase-lifted rooted T* return with a protected U3 bulk and fixed finite collars, the global mod-5 carry condition reduces to one width-independent 120-phase equation.

For each phase, Q01 complementary carry reflection gives \(M_t(k)=3k+d_t\). The 120-step overflow clock and endpoint gain force \(\sum_{t=0}^{119}2^{119-t}d_t\equiv0\pmod5\).

The report also proves the scalar mod-99 clock identity and records that the mod-13 prefactor is width-independent. It does not treat Q54's unverified midpoint gate as a hard filter.

**Scope:** conditional U3 phase-lift only. No complete seam return, all-time nonpalindrome certificate, or decimal Lychrel number is claimed.

Report: reports/Q31TStarCarryChargeReduction.md  
Control: calculation/new_structures/Q31/verify_carry_gate.py