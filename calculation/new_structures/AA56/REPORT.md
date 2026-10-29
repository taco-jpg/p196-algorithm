# AA56 report

Status: PARTIAL (one documented seam tested; no all-time lemma supplied).

## Question
Can a 360-step macro restore the phase-0 rooted p12/m9 template while allowing the centre to move, instead of demanding a fixed seam at each 120-step epoch?

## Reproducible test
Fixture: B and W are the canonical phase-zero rows in `calculation/decimal_frontier/lattice_kinks/data/lat_p12m9.txt`; J=[5], U=[9,14,4], C=[10]. The test constructs the canonical decimal integer realizing the symmetric coefficient pairword, performs 360 ordinary integer reverse-and-add steps, then compares the final folded pairword with the fixed-seam target T(q,k+15).

| q | k | steps | overflow sum | first mismatch | expected 9q-32 |
|---:|---:|---:|---:|---:|---:|
| 20 | 20 | 360 | 90 | 148 | 148 |
| 40 | 40 | 360 | 90 | 328 | 328 |
| 80 | 80 | 360 | 90 | 688 | 688 |
| 160 | 160 | 360 | 90 | 1408 | 1408 |

All four comparisons are exact big-integer replays. The mismatch indices fit 9q-32, but this finite sample does not prove the formula for all q or k.

## Honest conclusion
The selected R30 negative seam does not become a fixed-seam return merely by extending the macro to 360 steps. Its first mismatch is at a position that scales with the W9 block, before the interior seam, so a centre-only correction is not enough for this candidate. This does not rule out a different moving seam, a different primitive root, or a phase-dependent W9 family. No certificate, general obstruction, or all-time result is claimed.
