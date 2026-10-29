# AA56 negative ideas and route changes

## Fixed seams do not close at 360 steps; mismatch is boundary-local
Four R30 regression seeds fail the fixed-seam target k -> k+15 after 360 steps. See `replay_360.py` for 44 genuine-integer checks and 36 signature checks. Their first mismatch indices are 9q-32, 9q-36, 9q-34, and 9q-33. The mismatch is 66,70,68,67 coefficients before the inner W cut, respectively, so this is a finite-apron defect, not a no-go for moving seams.

## Universal one-epoch map found, but it consumes the defect budget
For J=[5], U=(9,14,4), C=[10], the symbolic checker verifies a 360-step transition for every independent q,k >= 2048:
- q' = q-8;
- k' = k-90;
- U' = (4,9,14);
- |J'|=252 and |C'|=273, with fixed finite words J',C';
- overflow clock (1000)^90 and an odd pair-coefficient guard at all 360 phases.

Reproduction: `python3 calculation/new_structures/AA56/check_epoch1_symbolic.py`. Full scope and caveats are in `results/AA56_Epoch1BoundaryTransition.md`.

This is an exact universal edge, but not an all-time certificate: it spends eight W9 copies and ninety U3 copies each macro-cycle. Concrete later epochs show the state-growth increments change. The remaining missing lemma is a repair/cycle that returns the consumed outer-band budget, or a proof that this route cannot do so.
