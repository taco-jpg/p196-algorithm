# AA56 running log

- 2026-10-29: Registered initial moving-seam/two-W9 exchange premise, then withdrew it because it overlapped AA55.
- 2026-10-29: Registered the distinct 360/720-step moving-centre/glider premise.
- 2026-10-29: Read `docs/FOCUS_SWARM.md`, `OPEN_PROBLEMS.md`, `FORMATS.md`, and R30's exact pairword checker specification/source via raw repository reads. Core authenticated file reads were initially rate-limited, but raw source reads succeeded.
- 2026-10-29: Implemented an independent Python big-integer replay for four R30 documented negative seam seeds. At q=k=20,40,80,160, all 360-step trials produce 90 overflows with the rooted clock prefix, but do not return to the fixed-seam target with k increased by 15. Mismatch sequences: 148,328,688,1408; 144,324,684,1404; 146,326,686,1406; 147,327,687,1407. Reproducible script: `replay_360.py`.
- 2026-10-29: Corrected initial interpretation: W occupies indices [34,34+9q), so these mismatch indices lie 66,70,68,67 coefficients before the inner W cut, respectively. This is a fixed-offset boundary defect, not a defect deep in the W bulk. It motivates a finite-apron seam/glider state model and does not rule out moving seams.
- Status remains PARTIAL: no uniform affine mismatch theorem, seam-cycle model, or all-time certificate.
