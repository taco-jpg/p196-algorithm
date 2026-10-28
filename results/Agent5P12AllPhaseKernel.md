# Agent5P12AllPhaseKernel

**PAPER PROOF.** Complete single-symmetric-site response kernel for the
published decimal p=12, m=9 lattice, all 12 temporal phases, both input
length parities, and every sufficiently interior site (any band length).
With a common unchanged exterior and overflow, a changed coefficient
is invisible after one reverse-and-add pair-word step exactly at:
phase 0 residues 0..6,8; phase 4 residues 0..3,5..8;
phase 8 residues 0,2..8; no residues in the nine non-overflow phases.
The unique replacement at each allowed residue is the ±9 value in
`reports/Agent5P12AllPhaseKernel.md`. Carry reset and two local equations
prove completeness; a finite 12x9x19 enumeration checks the arithmetic.
Scope: single symmetric coefficient change in the interior, not arbitrary
centres, any-period no-go, a decimal Lychrel certificate, or the orbit 196.
Reproduce: `python3 calculation/decimal_frontier/lattice_kinks/code/classify_all_phase.py`.