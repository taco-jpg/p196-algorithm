# Agent14ChargeSaturation
**PAPER PROOF.** For the two reachable base-10 p8/m20 lattices rec0/rec1, all three necessary centre congruences mod 3, 9 and 11 for an even-to-odd complemented 18-step half-return and ordinary 80-step return are jointly satisfiable at every sufficiently long length and every centre half-width w>=3.
Three legal coefficients (u,v,2r) constructively attain all 297 residue triples. These charges alone cannot exclude such a centre at any width w>=3.
Scope: modular feasibility only, not actual reverse-and-add transitions, a finite centre, other invariants, a decimal Lychrel certificate or 196.
Proof: `reports/Agent14ChargeSaturation.md`.
Code and independent exhaustive checker: `calculation/decimal_frontier/lattice_kinks/code/agent14_charge_saturation.py`, `agent14_charge_saturation_independent.cpp` (same directory).
Reproduce: `python3 calculation/decimal_frontier/lattice_kinks/code/agent14_charge_saturation.py`; `g++ -O2 -std=c++17 calculation/decimal_frontier/lattice_kinks/code/agent14_charge_saturation_independent.cpp -o /tmp/p196_agent14_charge && /tmp/p196_agent14_charge`.
Controls: 297/297 residue classes (uncapped), 1,280 direct rec0/rec1 pairword cases, independent enumeration of 3,610 triples.
