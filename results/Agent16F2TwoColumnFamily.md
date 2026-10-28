# Agent16F2TwoColumnFamily

**PAPER PROOF.** For every integer `r>=1` and base `b=2^(r+1)`, the
canonical-root position automaton for overflow word `g_r=1 0^r 11 0^(r+1)`
has at least **four distinct paths of exactly two spatial transitions**.
Both transitions are time-closed at temporal period `2r+4`.
The four paths are given explicitly, with arbitrary parameters
`mode,free in {0,1}` and no state-search cap.

This is an infinite family of **two-column prefixes**, not a reachable
periodic exterior SCC, a complete band or Lychrel certificate,
or a conclusion about base 10 or the seed 196.
Proof and formulas: `reports/Agent16F2TwoColumnFamily.md`.
Replay controls: `python3 calculation/decimal_frontier/lattice_formats/code/agent16_two_column_family.py`.
