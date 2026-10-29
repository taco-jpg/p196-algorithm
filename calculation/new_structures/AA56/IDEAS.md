# AA56 negative ideas and route changes

## Four documented fixed seams do not close at 360 steps
Candidate seeds from the R30 regression set, each tested against target k -> k+15 after 360 ordinary decimal reverse-and-add steps:

- J=[5], U=[9,14,4], C=[10]: mismatch indices 148, 328, 688, 1408 for q=k=20,40,80,160 (=9q-32).
- J=[6,4], U=[9,2,16], C=[12]: mismatch indices 144, 324, 684, 1404 (=9q-36).
- J=[1,8,2], U=[9,0,18], C=[4,8,4]: mismatch indices 146, 326, 686, 1406 (=9q-34).
- J=[5], U=[14,4,9], C=[10]: mismatch indices 147, 327, 687, 1407 (=9q-33).

All 16 exact big-integer replays have overflow sum 90 and the expected rooted clock prefix. Script: `python3 calculation/new_structures/AA56/replay_360.py`. These are COMPUTED at the listed widths only; the affine mismatch formulas are not proved uniformly.

Route implication: for these fixed-seam candidates, a glider confined to the interior seam/centre cannot repair a mismatch located in the repeated W9 region. Do not spend more work on these exact candidates under a 360-step macro. This does not rule out a genuinely moving seam that changes the W9 phase/profile or another primitive root.
