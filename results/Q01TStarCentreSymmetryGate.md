# Q01TStarCentreSymmetryGate

**PAPER PROOF.** The exact T* U3 bulk map sends every one of the 30 charge-zero rows around a 120-step gamma=(1000)^30 phase cycle; each row's carry-reset value tau_U is 0 at 60 phases and 1 at 60 phases.

A palindromic centre C can preserve the bulk complement-reflection carry law only if C has odd length, its non-9 coefficient types alternate low/high, and its central coefficient is low when tau_U=1 and high when tau_U=0. Even-length C cannot preserve this law at any phase.

**Corollary:** no single phase-independent centre can preserve complementary carry reflection through all T* phases. A centre collar that breaks the symmetry or a phase-changing centre state remains possible; this is not a general no-go for decimal certificates.

Proof and exact formulas: reports/Q01TStarCentreSymmetryGate.md. Reproduce: python3 calculation/new_structures/Q01/tstar_phase_center_gate.py. Controls passed: 1,440 canonical-integer phase/U checks and 419,920 centre/carry cases. No full T* return or Lychrel number is claimed.
