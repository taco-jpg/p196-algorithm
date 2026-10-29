# Agent3Rec2PerturbationRadius

**PAPER PROOF.** Decimal rec2 p8/m48 all-Boolean six-bit GF(2) local covariance (64 features, eight phases, 512 coefficients): the 2,252 reference/adjacent perturbations have rank388; all distance-two pairs increase rank to396; all contiguous triples increase it to398; distance-three pairs reach the universal maximum rank400.
Every +/-1 perturbation supported inside **three consecutive cyclic cells** is exhausted and leaves two nonuniversal solutions; support inside **four consecutive cells** suffices. All 34,236 additional arbitrary-distance two-site +/-1 rows alone reach only rank398. The 14 universal graph-coboundary masks per phase certify the 112-dimensional zero-function kernel.
Twelve explicit new independent tags plus 388 base tags give a 400-row exact rank certificate. No finite-centre exclusion, decimal Lychrel certificate, or Lean verification is claimed.
Full proof: reports/Agent3Rec2PerturbationRadius.md; complete code, raw lattice, compact certificates, exact commands, and independent digit-normalization checker: calculation/decimal_frontier/lattice_kinks/agent3_perturbation_radius/.
Reproduce: python3 calculation/decimal_frontier/lattice_kinks/agent3_perturbation_radius/verify.py && python3 calculation/decimal_frontier/lattice_kinks/agent3_perturbation_radius/independent_check.py
