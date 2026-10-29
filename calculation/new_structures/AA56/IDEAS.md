# AA56 negative ideas and route changes

## Fixed seams do not close at 360 steps; mismatch is boundary-local
Four fixed-seam seeds fail the fixed-seam target after 360 steps. See `replay_360.py` for 44 genuine-integer mismatch replays and 36 signature checks. The mismatch is a fixed offset before the inner W cut, so this is a finite-apron defect, not a no-go for moving seams.

## Five universal epoch edges found, but they consume the defect budget
For the rooted p12/m9 family starting J=[5], U=(9,14,4), C=[10], `check_epoch_chain_symbolic.py` verifies five successive 360-step transitions for all independent q,k >= 2048. Every edge has q -> q-8, while k loses 90,91,92,93,94. The output seam lengths are 252,504,756,1008,1260; centre lengths are 273,549,831,1119,1413; U settles to rotation (4,9,14). Each edge has exact overflow clock (1000)^90 and odd pair-coefficient guards at all phases.

The output seams begin with 0,1,1,2,2 complete copies of W across edges 1..5. Even if those prefix copies are reclassified back into the W exponent, the effective q changes over the five edges are still -8,-7,-8,-7,-8. This is a finite observed pattern, not an all-n theorem, but it confirms that this candidate chain has no immediate W9 budget refund.

This is an exact state-map chain, not a certificate. The outer W9 budget decreases along the five checked edges, and five edges do not prove the pattern for all epochs. The missing result is either a provable repair/cycle restoring W9 copies or a proof that no such repair exists for this family.
