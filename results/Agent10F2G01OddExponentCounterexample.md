# Agent10F2G01OddExponentCounterexample
**COMPUTED.** The proposed family "all bases b=2^(2k+1) admit a g=01
neutral exterior" is false: exact canonical-root position-automaton BFS
at b=2^17=131072 exhausts 14,977 states (max depth 3,744) with ZERO
accepting cuts, excluding every B-width for this one base and g=01.
A separate all-carry-class Python engine agrees with the existing
O(b) C++ solver and reproduces positive b=2^13 (31,811 states, width
1,450), b=2^15 (131,072, width 4,441), b=2^19 (2,097,152, width
501,157); b=2^17 is a genuine counterexample, not monotone cutoff.
Proof/limits: `reports/Agent10F2G01OddExponentCounterexample.md`.
Reproduce: `python3 calculation/decimal_frontier/lattice_formats/code/agent10_g01_pow2_counterexample.py 13 15 17 19`.
Scope: period-two g=01 neutral exterior only; no other family, centre,
full Lychrel certificate, decimal 196 or Lean theorem is claimed.