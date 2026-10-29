# AA56 report

Status: PARTIAL (four documented seam seeds tested; no all-time lemma supplied).

## Question
Can a 360-step macro restore the phase-0 rooted p12/m9 template while allowing the centre to move, instead of demanding a fixed seam at each 120-step epoch?

## Reproducible test
Run `python3 calculation/new_structures/AA56/replay_360.py`. The script embeds the canonical phase-zero B and W rows from `calculation/decimal_frontier/lattice_kinks/data/lat_p12m9.txt`, constructs canonical integers from symmetric coefficient pairwords, performs 360 ordinary reverse-and-add steps, and compares the final folded pairword against fixed-seam target T(q,k+15). It checks four known seed triples (J,U,C) at q=k=20,40,80,160.

| case | J | U | C | first mismatch at q=20,40,80,160 |
|---:|---|---|---|---|
| 0 | [5] | [9,14,4] | [10] | 148, 328, 688, 1408 |
| 1 | [6,4] | [9,2,16] | [12] | 144, 324, 684, 1404 |
| 2 | [1,8,2] | [9,0,18] | [4,8,4] | 146, 326, 686, 1406 |
| 3 | [5] | [14,4,9] | [10] | 147, 327, 687, 1407 |

Each run has 90 overflows, begins with the rooted clock `(100010001000)^4`, and produces equal-length observed and target pairwords. The mismatch indices fit 9q plus a case-dependent constant in these samples. This is a finite computed observation, not a uniform affine formula or proof.

## Honest conclusion
None of these four fixed-seam seeds becomes a fixed-seam return merely by extending the macro to 360 steps. The first mismatch scales with the repeated W9 region and occurs before the interior seam. Thus a centre-only correction cannot fix these particular candidates. This does not rule out a genuinely moving seam that changes the W9 phase/profile or another primitive root. No certificate, general obstruction, or all-time result is claimed.
