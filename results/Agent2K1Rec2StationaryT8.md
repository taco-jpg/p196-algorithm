# Agent2K1Rec2StationaryT8
**COMPUTED.** In base 10 for the period-8 overflow word `10101010`, the
spatial-period-48 rec2 lattice admits no stationary first-defect column with
a temporally period-8 infinite right-side bulk continuation, at any of 48
departure phases. The finite cut-state graph (8 ascending bits, 8 descending
bits, four descending digits) is exhausted after 2,852 reachable states and
1,624 distinct directed edges, with no reachable directed cycles or caps.
The C++ search and independently encoded tuple-Python checker agree for all
48 phases; the unperturbed rec2 lattice passes all 48 positive controls.
Reproduce: `sh calculation/decimal_frontier/lattice_kinks/code/rec2_t8_run.sh`.
Sources: `calculation/decimal_frontier/lattice_kinks/code/rec2_t8_transfer.cpp`,
`rec2_t8_checker.py`, `rec2_t8_run.sh`, and `data/rec2_t8_rows.txt`.
The original `data/lat2.txt` is independently cross-checked on each run.
**Not claimed:** longer time periods, moving defects, any finite centre,
a decimal certificate, or anything specific about 196.
