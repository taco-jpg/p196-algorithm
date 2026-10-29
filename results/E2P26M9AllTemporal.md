# E2P26M9AllTemporal

**COMPUTED.** Complete all-temporal-period census of the base-10, p=26 overflow stream `10010100010101001010001000`, among self-mirror absorbing bulk rows of primitive spatial period 9.
For each of nine reflection axes, all `19^5=2,476,099` palindromic rows were followed in the deterministic 26-step row-map functional graph: **22,284,891** vertices in total, with no state/time cap.
Every axis has one undefined neutral row, 25 recurrent cycles, and 17 primitive-spatial-9 recurrent cycles. Minimal temporal block-period counts over all axes are `k=1:18, 2:36, 4:18, 5:18, 6:9, 19:18, 24:18, 57:18`; there are no other periods.
Thus the primitive cycles have 2,106 axis-labelled recurrent starts, and the maximum checked row-map period is 57 blocks (1,482 reverse-add steps).
Every elementary transition was byte-compared between independent anchor-carry and cyclic fixed-point carry implementations; each representative cycle was then replayed through its complete period with the moving reflection axis and both carry constructions.
Reproduce: `g++ -O3 -std=c++17 calculation/decimal_frontier/lattice_formats/code/census_p26_m9_all_temporal.cpp -o /tmp/p26full`; run `/tmp/p26full --selftest`, then `/tmp/p26full /tmp/p26full.state /tmp/p26full.summary /tmp/p26full.cycles`.
The program checkpoints after each completed axis and rejects a result other than the stated exact per-axis graph signature.
Code: `calculation/decimal_frontier/lattice_formats/code/census_p26_m9_all_temporal.cpp`.
**Not claimed:** exterior/root reachability, an integer reverse-and-add orbit, non-self-mirror or non-period-9 bulk rows, a decimal certificate, or any conclusion about 196.
