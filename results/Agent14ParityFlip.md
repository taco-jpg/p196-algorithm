# Agent14ParityFlip
**PAPER PROOF.** Complete parity-changing physically aligned coefficient-complement classification of the four stored reachable decimal non-self-mirror absorbing lattices. For period-8 m20 rec0/rec1, only even-start d=18 mod80 and odd-start d=62 mod80 work for all overflow phases; rec2/m48 and p12/m9 have none.
The steady carries complement at the same glides. The two-stage complementary return takes at least 18+62=80 steps; a shortened 18-step centre certificate does not follow.
Scope: exact necessary exterior condition for arbitrary finite centre width, not a finite-centre existence/no-go, a decimal Lychrel certificate or a conclusion about 196. Complete finite proof, no state caps.
Proof: `reports/Agent14ParityFlip.md`.
Full reproducible source: `calculation/decimal_frontier/lattice_kinks/code/agent14_parity_flip.py` plus independent checker `agent14_parity_flip_independent.cpp` in that directory.
Commands: `python3 calculation/decimal_frontier/lattice_kinks/code/agent14_parity_flip.py`; `g++ -O2 -std=c++17 calculation/decimal_frontier/lattice_kinks/code/agent14_parity_flip_independent.cpp -o /tmp/p196_agent14_independent && /tmp/p196_agent14_independent`.
