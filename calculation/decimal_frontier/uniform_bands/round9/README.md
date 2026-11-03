# Round 9 (Studio, 2026-11-02)

- `last_cell/`: the T = 32 clock 0000111000110001 cell, closed by a forward BFS pruned with co-reachability windows BB_w
  (window contents from which a target window is abstractly reachable inside A_w). Proof, controls and sizes: `last_cell/FINAL_R9U.md`.
  Also adds wrapped windows (across t = T-1 -> 0) with an exhaustive 0-violation check; round 8 never used them.
- `chain1/`: backward cones for chain 1 at P = 72, 88, 96 (all UNDECIDED: >2.9e9 states by layer 5-11, and the N12 control is not
  recovered at T = 72 either, so the method does not scale), plus `ktail.cpp` (all-period minimum exterior heights for the Agent6 ports:
  >= 18, >= 19 for alignment 1, >= 16 for the period-16 port). Details: `chain1/FINAL_R9.md`. P = 88 is closed by
  `results/Clock0001ThreeDividesR.md` anyway.
