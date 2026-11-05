# r11b: (32, 01) with wider windows — UNDECIDED

Goal: close the last capped word of the uniform-band census, clock (01)^16 at T = 32, using level families of
co-reachability windows (BB_w) wider than round 10's w = 10. Sources: `lvl*.cpp` (level-family window builder),
`reachdisk_r11b.cpp` (forward BFS with HWIN sparse level filter), `pathcheck_h.cpp`, `bwin.cpp`, `wbuild.cpp`, `win*.h`.
The agent driving this route stopped before writing a report; this README records the state from its logs.

- Validation (`val2.sh`, `val_small.sh`, `ctrl.sh`, `ctrl_p11.sh`; `logs/val2*.log`, `logs/ctrl*.log`): the HWIN filter at w = 9
  and 11 keeps the known streams (p11, N12 at (24, 0001)).
- w = 11 level family for B = 10, clock 01 (`logs/l11b_ph0.log`, `logs/l11b_ph1.log`): |BB'| / |A'| = 656,800,724 / 660,185,772
  (99.5 %) in phase 0 and 1,673,557,378 / 1,776,407,500 (94.2 %) in phase 1. So the w = 11 windows prune almost nothing.
- Forward BFS on (32, 01) with HWIN = 11 (`logs/f32_h11.log`): stopped at height 58 (13,403,333 orbits, still growing) when the
  run was interrupted; no target and no stream reached by then.

**Status: UNDECIDED.** Finite windows up to w = 11 do not separate (32, 01) from the bottom; see also
`../chain6_chain8/FINAL.md` (P96: BB_10 is target-independent).
