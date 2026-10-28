# Agent3SpatialWeightsMod198

**PAPER PROOF (finite exact arithmetic certificates).** For decimal p8/m48 rec2, allow 384 independent phase/spatial pair-coefficient weights v_(t,j) and 384 independent descending-carry weights w_(t,j), with v_(0,0)=1. The cyclic bulk charge C_t(P)=sum_j(v_(t,j)P_j+w_(t,j)d_j(P)) obeys 11/2 covariance on all eight rec2 rows, every admissible one-site ±1 perturbation, and every adjacent two-site ±1 perturbation **if and only if modulus M divides 198**.
Four exact integer linear-combination certificates force M|396 (gcd of their RHS); an 82-term certificate forces failure modulo 4. Mod-2 weights v_(0,0)=v_(0,1)=v_(1,1)=1, all other weights 0, and mod-99 weights v_(t,j)=10^j, w=0 prove sufficiency by CRT.
Scope: only this restricted cyclic bulk covariance ansatz and its exactly 2252 local row tests. Not a centre-width exclusion, finite decimal certificate or Lean proof.
Proof: `reports/Agent3SpatialWeightsMod198.md`.
Reproduce from the commit alone: `calculation/decimal_frontier/lattice_kinks/agent3_spatial_mod198/README.md` (generator, raw rec2 data, independent checker, control runs).
