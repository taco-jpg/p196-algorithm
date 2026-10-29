# AA56 running log

- 2026-10-29: Registered initial moving-seam/two-W9 exchange premise, then immediately withdrew it because it overlapped AA55.
- 2026-10-29: Registered the distinct 360/720-step moving-centre/glider premise.
- 2026-10-29: Read `docs/FOCUS_SWARM.md`, `OPEN_PROBLEMS.md`, `FORMATS.md`, and R30's exact pairword checker specification/source via raw repository reads. Core authenticated file reads were rate-limited, but raw source reads succeeded.
- 2026-10-29: Implemented an independent Python big-integer replay for the R30 documented negative seam J=[5], U=[9,14,4], C=[10]. At q=k=20,40,80,160, 360 steps produce 90 overflows with the expected clock prefix, but do not return to the fixed-seam target with k increased by 15. First pairword mismatch indices are 148, 328, 688, 1408 (=9q-32). These are finite checks only, not an all-width theorem and not an ALERT.
- Interpretation: for this particular fixed seam, a centre-only/glider repair cannot fix the observed mismatch if its physical support remains interior to J/C: the first mismatch lies in the W9-sized repeated region before J. This is a scoped diagnostic, not a general no-go for moving seams.
