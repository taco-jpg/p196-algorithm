# AgentS12EvenCentreCarrySourceDelta
**PAPER PROOF.** For every fixed rooted prefix/suffix, even palindromic centre, and charge-zero U3 motif, the exact mod-101 physical carry source changes by the formula in calculation/new_structures/S12/NOTES.md under k→k+5.
The proof uses carry reset on U and reverse(U), together with (-10)^4=1 mod 101; it is uniform for all q and k≥1.
The induced two-epoch checksum condition is stated in NOTES.md and can be used as a phase-interface constraint for the epoch-map search.
Reproducible controls: epoch_delta.cpp (compiled carry scan) and epoch_delta.py (independent native-bigint reverse-add).
Both check 2,400 cases: 30 U motifs, four even-centre collars, and 20 (q,k) pairs including q,k=20,40,80,160.
**Scope:** exact carry-source identity and necessary checksum only; no full 120/240-step seam return, universal no-go, or decimal Lychrel certificate.