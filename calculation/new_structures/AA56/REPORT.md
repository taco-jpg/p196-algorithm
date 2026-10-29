# AA56 report

Status: PARTIAL. Six successive universal 360-step epoch-map edges are symbolically checked; no closed cycle or all-time lemma is established.

## Exact transition chain
The initial rooted p12/m9 pairword has J=[5], U=(9,14,4), C=[10]. For each epoch n=1..6, the symbolic checker verifies a 360-step edge for all independent q,k >= 2048:
- q' = q - 8;
- k' = k - (89+n), i.e. losses 90 through 95;
- output U' = (4,9,14);
- output seam lengths 252, 504, 756, 1008, 1260, 1512;
- output palindromic centre lengths 273, 549, 831, 1119, 1413, 1713.

The checked lengths follow |J_n|=252n and |C_n|=3n²+267n+3 for n=1..6. Each fixed output seam/centre is discovered from a concrete orbit, then the R30 symbolic pairword checker verifies the full 360-step equality for all widths. Every edge has exact overflow clock `(1000)^90`, total overflow 90, and an odd pair-coefficient witness at every one of the 360 intermediate phases. This is a universal width-parametric edge, not a finite-width extrapolation.

Reproduce with `python3 calculation/new_structures/AA56/check_epoch_chain_symbolic.py`. The exact scope and limitations are in `results/AA56_Epoch1BoundaryTransition.md` (label COMPUTED).

## Why this does not solve the target
The edges consume 8 W9 copies and increasing numbers of U3 copies per 360-step epoch, while the seam and centre expand. Six edges do not prove the pattern for all epochs, and no repair or closed cycle has been found. This is useful state-map data, but it is not a decimal Lychrel certificate and must not be ALERTed as one.

## Earlier diagnostics
The companion `replay_360.py` contains 44 concrete big-integer mismatch replays for four fixed-seam seeds plus 36 boundary/centre signature checks.
