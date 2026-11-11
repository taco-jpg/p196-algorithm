# Main-session independent check of r13b, and the p12m9 budget-frame closure

Programs written by the main session from the definitions (depth, fold map F_K, relaxation R_K of the round-12 K1 setting);
no code shared with r13b's kcommon.h / indep_acc.cpp or with klib.py. Run on the Studio on 2026-11-08 / 2026-11-09; the
scripts use the run-machine paths `~/p196_run/...` (and `~/p196_repo` = a checkout of this repository).

| file | what |
|---|---|
| `mklat13.py`, `mklat_p12.py` | lattice files `lat/*.txt` built directly from `lattice_formats/p8_scc.txt` and `lattice_kinks/data/lat_p12m9.txt` |
| `mc13b.cpp` | `mc13b selftest LAT SEED COUNT` (genuine big-number addition vs F_K and R_K); `mc13b run LAT ORBIT KMAX THREADS` = E_acc(K, Lo) level by level, exact fold check inside |
| `mc13c.cpp` | adds `runscc LAT ORBIT KMAX THREADS PRINT`: all-period version (states on cycles through an accepting state, Tarjan), exact periodic orbits listed |
| `mc13d.cpp` | budget frame: the window may shift by one column, two shifts at least B steps apart (contains every schedule of drift 0 <= d <= 1/B); `mc13d LAT B KMAX THREADS [zero]`; `mc13d LAT B selftest SEED COUNT` |
| `pybudget.py` | independent plain-Python budget closure (explicit carries down to column 0, own Tarjan) |
| `pyscc.py`, `depth0.py` | Python all-period closure for small K; depth-0 test by genuine big-number addition |
| `compare13.py` | level-by-level comparison of `logs/*_o*.log` with r13b's `../logs/acc_*.log` (output `compare13.out`) |
| `first.sh`, `drive1.sh` .. `drive7.sh` | the exact commands that produced `logs/` and `drive*.out` |

## Results reproduced (logs/)

* rec0, rec1, all four phase orbits, T = 80: E_acc(44,80) = 709 (6 accepting), EMPTY at K = 45, 0 exact orbits at every K
  (`logs/rec{0,1}_o{0..3}.log`). rec2, T = 192, all four orbits computed directly: EMPTY at K = 40 (orbits 0, 2) and K = 41
  (orbits 1, 3) (`logs/rec2_o*.log`). `compare13.out`: 0 differences in (E_acc, accepting, parents kept, exact orbits) at every level.
* Depth 0: `logs/depth0_bigint.out` (no phase orbit maps the all-lattice word to itself all the way round; rec0, rec1, rec2, p12m9).
* Selftests: `drive3.out`, `drive6.out` (PASS).

## p12m9 budget frame (new, main session)

Lattice B0/W9 (clock 100010001000, m = 9; the centre moves at speed 1/8). `drive5.out`, `logs/p12m9_budget8.log`, `logs/p12m9_zero.log`:
the budget-8 closure (frame shifts at least 8 steps apart, i.e. every drift 0 <= d <= 1/8, including the centre speed) and the
drift-0 closure (no shifts) have IDENTICAL sizes at every K = 7..14 (K = 7: 143,100; K = 14: 127,210,896), while they differ at
K <= 6 (K = 6: 811,920 vs 56,847). Python (`logs/py_budget8_p12m9.log`, `logs/py_zero_p12m9.log`) agrees exactly for K = 1..7.
Reading: the drift-0 sets are subsets of the budget sets (fewer edges, nested parents), so equal sizes mean equal sets; a cycle
using a shift passes through a state with wait counter beta = 7 > 0, which no drift-0 cycle has. Hence for K >= 7 no closed walk
through an accepting state uses a shift (for K > 7 by projection to the bottom 7 cells). So a defect boundary of p12m9 whose
frame advances at least once per period with gaps >= 8 steps cannot lie 7 or more cells below the middle; only stationary
frames (d = 0) survive, and those sets keep growing (UNDECIDED; mc13d stops at K = 15 by its candidate cap).
Control: base 9 (b9r0, budget 5) does not die (`drive5.out`). The p8 lattices (rec0, rec2, budget 5) do not close by K = 8 (`logs/rec*_budget5.log`; no statement).
Reproduce: `sh drive5.sh` (about 5 min, 8 threads), `sh drive6.sh` (Python, about 3 min).
