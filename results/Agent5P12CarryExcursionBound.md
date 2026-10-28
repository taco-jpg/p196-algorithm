# Agent5P12CarryExcursionBound

**PAPER PROOF.** For the decimal period-12/m=9 absorbing lattice,
every first symmetric bulk coefficient defect initiates a finite
carry-state excursion: in ALL 12 temporal phases, if the successor
pairword keeps matching the baseline, then within at most 11 bulk
columns the two-sided carry state must RETURN to baseline (ending that
connected excursion), or a successor pairword coefficient must differ.
The exact per-phase maximum matching-column delays, in phases t=0..11,
are (9,11,7,0,9,11,7,0,9,11,7,0). Every reachable nonbaseline
subgraph of the 36-state gamma0/684-state gamma1 transfer is acyclic.
This is a connected-excursion bound ONLY: independent later defects
can cause arbitrarily delayed visible mismatches, as proved separately.
Scope excludes exterior/centre-reaching defects, multi-step centre return, any decimal certificate, and the orbit of 196.
Proof: `reports/Agent5P12CarryExcursionBound.md`; reproduce: `python3 calculation/decimal_frontier/lattice_kinks/code/k2_component_dag.py`.