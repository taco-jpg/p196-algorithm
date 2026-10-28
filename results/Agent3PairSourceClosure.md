# Agent3PairSourceClosure

**PAPER PROOF.** Exact correlated-carry two-step midpoint-source alphabets
for decimal p=8, spatial-period-48 rec2: 10 residues for even-start pairs,
20 for odd-start pairs. Their relaxed mod-99 closure has 99 or 90 residues
after two pairs, depending on the final pair parity, for all periods 192k.
For every returned bounded centre separated from the rec2 exterior, initial
length `n0=400+o+96r`, `o=1,3`, its initial centre-defect weighted charge
`D0=sum 10^i(P0[i]-F0[i]) mod 11` **cannot equal 8**, regardless of width.
The other residues and `o=0,2` remain UNDECIDED; no centre or Lychrel
certificate is established. This is not a finite-width SAT exclusion.
Proof: `reports/Agent3PairSourceClosure.md`.
Reproduce: `python3 calculation/decimal_frontier/lattice_kinks/code/agent3_pair_source_closure.py calculation/decimal_frontier/lattice_kinks/data/lat2.txt`.
Checks: all 48 cuts, 192/384/576 steps, 1,600 physical centre transitions.
