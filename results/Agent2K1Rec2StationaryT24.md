# Agent2K1Rec2StationaryT24
**COMPUTED.** In base 10, period-8 overflow `10101010`, rec2 lattice
(spatial m=48): no stationary first-defect column with temporal period
T=24 at any of the 48 possible spatial departure phases.
Full 96-bit cut-state DFS (cap 3,000,000 states/phase): all 48 decided,
10,393,040 reachable states, 8,273,248 enumerated edges, zero cycles.
Independent C++ Kahn elimination after exact time-shift-8 quotient:
3,466,248 states, 2,758,832 distinct edges, zero cyclic cores.
Python carry arithmetic checks all 48 lattice positive controls.
Reproduce from root: `sh calculation/decimal_frontier/lattice_kinks/code/rec2_t24_run.sh`.
Sources: `calculation/decimal_frontier/lattice_kinks/code/rec2_t24_raw.cpp`,
`rec2_t24_kahn.cpp`, `rec2_t24_controls.py`, `rec2_t24_run.sh`;
input `calculation/decimal_frontier/lattice_kinks/data/rec2_t24_rows.txt`
(checked against existing `data/lat2.txt`).
Not claimed: temporal periods >=32, moving fronts, a certificate, or 196.
