# Round 10 (Studio, 2026-11-03): clock 01 at T = 24 and T = 32

Same method as `../round9/last_cell` (forward BFS pruned by co-reachability windows BB_w, wrapped windows included), targets = every
uniform band with period dividing T and every 9-wire stream.
- (24, 01), w = 10: COMPLETE, frontier empty after height 3350, 500,036,674 orbits, 0 bands, 0 wire streams (`logs/fwdB10_T24_01.log`).
  Independent w = 9 cross-check (finished 2026-11-03): frontier empty after height 3350, 795,389,414 orbits, 0 of 10 band targets,
  0 streams, 31,291 s, max RSS 7.49 GB (`logs/fwdB9_T24_01_single.log`).
- (32, 01), w = 10: stopped by hand at height 260 (568,042,999 orbits, about 4e6 new per height, not shrinking): UNDECIDED.
- Controls, same binary: (12, 0001) and (24, 0001) N12 at height 53, COMPLETE; (16, 01) COMPLETE, no band; window check 0 violations on
  2.1e9 successors; `pathcheck` on small full graphs (bases 2, 6, 8): no on-path state outside BB_w.
Build: `c++ -O3 -std=c++17 -pthread reachdisk_wc_r10.cpp -o reachdisk_wc_r10` (same for bwin, wbuild, pathcheck).
