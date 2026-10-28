# Agent3CentreBoundaryFlux

**PAPER PROOF.** For every base b>=2, the half-pair-word weighted charge modulo b²-1 obeys an exact one-step boundary-flux identity: 2Q (no overflow) or (b+1)Q (overflow), plus a fixed-boundary source and a four-case *physical midpoint* source determined by n parity and overflow.
For decimal p8/m48 rec2, every returned bounded centre of any width and period T=192k must satisfy an explicit width-independent centre-source congruence modulo 9; the 48 possible exterior cut residues contribute zero to that congruence.
This is a necessary condition only. It does not exclude any centre or certify a base-10 Lychrel number; no Lean verification is claimed.
Proof and exact source formulas: reports/Agent3CentreBoundaryFlux.md.
Reproduce 90,000 schoolbook steps in bases 2..31 and all 48 rec2 exterior cuts: python3 calculation/decimal_frontier/lattice_kinks/code/agent3_boundary_flux_check.py.
