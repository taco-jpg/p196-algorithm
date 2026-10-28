# Agent2K1Rec2StationaryT16
**COMPUTED.** Base 10, overflow `10101010` (p=8), rec2 lattice
(spatial m=48): no stationary first-defect column with a temporal
period T=16 at any of the 48 spatial departure phases.
Exact search: 1,317,912 reachable states, 1,269,072 distinct edges,
no cycles or caps (2,000,000-state cap per phase).
Independent bit-packed C++ transfer and Python tuple-state BFS +
topological cycle elimination agree; 48 lattice controls pass.
Reproduce: `sh calculation/decimal_frontier/lattice_kinks/code/rec2_t16_run.sh`.
Code: `calculation/decimal_frontier/lattice_kinks/code/rec2_t16_transfer.cpp`,
`rec2_t16_checker.py`, `rec2_t16_run.sh`. Compact input:
`calculation/decimal_frontier/lattice_kinks/data/rec2_t8_rows.txt`,
cross-checked against original `data/lat2.txt`.
Not claimed: T>=24, moving fronts, decimal certificate, or 196.
