# AA56 negative ideas and route changes

## Fixed seams do not close at 360 steps; mismatch is boundary-local, not bulk-wide
Candidate seeds from the R30 regression set, each tested against target k -> k+15 after 360 ordinary decimal reverse-and-add steps:

- J=[5], U=[9,14,4], C=[10]: mismatch indices 148, 328, 688, 1408 for q=k=20,40,80,160 (=9q-32).
- J=[6,4], U=[9,2,16], C=[12]: mismatch indices 144, 324, 684, 1404 (=9q-36).
- J=[1,8,2], U=[9,0,18], C=[4,8,4]: mismatch indices 146, 326, 686, 1406 (=9q-34).
- J=[5], U=[14,4,9], C=[10]: mismatch indices 147, 327, 687, 1407 (=9q-33).

All 16 exact big-integer replays have overflow sum 90 and the expected rooted clock prefix. Script: `python3 calculation/new_structures/AA56/replay_360.py`. These are COMPUTED at the listed widths only; the affine mismatch formulas are not proved uniformly.

Correction to the first interpretation: W starts at index 34 and ends at 34+9q. The mismatch is a fixed distance 66, 70, 68, or 67 coefficients before the inner W cut, not a defect deep in the band. Therefore these tests do NOT rule out a moving seam or a seam extension with a finite boundary apron. The next meaningful step is to model the finite boundary state explicitly and ask whether its 360-step update has a cycle that preserves the outer W9 copies while advancing the U3 exponent by 15.

Do not spend more work on the exact *fixed-seam* candidates. Do not generalize the failure to a no-go for moving seams, changing W profiles, or other primitive roots.
