# W11: bivariate four-corner decimal packet trajectory
- **COMPUTED:** base-10 initial word `88 0^(q2+delta) 3 0^q2 75` for every q2,delta>=11986 avoids palindromes at steps 0..20000.
- Every state has four exact polynomial packet corners in 1,10^q2,10^(q2+delta),10^(2q2+delta); its raw pairword has four disjoint finite zones.
- **PAPER PROOF:** exact reflection/merge recurrence and conservative integer dominance bound for every allowed parameter pair.
- At step 1 two middle packets synchronize exactly; equality of packets and offsets persists algebraically for all checked edges.
- Sample q2=delta=14000: separate digitwise and full GMP replay agree on all 20001 states; 21 paired hashes and full 10k/20k integers match, final 50259 digits.
- Computed sufficient bounds: packet/pairword (q2,delta)>=(11969,11953), nonpalindrome q2,delta>=11986.
- Sources: `calculation/new_structures/agent-W11/{four_corner_replay.cpp,independent_four_gmp.cpp,four_checkpoints.tsv}`.
- Derivation, exact commands, negative control: `reports/AgentW11FourCornerPolynomial.md`.
- **NOT CLAIMED:** a closed cycle, infinite Lychrel proof, Lean verification, or anything about 196.
