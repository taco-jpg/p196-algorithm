# AA56 running log

- 2026-10-29: Registered initial moving-seam/two-W9 exchange premise, then withdrew it because it overlapped AA55.
- 2026-10-29: Registered the distinct 360/720-step moving-centre/glider premise.
- 2026-10-29: Read `docs/FOCUS_SWARM.md`, `OPEN_PROBLEMS.md`, `FORMATS.md`, and R30's exact pairword checker specification/source via raw repository reads.
- 2026-10-29: Built `replay_360.py`. It performs 44 genuine-integer mismatch replays for four documented R30 negative seam seeds at q in {20,40,80,160} and diagonal/off-diagonal k values {max(20,q/2),q,2q}. Every run has 90 overflows and the expected rooted clock prefix. For each seed, the first mismatch is affine in q and invariant across sampled k.
- 2026-10-29: Added 36 signature checks over q,k in {40,80,160}. For each seed, the last 90 W-region coefficients are invariant across sampled width pairs; the central 21-coefficient window is independent of q at fixed k but varies with k.
- 2026-10-29: Derived a candidate 360-step output family for J=[5], U=(9,14,4), C=[10]: q -> q-8, k -> k-90, U rotates to (4,9,14), |J'|=252, |C'|=273. The candidate J'/C' words were discovered from one concrete seed, checked against independent concrete widths, and the complete 360-step transition was verified with the R30 symbolic pairword checker for all independent q,k >= 2048. Every phase has an odd pair coefficient and the overflow clock is exactly (1000)^90. See `check_epoch1_symbolic.py` and `results/AA56_Epoch1BoundaryTransition.md`.
- 2026-10-29: The transition is not self-reproducing: q and k decrease. Concrete second/third epoch experiments also show changing width-loss/growth increments; no closed cycle or all-time certificate is known.
- Status remains PARTIAL: the missing step is a provable repair/cycle that prevents cumulative W9 and U3 erosion.
