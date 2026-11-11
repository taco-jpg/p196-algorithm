# P12M9SlowFrameDepth6

**Claim (COMPUTED; main session, 2026-11-09).** On the decimal p = 12 lattice B0/W9 (clock 100010001000, m = 9; the centre moves at
speed 1/8) a defect whose lower boundary advances towards the middle with drift 0 < d <= 1/8 (infinitely many one-column shifts, any
two at least 8 steps apart) cannot keep its boundary 7 or more columns below the middle: only a stationary boundary (d = 0) survives at depth >= 7.
- New relative to EdgeRelaxW9NoCentre (boundary moving exactly with the centre: dies at K = 6). Budget-8 relaxation: K-cell window above the
  boundary, lattice exact below, everything above free, one-column shifts with gaps >= 8 (contains every schedule of drift <= 1/8).
  Its accepting cyclic set (all periods, Tarjan) equals the drift-0 set at every K = 7..14 (K = 7: 143,100 states; K = 14: 127,210,896),
  while K = 6 differs (811,920 vs 56,847). A cycle with a shift visits a waiting state that no drift-0 cycle has, so no accepting closed
  walk shifts at K = 7, hence at no K >= 7 (projection to the bottom 7 cells).
Checks: independent plain-Python closure (explicit carries down to column 0, own Tarjan) equal for K = 1..7; genuine-addition selftest
400,000 cases PASS; base-9 control (budget 5) keeps its centres.
**Not claimed:** the stationary case d = 0 (accepting cyclic sets keep growing, K <= 14 computed: UNDECIDED); the p8 lattices (budget-5
closures do not close by K = 8); anything about 196.
Code: `calculation/decimal_frontier/round13/k1_fixed_period/main_check/` (mc13d.cpp, pybudget.py, drive5.sh, drive6.sh, README.md).
