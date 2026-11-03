# Rounds 6-8 tools (Studio, 2026-10-31 .. 2026-11-01)

Sources behind `results/ReachDiskRounds6to8.md` / `reports/ReachDiskRounds6to8.md`. Same graph as `../reach.cpp` / `../reachmt.cpp`
(see `../README.md`); these versions keep the visited set on disk and add backward cones and the window filter.

| file | what |
|---|---|
| `bands/reachdisk.cpp` | round 6: external-memory forward BFS (reachmt with on-disk visited set, resumable manifest). Design: `design/DESIGN_R6.md` |
| `bands/backdisk.cpp` | round 7: backward cone from target keys through predecessors, same keys / ROT quotient. Design: `design/DESIGN_R7.md` |
| `bands/window.cpp` | round 7: window abstraction (sound over-approximation for every T on a clock word). Proof and checks: `design/FILTER_R8.md` |
| `r8/backdisk.cpp`, `r8/reachdisk_wc.cpp` | round 8 versions (window filter inside the cone, `WIN=w`; forward run with window check) |
| `r8/reach_w.cpp` | single-thread reach with parent pointers, WIRE mode (left-end reconstruction) |
| `r8/verify_ext.py`, `r8/equiv.py`, `r8/brute_r8.py` | premise (B): reach left ends vs the Agent120 exterior system (`calculation/neutral_band_search.py`); `design/EQUIV_R8.md` |
| `r8/m8dump.cpp`, `r8/a10m.cpp` | chain 6 (clock (01)^8, m = 8 cycles) and the Agent10 E2 cone with its controls |
| `r6/run_r6.py`, `r7/run_r7.py`, `r7/*.sh`, `r7/specs.py` | queue runners and target specs as run on the Studio (paths assume `~/p196_run`) |

Build: `c++ -O3 -std=c++17 -pthread X.cpp -o X` (`r8/a10m.cpp` includes `<bits/stdc++.h>`, so it needs g++). Positive controls are listed in each design note and in the report.
