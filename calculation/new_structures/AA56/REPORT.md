# AA56 report

Status: PARTIAL. A universal one-epoch transition is now symbolically checked; no closed cycle or all-time lemma is established.

## Exact transition discovered
The source family is the rooted p12/m9 pairword with J=[5], U=(9,14,4), C=[10]. The 360-step epoch does not return to the same template. It maps to a new family with:
- q' = q - 8;
- k' = k - 90;
- U' = (4,9,14);
- a fixed output seam J' of length 252;
- a fixed palindromic output centre C' of length 273.

The output template is constructed from one concrete seed only to discover the finite words J' and C'. The script then uses the R30 symbolic pairword checker to verify the full 360-step equality for all independent q,k >= 2048. It also checks the exact overflow clock `(1000)^90`, total overflow 90, and an odd pair-coefficient witness at every one of the 360 intermediate phases. This is a universal width-parametric edge, not a finite-width extrapolation.

Reproduce with `python3 calculation/new_structures/AA56/check_epoch1_symbolic.py`. The result is recorded in `results/AA56_Epoch1BoundaryTransition.md` (label COMPUTED).

## Why this does not solve the target
The edge consumes 8 W9 copies and 90 U3 copies per 360-step epoch, while the seam and centre expand. The second and third transitions also show changing width-loss/growth increments, so no invariant or cycle has been proved. This is useful state-map data, but it is not a decimal Lychrel certificate and must not be ALERTed as one.

## Earlier diagnostics
The companion `replay_360.py` contains 44 concrete big-integer mismatch replays for four documented fixed-seam seeds plus 36 boundary/centre signature checks. These identify a finite boundary apron and a centre state that depends on k. See `IDEAS.md` for the scoped negative interpretation.
