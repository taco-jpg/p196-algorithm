# Agent3VectorCarryCovariance
**PAPER PROOF.** For the decimal p8/m48 rec2 cyclic row map, consider the entire 48-parameter, time-independent spatial correction family C(P)=sum_(j=0..47) 10^j (P_j+alpha_j d_j(P)) modulo any M>=2, with d the actual unique periodic descending carry.
If C(F_g(P))=(11 if g=1 else 2)C(P) is required on the eight rec2 phase rows AND every admissible one-site ±1 perturbation, some alpha_0,...,alpha_47 exists **if and only if M divides 99**; alpha_j=0 works whenever M|99.
Three explicit perturbation differences already force M|(10^48-1) and M|990; their gcd is 99. No state cap and no assumption on the spatial period of alpha.
Scope: only this fixed-weight cyclic-bulk covariance ansatz. No phase-dependent correction, nonlocal centre invariant, finite-width centre exclusion, decimal certificate or Lean verification.
Proof: reports/Agent3VectorCarryCovariance.md.
Reproduce: calculation/decimal_frontier/lattice_kinks/agent3_vector_covariance/README.md (primary + independent checkers, rec2 data, exact controls).
