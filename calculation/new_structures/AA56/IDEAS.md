# AA56 negative ideas and route changes

## Four fixed seams do not close at 360 steps; mismatch is boundary-local
Candidate seeds from the R30 regression set, each tested against target k -> k+15 after 360 ordinary decimal reverse-and-add steps:

- J=[5], U=[9,14,4], C=[10]: mismatch index 9q-32.
- J=[6,4], U=[9,2,16], C=[12]: mismatch index 9q-36.
- J=[1,8,2], U=[9,0,18], C=[4,8,4]: mismatch index 9q-34.
- J=[5], U=[14,4,9], C=[10]: mismatch index 9q-33.

44 exact big-integer replays at q in {20,40,80,160} and k in {max(20,q/2),q,2q} show the same mismatch formula across sampled independent k values. A further 36 signature checks over q,k in {40,80,160} show that the final 90 coefficients of the W-region are invariant across these sampled width pairs, while the central 21 coefficients depend on k but not on q in the tested range. Script: `python3 calculation/new_structures/AA56/replay_360.py`. These are COMPUTED at the listed widths only; no affine formula is proved uniformly.

W starts at index 34 and ends at 34+9q. The mismatch is 66, 70, 68, or 67 coefficients before the inner W cut, respectively. Therefore these tests do NOT rule out a moving seam or a seam extension with a finite boundary apron. The next meaningful step is to model the 90-coefficient apron jointly with the width-dependent centre and ask whether the 360-step state update has a cycle preserving the outer W9 copies while advancing the U3 exponent by 15.

Do not spend more work on the exact fixed-seam candidates. Do not generalize the failure to a no-go for moving seams, changing W profiles, or other primitive roots.
