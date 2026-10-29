# AA56 negative ideas and route changes

## Four fixed seams do not close at 360 steps; mismatch is boundary-local
Candidate seeds from the R30 regression set, each tested against target k -> k+15 after 360 ordinary decimal reverse-and-add steps:

- J=[5], U=[9,14,4], C=[10]: mismatch index 9q-32.
- J=[6,4], U=[9,2,16], C=[12]: mismatch index 9q-36.
- J=[1,8,2], U=[9,0,18], C=[4,8,4]: mismatch index 9q-34.
- J=[5], U=[14,4,9], C=[10]: mismatch index 9q-33.

For each seed, exact big-integer tests at q in {20,40,80,160} and k in {max(20,q/2),q,2q} give the same mismatch for all sampled k: 40 runs total. Each has overflow sum 90 and the expected rooted clock prefix. Script: `python3 calculation/new_structures/AA56/replay_360.py`. These are COMPUTED at the listed widths only; the affine formulas are not proved uniformly.

W starts at index 34 and ends at 34+9q. The mismatch is 66, 70, 68, or 67 coefficients before the inner W cut, respectively. Therefore these tests do NOT rule out a moving seam or a seam extension with a finite boundary apron. The next meaningful step is to model the finite boundary state explicitly and ask whether its 360-step update has a cycle that preserves the outer W9 copies while advancing the U3 exponent by 15.

Do not spend more work on the exact fixed-seam candidates. Do not generalize the failure to a no-go for moving seams, changing W profiles, or other primitive roots.
