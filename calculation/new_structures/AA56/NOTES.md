# AA56 running log

- 2026-10-29: Registered initial moving-seam/two-W9 exchange premise, then withdrew it because it overlapped AA55.
- 2026-10-29: Registered the distinct 360/720-step moving-centre/glider premise.
- 2026-10-29: Read `docs/FOCUS_SWARM.md`, `OPEN_PROBLEMS.md`, `FORMATS.md`, and R30's exact pairword checker specification/source via raw repository reads. Core authenticated file reads were initially rate-limited, but raw source reads succeeded.
- 2026-10-29: Built `replay_360.py`. It performs 44 genuine-integer mismatch replays for four documented R30 negative seam seeds at q in {20,40,80,160} and diagonal/off-diagonal k values {max(20,q/2),q,2q}. Every run has 90 overflows and the expected rooted clock prefix. For each seed, the first mismatch is affine in q and invariant across the sampled independent k values.
- 2026-10-29: Added 36 signature checks over q,k in {40,80,160}. For each seed, the last 90 coefficients of the W-region are identical across all sampled width pairs; the central 21-coefficient window is independent of q at each fixed sampled k, but varies with k.
- 2026-10-29: Mismatch indices are 66,70,68,67 coefficients before the inner W cut, respectively. This is a fixed-offset boundary defect, not a defect deep in the W bulk. It motivates a finite-apron seam state coupled to a width-dependent centre.
- Status remains PARTIAL: no uniform affine mismatch theorem, seam-cycle model, or all-time certificate.
