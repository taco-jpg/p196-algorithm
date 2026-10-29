# AA56 report

Status: PARTIAL (four documented seam seeds tested; no all-time lemma supplied).

## Question
Can a 360-step macro restore the phase-0 rooted p12/m9 template while allowing a moving seam/centre family, rather than demanding a fixed seam at each 120-step epoch?

## Reproducible test
Run `python3 calculation/new_structures/AA56/replay_360.py`. The script embeds the canonical phase-zero B and W rows from `calculation/decimal_frontier/lattice_kinks/data/lat_p12m9.txt`, constructs canonical integers from symmetric coefficient pairwords, performs 360 ordinary reverse-and-add steps, and compares the final folded pairword against fixed-seam target T(q,k+15).

It performs 44 exact mismatch replays across four known seed triples at q in {20,40,80,160}, with diagonal/off-diagonal k values from {max(20,q/2),q,2q}. All give 90 overflows and first mismatch indices 9q-32, 9q-36, 9q-34, or 9q-33 for the respective seeds.

| case | J | U | C | first mismatch |
|---:|---|---|---|---|
| 0 | [5] | [9,14,4] | [10] | 9q-32 |
| 1 | [6,4] | [9,2,16] | [12] | 9q-36 |
| 2 | [1,8,2] | [9,0,18] | [4,8,4] | 9q-34 |
| 3 | [5] | [14,4,9] | [10] | 9q-33 |

The script additionally performs 36 signature checks for q,k in {40,80,160}. For each seed, the last 90 coefficients of the observed W-region are identical across all nine (q,k) pairs. The central 21-coefficient window is independent of q for each sampled k, but differs across sampled k values. These are finite computed observations, not uniform theorems.

## Boundary-state observation
W starts at coefficient index 34 and ends at 34+9q. The first mismatch lies a fixed distance from the inner end of W^q: 66, 70, 68, and 67 coefficients for cases 0–3. It is not a defect deep in the repeated band. A seam extension or moving boundary defect with a finite apron could absorb the mismatch, but exact closure must track the width-dependent centre too.

Next step: encode the 90-coefficient apron and centre state as an explicit epoch state, then derive and verify its 360-step transition. No certificate, general obstruction, or all-time result is claimed.
