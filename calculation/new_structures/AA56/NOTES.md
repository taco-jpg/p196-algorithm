# AA56 running log

- 2026-10-29: Registered initial moving-seam/two-W9 exchange premise, then withdrew it because it overlapped AA55.
- 2026-10-29: Registered the distinct 360/720-step moving-centre/glider premise.
- 2026-10-29: Read `docs/FOCUS_SWARM.md`, `OPEN_PROBLEMS.md`, `FORMATS.md`, and R30's exact pairword checker specification/source via raw repository reads.
- 2026-10-29: Built `replay_360.py`: 44 genuine-integer mismatch replays for four documented fixed-seam seeds plus 36 boundary/centre signature checks. The first mismatch is at a fixed offset before the inner W cut; the final 90 W-region coefficients are invariant across sampled widths, while the centre state depends on k.
- 2026-10-29: Built `check_epoch1_symbolic.py` and `check_epoch_chain_symbolic.py`. The chain script discovers finite seam/centre words from concrete seeds and symbolically verifies five successive 360-step transitions for all independent q,k >= 2048. q losses are 8 each; k losses are 90,91,92,93,94; seam lengths are 252,504,756,1008,1260; centre lengths are 273,549,831,1119,1413. Each edge has exact overflow clock (1000)^90 and an odd pair-coefficient guard at every phase.
- 2026-10-29: The five-edge chain is not self-reproducing: q and k decrease. It does not establish a pattern for all epochs or an all-time certificate. The missing step is a repair/cycle that prevents cumulative W9 and U3 erosion.
