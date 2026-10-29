# Agent5P12StrictContiguousNoErase

**PAPER PROOF.** In decimal p=12, spatial-m=9 lattice with overflow
`100010001000`, no time phase with gamma=0 (t=1,2,3,5,6,7,9,10,11)
admits a **strictly contiguous** nonempty lower-half bulk interval in
which EVERY symmetric coefficient pair is changed (0..18) and the
complete one-step reverse-and-add successor pair word is unchanged.
All nine spatial residues and all widths have zero accepting paths
in the exhaustive 36-state carry graph; positive collisions requiring an
unchanged internal site remain possible. Both input parities tested.
Reproduce (Python3 stdlib, no cap):
`python3 calculation/decimal_frontier/lattice_kinks/strict_contiguous_gamma0/run_checks.py`
Source, lattice snapshot, 81-root counts, independent checker:
`calculation/decimal_frontier/lattice_kinks/strict_contiguous_gamma0/`.
No K1 centre nonexistence, multistep no-go, decimal certificate or 196 claim.
